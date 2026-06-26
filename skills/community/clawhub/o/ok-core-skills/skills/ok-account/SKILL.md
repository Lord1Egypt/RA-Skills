---
name: ok-account
description: |
  OK.com 账户相关操作：收藏管理、我的帖子管理。所有命令需要登录状态。
  当用户要求查看/管理收藏、查看/删除/编辑我的帖子时触发。
---

# ok-account — 收藏与我的帖子

管理 OK.com 的收藏列表和用户自己的帖子。**所有命令需要登录状态**，未登录会直接报错。

> **WARNING**: 执行以下任何命令前，必须确保已登录。CLI 会自动检测登录状态，未登录时返回错误。

## 执行约束（强制）

- 所有操作只能通过 `uv run --project <SKILL_DIR> ok-cli` 执行
- `<SKILL_DIR>` 是本 SKILL.md 的**上两级目录**（即包含 `pyproject.toml` 的项目根目录）

---

## 步骤 1 — 检查目标站点登录状态

> **重要**：ok.com 各国站登录态独立（sg.ok.com 登录 ≠ au.ok.com 登录）。
> 必须用 `--subdomain` 指定目标站点，否则可能误判为"已登录"。

```bash
uv run --project <SKILL_DIR> ok-cli check-login --subdomain <子域名>
```

- 返回 `"logged_in": true` → 继续步骤 2
- 返回 `"logged_in": false` → 执行登录（见下方）

### 登录方式

**方式 A：邮箱密码登录**（需向用户确认邮箱和密码，禁止自行猜测）：
```bash
uv run --project <SKILL_DIR> ok-cli login --subdomain <子域名> --email "<邮箱>" --password "<密码>"
```

**方式 B：等待用户手动 OAuth 登录**（Google/Facebook/Apple）：
```bash
uv run --project <SKILL_DIR> ok-cli wait-login --subdomain <子域名> --timeout 120
```

提示用户在浏览器中完成登录操作，CLI 会轮询检测。

> `--subdomain` 确保在目标站点上执行登录，避免登错站。

---

## 步骤 2 — 执行命令

### Favorites — 收藏管理

```bash
# 查看收藏列表
uv run --project <SKILL_DIR> ok-cli list-favorites --subdomain <子域名>

# 收藏帖子（传入帖子详情页 URL）
uv run --project <SKILL_DIR> ok-cli add-favorite --url "<帖子URL>"

# 取消收藏（推荐：按索引，配合 list-favorites 结果使用）
uv run --project <SKILL_DIR> ok-cli remove-favorite --subdomain <子域名> --index <编号>

# 取消收藏（按详情页 URL）
uv run --project <SKILL_DIR> ok-cli remove-favorite --url "<帖子URL>"
```

### My Posts — 我的帖子管理

```bash
# 查看我的帖子（可按状态筛选）
uv run --project <SKILL_DIR> ok-cli list-my-posts --subdomain <子域名> [--state active|pending|expired|draft]

# 删除帖子（按索引）
uv run --project <SKILL_DIR> ok-cli delete-post --subdomain <子域名> --index <编号>

# 获取帖子编辑链接（按索引）
uv run --project <SKILL_DIR> ok-cli edit-post --subdomain <子域名> --index <编号>
```

---

## 参数说明

**`--subdomain`** 是国家对应的子域名缩写，不是国家全名：

| 国家 | --subdomain |
|------|-------------|
| Singapore | sg |
| Canada | ca |
| USA | us |
| UAE | ae |
| Australia | au |
| Hong Kong | hk |
| Japan | jp |
| UK | gb |
| Malaysia | my |
| New Zealand | nz |

**`--index`** 是帖子在列表中的位置（从 0 开始）。

---

## 完整示例

**用户："查看我在澳大利亚的收藏"**

```bash
# 步骤1：检查 au 站登录状态
uv run --project <SKILL_DIR> ok-cli check-login --subdomain au
# → logged_in: false

# 登录 au 站
uv run --project <SKILL_DIR> ok-cli wait-login --subdomain au --timeout 120
# → 等待用户在浏览器中登录

# 步骤2：查看收藏
uv run --project <SKILL_DIR> ok-cli list-favorites --subdomain au
```

**用户："删除我在新加坡的第一条帖子"**

```bash
# 步骤1：检查 sg 站登录状态
uv run --project <SKILL_DIR> ok-cli check-login --subdomain sg
# → logged_in: true

# 步骤2：先查看帖子列表
uv run --project <SKILL_DIR> ok-cli list-my-posts --subdomain sg

# 确认后删除
uv run --project <SKILL_DIR> ok-cli delete-post --subdomain sg --index 0
```
