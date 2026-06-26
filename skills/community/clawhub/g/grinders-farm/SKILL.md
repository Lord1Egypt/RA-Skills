---
name: grinders-farm
description: "Requires grinders-farm CLI + openclaw-plugin-grinders-farm before use. Maps intents to grinders_farm. 使用前需先安装 grinders-farm 与 openclaw-plugin-grinders-farm。"
metadata: { "openclaw": { "emoji": "🌾", "requires": { "bins": ["npx"] } } }
command-dispatch: tool
command-tool: grinders_farm
disable-model-invocation: false
---

# Grinder's Farm

**Languages:** [English](#english) · [中文](#中文)

![Farm preview (4×5 grid, four crop types)](docs/images/demo-farm.png)

---

## English

This skill maps user chat into **exactly one** `grinders_farm` tool call.

### Prerequisites (install before this skill works)

The `grinders_farm` tool is provided by the game CLI and the OpenClaw plugin. **Install both from npm first**, then install this skill from ClawHub:

```bash
npm install -g grinders-farm
openclaw plugins install openclaw-plugin-grinders-farm --dangerously-force-unsafe-install
```

Restart the OpenClaw Gateway after installing the plugin. Without these packages, `/farm` and `grinders_farm` will not run.

### Install this skill (optional but recommended for NL)

After the two packages above:

```bash
openclaw skills install grinders-farm
```

### How users play (after setup)

- **Slash commands (always works once the plugin is loaded):** in Telegram / WebChat / etc., send  
  `/farm <command>` — examples: `/farm farm`, `/farm plant carrot A1`, `/farm help`.  
  The part after `/farm` is the same command string you would pass to `grinders-farm-oneshot`.
- **Natural language (this skill):** when the skill is installed and the agent is allowed to use tools, the user can say things like “plant carrot at A4”; you should map that to `grinders_farm` with `command: "plant carrot A4"`.
- **This skill does not replace the plugin or the `grinders-farm` package** — it only helps choose the right tool arguments.

### Rules

1. While playing the farm, always use the `grinders_farm` tool.
2. Do not use shell/exec/cargo or other execution paths.
3. Do not only explain—execute (unless the user explicitly says not to).
4. Crops only: `carrot` `potato` `tomato` `pumpkin`.
5. Plot labels: `A1`–`D5` (rows A–D, columns 1–5).

### Allowed commands

- `farm`
- `plant <crop> <pos>`
- `water [pos]`
- `harvest [pos]`
- `shop`
- `sell`
- `inventory`
- `start`
- `stop`
- `reset`
- `help`

### Intent mapping (priority)

1. **Auto-advance**
   - "start auto" / "enable auto" → `start`
   - "stop auto" / "disable auto" → `stop`
2. **Plant**
   - plant intent + crop + position → `plant <crop> <pos>`
3. **Water**
   - water + position → `water <pos>`
   - water only → `water`
4. **Harvest**
   - harvest + position → `harvest <pos>`
   - harvest only → `harvest`
5. **Trade / info**
   - shop → `shop`
   - sell → `sell`
   - inventory → `inventory`
6. **Reset / help**
   - reset → `reset`
   - help → `help`
7. **Fallback**
   - farm-related but unclear → `farm`

### Output

1. Prefer the tool’s text as-is.
2. If there is a markdown table, output it without wrapping in a code fence.
3. Keep image URLs as plain clickable links (no backticks).
4. On failure: return the error first, then one example command.

### Examples

- "plant carrot at A4" → `command: "plant carrot A4"`
- "show farm" → `command: "farm"`
- "water all" → `command: "water"`
- "harvest A2" → `command: "harvest A2"`
- "start auto" → `command: "start"`
- "stop auto" → `command: "stop"`

### OpenClaw notes

- Plugin: `openclaw-plugin-grinders-farm`
- Run `/farm farm` once per channel to bind delivery.
- `/farm start` auto-advances (one day every **20 minutes**).
- `/farm stop` stops auto-advance.

### Local state files

- `~/.grinders-farm/farm.json`
- `~/.grinders-farm/farm.png`
- `~/.grinders-farm/auto.log`
- `~/.grinders-farm/openclaw-deliveries.json`

---

## 中文

此 Skill 的目标只有一个：把用户输入映射成**唯一明确**的 `grinders_farm` 命令并执行。

### 先决条件（使用本 skill 前必须先装）

`grinders_farm` 工具由**主游戏 CLI** 与 **OpenClaw 插件**一起提供。请**先全局安装这两个 npm 包**，再从 ClawHub 安装本 skill：

```bash
npm install -g grinders-farm
openclaw plugins install openclaw-plugin-grinders-farm --dangerously-force-unsafe-install
```

安装插件后请**重启 OpenClaw Gateway**。若未安装上述包，`/farm` 与 `grinders_farm` 无法运行。

### 再安装本 skill（想用自然语言时）

两个 npm 包装好后，再执行：

```bash
openclaw skills install grinders-farm
```

### 用户怎么玩（装好之后）

- **斜杠命令（插件加载后可用）：** 在 Telegram / WebChat 等里发  
  `/farm <子命令>`，例如 `/farm farm`、`/farm plant carrot A1`、`/farm help`。  
  `/farm` 后面这一段，与传给 `grinders-farm-oneshot` 的参数一致。
- **自然语言（本 skill）：** 用户说「在 A4 种胡萝卜」时，应映射为 `grinders_farm`，`command: "plant carrot A4"`。
- **本 skill 不能替代插件和主包** —— 只负责把聊天意图转成正确 tool 参数。

### 必须遵守

1. 用户在玩农场时，必须调用 `grinders_farm` tool。  
2. 不用 shell/exec/cargo 等其它执行路径。  
3. 不要只讲解不执行（除非用户明确说“先别执行”）。  
4. 作物只允许：`carrot` `potato` `tomato` `pumpkin`。  
5. 坐标格式固定：`A1`~`D5`（行 A-D，列 1-5）。

### 命令白名单（仅这些）

- `farm`
- `plant <crop> <pos>`
- `water [pos]`
- `harvest [pos]`
- `shop`
- `sell`
- `inventory`
- `start`
- `stop`
- `reset`
- `help`

### 意图映射（按优先级匹配）

命中后立即执行，不要多重猜测。

1. **自动推进**
   - “开启自动 / 开始挂机 / start auto” -> `start`
   - “停止自动 / 关掉挂机 / stop auto” -> `stop`
2. **种植**
   - 包含“种/种植/播种”且有作物+坐标 -> `plant <crop> <pos>`
3. **浇水**
   - “浇水”+坐标 -> `water <pos>`
   - 仅“浇水” -> `water`
4. **收获**
   - “收获”+坐标 -> `harvest <pos>`
   - 仅“收获” -> `harvest`
5. **交易/信息**
   - “商店/买什么” -> `shop`
   - “卖掉/出售” -> `sell`
   - “仓库/库存/背包” -> `inventory`
6. **重置/帮助**
   - “重置/重开” -> `reset`
   - “帮助/help” -> `help`
7. **兜底**
   - 农场相关但不够明确 -> `farm`

### 输出规则（避免歧义）

1. 工具返回内容优先，尽量原样呈现。  
2. 若含 markdown 表格，原样输出，不包代码块。  
3. 若含图片 URL，保持纯链接可点击，不加反引号。  
4. 命令失败时：先返回错误原文，再给一条可执行示例命令。

### 标准示例

- “在 A4 种胡萝卜” -> `command: "plant carrot A4"`
- “看农场” -> `command: "farm"`
- “全部浇水” -> `command: "water"`
- “收 A2” -> `command: "harvest A2"`
- “开自动” -> `command: "start"`
- “停自动” -> `command: "stop"`

### OpenClaw 使用要点

- 插件：`openclaw-plugin-grinders-farm`
- 先在每个目标频道执行一次 `/farm farm` 完成绑定
- 执行 `/farm start` 开始自动推进（固定 **20 分钟**/天）
- 执行 `/farm stop` 停止自动推进

### 本地状态文件

- `~/.grinders-farm/farm.json`
- `~/.grinders-farm/farm.png`
- `~/.grinders-farm/auto.log`
- `~/.grinders-farm/openclaw-deliveries.json`
