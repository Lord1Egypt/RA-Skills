---
name: ok-auth
description: |
  OK.com 认证管理技能。检查登录状态、邮箱密码登录、等待 OAuth 登录。
  当用户要求登录 OK.com、检查登录状态时触发。
---

# ok-auth — 认证管理

管理 OK.com 的登录状态，支持邮箱密码登录和第三方 OAuth 引导登录。

## 执行约束

`<SKILL_DIR>` 是本 SKILL.md 的**上两级目录**（即包含 `pyproject.toml` 的项目根目录）。

## 命令

```bash
# 检查登录状态（当前页面）
uv run --project <SKILL_DIR> ok-cli check-login

# 检查特定站点的登录状态（推荐：各国站登录态独立）
uv run --project <SKILL_DIR> ok-cli check-login --subdomain au

# 邮箱密码登录（指定目标站点，推荐）
uv run --project <SKILL_DIR> ok-cli login --subdomain au --email "user@example.com" --password "yourpassword"

# 等待用户手动完成 OAuth 登录（指定目标站点，推荐）
uv run --project <SKILL_DIR> ok-cli wait-login --subdomain au --timeout 120

# （可选）仅使用 Playwright 时，首次安装浏览器
uv run playwright install chromium
```

## 参数说明

- `--subdomain`: 目标站点子域名（如 `au`、`sg`、`us`）。`check-login`/`login`/`wait-login` 均支持。**各国站登录态独立**，建议始终指定
- `--email`: 邮箱地址（登录/注册共用，如果邮箱未注册会自动进入注册流程）
- `--password`: 密码（8-16 位，至少 1 个数字、1 个大写字母、1 个小写字母）
- `--timeout`: 等待手动登录的超时秒数（默认 120）
- `--country`: 国家代码，用于导航（默认 `singapore`）

## 工作流程

### 第一步：检查登录状态

```bash
# 检查特定站点（推荐）
uv run --project <SKILL_DIR> ok-cli check-login --subdomain au

# 或检查当前页面
uv run --project <SKILL_DIR> ok-cli check-login
```

返回值：
```json
{"logged_in": true, "user_name": "用户名", "subdomain": "au"}
```
或
```json
{"logged_in": false, "user_name": null, "subdomain": "au"}
```

### 第二步：根据情况选择登录方式

#### 方式 A：邮箱密码登录（推荐）

**必须先向用户确认邮箱和密码，不得从历史对话中自动填入。**

```bash
uv run --project <SKILL_DIR> ok-cli login --subdomain <子域名> --email "user@example.com" --password "Pass1234"
```

返回值：
- 登录成功：`{"logged_in": true, "account_type": "login", "message": "登录成功"}`
- 注册成功：`{"logged_in": true, "account_type": "register", "message": "注册并登录成功"}`
- 登录失败：`{"logged_in": false, "account_type": "login", "message": "登录失败: 密码错误"}`

> 如果邮箱不存在，OK.com 会自动进入注册流程，使用相同的邮箱和密码完成注册。

#### 方式 B：OAuth 引导登录（Google/Facebook/Apple）

1. 提示用户在浏览器中点击对应的第三方登录按钮
2. 运行 `wait-login` 等待登录完成

```bash
uv run --project <SKILL_DIR> ok-cli wait-login --subdomain <子域名> --timeout 120
```

## 说明

- OK.com 浏览帖子不需要登录
- 发布帖子、联系卖家等操作需要登录
- 密码仅在当前会话中使用，不会被持久化保存
- **不要频繁重复登录或退出登录**，避免触发风控
- 登录弹窗是覆盖在当前页面上的，没有独立的登录 URL
