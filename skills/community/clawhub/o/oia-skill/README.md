# @oia-ai/oia-skill

Claude Code skill：一键初始化基于 **oia 框架**（`@oia-ai/oia-fresh`，Deno + Fresh 2 + Vite）的 Web 项目。

## 安装

```bash
npx @oia-ai/oia-skill           # 安装到当前项目 .claude/skills/oia-skill
npx @oia-ai/oia-skill --global  # 安装到用户目录 ~/.claude/skills/oia-skill（所有项目可用）
```

也可以手动：把本目录（含 SKILL.md）复制到 `.claude/skills/oia-skill/` 下。

## 使用

在 Claude Code 里说「初始化一个 oia 项目」「用 oia-fresh 创建应用」，或输入 `/oia-skill`。

skill 会按流程执行：环境检查 → `npx @oia-ai/oia-fresh init` 脚手架 → 启动 `deno task dev` 并验证首页返回 200 → 汇报结果。

## 环境要求

- Deno 2.x（项目运行）
- Node / npx（仅执行 init 与 skill 安装脚本）
