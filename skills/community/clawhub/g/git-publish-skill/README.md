# git-publish

将当前项目一键推送到 GitHub 远程仓库的 AI Coding Agent Skill，兼容 Claude Code、Codex CLI、OpenCode 等主流 AI 编程工具。

## 功能

- 自动检测并初始化 Git 仓库（如果尚未初始化）
- 自动暂存并提交未保存的改动，生成规范的 commit message
- 自动检测当前分支并推送到远程仓库
- 推送失败时提供强制推送选项
- **仓库地址记忆** — 自动记录本地项目路径与 GitHub 仓库的对应关系，再次推送时无需重复提供仓库地址

## 安装

### Claude Code

将本仓库克隆到 Claude Code 的 skills 目录：

```bash
# 全局安装（所有项目可用）
git clone https://github.com/orbisz/git-publish-skill.git ~/.claude/skills/git-publish

# 或者项目级安装（仅当前项目可用）
git clone https://github.com/orbisz/git-publish-skill.git .claude/skills/git-publish
```

安装后重启 Claude Code 即可生效。

### Codex CLI

Codex CLI（v0.65+）兼容 Claude Code 的 skill 格式，直接复制即可使用：

```bash
# 全局安装
git clone https://github.com/orbisz/git-publish-skill.git ~/.codex/skills/git-publish

# 或者项目级安装
git clone https://github.com/orbisz/git-publish-skill.git .codex/skills/git-publish
```

如果尚未启用 skills 功能，需在 `~/.codex/config.toml` 中添加：

```toml
[features]
skills = true
```

然后重启 Codex，使用 `/skills` 查看已安装的技能。

### OpenCode

OpenCode（v1.0.110+）通过插件支持 skills，首先在 `~/.config/opencode/opencode.json` 中启用插件：

```json
{
  "plugin": ["opencode-agent-skills"]
}
```

然后将本仓库安装到 skills 目录：

```bash
# 全局安装
git clone https://github.com/orbisz/git-publish-skill.git ~/.opencode/skills/git-publish

# 或者项目级安装
git clone https://github.com/orbisz/git-publish-skill.git .opencode/skills/git-publish
```

重启 OpenCode 后生效。

### 其他 AI 工具

任何遵循 Anthropic Agent Skills 规范的工具都可以使用本 skill，只需将仓库克隆到对应工具的 skills 目录下即可。

## 使用方式

在任何支持的 AI 工具中，进入项目目录，直接对话即可：

- "帮我把这个项目推送到 GitHub"
- "push 到 https://github.com/user/repo.git"
- "上传到远程仓库"

AI 会自动识别并调用此 skill，按以下流程执行：

1. **查找仓库地址** — 自动在映射表中查找当前项目对应的 GitHub 仓库地址；如未记录则询问用户
2. **初始化 Git**（如需） — 如果项目还未初始化 git，自动执行 `git init` + 初始提交 + 添加 remote
3. **处理未提交改动** — 自动暂存所有改动，基于 diff 生成 conventional commit 格式的提交信息
4. **推送到远程** — 自动检测当前分支，先尝试普通推送；失败时询问是否强制推送
5. **保存映射** — 推送成功后自动记录项目路径与仓库地址的对应关系，下次免输入

## 支持的仓库地址格式

- `https://github.com/user/repo.git`
- `git@github.com:user/repo.git`
- `https://github.com/user/repo`

## 示例

```
用户: 把这个项目push到 https://github.com/myuser/my-project.git

AI 会:
1. 检查 git 状态
2. 如需则 git init 并初始提交
3. 处理未提交改动，生成如 "feat: add user authentication module" 的提交信息
4. git push -u origin main
5. 报告推送结果
```
