# OpenClaw Session Cleanup Skill

一个面向 OpenClaw 的运维型 Skill，用来处理长时间运行后的 session 堆积、gateway 不稳定、browser control timeout、WebSocket 1006 abnormal closure，以及小规格 VPS 的资源压力问题。

仓库地址：
[https://github.com/NeoCh3n/openclaw-session-cleanup-skill](https://github.com/NeoCh3n/openclaw-session-cleanup-skill)

## 这个仓库现在符合 OpenClaw 生态的点

- 根目录提供 [`SKILL.md`](./SKILL.md)，这是 OpenClaw 原生识别的技能入口。
- 附带 `scripts/`、`templates/`、`docs/` 作为 skill 资源包。
- 可以直接放进 `~/.openclaw/skills/` 或 `<workspace>/skills/`。
- 后续也可以直接用 `clawhub publish` 发布到 ClawHub。

参考的官方文档：

- OpenClaw Skills 文档说明 skill 是“一个目录 + `SKILL.md`”，并从 `~/.openclaw/skills` 或 `<workspace>/skills` 加载。
- Creating Skills 文档给出的最小结构也是技能目录下放 `SKILL.md`。
- ClawHub 文档说明可以用 `clawhub publish <path>` 发布，用 `clawhub install <slug>` 安装。

## 目录结构

```text
.
├── SKILL.md
├── LICENSE
├── README.md
├── README.zh-CN.md
├── docs/
│   └── openclaw.session_cleanup_v1.md
├── scripts/
│   ├── install-cron-prune.sh
│   ├── install-to-openclaw.sh
│   ├── install-watchdog.sh
│   └── render-openclaw-config.sh
└── templates/
    ├── openclaw-watchdog.service
    ├── openclaw-watchdog.timer
    └── openclaw.json
```

## 新用户如何一键安装到自己的 OpenClaw

### 方式 1：从 GitHub 一键安装

直接运行：

```bash
curl -fsSL https://raw.githubusercontent.com/NeoCh3n/openclaw-session-cleanup-skill/main/scripts/install-to-openclaw.sh | bash
```

默认会把这个 skill 安装到：

```bash
~/.openclaw/skills/openclaw-session-cleanup
```

安装完成后，重新开始一个新的 OpenClaw session，或者重启 gateway 让它重新索引 skill。

### 方式 2：手动克隆后安装

```bash
git clone https://github.com/NeoCh3n/openclaw-session-cleanup-skill.git
cd openclaw-session-cleanup-skill
bash ./scripts/install-to-openclaw.sh
```

### 方式 3：作为 workspace skill 使用

如果你希望它只在当前 workspace 生效，把整个目录复制到：

```bash
<your-workspace>/skills/openclaw-session-cleanup
```

这符合 OpenClaw 官方推荐的 workspace skill 目录。

## 安装后如何使用

在 OpenClaw 中直接描述问题，例如：

- `我的 openclaw 跑几天后 gateway 会 1006 断开，帮我排查`
- `Sessions: 16 active, Agents: 6, browser control timeout，帮我稳定化`
- `帮我给 2GB VPS 配一套 openclaw 稳定运行方案`

也可以让它直接引导你执行：

- session prune / clear
- runtime config 调整
- cron 自动清理
- watchdog 安装
- browser 单实例约束
- swap 配置

## 附带资源

- [`SKILL.md`](./SKILL.md): OpenClaw 原生 skill 入口
- [`docs/openclaw.session_cleanup_v1.md`](./docs/openclaw.session_cleanup_v1.md): 详细排障/运维说明
- [`templates/openclaw.json`](./templates/openclaw.json): 推荐 runtime 配置
- [`templates/openclaw-watchdog.service`](./templates/openclaw-watchdog.service): watchdog service 模板
- [`templates/openclaw-watchdog.timer`](./templates/openclaw-watchdog.timer): watchdog timer 模板
- [`scripts/install-cron-prune.sh`](./scripts/install-cron-prune.sh): 定时 prune 安装脚本
- [`scripts/install-watchdog.sh`](./scripts/install-watchdog.sh): watchdog 安装脚本
- [`scripts/render-openclaw-config.sh`](./scripts/render-openclaw-config.sh): runtime 配置渲染脚本

## 发布到 ClawHub

如果你后续要把它发布到 OpenClaw 的公共技能仓库，可以按官方命令：

```bash
clawhub login
clawhub publish . --slug openclaw-session-cleanup --name "OpenClaw Session Cleanup" --version 1.0.0 --tags latest,openclaw,ops
```

或者后续更新时：

```bash
clawhub sync --all
```

## License

本项目使用 MIT License，见 [`LICENSE`](./LICENSE)。
