const { tavily } = require("@tavily/core");

// API Key 检查
const apiKey = process.env.TAVILY_API_KEY;

if (!apiKey) {
  console.error("❌ 错误: 请配置 TAVILY_API_KEY 环境变量");
  console.error("   访问 https://tavily.com 获取 API Key");
  console.error("   设置方式: export TAVILY_API_KEY=\"tvly-your-api-key\"");
  process.exit(1);
}

const args = process.argv.slice(2);

if (args.length < 1) {
  console.log(`
Tavily 搜索工具

用法: node tavily.js <命令> [参数]

命令:
  search <查询>           搜索网页
  extract <URL>           提取网页内容
  crawl <URL>             抓取网页
  map <URL>               绘制网页映射
  research <主题>         创建研究任务

选项:
  --depth <basic|advanced>   搜索深度 (默认: basic)
  --max-results <N>           最大结果数 (默认: 10)
  --instructions <文本>      抓取说明
  --max-pages <N>            最大页面数

示例:
  node tavily.js search "AI 新闻" --depth advanced --max-results 5
  node tavily.js extract "https://example.com"
  node tavily.js crawl "https://docs.example.com" --instructions "提取所有文档"
  node tavily.js map "https://example.com"
  node tavily.js research "Python 最新版本"
`);
  process.exit(1);
}

const command = args[0];
const queryOrUrl = args[1];

// 解析选项
const options = {};
for (let i = 2; i < args.length; i++) {
  if (args[i] === "--depth" && args[i + 1]) {
    options.searchDepth = args[i + 1];
    i++;
  } else if (args[i] === "--max-results" && args[i + 1]) {
    options.maxResults = parseInt(args[i + 1]);
    i++;
  } else if (args[i] === "--instructions" && args[i + 1]) {
    options.instructions = args[i + 1];
    i++;
  } else if (args[i] === "--max-pages" && args[i + 1]) {
    options.maxPages = parseInt(args[i + 1]);
    i++;
  } else if (args[i] === "--max-sources" && args[i + 1]) {
    options.maxSources = parseInt(args[i + 1]);
    i++;
  }
}

const tvly = tavily({ apiKey });

async function run() {
  try {
    switch (command) {
      case "search":
        if (!queryOrUrl) {
          console.error("❌ 错误: 请提供搜索查询");
          process.exit(1);
        }
        console.log(`🔍 搜索: ${queryOrUrl}\n`);
        const searchOptions = {
          searchDepth: options.searchDepth || "basic",
          maxResults: options.maxResults || 10,
          includeAnswer: true,
          includeRawContent: false,
          includeImages: false
        };
        const searchResp = await tvly.search(queryOrUrl, searchOptions);
        console.log("=== 搜索结果 ===\n");
        if (searchResp.answer) {
          console.log("📝 回答:", searchResp.answer, "\n");
        }
        searchResp.results?.forEach((r, i) => {
          console.log(`${i + 1}. ${r.title}`);
          console.log(`   ${r.url}`);
          console.log(`   ${r.content?.substring(0, 150)}...\n`);
        });
        break;

      case "extract":
        if (!queryOrUrl) {
          console.error("❌ 错误: 请提供 URL");
          process.exit(1);
        }
        console.log(`📄 提取: ${queryOrUrl}\n`);
        const extractResp = await tvly.extract(queryOrUrl);
        console.log("=== 提取结果 ===\n");
        extractResp.results?.forEach(r => {
          console.log(r.content?.substring(0, 2000));
        });
        break;

      case "crawl":
        if (!queryOrUrl) {
          console.error("❌ 错误: 请提供 URL");
          process.exit(1);
        }
        console.log(`🕷️ 抓取: ${queryOrUrl}\n`);
        if (!options.instructions) {
          console.warn("⚠️ 建议添加 --instructions 说明抓取目标");
        }
        const crawlResp = await tvly.crawl(queryOrUrl, options);
        console.log("=== 抓取结果 ===\n");
        crawlResp.results?.forEach((r, i) => {
          console.log(`${i + 1}. ${r.url}`);
          console.log(`   ${r.content?.substring(0, 200)}...\n`);
        });
        break;

      case "map":
        if (!queryOrUrl) {
          console.error("❌ 错误: 请提供 URL");
          process.exit(1);
        }
        console.log(`🗺️ 映射: ${queryOrUrl}\n`);
        const mapResp = await tvly.map(queryOrUrl, {
          depth: options.depth || 2,
          maxPages: options.maxPages || 20
        });
        console.log("=== 映射结果 ===\n");
        mapResp.results?.forEach((r, i) => {
          console.log(`${i + 1}. ${r.title} - ${r.url}`);
        });
        break;

      case "research":
        if (!queryOrUrl) {
          console.error("❌ 错误: 请提供研究主题");
          process.exit(1);
        }
        console.log(`📚 研究: ${queryOrUrl}\n`);
        const researchResp = await tvly.research(queryOrUrl, {
          depth: options.depth || "extensive",
          maxSources: options.maxSources || 10
        });
        console.log("=== 研究报告 ===\n");
        if (researchResp.answer) {
          console.log("📝 总结:", researchResp.answer, "\n");
        }
        researchResp.findings?.forEach((f, i) => {
          console.log(`\n--- 发现 ${i + 1} ---`);
          console.log(f.content);
          console.log("来源:", f.sources?.join(", "));
        });
        break;

      default:
        console.error(`❌ 未知命令: ${command}`);
        process.exit(1);
    }
  } catch (err) {
    console.error("❌ 错误:", err.message);
    process.exit(1);
  }
}

run();
