# openclaw-plugin-grinders-farm

**Languages:** [English](#english) · [中文](#中文)

OpenClaw plugin for **Grinder's Farm**: `/farm` command, `grinders_farm` tool, local save, and multi-channel push.

![Farm preview](../docs/images/demo-farm.png)

---

## English

### Before you install this plugin

1. Install **Node.js** (with `npm`).
2. Install the **game package** first — the plugin runs the game CLI under the hood:

```bash
npm install -g grinders-farm
```

3. Ensure **OpenClaw** is installed and you can run `openclaw` in a terminal.

Without `grinders-farm`, slash commands and the tool will fail.

After install, use `/farm ...` in chat to play, and enable auto-advance with push.

### Install the plugin

```bash
openclaw plugins install openclaw-plugin-grinders-farm --dangerously-force-unsafe-install
```

Then **restart the OpenClaw Gateway** and confirm `openclaw plugins inspect grinders-farm` shows `Status: loaded`.

Verify:

```bash
openclaw plugins inspect grinders-farm
```

### Recommended flow

1. In each target channel, send once:

```text
/farm farm
```

2. Start auto-advance:

```text
/farm start
```

3. Stop:

```text
/farm stop
```

Notes:

- `start` advances **one in-game day every 20 minutes**
- Pushes go to all bound channels (channels that sent `/farm ...` at least once)

### Configuration

In OpenClaw plugin config:

- `autoStartWorkerOnGatewayBoot` — auto-start worker when Gateway boots
- `imageServerPort` — local farm PNG HTTP port
- `gameRoot` — manual repo root if auto-detection fails

Minimal example:

```json
{
  "plugins": {
    "entries": {
      "grinders-farm": {
        "enabled": true,
        "source": "openclaw-plugin-grinders-farm",
        "config": {
          "autoStartWorkerOnGatewayBoot": true
        }
      }
    }
  }
}
```

### Troubleshooting

**Command not available after install**

```bash
openclaw plugins inspect grinders-farm
```

If not `loaded`, restart Gateway.

**Installed plugin but still errors about `grinders-farm`**

Install the CLI: `npm install -g grinders-farm`, then restart Gateway.

**Push missing for a channel**

Run `/farm farm` in that channel once to bind, then `/farm start`.

**Cannot find `grinders-farm` binary**

Set env and restart Gateway:

- `GRINDERS_FARM_ROOT`
- `GRINDERS_FARM_CLI_BIN`

---

## 中文

`Grinder's Farm` 的 OpenClaw 插件。  
安装后你可以直接在聊天里使用 `/farm ...` 命令游玩，并开启自动推进与多频道推送。

### 安装本插件之前

1. 本机已装 **Node.js**（含 `npm`）。
2. **先装主游戏包**（插件会调用其中的 CLI）：

```bash
npm install -g grinders-farm
```

3. 已安装 **OpenClaw**，终端里能执行 `openclaw`。

没有 `grinders-farm`，`/farm` 和工具调用会失败。

### 安装插件

```bash
openclaw plugins install openclaw-plugin-grinders-farm --dangerously-force-unsafe-install
```

安装后请**重启 OpenClaw Gateway**，并用 `openclaw plugins inspect grinders-farm` 确认 `Status: loaded`。

安装完成后，确认已加载：

```bash
openclaw plugins inspect grinders-farm
```

### 使用流程（推荐）

1. 在目标频道发送一次：

```text
/farm farm
```

2. 开始自动推进：

```text
/farm start
```

3. 停止自动推进：

```text
/farm stop
```

说明：

- `start` 固定每 **20 分钟**推进一天
- 会自动推送到所有已绑定频道（先发送过 `/farm ...` 的频道）

### 常用配置

你可以在 OpenClaw 的 plugin 配置里设置：

- `autoStartWorkerOnGatewayBoot`：Gateway 启动时是否自动启动推进
- `imageServerPort`：本地农场图片服务端口
- `gameRoot`：当自动定位失败时，手动指定项目根目录

最小配置示例：

```json
{
  "plugins": {
    "entries": {
      "grinders-farm": {
        "enabled": true,
        "source": "openclaw-plugin-grinders-farm",
        "config": {
          "autoStartWorkerOnGatewayBoot": true
        }
      }
    }
  }
}
```

### 常见问题

### 插件已安装但命令不可用

先检查：

```bash
openclaw plugins inspect grinders-farm
```

如果不是 `loaded`，重启 Gateway 后再试。

### 插件装了但仍提示找不到 grinders-farm

先执行 `npm install -g grinders-farm`，再重启 Gateway。

### 自动推送没有发到某个频道

在该频道先执行一次 `/farm farm` 完成绑定，再执行 `/farm start`。

### 找不到 `grinders-farm` 可执行文件

可设置环境变量：

- `GRINDERS_FARM_ROOT`
- `GRINDERS_FARM_CLI_BIN`

然后重启 Gateway。
