#!/usr/bin/env node

/**
 * Sensitive Word Loader - 敏感词词库加载器
 * 
 * 功能：
 * 1. 加载敏感词词库文件
 * 2. 检查文本是否包含敏感词
 * 3. 支持热更新
 * 4. 与代码完全分离
 */

const fs = require('fs');
const path = require('path');

const DEFAULT_LIBRARY_PATH = path.join(__dirname, 'sensitive-words.txt');

class SensitiveWordLoader {
  constructor(libraryPath = DEFAULT_LIBRARY_PATH) {
    this.libraryPath = libraryPath;
    this.rules = [];
    this.lastLoaded = null;
    this.load();
  }
  
  /**
   * 加载词库
   */
  load() {
    try {
      if (!fs.existsSync(this.libraryPath)) {
        console.warn(`⚠️  词库文件不存在：${this.libraryPath}`);
        this.createDefaultLibrary();
        return;
      }
      
      const content = fs.readFileSync(this.libraryPath, 'utf-8');
      const lines = content.split('\n');
      
      this.rules = [];
      let lineCount = 0;
      let commentCount = 0;
      let ruleCount = 0;
      
      for (let i = 0; i < lines.length; i++) {
        lineCount++;
        const line = lines[i].trim();
        
        // 跳过空行和注释
        if (!line || line.startsWith('#')) {
          if (line.startsWith('#')) commentCount++;
          continue;
        }
        
        // 解析规则：类型 | 模式 | 动作 | 说明
        const parts = line.split('|');
        if (parts.length < 3) {
          console.warn(`⚠️  词库第${i + 1}行格式错误（需要 3 个字段）：${line}`);
          continue;
        }
        
        const [type, pattern, action, ...descParts] = parts;
        const description = descParts.join('|')?.trim() || '';
        
        // 验证类型
        const validTypes = ['regex', 'keyword', 'path'];
        if (!validTypes.includes(type.trim())) {
          console.warn(`⚠️  词库第${i + 1}行类型错误（应为 ${validTypes.join('/')}）：${type}`);
          continue;
        }
        
        // 验证动作
        const validActions = ['block', 'alert', 'log'];
        if (!validActions.includes(action.trim())) {
          console.warn(`⚠️  词库第${i + 1}行动作错误（应为 ${validActions.join('/')}）：${action}`);
          continue;
        }
        
        this.rules.push({
          type: type.trim(),
          pattern: pattern.trim(),
          action: action.trim(),
          description: description,
          line: i + 1
        });
        
        ruleCount++;
      }
      
      this.lastLoaded = new Date();
      console.log(`✅ 已加载 ${ruleCount} 条敏感词规则（共${lineCount}行，注释${commentCount}行）`);
      
    } catch (e) {
      console.error(`❌ 加载词库失败：${e.message}`);
      this.rules = [];
    }
  }
  
  /**
   * 创建默认词库
   */
  createDefaultLibrary() {
    const defaultContent = `# 敏感词词库 - 默认配置
# 格式：类型 | 模式 | 动作 | 说明

# ===== 账号 ID 检测 =====
regex|/ou_[a-f0-9]{32}/g|block|飞书账号 ID

# ===== 记忆文件检测 =====
regex|/MEMORY\\.md/i|alert|记忆文件提及
regex|/memory\\.md/i|alert|记忆文件提及（小写）

# ===== 用户记忆路径 =====
regex|/memory/users/[^/]+\\.md/i|block|用户记忆文件路径
regex|/memory/sessions/[^/]+/user\\.md/i|block|Session 记忆文件路径
`;
    
    const dir = path.dirname(this.libraryPath);
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true });
    }
    
    fs.writeFileSync(this.libraryPath, defaultContent, 'utf-8');
    console.log(`✅ 已创建默认词库：${this.libraryPath}`);
    this.load();
  }
  
  /**
   * 检查文本是否包含敏感词
   * @param {string} text - 待检查的文本
   * @returns {{passed: boolean, violations: Array}} - 检查结果
   */
  check(text) {
    if (!text) {
      return { passed: true, violations: [] };
    }
    
    const violations = [];
    
    for (const rule of this.rules) {
      try {
        let matched = false;
        
        if (rule.type === 'regex') {
          // 解析正则：/pattern/flags
          const match = rule.pattern.match(/^\/(.+)\/([gimuy]*)$/);
          if (match) {
            const regex = new RegExp(match[1], match[2]);
            matched = regex.test(text);
          } else {
            console.warn(`⚠️  正则格式错误：${rule.pattern}`);
            continue;
          }
        } else if (rule.type === 'keyword') {
          matched = text.includes(rule.pattern);
        } else if (rule.type === 'path') {
          matched = text.includes(rule.pattern);
        }
        
        if (matched) {
          violations.push({
            rule: rule.type,
            pattern: rule.pattern,
            action: rule.action,
            description: rule.description,
            line: rule.line,
            severity: rule.action === 'block' ? 'high' : 'medium'
          });
        }
        
      } catch (e) {
        console.error(`❌ 规则 ${rule.line} 执行失败：${e.message}`);
      }
    }
    
    return {
      passed: violations.length === 0,
      violations,
      checkedAt: new Date(),
      ruleCount: this.rules.length
    };
  }
  
  /**
   * 获取所有规则
   */
  getRules() {
    return this.rules;
  }
  
  /**
   * 获取规则统计
   */
  getStats() {
    const stats = {
      total: this.rules.length,
      byType: { regex: 0, keyword: 0, path: 0 },
      byAction: { block: 0, alert: 0, log: 0 },
      lastLoaded: this.lastLoaded
    };
    
    this.rules.forEach(rule => {
      stats.byType[rule.type]++;
      stats.byAction[rule.action]++;
    });
    
    return stats;
  }
  
  /**
   * 重新加载词库（热更新）
   */
  reload() {
    console.log('🔄 重新加载敏感词词库...');
    this.load();
  }
  
  /**
   * 添加规则到文件
   */
  addRule(type, pattern, action, description = '') {
    const validTypes = ['regex', 'keyword', 'path'];
    const validActions = ['block', 'alert', 'log'];
    
    if (!validTypes.includes(type)) {
      throw new Error(`无效的类型：${type}，应为 ${validTypes.join('/')}`);
    }
    
    if (!validActions.includes(action)) {
      throw new Error(`无效的动作：${action}，应为 ${validActions.join('/')}`);
    }
    
    const newRule = `${type}|${pattern}|${action}|${description}`;
    
    try {
      fs.appendFileSync(this.libraryPath, `\n${newRule}`, 'utf-8');
      console.log(`✅ 已添加规则：${newRule}`);
      this.reload();
      return true;
    } catch (e) {
      console.error(`❌ 添加规则失败：${e.message}`);
      return false;
    }
  }
}

// CLI 模式
if (require.main === module) {
  const command = process.argv[2];
  const loader = new SensitiveWordLoader();
  
  if (command === 'list') {
    console.log('\n📋 敏感词词库:\n');
    loader.getRules().forEach((rule, i) => {
      console.log(`${i + 1}. [${rule.type}] ${rule.pattern}`);
      console.log(`   动作：${rule.action} | 说明：${rule.description}`);
      console.log();
    });
    
  } else if (command === 'stats') {
    const stats = loader.getStats();
    console.log('\n📊 词库统计:\n');
    console.log(`总规则数：${stats.total}`);
    console.log(`最后加载：${stats.lastLoaded}`);
    console.log('\n按类型:');
    console.log(`  - regex: ${stats.byType.regex}`);
    console.log(`  - keyword: ${stats.byType.keyword}`);
    console.log(`  - path: ${stats.byType.path}`);
    console.log('\n按动作:');
    console.log(`  - block: ${stats.byAction.block}`);
    console.log(`  - alert: ${stats.byAction.alert}`);
    console.log(`  - log: ${stats.byAction.log}`);
    console.log();
    
  } else if (command === 'test') {
    const text = process.argv.slice(3).join(' ');
    if (!text) {
      console.log('用法：node sensitive-word-loader.js test <文本>');
      process.exit(1);
    }
    
    const result = loader.check(text);
    if (result.passed) {
      console.log('✅ 通过检查，未检测到敏感词');
    } else {
      console.log('❌ 检测到敏感词:\n');
      result.violations.forEach((v, i) => {
        console.log(`${i + 1}. ${v.description}`);
        console.log(`   类型：${v.rule} | 动作：${v.action} | 严重程度：${v.severity}`);
        console.log(`   模式：${v.pattern}`);
        console.log();
      });
    }
    
  } else if (command === 'add') {
    const type = process.argv[3];
    const pattern = process.argv[4];
    const action = process.argv[5];
    const description = process.argv[6] || '';
    
    if (!type || !pattern || !action) {
      console.log('用法：node sensitive-word-loader.js add <type> <pattern> <action> [description]');
      process.exit(1);
    }
    
    loader.addRule(type, pattern, action, description);
    
  } else if (command === 'reload') {
    loader.reload();
    console.log('✅ 词库已重新加载');
    
  } else {
    console.log(`
敏感词词库加载器

用法:
  node sensitive-word-loader.js list      # 列出所有规则
  node sensitive-word-loader.js stats     # 查看统计信息
  node sensitive-word-loader.js test <文本> # 测试文本
  node sensitive-word-loader.js add <type> <pattern> <action> [desc] # 添加规则
  node sensitive-word-loader.js reload    # 重新加载

示例:
  node sensitive-word-loader.js test "这是测试文本"
  node sensitive-word-loader.js add regex "/test/g" block "测试规则"
  node sensitive-word-loader.js stats
    `);
  }
}

// 导出
module.exports = { SensitiveWordLoader };
