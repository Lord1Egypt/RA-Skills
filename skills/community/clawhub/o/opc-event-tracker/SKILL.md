---
name: OPC赛事活动追踪
slug: opc-event-tracker
displayName: OPC赛事活动追踪
version: "2.3.0"
description: 追踪 OPC/AI/独立开发者相关赛事活动。从信息源抓取 → 提取结构化信息 → 提交到 OPC 公共赛事池。安装时引导用户获取 API Key。触发词：赛事、比赛、hackathon、活动、OPC赛事、AI比赛、独立开发者大赛、收录赛事、加到OPC
agent_created: true
triggers:
  - 赛事
  - 比赛
  - hackathon
  - 活动
  - OPC赛事
  - AI比赛
  - 独立开发者大赛
  - 收录赛事
  - 加到OPC
  - 推到OPC
xiaping_trigger:
  - 赛事
  - 比赛
  - hackathon
  - 活动
  - OPC
  - AI比赛
  - 收录赛事
xiaping_category:
  - 效率工具
  - 信息聚合
xiaping_tags:
  - 赛事追踪
  - OPC
  - 黑客松
  - AI
  - 创业大赛
  - 独立开发者
---

# 赛事活动追踪

## 首次安装引导（必须执行）

安装本技能后，**必须首先告知用户数据行为，由用户自主选择**。

### 引导流程

**第一步：数据透明度告知**

```
🔑 OPC赛事活动追踪 — 首次使用配置

本技能涉及两类数据处理，请仔细阅读后选择：

📤 数据上传（可选）
  • 目标：将你发现的赛事信息提交到 OPC 公共赛事池（https://mrkjai.com）
  • 上传内容：赛事名称、简介、类型、地区、主办方、时间、链接
  • 上传方式：HTTPS 加密传输，使用你的个人 API Key 鉴权
  • 去重机制：同一链接不会重复收录
  • 可见范围：提交后赛事对所有 OPC 用户可见

📁 本地存储（始终生效）
  • 追踪记录保存在本机 scripts/data/ 目录下
  • 不上传任何数据到外部服务器

⚠️ 你可以随时关闭上传：说「关闭赛事上传」即可
⚠️ 即使不上传，技能的本地追踪功能完全可用

请选择：
  1️⃣ 开启上传 — 我会引导你获取 API Key，赛事将提交到 OPC 公共池
  2️⃣ 关闭上传 — 技能仅本地运行，不上传任何数据
  3️⃣ 稍后配置 — 先跳过，后续说「配置赛事上传」再设置
```

**第二步：根据用户选择执行**

| 用户选择 | 操作 |
|---------|------|
| **1️⃣ 开启上传** | 输出获取 Key 引导 → 用户提供 Key → 写入 `user_config.json`（`upload_enabled=true`） |
| **2️⃣ 关闭上传** | 写入 `user_config.json`（`upload_enabled=false`），告知：「✅ 已关闭上传，所有数据仅保存在本地」 |
| **3️⃣ 稍后配置** | 不做修改，告知：「好的，后续说『配置赛事上传』可随时开启」 |

**第三步：获取 API Key 引导（仅选项1时执行）**

```
📋 API Key 获取方式：
  1. 打开 https://mrkjai.com
  2. 登录/注册账号
  3. 进入「我的 → 个人集成（API Key）」页面
  4. 复制你的 Key（格式：opc_user_xxx...）
  5. 回到这里，把 Key 发给我

💡 Key 仅保存在本地 scripts/user_config.json，不会上传到任何地方。
```

### 运行时检查

每次执行上传操作前，必须检查 `upload_enabled` 字段：
- `upload_enabled: true` + 有 Key → 正常上传
- `upload_enabled: false` → 跳过上传，仅本地操作
- `upload_enabled: true` + 无 Key → 提示用户设置 Key

---

## 触发方式

- 用户提供赛事链接 + 说"收录"/"加到OPC"/"推到OPC" → **提取+提交到 OPC**
- 用户主动问"有什么赛事" → 展示本地追踪记录
- 用户主动问"有什么赛事"/"OPC有什么比赛"/"查一下赛事池" → **查询 OPC 赛事池**
- 用户说"查一下AI比赛"/"看看黑客松" → **按条件查询**

### 流程C：查询 OPC 赛事池

1. 用户说「有什么赛事」/「OPC有什么比赛」/「查一下赛事池」
2. 调用 `GET /api/events/list` 查询 OPC 赛事池
3. 格式化返回结果展示给用户（表格形式）
4. 支持按 type/region/status/keyword/contributor 过滤
5. 支持分页（limit/offset）和排序（sort）

**查询示例**：
- "有什么赛事" → 查全部（默认20条，按发布时间倒序）
- "有什么黑客松" → type=hackathon
- "上海有什么AI比赛" → region=shanghai + keyword=AI
- "报名截止的赛事" → status=open

### 流程D：定时追踪
- 用户说"新增信息源" → 追加到 sources.json
- 用户说"关闭赛事上传"/"关闭上传" → **关闭上传**（设置 upload_enabled=false）
- 用户说"开启赛事上传"/"配置赛事上传" → **开启上传**（引导设置 Key）

---

## 核心流程

### 流程A：用户提供链接 → 收录到 OPC

1. 用 WebFetch 抓取链接内容
2. 从页面中提取结构化字段（见下方字段映射表）
3. 展示确认清单，等用户确认
4. 调用 OPC API 提交
5. 同时写入本地 events_history.json

### 流程B：定时追踪 → 自动抓取+提交

1. 读取 `scripts/sources.json`，获取所有已启用的信息源
2. 逐个信息源抓取页面内容
3. 调用对应解析器提取结构化字段
4. 与 `scripts/events_history.json` 比对
5. 新赛事 → 调用 OPC API 提交（使用用户的 API Key）
6. 更新本地历史 JSON + Markdown 记录
7. 输出摘要

---

## OPC API 接口规范

### 提交接口：POST /api/events/ingest

| 项目 | 值 |
|------|-----|
| 方法 | POST |
| 路径 | `/api/events/ingest` |
| 域名 | 从 user_config.json 读取 `api_base`，默认 `https://mrkjai.com` |
| Content-Type | application/json; charset=utf-8 |
| 鉴权 | Header `X-API-Key: {api_key}` |

### 必填字段

| 字段 | 类型 | 限制 | 说明 |
|------|------|------|------|
| `title` | string | 1-120 字符 | 赛事名称 |
| `summary` | string | 1-300 字符 | 一句话描述 |
| `type` | enum | 见下方 | 赛事类型 |
| `region` | enum | 见下方 | 地区 |
| `organizer` | string | 1-100 字符 | 主办方 |
| `publishedAt` | string | ISO 8601 | 赛事发布/开始时间 |
| `deadlineAt` | string | ISO 8601 | 报名截止时间，必须晚于 publishedAt |
| `externalUrl` | string | 合法 URL | 赛事详情页 URL，去重键 |

### 选填字段

| 字段 | 类型 | 限制 |
|------|------|------|
| `tags` | string[] | 最多 8 个 |

### 枚举值

**type**：`startup`(创业大赛) / `hackathon`(黑客松) / `design`(设计比赛) / `academic`(学术竞赛) / `summit`(行业峰会)

**region**：`online`(线上) / `beijing` / `shanghai` / `hangzhou` / `shenzhen` / `national`(全国) / `overseas`(海外)

### 返回码

| code | 含义 |
|------|------|
| `created` | 成功收录 |
| `exists` | externalUrl 已存在（幂等） |
| `unauthenticated` | 缺 X-API-Key |
| `invalid_key` | Key 无效 |
| `key_revoked` | Key 已撤销 |
| `validation_error` | 字段校验失败 |
| `internal_error` | 服务器异常 |

### 查询接口：GET /api/events/list

| 项目 | 值 |
|------|-----|
| 方法 | GET |
| 路径 | `/api/events/list` |
| 鉴权 | Header `X-API-Key: {api_key}`（同 ingest，同一个 key） |

**Query 参数（全部可选）**：

| 参数 | 类型 | 默认 | 说明 |
|------|------|------|------|
| `type` | enum | — | `startup` / `hackathon` / `design` / `academic` / `summit` |
| `region` | enum | — | `online` / `beijing` / `shanghai` / `hangzhou` / `shenzhen` / `national` / `overseas` |
| `status` | enum | — | `fresh`(7天内新发布) / `open`(报名中) / `closing`(3天内截止) / `ended`(已截止) |
| `keyword` | string | — | 模糊搜索 title/summary/organizer |
| `contributor` | string | — | 贡献者账号名（精确匹配） |
| `limit` | int 1-100 | 20 | 每页条数 |
| `offset` | int ≥0 | 0 | 跳过条数 |
| `sort` | enum | `published_desc` | `published_desc` / `deadline_asc` / `deadline_desc` / `created_desc` |

**响应格式**：

```json
{
  "ok": true,
  "data": {
    "items": [{ "id", "title", "summary", "type", "region", "organizer",
                "publishedAt", "deadlineAt", "externalUrl", "tags",
                "contributor", "createdAt", "updatedAt" }],
    "total": 38,
    "limit": 20,
    "offset": 0,
    "hasMore": true
  }
}
```

**错误码**：同 ingest（unauthenticated / invalid_key / key_revoked / validation_error / internal_error）

---

## 字段提取规则

### 从页面内容推断字段

| 抓取内容 | API 字段 | 推断规则 |
|----------|---------|---------|
| 页面 h1 / title | `title` | 去站点后缀、清理空白 |
| meta description / 首个 p | `summary` | 截断到 300 字符 |
| 主办方/承办方文本 | `organizer` | 截断到 100 字符 |
| 比赛开始时间 | `publishedAt` | 转 ISO 8601；找不到用当前时间 |
| 报名截止时间 | `deadlineAt` | 转 ISO 8601；找不到传 publishedAt + 30 天 |
| 详情页 URL | `externalUrl` | 原样传，用于去重 |
| 关键词/分类 | `tags` | 取前 8 个 |

### type 推断

```
含"黑客松/hackathon/编程马拉松" → hackathon
含"创业/路演/business plan/startup" → startup
含"设计/UI/UX/品牌/visual" → design
含"数学/建模/学术/ACM/科研" → academic
含"峰会/summit/conference/大会" → summit
都匹配不到 → hackathon（默认）
```

### region 推断

```
含"线上/online/远程" → online
含"北京" → beijing
含"上海" → shanghai
含"杭州" → hangzhou
含"深圳" → shenzhen
含"全国/中国" → national
含"海外/国外/overseas" → overseas
都没匹配 → online（默认）
```

### 重要规则

- deadlineAt 抓不到时传 publishedAt + 30 天，summary 里注明"长期有效"
- title 或 organizer 抓不到 → 直接告诉用户缺失，不瞎猜
- 同一 externalUrl 重复提交是幂等的（接口返回 exists）
- publishedAt 不要设为未来时间

---

## 执行命令

```bash
# 追踪模式（默认）：抓取信息源 + 提交到 OPC
python3 track_events.py

# 查询模式：查 OPC 赛事池已有数据
python3 track_events.py query

# 查询 + 过滤：只看黑客松
python3 track_events.py query --type hackathon

# 查询 + 过滤 + 分页：上海地区，AI关键词，5条
python3 track_events.py query --region shanghai --keyword AI --limit 5

# 查询 + 排序：按报名截止时间升序
python3 track_events.py query --sort deadline_asc
```

---

## 信息源管理

配置文件：`scripts/sources.json`

用户新增信息源时，追加到 `sources` 数组：

```json
{
  "id": "唯一标识",
  "name": "显示名称",
  "url": "抓取地址",
  "type": "forum_post | official_page | rss | api | campaign_page",
  "category": "OPC赛事 | AI赛事 | 创业大赛 | 独立开发者",
  "organizer": "主办方",
  "enabled": true,
  "notes": "备注"
}
```

新增信息源后，在 `scripts/track_events.py` 的 `PARSERS` 字典注册对应解析函数。

### 已配置信息源

| ID | 名称 | URL | 类型 | 状态 |
|----|------|-----|------|------|
| trae_forum | TRAE AI 创造力大赛 | https://forum.trae.cn/t/topic/28826 | forum_post | ✅ |
| workbuddy_super_individual | WorkBuddy 超级个体大赛 | https://www.codebuddy.cn/events/super-individual | campaign_page | ✅ |

---

## 数据存储

| 文件 | 安装后路径 | 用途 |
|------|---------|------|
| user_config.json | `scripts/user_config.json` | 用户 API Key + 上传开关配置（**勿提交到公开仓库**） |
| sources.json | `scripts/sources.json` | 信息源配置 |
| events_history.json | `scripts/events_history.json` | 历史赛事记录（自动生成） |
| 赛事记录.md | `scripts/data/赛事记录.md` | 人类可读记录（自动生成） |

---

## 数据透明度声明

本技能遵循最小权限和透明原则：

| 行为 | 是否上传 | 目标服务器 | 用户控制 |
|------|---------|----------|---------|
| 本地追踪（抓取赛事信息） | ❌ 仅本地 | — | 始终生效 |
| 赛事提交到 OPC 赛事池 | ✅ 可选 | https://mrkjai.com | `upload_enabled` 字段控制 |
| 查询 OPC 赛事池 | ✅ 发起 GET 请求 | https://mrkjai.com | 需要 API Key |

**user_config.json 完整结构**：

```json
{
  "api_key": "opc_user_xxx...",
  "api_base": "https://mrkjai.com",
  "upload_enabled": true,
  "configured_at": "2026-06-22T17:00:00+08:00"
}
```

- `upload_enabled: true` → 新发现的赛事自动提交到 OPC 公共池
- `upload_enabled: false` → 所有功能仅在本地运行，不发送任何赛事数据
- 可随时说「关闭赛事上传」或「开启赛事上传」切换

---

- [sources-mgmt.md](references/sources-mgmt.md) — 信息源添加规范
- [api-spec.md](references/api-spec.md) — OPC API 完整对接文档（可复制给其他 AI）

---

## 开源发布注意事项

### ⚠️ 安全提醒

- **`scripts/user_config.json` 包含用户 API Key，切勿提交到公开仓库**
- 建议在 `.gitignore` 中添加：`scripts/user_config.json` 和 `scripts/data/`
- `scripts/events_history.json` 和 `scripts/last_run_summary.json` 是运行时产物，也不应提交

### 推荐的 `.gitignore`

```
scripts/user_config.json
scripts/events_history.json
scripts/last_run_summary.json
scripts/data/
```

### 开源适配清单

| 检查项 | 状态 |
|--------|------|
| 无硬编码绝对路径 | ✅ DATA_DIR 改为相对路径 |
| 无真实 API Key | ✅ user_config.json 已清空 |
| Python 路径通用化 | ✅ 执行命令改为 python3 |
| 勿提交运行时产物 | ✅ .gitignore 已建议 |

---

## 📝 版本迭代记录

| 版本 | 日期 | 更新内容摘要 | 操作人 |
|------|------|------------|--------|
| v1.0 | 2026-06-22 | 创建技能（WebSearch 方案） | Kyle |
| v1.1 | 2026-06-22 | 升级脚本化抓取 + JSON历史比对 | Kyle |
| v2.0 | 2026-06-22 | 重大升级：集成 OPC API 提交 + 安装引导获取 Key + 用户链路 | Kyle |
| v2.1 | 2026-06-22 | 开源适配：清空真实 Key、路径通用化、添加 .gitignore 建议 | Kyle |
| v2.2 | 2026-06-22 | 新增赛事查询功能：GET /api/events/list + query 模式 + 表格格式化 | Kyle |
| v2.3 | 2026-06-22 | 安全修复：清空泄露 Key + 新增 upload_enabled 开关 + 首次安装数据透明度告知 | Kyle |
