/**
 * 中央数据总线 v2.8.2
 *
 * 所有技能输出结构化 JSON，强制文件传递
 * 支持追溯、审计、续接执行
 *
 * v2.8.0 新增：
 * - 路径安全化（防止路径穿越攻击）
 * - 输入验证增强
 */

const fs = require('fs');
const path = require('path');

class DataBus {
  constructor(userInput, options = {}) {
    this.schemaVersion = '1.0';

    // 第 1 级：用户隔离（⭐ v2.8.0 新增路径安全化）
    const userId = this.sanitizePath(options.userId || this.getDefaultUserId());

    // 第 2 级：需求隔离（⭐ v2.8.0 新增路径安全化）
    const projectName = this.sanitizePath(this.extractProjectName(userInput));

    // ✅ 修复：使用 workspace 根目录作为输出目录基路径
    // __dirname = skills/prd-workflow/workflows
    // ../../.. = workspace 根目录
    const workspaceRoot = path.resolve(__dirname, '../../..');
    
    // ⭐ 支持自定义输出目录（通过环境变量）
    if (process.env.CUSTOM_OUTPUT_DIR) {
      this.outputDir = path.join(process.env.CUSTOM_OUTPUT_DIR, '');
      console.log(`⭐ 使用自定义输出目录（环境变量）: ${this.outputDir}`);
    } else {
      this.outputDir = path.join(workspaceRoot, 'output', userId, projectName, '');
    }

    // 生成会话 ID（用于锁机制）
    const timestamp = Date.now();
    const randomId = Math.random().toString(36).substring(7);
    this.sessionId = `${timestamp}-${randomId}`;

    console.log(`📁 输出目录：${this.outputDir}`);
    console.log(`   用户 ID: ${userId}`);
    console.log(`   需求名称：${projectName}`);

    this.ensureOutputDir();
    this.acquireLock();
  }

  /**
   * ⭐ v2.8.0 新增：路径安全化
   *
   * 防止路径穿越攻击，确保路径只包含安全字符
   *
   * @param {string} input - 待安全化的输入
   * @returns {string} 安全化后的路径组件
   */
  sanitizePath(input) {
    if (!input || typeof input !== 'string') {
      return 'default';
    }

    // 限制长度
    let safe = input.trim().slice(0, 100);

    // 只允许安全字符：字母、数字、中文、下划线、连字符、点
    safe = safe.replace(/[^\w\-\u4e00-\u9fa5.]/g, '_');

    // 防止路径穿越
    const dangerous = ['..', '/', '\\', '\0', '\n', '\r'];
    dangerous.forEach(d => {
      if (safe.includes(d)) {
        console.warn(`⚠️  检测到危险路径组件：${d}，已替换`);
        safe = safe.replace(new RegExp(d.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'g'), '_');
      }
    });

    // 防止空结果
    if (!safe || safe === '.' || safe === '_') {
      return 'default';
    }

    return safe;
  }

  /**
   * 获取默认用户 ID
   */
  getDefaultUserId() {
    // 从环境变量获取（OpenClaw 注入）
    if (process.env.OPENCLAW_USER_ID) {
      return process.env.OPENCLAW_USER_ID;
    }

    // 从渠道配置获取
    if (process.env.DINGTALK_USER_ID) {
      return `dingtalk-${process.env.DINGTALK_USER_ID}`;
    }

    // Fallback：单机模式
    return 'default';
  }

  /**
   * 从用户输入提取需求名称
   */
  extractProjectName(userInput) {
    // 智能提取：养老规划功能 → 养老规划
    const patterns = [
      /生成\s*(.+?)\s*的?\s*PRD/i,
      /生成\s*(.+?)\s*功能/i,
      /生成\s*(.+?)\s*需求/i,
      /生成\s*(.+?)\s*的?/i,
      /(.+?)\s*的\s*PRD/i,
      /(.+?)\s*PRD/i,
    ];

    for (const pattern of patterns) {
      const match = userInput.match(pattern);
      if (match && match[1] && match[1].trim().length > 1) {
        // ⭐ v2.8.0：使用安全化方法
        return this.sanitizePath(match[1].trim());
      }
    }

    // Fallback：使用时间戳
    return 'prd-' + Date.now().toString(36);
  }
  
  /**
   * 确保输出目录存在
   */
  ensureOutputDir() {
    if (!fs.existsSync(this.outputDir)) {
      fs.mkdirSync(this.outputDir, { recursive: true });
      console.log(`✅ 创建输出目录：${this.outputDir}`);
    }
  }
  
  /**
   * 获取目录锁
   */
  acquireLock() {
    const lockFile = path.join(this.outputDir, '.lock');
    
    if (fs.existsSync(lockFile)) {
      try {
        const lockData = JSON.parse(fs.readFileSync(lockFile, 'utf8'));
        const age = Date.now() - lockData.timestamp;
        
        // 如果锁超过 5 分钟，认为是 stale lock
        if (age < 300000) { // 5 分钟
          throw new Error(`检测到并发流程（${age}ms 前），请使用不同的 outputDir 或等待完成`);
        }
        
        console.warn(`⚠️  检测到过期锁文件（${age}ms 前），将覆盖`);
      } catch (error) {
        if (error.message.includes('检测到并发流程')) {
          throw error;
        }
        // JSON 解析错误或其他错误，忽略并覆盖
      }
    }
    
    // 创建锁文件
    fs.writeFileSync(lockFile, JSON.stringify({
      sessionId: this.sessionId,
      timestamp: Date.now(),
      pid: process.pid
    }), 'utf8');
    
    console.log(`🔒 获取锁：${this.sessionId}`);
  }
  
  /**
   * 释放目录锁
   */
  releaseLock() {
    const lockFile = path.join(this.outputDir, '.lock');
    
    if (fs.existsSync(lockFile)) {
      try {
        const lockData = JSON.parse(fs.readFileSync(lockFile, 'utf8'));
        if (lockData.sessionId === this.sessionId) {
          fs.unlinkSync(lockFile);
          console.log(`🔓 释放锁：${this.sessionId}`);
        }
      } catch (error) {
        console.warn(`⚠️  释放锁失败：${error.message}`);
      }
    }
  }
  
  /**
   * 写入数据到总线
   * 
   * @param {string} skill - 技能名称
   * @param {object} data - 技能输出数据
   * @param {object} quality - 质量验证结果
   * @param {object} traceability - 追溯信息
   * @returns {string} 文件路径
   */
  write(skill, data, quality, traceability = {}) {
    const filename = `${skill}.json`;
    const filepath = path.join(this.outputDir, filename);
    const backupPath = filepath + '.bak';
    
    const record = {
      version: this.schemaVersion,
      timestamp: new Date().toISOString(),
      skill: skill,
      data: data,
      quality: quality,
      traceability: traceability
    };
    
    // 先备份旧文件（如果存在）
    if (fs.existsSync(filepath)) {
      try {
        fs.copyFileSync(filepath, backupPath);
      } catch (error) {
        console.warn(`⚠️  备份失败：${backupPath}`);
      }
    }
    
    // 写入新文件
    fs.writeFileSync(filepath, JSON.stringify(record, null, 2), 'utf8');
    
    const status = quality.passed ? '✅' : '⚠️';
    console.log(`${status} 数据总线：${skill} → ${filepath}`);
    
    return filepath;
  }
  
  /**
   * 从总线读取数据
   * 
   * @param {string} skill - 技能名称
   * @returns {object|null} 数据记录，不存在返回 null
   */
  read(skill) {
    const filename = `${skill}.json`;
    const filepath = path.join(this.outputDir, filename);
    const backupPath = filepath + '.bak';
    
    if (!fs.existsSync(filepath)) {
      console.log(`⚠️  数据总线：${skill} 不存在`);
      return null;
    }
    
    try {
      const record = JSON.parse(fs.readFileSync(filepath, 'utf8'));
      console.log(`✅ 数据总线：读取 ${skill} ← ${filepath}`);
      return record;
    } catch (error) {
      console.warn(`⚠️  文件损坏：${filepath}`);
      console.warn(`   错误：${error.message}`);
      
      // 尝试从备份恢复
      if (fs.existsSync(backupPath)) {
        console.log('🔄 从备份恢复...');
        try {
          const backupRecord = JSON.parse(fs.readFileSync(backupPath, 'utf8'));
          console.log(`✅ 备份恢复成功：${skill}`);
          return backupRecord;
        } catch (backupError) {
          console.warn(`⚠️  备份文件也损坏：${backupPath}`);
        }
      }
      
      throw new Error(`文件损坏且无备份：${filepath}`);
    }
  }
  
  /**
   * 检查技能链完整性
   * 
   * @param {Array<string>} requiredSkills - 需要的技能列表
   * @returns {object} 检查结果
   */
  validateChain(requiredSkills) {
    const missing = [];
    const existing = [];
    
    requiredSkills.forEach(skill => {
      const filepath = path.join(this.outputDir, `${skill}.json`);
      if (fs.existsSync(filepath)) {
        existing.push(skill);
      } else {
        missing.push(skill);
      }
    });
    
    const result = {
      valid: missing.length === 0,
      missing: missing,
      existing: existing,
      allSkills: requiredSkills
    };
    
    if (result.valid) {
      console.log(`✅ 数据链完整：${existing.join(' → ')}`);
    } else {
      console.warn(`⚠️  数据链断裂：缺失 ${missing.join(', ')}`);
    }
    
    return result;
  }
  
  /**
   * 获取所有已完成技能
   * 
   * @returns {Array<string>} 技能列表
   */
  getCompletedSkills() {
    if (!fs.existsSync(this.outputDir)) {
      return [];
    }
    
    const files = fs.readdirSync(this.outputDir);
    const skills = files
      .filter(f => f.endsWith('.json'))
      .map(f => f.replace('.json', ''));
    
    return skills;
  }
  
  /**
   * 生成状态报告
   * 
   * @returns {object} 状态报告
   */
  getStatus() {
    const skills = this.getCompletedSkills();
    const allSkills = [
      'interview',
      'decomposition',
      'prd',
      'review',
      'flowchart',
      'quality',
      'design',
      'prototype',
      'export'
    ];
    
    const completed = allSkills.filter(s => skills.includes(s));
    const pending = allSkills.filter(s => !skills.includes(s));
    
    return {
      outputDir: this.outputDir,
      completed: completed,
      pending: pending,
      progress: `${completed.length}/${allSkills.length}`,
      nextStep: pending[0] || '完成'
    };
  }
  
  /**
   * 清理输出目录
   * 
   * @param {boolean} keepJson - 是否保留 JSON 文件
   */
  cleanup(keepJson = true) {
    if (!fs.existsSync(this.outputDir)) {
      return;
    }
    
    const files = fs.readdirSync(this.outputDir);
    
    files.forEach(file => {
      const filepath = path.join(this.outputDir, file);
      const stat = fs.statSync(filepath);
      
      if (stat.isFile()) {
        if (keepJson && file.endsWith('.json')) {
          return; // 保留 JSON 文件
        }
        fs.unlinkSync(filepath);
      }
    });
    
    console.log(`✅ 清理完成：${this.outputDir}`);
  }
}

module.exports = { DataBus };
