#!/usr/bin/env node
/**
 * LLM Wiki 编译引擎
 * 从原始资料编译结构化知识库
 *
 * 用法：
 *   node compile.js                          # 使用默认配置
 *   node compile.js --config entities.json    # 从配置文件读取实体定义
 */

import { readFileSync, writeFileSync, readdirSync, statSync, existsSync } from 'fs';
import { join, basename } from 'path';
import { fileURLToPath } from 'url';

const __dirname = fileURLToPath(new URL('.', import.meta.url));
const ROOT = join(__dirname, '..');
const RAW_DIR = join(ROOT, 'raw');
const WIKI_DIR = join(ROOT, 'wiki');
const CONCEPTS_DIR = join(WIKI_DIR, 'concepts');
const ENTITIES_DIR = join(WIKI_DIR, 'entities');

// 解析命令行参数
function parseArgs() {
  const args = process.argv.slice(2);
  const config = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--config' && args[i + 1]) {
      config.configFile = args[i + 1];
      i++;
    }
  }
  return config;
}

// 读取源文件
function getSourceFiles() {
  if (!existsSync(RAW_DIR)) {
    console.log('⚠️  raw/ 目录不存在，跳过源文件读取');
    return [];
  }
  const files = readdirSync(RAW_DIR)
    .filter(f => f.endsWith('.md') && !f.startsWith('.'))
    .map(f => ({
      name: f,
      path: join(RAW_DIR, f),
      content: readFileSync(join(RAW_DIR, f), 'utf-8')
    }));
  return files;
}

// 写入 wiki 页面
function writePage(type, filename, content) {
  const dir = type === 'concept' ? CONCEPTS_DIR : ENTITIES_DIR;
  const path = join(dir, filename);
  writeFileSync(path, content, 'utf-8');
  console.log(`✓ ${type}: ${filename}`);
  return path;
}

// 生成 entity 页面
function generateEntity(name, data, sourceFile) {
  const date = new Date().toISOString().split('T')[0];
  let content = `# ${name}\n\n`;
  content += `> **实体类型:** ${data.type || '公司'}\n`;
  content += `> **来源文件:** [[${sourceFile}]]\n`;
  content += `> **编译日期:** ${date}\n\n`;

  if (data.overview) {
    content += `## 概述\n${data.overview}\n\n`;
  }

  if (data.attributes) {
    content += `## 核心属性\n`;
    for (const [key, value] of Object.entries(data.attributes)) {
      content += `- **${key}:** ${value}\n`;
    }
    content += '\n';
  }

  if (data.metrics) {
    content += `## 关键数据\n`;
    content += '| 指标 | 数值 |\n';
    content += '|------|------|\n';
    for (const [key, value] of Object.entries(data.metrics)) {
      content += `| ${key} | ${value} |\n`;
    }
    content += '\n';
  }

  if (data.business) {
    content += `## 业务详情\n${data.business}\n\n`;
  }

  if (data.related) {
    content += `## 关联概念\n`;
    for (const r of data.related) {
      content += `- [[${r}]]\n`;
    }
    content += '\n';
  }

  content += `## 引用\n- [[${sourceFile}]]\n\n`;
  content += `---\n*本页面由 LLM Wiki 编译生成*\n`;

  return content;
}

// 从配置文件读取实体定义
function loadEntitiesFromConfig(configFile) {
  const configPath = join(ROOT, configFile);
  if (!existsSync(configPath)) {
    console.error(`❌ 配置文件不存在: ${configPath}`);
    return [];
  }
  const config = JSON.parse(readFileSync(configPath, 'utf-8'));
  return config.entities || [];
}

// 主编译流程
async function compile() {
  console.log('📚 LLM Wiki 编译引擎\n');
  console.log(`源目录: ${RAW_DIR}`);
  console.log(`目标目录: ${WIKI_DIR}\n`);

  const args = parseArgs();
  const files = getSourceFiles();

  if (files.length > 0) {
    console.log(`发现 ${files.length} 个源文件:\n`);
    files.forEach(f => console.log(`  - ${f.name}`));
    console.log('');
  }

  // 编译实体页面
  console.log('🏗️ 编译实体页面...\n');

  if (args.configFile) {
    // 从配置文件读取实体
    const entities = loadEntitiesFromConfig(args.configFile);
    for (const entity of entities) {
      const content = generateEntity(entity.name, entity.data, entity.sourceFile || 'manual');
      writePage(entity.pageType || 'entity', entity.filename, content);
    }
  } else {
    console.log('ℹ️  未指定 --config，跳过实体编译');
    console.log('   使用方式: node compile.js --config entities.json');
    console.log('');
  }

  console.log('\n✅ 编译完成！\n');

  // 更新 index.md
  updateIndex();
}

function updateIndex() {
  const conceptFiles = existsSync(CONCEPTS_DIR)
    ? readdirSync(CONCEPTS_DIR).filter(f => f.endsWith('.md'))
    : [];
  const entityFiles = existsSync(ENTITIES_DIR)
    ? readdirSync(ENTITIES_DIR).filter(f => f.endsWith('.md'))
    : [];

  let index = '# LLM Wiki 知识库\n\n';
  index += `> 编译日期: ${new Date().toISOString().split('T')[0]}\n\n`;

  if (entityFiles.length > 0) {
    index += '## 实体索引\n\n';
    for (const f of entityFiles) {
      const name = f.replace('.md', '');
      index += `- [[${name}]]\n`;
    }
    index += '\n';
  }

  if (conceptFiles.length > 0) {
    index += '## 概念索引\n\n';
    for (const f of conceptFiles) {
      const name = f.replace('.md', '');
      index += `- [[${name}]]\n`;
    }
    index += '\n';
  }

  if (entityFiles.length === 0 && conceptFiles.length === 0) {
    index += '> 知识库为空，请通过 Ingest 流程添加内容。\n\n';
  }

  index += '---\n*由 LLM Wiki 编译引擎自动生成*\n';

  writeFileSync(join(WIKI_DIR, 'index.md'), index, 'utf-8');
  console.log('✓ index.md 已更新\n');
}

// 运行
compile().catch(console.error);
