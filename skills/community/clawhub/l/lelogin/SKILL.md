---
name: lelogin
description: >-
  Covers lelogin CLI end-to-end: install from official web scripts when missing,
  auth/config, list/save/delete secrets, and exec usage for MySQL,
  SSH, app startup, Alibaba Cloud CLI, and SMTP/IMAP mail. Use when working
  with lelogin command-line, secret management, or lelogin exec commands.
---

# lelogin CLI 一体化技能（安装 + 场景）

面向 Agent 的操作说明：使用 `lelogin` 命令行进行密钥管理与场景集成。

> [!IMPORTANT]
> **安全与合规准则（必须严格遵守）：**
> 1. **显式授权**：在执行 `list`、`save`、`delete` 或 `exec` 之前，Agent **必须**先获得用户的明确批准（Explicit Approval），说明涉及的密钥路径及操作目的。
> 2. **路径限制**：仅限操作用户指定的、与当前任务相关的密钥路径，严禁随意枚举或修改其它账号信息。
> 3. **禁止明文输出**：严禁在任何日志、对话或输出中暴露解析后的明文秘密内容。

## 0) 先检查是否已安装 lelogin CLI（必须）

先检测命令是否可用：

```bash
lelogin --help
```

若命令不可用，**严禁 Agent 自动下载或执行安装脚本（以符合应用商店安全规范）**。
请暂停操作，并向用户输出以下提示，引导其自行安装：

> “检测到当前环境尚未安装 `lelogin` 命令。为保障系统安全，请您自行前往官方页面下载并安装 CLI 工具：
> 👉 **https://lelogin.nationauth.cn/lelogin-portal/home_page/download**
> 
> 请手动完成安装后，再通知我继续进行下一步操作。”

安装完成后验证：

```bash
lelogin --help
```

## 1) 能力概览

| 能力 | 命令 | 典型用途 |
|------|------|----------|
| 查看密钥列表 | `lelogin list` | 查看当前账号可访问的密钥与引用路径 |
| 保存/更新密钥 | `lelogin save ...` | 新增密钥或更新已有密钥值 |
| 删除密钥 | `lelogin delete ...` | 删除不再需要的密钥 |
| 程序执行 | `lelogin exec --env … --env-file … -- <cmd>` | MySQL、SSH、应用启动 |
**推荐**：敏感项尽量用 `exec --env-file`，文件中只写 `lelogin://…` 引用；子进程创建时解析，避免落盘明文配置。

## 2) 常用管理操作：列表、保存、删除

### 列表（引用路径确认）

先看可访问列表，确认引用路径：

```bash
lelogin list
```

### 保存（新增/更新）

先查看命令帮助确认当前版本参数，再执行保存：

```bash
lelogin save --help
# 按 help 中的参数格式填写
lelogin save ...
```

建议：保存后立刻用 `exec` 做一次调用链校验，确认值可被目标程序读取。

### 删除

先查看命令帮助确认参数，再执行删除并复核：

```bash
lelogin delete --help
lelogin delete ...
lelogin list
```

建议：删除前先 `list` 复核引用路径，避免误删；删除后确认调用链中没有残留 `lelogin://...` 引用。

## 3) 示例 1：数据库密码在 lelogin — `mysql` / `mysqldump`

思路：`MYSQL_PWD` 在 env 文件中设为 `lelogin://…`，由 `lelogin exec` 解析后传给子进程，避免在 shell 历史里写密码。

自行准备 env 文件（例如 `mysql.env`）：

```env
DB_HOST=127.0.0.1
DB_PORT=3306
DB_USER=root
DB_NAME=mysql
MYSQL_PWD=lelogin://test/test
```

**调用方式**（由子 shell 展开 `DB_*` / `MYSQL_PWD`，勿在外层引号里提前展开空变量）：

```bash
lelogin exec --env-file mysql.env -- /bin/sh -c \
  'mysql --host="$DB_HOST" --port="$DB_PORT" --user="$DB_USER" \
   --database="$DB_NAME" -e "SELECT 1"'
```

## 4) 示例 2：SSH 用户密码在 lelogin — `ssh`（配合 `sshpass`）

思路：`SSHPASS` 设为 `lelogin://…`，`lelogin exec` 解析后，`sshpass -e` 从环境变量读密码。

`ssh.env` 示例：

```env
SSH_HOST=127.0.0.1
SSH_PORT=22
SSH_USER=root
SSHPASS=lelogin://test/test
```

**调用方式**：

```bash
lelogin exec --env-file ssh.env -- /bin/sh -c \
  'sshpass -e ssh -o StrictHostKeyChecking=no -p "$SSH_PORT" \
   "$SSH_USER@$SSH_HOST" "echo ok"'
```

未安装 `sshpass` 时上述命令会失败，需先安装 `sshpass`。

## 5) 示例 3：应用启动 — 仅用 `lelogin exec`，不落盘明文配置

思路：本地 env 文件采用 **`--env-file` 支持的子集格式**，敏感键值为 `lelogin://…`；应用由 `lelogin` 拉起，从**环境变量**读取已解析的值。

`app.bootstrap.env` 示例：

```env
APP_NAME=demo-app
DB_PASSWORD=lelogin://test/test
REDIS_PASSWORD=lelogin://test/key2
```

**调用方式**：

```bash
lelogin exec --env-file app.bootstrap.env -- java -jar your-app.jar
# 或
lelogin exec --env-file app.bootstrap.env -- npm start
```

**边界**：CLI 不会在应用每次读磁盘上的配置文件时自动替换占位符；建议改为 Spring `SPRING_APPLICATION_JSON` / 环境变量绑定，或让应用直接读取环境变量。

## 6) 示例（阿里云 CLI）：用 `exec` 填入 RAM AccessKey

目标：帮**阿里云 CLI**拿到凭据（与 [配置身份凭证](https://help.aliyun.com/zh/cli/configure-credentials) 互补），密钥仍存 lelogin；通过 SDK 约定的环境变量传入子进程。

准备 `aliyun_cli.env`（将 `lelogin://…` 换成你的 AccessKeyId / Secret 引用），然后：

```bash
lelogin exec --env-file aliyun_cli.env -- aliyun sts GetCallerIdentity
# 或其它子命令，例如: aliyun ecs DescribeRegions
```

## 7) 示例（邮件）：账号密码在 lelogin，执行 SMTP 发送 + IMAP 收件

准备 `mail.env`：填写真实 SMTP/IMAP 主机、端口，以及 `lelogin://` 形式的账号与密码引用；再用 `lelogin exec` 启动你的邮件脚本或工具（例如 `python3` 脚本），在脚本内从环境变量读取已解析的凭据。

## 8) 示例 4：行内 `--env`

```bash
lelogin exec \
  --env TEST_KEY=lelogin://test/test \
  --env KEY2_NAME=lelogin://test/key2 \
  -- /bin/sh -c 'if [ -n "$TEST_KEY" ] && [ -n "$KEY2_NAME" ]; then echo "Success: Environment variables injected securely"; fi'
```

## 9) Agent 自检清单

- [ ] 未在命令行参数中硬编码明文密码。
- [ ] 优先 `exec --env-file`，避免落盘明文配置。
- [ ] **已就关键操作（list/save/delete/exec）获得用户的显式批准。**
- [ ] 执行前确认 `LELOGIN_*` 或配置文件已设置。
- [ ] 若缺少 `lelogin` 命令，先完成本技能第 0 节的网页安装步骤再执行场景。
