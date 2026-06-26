---
name: meituan-passport-user-auth
description: 美团 Passport 用户授权登录 Skill。通过 pt-passport CLI 获取授权链接，展示给用户完成确认后轮询拿到鉴权凭证（用户态登录 Token）。适用场景：(1) 用户主动触发美团授权登录；(2) 其他 Skill 命令模板中出现 ${passport_token} 占位符时自动被依赖调用，Token 透明注入，无需用户感知。不适用于服务端 AppKey/Secret 鉴权或非美团系统授权。触发词：美团授权登录、获取授权码、获取 token、token 授权、passport 登录、触发登录、美团登录、重新授权、强制刷新 token、meituan passport auth、${passport_token}。

metadata:
  skillhub.creator: "suntiansheng"
  skillhub.updater: "suntiansheng"
  skillhub.version: "V17"
  skillhub.source: "FRIDAY Skillhub"
  skillhub.skill_id: "22364"
  skillhub.high_sensitive: "false"
---

## [MANDATORY] SKILLHUB_METRIC_REPORTER_START
执行本 Skill 的任何操作之前，必须先执行 Skill：`skill-metric-reporter`。
按照 `skill-metric-reporter` 的要求完成 `skill_start` 上报后，才可继续本 Skill 正文。
本 Skill 全部操作完成后，同样按照 `skill-metric-reporter` 的要求完成 `skill_end` 上报。
## [MANDATORY] SKILLHUB_METRIC_REPORTER_END

# 美团 Passport 用户授权登录

## 概述

通过 `pt-passport` CLI 完成美团 Passport 授权，获取用户鉴权 Token。支持两种模式：

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
- `No local tgz bundle found`：**STOP**，提示 skill 安装包缺失，请重新安装此 Skill
- 其他失败：**STOP**，提示联系管理员

---

### Step 1：确认参数

按优先级解析，找到即用，不追问：

| 参数         | 优先级来源                                      | 缺失时        |
| ------------ | ----------------------------------------------- | ------------- |
| `client_id`  | ① `skill-dependencies.*.client_id` → ② 用户提供 | **STOP** 索要 |
| `env`        | ① `skill-dependencies.*.env` → ② 用户说「test」 | 默认 `prod`   |
| `--force`    | 用户说「重新授权」「强制刷新」「忽略缓存」      | 不加          |
| `--base_url` | 用户说「泳道」或提供 URL（优先级高于 `--env`）  | 不加          |

**环境一致性约束**：`client_id` 与 `env` 必须属同一环境，混用则 **STOP**：

```
❌ 环境与 client_id 不匹配：当前环境为 <env>，但 client_id 可能属于另一环境，请确认后重试。
```

---

### Step 2：运行授权脚本

**先尝试缓存（未使用 `--force` 时）：**

```bash
pt-passport get-token --client_id <client_id> [--env test]
```

> `get-token` 仅读本地缓存文件，不调用任何后端接口。先执行此步可在缓存命中时完全跳过 `auth get-code`，避免不必要的后端请求。

- 退出码 `0`：缓存命中 → 直接调用输出 `✅ 您已完成过授权。`；被依赖调用则注入 Token 继续
- 退出码 `1`：无缓存，继续发起授权

**发起授权：**

```bash
pt-passport auth get-code --client_id <client_id> [--env test] [--force] [--base_url <url>]
```

- 输出 `Token: <token>`：缓存命中，同上处理
- 输出 `AUTH_LINK: <url>`：→ 执行 Step 3
- 输出 `❌`：**STOP**，提取 `code=xxx`，按[错误码表](reference.md#后端业务错误码)告知用户
- 其他异常输出：**STOP**，提示检查 Node.js 版本或联系管理员

---

### Step 3：展示链接与二维码（立即执行 Step 4，不等待用户回复）

**生成二维码：**

```bash
bash "$SKILL_DIR/scripts/qrcode.sh" "<url>" "<client_id>"
```

- 输出 `QRCODE_IMAGE:<path>`：用 `read_file` 读取该图片（供视觉分析），**同时在回复正文中用 Markdown 图片语法 `![二维码](<path>)` 将图片内联渲染给用户**（同 `client_id` 每次覆盖同一文件）
- 输出 `QRCODE_TEXT:<qr>`：提取 `QRCODE_TEXT:` 之后的内容，**用代码块（三个反引号）包裹后原样输出**（代码块内天然等宽、无行间距；开头反引号后紧跟换行，二维码内容顶行开始，结尾反引号单独一行，中间不得插入任何空行）
- 输出 `QRCODE_SKIP`：跳过二维码，仅展示文字链接

**向用户输出顺序（严格按此顺序）：**

1. **若收到 `QRCODE_IMAGE`**：用 `read_file` 读取图片后，**必须将 `![二维码](<path>)` 写入回复正文**（使用绝对路径）——这是图片在聊天框中可见的唯一方式；⚠️ 仅调用 `read_file` 而不输出此标签，图片**不会显示**
2. **若收到 `QRCODE_TEXT`**：用代码块（三个反引号）原样包裹字符二维码，格式如下——开头 ` ``` ` 后**立即换行**，首行即为二维码第一行，结尾 ` ``` ` 独占一行，**全程不得插入空行**（`<pre>` 标签或 Markdown 列表/引用嵌套均会引入行间距，导致无法扫码）
3. **再输出文字提示**

首次授权（未使用 `--force`）的文字提示：

```
<图片或字符二维码内容>

---
📱 **扫码授权 / 点击链接**

请用美团 App 扫描上方二维码，或点击下方链接，在授权页点击「**确认授权**」：

👉 [点击授权](<url>)

> ⏱ 链接有效期 **10 分钟**，授权完成后将自动继续。
```

强制重新授权（使用了 `--force`）的文字提示：

```
<图片或字符二维码内容>

---
🔄 **授权已过期，需要重新授权**

请用美团 App 扫描上方二维码，或点击下方链接，在授权页点击「**确认授权**」：

👉 [点击授权](<url>)

> ⏱ 链接有效期 **10 分钟**，授权完成后将自动继续。
```

---

### Step 4：轮询等待授权

```bash
pt-passport auth poll-token --client_id <client_id> [--base_url <url>]
```

> `poll-token` 从 session 文件读取 auth_code，无需再传 `--env`（env 已记录在 session 中）。

**先检查退出码，再解析输出：**

- 退出码 `0` 且含 `Token: <token>`：输出 `✅ 授权成功。`，取出 Token：
  ```bash
  TOKEN=$(pt-passport get-token --client_id <client_id> [--env test])
  ```
  被依赖调用时，LLM 将命令模板中所有 `${passport_token}` 替换为实际 Token 后执行（详见[占位符规范](reference.md#占位符替换规则)）
- 退出码非 `0`：**STOP**，按[错误码表](reference.md#后端业务错误码)告知用户

---

## 注意事项

- **Token 安全**：严禁输出到回复正文、日志或任何用户可见位置，仅用于 HTTP 请求头/参数
- **会话级缓存**：同 `client_id@env` 会话内只授权一次，后续复用（详见 [reference.md](reference.md#token-缓存)）
- **不支持并发授权**：同一 `client_id@env` 同时只能有一个授权会话
- **仅支持美团内网**：外网无法访问 npm registry 和授权接口

---

## 跨 Skill 协作规范

本节具有**最高优先级**，外部 Skill 自定义逻辑与本节冲突时以本节为准。

### 触发规则

命令模板出现 `${passport_token}` 时触发完整授权流程（Step 0→4）。触发时机：先生成含占位符的业务命令，用户确认后再取 Token 替换（**延迟触发**）。

### 依赖声明

```yaml
skill-dependencies:
  meituan-passport-user-auth:
    passport_token_placeholder: ${passport_token} # 必填，固定值
    client_id: your_client_id # 必填
    env: prod # 可选，默认 prod
    prompt: 用于调用 XXX 接口的用户授权 Token # 可选
```

命令模板中占位符**必须用单引号**（防 shell 提前展开）：

```bash
curl -H 'token: ${passport_token}' https://your-api/endpoint
```

详细替换规则、多占位符处理、错误处理见 [reference.md#跨-skill-协作](reference.md#跨-skill-协作)。

---

## 相关资源

- [reference.md](reference.md) — 参数说明、子命令、错误码表、Token 缓存、环境地址、占位符规范
- [scripts/install.sh](scripts/install.sh) — CLI 安装/更新脚本（从本地安装包安装）
- [scripts/qrcode.sh](scripts/qrcode.sh) — 二维码生成脚本
- [scripts/mtuser-pt-passport-\*.tgz](scripts/) — `@mtuser/pt-passport` CLI 本地安装包，由 `install.sh` 自动读取，无需网络
- Passport 注册 client_id：联系美团 Passport 团队或管理员
