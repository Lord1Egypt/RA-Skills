#!/usr/bin/env node

/**
 * 自媒体文章生成主脚本
 * 根据主题和关键词自动搜索、汇总数据、生成文章
 */

const fs = require('fs');
const path = require('path');
const yargs = require('yargs/yargs');
const { hideBin } = require('yargs/helpers');

// 导入自定义模块
const { searchContent } = require('./search-content.js');
const { extractData } = require('./extract-data.js');
const { formatArticle } = require('./format-article.js');

const argv = yargs(hideBin(process.argv))
  .option('topic', {
    alias: 't',
    type: 'string',
    description: '文章主题',
    demandOption: true
  })
  .option('keywords', {
    alias: 'k',
    type: 'string',
    description: '关键词，用逗号分隔',
    default: ''
  })
  .option('platform', {
    alias: 'p',
    type: 'string',
    description: '目标平台：douyin, xiaohongshu, weibo, all',
    default: 'all'
  })
  .option('search-count', {
    alias: 'n',
    type: 'number',
    description: '搜索结果数量',
    default: 10
  })
  .option('days', {
    alias: 'd',
    type: 'number',
    description: '搜索时间范围（天）',
    default: 30
  })
  .option('deep-search', {
    type: 'boolean',
    description: '使用深度搜索模式',
    default: false
  })
  .option('output-dir', {
    alias: 'o',
    type: 'string',
    description: '输出目录',
    default: './output'
  })
  .option('dry-run', {
    type: 'boolean',
    description: '仅显示过程，不保存文件',
    default: false
  })
  .option('verbose', {
    alias: 'v',
    type: 'boolean',
    description: '显示详细过程',
    default: false
  })
  .help()
  .alias('help', 'h')
  .argv;

async function main() {
  console.log('🎬 开始生成自媒体文章...');
  console.log(`📝 主题：${argv.topic}`);
  console.log(`🔑 关键词：${argv.keywords || '使用默认关键词'}`);
  console.log(`📱 平台：${argv.platform}`);
  
  // 1. 搜索相关内容
  console.log('\n🔍 步骤1：搜索相关内容...');
  const searchResults = await searchContent({
    topic: argv.topic,
    keywords: argv.keywords.split(',').filter(k => k.trim()),
    count: argv.searchCount,
    days: argv.days,
    deep: argv.deepSearch,
    verbose: argv.verbose
  });
  
  if (argv.verbose) {
    console.log(`📊 搜索到 ${searchResults.sources?.length || 0} 个来源`);
  }
  
  // 2. 提取关键数据
  console.log('📋 步骤2：提取关键数据...');
  const extractedData = extractData(searchResults, {
    topic: argv.topic,
    verbose: argv.verbose
  });
  
  if (argv.verbose) {
    console.log('📈 提取的数据结构：');
    console.log(JSON.stringify(extractedData, null, 2));
  }
  
  // 3. 生成文章
  console.log('✍️ 步骤3：生成文章内容...');
  const platforms = argv.platform === 'all' 
    ? ['douyin', 'xiaohongshu', 'weibo'] 
    : [argv.platform];
  
  const articles = {};
  
  for (const platform of platforms) {
    console.log(`  生成 ${platform} 文章...`);
    articles[platform] = formatArticle(extractedData, platform);
  }
  
  // 4. 保存输出
  if (!argv.dryRun) {
    console.log('💾 步骤4：保存文章...');
    
    // 创建输出目录
    const outputDir = path.resolve(argv.outputDir);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }
    
    // 生成时间戳
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
    const topicSlug = argv.topic.replace(/[^\w\u4e00-\u9fa5]/g, '-').toLowerCase();
    
    for (const [platform, content] of Object.entries(articles)) {
      const filename = `${topicSlug}-${platform}-${timestamp}.md`;
      const filepath = path.join(outputDir, filename);
      
      fs.writeFileSync(filepath, content, 'utf8');
      console.log(`  已保存：${filename}`);
      
      // 同时保存一个简化的txt版本
      const txtContent = content.replace(/[#*`]/g, '').replace(/\n{3,}/g, '\n\n');
      const txtFilename = `${topicSlug}-${platform}-${timestamp}.txt`;
      const txtFilepath = path.join(outputDir, txtFilename);
      
      fs.writeFileSync(txtFilepath, txtContent, 'utf8');
    }
    
    // 保存原始数据（用于调试）
    const dataFilename = `${topicSlug}-data-${timestamp}.json`;
    const dataFilepath = path.join(outputDir, dataFilename);
    
    fs.writeFileSync(dataFilepath, JSON.stringify({
      topic: argv.topic,
      keywords: argv.keywords,
      searchResults,
      extractedData,
      generatedAt: new Date().toISOString()
    }, null, 2), 'utf8');
    
    console.log(`\n✅ 所有文章已保存到：${outputDir}`);
  } else {
    console.log('\n🔍 干运行模式，不保存文件');
  }
  
  // 5. 显示生成的文章预览
  console.log('\n📄 生成的文章预览：');
  console.log('='.repeat(50));
  
  for (const [platform, content] of Object.entries(articles)) {
    console.log(`\n📱 ${platform.toUpperCase()} 文章预览：`);
    console.log('-'.repeat(30));
    
    // 显示前10行
    const lines = content.split('\n').slice(0, 15);
    console.log(lines.join('\n'));
    
    if (content.split('\n').length > 15) {
      console.log('...（更多内容已保存到文件）');
    }
    
    console.log('-'.repeat(30));
  }
  
  console.log('='.repeat(50));
  console.log('🎉 文章生成完成！');
}

// 错误处理
main().catch(error => {
  console.error('❌ 生成文章时出错：', error.message);
  if (argv.verbose) {
    console.error(error.stack);
  }
  process.exit(1);
});