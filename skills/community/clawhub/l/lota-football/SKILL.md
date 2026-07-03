---
name: lota-football
version: v2.1.0
description: 查询足球比赛列表和单场特征报告。世界杯历史比赛免费访问。包含 AI Agent 投注分析提示词（引导词/数据提示词/决策框架/输出格式）。
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

## 世界杯历史比赛免费访问 🆓

已结束的世界杯比赛（`league_name` = `"世界杯"` 或 `"世界杯附"`）**无需 API Key 即可免费访问** compact-fet 特征报告。

### 机制
- 服务端维护 Redis 白名单 (`cf:wl:ids`)，自动收录已结束的世界杯比赛 lota_id
- 白名单比赛请求**不消耗任何 API 配额**，绕过 `free_compact_fet` 每日 50 次限制
- **仅受 IP 频率限制**：每个 IP 每 60 秒最多 10 次请求
- 其他比赛仍需 API Key 或使用免费额度（50次/天）

### 使用方式
```bash
# 无需 API Key 即可查询世界杯历史完场比赛
bash lota_compact_fet.sh Lota123456 --plain
```

> **注意**：仅 state=6（完场）的世界杯比赛在白名单中。进行中或未开始的世界杯比赛仍需 API Key。

---

## AI Agent 比赛分析指南

本技能提供的 compact_fet 特征文本可直接作为 AI 大模型的输入。以下是推荐的 prompt 结构。

### 角色设定

```
你是足球数据分析师。根据比赛数据、赔率走势、历史规律，独立给出每场比赛的分析结论。
```

### 数据字段说明

compact_fet 是一段纯文本，以 `▋` 标记各小节标题。典型包含以下信息：

- **联赛/球队/时间/排名/身价** — 比赛基本面
- **公平赔率（模型推算）** — 欧赔理论值参考
- **Pinnacle 欧赔走势** — 初盘→终盘变化
- **Pinnacle 亚盘+水位** — 让球盘口及水位变化
- **皇冠大小球盘口** — 总进球盘口预期
- **Betfair 买卖方向** — 市场资金流向
- **离散赔率** — 多家庄赔率分歧度

实际内容因比赛数据源而异，以 API 返回为准。

### 分析框架

```
## 分析框架

1. 先看基本面：联赛级别、球队排名、主客场差异
2. 再看市场：欧赔 vs 公平盘偏差、亚盘水位方向、大小球预期
3. 从三个维度给出结论：
   - 胜平负倾向：欧盘概率 vs 公平盘偏差
   - 盘口方向：让球方向 + 水位走势
   - 进球预期：总进球模型 vs 盘口位置
4. 优先关注偏差明确（>5%概率差）、水位稳定的场次
5. 无明显信号的比赛直接标记 skip
```

### 输出格式

每场比赛输出一个独立分析区块，**必须包含 lota_id**：

```
```analysis
lota_id: Lota4459820
胜平负倾向: H
亚盘方向: H
大小球倾向: over
关键信号: 欧赔主胜概率比公平盘高6%, 亚盘水位稳定在0.82
信心: 中
```
```

信号不明确的比赛：

```
```analysis
lota_id: Lota4460938
结论: skip
原因: 多维度信号不一致，无明确方向
```
```

**规则**：
1. 每场比赛一个 ` ```analysis ``` ` 区块
2. lota_id 必须从比赛数据中原样复制
3. 倾向值：胜平负用 `H/D/A`，亚盘用 `H/A`，大小球用 `over/under`
4. 无明确信号时输出 skip，不强行给结论

### 完整 Prompt 组装示例

```
{角色设定}

## 比赛数据（共 N 场）

## 比赛 1: 主队A vs 客队B
  联赛: 世界杯 | 时间: 2026-07-02 20:00:00
  lota_id: Lota123456

{compact_fet 特征文本 — 通过 bash lota_compact_fet.sh Lota123456 --plain 获取}

---
## 比赛 2: ...
{...}

{分析框架}

{输出格式}
```

## 技术支持
获取 API 密钥或技术支持，请联系微信：mslota_com 或 researcher22。