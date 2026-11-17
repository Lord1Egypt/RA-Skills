# 安装命令 (install)

> 安装 SKILL.md 到各平台 skills 目录

## 命令列表

| 命令 | 说明 |
|------|------|
| `kugou-cli install` | 显示平台选择提示 |
| `kugou-cli install --all` | 安装 SKILL.md 到所有平台 |
| `kugou-cli install --claude` | 安装到 Claude skills 目录 |
| `kugou-cli install --mavis` | 安装到 Mavis skills 目录 |
| `kugou-cli install --hermes` | 安装到 Hermes skills 目录 |
| `kugou-cli install --openclaw` | 安装到 Openclaw skills 目录 |
| `kugou-cli install --codex` | 安装到 Codex skills 目录 |
| `kugou-cli install --workbuddy` | 安装到 Workbuddy skills 目录 |

---

## 详细用法

```bash
kugou-cli install                    # 显示平台选择提示
kugou-cli install --all              # 安装到所有平台
kugou-cli install --claude           # 仅安装到 Claude
kugou-cli install --hermes --claude  # 安装到 Hermes 和 Claude
```

**参数**:
- `--claude`: 安装到 `~/.claude/skills/kugou-skill/`
- `--mavis`: 安装到 `~/.mavis/skills/kugou-skill/`
- `--hermes`: 安装到 `~/.hermes/skills/kugou-skill/`
- `--openclaw`: 安装到 `~/.openclaw/skills/kugou-skill/`
- `--codex`: 安装到 `~/.codex/skills/kugou-skill/`
- `--workbuddy`: 安装到 `~/.workbuddy/skills/kugou-skill/`
- `--all`: 安装到以上所有平台

---

## 行为说明

- 无参数时输出"平台选择提示"，列出可用平台选项，不会进行任何安装操作
- 只会在目标平台的 skills 父目录存在时才安装（不自动创建父目录）
- npm 安装时会自动安装 SKILL.md
- `kugou-cli install` 命令用于手动重新安装或更新 SKILL.md

---

## 通用命令

| 命令 | 说明 |
|------|------|
| `kugou-cli --version` / `kugou-cli version` | 输出版本号（`--version` 是 root flag，`version` 是子命令，两者输出相同） |
| `kugou-cli --help` | 显示帮助信息 |
| `kugou-cli <子命令> --help` | 显示子命令帮助（如 `kugou-cli music search --help`）|
