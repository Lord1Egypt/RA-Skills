# pings

与常见 Agent Skill 约定对齐的目录布局：

| 路径 | 说明 |
|------|------|
| `SKILL.md` | 主说明：触发条件、邮箱、展示格式、固定底部文案等（**必读**） |
| `reference.md` | 接口契约：Query、响应字段、错误与业务行为 |
| `examples.md` | 调用示例：HTTP / curl / CLI |
| `scripts/` | （可选）辅助脚本；需要时再添加 |

阅读顺序：先 `SKILL.md`，再按需 `reference.md` / `examples.md`。

**发现路径：** 仓库根目录 **`skills/`**（OpenClaw 等工作区）；另见 `.cursor/skills/`、`.claude/skills/`、`.openclaw/skills/` 下同名符号链接，均指向本目录。
