#!/usr/bin/env node

/**
 * OpenClaw性能监控脚本
 * 基于B站视频《OpenClaw 卡顿、响应慢？一条提示词让它提速 95%》的学习
 */

const fs = require('fs');
const path = require('path');
const readline = require('readline');

console.log('📊 OpenClaw性能监控控制台');
console.log('='.repeat(60));
console.log('基于《OpenClaw 卡顿、响应慢？一条提示词让它提速 95%》');
console.log('='.repeat(60));

class PerformanceMonitor {
  constructor() {
    this.metrics = {
      startTime: Date.now(),
      requestCount: 0,
      responseTimes: [],
      memoryReadings: [],
      errors: [],
      warnings: []
    };
    
    this.logDir = path.join(process.cwd(), 'openclaw-performance-skill', 'logs');
    this.ensureLogDirectory();
    
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    
    this.isMonitoring = false;
    this.monitorInterval = null;
  }
  
  ensureLogDirectory() {
    if (!fs.existsSync(this.logDir)) {
      fs.mkdirSync(this.logDir, { recursive: true });
    }
  }
  
  async start() {
    console.log('\n🔍 初始化监控系统...');
    
    // 启动指标收集
    this.startMetricCollection();
    
    // 显示菜单
    this.showMenu();
  }
  
  startMetricCollection() {
    console.log('📈 启动指标收集...');
    
    this.isMonitoring = true;
    this.monitorInterval = setInterval(() => {
      this.collectMetrics();
    }, 5000); // 每5秒收集一次
    
    console.log('✅ 指标收集已启动');
  }
  
  collectMetrics() {
    const timestamp = Date.now();
    
    // 收集内存指标
    const memory = process.memoryUsage();
    this.metrics.memoryReadings.push({
      timestamp,
      heapUsed: memory.heapUsed,
      heapTotal: memory.heapTotal,
      rss: memory.rss,
      external: memory.external
    });
    
    // 模拟请求计数（实际应用中应从OpenClaw获取）
    this.metrics.requestCount += Math.floor(Math.random() * 3);
    
    // 模拟响应时间（实际应用中应测量真实响应时间）
    this.metrics.responseTimes.push({
      timestamp,
      duration: 50 + Math.random() * 150 // 50-200ms
    });
    
    // 保留最近数据
    if (this.metrics.memoryReadings.length > 120) { // 保留10分钟数据
      this.metrics.memoryReadings.shift();
    }
    if (this.metrics.responseTimes.length > 120) {
      this.metrics.responseTimes.shift();
    }
    
    // 记录到日志文件
    this.logMetrics();
  }
  
  logMetrics() {
    const logEntry = {
      timestamp: new Date().toISOString(),
      metrics: {
        requestCount: this.metrics.requestCount,
        memoryMB: Math.round(this.metrics.memoryReadings[this.metrics.memoryReadings.length - 1]?.heapUsed / 1024 / 1024 || 0),
        avgResponseTime: this.calculateAverageResponseTime()
      }
    };
    
    const logFile = path.join(this.logDir, `performance-${new Date().toISOString().split('T')[0]}.log`);
    fs.appendFileSync(logFile, JSON.stringify(logEntry) + '\n');
  }
  
  calculateAverageResponseTime() {
    if (this.metrics.responseTimes.length === 0) return 0;
    
    const sum = this.metrics.responseTimes.reduce((total, rt) => total + rt.duration, 0);
    return Math.round(sum / this.metrics.responseTimes.length);
  }
  
  showMenu() {
    console.log('\n📋 监控菜单:');
    console.log('  1. 📊 查看实时指标');
    console.log('  2. 📝 查看系统日志');
    console.log('  3. 🚨 查看错误日志');
    console.log('  4. ⚡ 性能分析报告');
    console.log('  5. 🔧 优化建议');
    console.log('  6. 📈 实时监控模式');
    console.log('  7. 🚪 退出监控');
    
    this.rl.question('\n请选择选项 (1-7): ', (answer) => {
      this.handleMenuChoice(answer.trim());
    });
  }
  
  handleMenuChoice(choice) {
    switch (choice) {
      case '1':
        this.showRealTimeMetrics();
        break;
      case '2':
        this.showSystemLogs();
        break;
      case '3':
        this.showErrorLogs();
        break;
      case '4':
        this.generatePerformanceReport();
        break;
      case '5':
        this.showOptimizationSuggestions();
        break;
      case '6':
        this.startRealTimeMonitoring();
        break;
      case '7':
        this.exitMonitoring();
        break;
      default:
        console.log('❌ 无效选项，请重新选择');
        this.showMenu();
        break;
    }
  }
  
  showRealTimeMetrics() {
    console.log('\n📊 实时指标');
    console.log('='.repeat(50));
    
    const uptime = Math.round((Date.now() - this.metrics.startTime) / 1000);
    const minutes = Math.floor(uptime / 60);
    const seconds = uptime % 60;
    
    const latestMemory = this.metrics.memoryReadings[this.metrics.memoryReadings.length - 1];
    const memoryMB = latestMemory ? Math.round(latestMemory.heapUsed / 1024 / 1024) : 0;
    const memoryTotalMB = latestMemory ? Math.round(latestMemory.heapTotal / 1024 / 1024) : 0;
    
    const avgResponse = this.calculateAverageResponseTime();
    const requestRate = uptime > 0 ? (this.metrics.requestCount / uptime).toFixed(2) : 0;
    
    console.log(`⏱️  运行时间: ${minutes}分${seconds}秒`);
    console.log(`📊 总请求数: ${this.metrics.requestCount}`);
    console.log(`📈 请求频率: ${requestRate} 请求/秒`);
    console.log(`💾 内存使用: ${memoryMB}MB / ${memoryTotalMB}MB (${memoryTotalMB > 0 ? Math.round(memoryMB / memoryTotalMB * 100) : 0}%)`);
    console.log(`⚡ 平均响应: ${avgResponse}ms`);
    
    // 显示最近响应时间趋势
    if (this.metrics.responseTimes.length > 5) {
      const recentTimes = this.metrics.responseTimes.slice(-5).map(rt => rt.duration);
      const minRecent = Math.min(...recentTimes);
      const maxRecent = Math.max(...recentTimes);
      console.log(`📉 最近响应: ${minRecent}-${maxRecent}ms`);
    }
    
    // 显示内存趋势
    if (this.metrics.memoryReadings.length > 10) {
      const recentMemory = this.metrics.memoryReadings.slice(-10).map(m => m.heapUsed);
      const minMemory = Math.min(...recentMemory);
      const maxMemory = Math.max(...recentMemory);
      console.log(`📈 内存趋势: ${Math.round(minMemory / 1024 / 1024)}-${Math.round(maxMemory / 1024 / 1024)}MB`);
    }
    
    console.log('\n' + '='.repeat(50));
    this.returnToMenu();
  }
  
  showSystemLogs() {
    console.log('\n📝 系统日志');
    console.log('='.repeat(50));
    
    const logFile = path.join(this.logDir, `performance-${new Date().toISOString().split('T')[0]}.log`);
    
    if (fs.existsSync(logFile)) {
      const logs = fs.readFileSync(logFile, 'utf8').split('\n').filter(line => line.trim());
      const recentLogs = logs.slice(-10); // 显示最近10条日志
      
      if (recentLogs.length > 0) {
        console.log('最近10条日志记录:');
        recentLogs.forEach((log, index) => {
          try {
            const entry = JSON.parse(log);
            const time = new Date(entry.timestamp).toLocaleTimeString();
            console.log(`  ${index + 1}. [${time}] 请求: ${entry.metrics.requestCount}, 内存: ${entry.metrics.memoryMB}MB, 响应: ${entry.metrics.avgResponseTime}ms`);
          } catch {
            console.log(`  ${index + 1}. ${log.substring(0, 80)}...`);
          }
        });
      } else {
        console.log('暂无日志记录');
      }
    } else {
      console.log('日志文件不存在');
    }
    
    console.log('\n' + '='.repeat(50));
    console.log(`日志文件: ${logFile}`);
    this.returnToMenu();
  }
  
  showErrorLogs() {
    console.log('\n🚨 错误日志');
    console.log('='.repeat(50));
    
    const errorLogs = this.metrics.errors;
    
    if (errorLogs.length > 0) {
      console.log(`发现 ${errorLogs.length} 个错误:`);
      errorLogs.forEach((error, index) => {
        console.log(`  ${index + 1}. [${new Date(error.timestamp).toLocaleTimeString()}] ${error.message}`);
        if (error.details) {
          console.log(`     详情: ${error.details}`);
        }
      });
    } else {
      console.log('✅ 未发现错误');
    }
    
    // 显示警告
    const warnings = this.metrics.warnings;
    if (warnings.length > 0) {
      console.log(`\n⚠️  发现 ${warnings.length} 个警告:`);
      warnings.slice(-5).forEach((warning, index) => {
        console.log(`  ${index + 1}. [${new Date(warning.timestamp).toLocaleTimeString()}] ${warning.message}`);
      });
    }
    
    console.log('\n' + '='.repeat(50));
    this.returnToMenu();
  }
  
  generatePerformanceReport() {
    console.log('\n⚡ 性能分析报告');
    console.log('='.repeat(50));
    
    const uptime = Math.round((Date.now() - this.metrics.startTime) / 1000);
    const requestRate = uptime > 0 ? (this.metrics.requestCount / uptime).toFixed(2) : 0;
    
    console.log('📈 性能概览:');
    console.log(`  • 监控时长: ${uptime}秒`);
    console.log(`  • 总请求数: ${this.metrics.requestCount}`);
    console.log(`  • 平均请求率: ${requestRate} 请求/秒`);
    
    // 内存分析
    if (this.metrics.memoryReadings.length > 0) {
      const memoryValues = this.metrics.memoryReadings.map(m => m.heapUsed);
      const maxMemory = Math.max(...memoryValues);
      const minMemory = Math.min(...memoryValues);
      const avgMemory = memoryValues.reduce((sum, val) => sum + val, 0) / memoryValues.length;
      
      console.log('\n💾 内存分析:');
      console.log(`  • 最大内存: ${Math.round(maxMemory / 1024 / 1024)}MB`);
      console.log(`  • 最小内存: ${Math.round(minMemory / 1024 / 1024)}MB`);
      console.log(`  • 平均内存: ${Math.round(avgMemory / 1024 / 1024)}MB`);
      console.log(`  • 内存波动: ${Math.round((maxMemory - minMemory) / 1024 / 1024)}MB`);
      
      // 内存使用评级
      const avgMemoryMB = Math.round(avgMemory / 1024 / 1024);
      let memoryRating;
      if (avgMemoryMB < 500) memoryRating = '🟢 优秀';
      else if (avgMemoryMB < 1000) memoryRating = '🟡 良好';
      else if (avgMemoryMB < 2000) memoryRating = '🟠 一般';
      else memoryRating = '🔴 需要优化';
      
      console.log(`  • 内存评级: ${memoryRating}`);
    }
    
    // 响应时间分析
    if (this.metrics.responseTimes.length > 0) {
      const responseValues = this.metrics.responseTimes.map(rt => rt.duration);
      const maxResponse = Math.max(...responseValues);
      const minResponse = Math.min(...responseValues);
      const avgResponse = responseValues.reduce((sum, val) => sum + val, 0) / responseValues.length;
      
      // 计算P95响应时间
      const sortedResponses = [...responseValues].sort((a, b) => a - b);
      const p95Index = Math.floor(sortedResponses.length * 0.95);
      const p95Response = sortedResponses[p95Index];
      
      console.log('\n⚡ 响应时间分析:');
      console.log(`  • 最快响应: ${Math.round(minResponse)}ms`);
      console.log(`  • 最慢响应: ${Math.round(maxResponse)}ms`);
      console.log(`  • 平均响应: ${Math.round(avgResponse)}ms`);
      console.log(`  • P95响应: ${Math.round(p95Response)}ms`);
      
      // 响应时间评级
      let responseRating;
      if (avgResponse < 100) responseRating = '🟢 优秀';
      else if (avgResponse < 300) responseRating = '🟡 良好';
      else if (avgResponse < 1000) responseRating = '🟠 一般';
      else responseRating = '🔴 需要优化';
      
      console.log(`  • 响应评级: ${responseRating}`);
    }
    
    // 生成建议
    console.log('\n💡 优化建议:');
    const suggestions = this.generatePerformanceSuggestions();
    suggestions.forEach((suggestion, index) => {
      console.log(`  ${index + 1}. ${suggestion}`);
    });
    
    console.log('\n' + '='.repeat(50));
    this.returnToMenu();
  }
  
  generatePerformanceSuggestions() {
    const suggestions = [];
    
    // 基于B站视频的优化建议
    suggestions.push('使用 /compact 命令手动压缩上下文');
    suggestions.push('配置自动上下文压缩，设置triggerAtPercent: 75');
    suggestions.push('优化流式模式，使用chunked或full模式');
    suggestions.push('缩短上下文TTL至5分钟');
    suggestions.push('限制最大对话轮数为3轮');
    suggestions.push('启用内存限制，设置max_heap_mb: 2048');
    
    // 基于监控数据的建议
    if (this.metrics.memoryReadings.length > 0) {
      const latestMemory = this.metrics.memoryReadings[this.metrics.memoryReadings.length - 1];
      const memoryMB = Math.round(latestMemory.heapUsed / 1024 / 1024);
      
      if (memoryMB > 1000) {
        suggestions.push(`当前内存使用较高 (${memoryMB}MB)，建议优化内存管理`);
      }
    }
    
    if (this.metrics.responseTimes.length > 0) {
      const avgResponse = this.calculateAverageResponseTime();
      if (avgResponse > 300) {
        suggestions.push(`响应时间较慢 (${avgResponse}ms)，建议优化配置和提示词`);
      }
    }
    
    return suggestions.slice(0, 5); // 返回前5条建议
  }
  
  showOptimizationSuggestions() {
    console.log('\n🔧 优化建议');
    console.log('='.repeat(50));
    console.log('基于《OpenClaw 卡顿、响应慢？一条提示词让它提速 95%》视频内容:');
    console.log('');
    
    const videoSuggestions = [
      '🚀 更新到最新OpenClaw版本',
      '🧹 定期使用 /compact 压缩上下文',
      '⚡ 配置自动上下文压缩 (triggerAtPercent: 75)',
      '📨 优化流式模式 (使用chunked或full)',
      '💾 缩短上下文TTL至5分钟',
      '🔢 限制最大对话轮数为3轮',
      '🧠 启用智能上下文修剪',
      '🔄 配置代理解决国内访问延迟',
      '📊 启用本地向量数据库',
      '⚙️ 优化数据库连接池'
    ];
    
    videoSuggestions.forEach((suggestion, index) => {
      console.log(`  ${index + 1}. ${suggestion}`);
    });
    
    console.log('\n📚 参考资源:');
    console.log('  • B站视频: 《OpenClaw 卡顿、响应慢？一条提示词让它提速 95%》');
    console.log('  • 官方文档: https://docs.openclaw.ai/performance');
    console.log('  • 社区讨论: https://github.com/openclaw/openclaw/discussions');
    
    console.log('\n' + '='.repeat(50));
    this.returnToMenu();
  }
  
  startRealTimeMonitoring() {
    console.log('\n📈 实时监控模式');
    console.log('='.repeat(50));
    console.log('开始实时监控，每5秒更新一次指标');
    console.log('按任意键返回菜单');
    console.log('='.repeat(50));
    
    // 设置原始模式以捕获按键
    process.stdin.setRawMode(true);
    process.stdin.resume();
    
    let updateCount = 0;
    const updateInterval = setInterval(() => {
      updateCount++;
      this.displayRealTimeMetrics(updateCount);
    }, 5000);
    
    // 监听按键
    process.stdin.once('data', () => {
      clearInterval(updateInterval);
      process.stdin.setRawMode(false);
      process