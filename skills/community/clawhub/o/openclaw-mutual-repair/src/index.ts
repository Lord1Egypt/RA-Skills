/**
 * OpenClaw 双机互修助手
 * 
 * 功能：双机心跳监控、故障检测、自动修复
 * 作者：OpenClaw Skill Master
 * 版本：1.0.0
 */

import axios from 'axios';

// ==================== 配置 ====================

interface MutualRepairConfig {
  // 本机配置
  localHost: string;
  localPort: number;
  // 对端配置
  remoteHost: string;
  remotePort: number;
  // 心跳配置
  heartbeatInterval: number; // 毫秒，默认 5 分钟
  heartbeatTimeout: number;  // 毫秒，默认 30 秒
  // 告警配置
  memoryThreshold: number;   // 内存告警阈值，默认 85%
  cpuThreshold: number;      // CPU 告警阈值，默认 80%
}

// ==================== 心跳协议 ====================

interface HeartbeatRequest {
  type: 'heartbeat';
  timestamp: number;
  source: {
    host: string;
    port: number;
  };
  health: {
    status: 'ok' | 'warning' | 'critical';
    memory: number;
    cpu: number;
    uptime: number;
    connections: number;
  };
}

interface HeartbeatResponse {
  type: 'heartbeat_ack';
  timestamp: number;
  status: 'ok' | 'warning' | 'critical';
  message?: string;
}

interface RepairRequest {
  type: 'repair';
  timestamp: number;
  source: {
    host: string;
    port: number;
  };
  action: 'check' | 'restart' | 'diagnose';
  target?: string;
}

interface RepairResponse {
  type: 'repair_ack';
  timestamp: number;
  success: boolean;
  result?: any;
  error?: string;
}

// ==================== 健康检查 ====================

interface HealthStatus {
  status: 'ok' | 'warning' | 'critical';
  memory: {
    used: number;
    total: number;
    percent: number;
  };
  cpu: {
    percent: number;
  };
  uptime: number;
  connections: {
    websocket: number;
    http: number;
  };
  processes: {
    pm2?: {
      status: 'online' | 'stopped' | 'errored';
      memory: number;
      restarts: number;
    };
  };
}

async function checkSystemHealth(): Promise<HealthStatus> {
  const health: HealthStatus = {
    status: 'ok',
    memory: { used: 0, total: 0, percent: 0 },
    cpu: { percent: 0 },
    uptime: process.uptime(),
    connections: { websocket: 0, http: 0 },
    processes: {}
  };

  try {
    // 内存检查
    const memInfo = await execPromise('free -m');
    const memLines = memInfo.split('\n');
    const memTotal = parseInt(memLines[1].split(/\s+/)[1]);
    const memUsed = parseInt(memLines[1].split(/\s+/)[2]);
    health.memory.total = memTotal;
    health.memory.used = memUsed;
    health.memory.percent = Math.round((memUsed / memTotal) * 100);

    if (health.memory.percent > 85) {
      health.status = 'warning';
    }
    if (health.memory.percent > 95) {
      health.status = 'critical';
    }

    // CPU 检查
    const cpuInfo = await execPromise('top -bn1 | grep "Cpu(s)"');
    const cpuPercent = parseFloat(cpuInfo.split(',')[0].split(':')[1].trim());
    health.cpu.percent = cpuPercent;

    if (cpuPercent > 80) {
      health.status = health.status === 'critical' ? 'critical' : 'warning';
    }

    // PM2 进程检查
    try {
      const pm2Status = await execPromise('pm2 list --json');
      const processes = JSON.parse(pm2Status);
      const openclawProc = processes.find((p: any) => p.name === 'openclaw');
      
      if (openclawProc) {
        health.processes.pm2 = {
          status: openclawProc.status as 'online' | 'stopped' | 'errored',
          memory: openclawProc.monit.memory,
          restarts: openclawProc.pm2_env?.restart_time || 0
        };

        if (openclawProc.status !== 'online') {
          health.status = 'critical';
        }
        if ((openclawProc.pm2_env?.restart_time || 0) > 5) {
          health.status = health.status === 'critical' ? 'critical' : 'warning';
        }
      }
    } catch (e) {
      // PM2 未安装或无 openclaw 进程
    }

    // 连接数检查
    try {
      const connInfo = await execPromise('ss -tan | grep ESTAB | wc -l');
      health.connections.http = parseInt(connInfo.trim());
    } catch (e) {
      // 忽略
    }

  } catch (error) {
    console.error('Health check failed:', error);
    health.status = 'warning';
  }

  return health;
}

function execPromise(command: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const { exec } = require('child_process');
    exec(command, (error: any, stdout: string, stderr: string) => {
      if (error) {
        reject(error);
      } else {
        resolve(stdout);
      }
    });
  });
}

// ==================== 心跳服务 ====================

class HeartbeatService {
  private config: MutualRepairConfig;
  private lastRemoteHeartbeat: number = 0;
  private heartbeatTimer: NodeJS.Timeout | null = null;
  private checkTimer: NodeJS.Timeout | null = null;

  constructor(config: MutualRepairConfig) {
    this.config = config;
  }

  async start() {
    console.log('[Heartbeat] Starting heartbeat service...');
    console.log(`[Heartbeat] Local: ${this.config.localHost}:${this.config.localPort}`);
    console.log(`[Heartbeat] Remote: ${this.config.remoteHost}:${this.config.remotePort}`);

    // 启动心跳发送
    this.heartbeatTimer = setInterval(
      () => this.sendHeartbeat(),
      this.config.heartbeatInterval
    );

    // 启动远程心跳检查
    this.checkTimer = setInterval(
      () => this.checkRemoteHeartbeat(),
      this.config.heartbeatInterval / 2
    );

    // 立即发送一次
    await this.sendHeartbeat();
  }

  stop() {
    if (this.heartbeatTimer) clearInterval(this.heartbeatTimer);
    if (this.checkTimer) clearInterval(this.checkTimer);
    console.log('[Heartbeat] Heartbeat service stopped');
  }

  private async sendHeartbeat() {
    try {
      const health = await checkSystemHealth();
      
      const payload: HeartbeatRequest = {
        type: 'heartbeat',
        timestamp: Date.now(),
        source: {
          host: this.config.localHost,
          port: this.config.localPort
        },
        health: {
          status: health.status,
          memory: health.memory.percent,
          cpu: health.cpu.percent,
          uptime: Math.round(health.uptime),
          connections: health.connections.websocket + health.connections.http
        }
      };

      const url = `http://${this.config.remoteHost}:${this.config.remotePort}/api/heartbeat`;
      const response = await axios.post(url, payload, {
        timeout: this.config.heartbeatTimeout
      });

      console.log('[Heartbeat] Sent to remote:', response.data);
      this.lastRemoteHeartbeat = Date.now();

    } catch (error: any) {
      console.error('[Heartbeat] Failed to send:', error.message);
      
      // 如果连续失败，触发告警
      if (Date.now() - this.lastRemoteHeartbeat > this.config.heartbeatInterval * 3) {
        await this.handleRemoteDown();
      }
    }
  }

  private async checkRemoteHeartbeat() {
    const elapsed = Date.now() - this.lastRemoteHeartbeat;
    const threshold = this.config.heartbeatInterval * 2;

    if (elapsed > threshold && this.lastRemoteHeartbeat > 0) {
      console.error(`[Heartbeat] Remote heartbeat missing for ${elapsed}ms`);
      await this.handleRemoteDown();
    }
  }

  private async handleRemoteDown() {
    console.error('[Heartbeat] Remote node appears to be DOWN!');
    
    // 尝试远程诊断
    try {
      await this.diagnoseRemote();
    } catch (error) {
      console.error('[Heartbeat] Remote diagnosis failed:', error);
    }
  }

  private async diagnoseRemote() {
    console.log('[Diagnosis] Attempting remote diagnosis...');
    
    // 尝试 SSH 连接诊断（需要配置 SSH 密钥）
    // 这里提供诊断逻辑框架
    const diagnosis = {
      reachable: false,
      issues: [] as string[],
      suggestions: [] as string[]
    };

    // 检查网络连通性
    try {
      await execPromise(`ping -c 1 ${this.config.remoteHost}`);
      diagnosis.reachable = true;
    } catch (e) {
      diagnosis.issues.push('网络不可达');
      diagnosis.suggestions.push('检查网络连接和防火墙');
    }

    // 检查端口
    try {
      await execPromise(`nc -z ${this.config.remoteHost} ${this.config.remotePort}`);
    } catch (e) {
      diagnosis.issues.push(`端口 ${this.config.remotePort} 未开放`);
      diagnosis.suggestions.push('检查 OpenClaw 是否运行');
    }

    console.log('[Diagnosis] Result:', diagnosis);
    return diagnosis;
  }

  // HTTP 服务器 - 接收对端心跳
  createServer() {
    const http = require('http');
    
    const server = http.createServer(async (req: any, res: any) => {
      if (req.method === 'POST' && req.url === '/api/heartbeat') {
        let body = '';
        req.on('data', (chunk: any) => body += chunk);
        req.on('end', async () => {
          try {
            const heartbeat: HeartbeatRequest = JSON.parse(body);
            console.log('[Heartbeat] Received from remote:', heartbeat);
            
            this.lastRemoteHeartbeat = Date.now();
            
            // 检查对端健康状态
            if (heartbeat.health.status === 'critical') {
              console.warn('[Heartbeat] Remote node in CRITICAL state!');
              await this.offerHelp(heartbeat);
            }

            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({
              type: 'heartbeat_ack',
              timestamp: Date.now(),
              status: 'ok'
            }));
          } catch (error: any) {
            res.writeHead(400);
            res.end(JSON.stringify({ error: error.message }));
          }
        });
      } else if (req.method === 'POST' && req.url === '/api/repair') {
        // 处理修复请求
        let body = '';
        req.on('data', (chunk: any) => body += chunk);
        req.on('end', async () => {
          try {
            const repair: RepairRequest = JSON.parse(body);
            console.log('[Repair] Received request:', repair);
            
            const result = await this.executeRepair(repair);
            
            res.writeHead(200, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({
              type: 'repair_ack',
              timestamp: Date.now(),
              success: true,
              result
            }));
          } catch (error: any) {
            res.writeHead(500);
            res.end(JSON.stringify({
              type: 'repair_ack',
              success: false,
              error: error.message
            }));
          }
        });
      } else {
        res.writeHead(404);
        res.end('Not Found');
      }
    });

    server.listen(this.config.localPort, this.config.localHost, () => {
      console.log(`[Server] Listening on ${this.config.localHost}:${this.config.localPort}`);
    });

    return server;
  }

  private async offerHelp(heartbeat: HeartbeatRequest) {
    console.log('[Help] Offering help to remote node...');
    
    // 发送修复建议
    const suggestions = [];
    
    if (heartbeat.health.memory > 85) {
      suggestions.push('内存使用率高，建议重启 OpenClaw 进程');
    }
    if (heartbeat.health.cpu > 80) {
      suggestions.push('CPU 使用率高，检查是否有死循环或大量计算');
    }

    if (suggestions.length > 0) {
      console.log('[Help] Suggestions:', suggestions);
      // 可以通过 SSH 或其他方式执行修复
    }
  }

  private async executeRepair(repair: RepairRequest) {
    switch (repair.action) {
      case 'check':
        return await checkSystemHealth();
      
      case 'restart':
        return await this.restartOpenClaw();
      
      case 'diagnose':
        return await this.diagnoseLocal();
      
      default:
        throw new Error(`Unknown repair action: ${repair.action}`);
    }
  }

  private async restartOpenClaw() {
    console.log('[Repair] Restarting OpenClaw...');
    try {
      await execPromise('pm2 restart openclaw');
      return { success: true, message: 'OpenClaw restarted' };
    } catch (error: any) {
      try {
        await execPromise('systemctl restart openclaw');
        return { success: true, message: 'OpenClaw restarted via systemd' };
      } catch (e: any) {
        throw new Error('Failed to restart OpenClaw: ' + e.message);
      }
    }
  }

  private async diagnoseLocal() {
    return await checkSystemHealth();
  }
}

// ==================== Skill 导出 ====================

export default {
  name: 'openclaw-mutual-repair',
  version: '1.0.0',
  description: 'OpenClaw 双机互修助手 - 实现双机心跳监控和自动修复',
  
  triggers: [
    '心跳', 'heartbeat', '互修', 'mutual', '修复', 'repair',
    '监控', 'monitor', '健康', 'health', '诊断', 'diagnose'
  ],

  async execute(context: any) {
    const { message, config } = context;
    const text = message?.content?.toLowerCase() || '';

    // 初始化双机互修服务
    const mutualConfig: MutualRepairConfig = {
      localHost: config?.localHost || '0.0.0.0',
      localPort: config?.localPort || 9528,
      remoteHost: config?.remoteHost || '192.168.1.101',
      remotePort: config?.remotePort || 9528,
      heartbeatInterval: config?.heartbeatInterval || 300000, // 5 分钟
      heartbeatTimeout: config?.heartbeatTimeout || 30000,    // 30 秒
      memoryThreshold: config?.memoryThreshold || 85,
      cpuThreshold: config?.cpuThreshold || 80
    };

    if (text.includes('启动') || text.includes('start')) {
      const service = new HeartbeatService(mutualConfig);
      service.createServer();
      await service.start();
      
      return {
        content: `## ✅ 双机互修服务已启动\n\n**本机：** ${mutualConfig.localHost}:${mutualConfig.localPort}\n**对端：** ${mutualConfig.remoteHost}:${mutualConfig.remotePort}\n**心跳间隔：** ${mutualConfig.heartbeatInterval / 1000}秒\n\n服务正在后台运行，自动监控对端健康状态。`
      };
    }

    if (text.includes('停止') || text.includes('stop')) {
      // 需要在外部维护 service 实例
      return {
        content: '## ⚠️ 停止服务\n\n请通过进程管理工具停止服务，或重启 OpenClaw。'
      };
    }

    if (text.includes('状态') || text.includes('status') || text.includes('健康')) {
      const health = await checkSystemHealth();
      
      return {
        content: `## 🏥 健康检查结果\n\n**整体状态：** ${getStatusEmoji(health.status)} ${health.status.toUpperCase()}\n\n### 资源使用\n- **内存：** ${health.memory.percent}% (${health.memory.used}MB / ${health.memory.total}MB)\n- **CPU：** ${health.cpu.percent}%\n- **运行时间：** ${formatUptime(health.uptime)}\n\n### 进程状态\n${health.processes.pm2 
  ? `- **PM2 状态：** ${health.processes.pm2.status}\n- **进程内存：** ${health.processes.pm2.memory}MB\n- **重启次数：** ${health.processes.pm2.restarts}`
  : '- PM2 未检测到 OpenClaw 进程'
}\n\n### 建议\n${getSuggestions(health)}`
      };
    }

    if (text.includes('诊断') || text.includes('diagnose')) {
      const health = await checkSystemHealth();
      const diagnosis = await diagnoseIssues(health);
      
      return {
        content: `## 🔍 诊断报告\n\n${diagnosis.map((d: any) => `- **${d.issue}**\n  - 建议：${d.suggestion}`).join('\n')}`
      };
    }

    // 默认帮助
    return {
      content: `## 🤖 双机互修助手\n\n**可用命令：**\n- \`启动互修\` - 启动双机心跳监控\n- \`停止互修\` - 停止监控服务\n- \`健康检查\` / \`状态\` - 检查本机健康状态\n- \`诊断\` - 诊断潜在问题\n\n**配置项：**\n- localHost/localPort - 本机地址\n- remoteHost/remotePort - 对端地址\n- heartbeatInterval - 心跳间隔（毫秒）`
    };
  }
};

// ==================== 辅助函数 ====================

function getStatusEmoji(status: string): string {
  switch (status) {
    case 'ok': return '✅';
    case 'warning': return '⚠️';
    case 'critical': return '🚨';
    default: return '❓';
  }
}

function formatUptime(seconds: number): string {
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  return `${hours}小时${minutes}分钟`;
}

function getSuggestions(health: HealthStatus): string {
  const suggestions: string[] = [];
  
  if (health.memory.percent > 85) {
    suggestions.push('- ⚠️ 内存使用率高，建议配置 PM2 max_memory_restart');
  }
  if (health.cpu.percent > 80) {
    suggestions.push('- ⚠️ CPU 使用率高，检查是否有性能瓶颈');
  }
  if (health.processes.pm2 && health.processes.pm2.restarts > 5) {
    suggestions.push('- ⚠️ 进程重启频繁，检查日志排查崩溃原因');
  }
  if (health.processes.pm2 && health.processes.pm2.status !== 'online') {
    suggestions.push('- 🚨 OpenClaw 进程未运行，立即重启！');
  }
  
  return suggestions.length > 0 
    ? suggestions.join('\n') 
    : '- ✅ 一切正常，无需干预';
}

async function diagnoseIssues(health: HealthStatus) {
  const issues: any[] = [];
  
  if (health.memory.percent > 85) {
    issues.push({
      issue: '内存使用率过高',
      suggestion: '配置 PM2 max_memory_restart: 1G，或使用 clinic.js 分析内存泄漏'
    });
  }
  if (health.cpu.percent > 80) {
    issues.push({
      issue: 'CPU 使用率过高',
      suggestion: '检查是否有死循环、大量计算或未优化的查询'
    });
  }
  if (health.processes.pm2 && health.processes.pm2.restarts > 5) {
    issues.push({
      issue: '进程频繁重启',
      suggestion: '查看 PM2 日志：pm2 logs openclaw，排查崩溃原因'
    });
  }
  if (health.processes.pm2 && health.processes.pm2.status !== 'online') {
    issues.push({
      issue: '进程未运行',
      suggestion: '立即执行：pm2 restart openclaw 或 systemctl restart openclaw'
    });
  }
  
  if (issues.length === 0) {
    issues.push({
      issue: '无问题',
      suggestion: '系统运行正常'
    });
  }
  
  return issues;
}
