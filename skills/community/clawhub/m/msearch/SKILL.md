---
name: msearch
description: 集成16个搜索引擎（7个国内 + 9个国际），支持高级搜索操作符、时间筛选、站内搜索、隐私搜索引擎和 WolframAlpha 知识查询，无需 API 密钥。
version: 1.0.0
user-invocable: true
metadata:
  openclaw:
    emoji: 🔍
    homepage: https://clawhub.ai/sclawbot/msearch
---

# 多搜索引擎

集成 16 个搜索引擎进行网页抓取，无需 API 密钥。

## 工作流程

1. **准备阶段**：AI Agent 初始化一个空的运行时内存 Cookie 存储。Cookie 仅在搜索操作遇到访问拒绝时动态获取。

2. **语言评估**：检测搜索查询的语言属性。如果查询为中文，使用国内搜索引擎（百度、必应CN、必应INT、360、搜狗、微信、神马）。如果查询为非中文，使用国际搜索引擎（Google、Google HK、DuckDuckGo、Yahoo、Startpage、Brave、Ecosia、Qwant、WolframAlpha）。根据查询的相关性和可用性选择合适的引擎。

3. **受控搜索**：使用 web_fetch 执行搜索请求并进行速率限制：
   - 在请求之间添加 1-2 秒延迟以尊重服务器负载
   - 每组 3-4 个引擎批量请求，批次之间顺序执行
   - 包含标准浏览器请求头，标识为合法用户代理
   - 如果访问被拒绝（403/429），获取引擎首页以获取新的会话 Cookie

4. **Cookie 管理**：
   - Cookie 仅在运行时存储在内存中
   - Cookie 在搜索请求失败时按需获取
   - 不从 config.json 或任何文件读取或写入 Cookie
   - 搜索会话完成后立即清除 Cookie
   - 仅捕获搜索引擎域名的会话 Cookie

5. **重试机制**：如果搜索因 Cookie/会话问题失败，在 2 秒延迟后使用新获取的 Cookie 重试一次。

6. **结果聚合**：整合来自搜索引擎的成功结果，整理并汇总，输出核心搜索报告。

## 搜索引擎

### 国内引擎（7个）
- **百度**: `https://www.baidu.com/s?wd={keyword}`
- **必应 CN**: `https://cn.bing.com/search?q={keyword}&ensearch=0`
- **必应 INT**: `https://cn.bing.com/search?q={keyword}&ensearch=1`
- **360**: `https://www.so.com/s?q={keyword}`
- **搜狗**: `https://sogou.com/web?query={keyword}`
- **微信**: `https://wx.sogou.com/weixin?type=2&query={keyword}`
- **神马**: `https://m.sm.cn/s?q={keyword}`

### 国际引擎（9个）
- **Google**: `https://www.google.com/search?q={keyword}`
- **Google HK**: `https://www.google.com.hk/search?q={keyword}`
- **DuckDuckGo**: `https://duckduckgo.com/html/?q={keyword}`
- **Yahoo**: `https://search.yahoo.com/search?p={keyword}`
- **Startpage**: `https://www.startpage.com/sp/search?query={keyword}`
- **Brave**: `https://search.brave.com/search?q={keyword}`
- **Ecosia**: `https://www.ecosia.org/search?q={keyword}`
- **Qwant**: `https://www.qwant.com/?q={keyword}`
- **WolframAlpha**: `https://www.wolframalpha.com/input?i={keyword}`

## 快速示例

```javascript
// 基础搜索
web_fetch({"url": "https://www.google.com/search?q=python教程"})

// 站内搜索
web_fetch({"url": "https://www.google.com/search?q=site:github.com+react"})

// 文件类型搜索
web_fetch({"url": "https://www.google.com/search?q=机器学习+filetype:pdf"})

// 时间筛选（最近一周）
web_fetch({"url": "https://www.google.com/search?q=AI新闻&tbs=qdr:w"})

// 隐私搜索
web_fetch({"url": "https://duckduckgo.com/html/?q=隐私工具"})

// DuckDuckGo Bangs 快捷跳转
web_fetch({"url": "https://duckduckgo.com/html/?q=!gh+tensorflow"})

// 知识计算查询
web_fetch({"url": "https://www.wolframalpha.com/input?i=100+USD+to+CNY"})
```

## 高级搜索操作符

| 操作符 | 示例 | 描述 |
|----------|---------|-------------|
| `site:` | `site:github.com python` | 在指定网站内搜索 |
| `filetype:` | `filetype:pdf 报告` | 指定文件类型 |
| `""` | `"机器学习"` | 精确匹配 |
| `-` | `python -蛇` | 排除关键词 |
| `OR` | `猫 OR 狗` | 任意关键词 |

## 时间筛选参数

| 参数 | 描述 |
|-----------|-------------|
| `tbs=qdr:h` | 最近1小时 |
| `tbs=qdr:d` | 最近1天 |
| `tbs=qdr:w` | 最近1周 |
| `tbs=qdr:m` | 最近1月 |
| `tbs=qdr:y` | 最近1年 |

## 隐私搜索引擎

- **DuckDuckGo**: 不追踪用户
- **Startpage**: Google 搜索结果 + 隐私保护
- **Brave**: 独立索引
- **Qwant**: 符合欧盟 GDPR 规范

## Bangs 快捷命令（DuckDuckGo）

| Bang | 跳转目标 |
|------|-------------|
| `!g` | Google |
| `!gh` | GitHub |
| `!so` | Stack Overflow |
| `!w` | Wikipedia |
| `!yt` | YouTube |

## WolframAlpha 查询类型

- 数学计算: `integrate x^2 dx`
- 单位换算: `100 USD to CNY`
- 股票数据: `AAPL stock`
- 天气查询: `weather in Beijing`

## 参考文档

- `references/advanced-search.md` - 国内搜索引擎深度搜索指南
- `references/international-search.md` - 国际搜索引擎深度搜索指南

## 许可证

MIT

## 安全与隐私声明

### Cookie 处理
- **用途**：Cookie 仅在访问被拒绝（403/429 错误）时用于维护搜索会话状态
- **存储**：Cookie 严格保存在运行时内存中——绝不持久化到磁盘或配置文件
- **获取方式**：仅在搜索请求失败时从搜索引擎首页按需获取 Cookie
- **范围**：仅捕获来自特定搜索引擎域名的会话 Cookie
- **生命周期**：搜索会话完成后立即清除 Cookie
- **无预配置**：启动时不从 config.json 或任何外部文件加载 Cookie
- **无 API 密钥**：本工具使用标准网页搜索 URL，无需认证

### 爬取伦理
- **速率限制**：请求之间保持合理延迟（建议 1-2 秒）
- **遵守 robots.txt**：尊重搜索引擎爬取策略
- **服务条款**：用户有责任遵守各搜索引擎的服务条款
- **用途定位**：面向合法的搜索聚合场景，非大规模数据抓取

### 数据处理
- **无个人数据**：工具不收集或传输用户个人信息
- **本地执行**：所有操作均在本地运行，无外部数据传输
- **会话隔离**：Cookie 为会话级别，使用后立即清除
