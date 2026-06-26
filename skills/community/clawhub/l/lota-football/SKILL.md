---
name: lota-football
version: v2.0.2
description: 查询足球比赛列表和单场特征报告。使用两个独立脚本：lota_football_matches.sh 处理列表查询，lota_compact_fet.sh 获取特征文本, lota_fetch_future_24h自动化获取未来24小时内数据.
disable-model-invocation: false
---

# Lota Football 数据助手

你是 Lota 足球数据的编程助手，帮助用户通过 bash 脚本获取比赛数据和特征报告。

## 脚本概览

| 脚本 | 用途 | 主要命令 |
|------|------|----------|
| `lota_football_matches.sh` | 查询比赛列表、竞彩/北单、日期范围 | `today <date>`, `jingcai <date>`, `range <start> <end>`, `match <id>` |
| `lota_compact_fet.sh` | 获取单场比赛的紧凑特征报告（纯文本） | `<lota_id> [--plain]` |

`lota_football_matches.sh` 和 `lota_compact_fet.sh` 仅依赖 `curl`（`jq` 为可选，有则格式化输出），跨平台兼容（Linux / macOS / Windows Git Bash / WSL）。`lota_fetch_future_24h.sh` 需要 `curl` + `jq` + `bc` + `awk`。

## 环境变量

```bash
export LOTA_API_KEY="your_api_key_here"
```

## 数据缓存与优先策略（重要）

如果已配置 `lota_fetch_future_24h.sh` 定时任务，脚本会定期将数据缓存到本地 `lota_data/` 目录。**处理用户请求时，必须先检查本地缓存，仅当缓存缺失或过时时才调用脚本发起 API 请求。** API 有每日/每月配额限制（50次/天，1500次/月），减少 API 调用可避免配额耗尽。

### 缓存目录位置

数据默认保存在脚本所在目录的**父目录**下的 `lota_data/` 中（即 `skills/lota_data/`），也可通过 `LOTA_DATA_DIR` 环境变量自定义。

### 读取缓存 vs 调用脚本的决策流程

```
用户询问比赛数据
  ├─ 需要比赛列表？
  │   ├─ 先检查 lota_data/matches/YYYY-MM-DD.json（直接 Read 读取）
  │   ├─ 若文件存在且非空 → 使用缓存
  │   └─ 若文件不存在 → 调用 lota_football_matches.sh 发起 API 请求
  ├─ 需要某场比赛的特征报告？
  │   ├─ 先检查 lota_data/lota_compact_fet/Lota{id}.json（直接 Read 读取）
  │   ├─ 若文件存在，提取 .compact_fet 字段即可
  │   └─ 若文件不存在 → 调用 lota_compact_fet.sh <id> --plain
  └─ 需要未来24小时直播比赛？
      └─ 先检查 lota_data/matches/live.json
```

### 缓存文件格式速查

| 文件 | 读取方式 | 内容结构 |
|------|---------|---------|
| `lota_data/matches/YYYY-MM-DD.json` | `Read` 直接读 | matches 数组，每个元素含 `lota_id`, `home_name`, `away_name`, `league_name`, `match_time`, `state`, `score` 等 |
| `lota_data/matches/live.json` | `Read` 直接读 | 同上结构，仅含 state=1 的比赛 |
| `lota_data/lota_compact_fet/Lota{id}.json` | `Read` 直接读 | `{compact_fet: "...", score: "...", lota_id: "..."}` |
| `lota_data/fetch_metadata.json` | `Read` 直接读 | `{lota_id: 时间戳}` — 记录每场比赛上次更新时间 |

> **关键原则**：`Read` 工具直接读本地文件无需任何 API 消耗。始终优先用 Read 检查缓存文件，确认缺失后才调用 bash 脚本。

## 常用命令速查

### 比赛列表查询 (lota_football_matches.sh)


```bash
# 指定日期的所有比赛（日期必须显式传入，格式 YYYY-MM-DD）
bash lota_football_matches.sh today 2026-04-18

# 竞彩 / 北单比赛
bash lota_football_matches.sh jingcai 2026-04-18
bash lota_football_matches.sh beidan 2026-04-18

# 日期范围
bash lota_football_matches.sh range 2026-04-01 2026-04-07

# 根据 lota_id 获取单场基础信息
bash lota_football_matches.sh match Lota123456

# 获取某日所有联赛列表
bash lota_football_matches.sh leagues 2026-04-18
```
**选项**:
- `--pretty`：格式化 JSON 输出（需 `jq`）
- `--raw`：原始 JSON 输出
- `--output=<file>`：保存到文件

## 特征报告查询 (lota_compact_fet.sh)
```bash
# 获取纯文本特征报告（推荐，直接供 LLM 阅读）
bash lota_compact_fet.sh Lota123456 --plain

# 获取完整 JSON（含元数据）
bash lota_compact_fet.sh Lota123456
```

## API 端点说明

### 比赛列表接口
```text
GET /predictions/api/v2/matches/
```
参数：

date : 日期 (YYYY-MM-DD)

lota_id : 单场比赛ID

start_date, end_date : 日期范围

is_jingcai : true/false

is_beidan : true/false

league : 联赛名称模糊匹配

limit, offset : 分页


### 特征文本接口
```text
GET /predictions/api/v2/compact-fet/
```

参数：

lota_id : 比赛ID（必需）

返回 JSON 结构中，特征文本位于 data.compact_fet 字段。

## 典型工作流
当用户询问某场比赛详情时（例如”曼联 vs 曼城”或”昨天的竞彩比赛”），应按以下步骤操作：

1. 确定日期（如用户未明确，根据上下文推断，生成 YYYY-MM-DD 格式）。

2. **优先读取本地缓存**：用 `Read` 工具直接读 `lota_data/matches/YYYY-MM-DD.json`（路径在 skills/lota_data/ 下，绝对路径根据环境拼接）。

3. 若缓存文件不存在或为空，再调用 `lota_football_matches.sh` 获取候选列表（使用 `today <date>`、`jingcai <date>` 或 `range`）。

4. 在匹配列表中根据队名/时间找到目标比赛的 `lota_id`。

5. **优先读取本地缓存**：用 `Read` 工具读 `lota_data/lota_compact_fet/Lota{id}.json`，取 `.compact_fet` 字段。

6. 若缓存文件不存在，再调用 `lota_compact_fet.sh <lota_id> --plain` 获取特征报告。

7. 将特征报告内容与用户问题结合进行分析回答。

## 注意事项
所有日期参数必须显式提供：脚本不会自动计算“今天”、“昨天”，由调用方（LLM）根据当前日期生成 YYYY-MM-DD 格式传入。

批量获取原则：避免对每个可能的比赛单独调用 match，应先获取列表再本地匹配。

特征报告包含比分时：完场比赛（state=6）的 score 字段非空，可据此判断历史数据。

Windows 用户：请在 Git Bash 或 WSL 中执行脚本。

## 错误处理
缺少 lota_id 或日期参数时，脚本会输出错误信息并退出。

API 返回 404 时，响应体包含 {"error": "..."}，脚本会原样输出，可从中获取失败原因。

## 认证
支持通过 Header X-API-Key 传递 API 密钥，脚本已内置。

## 定时任务
为了方便自动获取未来24小时比赛数据，项目提供了批处理脚本 `lota_fetch_future_24h.sh`。

### 功能
- 获取今天和明天的比赛列表，保存到 `lota_data/matches/YYYY-MM-DD.json`
- 筛选未来24小时未开始的比赛保存到 `lota_data/matches/live.json`
- 根据比赛类型智能更新特征报告：
  - 竞彩比赛 (jingcai_number非空): 每30分钟更新一次
  - 北单比赛 (beidan_number非空): 每1小时更新一次
  - 其他比赛: 每1.5小时更新一次
- 内置频率限制（每秒最多2个请求）
- 自动记录上次更新时间，避免重复请求

### 使用方法
```bash
# 确保已设置 API 密钥
export LOTA_API_KEY="your_api_key_here"

# 执行脚本（默认只更新未开始的比赛）
bash lota_fetch_future_24h.sh

# 强制更新所有比赛（包括已开始的）
bash lota_fetch_future_24h.sh --force-update-all

# 干运行模式（仅显示将要执行的操作）
bash lota_fetch_future_24h.sh --dry-run
```

### 设置定时任务（Cron）
建议每15分钟执行一次，以确保竞彩比赛能及时更新（30分钟间隔）。

编辑 crontab：
```bash
crontab -e
```

添加以下行（根据你的环境调整路径和密钥）：
```bash
# 每15分钟执行一次
*/15 * * * * export LOTA_API_KEY="your_api_key_here" && cd /path/to/skills/lota_football && bash lota_fetch_future_24h.sh >> /path/to/lota_data/cron.log 2>&1
```

### 日志
脚本会输出带有时间戳的日志，可以重定向到文件进行监控。

## 目录结构

> **关联脚本**：本节描述 `lota_fetch_future_24h.sh` 自动脚本生成的数据目录结构。关于脚本的详细功能和使用方法，请参阅上文的[定时任务](#定时任务)章节。

自动脚本 `lota_fetch_future_24h.sh` 生成以下目录结构：

```
lota_data/
├── matches/                    # 比赛列表数据
│   ├── YYYY-MM-DD.json        # 指定日期的所有比赛（如 2026-04-23.json）
│   └── live.json               # 未来24小时未开始的比赛（state=1）
├── lota_compact_fet/           # 特征报告数据（每场比赛一个文件）
│   ├── Lota123456.json         # 单场比赛的特征报告（JSON格式）
│   └── Lota789012.json
├── fetch_metadata.json         # 元数据，记录每场比赛上次更新时间戳
└── cron.log                    # 定时任务日志（如果配置了重定向）
```

**文件说明**：
- `matches/YYYY-MM-DD.json`：纯 matches 数组（`[{lota_id, home_name, ...}, ...]`），由脚本从当天匹配中按日期筛选后保存。非完整 API 响应格式。
- `matches/live.json`：纯 matches 数组，仅含未来24小时内未开始的比赛（`state == 1`）
- `lota_compact_fet/Lota{id}.json`：单场比赛的完整特征报告，包含 `compact_fet` 文本字段和元数据
- `fetch_metadata.json`：JSON对象，键为 `lota_id`，值为上次更新时间戳（Unix时间戳，秒）


## 数据结构说明

### 比赛列表（matches/YYYY-MM-DD.json）
> **实际格式为纯 matches 数组**（由 `lota_fetch_future_24h.sh` 写入），不是完整 API 响应。
```json
[
  {
    "lota_id": "Lota123456",
    "home_name": "主队名",
    "away_name": "客队名",
    "league_name": "联赛名",
    "match_time": "2026-04-23 20:00:00",
    "score": "2:1",
    "match_type": "N/A",
    "state": 6,
    "state_name": "完场",
    "beidan_number": "27",
    "jingcai_number": null
  }
]
```

### 特征报告（lota_compact_fet/Lota123456.json）
```json
{
  "success": true,
  "lota_id": "Lota123456",
  "score": "2:1",
  "compact_fet": "▋联赛类型: 巴西甲｜地区: 南美洲...（详细特征文本）",
  "metadata": {
    "length": 5780,
    "character_count": 5780,
    "line_count": 207,
    "fet_version": "compact_v1"
  },
  "api_info": {
    "version": "v2",
    "authenticated": true,
    "rate_limit": {
      "daily_limit": 50,
      "monthly_limit": 1500
    }
  }
}
```

### 元数据（fetch_metadata.json）
```json
{
  "Lota123456": 1713811200,
  "Lota789012": 1713811300
}
```

## 技术支持
获取 API 密钥或技术支持，请联系微信：mslota_com 或 researcher22。