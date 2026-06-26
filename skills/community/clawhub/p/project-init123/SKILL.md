---
name: project-init
description: 自动初始化 Gitea 科研项目仓库。通过对话收集仓库名称、描述、创建者、成员、可见性等信息，自动创建仓库并写入标准目录结构（meeting/ docs/ src/ data/ reports/ profiles/）、README.md、CONTRIBUTING.md 及各成员档案文件（profiles/用户名.md）。自动将创建者设为仓库管理员（admin），其他成员以只读权限（read）加入仓库，同时创建启动期 Issue 并发送邮件通知。支持对已有空仓库执行初始化（幂等保护）。
metadata:
  openclaw:
    emoji: "🚀"
    requires:
      bins:
        - node
        - python3
---

# 科研项目仓库初始化工具

通过与用户对话，自动完成 Gitea 仓库的标准化初始化。

## 使用方式

用户说"帮我建一个新仓库"或"帮我初始化 xxx 仓库"时触发。

Skill 会依次询问（共 6 步）：

1. 仓库名称（英文，用于 URL）
2. 项目描述
3. 创建者的 Gitea 用户名（设为仓库管理员）
4. 其他参与成员的 Gitea 用户名（选填，以只读权限加入仓库）
5. 是否私有（默认公开）
6. 确认信息 → 执行初始化

## 初始化内容

- 标准目录：`meeting/` `docs/` `src/` `data/` `reports/` `profiles/`
- 基础文档：`README.md`（含变量替换）、`CONTRIBUTING.md`（固定协作规范）
- 成员档案：`profiles/用户名.md`（为创建者和每位成员各生成一个，待本人补充）
- 协作者权限：创建者设为 `admin`，其他成员设为 `read`
- 初始 Issue：全体通知 + 分工确认（分工 Issue 同时提示补充成员档案）
- 邮件通知：发送给所有提供的成员及创建者

## 幂等保护

若仓库中已存在 `README.md`，则跳过初始化并提示用户。

## 失败处理

任何步骤失败时，记录错误并发送失败通知邮件给创建者，说明失败步骤和建议的手动补救方式。

## 环境变量

参考 `env-example.txt`，配置于 `~/.config/project-init/.env`。

| 变量 | 说明 |
|------|------|
| `GITEA_URL` | Gitea 服务器地址 |
| `GITEA_TOKEN` | AIFusionBot 的 Personal Access Token |
| `GITEA_ORG` | 操作的 Gitea 组织名 |
| `EMAIL_SKILL_PATH` | imap-smtp-email Skill 的绝对路径 |
| `EMAIL_ACCOUNT` | 发件邮箱账号名称（留空使用默认账号） |
