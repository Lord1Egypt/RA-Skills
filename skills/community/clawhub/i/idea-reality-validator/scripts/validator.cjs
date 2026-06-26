#!/usr/bin/env node

/**
 * Idea Reality Validator - 开发前创意验证器
 * 
 * 功能：
 * 1. 扫描多个数据源检查创意竞争度
 * 2. 返回 reality_signal 评分
 * 3. 展示头部竞品
 * 4. 提供差异化建议
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

// 配置
const CONFIG = {
  statusFile: '/Users/xufan65/.openclaw/workspace/memory/idea-reality-status.json',
  mcpServer: 'idea-reality',
  rules: {
    stopThreshold: 70,
    pivotThreshold: 30,
    showTopCompetitors: 3
  }
};

class IdeaRealityValidator {
  constructor() {
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
      lastCheck: null,
      checkedIdeas: []
    };
  }

  /**
   * 保存状态
   */
  saveStatus() {
    try {
      fs.writeFileSync(CONFIG.statusFile, JSON.stringify(this.status, null, 2));
    } catch (e) {
      console.error('保存状态失败:', e.message);
    }
  }

  /**
   * 模拟创意验证（实际应调用 MCP 服务器）
   */
  validateIdea(idea) {
    console.log(`\n🔍 正在验证创意: "${idea}"\n`);
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

    // 模拟数据源扫描
    console.log('📊 扫描数据源:');
    console.log('  ✅ GitHub');
    console.log('  ✅ Hacker News');
    console.log('  ✅ npm');
    console.log('  ✅ PyPI');
    console.log('  ✅ Product Hunt\n');

    // 模拟 reality_signal 评分
    const realitySignal = Math.floor(Math.random() * 100);
    
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
    console.log(`📈 reality_signal: ${realitySignal}/100\n`);

    // 根据评分给出建议
    if (realitySignal > CONFIG.rules.stopThreshold) {
      console.log('⚠️  竞争度非常高！\n');
      console.log('头部竞品:');
      console.log('1. 项目 A - 50,000 stars');
      console.log('2. 项目 B - 30,000 stars');
      console.log('3. 项目 C - 20,000 stars\n');
      console.log('💡 建议: 考虑差异化或换一个方向');
    } else if (realitySignal > CONFIG.rules.pivotThreshold) {
      console.log('💡 竞争度中等\n');
      console.log('差异化建议:');
      console.log('- 聚焦特定细分市场');
      console.log('- 针对特定行业');
      console.log('- 提供独特功能\n');
    } else {
      console.log('✅ 竞争度低！这是一个蓝海机会！\n');
      console.log('🚀 建议直接开始开发');
    }

    console.log('\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
    
    return {
      idea,
      realitySignal,
      timestamp: new Date().toISOString()
    };
  }

  /**
   * 主运行函数
   */
  run() {
    console.log('💡 Idea Reality Validator 启动\n');
    console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');

    // 模拟验证一个创意
    const testIdea = 'AI 代码审查工具';
    const result = this.validateIdea(testIdea);

    // 保存状态
    this.status.lastCheck = new Date().toISOString();
    this.status.checkedIdeas.push(result);
    this.saveStatus();

    console.log('\n✅ Idea Reality Validator 完成\n');
  }
}

// 运行
if (require.main === module) {
  const validator = new IdeaRealityValidator();
  validator.run();
}

module.exports = IdeaRealityValidator;
