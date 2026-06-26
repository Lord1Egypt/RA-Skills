---
name: github-sync-skill
version: "2.0.0"
description: 将本地创建或修改的 Claude Code 技能自动同步到 GitHub 仓库。支持增量同步、单技能同步、自动生成 README.md。
author: kuiilabs
tags: ["github", "sync", "backup", "automation", "git", "skill-management"]
license: "MIT"
---

# GitHub Sync Skill - 技能同步工具

将本地技能自动同步到 GitHub 仓库的辅助工具。

## 触发场景

当用户要求：
- 把技能同步到 GitHub
- 发布技能到 GitHub
- 备份我的技能
- 更新 GitHub 上的技能仓库
- "sync my skills to GitHub"
- "把新创建的 skill 上传到 GitHub"

## 核心功能

### 1. 增量同步（默认）
- 自动检测远程仓库已有的技能
- 只同步本地有但远程没有的新技能
- 避免重复上传已存在的技能

### 2. 单技能同步
- 使用 `--skill <skill-name>` 指定同步单个技能
- 适合新创建技能后快速发布

### 3. 自动生成 README.md
- 每次同步后自动更新仓库的 README.md
- 包含所有技能的名称、描述、标签
- 提供安装和使用说明

### 4. Token 权限验证
- 检查 Token 有效性
- 验证 repo 权限
- 提供修复建议

## 使用方法

### 增量同步所有新技能（推荐）

```bash
# 自动检测并同步新技能
~/.claude/skills/github-sync-skill/scripts/sync_to_github.sh \
  --owner kuiilabs \
  --repo claude-skills \
  --token $GITHUB_TOKEN
```

### 同步单个技能

```bash
# 当你创建了 new-skill 后
~/.claude/skills/github-sync-skill/scripts/sync_to_github.sh \
  --skill new-skill \
  --owner kuiilabs \
  --repo claude-skills \
  --token $GITHUB_TOKEN
```

### 检查环境

```bash
# 检查 Git
git --version

# 检查 Token 环境变量
echo $GITHUB_TOKEN
```

### 验证 Token 权限

```bash
# 验证 Token 所有者
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user | jq -r '.login'

# 验证仓库权限
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/<owner>/<repo> | jq '.permissions'
```

## 输出格式

### 同步报告

```markdown
============================================================
  GitHub Sync Report
============================================================

仓库：kuiilabs/claude-skills
时间：2026-04-04 19:32:09
同步模式：增量同步
状态：✅ 成功

仓库链接：https://github.com/kuiilabs/claude-skills

============================================================
```

### README.md 自动更新

每次同步新技能后，README.md 会自动追加该技能的信息：

```markdown
### <技能名称>

<技能描述>

**标签**: tag1, tag2, tag3
```

## 工作流程

### 增量同步流程

1. 获取远程仓库已有的技能列表
2. 对比本地用户创建的技能
3. 识别新技能（本地有，远程没有）
4. 上传新技能的所有文件
5. 更新 README.md 添加新技能介绍
6. 生成同步报告

### 单技能同步流程

1. 验证指定的技能目录存在
2. 上传该技能的所有文件
3. 更新 README.md 添加该技能介绍
4. 生成同步报告

## 注意事项

1. **Token 安全**: 不要将 Token 提交到代码仓库
2. **权限要求**: Token 需要 `repo` scope
3. **网络环境**: 需要能访问 GitHub API
4. **冲突处理**: 如有冲突需手动解决
5. **README 更新**: 每次同步会自动更新 README.md

## 相关命令

```bash
# 增量同步所有新技能
~/.claude/skills/github-sync-skill/scripts/sync_to_github.sh

# 同步单个技能
~/.claude/skills/github-sync-skill/scripts/sync_to_github.sh --skill <skill-name>

# 仅检查变更
~/.claude/skills/github-sync-skill/scripts/check_changes.sh

# 验证 Token
~/.claude/skills/github-sync-skill/scripts/verify_token.sh
```

## 安全最佳实践

1. **Token 存储**: 使用环境变量或密钥管理工具
2. **Token 过期**: 设置提醒定期更新（建议 30-90 天）
3. **权限最小化**: 仅授予必要权限
4. **审计日志**: 定期检查 GitHub 登录活动

## 故障排查

| 问题 | 错误信息 | 解决方案 |
|------|---------|---------|
| Token 过期 | `401 Bad credentials` | 重新生成 Token |
| 权限不足 | `403 Resource not accessible` | 添加 `repo` scope |
| 仓库不存在 | `404 Not Found` | 先创建仓库 |
| 网络超时 | `Connection timeout` | 检查网络/代理设置 |
| README 更新失败 | `422 Unprocessable Entity` | 检查文件编码和格式 |

## 示例场景

### 场景 1：创建了新技能后

```bash
# 你创建了 new-skill 目录
mkdir -p ~/.claude/skills/new-skill
# ... 编辑 SKILL.md 和脚本 ...

# 同步到 GitHub
~/.claude/skills/github-sync-skill/scripts/sync_to_github.sh \
  --skill new-skill
```

### 场景 2：定期同步所有新技能

```bash
# 自动检测并同步所有新创建的技能
~/.claude/skills/github-sync-skill/scripts/sync_to_github.sh
```
