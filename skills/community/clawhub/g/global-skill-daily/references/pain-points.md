# ClawHub 痛点库

> 用于将通用推荐转化为"你的私人推荐"的核心分类

## 7 大痛点场景

每个场景包含：**场景名** + **关键词列表** + **典型 Skill 例子** + **下一步行动模板**

---

### 1. 🤖 自动化办公 (Office Automation)

**关键词**：
```
gmail, calendar, slack, trello, notion, sheets, drive, docs,
gmail-api, calendar-api, trello-api, notion-api, sheets-api,
office, workspace, gog, himalaya, contact, meeting, mail
```

**典型 Skill**：
- `Gog` - Google Workspace 全套
- `Slack` - Slack 集成
- `Trello` - 看板管理
- `Notion` - 文档管理
- `Himalaya` - 邮件 CLI

**下一步行动模板**：
- 试试用 [X] 接管你的 [Gmail/Notion/Slack] 工作流
- 在 [Gmail/Notion] 中配置 [X] 自动处理 [收件箱/任务]

---

### 2. 🛠️ 开发工具 (Dev Tools)

**关键词**：
```
github, mcp, browser, code, git, test, ci, debug, lint,
api, rest, graphql, docker, build, deploy, dev, programmer,
coding, repo, pull-request, action
```

**典型 Skill**：
- `Github` - GitHub CLI 集成
- `Agent Browser` - 浏览器自动化
- `Skill Vetter` - Skill 安全审计
- `Model Usage` - 模型用量统计

**下一步行动模板**：
- 在 IDE 中安装 [X] 并配置 MCP server
- 用 [X] 自动化你的 PR/Issue 流程

---

### 3. ✍️ 内容创作 (Content Creation)

**关键词**：
```
youtube, humanizer, video, image, pdf, writing, blog, post,
medium, notion, substack, twitter, x, social, content,
creator, editor, copywriting, transcript, frame
```

**典型 Skill**：
- `YouTube Watcher` - 视频字幕
- `Humanizer` - AI 痕迹去除
- `Nano Banana Pro` - 图像生成
- `Nano Pdf` - PDF 编辑

**下一步行动模板**：
- 用 [X] 改写你最近一篇 [文章/邮件]
- 用 [X] 提取你关注的 YouTube 频道

---

### 4. 🕷️ 数据采集 (Data Scraping)

**关键词**：
```
search, scraping, apify, firecrawl, polymarket, google,
bing, duckduckgo, brave, tavily, serp, crawler, scraper,
data, extract, monitor, watch
```

**典型 Skill**：
- `Multi Search Engine` - 16 引擎搜索
- `Tavily 搜索` - Tavily API
- `Baidu web search` - 百度搜索
- `Polymarket` - 预测市场

**下一步行动模板**：
- 用 [X] 监控你的竞品 [网站/数据源]
- 用 [X] 抓取 [行业/趋势] 数据生成日报

---

### 5. 🧠 AI 增强 (AI Enhancement)

**关键词**：
```
self-improving, proactive, memory, agent, reasoning,
reflection, learning, autonomous, cron, schedule, plan,
improve, optimize, automation, hal, wal
```

**典型 Skill**：
- `Self-Improving Agent` - 自我进化
- `Proactive Agent` - 主动预判
- `Self-Improving + Proactive` - 组合
- `Ontology` - 知识图谱

**下一步行动模板**：
- 把 [X] 加入你的 Skill 库，下次任务自动调用
- 让 [X] 持续优化你的 AI 工作流

---

### 6. 🇨🇳 中文支持 (Chinese Support)

**关键词**：
```
chinese, baidu, wechat, taobao, bilibili, qq, weibo,
douyin, jd, alipay, aliyun, tencent, 中文, 百度, 微信,
淘宝, B站, 微博, 抖音, 京东
```

**典型 Skill**：
- `Baidu web search` - 百度搜索
- `Tavily 搜索` - 中文搜索
- `Multi Search Engine` - 含 7 个中文引擎

**下一步行动模板**：
- 用 [X] 处理你的中文内容创作
- 把 [X] 接入你已有的中文工作流

---

### 7. 💰 金融分析 (Financial Analysis)

**关键词**：
```
polymarket, financial, stock, trading, invest, market,
price, prediction, alpha, fund, portfolio, backtest,
report, analyst, earnings
```

**典型 Skill**：
- `Polymarket` - 预测市场
- `Financial AI Analyst` - 金融分析（出版方）

**下一步行动模板**：
- 用 [X] 跟踪你的 [持仓/竞品] 动态
- 用 [X] 监控 [市场/政策] 信号

---

## 痛点匹配算法

```python
def match_pain_points(skill, pain_points_db):
    """返回该 Skill 命中的痛点场景列表"""
    text = f"{skill['displayName']} {skill['summary']} {' '.join(skill['capabilityTags'])}".lower()
    matched = []
    for scene, config in pain_points_db.items():
        for kw in config['keywords']:
            if kw.lower() in text:
                matched.append(scene)
                break
    return matched
```

## 痛点加权评分

```python
def pain_point_weight(matched_scenes, user_priority):
    """
    user_priority: dict, {scene: weight}
    """
    score = 0
    for scene in matched_scenes:
        score += user_priority.get(scene, 1.0)
    return score
```

## 默认用户优先级

```python
DEFAULT_USER_PRIORITY = {
    "🤖 自动化办公": 1.5,
    "🛠️ 开发工具": 1.5,
    "🧠 AI 增强": 1.3,
    "✍️ 内容创作": 1.2,
    "🕷️ 数据采集": 1.2,
    "🇨🇳 中文支持": 1.0,
    "💰 金融分析": 0.8,
}
```

用户可自定义调整。

## 扩展方法

要添加新痛点场景：

1. 在 `references/pain-points.md` 添加场景定义
2. 在 `daily_recommend.py` 的 `PAIN_POINTS_DB` 中同步
3. 在简报模板中按需更新分类标题
