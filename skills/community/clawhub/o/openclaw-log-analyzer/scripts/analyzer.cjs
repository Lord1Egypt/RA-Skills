#!/usr/bin/env node

/**
 * Log Analyzer - 日志分析工具
 * 
 * 功能：
 * 1. 扫描 OpenClaw 日志文件
 * 2. 检测错误模式
 * 3. 分析性能指标
 * 4. 生成报告
 * 5. 推送到 Discord
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const CONFIG = {
  logDirectory: '/Users/xufan65/.openclaw/logs',
  statusFile: '/Users/xufan65/.openclaw/workspace/memory/log-analyzer-status.json',
  cronJobsFile: '/Users/xufan65/.openclaw/cron/jobs.json',
  notifyChannel: 'discord',
  notifyTo: 'channel:1478698808631361647'
};

// 错误模式
const ERROR_PATTERNS = [
  { pattern: /ERROR|CRITICAL|FATAL/i, type: 'error', severity: 'high' },
  { pattern: /timeout|timed out/i, type: 'timeout', severity: 'medium' },
  { pattern: /failed|failure|fail/i, type: 'failure', severity: 'high' }
];

// 警告模式
const WARN_PATTERNS = [
  { pattern: /WARN|WARNING/i, type: 'warning', severity: 'medium' },
  { pattern: /slow|performance/i, type: 'performance', severity: 'low' }
];

class LogAnalyzer {
  constructor() {
    this.errors = [];
    this.warnings = [];
    this.performance = [];
    this.failedTasks = [];
    this.status = this.loadStatus();
  }

  /**
   * 加载状态
   */
  loadStatus() {
    try {
      if (fs.existsSync(CONFIG.statusFile)) {
        return JSON.parse(fs.readFileSync(CONFIG.statusFile, 'utf8'));
      }
    } catch (e) {
      console.error('加载状态失败:', e.message);
    }
    return { 
      lastScan: null, 
      errorCount: 0, 
      warningCount: 0,
      failedTaskCount: 0 
    };
  }

  /**
   * 保存状态
   */
  saveStatus() {
    try {
      const status = {
        lastScan: new Date().toISOString(),
        errorCount: this.errors.length,
        warningCount: this.warnings.length,
        failedTaskCount: this.failedTasks.length
      };
      fs.writeFileSync(CONFIG.statusFile, JSON.stringify(status, null, 2));
    } catch (e) {
      console.error('保存状态失败:', e.message);
    }
  }

  /**
   * 创建日志目录
   */
  createLogDirectory() {
    try {
      if (!fs.existsSync(CONFIG.logDirectory)) {
        fs.mkdirSync(CONFIG.logDirectory, { recursive: true });
        console.log(`✅ 创建日志目录: ${CONFIG.logDirectory}`);
      }
    } catch (e) {
      console.error('创建日志目录失败:', e.message);
    }
  }

  /**
   * 扫描日志目录
   */
  scanLogDirectory() {
    console.log('📁 扫描日志目录...\n');
    
    try {
      if (!fs.existsSync(CONFIG.logDirectory)) {
        console.log(`⚠️  日志目录不存在: ${CONFIG.logDirectory}`);
        this.createLogDirectory();
        return;
      }
      
      const logFiles = fs.readdirSync(CONFIG.logDirectory)
        .filter(file => file.endsWith('.log'))
        .sort((a, b) => b.localeCompare(a));
      
      console.log(`✅ 找到 ${logFiles.length} 个日志文件\n`);
      
      logFiles.forEach(file => {
        this.analyzeLogFile(path.join(CONFIG.logDirectory, file));
      });
    } catch (e) {
      console.error('❌ 扫描日志失败:', e.message);
    }
  }

  /**
   * 分析日志文件
   */
  analyzeLogFile(filePath) {
    try {
      const content = fs.readFileSync(filePath, 'utf8');
      const lines = content.split('\n');
      
      console.log(`📄 分析: ${path.basename(filePath)} (${lines.length} 行)`);
      
      lines.forEach((line, index) => {
        this.analyzeLine(line, index, filePath);
      });
    } catch (e) {
      console.error(`❌ 分析文件失败 ${path.basename(filePath)}:`, e.message);
    }
  }

  /**
   * 分析日志行
   */
  analyzeLine(line, lineNumber, filePath) {
    // 检测错误
    for (const errorPattern of ERROR_PATTERNS) {
      if (errorPattern.pattern.test(line)) {
        this.errors.push({
          timestamp: new Date().toISOString(),
          file: path.basename(filePath),
          line: lineNumber + 1,
          content: line.trim(),
          type: errorPattern.type,
          severity: errorPattern.severity
        });
        return;
      }
    }
    
    // 检测警告
    for (const warnPattern of WARN_PATTERNS) {
      if (warnPattern.pattern.test(line)) {
        this.warnings.push({
          timestamp: new Date().toISOString(),
          file: path.basename(filePath),
          line: lineNumber + 1,
          content: line.trim(),
          type: warnPattern.type,
          severity: warnPattern.severity
        });
        return;
      }
    }
    
    // 检测性能指标
    const perfMatch = line.match(/duration.*?(\d+\.?\d*)\s*(ms|s)/i);
    if (perfMatch) {
      const duration = parseFloat(perfMatch[1]);
      this.performance.push({
        timestamp: new Date().toISOString(),
        file: path.basename(filePath),
        duration: duration,
        unit: perfMatch[2]
      });
    }
  }

  /**
   * 诊断失败任务
   */
  diagnoseFailedTasks() {
    console.log('\n🔍 诊断失败任务...\n');
    
    try {
      if (!fs.existsSync(CONFIG.cronJobsFile)) {
        console.log('⚠️  Cron jobs 文件不存在');
        return;
      }
      
      const jobs = JSON.parse(fs.readFileSync(CONFIG.cronJobsFile, 'utf8')).jobs || [];
      
      const failedJobs = jobs.filter(job => {
        return job.state && job.state.lastStatus === 'error';
      });
      
      if (failedJobs.length > 0) {
        console.log(`❌ 发现 ${failedJobs.length} 个失败任务:\n`);
        failedJobs.forEach(job => {
          const error = job.state.lastError || 'Unknown error';
          console.log(`   • ${job.name}: ${error}`);
          this.failedTasks.push({
            name: job.name,
            error: error,
            lastRun: job.state.lastRunAt
          });
        });
      } else {
        console.log('✅ 没有发现失败任务');
      }
    } catch (e) {
      console.error('读取 cron jobs 失败:', e.message);
    }
  }

  /**
   * 生成报告
   */
  generateReport() {
    const timestamp = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    
    let report = `# 📊 日志分析报告\n\n`;
    report += `**分析时间**: ${timestamp}\n\n`;
    
    // 失败任务摘要
    if (this.failedTasks.length > 0) {
      report += `## ❌ 失败任务 (${this.failedTasks.length} 个)\n\n`;
      this.failedTasks.forEach(task => {
        report += `### ${task.name}\n`;
        report += `- **错误**: ${task.error}\n`;
        report += `- **最后运行**: ${task.lastRun || 'Unknown'}\n\n`;
      });
    }
    
    // 错误摘要
    if (this.errors.length > 0) {
      report += `## ❌ 错误 (${this.errors.length} 个)\n\n`;
      this.errors.slice(0, 5).forEach(error => {
        report += `### ${error.type} [${error.severity}]\n`;
        report += `- **文件**: ${error.file}:${error.line}\n`;
        report += `- **内容**: ${error.content}\n\n`;
      });
    } else {
      report += `## ✅ 没有发现错误\n\n`;
    }
    
    // 警告摘要
    if (this.warnings.length > 0) {
      report += `## ⚠️ 警告 (${this.warnings.length} 个)\n\n`;
      this.warnings.slice(0, 3).forEach(warning => {
        report += `### ${warning.type} [${warning.severity}]\n`;
        report += `- **文件**: ${warning.file}:${warning.line}\n`;
        report += `- **内容**: ${warning.content}\n\n`;
      });
    } else {
      report += `## ✅ 没有发现警告\n\n`;
    }
    
    // 性能摘要
    if (this.performance.length > 0) {
      const avgDuration = this.performance.reduce((sum, p) => sum + p.duration, 0) / this.performance.length;
      const maxDuration = Math.max(...this.performance.map(p => p.duration));
      const minDuration = Math.min(...this.performance.map(p => p.duration));
      
      report += `## ⏱️ 性能指标\n\n`;
      report += `- **平均响应时间**: ${avgDuration.toFixed(2)}s\n`;
      report += `- **最大响应时间**: ${maxDuration.toFixed(2)}s\n`;
      report += `- **最小响应时间**: ${minDuration.toFixed(2)}s\n`;
      report += `- **总请求数**: ${this.performance.length}\n\n`;
    }
    
    return report;
  }

  /**
   * 发送到 Discord
   */
  sendToDiscord(report) {
    try {
      // 使用 message tool 发送
      const message = report.substring(0, 1900); // Discord 限制
      execSync(`openclaw notify --channel ${CONFIG.notifyChannel} --to "${CONFIG.notifyTo}" --message "${message}"`, { 
        encoding: 'utf8' 
      });
      console.log('\n✅ 报告已推送到 Discord');
    } catch (e) {
      console.error('\n❌ 推送到 Discord 失败:', e.message);
    }
  }

  /**
   * 主运行函数
   */
  run() {
    console.log('🚀 Log Analyzer 启动\n');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

    // 1. 扫描日志
    this.scanLogDirectory();

    // 2. 诊断失败任务
    this.diagnoseFailedTasks();

    // 3. 保存状态
    this.saveStatus();

    // 4. 生成报告
    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    const report = this.generateReport();
    console.log(report);

    // 5. 发送到 Discord
    this.sendToDiscord(report);

    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    console.log('✅ Log Analyzer 完成\n');
  }
}

// 运行
if (require.main === module) {
  const analyzer = new LogAnalyzer();
  analyzer.run();
}

module.exports = LogAnalyzer;
