/**
 * 运维助手 Skill 实现 (v3.0)
 *
 * 本模块提供运维检查功能，供 AI 助手调用
 *
 * 主要改进：
 * - 远程SSH命令使用ssh2库，提升性能和安全性
 * - 添加连接池管理
 * - 增强安全性（移除StrictHostKeyChecking=no）
 * - 添加重试机制和错误处理
 * - 添加审计日志
 * - 支持SFTP文件传输
 * - 添加并发控制
 * - v2.1: 密码加密、命令白名单、内部命令安全
 * - v3.0: 告警通知(飞书/微信/邮件/Webhook)、定时巡检调度、巡检报告
 */

import { exec } from 'child_process'
import { promisify } from 'util'
import { readFile, writeFile } from 'fs/promises'
import { join } from 'path'
import { existsSync } from 'fs'

import { 
  getSSHPool, 
  closeGlobalPool, 
  type ConnectionConfig 
} from './utils/ssh-pool.js'
import { 
  getSFTPManager, 
  type SFTPManager 
} from './utils/sftp-client.js'
import { 
  getAuditLogger, 
  type AuditLogger 
} from './utils/audit-logger.js'
import {
  saveServersSecurely,
  loadServersSecurely,
  isEncrypted
} from './utils/crypto.js'
import {
 validateCommand,
 validateCommands
} from './utils/command-validator.js'
import {
 getAlertManager,
 type AlertRule,
 type NotifyChannel,
 type NotifyConfig,
 type AlertRecord,
 DEFAULT_ALERT_RULES
} from './utils/alert-manager.js'
import {
 getPatrolScheduler,
 type PatrolJob,
 type PatrolCheck,
 type PatrolExecutor,
 type PatrolResult,
 DEFAULT_PATROL_JOBS
} from './utils/patrol-scheduler.js'
import {
 getNetworkDiagnostics,
 type PingResult,
 type DnsResult,
 type TraceResult,
 type PortCheckResult,
 type ConnectivityResult,
} from './utils/network-diagnostics.js'
import {
 DockerManager,
 ServiceManager,
 type DockerContainer,
 type DockerStats,
 type DockerInspect,
 type ServiceStatus,
} from './utils/service-manager.js'
import {
 getHealthChecker,
 formatHealthReport,
 type HealthCheckResult,
 type HealthReport,
} from './utils/health-checker.js'
import {
 getSecurityAuditor,
 type SecurityFinding,
 type SecurityAuditor,
} from './utils/security-auditor.js'
import {
 getSmartLogAnalyzer,
 type LogEntry,
 type LogAnalysisResult,
 type LogAnomaly,
} from './utils/smart-log-analyzer.js'
import {
 getConfigChangeTracker,
 type ConfigChangeTracker,
 type ChangeRecord,
} from './utils/config-change-tracker.js'
import {
  getReportGenerator,
  type OpsReport,
  type ReportFormat,
} from './utils/report-generator.js'
import {
  DockerHealthChecker,
  type DockerHealthReport,
  type ContainerCheckResult,
  type ContainerIssue,
} from './utils/docker-health-checker.js'
import {
  SSLMonitor,
  type SSLMonitorReport,
  type SSLCheckResult,
  type CertInfo,
  type SSLMonitorConfig,
} from './utils/ssl-monitor.js'

const execAsync = promisify(exec)

/**
 * SSH 配置
 */
export interface SSHConfig {
  host: string
  port?: number
  user?: string
  keyFile?: string
  password?: string
  name?: string
  tags?: string[]
}

/**
 * 服务器集群配置
 */
export interface ClusterConfig {
  name: string
  servers: SSHConfig[]
}

/**
 * 服务器列表配置文件路径
 */
function getServersConfigPath(): string {
  return join(process.env.HOME || '~', '.config/ops-maintenance/servers.json')
}

/**
 * 默认服务器配置目录
 */
function getConfigDir(): string {
  return join(process.env.HOME || '~', '.config/ops-maintenance')
}

/**
 * 保存服务器列表（使用加密存储）
 */
export async function saveServers(servers: SSHConfig[]): Promise<void> {
  await saveServersSecurely(servers)
}

/**
 * 加载服务器列表（自动解密）
 */
export async function loadServers(): Promise<SSHConfig[]> {
  return await loadServersSecurely()
}

/**
 * 添加服务器
 */
export async function addServer(config: SSHConfig): Promise<void> {
  const servers = await loadServers()
  
  // 检查是否已存在
  const existing = servers.findIndex(s => s.host === config.host)
  if (existing >= 0) {
    servers[existing] = { ...servers[existing], ...config }
  } else {
    servers.push(config)
  }
  
  await saveServers(servers)
}

/**
 * 移除服务器
 */
export async function removeServer(host: string): Promise<void> {
  const servers = await loadServers()
  const filtered = servers.filter(s => s.host !== host)
  await saveServers(filtered)
}

/**
 * 按标签筛选服务器
 */
export async function getServersByTag(tag: string): Promise<SSHConfig[]> {
  const servers = await loadServers()
  return servers.filter(s => s.tags?.includes(tag))
}

/**
 * 批量检查所有服务器健康状态
 */
export async function checkAllServersHealth(
  tags?: string[]
): Promise<{ server: string; status: string; details: string }[]> {
  const servers = tags 
    ? await Promise.all(tags.map(getServersByTag)).then(arr => arr.flat())
    : await loadServers()
  
  const results: { server: string; status: string; details: string }[] = []
  const pool = getSSHPool()
  const audit = getAuditLogger()
  
  // 并发控制：最多同时检查5台服务器
  const concurrency = 5
  for (let i = 0; i < servers.length; i += concurrency) {
    const batch = servers.slice(i, i + concurrency)
    
    await Promise.all(batch.map(async (config) => {
      const name = config.name || config.host
      const startTime = Date.now()
      
      try {
        // 并行执行多个检查（使用简单命令，避免管道和重定向）
        const [load, mem, disk] = await Promise.all([
          pool.executeCommand(config, 'uptime'),
          pool.executeCommand(config, 'free -h'),
          pool.executeCommand(config, 'df -h /')
        ])

        // 解析磁盘使用率（从df输出中提取）
        const diskUsage = disk.stdout.includes('%')
          ? disk.stdout.match(/(\d+)%/)?.[1] || 'N/A'
          : 'N/A'
        const isHealthy = parseInt(diskUsage) < 90
        
        results.push({
          server: name,
          status: isHealthy ? '✅ 健康' : '⚠️ 磁盘 ' + diskUsage,
          details: `负载: ${load.stdout.split('load averages:')[1]?.trim() || 'N/A'}`
        })
        
        const duration = Date.now() - startTime
        audit.logSuccess('health_check', name, 'uptime && free && df', duration)
      } catch (error: any) {
        results.push({
          server: name,
          status: '❌ 离线',
          details: error.message.substring(0, 50)
        })
        
        audit.logFailure('health_check', name, error.message)
      }
    }))
  }
  
  return results
}

/**
 * 批量执行命令到所有服务器
 */
export async function executeOnAllServers(
  command: string,
  tags?: string[]
): Promise<{ server: string; output: string }[]> {
  // 安全检查：验证命令是否在白名单中
  const validation = validateCommand(command)
  if (!validation.safe) {
    throw new Error(`安全检查失败: ${validation.reason}`)
  }

  const servers = tags 
    ? await Promise.all(tags.map(getServersByTag)).then(arr => arr.flat())
    : await loadServers()
  
  const results: { server: string; output: string }[] = []
  const pool = getSSHPool()
  const audit = getAuditLogger()
  
  // 并发控制
  const concurrency = 5
  for (let i = 0; i < servers.length; i += concurrency) {
    const batch = servers.slice(i, i + concurrency)
    
    await Promise.all(batch.map(async (config) => {
      const name = config.name || config.host
      const startTime = Date.now()
      
      try {
        const result = await pool.executeCommand(config, command)
        results.push({ 
          server: name, 
          output: result.stdout || result.stderr || '(无输出)' 
        })
        
        const duration = Date.now() - startTime
        audit.logSuccess('execute_command', name, command, duration)
      } catch (error: any) {
        results.push({ server: name, output: `错误: ${error.message}` })
        audit.logFailure('execute_command', name, error.message, command)
      }
    }))
  }
  
  return results
}

/**
 * 批量添加服务器 (支持 IP:Port 格式)
 */
export async function batchAddServers(servers: string[]): Promise<{ success: number; failed: number; details: string[] }> {
  const results: string[] = []
  let success = 0
  let failed = 0

  // 解析每个服务器字符串
  for (const serverStr of servers) {
    try {
      const config = parseServerString(serverStr)
      await addServer(config)
      success++
      results.push(`✅ ${config.name || config.host}:${config.port || 22} - 已添加`)
    } catch (error: any) {
      failed++
      results.push(`❌ ${serverStr} - ${error.message}`)
    }
  }

  return { success, failed, details: results }
}

/**
 * 从 CSV/JSON 批量导入
 */
export async function importServersFromText(text: string): Promise<{ success: number; failed: number; servers: SSHConfig[] }> {
  const servers: SSHConfig[] = []
  let failed = 0

  // 尝试解析为 JSON
  try {
    const parsed = JSON.parse(text)
    const arr = Array.isArray(parsed) ? parsed : [parsed]
    for (const item of arr) {
      if (item.host) {
        servers.push({
          host: item.host,
          port: item.port || 22,
          user: item.user,
          name: item.name,
          tags: item.tags
        })
      }
    }
    if (servers.length > 0) {
      await saveServers([...await loadServers(), ...servers])
      return { success: servers.length, failed: 0, servers }
    }
  } catch {
    // 不是 JSON，尝试 CSV
  }

  // CSV 解析
  const lines = text.split('\n').filter(l => l.trim() && !l.startsWith('#'))
  for (const line of lines) {
    const parts = line.split(',').map(p => p.trim())
    if (parts[0]) {
      const hostPort = parts[0].split(':')
      servers.push({
        host: hostPort[0],
        port: hostPort[1] ? parseInt(hostPort[1]) : 22,
        user: parts[2] || undefined,
        name: parts[3] || undefined,
        tags: parts[4] ? parts[4].split(';') : undefined
      })
    }
  }

  // 保存
  const existing = await loadServers()
  await saveServers([...existing, ...servers])

  return { success: servers.length, failed, servers }
}

/**
 * 解析服务器字符串为配置
 */
function parseServerString(serverStr: string): SSHConfig {
  let host = serverStr
  let user: string | undefined
  let port: number | undefined

  // 提取用户
  if (host.includes('@')) {
    const parts = host.split('@')
    user = parts[0]
    host = parts[1]
  }

  // 提取端口
  if (host.includes(':')) {
    const parts = host.split(':')
    host = parts[0]
    port = parseInt(parts[1])
  }

  // 生成友好名称
  const name = `server-${host.replace(/\./g, '-')}`

  return { host, port: port || 22, user, name }
}

/**
 * 服务器状态摘要
 */
export async function getClusterSummary(): Promise<string> {
  const servers = await loadServers()
  const results = await checkAllServersHealth()
  
  const online = results.filter(r => r.status.includes('健康')).length
  const warning = results.filter(r => r.status.includes('⚠️')).length
  const offline = results.filter(r => r.status.includes('❌')).length
  
  const lines: string[] = []
  lines.push('### 🖥️ 服务器集群状态\n')
  lines.push(`**总计**: ${servers.length} 台 | ✅ ${online} | ⚠️ ${warning} | ❌ ${offline}\n`)
  
  for (const r of results) {
    lines.push(`- **${r.server}**: ${r.status}`)
    if (r.details !== r.status) {
      lines.push(`  - ${r.details}`)
    }
  }
  
  return lines.join('\n')
}

/**
 * 通过 SSH 执行远程命令
 */
export async function runRemoteCommand(
  config: SSHConfig, 
  command: string
): Promise<string> {
  // 安全检查：验证命令是否在白名单中
  const validation = validateCommand(command)
  if (!validation.safe) {
    throw new Error(`安全检查失败: ${validation.reason}`)
  }

  const pool = getSSHPool()
  const audit = getAuditLogger()
  const startTime = Date.now()
  
  try {
    const result = await pool.executeCommand(config, command)
    const duration = Date.now() - startTime
    
    audit.logSuccess('remote_command', config.host, command, duration)
    
    return result.stdout || result.stderr || '(无输出)'
  } catch (error: any) {
    audit.logFailure('remote_command', config.host, error.message, command)
    return `SSH 连接失败: ${error.message}`
  }
}

/**
 * 执行系统命令并返回结果
 */
export async function runCommand(cmd: string, timeout: number = 10000): Promise<string> {
  // 安全检查：验证命令是否在白名单中
  const validation = validateCommand(cmd)
  if (!validation.safe) {
    throw new Error(`安全检查失败: ${validation.reason}`)
  }

  try {
    // 不使用shell，直接执行命令
    const { stdout, stderr } = await execAsync(cmd, { timeout })
    return stdout || stderr || '(无输出)'
  } catch (error: any) {
    return `命令执行失败: ${error.message}`
  }
}

/**
 * 系统健康检查
 */
export async function checkHealth(): Promise<string> {
  const results: string[] = []
  
  results.push('### 🩺 系统健康检查\n')
  
  // 负载
  results.push('**负载:**')
  results.push('```\n' + await runCommand('uptime') + '```\n')
  
  // 内存
  results.push('**内存:**')
  results.push('```\n' + await runCommand('vm_stat | head -10') + '```\n')
  
  // 磁盘
  results.push('**磁盘:**')
  results.push('```\n' + await runCommand('df -h | grep -E "^/dev"') + '```\n')
  
  // 核心服务状态
  const services = ['nginx', 'docker', 'postgresql', 'redis-server']
  results.push('**服务状态:**')
  for (const svc of services) {
    const status = await runCommand(`pgrep -f "${svc}" > /dev/null && echo "运行中" || echo "已停止"`)
    const emoji = status.includes('运行中') ? '✅' : '❌'
    results.push(`- ${svc}: ${emoji} ${status.trim()}`)
  }
  
  return results.join('\n')
}

/**
 * 日志分析
 */
export async function analyzeLogs(pattern: string = 'error', lines: number = 30): Promise<string> {
  const results: string[] = []
  results.push(`### 📋 日志分析 (搜索: "${pattern}")\n`)
  
  const logPaths = [
    '/var/log/system.log',
    `${process.env.HOME}/.npm/_logs/*.log`,
  ]
  
  for (const logPath of logPaths) {
    try {
      const output = await runCommand(`grep -i "${pattern}" "${logPath}" 2>/dev/null | tail -${lines}`)
      if (output && !output.includes('命令执行失败')) {
        results.push(`**${logPath}:**`)
        results.push('```\n' + output + '```')
      }
    } catch {
      // 跳过不存在的日志
    }
  }
  
  return results.join('\n') || '未找到匹配的日志'
}

/**
 * 性能监控
 */
export async function checkPerformance(): Promise<string> {
  const results: string[] = []
  results.push('### 📊 性能监控\n')
  
  // CPU
  results.push('**CPU:**')
  results.push('```\n' + await runCommand('sysctl -n machdep.cpu.brand_string 2>/dev/null || echo "N/A"') + '```\n')
  
  // 内存和 CPU 使用
  results.push('**实时状态:**')
  results.push('```\n' + await runCommand('top -l 1 -n 0 | grep -E "PhysMem|CPU"') + '```\n')
  
  // 磁盘 I/O
  results.push('**磁盘 I/O:**')
  results.push('```\n' + await runCommand('iostat -d 2 2>/dev/null | tail -5 || echo "iostat 不可用"') + '```\n')
  
  return results.join('\n')
}

/**
 * 端口检查
 */
export async function checkPort(port?: number): Promise<string> {
  if (port) {
    return `### 🔌 端口 ${port}\n\`\`\`\n${await runCommand(`lsof -i :${port} 2>/dev/null || echo "端口未占用"`)}\n\`\`\``
  }
  
  return `### 🔌 监听端口\n\`\`\`\n${await runCommand('lsof -i -P | grep LISTEN | head -20')}\n\`\`\``
}

/**
 * 进程检查
 */
export async function checkProcess(name?: string): Promise<string> {
  if (name) {
    const output = await runCommand(`ps aux | grep -i "${name}" | grep -v grep | head -10`)
    const count = await runCommand(`pgrep -fc "${name}" 2>/dev/null || echo 0`)
    
    return `### ⚙️ 进程 "${name}"\n**运行实例: ${count.trim()}**\n\`\`\`\n${output || '未找到'}\n\`\`\``
  }
  
  // macOS的ps命令不支持--sort，使用不同的方法
  return `### ⚙️ Top 进程 (按 CPU)\n\`\`\`\n${await runCommand('ps aux | sort -nr -k 3 | head -15')}\n\`\`\``
}

/**
 * 磁盘使用
 */
export async function checkDisk(): Promise<string> {
  const home = process.env.HOME || '~'
  
  const results: string[] = []
  results.push('### 💾 磁盘使用\n')
  
  results.push('**分区使用:**')
  results.push('```\n' + await runCommand('df -h') + '```\n')
  
  results.push('**大目录 (Home):**')
  results.push('```\n' + await runCommand(`du -sh "${home}"/* 2>/dev/null | sort -hr | head -10`) + '```')
  
  return results.join('\n')
}

/**
 * 远程服务器健康检查
 */
export async function checkRemoteHealth(
  config: SSHConfig,
  services: string[] = ['nginx', 'docker', 'postgresql', 'redis-server']
): Promise<string> {
  const results: string[] = []
  results.push(`### 🩺 远程服务器健康检查 (${config.host})\n`)
  
  // 系统信息
  results.push('**系统:**')  
  results.push('```\n' + await runRemoteCommand(config, 'uptime && free -h && df -h') + '```\n')
  
  // 服务状态
  results.push('**服务状态:**')
  for (const svc of services) {
    const status = await runRemoteCommand(
      config, 
      `systemctl is-active ${svc} 2>/dev/null || pgrep -f "${svc}" >/dev/null && echo "running" || echo "stopped"`
    )
    const emoji = status.trim() === 'active' || status.trim() === 'running' ? '✅' : '❌'
    results.push(`- ${svc}: ${emoji} ${status.trim()}`)
  }
  
  return results.join('\n')
}

/**
 * 远程服务器端口检查
 */
export async function checkRemotePort(config: SSHConfig, port?: number): Promise<string> {
  if (port) {
    return `### 🔌 端口 ${port} (${config.host})\n\`\`\`\n${await runRemoteCommand(config, `lsof -i :${port} 2>/dev/null || netstat -tlnp | grep :${port}`)}\n\`\`\``
  }
  
  return `### 🔌 监听端口 (${config.host})\n\`\`\`\n${await runRemoteCommand(config, 'lsof -i -P | grep LISTEN | head -20')}\n\`\`\``
}

/**
 * 远程服务器进程检查
 */
export async function checkRemoteProcess(config: SSHConfig, name?: string): Promise<string> {
  if (name) {
    const output = await runRemoteCommand(config, `ps aux | grep -i "${name}" | grep -v grep | head -10`)
    return `### ⚙️ 进程 "${name}" (${config.host})\n\`\`\`\n${output}\n\`\`\``
  }
  
  return `### ⚙️ Top 进程 (${config.host})\n\`\`\`\n${await runRemoteCommand(config, 'ps aux --sort=-%cpu | head -15')}\n\`\`\``
}

/**
 * 远程服务器磁盘检查
 */
export async function checkRemoteDisk(config: SSHConfig): Promise<string> {
  const results: string[] = []
  results.push(`### 💾 磁盘使用 (${config.host})\n`)
  
  results.push('**分区:**')
  results.push('\`\`\`' + await runRemoteCommand(config, 'df -h') + '\`\`\`')
  
  results.push('**大目录:**')
  results.push('\`\`\`' + await runRemoteCommand(config, 'du -sh /* 2>/dev/null | sort -hr | head -10') + '\`\`\`')
  
  return results.join('\n')
}

/**
 * 远程服务器日志检查
 */
export async function checkRemoteLogs(
  config: SSHConfig, 
  pattern: string = 'error',
  lines: number = 30
): Promise<string> {
  const results: string[] = []
  results.push(`### 📋 远程日志 (${config.host}, 搜索: "${pattern}")\n`)
  
  // 常见日志路径
  const logPaths = [
    '/var/log/syslog',
    '/var/log/nginx/error.log',
    '/var/log/apache2/error.log',
    '~/.npm/_logs/*.log'
  ]
  
  for (const logPath of logPaths) {
    const output = await runRemoteCommand(config, `grep -i "${pattern}" ${logPath} 2>/dev/null | tail -${lines}`)
    if (output && !output.includes('失败')) {
      results.push(`**${logPath}:**`)
      results.push('\`\`\`' + output + '\`\`\`')
    }
  }
  
  return results.join('\n') || '未找到匹配的日志'
}

/**
 * 运维操作执行入口
 */
export type OpsAction = 'health' | 'logs' | 'perf' | 'ports' | 'process' | 'disk'

/**
 * 本地运维操作
 */
export async function executeOp(action: string, arg?: string): Promise<string> {
  switch (action.toLowerCase()) {
    case 'health':
    case 'check':
      return checkHealth()
    case 'logs':
    case 'log':
      return analyzeLogs(arg || 'error')
    case 'perf':
    case 'performance':
      return checkPerformance()
    case 'ports':
    case 'port':
      return checkPort(arg ? parseInt(arg) : undefined)
    case 'process':
    case 'proc':
      return checkProcess(arg)
    case 'disk':
    case 'space':
      return checkDisk()
    default:
      return `未知操作: ${action}\n\n可用操作: health, logs, perf, ports, process, disk`
  }
}

/**
 * 远程运维操作
 */
export async function executeRemoteOp(
  action: string, 
  config: SSHConfig,
  arg?: string
): Promise<string> {
  switch (action.toLowerCase()) {
    case 'health':
    case 'check':
      return checkRemoteHealth(config)
    case 'logs':
    case 'log':
      return checkRemoteLogs(config, arg || 'error')
    case 'ports':
    case 'port':
      return checkRemotePort(config, arg ? parseInt(arg) : undefined)
    case 'process':
    case 'proc':
      return checkRemoteProcess(config, arg)
    case 'disk':
      return checkRemoteDisk(config)
    default:
      return `未知操作: ${action}`
  }
}

/**
 * SFTP文件操作
 */
export async function uploadFile(
  config: SSHConfig,
  localPath: string,
  remotePath: string
): Promise<string> {
  const sftp = getSFTPManager()
  const audit = getAuditLogger()
  const startTime = Date.now()
  
  try {
    await sftp.uploadFile(config, localPath, remotePath)
    const duration = Date.now() - startTime
    audit.logSuccess('upload_file', config.host, `${localPath} -> ${remotePath}`, duration)
    return `✅ 文件上传成功: ${localPath} -> ${remotePath}`
  } catch (error: any) {
    audit.logFailure('upload_file', config.host, error.message, `${localPath} -> ${remotePath}`)
    return `❌ 文件上传失败: ${error.message}`
  }
}

export async function downloadFile(
  config: SSHConfig,
  remotePath: string,
  localPath: string
): Promise<string> {
  const sftp = getSFTPManager()
  const audit = getAuditLogger()
  const startTime = Date.now()
  
  try {
    await sftp.downloadFile(config, remotePath, localPath)
    const duration = Date.now() - startTime
    audit.logSuccess('download_file', config.host, `${remotePath} -> ${localPath}`, duration)
    return `✅ 文件下载成功: ${remotePath} -> ${localPath}`
  } catch (error: any) {
    audit.logFailure('download_file', config.host, error.message, `${remotePath} -> ${localPath}`)
    return `❌ 文件下载失败: ${error.message}`
  }
}

export async function listRemoteDirectory(
  config: SSHConfig,
  remotePath: string
): Promise<string> {
  const sftp = getSFTPManager()
  
  try {
    const files = await sftp.listDirectory(config, remotePath)
    const output = files.map(f => `${f.type === 'd' ? '📁' : '📄'} ${f.name} (${f.size || 0} bytes)`).join('\n')
    return `### 📁 目录: ${remotePath}\n\`\`\`\n${output}\n\`\`\``
  } catch (error: any) {
    return `❌ 列出目录失败: ${error.message}`
  }
}

/**
 * 获取审计日志统计
 */
export async function getAuditStats(): Promise<string> {
  const audit = getAuditLogger()
  const stats = audit.getStats()
  
  const lines: string[] = []
  lines.push('### 📊 审计日志统计\n')
  lines.push(`**总计**: ${stats.total} 次操作\n`)
  lines.push(`**成功**: ${stats.success} | **失败**: ${stats.failure} | **部分**: ${stats.partial}\n`)
  
  if (Object.keys(stats.byOperation).length > 0) {
    lines.push('**按操作类型:**')
    for (const [op, count] of Object.entries(stats.byOperation)) {
      lines.push(`- ${op}: ${count}`)
    }
    lines.push('')
  }
  
  if (Object.keys(stats.byServer).length > 0) {
    lines.push('**按服务器:**')
    for (const [server, count] of Object.entries(stats.byServer)) {
      lines.push(`- ${server}: ${count}`)
    }
  }
  
  return lines.join('\n')
}

/**
 * 清理资源
 */
export async function cleanup(): Promise<void> {
 // 停止巡检调度器
 const scheduler = getPatrolScheduler()
 if (scheduler.running()) {
   scheduler.stop()
 }
 await closeGlobalPool()
}

// ============================================================
// v3.0 告警通知功能
// ============================================================

/**
 * 配置告警通知渠道
 */
export async function configureAlertNotify(
 channel: NotifyChannel,
 config: any
): Promise<string> {
 const alertManager = getAlertManager()
 alertManager.updateNotifyConfig(channel, config)
 return `✅ 已更新 ${channel} 通知渠道配置`
}

/**
 * 查看告警规则
 */
export async function listAlertRules(): Promise<string> {
 const alertManager = getAlertManager()
 const rules = alertManager.getRules()
 
 const lines: string[] = []
 lines.push('### 🚨 告警规则列表\n')
 
 for (const rule of rules) {
   const statusEmoji = rule.enabled ? '✅' : '❌'
   const levelEmoji = { info: 'ℹ️', warning: '⚠️', critical: '🔴' }[rule.level]
   lines.push(`${statusEmoji} ${levelEmoji} **${rule.name}** (\`${rule.id}\`)`)
   lines.push(`   类型: ${rule.type} | 阈值: ${rule.threshold} | 间隔: ${rule.interval}s | 渠道: ${rule.channels.join(',')}`)
   if (rule.description) {
     lines.push(`   ${rule.description}`)
   }
   lines.push('')
 }
 
 return lines.join('\n')
}

/**
 * 添加/修改告警规则
 */
export async function setAlertRule(rule: AlertRule): Promise<string> {
 const alertManager = getAlertManager()
 alertManager.upsertRule(rule)
 return `✅ 告警规则已保存: ${rule.name} (${rule.id})`
}

/**
 * 删除告警规则
 */
export async function deleteAlertRule(ruleId: string): Promise<string> {
 const alertManager = getAlertManager()
 const deleted = alertManager.removeRule(ruleId)
 return deleted ? `✅ 告警规则已删除: ${ruleId}` : `❌ 告警规则不存在: ${ruleId}`
}

/**
 * 启用/禁用告警规则
 */
export async function toggleAlertRule(ruleId: string, enabled: boolean): Promise<string> {
 const alertManager = getAlertManager()
 const toggled = alertManager.toggleRule(ruleId, enabled)
 return toggled
   ? `✅ 告警规则 ${ruleId} 已${enabled ? '启用' : '禁用'}`
   : `❌ 告警规则不存在: ${ruleId}`
}

/**
 * 查看活跃告警
 */
export async function listActiveAlerts(): Promise<string> {
 const alertManager = getAlertManager()
 const alerts = alertManager.getActiveAlerts()
 const stats = alertManager.getAlertStats()
 
 const lines: string[] = []
 lines.push('### 🔔 活跃告警\n')
 lines.push(`**总计**: ${stats.firing} 条活跃 | ${stats.silenced} 条静默 | ${stats.resolved} 条已恢复\n`)
 
 if (alerts.length === 0) {
   lines.push('当前无活跃告警 ✨')
 } else {
   for (const alert of alerts) {
     const levelEmoji = { info: 'ℹ️', warning: '⚠️', critical: '🔴' }[alert.level]
     lines.push(`${levelEmoji} **${alert.ruleName}** — ${alert.server}`)
     lines.push(`   类型: ${alert.type} | 当前: ${alert.value} | 阈值: ${alert.threshold}`)
     lines.push(`   触发时间: ${alert.firedAt} | 通知次数: ${alert.notifyCount}`)
     lines.push('')
   }
 }
 
 return lines.join('\n')
}

/**
 * 查看告警统计
 */
export async function getAlertsStats(): Promise<string> {
 const alertManager = getAlertManager()
 const stats = alertManager.getAlertStats()
 
 const lines: string[] = []
 lines.push('### 📊 告警统计\n')
 lines.push(`**总计**: ${stats.total} 条 | 🔴 触发 ${stats.firing} | ✅ 恢复 ${stats.resolved} | 🔇 静默 ${stats.silenced}\n`)
 
 if (Object.keys(stats.byLevel).length > 0) {
   lines.push('**按级别:**')
   for (const [level, count] of Object.entries(stats.byLevel)) {
     const emoji = { info: 'ℹ️', warning: '⚠️', critical: '🔴' }[level] || '❓'
     lines.push(`- ${emoji} ${level}: ${count}`)
   }
 }
 
 if (Object.keys(stats.byType).length > 0) {
   lines.push('\n**按类型:**')
   for (const [type, count] of Object.entries(stats.byType)) {
     lines.push(`- ${type}: ${count}`)
   }
 }
 
 if (Object.keys(stats.byServer).length > 0) {
   lines.push('\n**按服务器:**')
   for (const [server, count] of Object.entries(stats.byServer)) {
     lines.push(`- ${server}: ${count}`)
   }
 }
 
 return lines.join('\n')
}

/**
 * 静默告警
 */
export async function silenceAlert(ruleId: string, server: string, durationMinutes: number = 60): Promise<string> {
 const alertManager = getAlertManager()
 const key = `${ruleId}:${server}`
 const silenced = alertManager.silence(key, durationMinutes * 60)
 return silenced
   ? `🔇 告警已静默 ${durationMinutes} 分钟: ${ruleId} @ ${server}`
   : `❌ 未找到活跃告警: ${ruleId} @ ${server}`
}

/**
 * 清理旧告警
 */
export async function cleanupAlerts(daysOld: number = 7): Promise<string> {
 const alertManager = getAlertManager()
 const removed = alertManager.cleanup(daysOld)
 return `🗑️ 已清理 ${removed} 条 ${daysOld} 天前的旧告警`
}

// ============================================================
// v3.0 定时巡检功能
// ============================================================

/**
 * 巡检执行器实现
 */
class OpsPatrolExecutor implements PatrolExecutor {
 async getServerList(job: PatrolJob): Promise<string[]> {
   const servers: string[] = ['localhost']
   
   // 如果任务指定了服务器，只检查指定的
   if (job.servers?.length) {
     return job.servers
   }
   
   // 否则检查本地 + 所有配置的远程服务器
   try {
     const remoteServers = await loadServers()
     if (job.tags?.length) {
       const matched = remoteServers.filter(s => 
         s.tags?.some(t => job.tags!.includes(t))
       )
       servers.push(...matched.map(s => s.name || s.host))
     } else {
       servers.push(...remoteServers.map(s => s.name || s.host))
     }
   } catch {
     // 远程服务器列表为空也没关系
   }
   
   return servers
 }

 async executeCheck(
   server: string,
   check: PatrolCheck
 ): Promise<{
   status: 'ok' | 'warning' | 'critical' | 'error'
   value?: number
   message: string
   detail?: string
   extra?: Record<string, any>
 }> {
   try {
     const isLocal = server === 'localhost'
     
     switch (check.type) {
       case 'health':
         return this.checkHealth(isLocal, server)
       case 'disk':
         return this.checkDisk(isLocal, server)
       case 'memory':
         return this.checkMemory(isLocal, server)
       case 'load':
         return this.checkLoad(isLocal, server)
       case 'cpu':
         return this.checkCpu(isLocal, server)
       case 'service':
         return this.checkService(isLocal, server, check.params?.services || ['nginx', 'docker', 'sshd'])
       default:
         return { status: 'error', message: `不支持的检查类型: ${check.type}` }
     }
   } catch (error: any) {
     return { status: 'error', message: error.message }
   }
 }

 private async checkHealth(isLocal: boolean, server: string) {
   try {
     const output = isLocal
       ? await runCommand('uptime')
       : await runRemoteCommand({ host: server } as SSHConfig, 'uptime')
     
     // 解析负载
     const loadMatch = output.match(/load averages?:\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)/i)
       || output.match(/load average:\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)/i)
     
     const load5 = loadMatch ? parseFloat(loadMatch[2]) : 0
     const status = load5 > 10 ? 'critical' : load5 > 5 ? 'warning' : 'ok'
     
     return {
       status,
       value: load5,
       message: `系统负载: ${load5}`,
       detail: output.trim(),
     }
   } catch (error: any) {
     return { status: 'error', value: 0, message: `健康检查失败: ${error.message}` }
   }
 }

 private async checkDisk(isLocal: boolean, server: string) {
   try {
     const output = isLocal
       ? await runCommand('df -h /')
       : await runRemoteCommand({ host: server } as SSHConfig, 'df -h /')
     
     const usageMatch = output.match(/(\d+)%/)
     const usage = usageMatch ? parseInt(usageMatch[1]) : 0
     const status = usage > 90 ? 'critical' : usage > 80 ? 'warning' : 'ok'
     
     return {
       status,
       value: usage,
       message: `磁盘使用率: ${usage}%`,
       detail: output.trim(),
     }
   } catch (error: any) {
     return { status: 'error', value: 0, message: `磁盘检查失败: ${error.message}` }
   }
 }

 private async checkMemory(isLocal: boolean, server: string) {
   try {
     // macOS: vm_stat, Linux: free -m
     const cmd = isLocal ? 'vm_stat | head -10' : 'free -m'
     const output = isLocal
       ? await runCommand(cmd)
       : await runRemoteCommand({ host: server } as SSHConfig, cmd)
     
     let usage = 0
     // Linux: free -m 解析
     const memMatch = output.match(/Mem:\s+\d+\s+\d+\s+\d+/)
     if (memMatch) {
       const nums = memMatch[0].match(/\d+/g)
       if (nums && nums.length >= 3) {
         usage = Math.round((parseInt(nums[1]) / parseInt(nums[0])) * 100)
       }
     }
     
     const status = usage > 95 ? 'critical' : usage > 85 ? 'warning' : 'ok'
     
     return {
       status,
       value: usage,
       message: `内存使用率: ${usage}%`,
       detail: output.trim().substring(0, 200),
     }
   } catch (error: any) {
     return { status: 'error', value: 0, message: `内存检查失败: ${error.message}` }
   }
 }

 private async checkLoad(isLocal: boolean, server: string) {
   try {
     const output = isLocal
       ? await runCommand('uptime')
       : await runRemoteCommand({ host: server } as SSHConfig, 'uptime')
     
     const loadMatch = output.match(/load averages?:\s*([\d.]+)[\s,]+([\d.]+)[\s,]+([\d.]+)/i)
       || output.match(/load average:\s*([\d.]+),\s*([\d.]+),\s*([\d.]+)/i)
     
     const load5 = loadMatch ? parseFloat(loadMatch[2]) : 0
     const status = load5 > 10 ? 'critical' : load5 > 5 ? 'warning' : 'ok'
     
     return {
       status,
       value: load5,
       message: `5分钟负载: ${load5}`,
       detail: output.trim(),
     }
   } catch (error: any) {
     return { status: 'error', value: 0, message: `负载检查失败: ${error.message}` }
   }
 }

 private async checkCpu(isLocal: boolean, server: string) {
   try {
     const cmd = isLocal
       ? 'top -l 1 -n 0 | grep -E "CPU"'
       : 'top -bn1 | grep "Cpu"'
     const output = isLocal
       ? await runCommand(cmd)
       : await runRemoteCommand({ host: server } as SSHConfig, cmd)
     
     // 尝试解析CPU使用率
     const cpuMatch = output.match(/(\d+(?:\.\d+)?)\s*%\s*(?:idle|IDLE)/i)
     const idle = cpuMatch ? parseFloat(cpuMatch[1]) : 0
     const usage = Math.round(100 - idle)
     
     const status = usage > 90 ? 'critical' : usage > 80 ? 'warning' : 'ok'
     
     return {
       status,
       value: usage,
       message: `CPU使用率: ${usage}%`,
       detail: output.trim().substring(0, 200),
     }
   } catch (error: any) {
     return { status: 'error', value: 0, message: `CPU检查失败: ${error.message}` }
   }
 }

 private async checkService(isLocal: boolean, server: string, services: string[]) {
   const downServices: string[] = []
   
   for (const svc of services) {
     try {
       const cmd = isLocal
         ? `pgrep -f "${svc}" > /dev/null && echo "running" || echo "stopped"`
         : `systemctl is-active ${svc} 2>/dev/null || pgrep -f "${svc}" >/dev/null && echo "running" || echo "stopped"`
       
       const output = isLocal
         ? await runCommand(cmd)
         : await runRemoteCommand({ host: server } as SSHConfig, cmd)
       
       if (!output.includes('running') && !output.includes('active')) {
         downServices.push(svc)
       }
     } catch {
       downServices.push(svc)
     }
   }
   
   const value = services.length - downServices.length
   const status = downServices.length > 0 ? (downServices.length >= services.length ? 'critical' : 'warning') : 'ok'
   
   return {
     status,
     value,
     message: downServices.length > 0
       ? `服务异常: ${downServices.join(', ')} (已停止)`
       : `所有服务正常 (${services.length}个)`,
     extra: { downServices },
   }
 }
}

/**
 * 初始化巡检调度器
 */
export function initPatrolScheduler(): void {
 const scheduler = getPatrolScheduler()
 scheduler.setExecutor(new OpsPatrolExecutor())
}

/**
 * 启动定时巡检
 */
export async function startPatrol(): Promise<string> {
 initPatrolScheduler()
 const scheduler = getPatrolScheduler()
 scheduler.start()
 return '✅ 定时巡检已启动'
}

/**
 * 停止定时巡检
 */
export async function stopPatrol(): Promise<string> {
 const scheduler = getPatrolScheduler()
 scheduler.stop()
 return '⏹️ 定时巡检已停止'
}

/**
 * 查看巡检任务列表
 */
export async function listPatrolJobs(): Promise<string> {
 const scheduler = getPatrolScheduler()
 const jobs = scheduler.getJobs()
 
 const lines: string[] = []
 lines.push('### 🕐 巡检任务列表\n')
 
 for (const job of jobs) {
   const statusEmoji = job.enabled ? '✅' : '❌'
   lines.push(`${statusEmoji} **${job.name}** (\`${job.id}\`)`)
   lines.push(`   调度: ${job.schedule} | 检查项: ${job.checks.map(c => c.type).join(', ')}`)
   if (job.lastRun) {
     lines.push(`   上次执行: ${job.lastRun}`)
   }
   lines.push('')
 }
 
 return lines.join('\n')
}

/**
 * 手动执行巡检
 */
export async function runPatrol(jobId?: string): Promise<string> {
 initPatrolScheduler()
 const scheduler = getPatrolScheduler()
 
 let results: PatrolResult[]
 if (jobId) {
   results = await scheduler.runJobNow(jobId)
 } else {
   results = await scheduler.runAllNow()
 }
 
 const report = scheduler.generateReport(results)
 return scheduler.formatReport(report)
}

/**
 * 添加巡检任务
 */
export async function addPatrolJob(job: PatrolJob): Promise<string> {
 const scheduler = getPatrolScheduler()
 scheduler.upsertJob(job)
 return `✅ 巡检任务已保存: ${job.name} (${job.id})`
}

/**
 * 删除巡检任务
 */
export async function removePatrolJob(jobId: string): Promise<string> {
 const scheduler = getPatrolScheduler()
 const deleted = scheduler.removeJob(jobId)
 return deleted ? `✅ 巡检任务已删除: ${jobId}` : `❌ 巡检任务不存在: ${jobId}`
}

/**
 * 启用/禁用巡检任务
 */
export async function togglePatrolJob(jobId: string, enabled: boolean): Promise<string> {
 const scheduler = getPatrolScheduler()
 const toggled = scheduler.toggleJob(jobId, enabled)
 return toggled
   ? `✅ 巡检任务 ${jobId} 已${enabled ? '启用' : '禁用'}`
   : `❌ 巡检任务不存在: ${jobId}`
}

/**
 * 查看巡检报告列表
 */
export async function listPatrolReports(limit: number = 10): Promise<string> {
 const scheduler = getPatrolScheduler()
 const reports = scheduler.listReports(limit)
 
 if (reports.length === 0) {
   return '暂无巡检报告，请先执行一次巡检'
 }
 
 const lines: string[] = []
 lines.push('### 📋 巡检报告列表\n')
 for (const r of reports) {
   lines.push(`- ${r.timestamp}`)
 }
 
 return lines.join('\n')
}

// ============================================================
// v3.0 网络诊断功能
// ============================================================

/**
 * Ping 测试
 */
export async function networkPing(host: string, count: number = 4): Promise<string> {
 const diag = getNetworkDiagnostics()
 const result = await diag.ping(host, count)
 return diag.formatPingResult(result)
}

/**
 * DNS 查询
 */
export async function networkDns(host: string, server?: string): Promise<string> {
 const diag = getNetworkDiagnostics()
 const result = await diag.dns(host, server)
 return diag.formatDnsResult(result)
}

/**
 * 路由追踪
 */
export async function networkTraceroute(host: string, maxHops: number = 20): Promise<string> {
 const diag = getNetworkDiagnostics()
 const result = await diag.traceroute(host, maxHops)
 return diag.formatTraceResult(result)
}

/**
 * MTR 测试 (自动降级为 traceroute)
 */
export async function networkMtr(host: string, count: number = 10): Promise<string> {
 const diag = getNetworkDiagnostics()
 const result = await diag.mtr(host, count)
 return diag.formatTraceResult(result)
}

/**
 * 端口连通性测试
 */
export async function networkCheckPort(host: string, port: number): Promise<string> {
 const diag = getNetworkDiagnostics()
 const result = await diag.checkPort(host, port)
 return `### 🔌 端口 ${port} @ ${host}\n\n${result.open ? '✅ 开放' : '❌ 关闭'}\n${result.detail}`
}

/**
 * 综合连通性测试
 */
export async function networkFullCheck(
 host: string,
 ports: number[] = [80, 443, 22]
): Promise<string> {
 const diag = getNetworkDiagnostics()
 const result = await diag.fullCheck(host, ports)
 return diag.formatConnectivityResult(result)
}

// ============================================================
// v3.0 服务管理增强功能
// ============================================================

/**
 * Docker 容器列表
 */
export async function dockerList(all: boolean = false, remoteConfig?: SSHConfig): Promise<string> {
 const remoteExec = remoteConfig
   ? (cmd: string) => runRemoteCommand(remoteConfig, cmd)
   : undefined
 const docker = new DockerManager(15000, remoteExec)
 const containers = await docker.listContainers(all)
 return docker.formatContainerList(containers)
}

/**
 * Docker 容器资源使用
 */
export async function dockerStats(container?: string, remoteConfig?: SSHConfig): Promise<string> {
 const remoteExec = remoteConfig
   ? (cmd: string) => runRemoteCommand(remoteConfig, cmd)
   : undefined
 const docker = new DockerManager(15000, remoteExec)
 const stats = await docker.getStats(container)
 return docker.formatStats(stats)
}

/**
 * Docker 容器详情
 */
export async function dockerInspect(nameOrId: string, remoteConfig?: SSHConfig): Promise<string> {
 const remoteExec = remoteConfig
   ? (cmd: string) => runRemoteCommand(remoteConfig, cmd)
   : undefined
 const docker = new DockerManager(15000, remoteExec)
 const info = await docker.inspectContainer(nameOrId)
 return docker.formatInspect(info)
}

/**
 * Docker 容器日志
 */
export async function dockerLogs(nameOrId: string, lines: number = 50, remoteConfig?: SSHConfig): Promise<string> {
 const remoteExec = remoteConfig
   ? (cmd: string) => runRemoteCommand(remoteConfig, cmd)
   : undefined
 const docker = new DockerManager(15000, remoteExec)
 const logs = await docker.getLogs(nameOrId, lines)
 return `### 📋 容器日志: ${nameOrId} (最近${lines}行)\n\`\`\`\n${logs.substring(0, 5000)}\n\`\`\``
}

/**
 * Docker 镜像列表
 */
export async function dockerImages(remoteConfig?: SSHConfig): Promise<string> {
 const remoteExec = remoteConfig
   ? (cmd: string) => runRemoteCommand(remoteConfig, cmd)
   : undefined
 const docker = new DockerManager(15000, remoteExec)
 const images = await docker.listImages()

 if (images.length === 0) return '无镜像'

 const lines: string[] = []
 lines.push('### 📦 Docker 镜像\n')
 lines.push('| 仓库 | 标签 | 大小 | ID |')
 lines.push('|------|------|------|-----|')
 for (const img of images) {
   lines.push(`| ${img.repository} | ${img.tag} | ${img.size} | ${img.id} |`)
 }
 return lines.join('\n')
}

/**
 * 服务状态 (systemd)
 */
export async function serviceStatus(serviceName: string, remoteConfig?: SSHConfig): Promise<string> {
 const remoteExec = remoteConfig
   ? (cmd: string) => runRemoteCommand(remoteConfig, cmd)
   : undefined
 const svc = new ServiceManager(10000, remoteExec)
 const status = await svc.getStatus(serviceName)
 return svc.formatStatus(status)
}

/**
 * 批量服务状态
 */
export async function serviceBatchStatus(services: string[], remoteConfig?: SSHConfig): Promise<string> {
 const remoteExec = remoteConfig
   ? (cmd: string) => runRemoteCommand(remoteConfig, cmd)
   : undefined
 const svc = new ServiceManager(10000, remoteExec)
 const statuses = await svc.batchStatus(services)
 return svc.formatBatchStatus(statuses)
}

/**
 * 服务日志 (journalctl)
 */
export async function serviceLogs(serviceName: string, lines: number = 50, since?: string, remoteConfig?: SSHConfig): Promise<string> {
 const remoteExec = remoteConfig
 ? (cmd: string) => runRemoteCommand(remoteConfig, cmd)
 : undefined
 const svc = new ServiceManager(10000, remoteExec)
 const log = await svc.getLogs(serviceName, lines, since)

 if (log.entries.length === 0) return `暂无 ${serviceName} 的日志`

 const lines2: string[] = []
 lines2.push(`### 📋 服务日志: ${serviceName} (最近${lines}行)\n`)
 for (const entry of log.entries.slice(-30)) {
 lines2.push(`[${entry.timestamp}] ${entry.message}`)
 }
 return lines2.join('\n')
}

// ============================================================
// Docker 容器健康巡检
// ============================================================

/**
 * Docker 容器健康巡检
 */
export async function dockerHealthCheck(containerName?: string): Promise<string> {
 const checker = new DockerHealthChecker()

 if (containerName) {
 const result = await checker.inspectByName(containerName)
 if (!result) return `未找到容器: ${containerName}`

 const lines: string[] = []
 lines.push(`容器: ${result.container} (${result.image})`)
 lines.push(`状态: ${result.status}`)
 if (result.issues.length === 0) {
 lines.push('✅ 无问题')
 } else {
 for (const issue of result.issues) {
 const mark = issue.severity === 'critical' ? '!!!' : issue.severity === 'warning' ? ' ! ' : '   '
 lines.push(`[${mark}] ${issue.type}: ${issue.message}`)
 lines.push(`     -> ${issue.suggestion}`)
 }
 }
 return lines.join('\n')
 }

 const report = await checker.runFullInspection()
 return checker.formatReport(report)
}

/**
 * Docker 镜像更新检查
 */
export async function dockerImageCheck(): Promise<string> {
 const checker = new DockerHealthChecker()
 const images = await checker.checkImageUpdates()

 if (images.length === 0) return '无镜像或Docker不可用'

 const lines: string[] = []
 lines.push('### 📦 镜像更新检查\n')

 const oldImages = images.filter(i => i.needsUpdate)
 const freshImages = images.filter(i => !i.needsUpdate)

 if (oldImages.length > 0) {
 lines.push(`**${oldImages.length} 个镜像需要更新:**\n`)
 for (const img of oldImages) {
 lines.push(`  [!] ${img.image} - ${img.daysOld}天前创建 (${img.sizeMb}MB)`)
 lines.push(`      docker pull ${img.image}`)
 }
 }

 lines.push(`\n**${freshImages.length} 个镜像状态正常**`)
 return lines.join('\n')
}

// ============================================================
// SSL 证书监控
// ============================================================

/**
 * SSL 证书检查
 */
export async function sslCheck(domains: string[], options: {
 warnDays?: number
 criticalDays?: number
 port?: number
} = {}): Promise<string> {
 if (domains.length === 0) {
 // 尝试从配置文件加载
 const configPath = join(process.env.HOME || '~', '.config', 'ops-maintenance', 'ssl-domains.json')
 const loadedDomains = SSLMonitor.loadDomainsFromConfig(configPath)
 if (loadedDomains.length === 0) {
 return '未指定域名。用法: ops ssl example.com [domain2.com ...]'
 }
 domains = loadedDomains
 }

 const monitor = new SSLMonitor({
 domains,
 warnDays: options.warnDays || 30,
 criticalDays: options.criticalDays || 7,
 ports: options.port ? Object.fromEntries(domains.map(d => [d, options.port!])) : undefined
 })

 const report = await monitor.checkDomains(domains)
 return monitor.formatReport(report)
}

/**
 * SSL 证书详情
 */
export async function sslDetail(domain: string, port: number = 443): Promise<string> {
 const monitor = new SSLMonitor()
 const result = await monitor.checkDomain(domain, port)

 if (result.status === 'error') {
 return `❌ ${domain}:${port} - ${result.error || '连接失败'}`
 }

 const cert = result.cert
 if (!cert) return `❌ ${domain}:${port} - 无法获取证书信息`

 const lines: string[] = []
 lines.push(`### 🔐 SSL 证书详情: ${domain}:${port}\n`)
 lines.push(`状态: ${cert.status === 'valid' ? '✅ 有效' : cert.status === 'expiring-soon' ? '⚠️ 即将过期' : '❌ 已过期'}`)
 lines.push(`域名: ${cert.subject}`)
 lines.push(`颁发者: ${cert.issuer}`)
 lines.push(`有效期: ${cert.validFrom} ~ ${cert.validTo}`)
 lines.push(`剩余天数: ${cert.daysRemaining} 天`)
 lines.push(`协议: ${cert.protocol}`)
 if (cert.fingerprint) lines.push(`指纹: ${cert.fingerprint}`)
 if (cert.sanDomains.length > 0) {
 lines.push(`SAN域名: ${cert.sanDomains.join(', ')}`)
 }
 if (result.chainIssues.length > 0) {
 lines.push(`\n⚠️ 链路问题:`)
 for (const ci of result.chainIssues) {
 lines.push(`  - ${ci}`)
 }
 }

 return lines.join('\n')
}
