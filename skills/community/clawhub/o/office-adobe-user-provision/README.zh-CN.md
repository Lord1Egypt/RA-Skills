# office-adobe-user-provision

[English](./README.md) | **中文**

> **类型:** Agent Skill(兼容 Claude Code / Anthropic)· **入口:** [`SKILL.md`](./SKILL.md)
> **能力:** 开通与管理 **Microsoft 365(世纪互联 / 21Vianet)** 和 **Adobe Creative Cloud** 用户——创建、授权、重置密码、删除、查询、批量、自检。
> **凭据:** 本仓库不含任何真实凭据,只有 `.env.example` 模板;`.env` 已被 `.gitignore` 永久排除。

---

## 给 Agent 的速览(TL;DR)

| | |
|---|---|
| **它是什么** | 一个自包含 skill。`SKILL.md` 里是激活触发词和操作流程。 |
| **安装** | `git clone <本仓库> ~/.claude/skills/office-adobe-user-provision`,然后重启会话。 |
| **配置** | `cp .env.example .env`,填入你自己的 Entra App / Adobe UMAPI / SMTP 凭据。 |
| **调用** | `./oup <provider> <action> ...`(例:`./oup adobe create alice@corp.com --product cc`)。 |
| **运行时** | Python 3.9+。用 `./oup` 或 `python3 main.py`——**别用裸 `python`**(很多机器上是 Python 2)。 |

## 这是 skill 还是普通仓库?—— 是 skill。

本仓库**就是**一个 Claude Code Skill。契约如下:

- [`SKILL.md`](./SKILL.md) 以 YAML frontmatter 开头:
  - `name: office-adobe-user-provision`
  - `description:` 一句话简介 **+ `USE WHEN ...` 触发词**,让 Agent 能自动激活它。
- Claude Code 在**会话启动时扫描 skill 目录**来发现 skill。把本仓库放到
  `~/.claude/skills/office-adobe-user-provision/`(全局)或 `<项目>/.claude/skills/...`(项目级)即完成注册。
  **目录名就是 skill 名**,所以必须 clone 成这个确切的文件夹名。
- 它**同时**也是一个可独立运行的 Python CLI / HTTP 工具,不依赖任何 Agent 也能跑——便于测试或脚本化。

## 安装(clone 即装)

```bash
# 全局(本机每个会话都可用)
git clone https://github.com/eggyrooch-blip/office-adobe-user-provision.git \
  ~/.claude/skills/office-adobe-user-provision

# 项目级改成:
#   git clone <url> <你的仓库>/.claude/skills/office-adobe-user-provision
```

装好后**重启 Claude Code 会话**——skill 列表在启动时加载。

## 配置(填凭据)

```bash
cd ~/.claude/skills/office-adobe-user-provision
cp .env.example .env          # 按模板注释填入你自己的凭据
pip install -r requirements.txt
./oup office365 init          # 验证 O365 凭据 + 拉产品
./oup adobe init              # 验证 Adobe 凭据 + 拉产品
```

需自备的凭据(见 [`.env.example`](./.env.example)):

- **Office 365** —— Entra App `CLIENT_ID` / `TENANT_ID` / `CLIENT_SECRET`(需管理员同意 `User.ReadWrite.All`、`LicenseAssignment.ReadWrite.All`、`User-PasswordProfile.ReadWrite.All`),以及 `DEFAULT_DOMAIN`。
- **Adobe** —— UMAPI `ADOBE_CLIENT_ID` / `ADOBE_CLIENT_SECRET` / `ADOBE_ORG_ID`。
- **可选** —— SMTP 配置,用于发送账号通知邮件。

## 能力速查

```bash
./oup <provider> init                                  # 验证凭据 + 缓存产品
./oup <provider> products [--refresh]                  # 列出 / 刷新产品目录
./oup office365 create <ldap> --display-name "<姓名>"   # 创建 + 自动授权 + 发通知
./oup adobe   create <ldap>@<domain> --product cc      # cc=全家桶 · ps=Photoshop · acrobat=Acrobat Pro
./oup <provider> assign  <id> --product <p>            # 追加授权 / 产品
./oup <provider> reset   <id>                          # 重置密码
./oup <provider> delete  <id>                          # 删除用户
./oup <provider> inspect <id> --json                   # 查询(只读)
./oup <provider> selftest                              # 端到端自检(建→授权→重置→删临时用户)
python3 -m app.api.server                              # 启动镜像 CLI 的 HTTP API
```

provider 别名:`office365` = `o365` = `m365`;`adobe` = `ps`。
`oup` 是自带的 CLI wrapper——自动定位 skill 目录、加载 `.env`,可从任意路径调用。等价于 `python3 main.py ...`。

## 激活触发词

当用户说出以下内容(任意语言)时,Agent 应激活本 skill:

`给 XX 开账号` · `新建用户` · `入职开账号` · `开 Office` · `开 Adobe` · `全家桶 / All Apps` · `重置密码` · `删除用户` · `批量开户` · `查用户` · “create user”、“provision account”、“add Office/Adobe license”

## 安全红线(在 SKILL.md 中强制)

- **不覆盖已有用户** —— 先 `inspect`,若已存在,确认是"重置"还是"跳过"。
- **初始密码不回显到日志** —— 只出现在通知邮件正文。
- **LDAP 不自作主张生成** —— 必须用户明确给出。
- **`.env` 永不入库** —— `.gitignore` 已排除;任何提交前先 `git status` 确认。

## 架构

```
入口(main.py CLI · app/api/server.py Flask)
   └─ app/services/user_service.py      ← 统一业务门面(所有入口都走这里)
        └─ app/providers/office365/     ← Graph API:认证、用户、授权、邮件
        └─ app/providers/adobe/         ← UMAPI:认证、addAdobeID + 分组授权
```

扩展时先加到 `user_service.py`,再让 CLI/API 暴露。完整流程、Red Flags 表和各 provider 细节见 [`SKILL.md`](./SKILL.md)。
