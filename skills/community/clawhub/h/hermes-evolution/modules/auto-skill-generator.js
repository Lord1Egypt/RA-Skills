/**
 * AutoSkillGenerator - P2-1 自动技能创建
 * 5+工具调用自动生成Skill
 * 
 * 核心思路：
 * 1. 观察 Agent 的工具调用模式
 * 2. 识别重复工作流
 * 3. 自动生成 Skill 封装
 */

const fs = require('fs');
const path = require('path');

/**
 * 工具调用记录
 */
class ToolCall {
  constructor(toolName, args, result, timestamp = new Date()) {
    this.id = `call_${Date.now()}_${Math.random().toString(36).substr(2, 4)}`;
    this.toolName = toolName;
    this.args = args;
    this.result = result;
    this.timestamp = timestamp.toISOString();
    this.duration = 0;  // 毫秒
    this.success = true;
    this.error = null;
  }

  /**
   * 标记为成功
   */
  markSuccess(duration = 0) {
    this.success = true;
    this.duration = duration;
    return this;
  }

  /**
   * 标记为失败
   */
  markFailure(error) {
    this.success = false;
    this.error = error;
    return this;
  }
}

/**
 * 工作流模式
 */
class WorkflowPattern {
  constructor(name, toolCalls, frequency = 1) {
    this.id = `pattern_${Date.now()}`;
    this.name = name;
    this.toolCalls = toolCalls;  // 工具调用序列
    this.frequency = frequency;
    this.successRate = 1.0;
    this.avgDuration = 0;
    this.firstSeen = new Date().toISOString();
    this.lastSeen = new Date().toISOString();
  }

  /**
   * 增加使用频率
   */
  increment() {
    this.frequency++;
    this.lastSeen = new Date().toISOString();
  }

  /**
   * 更新成功率
   */
  updateSuccessRate(success) {
    const total = this.frequency;
    const successes = this.successRate * (total - 1);
    this.successRate = success ? (successes + 1) / total : successes / total;
  }
}

/**
 * 自动技能生成器
 */
class AutoSkillGenerator {
  constructor(options = {}) {
    this.callHistory = [];           // 工具调用历史
    this.patterns = new Map();      // 发现的工作流模式
    this.generatedSkills = [];      // 生成的技能
    this.minFrequency = options.minFrequency || 3;  // 最少出现次数
    this.windowSize = options.windowSize || 100;     // 分析窗口大小
    
    this.callLogFile = path.join(__dirname, '.tool-calls.jsonl');
    this.patternFile = path.join(__dirname, '.workflow-patterns.json');
    this.skillOutputDir = path.join(__dirname, '..', '..', 'skills', 'auto-generated');
    
    // 确保输出目录存在
    if (!fs.existsSync(this.skillOutputDir)) {
      fs.mkdirSync(this.skillOutputDir, { recursive: true });
    }
  }

  /**
   * 记录工具调用
   */
  recordCall(toolName, args, result) {
    const call = new ToolCall(toolName, args, result);
    this.callHistory.push(call);
    
    // 追加到日志
    fs.appendFileSync(this.callLogFile, JSON.stringify(call) + '\n', 'utf-8');
    
    // 维护窗口大小
    if (this.callHistory.length > this.windowSize) {
      this.callHistory.shift();
    }
    
    // 检测模式
    this.detectPatterns();
    
    return call;
  }

  /**
   * 检测工作流模式
   */
  detectPatterns() {
    // 简单的模式检测：连续的工具调用序列
    if (this.callHistory.length < 3) return;
    
    // 获取最近的调用序列
    const recentCalls = this.callHistory.slice(-5);
    const sequence = recentCalls.map(c => c.toolName).join(' → ');
    
    // 检查是否已存在
    let pattern = null;
    for (const [key, p] of this.patterns) {
      if (this.sequenceMatches(p.toolCalls.map(t => t.toolName), recentCalls.map(c => c.toolName))) {
        pattern = p;
        pattern.increment();
        // 更新成功率
        pattern.updateSuccessRate(recentCalls[recentCalls.length - 1].success);
        break;
      }
    }
    
    // 如果没找到且频率达标，创建新模式
    if (!pattern) {
      pattern = new WorkflowPattern(
        `自动模式_${sequence.substring(0, 30)}`,
        recentCalls,
        1
      );
      this.patterns.set(pattern.id, pattern);
    }
    
    // 如果频率达标，生成 Skill
    if (pattern.frequency >= this.minFrequency) {
      this.generateSkillFromPattern(pattern);
    }
  }

  /**
   * 检查两个序列是否匹配
   */
  sequenceMatches(seq1, seq2) {
    if (seq1.length !== seq2.length) return false;
    
    // 允许模糊匹配（工具名部分匹配）
    for (let i = 0; i < seq1.length; i++) {
      const t1 = seq1[i].toLowerCase();
      const t2 = seq2[i].toLowerCase();
      if (!t1.includes(t2) && !t2.includes(t1)) {
        return false;
      }
    }
    return true;
  }

  /**
   * 从模式生成 Skill
   */
  generateSkillFromPattern(pattern) {
    // 检查是否已生成过
    const existing = this.generatedSkills.find(s => 
      s.patternId === pattern.id
    );
    if (existing) return existing;
    
    const skillName = this.sanitizeName(pattern.name);
    const toolNames = pattern.toolCalls.map(c => c.toolName).join(', ');
    
    const skill = {
      name: skillName,
      description: `自动生成的技能：${toolNames}`,
      tier: 3,  // 完整级别
      procedure: pattern.toolCalls.map((call, i) => ({
        step: i + 1,
        description: `调用 ${call.toolName}`,
        tool: call.toolName,
        parameters: call.args ? Object.keys(call.args) : []
      })),
      pitfalls: [{
        mistake: '参数不正确',
        consequence: '工具调用失败',
        solution: '参考 examples 中的参数格式'
      }],
      verification: {
        method: '运行测试用例验证',
        expectedResult: '所有工具调用成功'
      },
      examples: pattern.toolCalls.slice(0, 2).map(call => ({
        input: JSON.stringify(call.args),
        output: call.success ? '成功' : `失败: ${call.error}`
      })),
      metadata: {
        version: '1.0.0',
        author: 'auto-generator',
        autoGenerated: true,
        patternId: pattern.id,
        frequency: pattern.frequency,
        successRate: pattern.successRate,
        generatedAt: new Date().toISOString()
      }
    };
    
    // 保存 Skill
    const skillFile = path.join(this.skillOutputDir, `${skillName}.skill.json`);
    fs.writeFileSync(skillFile, JSON.stringify(skill, null, 2), 'utf-8');
    
    this.generatedSkills.push(skill);
    
    console.log(`[AutoSkillGenerator] ✅ 自动生成 Skill: ${skillName}`);
    console.log(`   文件: ${skillFile}`);
    console.log(`   模式频率: ${pattern.frequency}`);
    console.log(`   成功率: ${(pattern.successRate * 100).toFixed(1)}%`);
    
    return skill;
  }

  /**
   * 清理名称
   */
  sanitizeName(name) {
    return name
      .replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_')
      .replace(/_+/g, '_')
      .substring(0, 50);
  }

  /**
   * 获取统计
   */
  getStats() {
    return {
      totalCalls: this.callHistory.length,
      patterns: this.patterns.size,
      candidatePatterns: Array.from(this.patterns.values())
        .filter(p => p.frequency >= this.minFrequency).length,
      generatedSkills: this.generatedSkills.length,
      topPatterns: Array.from(this.patterns.values())
        .sort((a, b) => b.frequency - a.frequency)
        .slice(0, 5)
        .map(p => ({
          name: p.name,
          frequency: p.frequency,
          successRate: p.successRate
        }))
    };
  }

  /**
   * 打印状态
   */
  printStatus() {
    const stats = this.getStats();
    
    console.log('\n📊 Auto Skill Generator 状态');
    console.log('═'.repeat(50));
    console.log(`工具调用: ${stats.totalCalls}`);
    console.log(`发现模式: ${stats.patterns}`);
    console.log(`候选模式: ${stats.candidatePatterns} (频率>=${this.minFrequency})`);
    console.log(`已生成 Skills: ${stats.generatedSkills}`);
    
    if (stats.topPatterns.length > 0) {
      console.log('\n高频模式:');
      for (const p of stats.topPatterns) {
        console.log(`  - ${p.name}`);
        console.log(`    频率: ${p.frequency}, 成功率: ${(p.successRate * 100).toFixed(1)}%`);
      }
    }
    
    console.log('═'.repeat(50));
  }

  /**
   * 加载历史调用
   */
  loadHistory() {
    if (!fs.existsSync(this.callLogFile)) return;
    
    const lines = fs.readFileSync(this.callLogFile, 'utf-8')
      .split('\n')
      .filter(l => l.trim());
    
    for (const line of lines.slice(-this.windowSize)) {
      try {
        const call = JSON.parse(line);
        this.callHistory.push(call);
      } catch (e) {}
    }
    
    console.log(`[AutoSkillGenerator] 📂 加载 ${this.callHistory.length} 条历史调用`);
  }

  /**
   * 触发一次模式分析
   */
  analyzeNow() {
    console.log('[AutoSkillGenerator] 🔍 立即分析...');
    this.detectPatterns();
    
    const stats = this.getStats();
    if (stats.candidatePatterns > 0) {
      console.log(`[AutoSkillGenerator] 📝 发现 ${stats.candidatePatterns} 个候选模式`);
    }
    
    return stats;
  }
}

// 导出
module.exports = {
  ToolCall,
  WorkflowPattern,
  AutoSkillGenerator
};
