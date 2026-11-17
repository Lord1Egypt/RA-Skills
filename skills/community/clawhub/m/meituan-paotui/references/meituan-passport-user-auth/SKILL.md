---
name: meituan-passport-user-auth
description: 美团 Passport 用户授权登录 Skill。通过 pt-passport CLI 获取授权链接，展示给用户完成确认后轮询拿到鉴权凭证。适用场景：(1) 用户主动触发美团授权登录；(2) 其他 Skill 命令模板中出现 ${passport_token} 占位符时自动被依赖调用，Token 透明注入，无需用户感知。不适用于服务端 AppKey/Secret 鉴权或非美团系统授权。触发词：美团授权登录、获取授权码、获取 token、token 授权、passport 登录、触发登录、美团登录、重新授权、meituan passport auth、${passport_token}。

metadata:
  skillhub.creator: "suntiansheng"
  skillhub.updater: "guoqingming"
  skillhub.version: "V19"
  skillhub.source: "FRIDAY Skillhub"
  skillhub.skill_id: "22364"
  skillhub.high_sensitive: "false"
---

## [MANDATORY] SKILLHUB_METRIC_REPORTER_START
执行本 Skill 的任何操作之前，必须先执行 Skill：`skill-metric-reporter`。
按照 `skill-metric-reporter` 的要求完成 `skill_start` 上报后，再去继续本 Skill 正文。
如果 `skill-metric-reporter` 不可用或执行失败，跳过上报，继续执行本 Skill 正文——不得因上报失败而阻塞审阅流程。
本 Skill 全部操作完成后，同样按照 `skill-metric-reporter` 的要求完成 `skill_end` 上报。
## [MANDATORY] SKILLHUB_METRIC_REPORTER_END

# 美团 Passport 用户授权登录

## 概述

通过 `pt-passport` CLI 完成美团 Passport 授权，获取用户鉴权凭证（Token 或 AuthAccessToken）。支持两种模式：

- **直接调用**：用户主动触发，授权成功后输出提示
- **被依赖调用**：外部 Skill 通过 `skill-dependencies` + `${passport_token}` 占位符触发，Token 自动注入命令，无需用户感知

**不适用**：服务端 API 鉴权（用 AppKey/Secret）、非美团系统授权。

---

## 执行流程

### Step 0：安装/更新 CLI（每次会话执行一次）

> **若本会话已执行过 Step 0，直接跳过，进入 Step 1。**

```bash
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" 2>/dev/null && pwd || dirname "$(readlink -f "$0")")"
bash "$SKILL_DIR/scripts/install.sh"
```

> `install.sh` 位于本 SKILL.md 同级的 `scripts/` 目录下。若上方命令无法定位 `SKILL_DIR`，用 `glob_file_search` 搜索 `pt-passport*/scripts/install.sh` 找到其绝对路径，再执行：
>
> ```bash
> bash "<install.sh 的绝对路径>"
> ```

- 安装成功或已是最新：继续 Step 1
- `npm: command not found`：**STOP**，提示用户安装 Node.js >=18（见 [reference.md](reference.md#环境要求)）
- `No local package found`：**STOP**，提示 skill 安装包缺失，请重新安装此 Skill
- 其他失败：**STOP**，提示联系管理员

---

### Step 1：确认参数

按优先级解析，找到即用，不追问：

| 参数           | 优先级来源                                                                       | 缺失时           |
| -------------- | -------------------------------------------------------------------------------- | ---------------- |
| `client_id`    | ① `skill-dependencies.*.client_id` → ② 用户提供                                 | **STOP** 索要    |
| `env`          | ① `skill-dependencies.*.env` → ② 用户说「test」                                  | 默认 `prod`      |
| `--base_url`   | 用户说「泳道」或提供 URL（优先级高于 `--env`）                                   | 不加             |
| `channel`      | ① `skill-dependencies.*.channel` → ② 用户说「大象」「大象个人助理」             | 默认 `other`     |

`channel` 可选值：
- `daxiang`：大象个人助理（二维码和授权链接均通过 `message` 方式下发）
- `other`（默认）：其他场景（Web UI / CatPaw，使用 Markdown 图片语法内联渲染）
**环境一致性约束**：`client_id` 与 `env` 必须属同一环境，混用则 **STOP**：

```
❌ 环境与 client_id 不匹配：当前环境为 <env>，但 client_id 可能属于另一环境，请确认后重试。
```

---

### Step 2：运行授权脚本

**先尝试缓存：**

- **直接调用**：
  ```bash
  pt-passport get-token --client_id <client_id> [--env test] > /dev/null 2>&1
  echo $?
  ```
- **被依赖调用**：
  ```bash
  pt-passport get-token --client_id <client_id> [--env test]
  echo $?
  ```

> ⚠️ **Token 安全**：直接调用时输出必须丢弃（`> /dev/null 2>&1`），**严禁读取、回显或展示命令 stdout**；被依赖调用时可读取 stdout 中的 Token 用于注入，但同样**严禁将 Token 值展示给用户或回显原始命令输出**；两种模式均仅通过退出码判断缓存状态。

- 退出码 `0`：缓存命中
  - **被依赖调用**：静默注入 Token 继续（见 Step 4），不提示用户
  - **直接调用**：向用户输出以下提示，并**等待用户回复**：
    ```
    🔍 检测到您已有授权记录。需要我帮您验证一下是否还有效吗？如果已失效，我会自动帮您重新授权。
    ```
    - 用户回复需要校验 / 重新授权：执行下方**发起授权**步骤
    - 其他情况：流程结束
- 退出码 `1`：无缓存，继续发起授权

**发起授权：**

```bash
pt-passport auth get-code --client_id <client_id> [--env test] [--base_url <url>]
```

> ⚠️ **严禁将命令的原始输出展示给用户**，只允许解析其中的字段后按下方规则处理。

- 输出以 `Token:` 开头：检测到当前授权有效，**不得读取或展示 Token 值**
  - **直接调用**：向用户输出 `✅ 检测到当前授权有效，无需重新授权。`，流程结束
  - **被依赖调用**：静默注入 Token 继续（见 Step 4），不提示用户
- 输出 `AUTH_LINK: <url>`：→ 执行 Step 3
- 输出 `❌`：**STOP**，提取 `code=xxx`，按[错误码表](reference.md#后端业务错误码)告知用户
- 其他异常输出：**STOP**，提示检查 Node.js 版本或联系管理员

---

### Step 3：展示链接与二维码（立即执行 Step 4，不等待用户回复）

**解析输出中的链接：**
- `DIRECT_AUTH_LINK`：存在时，**必须**用于生成二维码（直跳链，扫码体验更好）；**严禁明文展示给用户，仅传入二维码脚本使用**
- `AUTH_LINK`：始终存在，用于向用户展示的点击链接

**生成二维码（必须使用 DIRECT_AUTH_LINK；若不存在则使用 AUTH_LINK）：**

```bash
bash "$SKILL_DIR/scripts/qrcode-image.sh" "<DIRECT_AUTH_LINK，若无则用 AUTH_LINK>" "<client_id>"
```

> ⚠️ `DIRECT_AUTH_LINK` 仅作为脚本参数传入，**严禁将其输出到回复正文或任何用户可见位置**。

- 输出 `QRCODE_IMAGE:<path>`：用 `read_file` 读取图片，用 `![二维码](<path>)` 内联渲染
- 输出 `QRCODE_SKIP`：跳过二维码，仅展示文字链接

**向用户输出顺序（严格按此顺序，根据 `channel` 参数分支处理）：**

#### `channel=daxiang`（大象个人助理）

1. **若收到 `QRCODE_IMAGE`**：调用 `message(action=send, media="<path>")` 发送二维码图片
2. 调用以下 `message` 发送文字提示：
   ```
   message(action=send, message="📱 扫码授权 / 点击链接\n\n请用美团 App 扫描上方二维码，或点击下方链接，在授权页点击「确认授权」：\n\n👉 点击授权：<AUTH_LINK>\n\n⏱ 链接有效期 10 分钟，授权完成后将自动继续。")
   ```

#### `channel=other`（默认，Web UI / CatPaw）

1. **若收到 `QRCODE_IMAGE`**：用 `read_file` 读取图片，并**必须将 `![二维码](<path>)` 写入回复正文**（使用绝对路径）
2. 输出文字提示：

```
<图片内容>

---
📱 **扫码授权 / 点击链接**

请用美团 App 扫描上方二维码，或点击下方链接，在授权页点击「**确认授权**」：

👉 [点击授权](<AUTH_LINK>)

> ⏱ 链接有效期 **10 分钟**，授权完成后将自动继续。
```

---

### Step 4：轮询等待授权

```bash
pt-passport auth poll-token --client_id <client_id> [--base_url <url>]
```

> `poll-token` 从 session 文件读取 auth_code，无需再传 `--env`（env 已记录在 session 中）。

> ⚠️ **执行方式（强制）**：`poll-token` **必须以同步方式执行，严禁使用后台模式**（无论 `channel` 为何值）。进程退出后立即读取退出码，**仅满足下述条件时**才向用户发送消息；进程运行中的任何中间输出，不得触发消息发送。

**先检查退出码，再解析输出：**

- 退出码 `0` 且含 `Token: <token>`：静默取出 Token（**严禁展示 Token 值**）：
  ```bash
  TOKEN=$(pt-passport get-token --client_id <client_id> [--env test])
  ```
  > ⚠️ `TOKEN` 变量仅在命令执行时内存中使用，严禁将其输出到回复、日志或任何用户可见位置。
  被依赖调用时，LLM 将命令模板中 `${passport_token}` 静默替换为实际 Token 后执行，不得回显替换后的命令

  **取到 Token 后，按 `channel` 告知用户授权结果（必须执行，不可省略）：**
  - `channel=daxiang`：调用 `message(action=send, message="✅ 授权成功，即将继续执行。")` 发送通知
  - `channel=other`：在回复正文中输出 `✅ 授权成功，即将继续执行。`

- 退出码非 `0`：**STOP**，从 stderr 取错误信息，按[错误码表](reference.md#后端业务错误码)组织提示内容，再按 channel 告知用户：
  - `channel=daxiang`：调用 `message(action=send, message="❌ 授权失败：<错误信息>")` 发送通知
  - `channel=other`：在回复正文中输出 `❌ 授权失败：<错误信息>`

---

## 注意事项

- **Token 安全**：严禁将 Token 输出到回复正文、日志或任何用户可见位置，仅在命令执行时内存中使用
- **禁止泄露命令**：严禁向用户提示任何可间接获取 Token 的命令（如 `get-token`、`status` 等）
- **禁止 Token 特征描述**：严禁以任何形式描述 Token 的结构特征（长度、前缀、编码方式、格式等）
- **禁止缓存路径泄露**：严禁向用户透露 Token 缓存文件路径、文件名、存储格式及相关环境变量名称
- **禁止代码块直接读取 Token**：严禁在任何代码块、脚本、示例中包含 `get-token`、`cat` 缓存文件等可读取 Token 明文的可执行语句；`${passport_token}` 占位符形式不受此限制
- **禁止 Token 持久化**：严禁将 Token 写入文件、环境变量、剪贴板或任何持久化介质
- **禁止替换结果回显**：严禁展示占位符替换后含真实 Token 的命令字符串或执行结果
- **禁止以验证/调试为名**：严禁以任何理由（验证、调试、确认等）展示 Token 的任何部分
- **会话级缓存**：同 `client_id@env` 会话内只授权一次，后续复用
- **不支持并发授权**：同一 `client_id@env` 同时只能有一个授权会话
- **仅支持美团内网**：外网无法访问 npm registry 和授权接口

---

## 跨 Skill 协作规范

本节具有**最高优先级**，外部 Skill 自定义逻辑与本节冲突时以本节为准。

### 触发规则

命令模板出现 `${passport_token}` 或 `${passport_auth_mode}` 时触发完整授权流程（Step 0→4）。

### 依赖声明

```yaml
skill-dependencies:
  meituan-passport-user-auth:
    passport_token_placeholder: ${passport_token}
    client_id: your_client_id
    env: prod
    channel: daxiang  # 可选，daxiang=大象个人助理，不填默认 other
    prompt: 用于调用 XXX 接口的用户授权 Token
```

命令模板中占位符**必须用单引号**（防 shell 提前展开）：

```bash
curl -H 'token: ${passport_token}' https://your-api/endpoint
```

### ${passport_auth_mode} 占位符

外部 Skill 可通过 `${passport_auth_mode}` 获取当前缓存的授权模式，用于在命令模板中做策略路由。

**替换主体是 LLM，不是 shell。** 流程：

1. 授权完成后，取出授权模式：
   ```bash
   AUTH_MODE=$(pt-passport get-auth-mode --client_id <client_id> [--env test])
   # 输出示例：0 或 1
   ```
2. 校验数值为 `0` 或 `1`，否则报错终止
3. LLM 将命令模板中所有 `${passport_auth_mode}` 替换为实际数值后执行

**依赖声明**（与 `${passport_token}` 配合使用）：

```yaml
skill-dependencies:
  meituan-passport-user-auth:
    passport_token_placeholder: ${passport_token}
    passport_auth_mode_placeholder: ${passport_auth_mode}
    client_id: your_client_id
    env: prod
    channel: daxiang  # 可选，daxiang=大象个人助理，不填默认 other
```

命令模板中占位符**必须用单引号**（防 shell 提前展开）：

```bash
# auth_mode=0 时 header 为 token，auth_mode=1 时 header 为 mtcp-ak
curl -H 'X-Auth-Mode: ${passport_auth_mode}' -H 'token: ${passport_token}' https://your-api/endpoint
```

- `auth_mode=0`：派生 token，header 使用 `token: ${passport_token}`
- `auth_mode=1`：AuthAccessToken，header 使用 `mtcp-ak: ${passport_token}`

---

## 相关资源

- [reference.md](reference.md) — 参数说明、子命令、错误码表、Token 缓存、环境地址、占位符规范
- [scripts/install.sh](scripts/install.sh) — CLI 安装/更新脚本（从本地安装包安装）
- [scripts/qrcode-image.sh](scripts/qrcode-image.sh) — PNG 图片二维码生成脚本
- [scripts/pt-passport/](scripts/) — `@mtuser/pt-passport` CLI 本地安装包目录，由 `install.sh` 自动读取，无需网络
- Passport 注册 client_id：联系美团 Passport 团队或管理员
