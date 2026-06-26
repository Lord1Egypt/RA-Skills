# GitLab Code Review Skill 安装指南

自动监控 GitLab 提交，定时生成代码审查报告。

## 安装方式

### 方式一：通过 ClawHub CLI 安装（推荐）

```bash
# 1. 安装 ClawHub CLI
npm i -g clawhub

# 2. 登录（首次使用）
clawhub login

# 3. 安装 Skill
clawhub install gitlab-code-review
```

### 方式二：网页下载手动安装

如果 ClawHub CLI 安装不成功，可以通过网页下载：

1. 访问 https://clawhub.ai/zhanghaiyu0511/gitlab-code-review
2. 点击 **Download ZIP** 下载
3. 解压到 OpenClaw workspace 的 skills 目录：

```bash
# 解压到 workspace/skills/ 目录
cd ~/.openclaw/workspace/skills
unzip ~/Downloads/gitlab-code-review.zip
```

## 配置步骤

安装完成后，在 OpenClaw 中说：

> 「配置 GitLab code review」

然后回答以下问题：

| 问题 | 示例 |
|------|------|
| GitLab URL | `https://gitlab.example.com` |
| 项目路径 | `group/project` |
| 分支名称 | `main` 或 `dev` |
| Personal Access Token | `glpat-xxxxxxxx` |

**获取 Token**：
1. 打开 GitLab → 用户设置 → Access Tokens
2. 勾选 `read_api` 权限
3. 创建并复制 Token

配置完成后，整点将自动检查新提交并推送审查报告。

**注意**：首次运行只获取最近 2 个提交进行审查，之后每次获取新提交。

## 使用说明

### 自动执行

每小时整点自动检查新提交：
- 有新提交 → 生成审查报告 → 推送通知
- 无新提交 → 静默（不发送消息）

### 手动触发

```bash
python ~/.openclaw/workspace/skills/gitlab-code-review/scripts/fetch_commits.py
```

或在 OpenClaw 中说：
> 「检查 GitLab 是否有新提交」

## 配置文件

配置保存在 `workspace/.env`：

```
GITLAB_URL=https://gitlab.example.com
GITLAB_TOKEN=glpat-xxxxxxxx
GITLAB_PROJECT=group/project
GITLAB_BRANCH=main
```

**注意**：`.env` 文件包含敏感信息，已自动加入 `.gitignore`。

## 故障排查

### 提示缺少配置

```
Error: Missing config: GITLAB_TOKEN, GITLAB_PROJECT
```

**解决**：重新运行配置流程，或手动检查 `workspace/.env` 文件。

### 脚本执行失败

```bash
# 检查依赖
pip3 install requests python-dotenv

# 测试连接
python ~/.openclaw/workspace/skills/gitlab-code-review/scripts/fetch_commits.py
```

### Token 权限不足

确保 Token 有 `read_api` 权限。

### Token 已失效

如果看到 `Token was revoked` 错误，需要重新生成 Token。

## 文件说明

| 文件 | 说明 |
|------|------|
| `workspace/.env` | GitLab 配置（敏感） |
| `workspace/HEARTBEAT.md` | 定时任务配置 |
| `memory/gitlab_review_state.json` | 审查状态记录 |
| `memory/pending_review_*.json` | 待审查提交 |
| `memory/code_review_*.md` | 审查报告 |

## 更新 Skill

```bash
clawhub update gitlab-code-review
```

或重新从网页下载最新版本。

## 链接

- Skill 主页: https://clawhub.ai/zhanghaiyu0511/gitlab-code-review
- OpenClaw 文档: https://docs.openclaw.ai
- ClawHub 社区: https://clawhub.com
