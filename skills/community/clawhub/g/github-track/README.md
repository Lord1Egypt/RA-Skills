# GitHub Track

> 追踪 GitHub 仓库动态的 AI Agent 技能

持续追踪你关心的开源项目，不错过任何重要更新。

## 功能

- **Star 追踪** - 获取当前 star 数，与历史对比
- **Issues 追踪** - 查看最新 open/closed issues，过滤标签
- **PR 追踪** - 查看 open/merged/closed PRs
- **关键词搜索** - 搜索特定 issue/PR
- **变更对比** - 与上次记录对比，发现新增内容
- **定时报告** - 自动生成每日追踪报告

## 安装

```bash
# 克隆仓库
git clone https://github.com/your-repo/github-track.git
cd github-track

# 或使用 ClawHub 安装
clawhub install github-track
```

## 使用方式

### 追踪仓库

```bash
# 添加追踪
python3 scripts/track.py add --owner anthropics --repo claude-code

# 查看列表
python3 scripts/track.py list

# 刷新数据
python3 scripts/track.py refresh --owner anthropics --repo claude-code
```

### 关键词搜索

```bash
# 搜索 issues
python3 scripts/track.py search-issue --owner anthropics --repo claude-code --keyword "PreToolUse"

# 搜索 PRs
python3 scripts/track.py search-pr --owner anthropics --repo claude-code --keyword "hook"
```

### 查看详情

```bash
# 查看 Issue
python3 scripts/track.py show-issue --owner anthropics --repo claude-code --number 123

# 查看 PR
python3 scripts/track.py show-pr --owner anthropics --repo claude-code --number 456
```

### 定时任务

```bash
# 添加 cron 任务（每天 10:00 执行）
crontab -e
# 0 10 * * * /path/to/github-track/scripts/daily-report.sh
```

或使用 systemd timer（已包含配置）:

```bash
cp scripts/github-track.service /etc/systemd/system/
cp scripts/github-track.timer /etc/systemd/system/
systemctl daemon-reload
systemctl enable github-track.timer
```

## 配置

### GitHub Token（可选）

在 `~/.openclaw/workspace/TOOLS.md` 中添加：

```markdown
### GitHub
- GITHUB_TOKEN: your_github_personal_access_token
```

获取 Token: https://github.com/settings/tokens

### 追踪配置

配置存储在 `~/.openclaw/workspace/memory/github-track-config.json`

## 项目结构

```
github-track/
├── SKILL.md              # 技能文档
├── scripts/
│   ├── track.py          # 主追踪脚本
│   └── daily-report.sh   # 每日报告脚本
└── README.md
```

## License

MIT
