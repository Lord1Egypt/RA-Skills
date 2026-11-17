---
name: kepler-agent-search
description: >
  支持 Bing/Baidu 通用搜索、知乎中文问答社区、小红书生活方式社区、GitHub代码仓库、
  arXiv学术论文、199it互联网数据、东方财富财经资讯、智联招聘、前程无忧等多源搜索【按需持续增加】。
  从多个平台搜索内容，实现统一搜索和内容提取，帮助AI Agent获取全网信息。
  
  只要涉及获取网络信息——无论是搜索资讯、调研主题、查找资料、提取文章、多源对比——
  都应立即调用。即使用户未明确说"搜索"，只要需要网络信息支撑，自动使用本skill。
compatibility: Requires mcp__kepler__web_search and mcp__kepler__web_reader tools
---

## 前置要求

本技能依赖 **Kepler MCP 服务**，使用前需配置 MCP 服务器。

**快速配置**：
```json
{
  "mcpServers": {
    "kepler": {
      "type": "sse",
      "url": "https://apisec.cn/sse",
      "headers": { "Authorization": "Bearer <API-KEY>" }
    }
  }
}
```

📖 **[完整安装指南](references/mcp-setup.md)** — 支持 Claude Code、OpenClaw、Codex 等多个 Agent 平台

## 常驻规则（全程适用）

1. **数据源选择策略**：
   - 通用问题 → 使用 Bing/Baidu 搜索
   - 中文知识问答/经验分享 → 优先搜索知乎
   - 生活方式/种草/攻略/消费决策 → 优先搜索小红书 (xhs)
   - 代码/开源项目 → 优先搜索 GitHub
   - 学术论文/研究 → 优先搜索 arXiv
   - 互联网数据/行业报告 → 优先搜索 199it
   - 财经/股票/基金资讯 → 优先搜索东方财富 (eastmoney)
   - 招聘职位/工作机会 → 优先搜索智联招聘 (zhaopin) 或前程无忧 (51job)
   - 综合调研 → 多数据源并行搜索

2. **搜索优先原则**：涉及时效性内容（新闻、最新动态）时，先用 `mcp__kepler__web_search` 获取最新信息，不要依赖训练数据。

3. **平台内容特殊处理**：
   - 优先使用专用引擎搜索，遇到不可用的时候可以降级为通用搜索
   - 知乎文章/回答、小红书笔记、GitHub项目可以直接使用 `mcp__kepler__web_reader` 读取完整内容
   - 部分平台内容可能需要特定关键词格式

4. **参数规范**（重点！engines 参数每次只能指定单个引擎）：
   - `mcp__kepler__web_search`: `query` (必填), `engines` (可选, 默认 ['bing'], 可选值: ['bing'], ['baidu'], ['zhihu'], ['xhs'], ['github'], ['arxiv'], ['199it'], ['eastmoney'], ['zhaopin'], ['51job']), `max_results` (可选, 默认10, 最大50), `fetch_content` (可选, 默认false), `max_fetch` (可选, 默认3, 最大10)
   - `mcp__kepler__web_reader`: `url` (必填), `format` (可选, markdown/text/html, 默认 markdown), `extract_article` (可选, 默认 true)

## 搜索路由表

按场景分类的详细参考文档：

| 分类 | 说明 | 参考文档 |
|------|------|----------|
| **search** | 网页搜索 | [references/search.md](references/search.md) |
| **social** | 社交媒体 | [references/social.md](references/social.md) |
| **github** | 开源代码 | [references/github.md](references/github.md) |
| **arxiv** | 学术研究 | [references/arxiv.md](references/arxiv.md) |
| **data** | 行业数据 | [references/data.md](references/data.md) |
| **finance** | 财经资讯 | [references/finance.md](references/finance.md) |
| **career** | 招聘信息 | [references/career.md](references/career.md) |

### 快速选择指南

| 用户意图 | 推荐策略 | 工具 | 参数示例 |
|---------|---------|------|---------|
| 通用搜索 | Bing/Baidu 搜索 | mcp__kepler__web_search | `engines: ["bing"]` 或 `engines: ["baidu"]` |
| 知乎搜索 | 指定 zhihu 引擎 | mcp__kepler__web_search | `engines: ["zhihu"]` |
| 小红书搜索 | 指定 xhs 引擎 | mcp__kepler__web_search | `engines: ["xhs"]` |
| GitHub搜索 | 指定 github 引擎 | mcp__kepler__web_search | `engines: ["github"]` |
| 学术论文 | 指定 arxiv 引擎 | mcp__kepler__web_search | `engines: ["arxiv"]` |
| 行业数据 | 指定 199it 引擎 | mcp__kepler__web_search | `engines: ["199it"]` |
| 财经资讯 | 指定 eastmoney 引擎 | mcp__kepler__web_search | `engines: ["eastmoney"]` |
| 智联招聘 | 指定 zhaopin 引擎 | mcp__kepler__web_search | `engines: ["zhaopin"]` |
| 前程无忧 | 指定 51job 引擎 | mcp__kepler__web_search | `engines: ["51job"]` |
| 多源对比 | 依次执行多个引擎 | mcp__kepler__web_search | 依次调用不同 engines |
| 读取网页 | 直接访问 URL | mcp__kepler__web_reader | `url: "..."` |
| 深度调研 | 搜索 → 读取 → 分析 | 两者组合 | - |

## 搜索模式

### 模式一：单源搜索

**Bing 通用搜索：**
```
用户：「搜索 Python 异步编程最佳实践」
→ 调用 mcp__kepler__web_search，query="Python 异步编程最佳实践"
```

**Baidu 通用搜索：**
```
用户：「百度搜索 Python 异步编程最佳实践」
→ 调用 mcp__kepler__web_search，query="Python 异步编程最佳实践", engines=["baidu"]
```

**知乎定向搜索（使用 engines 参数）：**
```
用户：「知乎上关于 Python 异步编程的讨论」
→ 调用 mcp__kepler__web_search，query="Python 异步编程", engines=["zhihu"]
```

**知乎定向搜索（使用关键词）：**
```
用户：「知乎上关于 Python 异步编程的讨论」
→ 调用 mcp__kepler__web_search，query="Python 异步编程 site:zhihu.com" 或 "Python 异步编程 知乎"
```

**小红书定向搜索：**
```
用户：「小红书上关于上海咖啡探店的分享」
→ 调用 mcp__kepler__web_search，query="上海咖啡探店", engines=["xhs"]
```

**GitHub 代码搜索：**
```
用户：「搜索 React 组件库开源项目」
→ 调用 mcp__kepler__web_search，query="React component library", engines=["github"]
```

**arXiv 学术论文搜索：**
```
用户：「搜索 transformer 架构的最新论文」
→ 调用 mcp__kepler__web_search，query="transformer architecture", engines=["arxiv"]
```

**199it 行业数据搜索：**
```
用户：「搜索 2024 年电商行业数据报告」
→ 调用 mcp__kepler__web_search，query="2024 电商行业报告", engines=["199it"]
```

**东方财富财经搜索：**
```
用户：「搜索贵州茅台股票最新资讯」
→ 调用 mcp__kepler__web_search，query="贵州茅台", engines=["eastmoney"]
```

**智联招聘职位搜索：**
```
用户：「搜索北京 Java 开发工程师职位」
→ 调用 mcp__kepler__web_search，query="Java 开发工程师 北京", engines=["zhaopin"]
```

**前程无忧职位搜索：**
```
用户：「搜索上海产品经理职位」
→ 调用 mcp__kepler__web_search，query="产品经理 上海", engines=["51job"]
```

### 模式二：多引擎搜索（推荐！）

**同时使用 Bing、知乎和小红书搜索：**
```
用户：「搜索 Python 异步编程」
→ 依次执行三次搜索：
   1. 调用 mcp__kepler__web_search，query="Python 异步编程", engines=["bing"]
   2. 调用 mcp__kepler__web_search，query="Python 异步编程", engines=["zhihu"]
   3. 调用 mcp__kepler__web_search，query="Python 异步编程", engines=["xhs"]
→ 自动返回来自 Bing、知乎和小红书的综合结果

注意：多引擎搜索只能依次执行，不支持 engines=["bing", "zhihu", "xhs"] 这种多引擎同时调用的模式
```

**学术调研（arXiv + Bing）：**
```
用户：「调研大语言模型最新进展」
→ 依次执行：
   1. mcp__kepler__web_search，query="large language models", engines=["arxiv"]
   2. mcp__kepler__web_search，query="大语言模型 最新进展", engines=["bing"]
   3. mcp__kepler__web_search，query="大语言模型 知乎", engines=["zhihu"]
→ 综合学术论文、最新资讯和社区讨论
```

**技术调研（GitHub + Bing + 知乎）：**
```
用户：「调研 React 19 新特性」
→ 依次执行：
   1. mcp__kepler__web_search，query="React 19", engines=["github"]
   2. mcp__kepler__web_search，query="React 19 new features", engines=["bing"]
   3. mcp__kepler__web_search，query="React 19 新特性", engines=["zhihu"]
→ 综合开源项目、技术文档和社区讨论
```

**行业调研（199it + Bing + 知乎）：**
```
用户：「调研 2024 年 AI 行业发展」
→ 依次执行：
   1. mcp__kepler__web_search，query="2024 AI industry report", engines=["199it"]
   2. mcp__kepler__web_search，query="AI 行业 2024", engines=["bing"]
   3. mcp__kepler__web_search，query="2024 AI 发展 知乎", engines=["zhihu"]
→ 综合行业数据、最新资讯和社区观点
```

**财经调研（Eastmoney + Bing）：**
```
用户：「调研新能源汽车行业」
→ 依次执行：
   1. mcp__kepler__web_search，query="新能源汽车", engines=["eastmoney"]
   2. mcp__kepler__web_search，query="新能源汽车行业", engines=["bing"]
   3. mcp__kepler__web_search，query="新能源汽车 投资", engines=["zhihu"]
→ 综合财经资讯、行业动态和投资观点
```

**职位调研（Zhaopin + 51job + Bing）：**
```
用户：「调研 AI 算法工程师招聘市场」
→ 依次执行：
   1. mcp__kepler__web_search，query="AI 算法工程师", engines=["zhaopin"]
   2. mcp__kepler__web_search，query="AI 算法工程师", engines=["51job"]
   3. mcp__kepler__web_search，query="AI 算法工程师 薪资", engines=["bing"]
   4. mcp__kepler__web_search，query="AI 算法工程师 面试", engines=["zhihu"]
→ 综合招聘平台职位信息和市场趋势
```

### 模式三：多源并行搜索

```
用户：「多源搜索 Python 异步编程」
→ 并行执行：
   1. mcp__kepler__web_search: "Python 异步编程 best practices", engines=["bing"]
   2. mcp__kepler__web_search: "Python 异步编程 知乎", engines=["zhihu"]
   3. mcp__kepler__web_search: "Python 异步编程 小红书", engines=["xhs"]
→ 综合结果去重并呈现
```

### 模式四：搜索+深度阅读

```
用户：「调研 Python asyncio 的性能优势」
→ 步骤：
   1. mcp__kepler__web_search 搜索 "Python asyncio performance"
   2. mcp__kepler__web_search 搜索 "asyncio 性能 知乎"
   3. 筛选 3-5 个高质量链接（优先知乎、官方文档、知名博客）
   4. mcp__kepler__web_reader 读取重点页面详细内容
   5. 综合分析输出结构化报告
```

### 模式五：知乎/小红书内容精读

**知乎文章精读：**
```
用户：「帮我读一下这个知乎回答 https://zhuanlan.zhihu.com/...」
→ 直接调用 mcp__kepler__web_reader，format="markdown"
→ 提取文章核心观点并总结
```

**小红书笔记精读：**
```
用户：「帮我读一下这篇小红书笔记 https://www.xiaohongshu.com/...」
→ 直接调用 mcp__kepler__web_reader，format="markdown"
→ 提取笔记核心内容和种草要点
```

## 输出格式规范

### 单源搜索结果

```
## 搜索结果：[关键词]

### 1. [标题](链接)
📰 来源：网站名 | 日期
📝 摘要：内容摘要...

### 2. [标题](链接)
...

---
🔍 数据源：Bing
```

### 多源搜索结果

```
## 多源搜索结果：[关键词]

### 🔵 Bing 搜索结果

#### 1. [标题](链接)
📰 来源：XXX | 日期
📝 摘要：...

### 🟠 知乎相关结果

#### 1. [标题](链接)
📰 来源：知乎 | 日期
📝 摘要：...

### 🔴 小红书相关结果

#### 1. [标题](链接)
📕 来源：小红书 | 日期
📝 摘要：...

---
🔍 多源搜索整合：Bing + 知乎 + 小红书
```

### 知乎文章精读

```
## 📄 知乎文章精读

**🔗 来源**：[知乎专栏/回答](URL)
**✍️ 作者**：XXX
**📅 发布日期**：XXXX-XX-XX
**💬 互动数据**：XXX 赞同 · XX 评论（如有）

### 💡 核心观点
一句话总结文章核心内容。

### 📝 详细内容
正文内容...

### 🔖 精彩评论（如有）
- 评论一...
- 评论二...

---
📚 来源：知乎 · Kepler Web Reader
```

### 小红书笔记精读

```
## 📕 小红书笔记精读

**🔗 来源**：[小红书笔记](URL)
**✍️ 作者**：XXX
**📅 发布日期**：XXXX-XX-XX
**❤️ 互动数据**：XXX 点赞 · XX 收藏 · XX 评论（如有）

### 💡 核心内容
一句话总结笔记核心内容。

### 📝 详细内容
笔记正文...

### 🏷️ 标签/话题
- #标签一
- #标签二

---
📚 来源：小红书 · Kepler Web Reader
```

### 综合调研报告

```
## 🔍 多源调研报告：[主题]

### 📊 数据来源概览
- Bing 搜索结果：X 条
- 知乎相关内容：X 条
- 小红书相关内容：X 条
- 其他来源：X 条

### 🎯 核心发现
1. **发现一**：[内容] [来源: 网站名]
2. **发现二**：[内容] [来源: 知乎]
3. **发现三**：[内容] [来源: 网站名]

### 📚 详细分析

#### 技术博客/文档观点
...

#### 知乎社区讨论
...

### 🔗 参考来源
- [标题](链接) — Bing/Blog
- [标题](链接) — 知乎
- ...

---
🔍 多源搜索整合 | 时间：YYYY-MM-DD HH:MM
```

## 使用技巧

### Engines 参数用法（重点）

**支持的数据源（每次调用只能指定一个）：**

| 引擎 | 标识 | 适用场景 |
|------|------|----------|
| Bing | `"bing"` | 通用搜索、英文内容 |
| Baidu | `"baidu"` | 通用搜索、中文内容 |
| 知乎 | `"zhihu"` | 中文知识问答 |
| 小红书 | `"xhs"` | 生活方式、种草 |
| GitHub | `"github"` | 开源代码、项目 |
| arXiv | `"arxiv"` | 学术论文、研究 |
| 199it | `"199it"` | 行业数据、报告 |
| 东方财富 | `"eastmoney"` | 财经资讯、股票 |
| 智联招聘 | `"zhaopin"` | 招聘职位、人才 |
| 前程无忧 | `"51job"` | 招聘职位、人才 |

**多源搜索策略（依次执行）：**
```yaml
# 通用搜索
engines: ["bing"]
engines: ["baidu"]

# 社交媒体
engines: ["zhihu"]
engines: ["xhs"]

# 开发/学术
engines: ["github"]
engines: ["arxiv"]

# 数据/财经
engines: ["199it"]
engines: ["eastmoney"]
```

**推荐策略：**
- 通用信息 → `engines: ["bing"]` 或 `engines: ["baidu"]`
- 中文知识/经验 → `engines: ["zhihu"]`
- 生活方式/消费决策/攻略 → `engines: ["xhs"]`
- 开源代码/项目 → `engines: ["github"]`
- 学术论文/研究 → `engines: ["arxiv"]`
- 行业数据/报告 → `engines: ["199it"]`
- 财经资讯/股票 → `engines: ["eastmoney"]`
- 智联招聘职位 → `engines: ["zhaopin"]`
- 前程无忧职位 → `engines: ["51job"]`
- 综合调研 → 依次调用多个引擎，然后合并结果

### 搜索词优化

**GitHub 定向搜索：**
```yaml
query: "react state management"
engines: ["github"]
# 返回 React 状态管理相关的开源项目和代码仓库
```

**arXiv 定向搜索：**
```yaml
query: "attention mechanism transformer"
engines: ["arxiv"]
# 返回 transformer attention mechanism 相关的学术论文
```

**199it 定向搜索：**
```yaml
query: "2024 电商行业报告"
engines: ["199it"]
# 返回 2024 年电商行业相关的数据报告
```

**东方财富定向搜索：**
```yaml
query: "贵州茅台"
engines: ["eastmoney"]
# 返回贵州茅台股票相关的财经资讯和行情
```

**知乎定向搜索（方式一：使用 engines 参数）：**
```yaml
query: "Python 异步编程"
engines: ["zhihu"]
```

**小红书定向搜索（方式一：使用 engines 参数）：**
```yaml
query: "上海探店 咖啡"
engines: ["xhs"]
```

**知乎/小红书定向搜索（方式二：使用关键词）：**
- `site:zhihu.com 关键词` — 只搜索知乎内容
- `site:xiaohongshu.com 关键词` — 只搜索小红书内容
- `关键词 知乎` — 获取知乎相关结果
- `关键词 小红书` — 获取小红书相关结果

**Bing 高级搜索：**
- `"精确短语"` — 精确匹配
- `关键词 filetype:pdf` — 搜索 PDF 文档
- `关键词 -排除词` — 排除特定词汇

### 多源并行策略

对于重要调研任务，建议依次搜索：
1. 英文关键词 → Bing (`engines: ["bing"]`)，获取英文资源
2. 中文关键词 → Baidu (`engines: ["baidu"]`)，获取中文通用内容
3. 中文知识 → 知乎 (`engines: ["zhihu"]`)，获取中文社区讨论
4. 生活方式/消费 → 小红书 (`engines: ["xhs"]`)，获取真实体验分享
5. 开源项目 → GitHub (`engines: ["github"]`)，获取代码和文档
6. 学术论文 → arXiv (`engines: ["arxiv"]`)，获取研究论文
7. 行业数据 → 199it (`engines: ["199it"]`)，获取数据报告
8. 财经资讯 → 东方财富 (`engines: ["eastmoney"]`)，获取股票财经
9. 智联招聘 → 职位 (`engines: ["zhaopin"]`)，获取招聘信息
10. 前程无忧 → 职位 (`engines: ["51job"]`)，获取招聘信息
11. 综合对比 → 合并多源结果

### GitHub 内容获取技巧

1. **项目仓库**：URL 通常为 `github.com/owner/repo`
2. **代码文件**：`github.com/owner/repo/blob/main/file.js`
3. **Issues**：`github.com/owner/repo/issues`
4. **搜索技巧**：
   - 使用英文关键词效果更佳
   - 可以加上 `stars:>100` 筛选热门项目
   - `language:python` 筛选特定语言

GitHub 内容使用 `mcp__kepler__web_reader` 时：
- 默认提取 README 内容
- 代码文件会保留格式
- Issue 和 PR 页面会提取讨论内容

### arXiv 内容获取技巧

1. **论文页面**：URL 通常为 `arxiv.org/abs/xxxx.xxxxx`
2. **PDF 下载**：`arxiv.org/pdf/xxxx.xxxxx`
3. **搜索技巧**：
   - 使用英文关键词
   - 可以加上分类如 `cs.AI`, `cs.CL`, `cs.LG`

arXiv 内容使用 `mcp__kepler__web_reader` 时：
- 自动提取论文标题、作者、摘要
- 保留数学公式格式
- 支持获取 PDF 内容

### 199it 内容获取技巧

1. **报告页面**：URL 通常为 `199it.com/archives/xxxxxx`
2. **分类页面**：`199it.com/category/xxxx`
3. **搜索技巧**：
   - 使用中文关键词
   - 可以加上年份筛选

199it 内容使用 `mcp__kepler__web_reader` 时：
- 自动提取报告标题和摘要
- 保留数据表格
- 部分报告可能需要登录查看完整内容

### 东方财富内容获取技巧

1. **个股页面**：URL 通常为 `quote.eastmoney.com/symbol`
2. **资讯页面**：`finance.eastmoney.com/...`
3. **研报页面**：`report.eastmoney.com/...`

东方财富内容使用 `mcp__kepler__web_reader` 时：
- 自动提取股票行情数据
- 保留财经新闻内容
- 研报会提取核心观点

### 智联招聘内容获取技巧

1. **职位详情页**：URL 通常为 `jobs.zhaopin.com/...` 或 `www.zhaopin.com/jobs/...`
2. **搜索结果页**：`sou.zhaopin.com/?...`
3. **公司主页**：`company.zhaopin.com/...`

智联招聘搜索优化：
- **职位名称**：使用精准职位名，如 "Java 后端工程师"
- **地点筛选**：城市名 + 职位，如 "上海 Python 开发"
- **经验要求**：可加上 "3-5 年"、"应届生"
- **行业筛选**：如 "互联网"、"金融"

智联招聘内容使用 `mcp__kepler__web_reader` 时：
- 自动提取职位描述和要求
- 保留薪资范围和工作地点
- 提取公司信息和福利待遇

### 前程无忧内容获取技巧

1. **职位详情页**：URL 通常为 `jobs.51job.com/...`
2. **搜索结果页**：`search.51job.com/jobsearch/...`
3. **公司主页**：`company.51job.com/...`

前程无忧搜索优化：
- **职位名称**：使用标准职位名称，如 "产品经理"
- **地点筛选**：城市 + 区域，如 "北京 朝阳区"
- **薪资范围**：可搜索 "15-25K"、"年薪"
- **公司规模**：如 "互联网大厂"、"外企"

前程无忧内容使用 `mcp__kepler__web_reader` 时：
- 自动提取岗位职责和任职要求
- 保留公司介绍和联系方式
- 提取薪资福利和晋升空间

### 知乎内容获取技巧

1. **专栏文章**：URL 通常为 `zhuanlan.zhihu.com/p/xxxx`
2. **问题回答**：URL 通常为 `zhihu.com/question/xxxx`
3. **用户主页**：`zhihu.com/people/username`

知乎内容使用 `mcp__kepler__web_reader` 时：
- 默认提取文章正文
- 自动过滤广告和推荐内容
- 保留原文格式和结构

### 小红书内容获取技巧

1. **笔记链接**：URL 通常为 `www.xiaohongshu.com/explore/xxxx` 或 `xhslink.com/xxxx`
2. **用户主页**：`www.xiaohongshu.com/user/profile/xxxx`
3. **话题页面**：`www.xiaohongshu.com/search_result?keyword=xxxx`

小红书内容使用 `mcp__kepler__web_reader` 时：
- 自动提取笔记正文和图片说明
- 保留标签和话题信息
- 过滤广告和推荐内容

## 工具调用示例

### Bing 搜索（默认）

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">Python asyncio 性能优化</arg>
<arg name="engines">["bing"]</arg>
<arg name="max_results">10</arg>
</invoke>
</function_calls>

### 知乎搜索（使用 engines 参数）

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">Python asyncio 性能优化</arg>
<arg name="engines">["zhihu"]</arg>
<arg name="max_results">10</arg>
</invoke>
</function_calls>

### 小红书搜索（使用 engines 参数）

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">上海咖啡探店</arg>
<arg name="engines">["xhs"]</arg>
<arg name="max_results">10</arg>
</invoke>
</function_calls>

### Baidu 搜索

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">Python 异步编程 最佳实践</arg>
<arg name="engines">["baidu"]</arg>
<arg name="max_results">10</arg>
</invoke>
</function_calls>

### GitHub 搜索

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">react state management</arg>
<arg name="engines">["github"]</arg>
<arg name="max_results">10</arg>
</invoke>
</function_calls>

### arXiv 学术论文搜索

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">transformer attention mechanism</arg>
<arg name="engines">["arxiv"]</arg>
<arg name="max_results">10</arg>
</invoke>
</function_calls>

### 199it 行业数据搜索

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">2024 电商行业报告</arg>
<arg name="engines">["199it"]</arg>
<arg name="max_results">10</arg>
</invoke>
</function_calls>

### 东方财富财经搜索

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">贵州茅台</arg>
<arg name="engines">["eastmoney"]</arg>
<arg name="max_results">10</arg>
</invoke>
</function_calls>

### 智联招聘职位搜索

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">Java 开发工程师 上海</arg>
<arg name="engines">["zhaopin"]</arg>
<arg name="max_results">10</arg>
</invoke>
</function_calls>

### 前程无忧职位搜索

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">产品经理 北京</arg>
<arg name="engines">["51job"]</arg>
<arg name="max_results">10</arg>
</invoke>
</function_calls>

### 多引擎搜索（Bing + 知乎 + 小红书）

**注意：需要依次执行三次搜索，不支持同时传递多个引擎**

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">Claude Code MCP skill</arg>
<arg name="engines">["bing"]</arg>
<arg name="max_results">10</arg>
</invoke>
<invoke name="mcp__kepler__web_search">
<arg name="query">Claude Code MCP skill</arg>
<arg name="engines">["zhihu"]</arg>
<arg name="max_results">10</arg>
</invoke>
<invoke name="mcp__kepler__web_search">
<arg name="query">Claude Code MCP</arg>
<arg name="engines">["xhs"]</arg>
<arg name="max_results">10</arg>
</invoke>
</function_calls>

### 传统多源并行搜索

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">Claude Code MCP skill</arg>
<arg name="max_results">10</arg>
</invoke>
<invoke name="mcp__kepler__web_search">
<arg name="query">Claude Code MCP 知乎</arg>
<arg name="max_results">10</arg>
</invoke>
</function_calls>

### 读取知乎文章

<function_calls>
<invoke name="mcp__kepler__web_reader">
<arg name="url">https://zhuanlan.zhihu.com/p/xxxxx</arg>
<arg name="format">text</arg>
<arg name="extract_article">true</arg>
</invoke>
</function_calls>

### 读取小红书笔记

<function_calls>
<invoke name="mcp__kepler__web_reader">
<arg name="url">https://www.xiaohongshu.com/explore/xxxxx</arg>
<arg name="format">text</arg>
<arg name="extract_article">true</arg>
</invoke>
</function_calls>

### 读取 GitHub 项目

<function_calls>
<invoke name="mcp__kepler__web_reader">
<arg name="url">https://github.com/facebook/react</arg>
<arg name="format">markdown</arg>
<arg name="extract_article">true</arg>
</invoke>
</function_calls>

### 读取 arXiv 论文

<function_calls>
<invoke name="mcp__kepler__web_reader">
<arg name="url">https://arxiv.org/abs/1706.03762</arg>
<arg name="format">markdown</arg>
<arg name="extract_article">true</arg>
</invoke>
</function_calls>

### 搜索并自动获取内容（fetch_content）

<function_calls>
<invoke name="mcp__kepler__web_search">
<arg name="query">Claude Code MCP skill</arg>
<arg name="engines">["bing"]</arg>
<arg name="max_results">10</arg>
<arg name="fetch_content">true</arg>
<arg name="max_fetch">3</arg>
</invoke>
</function_calls>

## 故障处理

### 搜索无结果
- 尝试简化关键词
- 中英文关键词互换
- 使用更通用的词汇

### 知乎内容读取失败
- 检查 URL 是否完整
- 部分知乎页面需要登录，可能无法读取完整内容
- 尝试切换 format 参数（markdown/text/html）

### 内容不完整
- 知乎回答过长时可能只提取核心内容
- 需要详细内容可指定具体段落读取

## 限制说明

1. **搜索范围**：通过各引擎原生搜索获取结果
2. **访问限制**：
   - 部分网站有反爬机制，可能需要重试或者无法读取
   - 无法读取需要登录的私有内容
3. **内容安全**：遵守内容安全政策

## 工作区规则

临时搜索结果直接输出到对话中。如需保存调研报告，使用 `/tmp/` 目录。

---

🔍 **Kepler Agent Search** — 整合多源信息，一站式多源搜索解决方案。
