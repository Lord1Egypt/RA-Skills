/**
 * EnhancedSkill - P0-3 Skill结构增强
 * 
 * 增强后的 Skill 结构：
 * - procedure: 使用步骤（how to use）
 * - pitfalls: 常见错误（common mistakes）
 * - verification: 验证方法（how to verify it worked）
 * - examples: 使用示例
 * - metadata: 元数据（版本、作者、依赖等）
 */

const fs = require('fs');
const path = require('path');

const SKILLS_DIR = path.join(__dirname, '..', '..', 'skills');

/**
 * Skill 结构类
 */
class EnhancedSkill {
  constructor(data = {}) {
    // 原有字段
    this.name = data.name || '';
    this.description = data.description || '';
    
    // P0-3 新增字段
    this.procedure = data.procedure || [];           // 使用步骤
    this.pitfalls = data.pitfalls || [];             // 常见错误
    this.verification = data.verification || null;   // 验证方法
    this.examples = data.examples || [];             // 使用示例
    this.metadata = data.metadata || {};             // 元数据
    
    // 元数据默认值
    this.metadata = {
      version: this.metadata.version || '1.0.0',
      author: this.metadata.author || 'sensen',
      createdAt: this.metadata.createdAt || new Date().toISOString(),
      updatedAt: this.metadata.updatedAt || new Date().toISOString(),
      tags: this.metadata.tags || [],
      ...this.metadata
    };
  }

  /**
   * 添加步骤
   */
  addStep(step, description = '', tips = []) {
    this.procedure.push({
      step,
      description,
      tips,
      timestamp: new Date().toISOString()
    });
    this.metadata.updatedAt = new Date().toISOString();
    return this;
  }

  /**
   * 添加陷阱
   */
  addPitfall(mistake, consequence, solution = '') {
    this.pitfalls.push({
      mistake,
      consequence,
      solution,
      timestamp: new Date().toISOString()
    });
    this.metadata.updatedAt = new Date().toISOString();
    return this;
  }

  /**
   * 设置验证方法
   */
  setVerification(method, expectedResult, failureIndicator = '') {
    this.verification = {
      method,
      expectedResult,
      failureIndicator,
      timestamp: new Date().toISOString()
    };
    this.metadata.updatedAt = new Date().toISOString();
    return this;
  }

  /**
   * 添加示例
   */
  addExample(input, expectedOutput, description = '') {
    this.examples.push({
      input,
      expectedOutput,
      description,
      timestamp: new Date().toISOString()
    });
    this.metadata.updatedAt = new Date().toISOString();
    return this;
  }

  /**
   * 验证 Skill 完整性
   */
  validate() {
    const errors = [];
    
    if (!this.name) errors.push('缺少 name 字段');
    if (!this.description) errors.push('缺少 description 字段');
    if (this.procedure.length === 0) errors.push('缺少 procedure（使用步骤）');
    
    // 检查 procedure 格式
    for (let i = 0; i < this.procedure.length; i++) {
      const step = this.procedure[i];
      if (!step.step) {
        errors.push(`Procedure[${i}] 缺少 step 字段`);
      }
    }
    
    return {
      valid: errors.length === 0,
      errors,
      score: this.calculateCompleteness()
    };
  }

  /**
   * 计算完整度得分
   */
  calculateCompleteness() {
    let score = 0;
    const maxScore = 100;
    
    // 基础字段 (40%)
    if (this.name) score += 10;
    if (this.description) score += 10;
    if (this.procedure.length > 0) score += 10;
    if (this.pitfalls.length > 0) score += 5;
    if (this.verification) score += 5;
    
    // 增强字段 (60%)
    if (this.examples.length >= 2) score += 15;
    if (this.pitfalls.length >= 2) score += 15;
    if (this.metadata.version) score += 10;
    if (this.metadata.tags.length >= 2) score += 10;
    if (this.procedure.length >= 3) score += 10;
    
    return Math.min(score, maxScore);
  }

  /**
   * 导出为标准格式
   */
  toJSON() {
    return {
      name: this.name,
      description: this.description,
      procedure: this.procedure,
      pitfalls: this.pitfalls,
      verification: this.verification,
      examples: this.examples,
      metadata: this.metadata
    };
  }

  /**
   * 从文件加载
   */
  static load(skillPath) {
    if (!fs.existsSync(skillPath)) {
      throw new Error(`Skill 文件不存在: ${skillPath}`);
    }
    
    const data = JSON.parse(fs.readFileSync(skillPath, 'utf-8'));
    return new EnhancedSkill(data);
  }

  /**
   * 保存到文件
   */
  save(skillPath = null) {
    const pathToSave = skillPath || path.join(SKILLS_DIR, `${this.name}.skill.json`);
    
    fs.writeFileSync(pathToSave, JSON.stringify(this.toJSON(), null, 2), 'utf-8');
    console.log(`[EnhancedSkill] 💾 已保存: ${this.name}`);
    
    return this;
  }
}

/**
 * 验证现有 Skills 目录
 */
function auditSkills(skillsDir = SKILLS_DIR) {
  if (!fs.existsSync(skillsDir)) {
    return { error: `Skills 目录不存在: ${skillsDir}` };
  }
  
  const files = fs.readdirSync(skillsDir, { recursive: true })
    .filter(f => typeof f === 'string' && (f.endsWith('.md') || f.endsWith('.json')));
  
  const results = {
    total: files.length,
    enhanced: 0,
    legacy: 0,
    issues: []
  };
  
  for (const file of files) {
    const filePath = path.join(skillsDir, file);
    
    try {
      const content = fs.readFileSync(filePath, 'utf-8');
      
      if (file.endsWith('.json')) {
        const data = JSON.parse(content);
        // 检查是否是 Enhanced Skill
        if (data.procedure || data.pitfalls || data.verification) {
          results.enhanced++;
          const skill = new EnhancedSkill(data);
          const validation = skill.validate();
          if (!validation.valid) {
            results.issues.push({
              file,
              errors: validation.errors
            });
          }
        } else {
          results.legacy++;
        }
      } else if (file.endsWith('.md')) {
        // 检查 markdown 是否包含增强字段
        if (content.includes('## Procedure') || 
            content.includes('## Pitfalls') ||
            content.includes('## Verification')) {
          results.enhanced++;
        } else {
          results.legacy++;
        }
      }
    } catch (e) {
      results.issues.push({ file, error: e.message });
    }
  }
  
  return results;
}

/**
 * 打印 Skill 详情
 */
function printSkillDetails(skill) {
  console.log(`\n📋 Skill: ${skill.name}`);
  console.log('═'.repeat(60));
  console.log(`描述: ${skill.description}`);
  console.log(`完整度: ${skill.calculateCompleteness()}%`);
  
  if (skill.procedure.length > 0) {
    console.log('\n📝 Procedure（使用步骤）');
    for (const step of skill.procedure) {
      console.log(`  ${step.step}. ${step.description}`);
      if (step.tips && step.tips.length > 0) {
        console.log(`     💡 ${step.tips.join(', ')}`);
      }
    }
  }
  
  if (skill.pitfalls.length > 0) {
    console.log('\n⚠️ Pitfalls（常见错误）');
    for (const pitfall of skill.pitfalls) {
      console.log(`  ❌ ${pitfall.mistake}`);
      console.log(`     后果: ${pitfall.consequence}`);
      if (pitfall.solution) {
        console.log(`     解决: ${pitfall.solution}`);
      }
    }
  }
  
  if (skill.verification) {
    console.log('\n✅ Verification（验证方法）');
    console.log(`  方法: ${skill.verification.method}`);
    console.log(`  预期: ${skill.verification.expectedResult}`);
  }
  
  if (skill.examples.length > 0) {
    console.log('\n📖 Examples（使用示例）');
    for (const ex of skill.examples) {
      console.log(`  输入: ${ex.input}`);
      console.log(`  输出: ${ex.expectedOutput}`);
    }
  }
  
  console.log('\n元数据:', skill.metadata);
}

// 导出
module.exports = {
  EnhancedSkill,
  auditSkills,
  printSkillDetails
};
