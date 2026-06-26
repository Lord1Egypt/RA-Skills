---
name: lark-meeting
description: 帮助用户预约会议室, 当用户需要预约会议室时执行此技能
---

# 预约会议室

通过本仓库脚本调用飞书会议室与日历能力完成**初始化**（层级 + 会议室列表）与**按忙闲自动预约**。依赖本机已配置且已登录的 `lark-cli` 及相应 API 权限。

## 仓库内配置文件（`conf/`）

| 文件 | 作用 |
|------|------|
| `meeting.json` | 城市/大厦/楼层与 `rooms` 顺序；预约脚本默认读取 |
| `meeting_room_blacklist.json` | **会议室黑名单**（初始化写列表、预约时再次过滤），可直接编辑；技能更新黑名单即改此文件 |

### `meeting_room_blacklist.json` 字段

与 `meeting.json` **同目录**（默认均为 `conf/`）。若文件不存在，脚本使用内置默认（等价于仓库内示例）。

| 字段 | 类型 | 说明 |
|------|------|------|
| `name_substrings` | 字符串数组 | 会议室**名称**包含其中**任一字串**则排除；设为 `[]` 可关闭名称规则 |
| `exclude_if_capacity_gt` | 整数或 `null` | 飞书返回的 `capacity` **大于**该值则排除；设为 `null` 可关闭人数规则（**预约阶段**配置里的 `rooms` 通常无 `capacity`，此项主要在**重新初始化**拉取会议室时生效） |
| `room_ids` | 字符串数组 | 显式按 `room_id` 排除 |

**维护方式：**用户说「不要某会议室 / 排除面试间 / 拉黑某 room_id」时，由 **AI 编辑** `conf/meeting_room_blacklist.json`（保持合法 JSON）。  
- 改 **名称 / room_id** 规则后，**无需重跑初始化**即可影响下次预约（预约脚本会读黑名单）。  
- 改 **容量**规则或希望 **从飞书重新拉全量列表** 时，在用户确认后**再执行一次** `meeting_init_processor.py`（同城市/大厦/楼层），以刷新 `meeting.json` 中的 `rooms`。

**权限提示：**若无法写入 `conf/`，可提示用户在终端授权，例如：`sudo chown -R $(whoami):staff <技能仓库>/conf/`（路径按实际技能目录替换）。

## 入口命令（在仓库根目录执行）

| 能力 | 命令 | 说明 |
|------|------|------|
| 初始化 | `python scripts/meeting_init_processor.py` | **交互**：按提示选城市 → 职场（大厦）→ 楼层。**非交互**：同时传 `--city`、`--workplace` 或 `--building`、`--floor`；写入 `meeting.json`，并按黑名单过滤 `rooms` |
| 预约 | `python scripts/meeting_processor.py --start-time <ISO> --end-time <ISO> --summary "<主题>"` | 按 `rooms` 顺序查忙闲；应用同目录黑名单后取首个空闲并创建日程 |

**初始化脚本参数：**`--top-n`、`--page-size`；非交互三项见上。**预约脚本参数：**`--description`、`--config`（默认 `conf/meeting.json`）、`--calendar-id`（默认 `primary`）。

**首次使用：**若未配置 `lark-cli`，先按 `lark-shared` 完成 `lark-cli config init` 与 `lark-cli auth login`。

## AI 工作方式

### 初始化

- **优先非交互**：用户已给出城市、大厦、楼层且名称不易歧义时，确认后执行：  
  `python scripts/meeting_init_processor.py --city "…" --building "…" --floor "…"`  
  匹配失败时脚本会打印参考列表（Top 10 等），再据报错收窄名称。
- **缺信息或易歧义**：请用户补全或自行交互运行初始化脚本。
- 成功后**可简述** `meeting.json` 关键信息（城市/楼层/会议室数量），并提醒可开始预约。

### 预约

- **时间：**默认东八区 `+08:00` 解析自然语言为 ISO（**精确到秒**），缺时长/结束须追问。
- **执行前**向用户一句话确认起止时间与主题。
- **约束：**单次时长 ≤ 4 小时；`meeting.json` 不存在时引导先初始化。

### 黑名单

- 按用户口述增删规则时，**直接改** `conf/meeting_room_blacklist.json`（与当前使用的 `meeting.json` 同目录；若用户自定义 `--config`，则黑名单为**该文件同目录**下的 `meeting_room_blacklist.json`）。
- 改完后预约立即生效；若用户依赖「容量」过滤或要重拉会议室列表，说明需**再跑一次初始化**。

## 示例话术

- 「用北京某某大厦 17 楼初始化」→ 确认无歧义后执行带 `--city` / `--building` / `--floor` 的非交互命令。
- 「明天下午 3 点会议室开周会」→ 解析 ISO + `--summary`，缺时长先问。
- 「别给我订面试间」→ 确认 `name_substrings` 含 `面试间`（默认已有）；若无则写入并说明已生效。

## 脚本说明

- `scripts/meeting_room_blacklist.py`：加载/解析黑名单规则（初始化与预约共用）。
- `scripts/meeting_init_processor.py`：写 `meeting.json`；黑名单路径固定为仓库内 `conf/meeting_room_blacklist.json`。
- `scripts/meeting_processor.py`：读 `meeting.json`；黑名单为 `config` 文件同目录的 `meeting_room_blacklist.json`。
- `scripts/lark_cli.py`：API 封装。

## 限制

- 依赖 `lark-cli` 可用及会议室/日历权限。
- 层级名称可能重名，非交互匹配失败时需用户改用更精确名称或交互初始化。
