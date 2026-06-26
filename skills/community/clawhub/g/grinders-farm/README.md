# 🌿 Grinder's Farm

<p align="center">
  <img src="docs/images/demo-farm.png" alt="Grinder's Farm — 4×5 pixel farm grid (four crops, multiple growth stages)" width="444" />
</p>

<p align="center"><sub>Demo render · Rows A–D: carrot, potato, tomato, pumpkin · Columns: early → mature growth</sub></p>
<p align="center"><sub>示意图 · 行 A–D：胡萝卜、土豆、番茄、南瓜 · 列：生长阶段由早到晚</sub></p>

**Languages:** [English](#english) · [中文](#中文)

---

## English

A lightweight pixel-art farm sim: plant, water, harvest, sell, and fulfill orders.  
Play in the **terminal** (CLI only) or in **OpenClaw** chat (Telegram, WebChat, etc.).

### What you need (new users)

| Requirement | Why |
|---|---|
| **Node.js** (includes `npm`) | Runs the game and installs packages from npm. |
| **OpenClaw CLI + Gateway** | Only if you play **in chat**. The Gateway must be running so `/farm` reaches the plugin. |

### What each package does

| Package | Role |
|---|---|
| **`grinders-farm`** | The game + CLI. Provides `grinders-farm` (interactive) and `grinders-farm-oneshot` (one command). **Required** for both terminal and OpenClaw. |
| **`openclaw-plugin-grinders-farm`** | OpenClaw integration: registers the `/farm` slash command and the `grinders_farm` tool. **Required** for chat play. |
| **ClawHub skill `grinders-farm`** (optional) | Helps the **agent** map natural language to `grinders_farm` commands. Not required if you only use `/farm ...` manually. |

### Two ways to play

- **Terminal only** — no OpenClaw, no plugin, no skill:  
  `npm install -g grinders-farm` → run `grinders-farm` and type commands at the prompt (`farm`, `help`, …).

- **OpenClaw chat** — install **both** npm packages, **restart the Gateway**, then use `/farm …` in a channel (see Quick start). Optionally install the skill so the agent understands free-form chat.

### Features

- 4×5 grid, start with 50G
- Order system (bonus rewards)
- Dynamic market prices (supply feedback)
- Multi-channel push (Telegram, WebChat, etc.)
- Text view + PNG farm image

### Quick start (OpenClaw chat)

Do these **in order**:

1. **Install the game CLI** (always required):

```bash
npm install -g grinders-farm
```

2. **Install the OpenClaw plugin** (registers `/farm` and the tool):

```bash
openclaw plugins install openclaw-plugin-grinders-farm --dangerously-force-unsafe-install
```

3. **Restart the OpenClaw Gateway** so the plugin loads (required after install or upgrade).

4. *(Optional)* **Install the ClawHub skill** if you want natural-language play via the agent:

```bash
openclaw skills install grinders-farm
```

5. **Bind each chat channel**

In every channel where you want pushes, send once:

```text
/farm farm
```

6. **Auto-advance** (optional)

```text
/farm start
```

- One in-game day advances every **20 minutes**
- Pushes fan out to all bound channels

Stop:

```text
/farm stop
```

**Check it works:** `openclaw plugins inspect grinders-farm` should show `Status: loaded` and a recent version. If `/farm` does nothing, confirm the Gateway was restarted after installing the plugin.

### Commands

| Command | Description |
|---|---|
| `farm` / `status` | View farm |
| `plant <crop> <pos>` | Plant (e.g. `plant carrot A1`) |
| `water [pos]` | Water one cell or all |
| `harvest [pos]` | Harvest one cell or all ready crops |
| `shop` | Shop |
| `sell` | Sell inventory |
| `inventory` / `inv` | Inventory |
| `start` | Start auto-advance + push |
| `stop` | Stop auto-advance |
| `reset` | New game |
| `help` | Help |

### Crops

| Crop | Days | Seed | Base sell |
|---|---:|---:|---:|
| 🥕 Carrot | 5 | 5G | 11G |
| 🥔 Potato | 7 | 8G | 22G |
| 🍅 Tomato | 6 | 9G | 24G |
| 🎃 Pumpkin | 8 | 12G | 34G |

### Push & channels

- Bindings: `~/.grinders-farm/openclaw-deliveries.json`
- After `/farm start`, pushes go to all bound targets
- WebChat uses `chat.inject`; other channels use `openclaw message send`

### Local data

| Path | Purpose |
|---|---|
| `~/.grinders-farm/farm.json` | Save game |
| `~/.grinders-farm/farm.png` | Latest PNG |
| `~/.grinders-farm/auto.pid` / `auto.config.json` | Auto worker |
| `~/.grinders-farm/auto.log` | Auto log |
| `~/.grinders-farm/image-server.json` | Image server metadata |

### Development

```bash
npm install
npm run generate-tiles
npm run build
npm run dev
```

Plugin package:

```bash
cd openclaw-plugin
npm install
npm run build
```

### License

MIT

---

## 中文

轻量像素农场游戏：种地、浇水、收获、卖货、接订单。  
可在**终端**单独玩，也可在 **OpenClaw** 聊天里玩（Telegram、WebChat 等）。

### 你需要什么（新用户）

| 条件 | 说明 |
|---|---|
| **Node.js**（含 `npm`） | 运行游戏并从 npm 安装包。 |
| **已安装 OpenClaw 且 Gateway 在跑** | 仅在**聊天里**玩时需要；否则 `/farm` 到不了插件。 |

### 各个包是干什么的

| 包 | 作用 |
|---|---|
| **`grinders-farm`** | 游戏本体 + CLI，提供 `grinders-farm`（交互）和 `grinders-farm-oneshot`（单次命令）。**终端与 OpenClaw 都需要。** |
| **`openclaw-plugin-grinders-farm`** | OpenClaw 集成：注册 `/farm` 斜杠命令和 `grinders_farm` 工具。**只在聊天里玩时需要。** |
| **ClawHub skill `grinders-farm`**（可选） | 帮**智能体**把自然语言映射成 `grinders_farm` 命令。若你**只手动打** `/farm ...`，可以不装。 |

### 两种玩法

- **只玩终端**：不需要 OpenClaw、不需要插件、不需要 skill。  
  `npm install -g grinders-farm` → 运行 `grinders-farm`，在提示符下输入命令（`farm`、`help` 等）。

- **在 OpenClaw 里玩**：需要**两个 npm 包都装**，装完插件后**重启 Gateway**，再在频道里用 `/farm …`（见下文「3 分钟上手」）。需要自然语言时可再装 skill。

### 这款游戏有什么

- 4×5 农田网格，开局 50G
- 订单系统（完成后有额外奖励）
- 动态市场价格（卖得多会有压价反馈）
- 多渠道自动推送（Telegram / WebChat 等）
- 文本农场视图 + PNG 像素图

### 3 分钟上手（OpenClaw 聊天）

请**按顺序**做：

1. **安装主游戏 CLI**（始终需要）：

```bash
npm install -g grinders-farm
```

2. **安装 OpenClaw 插件**（注册 `/farm` 与工具）：

```bash
openclaw plugins install openclaw-plugin-grinders-farm --dangerously-force-unsafe-install
```

3. **重启 OpenClaw Gateway**（装完或升级插件后必须，否则命令不生效）。

4. *（可选）* **安装 ClawHub skill**，让智能体能听懂自然语言：

```bash
openclaw skills install grinders-farm
```

5. **在聊天里绑定渠道**

在你希望收到推送的每个频道里，先发一次：

```text
/farm farm
```

6. **开始自动推进**（可选）

```text
/farm start
```

- 固定每 **20 分钟**推进一天
- 自动推送到所有已绑定频道

停止自动推进：

```text
/farm stop
```

**自检：** 执行 `openclaw plugins inspect grinders-farm`，应看到 `Status: loaded` 与较新版本。若 `/farm` 没反应，先确认装插件后是否已重启 Gateway。

### 命令速查

| 命令 | 说明 |
|---|---|
| `farm` / `status` | 查看农场 |
| `plant <crop> <pos>` | 种植（例：`plant carrot A1`） |
| `water [pos]` | 浇水（不填位置则浇全部） |
| `harvest [pos]` | 收获（不填位置则收全部成熟作物） |
| `shop` | 查看商店 |
| `sell` | 出售仓库全部作物 |
| `inventory` / `inv` | 查看仓库 |
| `start` | 启动自动推进与自动推送 |
| `stop` | 停止自动推进 |
| `reset` | 重开一局 |
| `help` | 查看帮助 |

### 作物一览

| 作物 | 成熟天数 | 种子价 | 基础售价 |
|---|---:|---:|---:|
| 🥕 Carrot | 5 | 5G | 11G |
| 🥔 Potato | 7 | 8G | 22G |
| 🍅 Tomato | 6 | 9G | 24G |
| 🎃 Pumpkin | 8 | 12G | 34G |

### 游戏循环建议

1. 先看 `shop`，根据现金和订单选种子
2. `plant` 后每天 `water`
3. 成熟后 `harvest`，再 `sell`
4. 利用订单奖励和市场反馈，滚动扩大收益

### 推送与渠道说明

- 绑定文件：`~/.grinders-farm/openclaw-deliveries.json`
- 执行 `/farm start` 后，自动 fan-out 到所有已绑定目标
- WebChat 走 `chat.inject`，消息渠道走 `openclaw message send`

### 本地数据文件

| 路径 | 用途 |
|---|---|
| `~/.grinders-farm/farm.json` | 存档 |
| `~/.grinders-farm/farm.png` | 最新像素图 |
| `~/.grinders-farm/auto.pid` / `auto.config.json` | 自动推进进程信息 |
| `~/.grinders-farm/auto.log` | 自动推进日志 |
| `~/.grinders-farm/image-server.json` | 图片服务元数据 |

### 开发者

```bash
npm install
npm run generate-tiles
npm run build
npm run dev
```

插件开发构建：

```bash
cd openclaw-plugin
npm install
npm run build
```

### License

MIT
