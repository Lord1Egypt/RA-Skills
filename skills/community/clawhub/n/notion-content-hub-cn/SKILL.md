# 飞书自媒体内容管理中枢

把飞书多维表格变成你的内容大脑：接入实时热榜生成选题、追踪发布数据、AI 月度复盘分析 —— 专为中文自媒体博主设计，无需翻墙，全程中文。

---

## 这套工具是什么

**飞书多维表格** = 你的内容数据库（可视化界面，手机电脑都能看，免费）
**本 skill** = AI 助理（生成选题、存数据、做分析）
**一稿多发助手**（配合使用）= 一个选题自动生成多平台内容版本

三者组合成完整流水线，你只需要做两件事：决策选题 + 复制内容去各平台发布。

---

## 完整工作流

```
周一：AI 拉热榜 → 生成5个选题 → 自动存飞书（10分钟）
         ↓
    你在飞书看板里选哪个做
         ↓
内容生产：告诉AI生成哪个 → 一稿多发生成各平台版本（5分钟/篇）
         ↓
    你复制粘贴到各平台发布
         ↓
发布后：说一句话录数据 → AI自动更新飞书（1分钟）
         ↓
月底：说"帮我做复盘" → AI读飞书数据 → 出爆款规律报告（5分钟）
```

---

## 📖 配置说明（一次性，约20分钟）

### 第一步：创建飞书多维表格

1. 打开飞书（feishu.cn 或手机 App）
2. 左侧点「+」新建 → 选「**多维表格**」
3. 名称填：`自媒体内容管理`
4. 创建完成后**复制浏览器地址栏链接**备用

> 表格字段不需要手动建，第一次使用时 AI 自动创建所有字段

### 第二步：创建飞书 API 应用

1. 浏览器打开 [open.feishu.cn](https://open.feishu.cn)，用飞书账号登录
2. 点「开发者后台」→「**创建企业自建应用**」
3. 应用名称填 `内容助手`，点确定
4. 进入应用 → 左侧「**凭证与基础信息**」
5. 复制 **App ID**（`cli_` 开头）和 **App Secret**（点查看后复制）

> ⚠️ App Secret 只显示一次，立刻复制保存

### 第三步：开通权限并发布

1. 左侧「**权限管理**」→ 搜索 `bitable` → 开通 `bitable:app`
2. 左侧「**版本管理与发布**」→「创建版本」→ 填 `1.0.0` → 提交
3. 点「申请线上发布」→ 选「无需审核直接发布」

### 第四步：把应用连接到你的表格

1. 打开「自媒体内容管理」多维表格
2. 右上角「···」→「**添加应用**」→ 找到「内容助手」→ 添加

### 第五步：配置到 OpenClaw

```
我的飞书 App ID 是 cli_xxx，App Secret 是 xxx，多维表格链接是 https://feishu.cn/base/xxx
```

AI 自动验证并创建所有字段，提示「✅ 已连接」即配置完成。

---

## 飞书4种视图（可视化管理）

配置完后，在飞书里点「+ 新增视图」可切换：

| 视图 | 用途 |
|------|------|
| 📋 表格视图 | 看所有文章状态和数据，直接在格子里填数字 |
| 🗂 看板视图 | 按「选题中/写作中/已发布」分组，拖拽改状态 |
| 📅 日历视图 | 按发布日期展示，看内容节奏 |
| 📊 图表视图 | 阅读/点赞趋势图、平台对比、TOP文章排行 |

---

## 开始用

```
今天知乎/微博有什么热点，帮我选 3 个适合我账号的选题
```
```
把「用 AI 做副业」标记为已发布，阅读 8000，点赞 320，涨粉 45
```
```
帮我做本月内容复盘
```
```
我有哪些草稿超过一周没动了
```

---

## 🔥 核心功能一：热榜选题生成

**这是这个 skill 最核心的功能。**

选题不靠拍脑袋，直接拉取实时热榜数据，结合你的账号方向，生成有流量基础的选题。

### 支持的热榜数据源

| 热榜 | 内容类型 | 适合平台 |
|------|---------|---------|
| 知乎热榜 | 深度问答、社会话题 | 知乎、公众号 |
| 微博热搜 | 实时事件、娱乐热点 | 微博、小红书 |
| 百度热搜 | 搜索趋势、大众话题 | 公众号、头条 |
| 今日头条热榜 | 资讯类热点 | 头条号、公众号 |
| 抖音热点 | 短视频话题 | 抖音、小红书 |
| B站热门 | 年轻圈层话题 | B站、小红书 |

### 使用示例

```
今天有什么热点适合做成公众号文章？我的方向是副业和 AI 工具
```
```
抓一下微博和知乎的热榜，找 3 个适合我的选题，写到飞书
```
```
帮我出本周内容计划，参考热榜数据，5 个选题
```

### 生成结果示例

假设你说：「帮我基于今天热榜，出 3 个公众号选题，方向是 AI 工具」

skill 会：
1. 拉取知乎热榜 + 百度热搜实时数据
2. 筛选与"AI工具"相关或可关联的热点
3. 生成 3 个选题，每个包含：

```
📌 选题 1
标题：《普通人怎么用 AI 工具月入过万？我试了 3 个月》
热点来源：知乎热榜「AI 副业」相关话题（热度 82万）
为什么会点：结合热点 + 利益驱动标题，点击率高
目标读者：想做副业的上班族
核心角度：亲身经历 + 具体方法，不是泛泛而谈
建议发布：周三晚 8-10 点
```

4. 全部自动写入飞书多维表格，状态标记「选题中」

---

## 📊 核心功能二：发布数据追踪

发完内容，一句话更新，告别手动填表。

```
昨天发的「DeepSeek 替代 ChatGPT」，公众号阅读 12000，点赞 450，涨粉 80
```

skill 自动：
- 在飞书里找到那篇文章（模糊匹配标题）
- 更新全部数据字段
- 顺带告诉你这篇在你历史里排第几

```
✅ 已更新「DeepSeek替代ChatGPT」
📊 阅读 12,000 — 近30天排名第 2
💡 「工具对比」类选题在你账号表现持续很好，建议加大这类比例
```

---

## 📈 核心功能三：月度复盘分析

```
帮我做 3 月内容复盘
```

自动读取飞书全部数据，生成结构化报告：

```
## 3 月内容复盘报告

📊 发布 14 篇 | 平均阅读 6,800（↑23%）| 总涨粉 312

### 平台对比
公众号  均值 9,200  ✅ 最强
小红书  均值点赞 180  ✅ 互动最好
知乎    均值 2,100  ⚠️ 产出比低

### 爆款规律（阅读 >10,000 的共同特征）
- 标题带数字：占爆款 80%
- 话题：AI工具 > 副业方法 > 效率提升
- 最佳发布时间：周三晚 8-10 点

### 下月建议
1. 公众号主推「AI工具测评」，标题必须带数字
2. 小红书加大频率，互动率高但内容量不够
3. 知乎减少投入，性价比低
4. 参考热榜追热点，本月追热点的 3 篇均破万
```

---

## ⏰ 核心功能四：拖稿提醒

```
我有哪些草稿超过一周没动了
```

```
⚠️ 3 篇草稿超过 7 天未更新

1. 「如何用 AI 写周报」— 搁置 12 天
2. 「2026年最值得学的技能」— 搁置 9 天
3. 「副业第一桶金怎么来的」— 搁置 8 天

帮你继续写某篇，还是标记归档？
```

---

## 🗂 飞书表格字段（自动创建）

| 字段 | 类型 | 说明 |
|------|------|------|
| 标题 | 文本 | 文章/视频标题 |
| 状态 | 单选 | 选题中 / 写作中 / 已发布 / 已归档 |
| 平台 | 多选 | 公众号 / 知乎 / 小红书 / 抖音 / B站 |
| 发布日期 | 日期 | 实际发布时间 |
| 阅读量 | 数字 | — |
| 点赞 | 数字 | — |
| 涨粉 | 数字 | — |
| 热点来源 | 文本 | 知乎热榜 / 微博热搜 / 原创 等 |
| 选题来源 | 单选 | AI生成 / 热榜追踪 / 读者建议 / 自选 |
| 关键词 | 文本 | SEO 关键词 |
| 备注 | 文本 | 写作思路、参考链接 |

---

## ❓ 常见问题

- **飞书要付费吗？** 免费版完全够用，API 也免费
- **热榜数据实时的吗？** 是，每次调用都拉取最新数据
- **没有历史数据可以用吗？** 可以，新账号直接基于热榜+你说的方向生成选题
- **手机上能看数据吗？** 可以，飞书 App 实时同步
- **需要额外配置吗？** OpenClaw 配置好 AI 即可（支持阿里云百炼、DeepSeek 等），再加飞书 App ID 和 App Secret
- **有问题找谁？** ClawHub 页面留言或联系 @ShuaigeSkillBot
- **需要帮你配置好直接用？** Telegram 私信 @ShuaigeSkillBot，飞书配置服务 ¥99，配好即用

---

## Trigger

When the user mentions any of:
"飞书", "多维表格", "选题", "热榜", "热点", "内容计划", "内容日历", "内容库", "发布追踪", "内容复盘", "自媒体管理", "选题库", "内容管理", "草稿提醒", "知乎热榜", "微博热搜"

Or phrases like:
"帮我生成选题", "今天有什么热点", "更新一下数据", "帮我做复盘", "哪些草稿没动"

## Configuration

Check for these at session start:
- `FEISHU_APP_ID` — starts with `cli_`
- `FEISHU_APP_SECRET`
- `FEISHU_BITABLE_URL` — the multidimensional table URL

If missing, guide user through setup with the step-by-step instructions above.

Get access token:
```
POST https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal
{"app_id": "{FEISHU_APP_ID}", "app_secret": "{FEISHU_APP_SECRET}"}
```
Token expires every 2 hours — re-fetch automatically when needed.

## Hot Data Sources

Fetch trending data from these free, no-auth endpoints (all accessible from mainland China):

```
知乎热榜:    GET https://tenapi.cn/v2/zhihuhot
微博热搜:    GET https://v2.xxapi.cn/api/weibohot
百度热搜:    GET https://tenapi.cn/v2/baiduhot
今日头条:    GET https://tenapi.cn/v2/toutiaohotnew
抖音热点:    GET https://tenapi.cn/v2/douyinhot
```

Response format (all return similar structure):
```json
{"code": 200, "data": [{"title": "热点标题", "url": "...", "hot": "热度数值"}]}
```

Fallback strategy: if one endpoint fails, try the next. If all fail, proceed with user's historical data only and note that hot data is temporarily unavailable.

## Workflow

### Step 1: Initialize
1. Get Feishu access token
2. Parse bitable URL → extract `app_token` and `table_id`
3. Check table schema; if missing fields, offer to create them
4. Confirm: "✅ 已连接飞书多维表格，共 XX 条记录"

### Step 2: Route Request

#### ACTION: generate_topics (核心功能)

Triggered by: 选题, 热点, 内容计划, 帮我出选题

Process:
1. Fetch hot data from relevant platforms based on user's target platform:
   - 公众号/知乎 → fetch 知乎热榜 + 百度热搜
   - 小红书/抖音 → fetch 微博热搜 + 抖音热点
   - 头条 → fetch 今日头条 + 百度热搜
   - If unspecified → fetch all 5 sources

2. Read user's last 20 published entries from Feishu (if any) to understand:
   - Content niche and style
   - Which topic types performed best (highest reads/likes)
   - Which platforms they publish to

3. Match hot topics to user's niche:
   - Filter irrelevant hot topics
   - Find angles that connect hot topics to user's vertical
   - Prioritize topics with high heat scores AND relevance

4. Generate N topics (default 5), each containing:
   - 标题 (title — specific, clickable, ideally with numbers)
   - 热点来源 (which hot list + heat score)
   - 为什么适合 (why it fits this account)
   - 目标读者
   - 核心写作角度
   - 建议发布平台
   - 建议发布时间 (based on user's historical best times, or default Wed/Fri 8-10pm)

5. Write all to Feishu with status="选题中", 选题来源="AI生成+热榜追踪"

6. Output summary to user, then confirm Feishu write

#### ACTION: update_publish_status

Triggered by: 已发布, 标记发布, 更新数据, 阅读量

Process:
1. Search Feishu records for matching title (fuzzy match on 标题 field)
2. If multiple matches → list them, ask user to choose
3. Update all provided fields: 状态, 发布日期, 平台, 阅读量, 点赞, 涨粉
4. Compare to user's average → generate brief performance note
5. Confirm update

#### ACTION: monthly_review

Triggered by: 复盘, 分析, 哪类内容, 表现, 爆款

Process:
1. Query all records with 状态=已发布 in specified date range
2. Calculate:
   - Total published, average reads/likes/followers
   - Per-platform performance table
   - Top 5 articles by reads and by likes
   - Common patterns in top performers (title style, topic category, publish time)
   - Month-over-month comparison if prior month data exists
3. Output structured Chinese report (format shown in Core Feature 3 above)
4. End with 3-5 specific, actionable recommendations

#### ACTION: overdue_drafts

Triggered by: 草稿, 没动, 超期, 拖稿

Process:
1. Query records with 状态 IN (选题中, 写作中)
2. Filter where creation/update time > 7 days ago
3. List with days overdue, sorted by most overdue first
4. Ask: "帮你继续写某篇，还是标记归档？"

#### ACTION: show_calendar

Triggered by: 本周计划, 内容日历, 几篇, 日历

Process:
1. Query records with 发布日期 in requested range
2. Display as day-by-day plan
3. Show gap days with "⬜ 待安排"

### Step 3: Feishu Bitable API

Headers for all requests:
```
Authorization: Bearer {tenant_access_token}
Content-Type: application/json
```

**List records:**
```
GET https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records?page_size=100
```

**Search records:**
```
POST https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/search
{
  "filter": {
    "conjunction": "and",
    "conditions": [
      {"field_name": "状态", "operator": "is", "value": ["已发布"]}
    ]
  },
  "sort": [{"field_name": "发布日期", "order": "DESC"}]
}
```

**Create record:**
```
POST https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records
{
  "fields": {
    "标题": "文章标题",
    "状态": "选题中",
    "平台": ["小红书"],
    "热点来源": "知乎热榜 · 热度82万",
    "选题来源": "AI生成+热榜追踪"
  }
}
```

**Update record:**
```
PATCH https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/records/{record_id}
{
  "fields": {
    "状态": "已发布",
    "阅读量": 8000,
    "点赞": 320,
    "涨粉": 45,
    "发布日期": "2026-03-29"
  }
}
```

**Create table fields (first-time setup):**
```
POST https://open.feishu.cn/open-apis/bitable/v1/apps/{app_token}/tables/{table_id}/fields
{"field_name": "阅读量", "type": 2}
```
Field types: 1=Text, 2=Number, 3=SingleSelect, 4=MultiSelect, 5=Date

### Step 4: Error Handling

| Error | Response |
|-------|----------|
| 401 Unauthorized | "App ID 或 App Secret 有问题，重新粘贴一下" |
| 403 Forbidden | "应用没有权限访问这个表格，检查一下是否已添加应用" |
| 404 Not Found | "找不到这个表格，链接是否正确？" |
| Hot API timeout | 跳过该热榜，用其他数据源，最后告知用户"XX热榜暂时不可用" |
| Title not found | 列出最近 10 条记录，让用户选择 |
| Token expired | 自动重新获取 token，无需用户操作 |

## Rules
1. 优先拉取热榜数据再生成选题，有数据支撑的选题才有价值
2. 新用户没有历史数据时，直接基于热榜+用户说的方向生成，不报错
3. 模糊匹配标题时，若有多个结果，必须让用户确认，不要猜
4. 删除操作必须二次确认
5. 全程中文输出，除非用户用英文提问
6. 每次飞书写入后都要明确确认："✅ 已存入飞书：[标题]"
7. API credentials 只在会话内存中，不写入任何文件
8. 热榜 API 失败时优雅降级，不影响其他功能

---
📢 每日市场数据播报，关注 Telegram 频道：https://t.me/shuaigeclaw
