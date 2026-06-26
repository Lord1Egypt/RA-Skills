#!/usr/bin/env node
/**
 * Knowledge Base Archiver v1.1.0
 * 
 * 智能本地知识库归档系统
 * 
 * Usage:
 *   node archive.mjs <文件路径> [分类] [--ai-classify]
 *   node archive.mjs <文件夹路径> [--pattern "*.xlsx"] [--ai-classify]
 *   node archive.mjs search <关键词> [--category <分类>]
 *   node archive.mjs stats
 * 
 * Features:
 * - AI智能分类（基于文件内容+文件名的语义分类）
 * - 关键词匹配作为 fallback
 * - 批量归档整个文件夹
 * - 全文索引搜索
 * - 知识库统计信息
 * - 小文件存本地、大文件可对接云存储
 * - 支持 Excel/Word/PPT/PDF/TXT 等格式
 */

import { execSync, spawn } from 'child_process';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KB_ROOT = path.resolve(__dirname, '..');
const SIZE_LIMIT = 10 * 1024 * 1024; // 10MB
const INDEX_DIR = path.join(KB_ROOT, '_index');
const MANIFEST_PATH = path.join(INDEX_DIR, '_manifest.json');

// ============ 配置 ============

// 分类关键词（作为 fallback）
const CATEGORIES = {
  '工作文件': ['数据', '报表', '统计', '追踪', '明细', '汇总', '门店', '评分', '差评', '推广', '消耗', '投入', '营业', '销售', '业绩', '订单'],
  '方案文档': ['方案', '计划', '策略', '执行表', '管理', '动作', '流程', '制度', '规范', '规划', '提案', '报告'],
  '参考资料': ['话术', '模板', '技巧', '申诉', '回访', '指南', '手册', '培训', '教程', '案例', '经验', '方法'],
};

const VALID_CATEGORIES = [...Object.keys(CATEGORIES), '其他文档'];

// AI 分类配置
const AI_CLASSIFY_CONFIG = {
  // 使用 OpenClaw 的默认模型
  model: process.env.OPENCLAW_MODEL || 'default',
  // 或者调用本地 LLM API（如果配置了）
  apiEndpoint: process.env.OPENCLAW_API_ENDPOINT || null,
  // 最大文本长度（字符）
  maxTextLength: 2000,
};

// 云存储配置（可选）
const CLOUD_STORAGE = {
  enabled: false,
  // type: 'cos',        // 'cos' | 's3' | 'oss' | 'obs'
  // bucket: '',
  // prefix: 'knowledge-base/',
  // region: '',
  // command: (filepath, remotePath) => `coscmd upload "${filepath}" "${remotePath}"`,
};

// ============ 工具函数 ============

/**
 * 显示进度条
 */
function showProgress(current, total, filename = '') {
  const percent = Math.round((current / total) * 100);
  const barLength = 30;
  const filled = Math.round(barLength * current / total);
  const bar = '█'.repeat(filled) + '░'.repeat(barLength - filled);
  const name = filename.length > 20 ? filename.substring(0, 17) + '...' : filename;
  process.stdout.write(`\r[${bar}] ${percent}% (${current}/${total}) ${name}`);
}

/**
 * 高亮匹配文本
 */
function highlight(text, keyword) {
  const regex = new RegExp(`(${escapeRegex(keyword)})`, 'gi');
  return text.replace(regex, '\x1b[33m$1\x1b[0m'); // 黄色高亮
}

function escapeRegex(str) {
  return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
}

/**
 * 格式化文件大小
 */
function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' B';
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB';
  if (bytes < 1024 * 1024 * 1024) return (bytes / 1024 / 1024).toFixed(2) + ' MB';
  return (bytes / 1024 / 1024 / 1024).toFixed(2) + ' GB';
}

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const result = {
    command: null,         // 'archive' | 'search' | 'stats'
    target: null,          // 文件/文件夹路径
    category: null,        // 手动指定分类
    aiClassify: false,     // 是否使用 AI 分类
    pattern: null,         // 文件匹配模式
    searchKeyword: null,   // 搜索关键词
    searchCategory: null,  // 搜索过滤分类
  };
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    
    if (arg === '--ai-classify') {
      result.aiClassify = true;
    } else if (arg === '--pattern' && args[i + 1]) {
      result.pattern = args[++i];
    } else if (arg === '--category' && args[i + 1]) {
      if (args[i - 1] === 'search') {
        result.searchCategory = args[++i];
      } else {
        result.category = args[++i];
      }
    } else if (arg === 'search') {
      result.command = 'search';
    } else if (arg === 'stats') {
      result.command = 'stats';
    } else if (!arg.startsWith('-') && !result.target) {
      result.target = arg;
    } else if (result.command === 'search' && !arg.startsWith('-')) {
      result.searchKeyword = arg;
    }
  }
  
  // 默认命令
  if (!result.command && result.target) {
    result.command = 'archive';
  }
  
  return result;
}

// ============ 核心功能 ============

/**
 * 关键词分类（fallback）
 */
function keywordClassify(filename, summary = '') {
  const text = (filename + ' ' + summary).toLowerCase();
  for (const [cat, keywords] of Object.entries(CATEGORIES)) {
    if (keywords.some(k => text.includes(k.toLowerCase()))) {
      return cat;
    }
  }
  return '其他文档';
}

/**
 * AI 智能分类
 */
async function aiClassify(filename, text, summary) {
  const prompt = `你是一个文件分类助手。请根据以下文件信息判断它应该归类到哪个分类。

文件名: ${filename}
内容摘要: ${summary.substring(0, 500)}
内容片段: ${text.substring(0, AI_CLASSIFY_CONFIG.maxTextLength)}

可选分类:
1. 工作文件 - 数据报表、销售业绩、门店运营、统计分析等
2. 方案文档 - 计划方案、策略规划、制度流程、管理规范等
3. 参考资料 - 话术模板、培训教程、案例经验、指南手册等
4. 其他文档 - 不属于以上分类的文档

请只输出分类名称（工作文件/方案文档/参考资料/其他文档），不要其他内容。`;

  try {
    // 方法1: 尝试调用 OpenClaw 的默认 LLM
    let result;
    
    // 使用 openclaw chat 命令（如果可用）
    try {
      result = execSync(`openclaw chat --prompt "${escapeShell(prompt)}" --model ${AI_CLASSIFY_CONFIG.model}`, {
        encoding: 'utf-8',
        timeout: 30000,
      }).trim();
    } catch (e) {
      // openclaw 命令不可用，尝试其他方法
    }
    
    // 如果 openclaw 不可用，尝试直接调用 API
    if (!result && AI_CLASSIFY_CONFIG.apiEndpoint) {
      const response = await fetch(AI_CLASSIFY_CONFIG.apiEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          model: AI_CLASSIFY_CONFIG.model,
          messages: [{ role: 'user', content: prompt }],
          max_tokens: 20,
        }),
      });
      const data = await response.json();
      result = data.choices?.[0]?.message?.content?.trim();
    }
    
    // 如果都没有，使用 Python 调用本地模型（如果安装了）
    if (!result) {
      try {
        result = execSync(`python3 -c "
import sys
try:
    # 尝试使用 transformers
    from transformers import pipeline
    classifier = pipeline('zero-shot-classification', model='facebook/bart-large-mnli')
    result = classifier('${escapeShell(summary.substring(0, 200))}', ['工作文件', '方案文档', '参考资料', '其他文档'])
    print(result['labels'][0])
except ImportError:
    print('')
"`, { encoding: 'utf-8', timeout: 60000 }).trim();
      } catch (e) {
        // Python 也不可用
      }
    }
    
    // 验证结果是否为有效分类
    if (result && VALID_CATEGORIES.includes(result)) {
      return result;
    }
    
    // 尝试从结果中提取分类名
    for (const cat of VALID_CATEGORIES) {
      if (result && result.includes(cat)) {
        return cat;
      }
    }
    
    // AI 分类失败，fallback 到关键词
    console.log('  ⚠️  AI分类未返回有效结果，使用关键词分类');
    return keywordClassify(filename, summary);
    
  } catch (e) {
    console.log(`  ⚠️  AI分类失败: ${e.message}，使用关键词分类`);
    return keywordClassify(filename, summary);
  }
}

function escapeShell(str) {
  return str.replace(/"/g, '\\"').replace(/\n/g, ' ').replace(/\r/g, '');
}

/**
 * 提取文件文本内容
 */
function extractText(filePath, ext) {
  try {
    if (ext === 'xlsx') {
      return extractExcel(filePath);
    } else if (ext === 'docx') {
      return extractDocx(filePath);
    } else if (ext === 'pptx') {
      return extractPptx(filePath);
    } else if (['pdf', 'txt', 'csv', 'md', 'json', 'xml', 'html', 'log'].includes(ext)) {
      try {
        return fs.readFileSync(filePath, 'utf-8');
      } catch {
        return '';
      }
    }
    return `[${ext} 格式不支持全文提取]`;
  } catch (e) {
    return `[提取失败: ${e.message}]`;
  }
}

function extractExcel(filePath) {
  const out = execSync(`python3 -c "
import openpyxl, json
try:
    wb = openpyxl.load_workbook('${filePath}', data_only=True)
    lines = []
    for sheet in wb.sheetnames:
        lines.append(f'Sheet: {sheet}')
        for row in wb[sheet].iter_rows(values_only=True):
            if any(c for c in row if c):
                lines.append(' | '.join(str(c) if c else '' for c in row))
    print(json.dumps('\\n'.join(lines)))
except Exception as e:
    print(json.dumps(f'Error: {str(e)}'))
"`, { encoding: 'utf-8', maxBuffer: 50 * 1024 * 1024 });
  return JSON.parse(out.trim());
}

function extractDocx(filePath) {
  const out = execSync(`python3 -c "
import zipfile, re, json
try:
    with zipfile.ZipFile('${filePath}') as z:
        doc = z.read('word/document.xml').decode('utf-8')
        texts = re.findall(r'<w:t[^>]*>([^<]+)</w:t>', doc)
        print(json.dumps(''.join(texts)))
except Exception as e:
    print(json.dumps(f'Error: {str(e)}'))
"`, { encoding: 'utf-8', maxBuffer: 50 * 1024 * 1024 });
  return JSON.parse(out.trim());
}

function extractPptx(filePath) {
  const out = execSync(`python3 -c "
import zipfile, re, json
try:
    with zipfile.ZipFile('${filePath}') as z:
        slides = sorted([f for f in z.namelist() if f.startswith('ppt/slides/slide') and f.endswith('.xml')])
        texts = []
        for sf in slides:
            slide = z.read(sf).decode('utf-8')
            texts.extend(re.findall(r'<a:t>([^<]+)</a:t>', slide))
        print(json.dumps('\\n'.join(texts)))
except Exception as e:
    print(json.dumps(f'Error: {str(e)}'))
"`, { encoding: 'utf-8', maxBuffer: 50 * 1024 * 1024 });
  return JSON.parse(out.trim());
}

/**
 * 生成摘要
 */
function generateSummary(filename, text) {
  const clean = text.replace(/\n/g, ' ').replace(/\s+/g, ' ').trim();
  if (clean.length <= 100) return clean || `${filename}`;
  return clean.substring(0, 100) + '...';
}

/**
 * 上传到云存储
 */
function uploadToCloud(filePath, remotePath) {
  if (!CLOUD_STORAGE.enabled || !CLOUD_STORAGE.command) {
    console.log('  ☁️  云存储未配置，跳过上传');
    return null;
  }
  try {
    const cmd = CLOUD_STORAGE.command(filePath, remotePath);
    execSync(cmd, { timeout: 120000 });
    return remotePath;
  } catch (e) {
    console.error(`  ❌ 云上传失败: ${e.message}`);
    return null;
  }
}

/**
 * 初始化目录结构
 */
function initDirectories() {
  for (const cat of VALID_CATEGORIES) {
    const catDir = path.join(KB_ROOT, cat);
    if (!fs.existsSync(catDir)) fs.mkdirSync(catDir, { recursive: true });
  }
  if (!fs.existsSync(INDEX_DIR)) fs.mkdirSync(INDEX_DIR, { recursive: true });
}

/**
 * 更新清单
 */
function updateManifest(entry) {
  let manifest = [];
  try {
    manifest = JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf-8'));
  } catch {}
  manifest.push(entry);
  fs.writeFileSync(MANIFEST_PATH, JSON.stringify(manifest, null, 2), 'utf-8');
}

/**
 * 读取清单
 */
function readManifest() {
  try {
    return JSON.parse(fs.readFileSync(MANIFEST_PATH, 'utf-8'));
  } catch {
    return [];
  }
}

// ============ 命令实现 ============

/**
 * 归档单个文件
 */
async function archiveFile(filePath, options = {}) {
  const { category: manualCategory, aiClassify } = options;
  
  if (!fs.existsSync(filePath)) {
    console.error(`❌ 文件不存在: ${filePath}`);
    return null;
  }
  
  const filename = path.basename(filePath);
  const stats = fs.statSync(filePath);
  const size = stats.size;
  const ext = filename.split('.').pop().toLowerCase();
  
  // 检查是否已归档
  const manifest = readManifest();
  const existing = manifest.find(m => m.name === filename && m.size === size);
  if (existing) {
    console.log(`  ⏭️  已存在，跳过: ${filename}`);
    return existing;
  }
  
  console.log(`\n📄 处理: ${filename} (${formatSize(size)})`);
  
  // 提取文本
  const text = extractText(filePath, ext);
  const summary = generateSummary(filename, text);
  
  // 确定分类
  let category;
  if (manualCategory && VALID_CATEGORIES.includes(manualCategory)) {
    category = manualCategory;
    console.log(`📂 分类: ${category} (手动指定)`);
  } else if (aiClassify) {
    console.log('🤖 AI分类中...');
    category = await aiClassify(filename, text, summary);
    console.log(`📂 分类: ${category} (AI)`);
  } else {
    category = keywordClassify(filename, summary);
    console.log(`📂 分类: ${category} (关键词)`);
  }
  
  console.log(`📝 摘要: ${summary.substring(0, 60)}...`);
  
  let storagePath = '';
  
  if (size < SIZE_LIMIT) {
    // 本地存储
    const destDir = path.join(KB_ROOT, category);
    const destPath = path.join(destDir, filename);
    
    // 处理重名文件
    let finalPath = destPath;
    let counter = 1;
    while (fs.existsSync(finalPath)) {
      const name = filename.replace(/\.[^.]+$/, '');
      finalPath = path.join(destDir, `${name}_${counter}.${ext}`);
      counter++;
    }
    
    fs.copyFileSync(filePath, finalPath);
    storagePath = `${category}/${path.basename(finalPath)}`;
    console.log(`💾 本地: ${finalPath}`);
  } else {
    // 云存储
    console.log(`☁️  上传到云存储 (>10MB)...`);
    const remotePath = `knowledge-base/${category}/${filename}`;
    const result = uploadToCloud(filePath, remotePath);
    storagePath = result ? `cloud://${remotePath}` : '';
    console.log(`☁️  云端: ${storagePath}`);
  }
  
  // 创建全文索引
  const idxName = filename.replace(/\.[^.]+$/, '').replace(/[^\w\u4e00-\u9fa5]/g, '_');
  const idxPath = path.join(INDEX_DIR, `${idxName}.txt`);
  const idxContent = [
    `# ${filename}`,
    `分类: ${category}`,
    `大小: ${formatSize(size)}`,
    `日期: ${new Date().toISOString().split('T')[0]}`,
    `路径: ${storagePath}`,
    '---',
    '',
    text,
  ].join('\n');
  fs.writeFileSync(idxPath, idxContent, 'utf-8');
  console.log(`📇 索引: ${idxName}.txt (${text.length} 字符)`);
  
  // 更新清单
  const entry = {
    name: filename,
    category,
    size,
    textLength: text.length,
    storagePath,
    indexFile: `${idxName}.txt`,
    summary,
    archivedAt: new Date().toISOString(),
  };
  updateManifest(entry);
  
  return entry;
}

/**
 * 批量归档文件夹
 */
async function archiveDirectory(dirPath, options = {}) {
  const { pattern, aiClassify, category } = options;
  
  if (!fs.existsSync(dirPath)) {
    console.error(`❌ 目录不存在: ${dirPath}`);
    return;
  }
  
  // 收集所有文件
  const files = [];
  const patternRegex = pattern ? new RegExp(pattern.replace(/\*/g, '.*').replace(/\?/g, '.')) : null;
  
  function collectFiles(dir) {
    const items = fs.readdirSync(dir);
    for (const item of items) {
      const fullPath = path.join(dir, item);
      const stat = fs.statSync(fullPath);
      if (stat.isDirectory()) {
        collectFiles(fullPath);
      } else if (stat.isFile()) {
        if (!patternRegex || patternRegex.test(item)) {
          files.push(fullPath);
        }
      }
    }
  }
  
  collectFiles(dirPath);
  
  if (files.length === 0) {
    console.log('❌ 未找到匹配的文件');
    return;
  }
  
  console.log(`\n📚 批量归档: ${files.length} 个文件`);
  console.log(`📂 目录: ${dirPath}`);
  if (pattern) console.log(`🔍 模式: ${pattern}`);
  if (aiClassify) console.log('🤖 AI分类: 开启');
  console.log('');
  
  const results = {
    success: 0,
    skipped: 0,
    failed: 0,
  };
  
  for (let i = 0; i < files.length; i++) {
    showProgress(i + 1, files.length, path.basename(files[i]));
    try {
      const result = await archiveFile(files[i], { category, aiClassify });
      if (result) {
        results.success++;
      } else {
        results.skipped++;
      }
    } catch (e) {
      results.failed++;
      console.error(`\n❌ 处理失败: ${files[i]} - ${e.message}`);
    }
  }
  
  console.log('\n\n');
  console.log('═══════════════════════════════════');
  console.log('📊 归档完成统计');
  console.log('═══════════════════════════════════');
  console.log(`✅ 成功: ${results.success}`);
  console.log(`⏭️  跳过: ${results.skipped}`);
  console.log(`❌ 失败: ${results.failed}`);
  console.log('═══════════════════════════════════\n');
}

/**
 * 搜索命令
 */
function searchCommand(keyword, options = {}) {
  const { category: filterCategory } = options;
  
  if (!keyword) {
    console.error('用法: node archive.mjs search <关键词> [--category <分类>]');
    process.exit(1);
  }
  
  console.log(`\n🔍 搜索: "${keyword}"`);
  if (filterCategory) console.log(`📂 分类过滤: ${filterCategory}`);
  console.log('');
  
  const manifest = readManifest();
  const results = [];
  
  for (const entry of manifest) {
    if (filterCategory && entry.category !== filterCategory) continue;
    
    // 搜索文件名和摘要
    const nameMatch = entry.name.toLowerCase().includes(keyword.toLowerCase());
    const summaryMatch = entry.summary.toLowerCase().includes(keyword.toLowerCase());
    
    // 搜索索引文件内容
    let contentMatch = false;
    let matchContext = '';
    
    if (entry.indexFile) {
      const idxPath = path.join(INDEX_DIR, entry.indexFile);
      if (fs.existsSync(idxPath)) {
        const content = fs.readFileSync(idxPath, 'utf-8');
        const lines = content.split('\n');
        for (const line of lines) {
          if (line.toLowerCase().includes(keyword.toLowerCase())) {
            contentMatch = true;
            // 获取匹配上下文
            const idx = line.toLowerCase().indexOf(keyword.toLowerCase());
            const start = Math.max(0, idx - 30);
            const end = Math.min(line.length, idx + keyword.length + 30);
            matchContext = '...' + line.substring(start, end) + '...';
            break;
          }
        }
      }
    }
    
    if (nameMatch || summaryMatch || contentMatch) {
      results.push({
        ...entry,
        matchType: nameMatch ? '文件名' : summaryMatch ? '摘要' : '内容',
        matchContext,
      });
    }
  }
  
  if (results.length === 0) {
    console.log('❌ 未找到匹配结果');
    return;
  }
  
  console.log(`找到 ${results.length} 个结果:\n`);
  console.log('─────────────────────────────────────────────────────────');
  
  for (const r of results) {
    console.log(`\n📄 ${highlight(r.name, keyword)}`);
    console.log(`   分类: ${r.category}`);
    console.log(`   大小: ${formatSize(r.size)}`);
    console.log(`   时间: ${r.archivedAt?.split('T')[0] || '未知'}`);
    console.log(`   匹配: ${r.matchType}`);
    if (r.matchContext) {
      console.log(`   上下文: ${highlight(r.matchContext, keyword)}`);
    }
    console.log('─────────────────────────────────────────────────────────');
  }
}

/**
 * 统计命令
 */
function statsCommand() {
  console.log('\n📊 知识库统计信息\n');
  
  const manifest = readManifest();
  
  // 按分类统计
  const categoryStats = {};
  for (const cat of VALID_CATEGORIES) {
    categoryStats[cat] = {
      count: 0,
      totalSize: 0,
      recentDate: null,
    };
  }
  
  let totalCount = 0;
  let totalSize = 0;
  let oldestDate = null;
  let newestDate = null;
  
  for (const entry of manifest) {
    const cat = entry.category || '其他文档';
    if (!categoryStats[cat]) {
      categoryStats[cat] = { count: 0, totalSize: 0, recentDate: null };
    }
    
    categoryStats[cat].count++;
    categoryStats[cat].totalSize += entry.size || 0;
    totalCount++;
    totalSize += entry.size || 0;
    
    const date = entry.archivedAt?.split('T')[0];
    if (date) {
      if (!categoryStats[cat].recentDate || date > categoryStats[cat].recentDate) {
        categoryStats[cat].recentDate = date;
      }
      if (!newestDate || date > newestDate) newestDate = date;
      if (!oldestDate || date < oldestDate) oldestDate = date;
    }
  }
  
  // 计算索引目录大小
  let indexSize = 0;
  let indexCount = 0;
  if (fs.existsSync(INDEX_DIR)) {
    const idxFiles = fs.readdirSync(INDEX_DIR).filter(f => f.endsWith('.txt'));
    indexCount = idxFiles.length;
    for (const f of idxFiles) {
      indexSize += fs.statSync(path.join(INDEX_DIR, f)).size;
    }
  }
  
  console.log('═══════════════════════════════════════════════════════');
  console.log('📁 分类统计');
  console.log('═══════════════════════════════════════════════════════');
  console.log('');
  console.log('分类名称       文件数    总大小      最近归档');
  console.log('─────────────────────────────────────────────────────');
  
  for (const [cat, stats] of Object.entries(categoryStats)) {
    if (stats.count > 0) {
      const name = cat.padEnd(10, '　');
      const count = String(stats.count).padStart(4);
      const size = formatSize(stats.totalSize).padStart(10);
      const date = stats.recentDate || '-';
      console.log(`${name}    ${count}    ${size}    ${date}`);
    }
  }
  
  console.log('');
  console.log('═══════════════════════════════════════════════════════');
  console.log('📈 总体统计');
  console.log('═══════════════════════════════════════════════════════');
  console.log('');
  console.log(`📄 总文件数: ${totalCount}`);
  console.log(`💾 总大小: ${formatSize(totalSize)}`);
  console.log(`📇 索引文件: ${indexCount} 个 (${formatSize(indexSize)})`);
  console.log(`📅 归档时间范围: ${oldestDate || '无'} ~ ${newestDate || '无'}`);
  console.log('');
  console.log('═══════════════════════════════════════════════════════\n');
}

/**
 * 显示帮助
 */
function showHelp() {
  console.log(`
知识库归档系统 v1.1.0

用法:
  node archive.mjs <文件路径> [分类] [--ai-classify]
    归档单个文件
  
  node archive.mjs <文件夹路径> [--pattern "*.xlsx"] [--ai-classify]
    批量归档整个文件夹
  
  node archive.mjs search <关键词> [--category <分类>]
    搜索已归档文件
  
  node archive.mjs stats
    显示知识库统计信息

参数:
  --ai-classify      使用AI智能分类（基于文件内容和语义）
  --pattern <模式>   批量归档时按文件名过滤（如 "*.xlsx"）
  --category <分类>  指定分类或搜索时过滤分类

支持格式:
  Excel (.xlsx), Word (.docx), PowerPoint (.pptx),
  PDF, TXT, CSV, Markdown, JSON, XML, HTML

分类:
  工作文件 - 数据报表、销售业绩、门店运营、统计分析
  方案文档 - 计划方案、策略规划、制度流程、管理规范
  参考资料 - 话术模板、培训教程、案例经验、指南手册
  其他文档 - 不属于以上分类的文档
`);
}

// ============ 主程序 ============

async function main() {
  const args = parseArgs();
  
  if (!args.command) {
    showHelp();
    process.exit(0);
  }
  
  initDirectories();
  
  switch (args.command) {
    case 'archive':
      if (!args.target) {
        console.error('❌ 请指定文件或文件夹路径');
        process.exit(1);
      }
      
      const stat = fs.statSync(args.target);
      if (stat.isDirectory()) {
        await archiveDirectory(args.target, {
          pattern: args.pattern,
          aiClassify: args.aiClassify,
          category: args.category,
        });
      } else if (stat.isFile()) {
        await archiveFile(args.target, {
          category: args.category,
          aiClassify: args.aiClassify,
        });
        console.log('\n✅ 归档完成!');
      } else {
        console.error('❌ 不支持的路径类型');
        process.exit(1);
      }
      break;
      
    case 'search':
      searchCommand(args.searchKeyword, { category: args.searchCategory });
      break;
      
    case 'stats':
      statsCommand();
      break;
  }
}

main().catch(e => {
  console.error('❌ 错误:', e.message);
  process.exit(1);
});
