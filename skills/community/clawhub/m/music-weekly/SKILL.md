---
name: music-weekly
description: Weekly music album curation system — auto-search new releases across regions (English/Chinese/Japanese/Korean/Latin), score-filter ≥7.5, dedup against history, write to Notion DB, and push to your preferred channel (QQ/Telegram/Discord/Signal/WeCom/Feishu). Includes one-command setup script that creates the Notion database from scratch, config file with sensible defaults, and all required directories. Ideal for cron-driven music recommendation workflows. Use when: (1) running weekly music recommendation cron, (2) user asks "本周有什么好专辑", (3) user needs to fix/backfill cover URLs, (4) setting up the music weekly system for the first time.
---

# Music Weekly — 音乐周报

一个可配置的每周音乐推荐系统。自动搜索各地区的本周新专辑，评分筛选≥7.5分的优质作品，写入 Notion 数据库，并通过你设定的频道推送到你手上。

---

## 目录

1. [快速开始](#快速开始)
2. [配置详解](#配置详解)
3. [推送频道设置](#推送频道设置)
4. [核心概念](#核心概念)
5. [工作流](#工作流)
6. [脚本工具](#脚本工具)
7. [自定义主题](#自定义主题)
8. [故障排除](#故障排除)

---

## 快速开始

### 安装

```bash
npx clawhub install music-weekly
cd skills/music-weekly
```

### 一行初始化（推荐）

```bash
python3 scripts/setup.py
```

按提示输入 Notion API Key 和推送目标即可。脚本会自动：

| 操作 | 说明 |
|------|------|
| ✅ 创建配置文件 | `~/.config/music-weekly/config.json`，默认值已填好 |
| ✅ 创建目录 | covers_dir、media_dir 自动建立 |
| ✅ 创建历史记录文件 | `music-recommended-log.md` 带表头 |
| ✅ 创建 Notion 数据库 | 所有字段齐全，直接可用 |

### 静默模式（传参）

```bash
python3 scripts/setup.py \
  --notion-key "ntn_你的密钥" \
  --parent-page "父页面ID" \
  --channel telegram \
  --target "123456789"
```

### 默认值

不配置时脚本自动使用以下路径（基于 OpenClaw 工作区约定）：

| 配置项 | 默认值 |
|--------|--------|
| `covers_dir` | `~/.openclaw/workspace/covers` |
| `media_dir` | `~/.openclaw/media/qqbot` |
| `history_log` | `~/.openclaw/workspace/music-recommended-log.md` |
| `sender_name` | `🎵 音乐编辑` |
| `delivery_channel` | `telegram` |

### 手动验证

```bash
python3 scripts/notion_utils.py config
```

如果返回了你的配置摘要（key 会被部分隐藏），就说明配好了。

---

## 配置详解

| 字段 | 必填 | 类型 | 默认值 | 说明 |
|------|------|------|--------|------|
| `notion_api_key` | ✅ | string | — | Notion 集成密钥，以 `ntn_` 开头 |
| `notion_db_id` | ⚠️ | string | — | Notion 数据库 UUID（可用 `setup.py --parent-page` 自动创建） |
| `delivery_channel` | ✅ | string | `telegram` | 推送频道，详见下表 |
| `delivery_target` | ✅ | string | — | 推送目标 ID |
| `covers_dir` | ❌ | string | `~/.openclaw/workspace/covers` | 封面图片本地缓存目录 |
| `media_dir` | ❌ | string | `~/.openclaw/media/qqbot` | 媒体暂存目录（QQ Bot） |
| `history_log` | ❌ | string | `~/.openclaw/workspace/music-recommended-log.md` | 历史推荐记录文件 |
| `sender_name` | ❌ | string | `🎵 音乐编辑` | 推送时显示的发件人名称 |

> ❌ = 自动填充默认值，不填也能用
> ✅ = 必须填写
> ⚠️ = 可用 setup 脚本自动创建

> 环境变量 `NOTION_KEY` 也可作为 `notion_api_key` 的备用来源。

### Notion 数据库要求

数据库必须包含以下字段（字段名精确匹配）：

| 字段名 | 类型 | 用途 |
|--------|------|------|
| 名称 | title | 专辑名（仅专辑名，不含艺术家） |
| 艺术家 | rich_text | 艺术家名 |
| 发行日期 | date | YYYY-MM-DD |
| 流派 | select | 主要 Genre |
| 综合评分 | number | 10分制 |
| 收听状态 | select | 未听 / 已听 / 循环中 / 想听 |
| 专辑类型 | select | 全长 / EP / 单曲 |
| 厂牌 | rich_text | 厂牌名 |
| 评论来源 | rich_text | 如 Pitchfork, AllMusic |
| 推荐短语 | rich_text | 30字以内精炼推荐 |
| 推荐理由 | rich_text | 100字以上推荐正文 |
| Apple Music链接 | url | Apple Music 专辑页 |
| 音乐分布 | multi_select | 🇺🇸 美国、🇰🇷 韩国 等 |
| 周次 | rich_text | 如 `2026年第20周 2期` |
| 推送日期 | date | 实际推送日期 |
| 封面URL | files | 专辑封面图（⚠️ 见下方注意） |

> **封面URL 字段类型是 files 不是 url**，这是一个常见坑。写入时使用外部文件格式，详见「核心概念」章节。

---

## 推送频道设置

### 支持的所有频道

| 频道 | `delivery_channel` 值 | `delivery_target` 格式 | 前提 |
|------|----------------------|----------------------|------|
| **QQ Bot** | `qqbot` | `qqbot:c2c:用户OpenID` | 需配置 `channels.qqbot` |
| **Telegram** | `telegram` | `123456789`（用户ID）或 `@username` | 需配置 `channels.telegram` |
| **Discord** | `discord` | `123456789012345678`（频道ID） | 需配置 `channels.discord` |
| **Signal** | `signal` | `+8613800138000` | 需配置 `channels.signal` |
| **企业微信** | `wecom` | 用户ID | 需配置 `channels.wecom` |
| **飞书** | `feishu` | `ou_xxxxxxxx`（open_id） | 需配置 `channels.feishu` |
| **Slack** | `slack` | `C1234567`（频道ID） | 需配置 `channels.slack` |
| **WhatsApp** | `whatsapp` | 手机号 | 需配置 `channels.whatsapp` |

### 推送内容格式

所有频道通用文字模板：

```
{sender_name} | {week_label}

━━━━━━━━━━━━━━━━━━

{序号}️⃣ {艺术家} — {专辑名}
📅 发行日期：yyyy-mm-dd
🏷️ {流派}
⭐ 综合评分：{分数}/10
💬 {推荐理由}

Apple Music: {链接}
━━━━━━━━━━━━━━━━━━

...（重复5张）

✨ 本周编辑精选 | {一句话总结}
```

### 不同频道的封面图发送方式

**QQ Bot：** 使用 `<qqmedia>` 标签嵌入到消息中。图片文件需先复制到配置的 `media_dir` 目录。

```
🎵 本周音乐精选 | 2026年5月15日
<qqmedia>/home/user/media/music/cover.jpg</qqmedia>

1️⃣ Broken Social Scene — Remember The Humans
📅 发行日期：2026-05-08
...
```

**Telegram / Discord / Signal 等：** 使用 `message` 工具的 `media` 参数，直接传本地文件路径。

⚠️ **原则：封面图和文字必须在同一条消息中发送，不要分开推送。**

---

## 核心概念

### 1. 周次命名规则

| 批次 | 运行日 | 命名 |
|------|--------|------|
| 第1期 | 周二 | `2026年第{X}周 1期` |
| 第2期 | 周五 | `2026年第{X}周 2期` |

### 2. 地区比例（每期5张）

| 地区 | 数量 | 说明 |
|------|------|------|
| 🇺🇸🇬🇧 英语圈 | **2-3张** | 核心内容，Soul / R&B / Jazz / Indie / Electronic 等 |
| 🇨🇳 华语 | **最多1张** | 不与日韩同周出现 |
| 🇯🇵🇰🇷 日韩 | **最多1张** | 不与华语同周出现 |
| 🌎 拉丁/其他 | **0-1张** | Reggaeton / Latin Pop 等 |

**补充规则：** 如果某周某地区确实找不到≥7.5分的好专辑，可从英语圈补位。但华语和日韩至少各保留候选席位，不要连续多周只有英语专辑。

### 3. 评分标准

- **基准线：≥7.5分**
- **优先推荐：≥8.0分**
- 低于7.5分不推荐
- 8分以下的专辑必须有充分理由才能推
- **禁止编造评分**：所有分数必须来自 Apple Music、Pitchfork、RateYourMusic、Metacritic、AllMusic、QQ音乐、网易云音乐等**真实可查的平台**
- 综合评分取多平台加权平均

### 4. 封面URL 是 files 类型

Notion 的「封面URL」字段类型是 **files**，不是 **url**。这是最常见的报错来源。

**✅ 正确写法：**
```json
"封面URL": {
  "files": [{
    "type": "external",
    "name": "cover.jpg",
    "external": {
      "url": "https://is1-ssl.mzstatic.com/.../600x600bb.jpg"
    }
  }]
}
```

**❌ 错误写法（会报 `封面URL is expected to be files`）：**
```json
"封面URL": {
  "url": "https://is1-ssl.mzstatic.com/..."
}
```

### 5. 查重规则

每次推荐前必须读取 `music-recommended-log.md` 全部历史记录。同一张专辑（相同艺术家+专辑名或相同 Apple Music ID）**永远不重复推荐**，无论相隔多少周。

---

## 工作流

完整的工作流步骤见 [`references/workflow.md`](references/workflow.md)，此处为概要：

```
Step 0: 读取历史 log，建立已推荐清单
Step 1: 搜索本周新发行（按地区分工）
Step 2: 筛选候选池（评分≥7.5，发行≤1个月）
Step 3: 逐一查重
Step 4: 跨地区平衡（最终5张）
Step 5: 收集详细信息（iTunes API获取封面、厂牌、曲目数等）
Step 6: 写入 Notion（封面URL用 files 格式）
Step 7: 推送消息（文字+封面图一起发）
Step 8: 追加到历史 log
```

---

## 脚本工具

### `scripts/notion_utils.py`

```bash
# 搜索专辑信息（iTunes API）
python3 scripts/notion_utils.py search "NMIXX" "Heavy Serenade"

# 通过 Apple Music 链接获取封面图 URL
python3 scripts/notion_utils.py artwork "https://music.apple.com/us/album/remember-the-humans/1871484971"

# 查看当前配置
python3 scripts/notion_utils.py config

# 补填数据库中所有缺失的封面URL
python3 scripts/notion_utils.py backfill

# 查看配置文件路径
python3 scripts/notion_utils.py config-path
```

### 在 Python 中调用

```python
from scripts.notion_utils import (
    search_itunes,
    get_artwork_from_apple_link,
    create_record,
    update_cover_url,
    query_all,
    get_config,
)

# 搜索专辑
info = search_itunes("Broken Social Scene", "Remember The Humans")
# info 包含: artist, album, release_date, artwork_url,
#            apple_music_url, track_count, copyright, genre

# 创建 Notion 记录
create_record({
    "名称": info["album"],
    "艺术家": info["artist"],
    "发行日期": info["release_date"],
    "流派": info["genre"],
    "综合评分": 8.0,
    "收听状态": "未听",
    "专辑类型": "全长" if info["track_count"] >= 10 else "EP",
    "厂牌": info["copyright"].replace("℗ ", ""),
    "推荐理由": "这是一张出色的专辑...",
    "Apple Music链接": info["apple_music_url"],
    "音乐分布": ["🇨🇦 加拿大"],
    "周次": "2026年第20周 2期",
    "推送日期": "2026-05-15",
    "封面URL": info["artwork_url"],
})
```

---

## 自定义主题

编辑推送消息的 `sender_name` 配置项可以自定义发件人名称。也可以在工作流的推送步骤中自定义消息格式，如：

- 增加 emoji 装饰
- 调整信息排列顺序
- 加入个人化的编辑推荐语

推送消息的完整模板见 [`references/workflow.md`](references/workflow.md) 的「推送」章节。

---

## 故障排除

### 「封面URL is expected to be files」

**原因：** 用了 url 类型写入，但该字段在 Notion 中实际是 files 类型。

**解决：** 使用 `scripts/notion_utils.py` 的 `create_record()` 函数（自动处理 files 格式），或参考「核心概念」章节手动构造正确的 JSON 格式。

### 「Could not find database with ID」

**原因：** Notion 集成没有连接到该数据库，或者数据库 ID 填错了。

**解决：**
1. 确认数据库已与你的集成共享（数据库页面右上角「…」→「连接到」→ 选择你的集成）
2. 确认配置文件中的 `notion_db_id` 正确（从数据库 URL 中提取 UUID）
3. 数据库中包含所需的全部字段

### iTunes 搜索不到专辑

**常见原因与对应策略：**

| 原因 | 策略 |
|------|------|
| 拼写差异 | 尝试不同的关键词组合 |
| 未在 Apple Music 上线 | 换一个候选专辑 |
| 仅部分地区可用 | 尝试用美区 iTunes 搜索 |

**重试策略：** 3次搜索失败 → 放弃该候选，换下一张。不要卡死在单一专辑上。

### 推送消息没有封面图

- **QQ Bot：** 图片需要先复制到配置的 `media_dir` 目录，使用 `<qqmedia>` 标签
- **其他频道：** 使用 `message` 工具的 `media` 参数传本地文件
- 文件权限问题：确保图片文件可读（`chmod 644`）

---

> 更多问题？在 OpenClaw Discord（https://discord.com/invite/clawd）或 ClawHub 上提出 issue。
