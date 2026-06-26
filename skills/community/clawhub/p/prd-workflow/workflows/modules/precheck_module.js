/**
 * 环境检查前置模块 v1.0
 *
 * 在工作流执行前检查所有依赖环境
 * - mermaid-cli (mmdc)
 * - Chrome/Puppeteer
 * - Python3
 * - .NET SDK (可选)
 * - adm-zip (可选)
 *
 * 检查结果写入 dataBus，供后续模块判断是否跳过
 */

const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

class PrecheckModule {
  /**
   * 执行环境检查
   */
  async execute(options) {
    console.log('\n🔍 执行环境检查...');
    console.log('   '.repeat(50));

    const { dataBus } = options;

    const checks = {
      mermaid: this.checkMermaidCli(),
      chrome: this.checkChrome(),
      python: this.checkPython(),
      dotnet: this.checkDotNet(),
      admZip: this.checkAdmZip(),
      nodeVersion: this.checkNodeVersion()
    };

    // 统计结果
    const passed = Object.values(checks).filter(c => c.available).length;
    const total = Object.keys(checks).length;
    const missing = Object.entries(checks)
      .filter(([k, v]) => !v.available)
      .map(([k, v]) => ({ name: k, message: v.message, impact: v.impact }));

    // 输出检查结果
    console.log('\n   环境检查结果：');
    Object.entries(checks).forEach(([name, result]) => {
      const icon = result.available ? '✅' : '⚠️';
      const version = result.version ? ` (${result.version})` : '';
      console.log(`   ${icon} ${name}${version}`);
      if (!result.available && result.message) {
        console.log(`      ${result.message}`);
      }
    });

    // 判断是否可以继续
    const criticalMissing = missing.filter(m => m.impact === 'critical');

    // 输出检查结果
    console.log('\n   环境检查结果：');
    Object.entries(checks).forEach(([name, result]) => {
      const icon = result.available ? '✅' : (result.impact === 'critical' ? '❌' : '⚠️');
      const version = result.version ? ` (${result.version})` : '';
      console.log(`   ${icon} ${name}${version}`);
      if (!result.available && result.message) {
        console.log(`      ${result.message}`);
      }
    });

    // 关键依赖缺失：记录但不要 throw（让调用方决定如何处理）
    if (criticalMissing.length > 0) {
      console.log('\n   ❌ 关键依赖缺失，无法继续执行：');
      criticalMissing.forEach(m => {
        console.log(`      - ${m.name}: ${m.message}`);
      });
      // ⭐ v2.8.0 修复：不要 throw，返回完整结果让调用方处理
    }

    // 非关键缺失：警告但继续
    if (missing.length > 0 && criticalMissing.length === 0) {
      console.log('\n   ⚠️  非关键依赖缺失，部分功能将降级：');
      missing.forEach(m => {
        console.log(`      - ${m.name}: ${m.message} → ${m.impact === 'skip' ? '跳过该步骤' : '降级执行'}`);
      });
    }

    console.log(`\n   📊 环境检查完成：${passed}/${total} 可用`);

    // 写入 dataBus 供后续模块使用
    if (dataBus) {
      dataBus.write('precheck', {
        checks: checks,
        summary: { passed, total, missing },
        timestamp: new Date().toISOString()
      }, { passed: criticalMissing.length === 0 });
    }

    return {
      passed: criticalMissing.length === 0,
      checks: checks,
      summary: { passed, total, missing },
      canProceed: criticalMissing.length === 0,
      criticalMissing: criticalMissing
    };
  }

  /**
   * 检查 mermaid-cli (mmdc)
   */
  checkMermaidCli() {
    try {
      const version = execSync('mmdc --version', {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe']
      }).trim();
      return {
        available: true,
        version: version,
        impact: 'optional'
      };
    } catch (e) {
      return {
        available: false,
        message: 'mmdc 未安装，流程图将跳过（npm install -g @mermaid-js/mermaid-cli）',
        impact: 'skip',
        installHint: 'npm install -g @mermaid-js/mermaid-cli'
      };
    }
  }

  /**
   * 检查 Chrome/Puppeteer
   */
  checkChrome() {
    // 检查环境变量
    const puppeteerPath = process.env.PUPPETEER_EXECUTABLE_PATH;

    // macOS Chrome 路径
    const macChromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

    // 检查路径
    const chromePath = puppeteerPath || macChromePath;

    if (fs.existsSync(chromePath)) {
      return {
        available: true,
        path: chromePath,
        impact: 'optional'
      };
    }

    // 尝试查找其他浏览器
    const firefoxPath = '/Applications/Firefox.app/Contents/MacOS/firefox';
    if (fs.existsSync(firefoxPath)) {
      return {
        available: true,
        path: firefoxPath,
        browser: 'firefox',
        impact: 'optional'
      };
    }

    return {
      available: false,
      message: 'Chrome 未找到，原型截图将跳过',
      impact: 'skip',
      installHint: '安装 Chrome 或设置 PUPPETEER_EXECUTABLE_PATH'
    };
  }

  /**
   * 检查 Python3
   */
  checkPython() {
    try {
      const version = execSync('python3 --version', {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe']
      }).trim();
      return {
        available: true,
        version: version,
        impact: 'critical'
      };
    } catch (e) {
      // 尝试 python
      try {
        const version = execSync('python --version', {
          encoding: 'utf8',
          stdio: ['pipe', 'pipe', 'pipe']
        }).trim();
        return {
          available: true,
          version: version,
          alias: 'python',
          impact: 'critical'
        };
      } catch (e2) {
        return {
          available: false,
          message: 'Python 未安装，PRD 生成/评审将失败',
          impact: 'critical',
          installHint: '安装 Python 3.8+'
        };
      }
    }
  }

  /**
   * 检查 .NET SDK (可选，用于 OpenXML 验证)
   */
  checkDotNet() {
    const os = require('os');

    // 尝试常见 .NET 安装路径
    const dotnetPaths = [
      // 官方安装（最常见）
      path.join(os.homedir(), '.dotnet', 'dotnet'),
      // macOS 官方路径
      '/usr/local/share/dotnet/dotnet',
      // Linux 路径
      '/usr/share/dotnet/dotnet',
      // Homebrew 可能的路径
      '/opt/homebrew/opt/dotnet/bin/dotnet',
      '/usr/local/opt/dotnet/bin/dotnet'
    ];

    // 1. 先尝试 PATH 中的 dotnet
    try {
      const version = execSync('dotnet --version', {
        encoding: 'utf8',
        stdio: ['pipe', 'pipe', 'pipe'],
        timeout: 5000
      }).trim();

      if (version && !version.includes('error')) {
        return {
          available: true,
          version: version,
          path: 'dotnet',
          impact: 'optional'
        };
      }
    } catch (e) {
      // PATH 中的 dotnet 可能损坏，继续检查其他路径
    }

    // 2. 检查已知的安装路径
    for (const dotnetPath of dotnetPaths) {
      if (fs.existsSync(dotnetPath)) {
        try {
          const version = execSync(`"${dotnetPath}" --version`, {
            encoding: 'utf8',
            stdio: ['pipe', 'pipe', 'pipe'],
            timeout: 5000
          }).trim();

          if (version && !version.includes('error')) {
            return {
              available: true,
              version: version,
              path: dotnetPath,
              impact: 'optional'
            };
          }
        } catch (e) {
          // 此路径不可用，继续尝试下一个
        }
      }
    }

    return {
      available: false,
      message: '.NET SDK 未安装，OpenXML 验证将跳过',
      impact: 'skip',
      installHint: '安装 .NET SDK 6.0+（可选）或设置 PATH'
    };
  }

  /**
   * 检查 adm-zip (用于检查 DOCX 内图片)
   */
  checkAdmZip() {
    try {
      require('adm-zip');
      return {
        available: true,
        impact: 'optional'
      };
    } catch (e) {
      return {
        available: false,
        message: 'adm-zip 未安装，Word 图片检查将跳过',
        impact: 'skip',
        installHint: 'npm install adm-zip（可选）'
      };
    }
  }

  /**
   * 检查 Node.js 版本
   */
  checkNodeVersion() {
    const version = process.version;
    const major = parseInt(version.replace('v', '').split('.')[0]);

    if (major >= 16) {
      return {
        available: true,
        version: version,
        impact: 'critical'
      };
    }

    return {
      available: false,
      message: `Node.js 版本过低 (${version})，需要 v16+`,
      impact: 'critical',
      installHint: '升级 Node.js 到 v16+'
    };
  }

  /**
   * 获取降级建议
   */
  getFallback(stepName, checks) {
    const fallbacks = {
      'flowchart': {
        condition: !checks.mermaid.available,
        action: 'skip',
        message: 'mermaid-cli 不可用，跳过流程图生成'
      },
      'prototype': {
        condition: !checks.chrome.available,
        action: 'skip',
        message: 'Chrome 不可用，跳过原型截图'
      },
      'quality': {
        condition: !checks.dotnet.available,
        action: 'degrade',
        message: '.NET SDK 不可用，跳过 OpenXML 验证，使用简化检查'
      }
    };

    return fallbacks[stepName];
  }
}

module.exports = PrecheckModule;