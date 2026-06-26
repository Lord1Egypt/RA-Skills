/**
 * Linguistic Landscape Analyzer - MCP Server
 * 语言景观分析 MCP 服务器
 * 
 * 功能：
 * - analyze_sentiment: 情感分析
 * - extract_keywords: 关键词提取
 * - list_notes: 笔记列表
 * - generate_weekly_report: 周报生成
 */

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";
import Sentiment from "sentiment";
import extractor from "keyword-extractor";
import fs from "fs";
import path from "path";
import { fileURLToPath } from "url";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// 创建 MCP 服务器
const server = new McpServer({
  name: "linguistic-landscape-analyzer",
  version: "1.0.0",
  description: "语言景观分析 MCP 工具 - 小红书情感分析与关键词提取"
});

// 初始化情感分析器
const sentiment = new Sentiment();

// 加载中文情感词典（简单版）
const positiveWords = ['好', '喜欢', '爱', '赞', '棒', '优秀', '满意', '推荐', '值得', '好用', '强大', '高效', '实用', '清晰', '简单'];
const negativeWords = ['差', '不好', '讨厌', '失望', '糟糕', '垃圾', '坑', '避雷', '劝退', '复杂', '难用', '慢', '贵', '问题'];

// 简单的中文分词（按字符分割 + 常用词匹配）
function simpleChineseTokenize(text) {
  // 移除标点和空格
  const cleaned = text.replace(/[^\w\s\u4e00-\u9fa5]/g, ' ');
  // 简单分割（按 2-3 字切分）
  const words = [];
  for (let i = 0; i < cleaned.length - 1; i++) {
    const word2 = cleaned.substring(i, i + 2);
    const word3 = cleaned.substring(i, i + 3);
    if (/\p{Script=Han}/u.test(word2[0]) && word2.trim()) words.push(word2);
    if (/\p{Script=Han}/u.test(word3[0]) && word3.trim()) i++;
  }
  return cleaned.split(/\s+/).filter(w => w.length > 0);
}

// 工具 1: analyze_sentiment - 情感分析
server.tool(
  "analyze_sentiment",
  "情感分析工具 - 分析文本的情感倾向（支持中文，基于简单词典）",
  {
    text: z.string().describe("要分析的文本内容"),
    language: z.enum(["zh", "en"]).optional().default("zh").describe("语言类型：zh(中文) 或 en(英文)")
  },
  async ({ text, language }) => {
    try {
      let score = 0;
      let positive = [];
      let negative = [];
      
      if (language === "zh") {
        // 中文情感分析（基于简单词典）
        const words = simpleChineseTokenize(text);
        words.forEach(word => {
          if (positiveWords.some(pw => word.includes(pw))) {
            score++;
            positive.push(word);
          } else if (negativeWords.some(nw => word.includes(nw))) {
            score--;
            negative.push(word);
          }
        });
      } else {
        // 英文情感分析（使用 sentiment 库）
        const result = sentiment.analyze(text);
        score = result.score;
        positive = result.positive || [];
        negative = result.negative || [];
      }
      
      const comparative = score / (text.length || 1);
      const sentimentLabel = score > 0 ? "positive" : score < 0 ? "negative" : "neutral";
      const confidence = Math.min(Math.abs(comparative) * 2, 1);
      
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            score,
            comparative: parseFloat(comparative.toFixed(3)),
            sentiment: sentimentLabel,
            confidence: parseFloat(confidence.toFixed(2)),
            positive,
            negative,
            textLength: text.length,
            language
          }, null, 2)
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: `情感分析失败：${error.message}`
        }],
        isError: true
      };
    }
  }
);

// 工具 2: extract_keywords - 关键词提取
server.tool(
  "extract_keywords",
  "关键词提取工具 - 从文本中提取关键词（支持中文）",
  {
    text: z.string().describe("要提取关键词的文本"),
    limit: z.number().optional().default(10).describe("返回关键词数量上限"),
    language: z.enum(["zh", "en"]).optional().default("zh").describe("语言类型")
  },
  async ({ text, limit, language }) => {
    try {
      let keywords = [];
      
      if (language === "zh") {
        // 中文关键词提取（简单版）
        const words = simpleChineseTokenize(text);
        const wordCount = {};
        
        words.forEach(word => {
          if (word.length >= 2) { // 忽略单字
            wordCount[word] = (wordCount[word] || 0) + 1;
          }
        });
        
        keywords = Object.entries(wordCount)
          .sort((a, b) => b[1] - a[1])
          .slice(0, limit)
          .map(([word]) => word);
      } else {
        // 英文关键词提取
        keywords = extractor.extract(text, {
          language: "english",
          return_changed_case: false
        }).slice(0, limit);
      }
      
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            keywords,
            count: keywords.length,
            limit,
            language
          }, null, 2)
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: `关键词提取失败：${error.message}`
        }],
        isError: true
      };
    }
  }
);

// 工具 3: list_notes - 笔记列表
server.tool(
  "list_notes",
  "笔记列表工具 - 读取 CSV 文件中的小红书笔记数据",
  {
    source: z.enum(["csv", "sample"]).optional().default("sample").describe("数据源类型"),
    limit: z.number().optional().default(10).describe("返回笔记数量上限"),
    sortBy: z.enum(["likes", "collects", "comments", "date"]).optional().default("date").describe("排序字段"),
    order: z.enum(["asc", "desc"]).optional().default("desc").describe("排序顺序")
  },
  async ({ source, limit, sortBy, order }) => {
    try {
      let csvPath;
      
      const projectRoot = path.resolve(__dirname, "..");
      const dataDir = path.join(projectRoot, "data");
      if (source === "sample") {
        csvPath = path.join(dataDir, "sample.csv");
      } else {
        csvPath = path.join(dataDir, "notes.csv");
      }
      
      if (!fs.existsSync(csvPath)) {
        return {
          content: [{
            type: "text",
            text: `数据文件不存在：${csvPath}`
          }],
          isError: true
        };
      }
      
      const csvContent = fs.readFileSync(csvPath, "utf-8");
      const lines = csvContent.trim().split("\n");
      const headers = lines[0].split(",");
      
      const notes = lines.slice(1).map(line => {
        const values = line.split(",");
        const note = {};
        headers.forEach((header, index) => {
          note[header] = values[index] || "";
        });
        return note;
      });
      
      // 排序
      notes.sort((a, b) => {
        let aVal = a[sortBy] || 0;
        let bVal = b[sortBy] || 0;
        
        if (sortBy === "date") {
          aVal = new Date(aVal);
          bVal = new Date(bVal);
        } else {
          aVal = parseInt(aVal) || 0;
          bVal = parseInt(bVal) || 0;
        }
        
        return order === "desc" ? bVal - aVal : aVal - bVal;
      });
      
      const result = notes.slice(0, limit);
      
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            notes: result,
            total: result.length,
            source,
            sortBy,
            order
          }, null, 2)
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: `读取笔记失败：${error.message}`
        }],
        isError: true
      };
    }
  }
);

// 工具 4: generate_weekly_report - 生成周报（简化版 MVP）
server.tool(
  "generate_weekly_report",
  "周报生成工具 - 生成语言景观分析周报（Markdown 格式）",
  {
    startDate: z.string().optional().describe("开始日期 (YYYY-MM-DD)"),
    endDate: z.string().optional().describe("结束日期 (YYYY-MM-DD)"),
    outputPath: z.string().optional().describe("输出文件路径"),
    limit: z.number().optional().default(10).describe("分析笔记数量上限")
  },
  async ({ limit }) => {
    try {
      // 直接读取 CSV 数据（简化实现）
      const projectRoot = path.resolve(__dirname, "..");
      const csvPath = path.join(projectRoot, "data", "sample.csv");
      
      if (!fs.existsSync(csvPath)) {
        return {
          content: [{ type: "text", text: `数据文件不存在：${csvPath}` }],
          isError: true
        };
      }
      
      const csvContent = fs.readFileSync(csvPath, "utf-8");
      const lines = csvContent.trim().split("\n");
      const headers = lines[0].split(",");
      
      const notes = lines.slice(1).map(line => {
        const values = line.split(",");
        const note = {};
        headers.forEach((header, index) => {
          note[header] = values[index] || "";
        });
        return note;
      }).slice(0, limit || 10);
      
      // 分析情感
      const sentimentResults = notes.map(note => {
        const content = note.content || note.title || "";
        return {
          title: note.title,
          likes: parseInt(note.likes) || 0,
          sentiment: "positive" // 简化处理
        };
      });
      
      // 生成 Markdown 报告
      const reportDate = new Date().toISOString().split("T")[0];
      const report = `# 语言景观周报

**生成时间：** ${reportDate}  
**分析笔记数：** ${notes.length}

## 📊 数据概览

| 指标 | 数值 |
|------|------|
| 总笔记数 | ${notes.length} |
| 总点赞数 | ${notes.reduce((sum, n) => sum + (parseInt(n.likes) || 0), 0)} |
| 总收藏数 | ${notes.reduce((sum, n) => sum + (parseInt(n.collects) || 0), 0)} |
| 总评论数 | ${notes.reduce((sum, n) => sum + (parseInt(n.comments) || 0), 0)} |

## 🔥 热门笔记 TOP5

${notes.slice(0, 5).map((note, index) => `${index + 1}. **${note.title}** - ${note.likes} 赞`).join("\n")}

## 💡 关键词分析

（待实现：关键词提取功能）

## 📈 建议

（待实现：智能建议生成）

---
*报告由 Linguistic Landscape Analyzer 自动生成*
`;
      
      // 保存报告（安全路径：技能目录内的 reports 文件夹）
      const projectRoot = path.resolve(__dirname, "..");
      const outputDir = path.join(projectRoot, "reports");
      if (!fs.existsSync(outputDir)) {
        fs.mkdirSync(outputDir, { recursive: true });
      }
      
      const outputPath = path.join(outputDir, `周报_${reportDate}.md`);
      fs.writeFileSync(outputPath, report, "utf-8");
      
      return {
        content: [{
          type: "text",
          text: JSON.stringify({
            status: "success",
            reportPath: outputPath,
            summary: {
              totalNotes: notes.length,
              topNote: notes[0]?.title || "N/A",
              reportDate
            }
          }, null, 2)
        }]
      };
    } catch (error) {
      return {
        content: [{
          type: "text",
          text: `生成周报失败：${error.message}`
        }],
        isError: true
      };
    }
  }
);

// 启动服务器
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("✅ 语言景观分析 MCP 服务器已启动");
  console.error("📦 可用工具：analyze_sentiment, extract_keywords, list_notes, generate_weekly_report");
  console.error("🔌 传输方式：stdio");
}

main().catch((error) => {
  console.error("❌ 服务器启动失败:", error);
  process.exit(1);
});
