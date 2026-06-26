# Distribution

## 推荐发布信息

- **skill folder / slug**: `openclaw-continuity-pack`
- **display name**: `OpenClaw全自动新对话续接`
- **version**: `0.5.0`

## 命名要求

- `SKILL.md` frontmatter 里的 `name` 必须保持 **hyphen-case**
- ClawHub 展示名可以保留人类可读形式，例如 `OpenClaw全自动新对话续接`

## 发布前建议检查

至少确认：
- `SKILL.md` frontmatter 合法
- `agents/openai.yaml` 存在且描述准确
- `scripts/` 里只有正式可分发脚本
- `assets/` 里没有 secrets、日志、真实 workspace 实例、`.bak_*`、`.tmp/`
- `references/` 里没有写死本机路径或一次性现场说明
- 文档描述与当前 live 目标一致：silent continuity prep、80/85/88/90 阈值、ordinary chat 无 continuity/context 提示

## 打包与发布

如果你的环境已经提供本地 skill 校验或发布工具，优先使用你自己的标准流程。

如果没有专用打包器，也可以把整个 source folder 打成 zip 包并使用 `.skill` 后缀，前提是压缩包内保留根目录：

```text
openclaw-continuity-pack/
  SKILL.md
  agents/
  assets/
  references/
  scripts/
  LICENSE
```

如果你的 ClawHub 环境支持 `clawhub publish`，按本地 CLI 语法发布当前 skill source folder 即可。
