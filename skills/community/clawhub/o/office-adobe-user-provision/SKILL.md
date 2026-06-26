---
name: office-adobe-user-provision
description: 统一开通/管理 Microsoft 365(世纪互联)与 Adobe Creative Cloud 用户的自包含工具。创建、授权、重置密码、删除、查询、批量、自检,CLI/HTTP API 共用同一套 provider。USE WHEN 给XX开账号, 新建用户, 新增用户, 入职开账号, 开Office, 加Office, 开Adobe, 加Adobe, 全家桶, All Apps, 重置密码, 删除用户, 批量开户, 查用户, office365, adobe, M365, Creative Cloud, 处理开户审批.
---

# Office 365 + Adobe 用户开通工具(自包含 skill)

统一的 Python CLI,管理 **Microsoft 365(世纪互联版)** 与 **Adobe Creative Cloud** 用户。
本 skill **自带完整代码 + 凭据**,解压即用,无需再 clone 原仓库。

## 0. 前置(每次执行前确认)

```bash
pip install -r requirements.txt   # 首次:requests / python-dotenv / flask(需 Python 3.9+)
```

### 两种调用方式(等价)

```bash
# 方式 A —— 自带 CLI(推荐手敲):oup 会自动定位 skill 目录、加载 .env,可从任意路径调用
./oup adobe inspect zhangsan@example.com
ln -sf "$PWD/oup" /usr/local/bin/oup   # 可选:软链到 PATH 后全局 `oup adobe ...`

# 方式 B —— 直接调脚本:必须先 cd 到 skill 目录,且用 python3(非交互 shell 里 python 可能是 py2)
cd <本 skill 所在目录> && python3 main.py adobe inspect zhangsan@example.com
```

> 下文示例统一用 `oup`;等价于 `python3 main.py`。**别用裸 `python`**——很多机器上它指向 Python 2,会直接 SyntaxError。

- **凭据在本目录 `.env`** —— 已随包含真实生产配置(`CLIENT_SECRET` / `ADOBE_CLIENT_SECRET` / `SMTP_PASSWORD` / `DEFAULT_PASSWORD` 等)。
- ⚠️ **安全红线:`.env` 已被 `.gitignore` 排除。把本 skill 放进任何 git 仓库前,务必确认 `.env` 不会被 `git add`。绝不能 commit/push 到 GitHub。**
- 凭据要换/轮换时,只改 `.env`,代码不动(`config.py` 是唯一读取处)。

## 1. 验证工具可用(开户前必做)

```bash
./oup office365 init    # 检查 .env、拉产品、缓存默认 license
./oup adobe init        # 检查 .env、拉 Adobe 产品/profile
```
两条 `init` 都正常返回产品列表 = 工具可用。失败先看 `.env` 与下方 Red Flags。

## 2. 触发场景 → 动作

| 用户说 | provider | 命令 |
|---|---|---|
| "给 XX 开账号 / 新建用户"(未说平台) | 先问 | 用 AskUserQuestion 问 provider/LDAP/姓名 |
| "新员工 / 入职开账号" | both | O365 → Adobe 顺序执行 |
| "给 XX 开 Office / 加 Office" | office365 | 见 §3 |
| "给 XX 开 Adobe / 全家桶 / All Apps" | adobe | 见 §4 |
| "批量开户" | — | 需要列表(CSV/粘贴),逐条执行后汇总 |

## 3. Office 365 开通

```bash
./oup office365 create <ldap> --display-name "<中文名>" [--product O365_BUSINESS]
```
- 未指定 `--product` → 用 `init` 缓存的默认 license
- CLI 自动:创建用户 → 分配 license → 按 `.env` SMTP 发通知邮件(含初始密码)
- 成功返回含 `id`、`userPrincipalName`、`password`
- 租户是**世纪互联版**(`entra.microsoftonline.cn` / `partner.onmschina.cn`),不是国际版

## 4. Adobe 开通

```bash
./oup adobe create <ldap>@<domain> [--product cc|ps|acrobat]
```
- **默认 = All Apps(全家桶)**;`--product cc`/`all`=全家桶,`ps`=Photoshop,`acrobat`=Acrobat Pro
- 底层 `addAdobeID` + `add group` 一次完成邀请与授权
- 期望返回 `{"completed":1,"result":"success"}`
- adobeID 类型走**邀请制**:新用户收到 Adobe 邀请邮件,接受后登录 https://creativecloud.adobe.com
- 注意:CLI 会从邮箱前缀自动拆 firstname/lastname(非中文名);adobeID 显示名影响小,需中文名要去 Adobe Admin Console 改

## 5. 安全红线(执行时遵守)

- **不覆盖已有用户**:先 `inspect`,返回 200/存在 → 用 AskUserQuestion 确认是"重置"还是"跳过",绝不静默覆盖。
- **初始密码不回显到日志**:只出现在通知邮件正文,控制台脱敏。
- **LDAP 不自作主张生成**:必须用户明确给出。
- **Adobe 座位不足**(`error.group.license_quota_exceeded`)→ 报告用户,不静默降级到其他产品。

## 6. 结果验证 + 交付

```bash
./oup office365 inspect <ldap> --json
./oup adobe inspect <ldap>@<domain> --json
```
给用户摘要:账号(LDAP+email)、初始密码/邀请说明、已授权产品、登录入口
(O365: https://portal.partner.microsoftonline.cn · Adobe: https://creativecloud.adobe.com)。

## 7. 其他命令

```bash
./oup <provider> products [--refresh]   # 列/刷新产品
./oup <provider> assign <id> --product <p>
./oup <provider> reset <id>             # 重置密码
./oup <provider> delete <id>            # 删除
./oup <provider> alias <name> <product> # 设产品别名
./oup <provider> selftest               # 端到端自检(会建→授→重置→删临时用户)
python3 -m app.api.server                         # 起 HTTP API(路由镜像 CLI)
```
provider 别名:`office365`/`o365`/`m365` 同义;`adobe`/`ps` 同义。

## Red Flags

| 症状 | 原因 | 处理 |
|---|---|---|
| O365 `Insufficient privileges` | Entra App 权限未管理员同意 | Entra → API 权限 → 授予管理员同意 |
| O365 `License not available` | license 池用完 | 购买/回收,不硬删他人 |
| Adobe `error.group.license_quota_exceeded` | 座位不够 | 报告用户,不降级 |
| Adobe `error.domain.trust.nonexistent` | federatedID 但域名未声明 | 改用 adobeID(默认就是) |
| 任一 `init` 报 missing env | `.env` 缺字段 | 对照 `.env.example` 补齐 |

## 架构(改 provider 行为前先读)

入口(`main.py` CLI / `app/api/server.py` Flask) → `app/services/user_service.py`(统一业务门面) → `app/providers/{office365,adobe}/`(对接外部 API)。
扩展功能先加到 `user_service.py` 再让 CLI/API 暴露。详见 `README.md`、`docs/README_ADOBE.md`、`docs/README_API.md`。
