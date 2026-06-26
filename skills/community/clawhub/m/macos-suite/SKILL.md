---
name: macos-suite
version: "0.2.3"
description: "macOS 系统应用自动化：打开/读取/创建（Mail/Calendar/Reminders/Notes/Maps/Freeform/Photos/Weather/Stocks/Clock）。"
metadata: "{\"openclaw\":{\"os\":[\"darwin\"],\"requires\":{\"bins\":[\"python3\",\"osascript\"]}}}"
---

# macos-suite

macOS 本地应用对接技能（偏安全、可扩展）。通过 AppleScript / UI 自动化（System Events）/ URL Scheme / `open` 命令实现对系统应用的打开、读取与常用动作。

## 规范符合性（官方）

- Skill 目录以 `SKILL.md` 为核心（YAML frontmatter + 说明），并使用 `metadata` 单行 JSON 进行 gating（仅 darwin、需要 `python3/osascript`）。参见 OpenClaw 官方 Skills 规范：https://docs.openclaw.ai/tools/skills
- ClawHub 发布/安装以“文件 bundle + metadata”进行版本化管理，核心仍是 `SKILL.md`。参见官方 ClawHub 文档：https://docs.openclaw.ai/tools/clawhub

## ⚠️ 安全与权限

- 本技能会触发本机应用自动化：首次调用可能弹出“允许控制某某应用”的系统授权提示。
- 读取类操作不需要 `confirm=YES`，但可能触发系统隐私授权（例如 Mail/Notes/Reminders/Calendar/Photos）。
- 修改型操作默认需要显式确认参数（否则拒绝执行）：
  - `mail.send` / `calendar.add` / `reminders.add` / `notes.create`
  - `freeform.*`（绘图/排版通过 UI 自动化，会修改画板内容）
- 若缺少 `confirm=YES`，命令会返回 `needsConfirm=true` 的 JSON，提示用户确认并给出只读替代命令（agent 应转述并向用户发起确认）。
- Freeform 的 UI 自动化需要系统开启“辅助功能/自动化”权限；若被拦截，命令返回 JSON 中会包含 `hint` 指引路径。

## 常见问题（权限与故障排查）

### 1) 首次调用弹权限框/被拒绝

在“系统设置 -> 隐私与安全性”中检查：
- 自动化：允许你运行脚本的宿主程序（例如 Terminal / iTerm / OpenClaw）控制 `System Events`，并允许控制 `Mail/Calendar/Reminders/Notes/Freeform` 等目标应用
- 辅助功能：如使用 Freeform 绘图/排版（UI 自动化），需要允许 Terminal/osascript 等具备“辅助功能”
- 日历/提醒事项/照片/通讯录/文件与文件夹：对应读取类能力若失败，通常是未授权导致

如果命令返回中出现 `osascript` 的 `not allowed to send keystrokes` / `不允许发送按键 (1002)`，就是“辅助功能”未开启。

### 2) Freeform 绘图/排版没反应或报错

Freeform 的绘图/排版命令依赖 UI 自动化（点击菜单 + 粘贴内容），请确认：
- Freeform 已能正常打开并在前台
- 你运行脚本的宿主程序已授予“辅助功能”与“自动化”权限

建议先跑一个最小验证：

```bash
python3 {baseDir}/scripts/main.py freeform.add_shape kind=rectangle confirm=YES
```

### 3) Reminders 读取不稳定

部分系统版本/隐私设置下 Reminders 的 AppleScript 读取会失败。此时建议启用 Shortcuts 兜底（见下方“Shortcuts 兜底”章节）。

## 使用方式

从 OpenClaw workspace 运行：

```bash
python3 {baseDir}/scripts/main.py <command> key=value key=value ...
```

输出为 JSON（便于 agent 解析）。

## Commands（摘要）

只读类：
- `mail.unread_count` / `mail.unread_list`
- `calendar.today` / `calendar.list`
- `reminders.lists` / `reminders.list`（读取不稳定时可用 Shortcuts 兜底）
- `notes.folders` / `notes.search`
- `photos.recent`（不支持时降级打开 Photos）
- `weather.current`（优先 Shortcuts；不配置则打开 Weather）
- `stocks.quote` / `stocks.batch`
- `stocks.history`（使用 stooq 返回近 N 个交易日历史数据）

修改类（均需 `confirm=YES`）：
- `mail.send` / `mail.draft`
- `calendar.add` / `reminders.add` / `notes.create`
- `freeform.new_board` / `freeform.add_text` / `freeform.add_sticky` / `freeform.add_shape` / `freeform.compose`

## Commands（详细示例）

### 打开应用 / 打开链接

```bash
python3 {baseDir}/scripts/main.py open app="Mail"
python3 {baseDir}/scripts/main.py open app="Maps"
python3 {baseDir}/scripts/main.py open url="http://maps.apple.com/?q=咖啡"
```

### 邮件（Mail）

```bash
# 未读数量 / 未读列表（读取）
python3 {baseDir}/scripts/main.py mail.unread_count
python3 {baseDir}/scripts/main.py mail.unread_list limit=20

# 创建草稿（不发送）
python3 {baseDir}/scripts/main.py mail.draft to="a@b.com" subject="主题" body="正文"

# 发送邮件（需要确认）
python3 {baseDir}/scripts/main.py mail.send to="a@b.com" subject="主题" body="正文" confirm=YES
```

可选参数：
- `cc`、`bcc`：逗号分隔
- `attachments`：逗号分隔的本地文件路径

### 备忘录（Notes）

```bash
python3 {baseDir}/scripts/main.py notes.folders
python3 {baseDir}/scripts/main.py notes.search query="购物" limit=10
python3 {baseDir}/scripts/main.py notes.create title="购物清单" body="牛奶\n鸡蛋" folder="备忘录" confirm=YES
```

### 提醒事项（Reminders）

```bash
python3 {baseDir}/scripts/main.py reminders.lists
python3 {baseDir}/scripts/main.py reminders.list list="提醒事项" limit=20
python3 {baseDir}/scripts/main.py reminders.add list="提醒事项" title="倒垃圾" notes="晚饭后" due="2026-03-03 20:30:00" confirm=YES
```

## Shortcuts 兜底（推荐）

macOS 的 Reminders/Weather 在不同系统版本与隐私设置下，AppleScript 读取可能不稳定。本技能支持用“快捷指令”兜底，做到稳定输出 JSON。

### Reminders 兜底：reminders.list

当 `reminders.list` 的 AppleScript 读取失败时，会尝试运行你指定的快捷指令：
- 通过参数：`shortcut="快捷指令名"`
- 或环境变量：`MACOS_SUITE_REMINDERS_SHORTCUT="快捷指令名"`

调用时会把如下 JSON 作为快捷指令输入（Shortcuts “获取快捷指令输入”拿到文件）：

```json
{"list":"提醒事项","limit":20,"includeCompleted":false}
```

快捷指令需要输出 JSON（文本即可）。推荐输出格式：

```json
{"items":[{"title":"倒垃圾","completed":false,"due":"2026-03-03 20:30:00"}]}
```

快捷指令搭建建议（动作顺序示例）：
- 获取快捷指令输入（会收到一个文件）
- 获取文件内容（文本）
- 从文本获取字典（把输入 JSON 转为字典）
- 获取提醒事项（可按清单过滤、按完成状态过滤、限制数量）
- 从列表创建字典数组（title/completed/due）
- 从字典创建 JSON（文本输出）

### 日历（Calendar）

```bash
python3 {baseDir}/scripts/main.py calendar.today limit=50
python3 {baseDir}/scripts/main.py calendar.list start="2026-03-03 00:00:00" end="2026-03-03 23:59:59" limit=50
python3 {baseDir}/scripts/main.py calendar.add calendar="家庭" title="家和钢琴课" start="2026-03-03 18:00:00" end="2026-03-03 19:00:00" location="XX琴行" notes="提前10分钟出门" confirm=YES
```

时间格式建议：
- `YYYY-MM-DD HH:MM:SS`（macOS AppleScript 可直接解析）

### 地图（Maps）

```bash
python3 {baseDir}/scripts/main.py maps.search query="北京三里屯停车场"
python3 {baseDir}/scripts/main.py maps.directions saddr="我家" daddr="北京南站" mode="d"
```

`mode`：
- `d` 驾车 / `w` 步行 / `r` 公交

### 其他应用（按需打开）

```bash
python3 {baseDir}/scripts/main.py photos.open
python3 {baseDir}/scripts/main.py photos.recent limit=20
python3 {baseDir}/scripts/main.py freeform.open
python3 {baseDir}/scripts/main.py freeform.new_board title="项目看板" confirm=YES
python3 {baseDir}/scripts/main.py freeform.add_text text="标题\n- 要点1\n- 要点2" confirm=YES
python3 {baseDir}/scripts/main.py freeform.add_sticky text="TODO：联系供应商" confirm=YES
python3 {baseDir}/scripts/main.py freeform.add_shape kind=rectangle confirm=YES
python3 {baseDir}/scripts/main.py freeform.compose file="{baseDir}/examples/freeform.json" confirm=YES
python3 {baseDir}/scripts/main.py weather.open
python3 {baseDir}/scripts/main.py weather.current shortcut="你的天气快捷指令名"
python3 {baseDir}/scripts/main.py clock.open
python3 {baseDir}/scripts/main.py stocks.open symbol="AAPL"
python3 {baseDir}/scripts/main.py stocks.quote symbol="AAPL"
python3 {baseDir}/scripts/main.py stocks.quote symbol="600519"
python3 {baseDir}/scripts/main.py stocks.batch symbols="AAPL,600519,00700"
python3 {baseDir}/scripts/main.py stocks.history symbol="AAPL" range=1y
```

#### 无边记（Freeform）绘图与排版

- 这些命令通过 UI 自动化完成（System Events 点击菜单 + 粘贴内容），需要系统开启“辅助功能”权限。
- `freeform.compose` JSON 示例：

```json
{
  "boardTitle": "项目看板",
  "items": [
    {"type": "text", "text": "标题\\n- 要点1\\n- 要点2"},
    {"type": "sticky", "text": "TODO：联系供应商"},
    {"type": "shape", "kind": "rectangle"},
    {"type": "shape", "kind": "arrow"}
  ]
}
```

#### 用无边记“绘制”走势图（建议）

本技能暂不支持把 PNG 图片直接插入 Freeform。要在无边记里呈现“走势图”，建议用 `stocks.history` 拉取数据后生成文本火花线（sparkline/ASCII 图），再用 `freeform.add_text` 插入到画板中。

最小流程：

```bash
python3 {baseDir}/scripts/main.py stocks.history symbol="AAPL" range=1y
python3 {baseDir}/scripts/main.py freeform.new_board title="AAPL 今年走势" confirm=YES
python3 {baseDir}/scripts/main.py freeform.add_text text="(把你生成的文本走势图粘贴在这里)" confirm=YES
```
