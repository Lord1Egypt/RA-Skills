# libai-perspective（李白视角 · Cursor Skill）

可单独发布、复制的 Agent Skill：用传世诗学与史传气质蒸馏的「太白式」思维与表达框架。

## 包内容

| 路径 | 说明 |
|------|------|
| `SKILL.md` | **必需**。Cursor 读取的主文件（YAML frontmatter + 正文） |
| `references/research/` | 可选。自行追加调研笔记，不影响 Skill 加载 |

## 安装

**项目内**：将整个 `libai-perspective` 目录放到仓库根目录下的 `.cursor/skills/`。

**本机全局**（所有项目可用）：

- macOS / Linux：`~/.cursor/skills/libai-perspective/`
- Windows：`%USERPROFILE%\.cursor\skills\libai-perspective\`

重启 Cursor 或重新打开工作区后，在对话中说「用李白的视角」「太白模式」等即可触发（见 `SKILL.md` 的 `description`）。

## 发布

将 `libai-perspective` 文件夹打成 zip，或推送到独立 Git 仓库；使用者只需解压/克隆到上述 `skills` 路径之一。

## 与 nuwa 造人仓库的关系

本包可作为「女娲蒸馏」产物独立存在；若在 monorepo 中保留 `nuwa-skill-main/examples/libai-perspective` 指针说明，请以本目录为**唯一正文来源**，避免双份漂移。

## 许可证

正文为原创蒸馏与公有领域古典文本的合理使用；二次分发请保留 `SKILL.md` 中的使用说明与诚实边界。
