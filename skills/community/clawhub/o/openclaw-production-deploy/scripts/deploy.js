#!/usr/bin/env node

/**
 * OpenClaw生产环境一键部署脚本
 * 基于B站视频《简单易用的openclaw的聊天界面》
 */

const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const readline = require('readline');

console.log('🚀 OpenClaw生产环境一键部署');
console.log('='.repeat(70));
console.log('基于《简单易用的openclaw的聊天界面》视频教程');
console.log('='.repeat(70));

class OpenClawDeployer {
  constructor() {
    this.steps = [];
    this.results = [];
    this.rl = readline.createInterface({
      input: process.stdin,
      output: process.stdout
    });
    this.platform = require('os').platform();
    this.isWindows = this.platform === 'win32';
    this.isLinux = this.platform === 'linux';
    this.isMac = this.platform === 'darwin';
  }
  
  async startDeployment() {
    console.log('\n🎯 部署目标: OpenClaw生产环境');
    console.log('='.repeat(50));
    console.log('包含以下功能:');
    console.log('   • OpenClaw核心安装');
    console.log('   • 聊天界面Web部署');
    console.log('   • 生产环境配置');
    console.log('   • 系统服务注册');
    console.log('   • 开机自启动');
    console.log('   • 监控和维护');
    console.log('='.repeat(50));
    
    try {
      // 显示部署说明
      await this.showDeploymentInfo();
      
      // 确认继续
      const proceed = await this.confirmProceed();
      if (!proceed) {
        console.log('\n部署已取消');
        this.rl.close();
        return;
      }
      
      // 运行部署步骤
      await this.runDeploymentSteps();
      
      // 完成部署
      this.completeDeployment();
      
    } catch (error) {
      console.error('\n❌ 部署失败:', error.message);
      this.generateErrorReport(error);
    } finally {
      this.rl.close();
    }
  }
  
  async showDeploymentInfo() {
    console.log('\n📖 部署说明:');
    console.log('='.repeat(50));
    
    const info = [
      '1. 本部署将安装OpenClaw到生产环境',
      '2. 配置为系统服务，实现开机自启',
      '3. 优化性能和安全性设置',
      '4. 部署Web聊天界面',
      '5. 设置监控和维护机制'
    ];
    
    info.forEach((item, index) => {
      console.log(`   ${index + 1}. ${item}`);
    });
    
    console.log('\n⏱️  预计时间: 10-15分钟');
    console.log('📊 系统要求: Node.js 22+, 4GB RAM, 2GB存储');
    console.log('🔒 需要管理员/root权限进行服务注册');
    console.log('='.repeat(50));
  }
  
  async confirmProceed() {
    return new Promise((resolve) => {
      this.rl.question('\n是否继续部署？(y/n): ', (answer) => {
        resolve(answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes');
      });
    });
  }
  
  async runDeploymentSteps() {
    const steps = [
      {
        name: '环境检查',
        action: async () => {
          console.log('\n1. 🔍 运行环境检查...');
          return await this.runEnvironmentCheck();
        }
      },
      {
        name: '安装OpenClaw',
        action: async () => {
          console.log('\n2. 📦 安装OpenClaw核心...');
          return await this.installOpenClaw();
        }
      },
      {
        name: '生产环境配置',
        action: async () => {
          console.log('\n3. ⚙️  配置生产环境...');
          return await this.configureProduction();
        }
      },
      {
        name: '部署聊天界面',
        action: async () => {
          console.log('\n4. 🌐 部署Web聊天界面...');
          return await this.deployWebInterface();
        }
      },
      {
        name: '注册系统服务',
        action: async () => {
          console.log('\n5. 🚀 注册系统服务...');
          return await this.registerSystemService();
        }
      },
      {
        name: '配置开机自启',
        action: async () => {
          console.log('\n6. 🔄 配置开机自启动...');
          return await this.configureAutoStart();
        }
      },
      {
        name: '设置监控',
        action: async () => {
          console.log('\n7. 📊 设置监控和维护...');
          return await this.setupMonitoring();
        }
      },
      {
        name: '验证部署',
        action: async () => {
          console.log('\n8. ✅ 验证部署结果...');
          return await this.verifyDeployment();
        }
      }
    ];
    
    for (const step of steps) {
      console.log(`\n🔧 步骤: ${step.name}`);
      console.log('-'.repeat(40));
      
      try {
        const result = await step.action();
        this.steps.push({
          step: step.name,
          status: 'completed',
          result: typeof result === 'string' ? result.substring(0, 200) + '...' : result
        });
        
        console.log(`   ✅ ${step.name}完成`);
      } catch (error) {
        console.log(`   ❌ ${step.name}失败: ${error.message}`);
        this.steps.push({
          step: step.name,
          status: 'failed',
          error: error.message
        });
        
        // 提供备用方案
        await this.provideFallbackSolution(step.name, error);
      }
    }
  }
  
  async runEnvironmentCheck() {
    // 运行环境检查脚本
    const checkScript = path.join(__dirname, 'step1-environment.js');
    
    if (!fs.existsSync(checkScript)) {
      throw new Error('环境检查脚本不存在');
    }
    
    const result = await this.executeCommand(`node "${checkScript}"`, 30000);
    
    if (result.includes('🚨 发现的问题') && result.includes('❌')) {
      console.log('   ⚠️  环境检查发现问题，但继续部署...');
    }
    
    return '环境检查完成';
  }
  
  async installOpenClaw() {
    console.log('   安装OpenClaw核心...');
    
    // 检查是否已安装
    try {
      const version = await this.executeCommand('openclaw --version', 5000);
      console.log(`   ℹ️  OpenClaw已安装: ${version.substring(0, 50)}...`);
      return { status: 'already_installed', version };
    } catch {
      // 未安装，继续安装
    }
    
    // 安装OpenClaw
    const installCommands = [
      // 官方安装脚本
      'npm install -g openclaw',
      // 国内镜像
      'npm config set registry https://registry.npmmirror.com && npm install -g openclaw'
    ];
    
    let lastError;
    
    for (const command of installCommands) {
      try {
        console.log(`   尝试安装命令: ${command}`);
        const output = await this.executeCommand(command, 180000); // 3分钟超时
        
        if (output.includes('added') || output.includes('installed') || !output.includes('ERR')) {
          console.log(`   ✅ OpenClaw安装成功`);
          
          // 验证安装
          const version = await this.executeCommand('openclaw --version', 5000);
          return { command, version: version.substring(0, 100) };
        }
        
        lastError = new Error(`安装命令未返回成功状态: ${command}`);
      } catch (error) {
        lastError = error;
        console.log(`   ⚠️  安装命令失败: ${command}`);
      }
    }
    
    // 如果所有命令都失败，尝试备用方案
    console.log('   尝试备用安装方案...');
    
    const fallbackCommands = [
      // 使用npx安装
      'npx -y openclaw@latest',
      // 从GitHub安装
      'git clone https://github.com/openclaw/openclaw.git && cd openclaw && npm install && npm run build'
    ];
    
    for (const command of fallbackCommands) {
      try {
        console.log(`   尝试备用命令: ${command}`);
        await this.executeCommand(command, 240000); // 4分钟超时
        console.log(`   ✅ 备用安装成功`);
        return { command: `fallback: ${command}`, status: 'installed_via_fallback' };
      } catch (error) {
        lastError = error;
      }
    }
    
    throw lastError || new Error('所有安装方法都失败');
  }
  
  async configureProduction() {
    console.log('   配置生产环境...');
    
    const configCommands = [
      // 设置生产环境模式
      'openclaw config set environment production',
      // 设置网关模式
      'openclaw config set gateway.mode local',
      // 启用认证
      'openclaw config set gateway.auth.enabled true',
      // 设置日志级别
      'openclaw config set logging.level info',
      // 启用性能监控
      'openclaw config set monitoring.enabled true'
    ];
    
    const results = {};
    
    for (const command of configCommands) {
      try {
        const output = await this.executeCommand(command, 10000);
        const configName = command.split(' ')[3]; // 获取配置项名称
        results[configName] = '配置成功';
        console.log(`   ✅ ${configName}: 配置成功`);
      } catch (error) {
        console.log(`   ⚠️  ${command}: 配置失败 - ${error.message}`);
        results[command] = `配置失败: ${error.message}`;
      }
    }
    
    // 创建生产环境配置文件
    const prodConfig = {
      environment: 'production',
      gateway: {
        mode: 'local',
        port: 18789,
        auth: {
          enabled: true,
          token: this.generateRandomToken()
        }
      },
      logging: {
        level: 'info',
        file: '~/.openclaw/logs/production.log',
        maxSize: '100MB',
        maxFiles: 10
      },
      monitoring: {
        enabled: true,
        port: 18790,
        metrics: true
      },
      performance: {
        maxMemory: '1GB',
        maxConcurrent: 10,
        timeout: 30000
      }
    };
    
    const configDir = path.join(require('os').homedir(), '.openclaw');
    const configFile = path.join(configDir, 'production-config.yaml');
    
    if (!fs.existsSync(configDir)) {
      fs.mkdirSync(configDir, { recursive: true });
    }
    
    const yamlContent = this.objectToYaml(prodConfig);
    fs.writeFileSync(configFile, yamlContent);
    
    console.log(`   ✅ 生产配置文件已创建: ${configFile}`);
    
    return { ...results, configFile };
  }
  
  async deployWebInterface() {
    console.log('   部署Web聊天界面...');
    
    // 视频中提到的简单易用的聊天界面
    // 这里我们配置OpenClaw自带的Web界面
    
    const webConfig = {
      web: {
        enabled: true,
        port: 18789,
        host: '0.0.0.0', // 允许局域网访问
        auth: true,
        theme: 'dark',
        features: {
          chat: true,
          files: true,
          skills: true,
          agents: true,
          settings: true
        }
      }
    };
    
    // 应用Web配置
    try {
      await this.executeCommand('openclaw config set web.enabled true', 5000);
      await this.executeCommand('openclaw config set web.host "0.0.0.0"', 5000);
      await this.executeCommand('openclaw config set web.theme dark', 5000);
      
      console.log('   ✅ Web界面配置完成');
    } catch (error) {
      console.log(`   ⚠️  Web配置失败: ${error.message}`);
    }
    
    // 创建访问说明
    const accessInfo = `
🎯 OpenClaw Web聊天界面访问信息:

📱 本地访问: http://localhost:18789
🌐 局域网访问: http://[你的IP地址]:18789
🔑 认证方式: Token认证（首次访问会生成）

💡 使用提示:
   1. 首次访问需要输入Token
   2. Token保存在 ~/.openclaw/config.yaml
   3. 支持暗色/亮色主题切换
   4. 响应式设计，支持手机访问

🚀 功能特性:
   • 实时聊天对话
   • 文件上传和处理
   • 技能管理和使用
   • 多Agent切换
   • 会话历史管理
   • 系统设置配置
`;
    
    console.log(accessInfo);
    
    return {
      url: 'http://localhost:18789',
      host: '0.0.0.0',
      port: 18789,
      auth: 'token_based'
    };
  }
  
  async registerSystemService() {
    console.log('   注册系统服务...');
    
    if (this.isWindows) {
      return await this.registerWindowsService();
    } else if (this.isLinux) {
      return await this.registerLinuxService();
    } else if (this.isMac) {
      return await this.registerMacService();
    } else {
      throw new Error(`不支持的操作系统: ${this.platform}`);
    }
  }
  
  async registerWindowsService() {
    console.log('   注册Windows服务...');
    
    const serviceCommands = [
      // 安装网关服务
      'openclaw gateway install',
      // 启动服务
      'openclaw gateway start',
      // 设置服务描述
      `sc description OpenClawGateway "OpenClaw AI Assistant Gateway Service - Production Environment"`
    ];
    
    const results = {};
    
    for (const command of serviceCommands) {
      try {
        const output = await this.executeCommand(command, 30000);
        results[command] = '成功';
        console.log(`   ✅ ${command.split(' ')[0]}: 成功`);
      } catch (error) {
        console.log(`   ⚠️  ${command}: 失败 - ${error.message}`);
        results[command] = `失败: ${error.message}`;
      }
    }
    
    // 创建服务配置文件
    const serviceConfig = `
<?xml version="1.0" encoding="UTF-8"?>
<service>
  <id>OpenClawGateway</id>
  <name>OpenClaw Gateway</name>
  <description>OpenClaw AI Assistant Gateway Service - Production Environment</description>
  <executable>${process.execPath}</executable>
  <argument>${require.main.filename}</argument>
  <logmode>rotate</logmode>
  <stoptimeout>30sec</stoptimeout>
  <startmode>Automatic</startmode>
  <interactive>false</interactive>
</service>
`;
    
    const configFile = path.join(process.cwd(), 'openclaw-service.xml');
    fs.writeFileSync(configFile, serviceConfig);
    
    console.log(`   ✅ Windows服务配置文件: ${configFile}`);
    
    return { ...results, serviceType: 'windows_service', configFile };
  }
  
  async registerLinuxService() {
    console.log('   注册Linux systemd服务...');
    
    const serviceConfig = `
[Unit]
Description=OpenClaw AI Assistant Gateway
After=network.target

[Service]
Type=simple
User=${process.env.USER}
WorkingDirectory=${process.cwd()}
ExecStart=${process.execPath} ${require.main.filename}
Restart=always
RestartSec=10
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=openclaw
Environment=NODE_ENV=production

[Install]
WantedBy=multi-user.target
`;
    
    const serviceFile = '/etc/systemd/system/openclaw.service';
    
    try {
      // 需要root权限
      fs.writeFileSync('/tmp/openclaw.service', serviceConfig);
      await this.executeCommand(`sudo cp /tmp/openclaw.service ${serviceFile}`, 10000);
      await this.executeCommand('sudo systemctl daemon-reload', 10000);
      await this.executeCommand('sudo systemctl enable openclaw.service', 10000);
      await this.executeCommand('sudo systemctl start openclaw.service', 10000);
      
      console.log(`   ✅ Linux systemd服务已注册: ${serviceFile}`);
      return { serviceType: 'systemd', serviceFile, status: 'enabled_and_started' };
    } catch (error) {
      console.log(`   ⚠️  Linux服务注册失败: ${error.message}`);
      
      // 备用方案：使用pm2
      console.log('   尝试使用pm2作为备用方案...');
      try {
        await this.executeCommand('npm install -g pm2', 60000);
        await this.executeCommand('pm2 start openclaw --name openclaw-gateway -- gateway run', 30000);
        await this.executeCommand('pm2 save', 10000);
        await this.executeCommand('pm2 startup', 10000);
        
        console.log('   ✅ 使用pm2管理服务成功');
        return { serviceType: 'pm2', status: 'managed_by_pm2' };
      } catch (pm2Error) {
        throw new Error(`Linux服务注册失败: ${error.message}, PM2备用方案也失败: ${pm2Error.message}`);
      }
    }
  }
  
  async registerMacService() {
    console.log('   注册macOS launchd服务...');
    
    // macOS使用launchd
    const launchdConfig = `
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www