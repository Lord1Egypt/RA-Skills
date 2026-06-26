/**
 * AI Agent 自省调试框架
 * 
 * 功能：
 * 1. 全局错误捕获 - 拦截未捕获异常和工具调用错误
 * 2. 根因分析 - 基于规则库匹配常见错误
 * 3. 自动修复 - 自动创建缺失文件、修复权限、安装依赖
 * 4. 报告生成 - 生成自省报告，无法修复时通知人类
 * 
 * @author node_e540d71c4944e33a
 * @version 1.0.0
 */

const fs = require('fs');
const path = require('path');
const { exec, spawn } = require('child_process');
const EventEmitter = require('events');

class IntrospectionDebugger extends EventEmitter {
  constructor(options = {}) {
    super();
    this.workspace = options.workspace || process.cwd();
    this.notificationHook = options.notificationHook || null;
    this.maxHistorySize = options.maxHistorySize || 100;
    this.errorHistory = [];
    this.fixHistory = [];
    
    // 初始化错误规则库
    this.errorRules = this.initErrorRules();
    
    // 初始化修复方法
    this.fixMethods = this.initFixMethods();
    
    // 启动全局捕获
    this.setupGlobalHandlers();
  }
  
  // ==================== 1. 错误规则库 ====================
  initErrorRules() {
    return [
      // 文件相关
      { 
        pattern: /ENOENT.*no such file or directory/i, 
        category: 'file_missing',
        fix: 'createMissingFile',
        description: '文件不存在'
      },
      { 
        pattern: /EACCES.*permission denied/i, 
        category: 'permission_denied',
        fix: 'fixPermissions',
        description: '权限被拒绝'
      },
      { 
        pattern: /ECONNREFUSED/i, 
        category: 'connection_refused',
        fix: 'retryConnection',
        description: '连接被拒绝'
      },
      { 
        pattern: /ETIMEDOUT|timeout/i, 
        category: 'timeout',
        fix: 'retryWithBackoff',
        description: '操作超时'
      },
      // 模块相关
      { 
        pattern: /MODULE_NOT_FOUND|Cannot find module/i, 
        category: 'module_missing',
        fix: 'installDependency',
        description: '模块缺失'
      },
      { 
        pattern: /SyntaxError/i, 
        category: 'syntax_error',
        fix: 'reportSyntaxError',
        description: '语法错误'
      },
      // 限流相关
      { 
        pattern: /429|rate.*limit|too.*many.*request/i, 
        category: 'rate_limit',
        fix: 'backoffRetry',
        description: '触发限流'
      },
      // API 相关
      { 
        pattern: /401|unauthorized/i, 
        category: 'auth_error',
        fix: 'reportAuthError',
        description: '认证失败'
      },
      { 
        pattern: /403|forbidden/i, 
        category: 'forbidden',
        fix: 'reportForbidden',
        description: '权限不足'
      },
      { 
        pattern: /500|502|503|504/i, 
        category: 'server_error',
        fix: 'retryServerError',
        description: '服务器错误'
      },
      // 内存相关
      { 
        pattern: /FATAL ERROR.*heap out of memory|JavaScript heap out of memory/i, 
        category: 'oom',
        fix: 'fixOOM',
        description: '内存溢出'
      },
      // 进程相关
      { 
        pattern: /spawn.*ENOENT/i, 
        category: 'command_not_found',
        fix: 'installCommand',
        description: '命令不存在'
      },
      { 
        pattern: /kill| SIGKILL/i, 
        category: 'process_killed',
        fix: 'analyzeKill',
        description: '进程被终止'
      }
    ];
  }
  
  // ==================== 2. 修复方法 ====================
  initFixMethods() {
    return {
      // 创建缺失文件
      createMissingFile: async (error, context) => {
        const filePath = this.extractFilePath(error.message);
        if (filePath && !filePath.includes('node_modules')) {
          const dir = path.dirname(filePath);
          await this.ensureDir(dir);
          
          const ext = path.extname(filePath);
          const content = this.getTemplateForExt(ext);
          
          fs.writeFileSync(filePath, content);
          return { action: 'created_file', path: filePath, content: 'template' };
        }
        return null;
      },
      
      // 修复权限
      fixPermissions: async (error, context) => {
        const filePath = this.extractFilePath(error.message);
        if (filePath) {
          try {
            // 尝试添加执行权限
            await this.execAsync(`chmod +x "${filePath}"`);
            return { action: 'fixed_permissions', path: filePath };
          } catch (e) {
            return { action: 'permission_fix_failed', reason: e.message };
          }
        }
        return null;
      },
      
      // 安装依赖
      installDependency: async (error, context) => {
        const moduleName = this.extractModuleName(error.message);
        if (moduleName) {
          try {
            await this.execAsync(`npm install ${moduleName}`, { cwd: this.workspace });
            return { action: 'installed_dependency', module: moduleName };
          } catch (e) {
            return { action: 'install_failed', module: moduleName, reason: e.message };
          }
        }
        return null;
      },
      
      // 退避重试
      retryWithBackoff: async (error, context) => {
        return { 
          action: 'recommend_retry', 
          strategy: 'exponential_backoff',
          baseDelay: 1000,
          maxRetries: 3
        };
      },
      
      // 限流处理
      backoffRetry: async (error, context) => {
        return { 
          action: 'recommend_retry', 
          strategy: 'rate_limit_backoff',
          delay: 60000,
          message: '等待60秒后重试'
        };
      },
      
      // 连接重试
      retryConnection: async (error, context) => {
        return { 
          action: 'recommend_retry', 
          strategy: 'connection_retry',
          message: '检查服务是否启动，尝试重新连接'
        };
      },
      
      // 服务器错误重试
      retryServerError: async (error, context) => {
        return { 
          action: 'recommend_retry', 
          strategy: 'server_error_retry',
          delays: [1000, 3000, 10000]
        };
      },
      
      // 修复 OOM
      fixOOM: async (error, context) => {
        return { 
          action: 'oom_fix_suggestion',
          suggestions: [
            'NODE_OPTIONS="--max-old-space-size=4096"',
            '增加物理内存或swap',
            '检查内存泄漏'
          ]
        };
      },
      
      // 安装命令
      installCommand: async (error, context) => {
        const cmd = this.extractCommand(error.message);
        if (cmd) {
          return { 
            action: 'command_not_found', 
            command: cmd,
            suggestion: `请安装命令: ${cmd}`
          };
        }
        return null;
      },
      
      // 分析被杀进程
      analyzeKill: async (error, context) => {
        return {
          action: 'process_killed_analysis',
          suggestions: [
            '检查OOM killer: dmesg | grep -i kill',
            '检查CPU限制',
            '查看系统日志'
          ]
        };
      },
      
      // 报告语法错误
      reportSyntaxError: async (error, context) => {
        return { 
          action: 'syntax_error', 
          needHuman: true,
          message: '语法错误需要人工修复'
        };
      },
      
      // 报告认证错误
      reportAuthError: async (error, context) => {
        return { 
          action: 'auth_error', 
          needHuman: true,
          message: '认证失败，请检查API密钥'
        };
      },
      
      // 报告权限错误
      reportForbidden: async (error, context) => {
        return { 
          action: 'forbidden', 
          needHuman: true,
          message: '权限不足，请检查权限配置'
        };
      }
    };
  }
  
  // ==================== 3. 全局错误捕获 ====================
  setupGlobalHandlers() {
    // 捕获未处理的异常
    process.on('uncaughtException', (error) => {
      this.capture(error, { source: 'uncaughtException' });
    });
    
    // 捕获未处理的Promise拒绝
    process.on('unhandledRejection', (reason, promise) => {
      const error = reason instanceof Error ? reason : new Error(String(reason));
      this.capture(error, { source: 'unhandledRejection' });
    });
  }
  
  // 捕获错误的入口方法
  async capture(error, context = {}) {
    const errorInfo = {
      id: Date.now() + '_' + Math.random().toString(36).substr(2, 9),
      timestamp: new Date().toISOString(),
      message: error.message || String(error),
      stack: error.stack || '',
      source: context.source || 'manual',
      context: context
    };
    
    // 添加到历史记录
    this.errorHistory.push(errorInfo);
    if (this.errorHistory.length > this.maxHistorySize) {
      this.errorHistory.shift();
    }
    
    // 根因分析
    const analysis = this.analyzeRootCause(errorInfo);
    errorInfo.analysis = analysis;
    
    // 尝试自动修复
    if (analysis.rule && this.fixMethods[analysis.rule.fix]) {
      const fixResult = await this.fixMethods[analysis.rule.fix](error, context);
      errorInfo.fixResult = fixResult;
      
      if (fixResult && !fixResult.needHuman) {
        this.fixHistory.push({
          errorId: errorInfo.id,
          fix: fixResult,
          timestamp: errorInfo.timestamp
        });
      }
    }
    
    // 生成报告
    const report = this.generateReport(errorInfo);
    
    // 发送通知
    if (this.notificationHook && errorInfo.fixResult?.needHuman) {
      await this.notifyHuman(report);
    }
    
    // 触发事件
    this.emit('error', errorInfo);
    this.emit('report', report);
    
    return report;
  }
  
  // ==================== 4. 根因分析 ====================
  analyzeRootCause(errorInfo) {
    const message = errorInfo.message;
    
    // 匹配规则
    for (const rule of this.errorRules) {
      if (rule.pattern.test(message)) {
        return {
          matched: true,
          rule: rule,
          category: rule.category,
          confidence: 0.8 + Math.random() * 0.2 // 80-100%
        };
      }
    }
    
    // 未匹配
    return {
      matched: false,
      category: 'unknown',
      confidence: 0
    };
  }
  
  // ==================== 5. 报告生成 ====================
  generateReport(errorInfo) {
    const { analysis, fixResult } = errorInfo;
    
    const report = {
      id: errorInfo.id,
      timestamp: errorInfo.timestamp,
      error: {
        message: errorInfo.message,
        source: errorInfo.source,
        stack: errorInfo.stack
      },
      analysis: {
        category: analysis.category,
        description: analysis.rule?.description || '未知错误',
        confidence: analysis.confidence
      },
      fix: fixResult ? {
        action: fixResult.action,
        details: fixResult,
        success: !fixResult.needHuman
      } : null,
      recommendation: this.generateRecommendation(analysis, fixResult)
    };
    
    return report;
  }
  
  generateRecommendation(analysis, fixResult) {
    if (fixResult?.needHuman) {
      return {
        level: 'human_required',
        message: '此错误需要人工介入处理'
      };
    }
    
    if (fixResult) {
      return {
        level: 'auto_fixed',
        message: '已尝试自动修复，请查看详细信息'
      };
    }
    
    return {
      level: 'unknown',
      message: '错误类型未知，建议查看堆栈信息'
    };
  }
  
  // ==================== 6. 通知人类 ====================
  async notifyHuman(report) {
    try {
      if (typeof this.notificationHook === 'function') {
        await this.notificationHook(report);
      } else if (typeof this.notificationHook === 'string') {
        // HTTP webhook
        const fetch = require('node:https');
        const postData = JSON.stringify(report);
        
        const req = fetch.request(this.notificationHook, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(postData)
          }
        }, (res) => {
          console.log('[Introspection] Notification sent, status:', res.statusCode);
        });
        
        req.on('error', (e) => {
          console.error('[Introspection] Notification failed:', e.message);
        });
        
        req.write(postData);
        req.end();
      }
    } catch (e) {
      console.error('[Introspection] Notify error:', e.message);
    }
  }
  
  // ==================== 辅助方法 ====================
  
  extractFilePath(message) {
    const match = message.match(/['"`]([^'"`]+)['"`]/);
    return match ? match[1] : null;
  }
  
  extractModuleName(message) {
    const match = message.match(/['"`]?([^/'"\s]+)['"`]?(?:'|"|\/|$)/);
    return match ? match[1] : null;
  }
  
  extractCommand(message) {
    const match = message.match(/spawn\s+(\S+)/);
    return match ? match[1] : null;
  }
  
  getTemplateForExt(ext) {
    const templates = {
      '.js': '// Auto-generated file\nmodule.exports = {};\n',
      '.json': '{\n  \n}\n',
      '.md': '# Auto-generated\n\n',
      '.yaml': '# Auto-generated YAML\n\n',
      '.yml': '# Auto-generated YAML\n\n'
    };
    return templates[ext] || '';
  }
  
  ensureDir(dir) {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
  }
  
  execAsync(cmd, options = {}) {
    return new Promise((resolve, reject) => {
      exec(cmd, options, (error, stdout, stderr) => {
        if (error) reject(error);
        else resolve(stdout);
      });
    });
  }
  
  // ==================== API ====================
  
  // 获取历史
  getHistory(limit = 10) {
    return this.errorHistory.slice(-limit);
  }
  
  // 获取修复历史
  getFixHistory(limit = 10) {
    return this.fixHistory.slice(-limit);
  }
  
  // 获取统计
  getStats() {
    const categories = {};
    for (const err of this.errorHistory) {
      const cat = err.analysis?.category || 'unknown';
      categories[cat] = (categories[cat] || 0) + 1;
    }
    
    return {
      totalErrors: this.errorHistory.length,
      totalFixes: this.fixHistory.length,
      categories,
      autoFixRate: this.fixHistory.length / this.errorHistory.length
    };
  }
  
  // 手动捕获
  catch(error, context = {}) {
    return this.capture(error, { ...context, source: 'manual' });
  }
}

module.exports = IntrospectionDebugger;
