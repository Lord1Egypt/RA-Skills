/**
 * master-agent-workflow-global OpenClaw钩子处理器
 * 版本: 2.0.0
 */

const fs = require('fs');
const path = require('path');

class MasterAgentWorkflowHandler {
  constructor(config) {
    this.config = config || {};
    this.skillName = 'master-agent-workflow-global';
    this.version = '2.0.0';
    
    // 技能根目录
    this.skillRoot = process.env.MAW_HOME || 
                    path.join(process.env.HOME || process.env.USERPROFILE, '.openclaw/global-skills/master-agent-workflow');
    
    // 配置目录
    this.configDir = path.join(this.skillRoot, 'config');
    
    // 确保目录存在
    this.ensureDirectories();
  }
  
  ensureDirectories() {
    const dirs = [this.configDir, path.join(this.skillRoot, 'templates'), path.join(this.skillRoot, 'logs')];
    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });
  }
  
  /**
   * 处理OpenClaw消息
   */
  async handleMessage(message, context) {
    const { text, user, channel } = message;
    
    // 检测是否触发技能
    if (this.shouldTrigger(text)) {
      return await this.processCommand(text, context);
    }
    
    return null;
  }
  
  /**
   * 检测是否触发技能
   */
  shouldTrigger(text) {
    const triggers = [
      '使用 master-agent-workflow-global',
      'maw ',
      'master-agent-workflow',
      '主控代理工作流'
    ];
    
    return triggers.some(trigger => text.toLowerCase().includes(trigger.toLowerCase()));
  }
  
  /**
   * 处理命令
   */
  async processCommand(text, context) {
    const command = this.extractCommand(text);
    
    switch (command.action) {
      case 'execute':
        return await this.handleExecute(command, context);
      case 'configure':
        return await this.handleConfigure(command, context);
      case 'template':
        return await this.handleTemplate(command, context);
      case 'migrate':
        return await this.handleMigrate(command, context);
      case 'help':
        return await this.handleHelp(command, context);
      default:
        return await this.handleDefault(command, context);
    }
  }
  
  /**
   * 提取命令
   */
  extractCommand(text) {
    // 移除触发词
    let cleaned = text.replace(/使用\s+master-agent-workflow-global\s*/i, '')
                     .replace(/maw\s+/i, '')
                     .replace(/主控代理工作流\s*/i, '');
    
    // 解析参数
    const parts = cleaned.split(/\s+/);
    const action = parts[0] || 'execute';
    const args = parts.slice(1);
    
    // 解析选项
    const options = {};
    for (let i = 0; i < args.length; i++) {
      if (args[i].startsWith('--')) {
        const key = args[i].slice(2);
        const value = args[i + 1] && !args[i + 1].startsWith('--') ? args[++i] : true;
        options[key] = value;
      }
    }
    
    return {
      action,
      args: args.filter(arg => !arg.startsWith('--')),
      options
    };
  }
  
  /**
   * 处理执行命令
   */
  async handleExecute(command, context) {
    const { args, options } = command;
    const task = args.join(' ');
    
    // 加载配置
    const config = await this.loadConfig(options.config);
    
    // 应用模板
    if (options.template) {
      const template = await this.loadTemplate(options.template);
      Object.assign(config, template.config);
    }
    
    // 生成执行指令
    const executionCommand = this.generateExecutionCommand(task, config);
    
    return {
      type: 'command',
      command: executionCommand,
      metadata: {
        skill: this.skillName,
        version: this.version,
        config: config,
        timestamp: new Date().toISOString()
      }
    };
  }
  
  /**
   * 处理配置命令
   */
  async handleConfigure(command, context) {
    const { args, options } = command;
    
    if (args[0] === 'list') {
      // 列出配置
      const configs = await this.listConfigs();
      return {
        type: 'message',
        content: `可用配置:\n${configs.map(c => `- ${c}`).join('\n')}`
      };
    } else if (args[0] === 'save') {
      // 保存配置
      const configName = args[1] || 'default';
      await this.saveConfig(configName, options);
      return {
        type: 'message',
        content: `配置已保存: ${configName}`
      };
    }
    
    return {
      type: 'message',
      content: '配置命令用法: configure [list|save] [名称] [--选项 值]'
    };
  }
  
  /**
   * 处理模板命令
   */
  async handleTemplate(command, context) {
    const { args } = command;
    
    if (args[0] === 'list') {
      const templates = await this.listTemplates();
      return {
        type: 'message',
        content: `可用模板:\n${templates.map(t => `- ${t.name}: ${t.description}`).join('\n')}`
      };
    }
    
    return {
      type: 'message',
      content: '模板命令用法: template list'
    };
  }
  
  /**
   * 处理迁移命令
   */
  async handleMigrate(command, context) {
    const { args, options } = command;
    
    if (args[0] === 'export') {
      const output = options.output || `maw-export-${Date.now()}.json`;
      await this.exportConfig(output, options);
      return {
        type: 'message',
        content: `配置已导出到: ${output}`
      };
    } else if (args[0] === 'import') {
      const file = args[1];
      if (!file) {
        return {
          type: 'message',
          content: '请指定要导入的文件'
        };
      }
      await this.importConfig(file, options);
      return {
        type: 'message',
        content: `配置已从 ${file} 导入`
      };
    }
    
    return {
      type: 'message',
      content: '迁移命令用法: migrate [export|import] [文件] [--选项 值]'
    };
  }
  
  /**
   * 处理帮助命令
   */
  async handleHelp(command, context) {
    const helpText = `
master-agent-workflow-global v${this.version}

用法:
  使用 master-agent-workflow-global [命令] [参数] [--选项 值]

命令:
  execute [任务]     执行任务
  configure         配置管理
  template          模板管理  
  migrate           迁移工具
  help              显示帮助

选项:
  --max-workers N    最大并行数 (默认: 5)
  --timeout H        超时时间(小时) (默认: 3)
  --template NAME    使用模板
  --config NAME      使用配置
  --dry-run          试运行

示例:
  使用 master-agent-workflow-global execute "处理文件" --max-workers 10
  使用 master-agent-workflow-global template list
  使用 master-agent-workflow-global migrate export --output config.json

快捷命令:
  maw [命令] [参数] [--选项 值]
    `;
    
    return {
      type: 'message',
      content: helpText
    };
  }
  
  /**
   * 处理默认命令
   */
  async handleDefault(command, context) {
    // 如果没有指定命令，默认执行
    return await this.handleExecute({
      action: 'execute',
      args: command.args,
      options: command.options
    }, context);
  }
  
  /**
   * 加载配置
   */
  async loadConfig(configName) {
    const defaultConfig = {
      max_workers: 5,
      timeout_hours: 3,
      worker_timeout_minutes: 30,
      stuck_threshold_minutes: 15,
      fail_threshold: 10,
      auto_cleanup: true,
      report_channel: 'feishu'
    };
    
    if (!configName || configName === 'default') {
      return defaultConfig;
    }
    
    const configFile = path.join(this.configDir, `${configName}.json`);
    if (fs.existsSync(configFile)) {
      try {
        const content = fs.readFileSync(configFile, 'utf8');
        return { ...defaultConfig, ...JSON.parse(content) };
      } catch (error) {
        console.error(`加载配置失败: ${configName}`, error);
        return defaultConfig;
      }
    }
    
    return defaultConfig;
  }
  
  /**
   * 保存配置
   */
  async saveConfig(name, config) {
    const configFile = path.join(this.configDir, `${name}.json`);
    fs.writeFileSync(configFile, JSON.stringify(config, null, 2), 'utf8');
  }
  
  /**
   * 列出配置
   */
  async listConfigs() {
    if (!fs.existsSync(this.configDir)) {
      return ['default'];
    }
    
    const files = fs.readdirSync(this.configDir);
    return files
      .filter(file => file.endsWith('.json'))
      .map(file => file.replace('.json', ''))
      .concat(['default']);
  }
  
  /**
   * 加载模板
   */
  async loadTemplate(templateName) {
    const templateFile = path.join(this.skillRoot, 'templates', `${templateName}.json`);
    
    if (fs.existsSync(templateFile)) {
      try {
        const content = fs.readFileSync(templateFile, 'utf8');
        return JSON.parse(content);
      } catch (error) {
        console.error(`加载模板失败: ${templateName}`, error);
      }
    }
    
    // 返回默认模板
    return {
      name: 'default',
      description: '默认模板',
      config: {}
    };
  }
  
  /**
   * 列出模板
   */
  async listTemplates() {
    const templatesDir = path.join(this.skillRoot, 'templates');
    
    if (!fs.existsSync(templatesDir)) {
      return [];
    }
    
    const files = fs.readdirSync(templatesDir);
    const templates = [];
    
    for (const file of files) {
      if (file.endsWith('.json')) {
        try {
          const content = fs.readFileSync(path.join(templatesDir, file), 'utf8');
          const template = JSON.parse(content);
          templates.push(template);
        } catch (error) {
          console.error(`解析模板失败: ${file}`, error);
        }
      }
    }
    
    return templates;
  }
  
  /**
   * 导出配置
   */
  async exportConfig(outputPath, options) {
    const exportData = {
      version: this.version,
      timestamp: new Date().toISOString(),
      configs: {},
      templates: []
    };
    
    // 导出配置
    const configs = await this.listConfigs();
    for (const configName of configs) {
      if (configName !== 'default') {
        exportData.configs[configName] = await this.loadConfig(configName);
      }
    }
    
    // 导出模板
    exportData.templates = await this.listTemplates();
    
    // 写入文件
    fs.writeFileSync(outputPath, JSON.stringify(exportData, null, 2), 'utf8');
  }
  
  /**
   * 导入配置
   */
  async importConfig(filePath, options) {
    if (!fs.existsSync(filePath)) {
      throw new Error(`文件不存在: ${filePath}`);
    }
    
    const content = fs.readFileSync(filePath, 'utf8');
    const importData = JSON.parse(content);
    
    // 导入配置
    if (importData.configs) {
      for (const [name, config] of Object.entries(importData.configs)) {
        await this.saveConfig(name, config);
      }
    }
    
    // 导入模板
    if (importData.templates && fs.existsSync(path.join(this.skillRoot, 'templates'))) {
      for (const template of importData.templates) {
        const templateFile = path.join(this.skillRoot, 'templates', `${template.name}.json`);
        fs.writeFileSync(templateFile, JSON.stringify(template, null, 2), 'utf8');
      }
    }
  }
  
  /**
   * 生成执行指令
   */
  generateExecutionCommand(task, config) {
    const params = [];
    
    if (config.max_workers !== 5) params.push(`--max-workers ${config.max_workers}`);
    if (config.timeout_hours !== 3) params.push(`--timeout ${config.timeout_hours}h`);
    if (config.worker_timeout_minutes !== 30) params.push(`--worker-timeout ${config.worker_timeout_minutes}m`);
    
    return `=== 使用 master-agent-workflow-global ===\n\n任务: ${task}\n\n配置:\n${JSON.stringify(config, null, 2)}\n\n执行参数: ${params.join(' ')}`;
  }
}

module.exports = MasterAgentWorkflowHandler;