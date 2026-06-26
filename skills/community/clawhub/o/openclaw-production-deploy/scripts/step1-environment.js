#!/usr/bin/env node

/**
 * OpenClaw生产环境部署 - 步骤1: 环境检查
 * 基于B站视频《简单易用的openclaw的聊天界面》
 */

const fs = require('fs');
const os = require('os');
const { exec } = require('child_process');

console.log('🔍 OpenClaw生产环境部署 - 环境检查');
console.log('='.repeat(70));
console.log('基于《简单易用的openclaw的聊天界面》视频教程');
console.log('='.repeat(70));

class EnvironmentChecker {
  constructor() {
    this.results = [];
    this.issues = [];
    this.recommendations = [];
    this.platform = os.platform();
    this.arch = os.arch();
    this.totalMemory = Math.round(os.totalmem() / (1024 * 1024 * 1024)); // GB
    this.freeMemory = Math.round(os.freemem() / (1024 * 1024 * 1024)); // GB
  }
  
  async runChecks() {
    console.log('\n📊 系统信息:');
    console.log(`   操作系统: ${os.type()} ${os.release()}`);
    console.log(`   架构: ${this.arch}`);
    console.log(`   内存: ${this.totalMemory}GB (可用: ${this.freeMemory}GB)`);
    console.log(`   处理器: ${os.cpus().length}核心 ${os.cpus()[0].model}`);
    console.log(`   主机名: ${os.hostname()}`);
    
    console.log('\n1. 🖥️  系统要求检查...');
    await this.checkSystemRequirements();
    
    console.log('\n2. ⚙️  软件依赖检查...');
    await this.checkSoftwareDependencies();
    
    console.log('\n3. 📁 文件系统检查...');
    await this.checkFilesystem();
    
    console.log('\n4. 🌐 网络环境检查...');
    await this.checkNetwork();
    
    console.log('\n5. 🔒 安全配置检查...');
    await this.checkSecurity();
    
    console.log('\n6. 📋 生成检查报告...');
    this.generateReport();
  }
  
  async checkSystemRequirements() {
    const requirements = [
      {
        name: '操作系统',
        check: () => {
          const supported = ['win32', 'linux', 'darwin'];
          return supported.includes(this.platform);
        },
        message: '支持的操作系统',
        error: '不支持的操作系统，需要Windows/Linux/macOS'
      },
      {
        name: '内存要求',
        check: () => this.totalMemory >= 4,
        message: `内存充足 (${this.totalMemory}GB >= 4GB)`,
        error: `内存不足 (${this.totalMemory}GB < 4GB)`
      },
      {
        name: '存储空间',
        check: async () => {
          try {
            const freeSpace = await this.getFreeDiskSpace();
            return freeSpace >= 2; // 2GB
          } catch {
            return true; // 如果无法检查，假设足够
          }
        },
        message: '存储空间充足',
        error: '存储空间不足，需要至少2GB'
      },
      {
        name: 'CPU核心',
        check: () => os.cpus().length >= 2,
        message: `CPU核心足够 (${os.cpus().length}核心)`,
        error: 'CPU核心不足，需要至少2核心'
      }
    ];
    
    for (const req of requirements) {
      try {
        const passed = await req.check();
        
        this.results.push({
          category: '系统要求',
          check: req.name,
          status: passed ? 'passed' : 'failed',
          message: passed ? req.message : req.error
        });
        
        const icon = passed ? '✅' : '❌';
        console.log(`   ${icon} ${req.name}: ${passed ? req.message : req.error}`);
        
        if (!passed) {
          this.issues.push(req.name);
          this.recommendations.push(`解决${req.name}问题: ${req.error}`);
        }
      } catch (error) {
        this.results.push({
          category: '系统要求',
          check: req.name,
          status: 'error',
          message: `检查失败: ${error.message}`
        });
        
        console.log(`   ⚠️  ${req.name}: 检查失败`);
      }
    }
  }
  
  async checkSoftwareDependencies() {
    const dependencies = [
      {
        name: 'Node.js版本',
        command: 'node --version',
        check: (output) => {
          const version = output.replace('v', '');
          const major = parseInt(version.split('.')[0]);
          return major >= 22;
        },
        message: 'Node.js版本符合要求',
        error: '需要Node.js 22.x或更高版本'
      },
      {
        name: 'npm版本',
        command: 'npm --version',
        check: (output) => {
          const major = parseInt(output.split('.')[0]);
          return major >= 10;
        },
        message: 'npm版本符合要求',
        error: '需要npm 10.x或更高版本'
      },
      {
        name: 'Git安装',
        command: 'git --version',
        check: (output) => output.includes('git version'),
        message: 'Git已安装',
        error: 'Git未安装，建议安装以便版本控制'
      },
      {
        name: 'PowerShell版本',
        command: 'powershell -Command "$PSVersionTable.PSVersion.Major"',
        check: (output) => parseInt(output) >= 5,
        message: 'PowerShell版本符合要求',
        error: '需要PowerShell 5.0或更高版本',
        windowsOnly: true
      }
    ];
    
    for (const dep of dependencies) {
      // 跳过Windows-only检查在非Windows系统
      if (dep.windowsOnly && this.platform !== 'win32') {
        continue;
      }
      
      try {
        const output = await this.executeCommand(dep.command);
        const passed = dep.check(output);
        
        this.results.push({
          category: '软件依赖',
          check: dep.name,
          status: passed ? 'passed' : 'failed',
          message: passed ? dep.message : dep.error,
          details: passed ? output.substring(0, 50) : '未安装或版本过低'
        });
        
        const icon = passed ? '✅' : '❌';
        console.log(`   ${icon} ${dep.name}: ${passed ? dep.message : dep.error}`);
        
        if (!passed) {
          this.issues.push(dep.name);
          this.recommendations.push(`安装或更新${dep.name}: ${dep.error}`);
        }
      } catch (error) {
        this.results.push({
          category: '软件依赖',
          check: dep.name,
          status: 'error',
          message: `检查失败: ${error.message}`,
          details: '命令执行错误'
        });
        
        console.log(`   ⚠️  ${dep.name}: 检查失败 - ${error.message}`);
        this.issues.push(dep.name);
      }
    }
  }
  
  async checkFilesystem() {
    console.log('   检查文件系统权限和空间...');
    
    const checks = [
      {
        name: '当前目录写入权限',
        check: () => {
          try {
            const testFile = './.openclaw-deploy-test';
            fs.writeFileSync(testFile, 'test');
            fs.unlinkSync(testFile);
            return true;
          } catch {
            return false;
          }
        },
        message: '当前目录可写入',
        error: '当前目录不可写入，请检查权限'
      },
      {
        name: 'OpenClaw配置目录',
        check: () => {
          const configDir = `${os.homedir()}/.openclaw`;
          try {
            if (!fs.existsSync(configDir)) {
              fs.mkdirSync(configDir, { recursive: true });
            }
            const testFile = `${configDir}/.test-write`;
            fs.writeFileSync(testFile, 'test');
            fs.unlinkSync(testFile);
            return true;
          } catch {
            return false;
          }
        },
        message: 'OpenClaw配置目录可访问',
        error: '无法访问OpenClaw配置目录'
      },
      {
        name: '临时目录',
        check: () => {
          try {
            const tmpDir = os.tmpdir();
            const testFile = `${tmpDir}/.openclaw-test-${Date.now()}`;
            fs.writeFileSync(testFile, 'test');
            fs.unlinkSync(testFile);
            return true;
          } catch {
            return false;
          }
        },
        message: '临时目录可访问',
        error: '无法访问临时目录'
      }
    ];
    
    for (const check of checks) {
      try {
        const passed = check.check();
        
        this.results.push({
          category: '文件系统',
          check: check.name,
          status: passed ? 'passed' : 'failed',
          message: passed ? check.message : check.error
        });
        
        const icon = passed ? '✅' : '❌';
        console.log(`   ${icon} ${check.name}: ${passed ? check.message : check.error}`);
        
        if (!passed) {
          this.issues.push(check.name);
        }
      } catch (error) {
        this.results.push({
          category: '文件系统',
          check: check.name,
          status: 'error',
          message: `检查失败: ${error.message}`
        });
        
        console.log(`   ⚠️  ${check.name}: 检查失败`);
      }
    }
  }
  
  async checkNetwork() {
    console.log('   检查网络连接和端口...');
    
    const networkChecks = [
      {
        name: '本地回环',
        host: '127.0.0.1',
        message: '本地网络正常',
        error: '本地网络异常'
      },
      {
        name: '外部网络',
        host: '8.8.8.8',
        message: '外部网络可访问',
        error: '外部网络不可访问'
      },
      {
        name: 'GitHub访问',
        host: 'github.com',
        message: '可访问GitHub',
        error: '无法访问GitHub'
      },
      {
        name: 'npm仓库',
        host: 'registry.npmjs.org',
        message: '可访问npm仓库',
        error: '无法访问npm仓库'
      }
    ];
    
    for (const check of networkChecks) {
      try {
        const { promisify } = require('util');
        const dns = require('dns');
        const resolve = promisify(dns.lookup);
        
        await resolve(check.host, { timeout: 5000 });
        
        this.results.push({
          category: '网络',
          check: `网络-${check.name}`,
          status: 'passed',
          message: check.message
        });
        
        console.log(`   ✅ ${check.name}: ${check.message}`);
      } catch (error) {
        this.results.push({
          category: '网络',
          check: `网络-${check.name}`,
          status: 'failed',
          message: check.error,
          details: error.message
        });
        
        console.log(`   ❌ ${check.name}: ${check.error}`);
        this.issues.push(`网络-${check.name}`);
        this.recommendations.push(`检查网络连接，确保可以访问${check.host}`);
      }
    }
    
    // 检查端口占用
    console.log('   检查端口占用情况...');
    const ports = [18789, 18790, 3000, 8080];
    
    for (const port of ports) {
      try {
        const net = require('net');
        const server = net.createServer();
        
        await new Promise((resolve, reject) => {
          server.once('error', (err) => {
            if (err.code === 'EADDRINUSE') {
              resolve(false); // 端口被占用
            } else {
              reject(err);
            }
          });
          
          server.once('listening', () => {
            server.close();
            resolve(true); // 端口可用
          });
          
          server.listen(port, '127.0.0.1');
        });
        
        const status = await this.executeCommand(`netstat -ano | findstr :${port}`, 5000).catch(() => '');
        const isUsed = status.includes(`:${port}`);
        
        if (isUsed) {
          console.log(`   ⚠️  端口${port}: 被占用`);
          if (port === 18789) {
            this.recommendations.push(`OpenClaw默认端口18789被占用，可能需要修改配置`);
          }
        } else {
          console.log(`   ✅ 端口${port}: 可用`);
        }
      } catch (error) {
        console.log(`   ⚠️  端口${port}: 检查失败`);
      }
    }
  }
  
  async checkSecurity() {
    console.log('   检查安全配置...');
    
    const securityChecks = [
      {
        name: '防火墙状态',
        check: async () => {
          if (this.platform === 'win32') {
            const status = await this.executeCommand('netsh advfirewall show allprofiles state', 5000).catch(() => '');
            return !status.includes('关闭');
          }
          return true; // 非Windows跳过
        },
        message: '防火墙已启用',
        error: '防火墙未启用，建议启用以提高安全性'
      },
      {
        name: '用户权限',
        check: () => {
          // 检查是否以管理员/root运行
          if (this.platform === 'win32') {
            try {
              fs.accessSync('C:\\Windows\\System32\\config\\systemprofile', fs.constants.W_OK);
              return false; // 有写入系统目录权限，可能是管理员
            } catch {
              return true; // 普通用户
            }
          }
          return process.getuid && process.getuid() !== 0; // Linux/macOS检查root
        },
        message: '适当的用户权限',
        error: '可能需要管理员/root权限进行安装'
      },
      {
        name: '安全更新',
        check: async () => {
          // 简单检查系统更新状态
          try {
            if (this.platform === 'win32') {
              const result = await this.executeCommand('systeminfo | findstr /B /C:"OS 版本"', 5000);
              return result.includes('Version');
            }
          } catch {
            // 忽略错误
          }
          return true;
        },
        message: '系统信息可获取',
        error: '无法获取系统更新信息'
      }
    ];
    
    for (const check of securityChecks) {
      try {
        const passed = await check.check();
        
        this.results.push({
          category: '安全',
          check: check.name,
          status: passed ? 'passed' : 'warning',
          message: passed ? check.message : check.error
        });
        
        const icon = passed ? '✅' : '⚠️';
        console.log(`   ${icon} ${check.name}: ${passed ? check.message : check.error}`);
        
        if (!passed) {
          this.recommendations.push(`安全建议: ${check.error}`);
        }
      } catch (error) {
        this.results.push({
          category: '安全',
          check: check.name,
          status: 'error',
          message: `检查失败: ${error.message}`
        });
        
        console.log(`   ⚠️  ${check.name}: 检查失败`);
      }
    }
  }
  
  async getFreeDiskSpace() {
    return new Promise((resolve, reject) => {
      if (this.platform === 'win32') {
        exec('wmic logicaldisk where "DeviceID=\'C:\'" get FreeSpace', (error, stdout) => {
          if (error) reject(error);
          const lines = stdout.trim().split('\n');
          if (lines.length > 1) {
            const freeBytes = parseInt(lines[1].trim());
            resolve(freeBytes / (1024 * 1024 * 1024)); // 转换为GB
          } else {
            reject(new Error('无法获取磁盘空间'));
          }
        });
      } else {
        // Linux/macOS
        exec('df -k . | tail -1 | awk \'{print $4}\'', (error, stdout) => {
          if (error) reject(error);
          const freeKB = parseInt(stdout.trim());
          resolve(freeKB / (1024 * 1024)); // 转换为GB
        });
      }
    });
  }
  
  async executeCommand(command, timeout = 10000) {
    return new Promise((resolve, reject) => {
      exec(command, { timeout, shell: true }, (error, stdout, stderr) => {
        if (error) {
          reject(new Error(stderr || error.message));
        } else {
          resolve(stdout.toString().trim());
        }
      });
    });
  }
  
  generateReport() {
    console.log('\n' + '='.repeat(70));
    console.log('📊 环境检查报告');
    console.log('='.repeat(70));
    
    const passed = this.results.filter(r => r.status === 'passed').length;
    const failed = this.results.filter(r => r.status === 'failed').length;
    const warnings = this.results.filter(r => r.status === 'warning').length;
    const errors = this.results.filter(r => r.status === 'error').length;
    const total = this.results.length;
    
    console.log(`✅ 通过: ${passed}/${total}`);
    console.log(`❌ 失败: ${failed}/${total}`);
    console.log(`⚠️  警告: ${warnings}/${total}`);
    console.log(`🚨 错误: ${errors}/${total}`);
    
    if (this.issues.length > 0) {
      console.log('\n🚨 发现的问题:');
      this.issues.forEach((issue, index) => {
        console.log(`   ${index + 1}. ${issue}`);
      });
    } else {
      console.log('\n🎉 所有检查通过！可以开始部署。');
    }
    
    if (this.recommendations.length > 0) {
      console.log('\n💡 建议操作:');
      this.recommendations.forEach((rec,