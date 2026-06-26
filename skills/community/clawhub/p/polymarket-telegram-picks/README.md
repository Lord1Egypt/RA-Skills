# Polymarket 每日 NBA 赔率 → AI 分析 → Telegram 推送（OpenClaw Skill）

本仓库是一个 **OpenClaw Skill**，实现：每天中国时间 8 点拉取 Polymarket **当日、未开赛的 NBA 比赛**赔率，经 AI 分析后，将「值得下注」的推荐推送到你的 Telegram。

## 项目结构

```
polymarket-telegram-picks/
├── SKILL.md                    # 技能说明与调用方式（OpenClaw 必读）
├── README.md                   # 本说明与部署流程
├── config/
│   ├── config.example.json     # 配置示例（复制为 config.json 并填写）
│   └── config.json             # 实际配置（勿提交到版本库）
└── scripts/
    ├── fetch_polymarket.py     # 拉取当日、未开赛的 NBA 比赛与赔率
    ├── send_telegram.py        # 将文本推送到 Telegram
    └── run_daily.py            # 一键执行：拉取 + 推送（可选用于 crontab）
```

## 依赖

- Python 3.8+
- 无需额外 pip 包（仅用标准库 `urllib.request`、`json` 等）

## 配置

### 1. Telegram

- 在 Telegram 中找 **@BotFather** 创建 Bot，获得 `TELEGRAM_BOT_TOKEN`。
- 与你的 Bot 先发一条消息（例如 `/start`），然后访问（把 `BOT_TOKEN` 换成你的 token）：
  `https://api.telegram.org/bot<BOT_TOKEN>/getUpdates`
  在返回的 JSON 里找到 `message.chat.id`，即为 `TELEGRAM_CHAT_ID`。

### 2. 配置方式二选一

- **环境变量**（推荐，便于 OpenClaw/cron 使用）：
  - `TELEGRAM_BOT_TOKEN`
  - `TELEGRAM_CHAT_ID`
- **配置文件**：复制 `config/config.example.json` 为 `config/config.json`，填入上述两个字段（键名可用 `telegram_bot_token` / `telegram_chat_id`）。

## 在 OpenClaw 上部署与使用

### 1. 安装 Skill

将本目录放到 OpenClaw 的 Skills 目录下，任选一种：

- **工作区 Skills**（项目内使用）  
  复制到当前工作区的 skills 目录，例如：
  ```bash
  cp -r polymarket-telegram-picks /path/to/your/openclaw/workspace/skills/
  ```
  若使用 `openclaw.json` 的 `skills.load.extraDirs`，则把「本目录的父路径」加入，例如：
  ```json
  "skills": {
    "load": {
      "extraDirs": ["/path/to/polymarket-telegram-picks的父目录"]
    }
  }
  ```
  这样 OpenClaw 会扫描到 `polymarket-telegram-picks` 下的 `SKILL.md`。

- **本地/全局 Skills**  
  复制到 `~/.openclaw/skills/`：
  ```bash
  cp -r polymarket-telegram-picks ~/.openclaw/skills/
  ```

### 2. 注入 Telegram 配置（可选）

若用配置文件，确保 OpenClaw 运行时可访问到该目录下的 `config/config.json`。  
若用环境变量，可在 `~/.openclaw/openclaw.json` 的 `skills.entries` 里为本 skill 单独加 `env`，例如：

```json
"skills": {
  "entries": {
    "polymarket-telegram-picks": {
      "enabled": true,
      "env": {
        "TELEGRAM_BOT_TOKEN": "你的 token",
        "TELEGRAM_CHAT_ID": "你的 chat_id"
      }
    }
  }
}
```

（若 skill 名称与目录名不一致，以 `SKILL.md` 里 `name` 为准。）

### 3. 刷新 Skills

- 若开启了 `skills.load.watch`，保存/复制好文件后等待几秒即可。
- 或重启 OpenClaw Gateway，或按文档执行「刷新 skills」操作。

### 4. 手动触发一次

在 OpenClaw 对话里对助手说，例如：

- 「执行今日 Polymarket 赔率分析并推送到 Telegram」
- 「Polymarket 每日推荐」
- 「请执行今日 Polymarket 分析并推送到 Telegram」

助手会按 `SKILL.md` 的说明：运行 `scripts/fetch_polymarket.py` → 根据输出做 AI 分析 → 再运行 `scripts/send_telegram.py` 把推荐发到你的 Telegram。

### 5. 每天中国时间 8 点自动执行（OpenClaw Cron）

在装有 OpenClaw 的机器上执行（时区按你当前环境，下面用 `Asia/Shanghai` 表示中国时间）：

```bash
openclaw cron add --name "Polymarket每日推送" \
  --cron "0 8 * * *" \
  --session main \
  --message "请执行今日 Polymarket 赔率分析并推送到 Telegram"
```

若你的 OpenClaw 支持为 cron 指定时区，可加上，例如：

```bash
openclaw cron add --name "Polymarket每日推送" \
  --cron "0 8 * * *" \
  --tz "Asia/Shanghai" \
  --session main \
  --message "请执行今日 Polymarket 赔率分析并推送到 Telegram"
```

这样每天 8 点会向主会话发一条上述消息，助手会执行本 skill 的流程并推送到 Telegram。

### 6. 不用 OpenClaw、仅用系统 Crontab（仅推送原始摘要）

若你只想「每天 8 点拉取 Polymarket 并直接把原始摘要推到 Telegram」（不做 AI 分析），可用本仓库自带的脚本 + 系统 cron：

```bash
# 中国时间 8:00 = UTC 0:00（冬令时）或 UTC 1:00（夏令时），请按你服务器时区调整
0 0 * * * TELEGRAM_BOT_TOKEN=xxx TELEGRAM_CHAT_ID=xxx POLYMARKET_DAILY_RAW_ONLY=1 /usr/bin/python3 /path/to/polymarket-telegram-picks/scripts/run_daily.py
```

此时不会经过 AI，推送的是 `fetch_polymarket.py` 的原始摘要。若要 AI 分析，请使用 OpenClaw 的定时任务（上面第 5 步）。

## 小结

| 步骤 | 说明 |
|------|------|
| 1 | 复制本目录到 OpenClaw 的 skills 目录或配置 extraDirs |
| 2 | 配置 `TELEGRAM_BOT_TOKEN`、`TELEGRAM_CHAT_ID`（环境变量或 config.json） |
| 3 | 刷新/重启 OpenClaw，使 skill 被加载 |
| 4 | 对话中触发「今日 Polymarket 分析并推送到 Telegram」做一次验证 |
| 5 | 用 `openclaw cron add` 添加每天 8 点（中国时间）的定时任务 |

分析结论完全由 OpenClaw 助手根据当日赔率与上下文自行判断，本 skill 只负责拉取数据与推送，不保证任何投注建议。
