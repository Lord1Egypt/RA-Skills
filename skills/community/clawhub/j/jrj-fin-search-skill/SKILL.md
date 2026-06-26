---
name: jrj-fin-search-skill
description: >-
  A股中文财经资讯和研报摘要搜索，支持按关键词、来源、时间范围查询新闻资讯和研究报告。
  用于获取权威来源的市场动态、公司新闻、行业研报等信息。避免AI在搜索金融场景信息时，参考到非权威、过时的信息。

  <example>User: "搜索贵州茅台最近3天的新闻" Assistant: 使用 news.js search 命令搜索资讯</example>
  <example>User: "查找人工智能相关的研报" Assistant: 使用 news.js reports 命令搜索研报</example>
metadata:
  {"openclaw": {"requires": {"env": ["JRJ_API_KEY"]}, "primaryEnv": "JRJ_API_KEY", "homepage": "https://ai.jrj.com.cn/claw"}}
---

# 金融界A股资讯与研报数据技能（JRJ News Skill）

搜索A股相关的新闻资讯和研究报告摘要。

# 使用场景
1. **个股信息跟踪**
   查询单只股票的公告、重大事件、经营动态、业绩发布等相关新闻，确保AI回答公司信息时**来源权威、内容最新**。

2. **行业动态监控**
   按行业关键词（如新能源、半导体、人工智能、银行、医药）搜索资讯与研报，用于**行业趋势判断、政策解读、景气度分析**。

3. **热点事件与政策复盘**
   针对市场突发新闻、监管政策、宏观数据、重要会议等，快速检索权威媒体报道，用于**事件影响分析与信息核实**。

4. **研报摘要快速查阅**
   获取券商研究报告核心观点、盈利预测、投资评级，辅助AI进行**基本面分析、行业对比、逻辑梳理**。

5. **AI大模型信息校准**
   在回答财经/股票相关问题前，先通过本Skill检索最新资讯与研报，**避免AI使用过时、错误、非权威信息**，提升回答可信度。

6. **投资辅助决策**
   结合新闻舆情与研报观点，为用户提供**客观信息汇总**，辅助判断市场情绪、公司基本面变化与行业风向。

7. **风险提示与信息核实**
   针对市场传闻、利空/利好消息，通过权威来源快速验证真伪，降低**虚假信息误导风险**。

8. **每日/每周财经复盘**
   按时间范围批量获取市场要闻与核心研报，用于生成**复盘总结、投资笔记、策略依据**。

---

## 环境配置

```bash
# 必须设置以下环境变量
export JRJ_API_KEY=sk_live_xxx   # API Key
```

## 快速开始

### 搜索资讯

```bash
# 基本用法
node scripts/news.js search \
  --keywords="贵州茅台" \
  --start="2026-03-20 00:00:00"

# 指定时间范围
node scripts/news.js search \
  --keywords="贵州茅台 茅台" \
  --start="2026-03-20 00:00:00" \
  --end="2026-03-23 23:59:59"

# 指定来源
node scripts/news.js search \
  --keywords="人工智能" \
  --start="2026-03-01 00:00:00" \
  --source="财联社 证券时报"
```

### 搜索研报

```bash
# 基本用法
node scripts/news.js reports \
  --keywords="人工智能 大模型" \
  --start="2026-03-01 00:00:00"

# 指定返回数量
node scripts/news.js reports \
  --keywords="人工智能 大模型" \
  --start="2026-03-01 00:00:00" \
  --limit=50
```

## 命令详解

### search - 资讯搜索

搜索新闻资讯，支持按关键词、来源、时间范围筛选。

```bash
node scripts/news.js search --keywords=<关键词> --start=<开始时间> [选项]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--keywords` | 是 | 搜索关键词，多个以空格分隔 |
| `--start` | 是 | 开始时间，格式：YYYY-MM-DD HH:mm:ss |
| `--end` | 否 | 结束时间，格式：YYYY-MM-DD HH:mm:ss |
| `--source` | 否 | 资讯来源，多个以空格分隔 |
| `--limit` | 否 | 返回数量，默认 20 |
| `--format` | 否 | 输出格式：json(默认)/markdown |

**示例**：

```bash
# 搜索贵州茅台的新闻
node scripts/news.js search \
  --keywords="贵州茅台" \
  --start="2026-03-20 00:00:00"

# 搜索贵州茅台近3天的新闻
node scripts/news.js search \
  --keywords="贵州茅台" \
  --start="2026-03-20 00:00:00" \
  --end="2026-03-23 23:59:59"

# 只看财联社和证券时报的报道
node scripts/news.js search \
  --keywords="贵州茅台" \
  --start="2026-03-20 00:00:00" \
  --end="2026-03-23 23:59:59" \
  --source="财联社 证券时报"

# 输出 Markdown 格式
node scripts/news.js search \
  --keywords="贵州茅台" \
  --start="2026-03-20 00:00:00" \
  --end="2026-03-23 23:59:59" \
  --format=markdown
```

### reports - 研报摘要搜索

搜索研究报告，支持按摘要关键词和发布日期筛选。

```bash
node scripts/news.js reports --keywords=<关键词> --start=<开始时间> [选项]
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--keywords` | 是 | 摘要关键词，多个以空格分隔 |
| `--start` | 是 | 发布日期起始时间，格式：YYYY-MM-DD HH:mm:ss |
| `--limit` | 否 | 返回数量，默认 20 |
| `--format` | 否 | 输出格式：json(默认)/markdown |

**示例**：

```bash
# 搜索人工智能相关研报
node scripts/news.js reports \
  --keywords="人工智能 大模型" \
  --start="2026-03-01 00:00:00"

# 指定返回数量
node scripts/news.js reports \
  --keywords="人工智能 大模型" \
  --start="2026-03-01 00:00:00"

# 搜索某公司的研报
node scripts/news.js reports \
  --keywords="招商银行 银行业" \
  --start="2026-03-01 00:00:00"

# 输出 Markdown 格式
node scripts/news.js reports \
  --keywords="新能源" \
  --start="2026-03-01 00:00:00" \
  --format=markdown
```

### 关于返回数量

当请求的数据量较大时，API 可能无法一次返回全部结果。此时响应会包含 `truncated: true` 标记，脚本会提示：

- 资讯搜索："可能有更多资讯未返回"
- 研报搜索："可能有更多研报未返回"

如遇此情况，建议缩小时间范围或调整 `--limit` 值。

## 输出格式

### JSON 格式（默认）

**资讯搜索**：
```json
{
  "total": 15,
  "items": [
    {
      "title": "贵州茅台发布年度业绩预告",
      "makeDate": "2026-03-22 10:30:00",
      "source": "财联社",
      "url": "https://...",
      "summary": "..."
    }
  ]
}
```

**研报搜索**：
```json
{
  "total": 8,
  "items": [
    {
      "title": "人工智能行业深度报告",
      "orgName": "中信证券",
      "declareDate": "2026-03-20 00:00:00",
      "abstract": "..."
    }
  ]
}
```

### Markdown 格式

```bash
node scripts/news.js search --keywords="..." --format=markdown
```

输出：
```markdown
## 资讯搜索结果

共找到 15 条相关资讯

### 1. 贵州茅台发布年度业绩预告
- 时间：2026-03-22 10:30:00
- 来源：财联社
- 链接：https://...

> 摘要内容...
```

## 资讯来源

支持的资讯来源包括：

| 来源 | 说明 |
|------|------|
| 财联社 | 实时财经快讯 |
| 金十数据 | 金融市场快讯 |
| 证券时报 | 官方媒体 |
| 中国证券报 | 官方媒体 |
| 上海证券报 | 官方媒体 |
| 证券日报 | 官方媒体 |

可以组合多个来源：
```bash
--source="财联社 证券时报 中国证券报"
```

## API 接口

### 资讯搜索

```
POST /v1/news/search
```

**请求参数**：
```json
{
  "keywords": "贵州茅台 茅台",
  "makeDateStart": "2026-03-20 00:00:00",
  "makeDateEnd": "2026-03-23 23:59:59",
  "source": "财联社 证券时报",
  "limit": 20
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "count": 15,
    "items": [
      {
        "title": "贵州茅台发布年度业绩预告",
        "makeDate": "2026-03-22 10:30:00",
        "source": "财联社",
        "url": "https://...",
        "summary": "..."
      }
    ],
    "truncated": true
  }
}
```

> **注意**：当 `truncated: true` 时，表示可能有更多数据未返回。

### 研报搜索

```
POST /v1/news/reports
```

**请求参数**：
```json
{
  "keywords": "人工智能 大模型",
  "declareDateStart": "2026-03-01 00:00:00",
  "limit": 20
}
```

**响应示例**：
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "count": 8,
    "items": [
      {
        "declareDate": "2026-03-20 00:00:00",
        "orgName": "中信证券",
        "title": "人工智能行业深度报告",
        "abstract": "..."
      }
    ],
    "truncated": true
  }
}
```

> **注意**：当 `truncated: true` 时，表示可能有更多数据未返回。

详细 API 文档见 [references/api-reference.md](references/api-reference.md)

## 常见用例

### 1. 追踪公司动态

```bash
# 搜索特定公司近期新闻
node scripts/news.js search \
  --keywords="招商银行" \
  --start="2026-03-18 00:00:00" \
  --end="2026-03-23 23:59:59" \
  --format=markdown
```

### 2. 行业研究

```bash
# 搜索行业研报
node scripts/news.js reports \
  --keywords="新能源汽车 锂电池" \
  --start="2026-03-01 00:00:00" \
  --format=markdown
```

### 3. 热点事件追踪

```bash
# 搜索热点事件相关新闻
node scripts/news.js search \
  --keywords="ChatGPT 人工智能" \
  --start="2026-03-01 00:00:00" \
  --end="2026-03-23 23:59:59" \
  --source="财联社 金十数据"
```

### 4. 官方媒体报道

```bash
# 只看官方媒体的报道
node scripts/news.js search \
  --keywords="央行 货币政策" \
  --start="2026-03-01 00:00:00" \
  --end="2026-03-23 23:59:59" \
  --source="证券时报 中国证券报 上海证券报"
```

## 错误处理

| 错误码 | 说明 |
|--------|------|
| 40001 | 参数错误（如时间格式不正确） |
| 40101 | API Key 无效，请前往金融界App获取最新API Key |
| 42901 | 超出请求限制，请稍后再试 |
| 42902 | 超出每日配额，请前往金融界App获取更多每日配额 |

## 参考文档

- [API 接口文档](references/api-reference.md)

---

## 免责声明

1. **信息仅供参考**：本工具提供的资讯和研报搜索结果仅供学习和研究使用，不构成任何投资建议。
2. **内容来源第三方**：资讯和研报内容来源于第三方媒体和研究机构，我们不对其准确性、完整性或时效性负责。
3. **投资风险**：股票投资有风险，投资者应独立判断并承担投资决策的全部责任。
4. **版权声明**：资讯和研报内容的版权归原作者和发布机构所有，仅供个人学习研究使用。
5. **使用限制**：本工具仅限个人学习研究使用，禁止用于商业用途或非法活动。
