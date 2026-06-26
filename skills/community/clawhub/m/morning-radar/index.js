#!/usr/bin/env node
/**
 * Morning Radar - 晨间资讯简报
 * 通用资讯自动收集与推送工具
 * 
 * 使用: node index.js [configPath]
 * 
 * 环境变量:
 *   BAIDU_API_KEY - 百度API Key
 *   FEISHU_APP_ID - 飞书App ID
 *   FEISHU_APP_SECRET - 飞书App Secret
 *   FEISHU_RECEIVER_OPEN_ID - 飞书接收者Open ID
 *   RADAR_QUERIES - 搜索查询（逗号分隔）
 *   RADAR_KEYWORDS - 过滤关键词（逗号分隔）
 *   RADAR_MAX_RESULTS - 每次搜索最大结果数（默认10）
 *   RADAR_MAX_ITEMS - 最终输出最大条数（默认15）
 *   RADAR_TITLE - 简报标题
 *   RADAR_SOURCE_NAME - 来源名称
 */

import { readFileSync, existsSync } from 'fs';
import { baiduSearch } from './lib/search.js';
import { parseResults, formatMessage } from './lib/format.js';
import { pushToFeishu } from './lib/push.js';

const CONFIG_PATH = process.argv[2] || './config.json';

// 默认配置
const DEFAULT_CONFIG = {
  search: {
    queries: ["AI人工智能", "大模型", "智能体"],
    keywords: ["AI", "大模型", "Agent", "人工智能"],
    maxResults: 10
  },
  output: {
    title: "🌅 晨间资讯简报",
    sourceName: "百度智能搜索",
    maxItems: 15
  }
};

function parseEnvList(value, defaultList) {
  if (!value) return defaultList;
  return value.split(',').map(s => s.trim()).filter(s => s);
}

function loadConfig() {
  // 从环境变量读取配置
  const envConfig = {
    baidu: {
      apiKey: process.env.BAIDU_API_KEY,
      apiUrl: "https://qianfan.baidubce.com/v2/ai_search/web_search"
    },
    feishu: {
      appId: process.env.FEISHU_APP_ID,
      appSecret: process.env.FEISHU_APP_SECRET,
      receiverOpenId: process.env.FEISHU_RECEIVER_OPEN_ID
    },
    search: {
      queries: parseEnvList(process.env.RADAR_QUERIES, DEFAULT_CONFIG.search.queries),
      keywords: parseEnvList(process.env.RADAR_KEYWORDS, DEFAULT_CONFIG.search.keywords),
      maxResults: parseInt(process.env.RADAR_MAX_RESULTS) || DEFAULT_CONFIG.search.maxResults
    },
    output: {
      title: process.env.RADAR_TITLE || DEFAULT_CONFIG.output.title,
      sourceName: process.env.RADAR_SOURCE_NAME || DEFAULT_CONFIG.output.sourceName,
      maxItems: parseInt(process.env.RADAR_MAX_ITEMS) || DEFAULT_CONFIG.output.maxItems
    }
  };
  
  // 检查环境变量是否完整
  const hasEnvConfig = envConfig.baidu.apiKey && 
                       envConfig.feishu.appId && 
                       envConfig.feishu.appSecret && 
                       envConfig.feishu.receiverOpenId;
  
  if (hasEnvConfig) {
    console.log("✓ 使用环境变量配置");
    return envConfig;
  }
  
  // 尝试从配置文件读取
  if (existsSync(CONFIG_PATH)) {
    try {
      console.log(`✓ 使用配置文件: ${CONFIG_PATH}`);
      const content = readFileSync(CONFIG_PATH, 'utf8');
      const fileConfig = JSON.parse(content);
      
      // 合并配置
      return {
        baidu: { ...envConfig.baidu, ...fileConfig.baidu },
        feishu: { ...envConfig.feishu, ...fileConfig.feishu },
        search: { ...DEFAULT_CONFIG.search, ...fileConfig.search },
        output: { ...DEFAULT_CONFIG.output, ...fileConfig.output }
      };
    } catch (e) {
      console.error(`❌ 加载配置文件失败: ${e.message}`);
    }
  }
  
  console.error("❌ 错误: 未找到配置");
  console.error("   请设置环境变量，或创建 config.json 文件");
  console.error("   详见 SKILL.md");
  process.exit(1);
}

async function main() {
  console.log("🌅 晨间雷达启动...\n");
  
  const config = loadConfig();
  
  // 验证配置
  if (!config.baidu?.apiKey) {
    console.error("❌ 错误: 未配置百度API Key");
    process.exit(1);
  }
  if (!config.feishu?.appId || !config.feishu?.appSecret) {
    console.error("❌ 错误: 未配置飞书应用信息");
    process.exit(1);
  }
  if (!config.feishu?.receiverOpenId) {
    console.error("❌ 错误: 未配置飞书接收者Open ID");
    process.exit(1);
  }
  
  console.log(`📋 搜索主题: ${config.search.queries.join(', ')}`);
  console.log(`🔑 过滤关键词: ${config.search.keywords.join(', ')}\n`);
  
  const allResults = [];
  
  // 执行搜索
  for (const query of config.search.queries) {
    console.log(`🔍 搜索: ${query}...`);
    const results = await baiduSearch(config.baidu.apiKey, query, config.search.maxResults);
    console.log(`   ✓ 获取 ${results.length} 条结果`);
    
    const articles = parseResults(results, config.search.keywords);
    allResults.push(...articles);
  }
  
  // 去重并限制数量
  const seen = new Set();
  const uniqueResults = allResults.filter(item => {
    const key = item.title.toLowerCase();
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  }).slice(0, config.output.maxItems);
  
  // 排序
  uniqueResults.sort((a, b) => {
    const order = { "高": 3, "中": 2, "低": 1 };
    return order[b.priority] - order[a.priority];
  });
  
  console.log(`\n✅ 共 ${uniqueResults.length} 条相关资讯`);
  
  // 格式化消息
  const message = formatMessage(uniqueResults, config.output);
  
  // 推送到飞书
  console.log("📤 推送到飞书...");
  await pushToFeishu(config.feishu, message);
  
  console.log("✅ 完成！");
}

main().catch(e => {
  console.error(`\n❌ 错误: ${e.message}`);
  process.exit(1);
});
