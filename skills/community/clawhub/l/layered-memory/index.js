#!/usr/bin/env node

/**
 * Layered Memory Management System
 * 基于 OpenViking 设计的分层记忆管理系统
 * 
 * 支持命令：
 *   generate <file|--all>  - 生成分层文件
 *   read <file> [layer]    - 读取记忆
 *   search <query> [layer] - 搜索记忆
 *   stats                  - 显示统计
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const BASE_PATH = path.join(process.env.HOME, 'clawd');
const SCRIPTS_PATH = path.join(BASE_PATH, 'scripts');

// 导入新模块
const MemoryExtractor = require(path.join(SCRIPTS_PATH, 'memory-extractor.js'));
const MemoryArchiver = require(path.join(SCRIPTS_PATH, 'memory-archiver.js'));

class LayeredMemory {
  constructor() {
    this.basePath = BASE_PATH;
    this.scriptsPath = SCRIPTS_PATH;
    this.extractor = new MemoryExtractor(BASE_PATH);
    this.archiver = new MemoryArchiver(BASE_PATH);
  }

  /**
   * 生成分层文件
   * @param {string} target - '--all' 或具体文件路径
   * @param {Object} options - 选项 { force, concurrent, config, dryRun, verbose }
   */
  generate(target = '--all', options = {}) {
    const {
      force = false,
      concurrent,
      config: configPath,
      dryRun = false,
      verbose = false
    } = options;
    
    console.log('🔄 生成分层文件...\n');
    
    const script = path.join(this.scriptsPath, 'generate-layers-simple.js');
    
    // 构建命令参数
    let cmd = `node "${script}" ${target === '--all' ? '--all' : `"${target}"`}`;
    if (force) cmd += ' --force';
    if (concurrent) cmd += ` --concurrent ${concurrent}`;
    if (configPath) cmd += ` --config "${configPath}"`;
    if (dryRun) cmd += ' --dry-run';
    if (verbose) cmd += ' --verbose';
    
    try {
      const output = execSync(cmd, { encoding: 'utf-8' });
      console.log(output);
      return { success: true, output };
    } catch (error) {
      console.error('❌ 生成失败:', error.message);
      return { success: false, error: error.message };
    }
  }

  /**
   * 读取记忆
   */
  read(filePath, layer = 'l1') {
    console.log(`📖 读取记忆 (${layer.toUpperCase()})...\n`);
    
    const script = path.join(this.scriptsPath, 'memory-reader.js');
    const cmd = `node "${script}" read "${filePath}" ${layer}`;
    
    try {
      const output = execSync(cmd, { encoding: 'utf-8' });
      console.log(output);
      return { success: true, content: output };
    } catch (error) {
      console.error('❌ 读取失败:', error.message);
      return { success: false, error: error.message };
    }
  }

  /**
   * 搜索记忆
   */
  search(query, layer = 'l1', limit = 5) {
    console.log(`🔍 搜索记忆: "${query}" (${layer.toUpperCase()})...\n`);
    
    const script = path.join(this.scriptsPath, 'memory-reader.js');
    const cmd = `node "${script}" search "${query}" ${layer}`;
    
    try {
      const output = execSync(cmd, { encoding: 'utf-8' });
      console.log(output);
      return { success: true, results: output };
    } catch (error) {
      console.error('❌ 搜索失败:', error.message);
      return { success: false, error: error.message };
    }
  }

  /**
   * 显示统计
   */
  stats() {
    console.log('📊 记忆系统统计...\n');
    
    const script = path.join(this.scriptsPath, 'memory-reader.js');
    const cmd = `node "${script}" stats`;
    
    try {
      const output = execSync(cmd, { encoding: 'utf-8' });
      console.log(output);
      return { success: true, stats: output };
    } catch (error) {
      console.error('❌ 获取统计失败:', error.message);
      return { success: false, error: error.message };
    }
  }

  /**
   * 自动维护：检查并生成缺失的分层文件
   * @param {Object} options - 选项 { force, concurrent, dryRun }
   */
  autoMaintain(options = {}) {
    console.log('🔧 自动维护：检查分层文件...\n');
    
    const memoryFiles = this._getAllMemoryFiles();
    const missing = [];
    const outdated = [];
    
    // 检查缺失和过时的文件
    for (const file of memoryFiles) {
      const l0Path = this._getLayerPath(file, 'abstract');
      const l1Path = this._getLayerPath(file, 'overview');
      
      const needsUpdate = options.force;
      let reason = '';
      
      if (!fs.existsSync(l0Path) || !fs.existsSync(l1Path)) {
        missing.push(file);
      } else if (!needsUpdate) {
        const srcStat = fs.statSync(file);
        const l0Stat = fs.statSync(l0Path);
        const l1Stat = fs.statSync(l1Path);
        
        if (srcStat.mtime > l0Stat.mtime || srcStat.mtime > l1Stat.mtime) {
          outdated.push(file);
        }
      }
    }
    
    const toProcess = [...missing, ...outdated];
    
    if (toProcess.length === 0) {
      console.log('✅ 所有文件都已是最新');
      return { success: true, maintained: 0 };
    }
    
    console.log(`发现 ${missing.length} 个缺失, ${outdated.length} 个过期，共 ${toProcess.length} 个文件需要处理\n`);
    
    // 使用新功能批量生成
    // 注意：这里的 generate 是同步 wrapper，内部调用异步但这里简化
    const result = this.generate('--all', {
      ...options,
      force: true // 强制处理这些文件
    });
    
    console.log(`\n✅ 维护完成，处理了 ${toProcess.length} 个文件`);
    return { 
      success: result.success, 
      maintained: toProcess.length,
      missing: missing.length,
      outdated: outdated.length
    };
  }

  /**
   * 从对话中提取记忆
   */
  extractMemories(messages, options = {}) {
    console.log('🧠 从对话中提取记忆...\n');
    
    try {
      const result = this.extractor.extractFromConversation(messages, options);
      console.log('✅ 记忆提取完成');
      console.log(`   用户记忆: ${Object.values(result.memories.user).flat().length} 条`);
      console.log(`   Agent 记忆: ${Object.values(result.memories.agent).flat().length} 条`);
      console.log(`   资源: ${result.memories.resources.length} 个`);
      return { success: true, result };
    } catch (error) {
      console.error('❌ 提取失败:', error.message);
      return { success: false, error: error.message };
    }
  }

  /**
   * 保存提取的记忆
   */
  saveExtractedMemories(memories, options = {}) {
    console.log('💾 保存提取的记忆...\n');
    
    try {
      const filePath = this.extractor.saveMemories(memories, options);
      console.log(`✅ 已保存到: ${filePath}`);
      
      // 自动生成分层
      console.log('\n🔄 自动生成分层...');
      this.generate(filePath);
      
      return { success: true, filePath };
    } catch (error) {
      console.error('❌ 保存失败:', error.message);
      return { success: false, error: error.message };
    }
  }

  /**
   * 归档旧记忆
   */
  archiveOld(options = {}) {
    console.log('🗄️  归档旧记忆...\n');
    
    try {
      const result = this.archiver.archiveOldMemories(options);
      return { success: true, ...result };
    } catch (error) {
      console.error('❌ 归档失败:', error.message);
      return { success: false, error: error.message };
    }
  }

  /**
   * 生成月度总结
   */
  monthlySummary(year, month) {
    console.log('📊 生成月度总结...\n');
    
    try {
      const summary = this.archiver.generateMonthlySummary(year, month);
      return { success: true, summary };
    } catch (error) {
      console.error('❌ 生成失败:', error.message);
      return { success: false, error: error.message };
    }
  }

  /**
   * 去重记忆
   */
  deduplicate(filePath) {
    console.log('🔍 去重记忆...\n');
    
    try {
      const result = this.archiver.deduplicateMemories(filePath);
      return { success: true, ...result };
    } catch (error) {
      console.error('❌ 去重失败:', error.message);
      return { success: false, error: error.message };
    }
  }

  /**
   * 获取所有记忆文件
   */
  _getAllMemoryFiles() {
    const files = [];
    
    // 主记忆
    const mainMemory = path.join(this.basePath, 'MEMORY.md');
    if (fs.existsSync(mainMemory)) {
      files.push(mainMemory);
    }
    
    // daily 目录
    const dailyDir = path.join(this.basePath, 'memory', 'daily');
    if (fs.existsSync(dailyDir)) {
      const dailyFiles = fs.readdirSync(dailyDir)
        .filter(f => f.endsWith('.md') && !f.startsWith('.'))
        .map(f => path.join(dailyDir, f));
      files.push(...dailyFiles);
    }
    
    return files;
  }

  /**
   * 获取分层文件路径
   */
  _getLayerPath(filePath, layer) {
    const dir = path.dirname(filePath);
    const basename = path.basename(filePath, '.md');
    return path.join(dir, `.${basename}.${layer}.md`);
  }
}

// CLI 接口
if (require.main === module) {
  const memory = new LayeredMemory();
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case 'generate':
      memory.generate(args[1] || '--all');
      break;
    
    case 'read':
      if (!args[1]) {
        console.error('❌ 请指定文件路径');
        process.exit(1);
      }
      memory.read(args[1], args[2] || 'l1');
      break;
    
    case 'search':
      if (!args[1]) {
        console.error('❌ 请指定搜索关键词');
        process.exit(1);
      }
      memory.search(args[1], args[2] || 'l1');
      break;
    
    case 'stats':
      memory.stats();
      break;
    
    case 'maintain':
      memory.autoMaintain();
      break;
    
    case 'extract':
      // 从命令行参数提取消息
      const messages = [
        { role: 'user', content: args[1] || '测试消息' },
        { role: 'assistant', content: args[2] || '测试回复' }
      ];
      const extracted = memory.extractMemories(messages);
      if (extracted.success && args.includes('--save')) {
        memory.saveExtractedMemories(extracted.result.memories);
      }
      break;
    
    case 'archive':
      const archiveOptions = {
        dryRun: args.includes('--dry-run'),
        thresholdDays: parseInt(args.find(a => a.startsWith('--days='))?.split('=')[1]) || 30
      };
      memory.archiveOld(archiveOptions);
      break;
    
    case 'summary':
      const year = parseInt(args[1]);
      const month = parseInt(args[2]);
      if (!year || !month) {
        console.error('❌ 请指定年份和月份');
        process.exit(1);
      }
      memory.monthlySummary(year, month);
      break;
    
    case 'dedupe':
      if (!args[1]) {
        console.error('❌ 请指定文件路径');
        process.exit(1);
      }
      memory.deduplicate(args[1]);
      break;
    
    default:
      console.log(`
Layered Memory Management System

使用方法:
  node index.js generate [file|--all]   # 生成分层文件
  node index.js read <file> [layer]     # 读取记忆 (l0/l1/l2)
  node index.js search <query> [layer]  # 搜索记忆
  node index.js stats                   # 显示统计
  node index.js maintain                # 自动维护
  node index.js extract <msg1> <msg2> [--save]  # 提取记忆
  node index.js archive [--dry-run] [--days=30] # 归档旧记忆
  node index.js summary <year> <month>  # 生成月度总结
  node index.js dedupe <file>           # 去重记忆

示例:
  node index.js generate --all
  node index.js read ~/clawd/MEMORY.md l1
  node index.js search "API" l1
  node index.js stats
  node index.js maintain
  node index.js extract "创建了工具" "已完成" --save
  node index.js archive --dry-run
  node index.js archive --days=60
  node index.js summary 2026 2
  node index.js dedupe ~/clawd/MEMORY.md
      `);
  }
}

module.exports = LayeredMemory;
