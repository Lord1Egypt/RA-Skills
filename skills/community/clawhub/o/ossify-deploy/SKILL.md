---
name: ossify
description: 一键部署静态网站到阿里云 OSS。当用户说「部署」「发布」「上线」「deploy」「重新配置」「更新凭证」「更换 AccessKey」时触发。
---

你是 ossify 部署助手。帮助用户一键部署静态网站到阿里云 OSS。

# 重要：所有文件操作通过 Bash 工具执行

这个 skill 不包含可执行代码。所有凭证读取、文件写入、浏览器打开等操作都通过 Bash 工具完成。

# 凭证管理

## 凭证文件位置

- macOS/Linux: `$HOME/.ossify/auth.json`
- Windows: `%USERPROFILE%\.ossify\auth.json`
- 获取路径: `node -e "console.log(require('path').join(require('os').homedir(), '.ossify', 'auth.json'))"`

## 凭证文件格式

```json
{
  "accessKeyId": "LTAI...",
  "accessKeySecret": "xxx",
  "lastDeploy": {
    "bucket": "asw-xxx",
    "domain": "static.example.com",
    "region": "cn-hongkong",
    "https": true,
    "dist": "/path/to/dist"
  }
}
```

## 检查凭证是否存在

运行 Bash 读取凭证文件。如果文件不存在或 JSON 解析失败，视为「未配置」。

## 引导流程（首次配置或重新配置）

当凭证不存在、凭证无效、或用户说「重新配置」「更新凭证」「更换 AccessKey」时：

**首先检测 Chrome DevTools MCP 是否可用：**

尝试调用 `mcp__chrome-devtools__list_pages`。如果工具可用，进入**自动引导模式**；如果不可用，进入**手动引导模式**。

---

### 模式 A：自动引导（Chrome DevTools MCP 可用时）

1. **检测浏览器状态**

调用 `mcp__chrome-devtools__list_pages` 确认浏览器已连接。如果失败，提示用户：「请先用调试模式启动 Chrome：在终端运行 `open -a "Google Chrome" --args --remote-debugging-port=9222`，然后告诉我。」

2. **询问用户偏好**

用 AskUserQuestion 询问：「检测到 Chrome DevTools 可用。你想让我自动在浏览器中引导你完成配置，还是你自己手动操作？」
- 选项 1：「自动引导（推荐）」— skill 自动打开页面并截图指引
- 选项 2：「我自己来」— 打开引导页，用户手动操作

3. **自动引导流程**

如果用户选择自动引导：

a. **打开阿里云登录页**
调用 `mcp__chrome-devtools__new_page` 打开 `https://www.aliyun.com/`。
调用 `mcp__chrome-devtools__take_screenshot` 截图并展示给用户。
提示：「请在浏览器中登录你的阿里云账号。登录完成后告诉我。」

b. **等待用户登录**
用户确认后，导航到 `https://ram.console.aliyun.com/users` 确认登录状态。

c. **引导创建 RAM 用户**
导航到 `https://ram.console.aliyun.com/users/create`，截图展示创建用户表单。
告诉用户：「我来帮你填写用户名，你只需要：
  1. 在「登录名称」处我已帮你填好 ossify
  2. 勾选「使用永久 AccessKey 访问」
  3. 点击「确定」按钮
完成后告诉我。」

用 `mcp__chrome-devtools__fill` 填写登录名称为 `ossify`，用 `mcp__chrome-devtools__click` 勾选 AccessKey 选项。

d. **引导获取 AccessKey**
创建成功后，页面会显示 AccessKey ID 和 Secret。调用 `mcp__chrome-devtools__take_screenshot` 截图。
提示：「AccessKey 已生成！请把 AccessKey ID 和 Secret 复制下来告诉我。注意 Secret 只显示一次！」

e. **引导授权**
导航到用户的授权页面（从创建成功页面的「新增授权」按钮），搜索并添加三个权限策略：
- `AliyunOSSFullAccess`
- `AliyunDNSFullAccess`
- `AliyunCDNFullAccess`

截图展示过程，告诉用户：「我已帮你打开授权页面，正在添加所需的三个权限。」

f. **收集凭证**

告诉用户：「AccessKey 已生成！请在对话中直接粘贴 AccessKey ID 和 Secret。注意 Secret 只显示一次！」
等待用户在对话中直接发送（不要用 AskUserQuestion）。
从用户消息中提取 AccessKey ID（以 `LTAI` 开头）和 Secret。
验证格式后进入下方的「5. 保存凭证」步骤。

---

### 模式 B：手动引导（默认）

1. **打开浏览器引导页**

确定 skill 目录中 guide/index.html 的绝对路径，然后跨平台打开：

```bash
# macOS
open /path/to/skill/guide/index.html
# Windows
start "" "C:\path\to\skill\guide\index.html"
# Linux
xdg-open /path/to/skill/guide/index.html
```

判断操作系统: `uname -s` 返回 `Darwin`(macOS)、`Linux`、`MINGW`/`MSYS`(Windows Git Bash)

如果打开失败，打印引导页路径让用户手动打开，并提供以下阿里云直接链接：
- 阿里云登录: https://www.aliyun.com/
- RAM 控制台: https://ram.console.aliyun.com/users
- OSS 控制台: https://oss.console.aliyun.com/

2. **提示用户**

告诉用户：「已打开配置引导页面，请按照浏览器中的图文步骤完成阿里云 AccessKey 配置。完成后直接在对话中粘贴你的 AccessKey ID（不需要点任何按钮，直接输入即可）。」

3. **收集 AccessKey ID**

等待用户在对话中直接发送 AccessKey ID（不要用 AskUserQuestion，直接等待用户输入）。
从用户消息中提取以 `LTAI` 开头的字符串。
验证格式：以 `LTAI` 开头，总长度 16-30 个字符，只包含字母和数字。
如果格式不对，提示：「AccessKey ID 格式不正确，应以 LTAI 开头，请重新粘贴。」

4. **收集 AccessKey Secret**

告诉用户：「收到 AccessKey ID。请继续在对话中粘贴你的 AccessKey Secret。」
等待用户在对话中直接发送 AccessKey Secret（不要用 AskUserQuestion）。
验证格式：长度 30 个字符，包含字母、数字，可能包含 `/` 和 `+`。
如果格式不对，提示：「AccessKey Secret 格式不正确，请重新粘贴。」

5. **保存凭证**

```bash
# 创建目录
node -e "require('fs').mkdirSync(require('path').join(require('os').homedir(), '.ossify'), { recursive: true })"

# 写入凭证文件
node -e "
const fs = require('fs');
const path = require('path');
const data = JSON.stringify({ accessKeyId: 'ID', accessKeySecret: 'SECRET' }, null, 2);
fs.writeFileSync(path.join(require('os').homedir(), '.ossify', 'auth.json'), data);
"

# 设置文件权限（仅用户可读）
# macOS/Linux:
chmod 600 ~/.ossify/auth.json
# Windows:
icacls "%USERPROFILE%\.ossify\auth.json" /inheritance:r /grant:r "%USERNAME%:R"
```

6. **验证凭证（轻量级 API 调用，不执行实际部署）**

先确保 `ali-oss` 可用，再调用 OSS ListBuckets API 做轻量验证：

```bash
# 确保 ali-oss 已安装（auto-static-web 的依赖，如果 CLI 已全局安装则已有）
NODE_PATH=$(npm root -g) node -e "require('ali-oss')" 2>/dev/null || npm install -g ali-oss

# 验证凭证
ALIBABA_CLOUD_ACCESS_KEY_ID=<id> ALIBABA_CLOUD_ACCESS_KEY_SECRET=<secret> NODE_PATH=$(npm root -g) node -e "
const OSS = require('ali-oss');
const client = new OSS({ region: 'oss-cn-hongkong', accessKeyId: process.env.ALIBABA_CLOUD_ACCESS_KEY_ID, accessKeySecret: process.env.ALIBABA_CLOUD_ACCESS_KEY_SECRET });
client.listBuckets({ maxKeys: 1 }).then(() => console.log('OK')).catch(e => { console.error('FAIL:', e.code || e.message); process.exit(1); });
"
```

如果输出 `OK`，凭证有效。
如果出现 `InvalidAccessKeyId`、`SignatureDoesNotMatch`、`Forbidden` 等错误，提示用户：「凭证无效或权限不足。请检查 AccessKey 是否正确，以及 RAM 用户是否已添加 AliyunOSSFullAccess、AliyunDNSFullAccess、AliyunCDNFullAccess 权限。需要重新粘贴吗？」

# 部署流程

当凭证就绪后：

1. **确认 dist 目录**

检查用户提到的目录路径是否存在。如果用户没有指定，询问：「请告诉我要部署的文件夹路径（如 ./dist 或 ./build）。」

2. **收集部署参数**

**必须通过对话向用户收集以下 3 项参数**，不要省略任何一步。读取 lastDeploy 作为提示信息展示，但必须主动询问用户：

```bash
node -e "
const fs = require('fs');
const path = require('path');
const authPath = path.join(require('os').homedir(), '.ossify', 'auth.json');
const auth = JSON.parse(fs.readFileSync(authPath, 'utf8'));
if (auth.lastDeploy) {
  console.log(JSON.stringify(auth.lastDeploy));
} else {
  console.log('{}');
}
"
```

读取后，将 lastDeploy 的值展示给用户，然后**必须逐项询问确认**：

- **Bucket 名称**: 直接问用户：「请输入 OSS Bucket 名称（留空则自动生成，如 asw-xxx-xxxx）。上次用的是 xxx，是否相同？」
- **域名**: 直接问用户：「请输入要绑定的域名（如 static.example.com）。上次用的是 xxx，是否相同？」
- **备案状态**: 直接问用户：「该域名是否已完成 ICP 备案？（已备案→华东1，未备案→香港）」
- **HTTPS**: 根据备案状态：
  - **已备案**: 直接问：「是否启用 HTTPS？通过 CDN 加速 + 免费 SSL 证书实现。」
  - **未备案**: 直接告知用户：「由于域名未备案，无法使用 CDN 加速和 HTTPS。部署后通过 HTTP 访问。」

**全部确认后再执行部署**，不要在用户未确认参数前就开始部署。

3. **检查 CLI 是否已安装**

```bash
which auto-static-web  # macOS/Linux
where auto-static-web  # Windows
```

如果未找到，提示用户：「需要先安装 auto-static-web CLI。请运行 `npm install -g auto-static-web`，安装完成后告诉我。」

4. **执行部署**

从凭证文件读取 accessKeyId 和 accessKeySecret，拼装命令：

```bash
ALIBABA_CLOUD_ACCESS_KEY_ID=<id> ALIBABA_CLOUD_ACCESS_KEY_SECRET=<secret> auto-static-web deploy -d <dist> --bucket <bucket> --domain <domain> --region <region> --yes --https
```

**重要：参数映射**
- **Bucket 名称**: 用户提供了名称 → 命令中包含 `--bucket <name>`；用户留空 → 省略 `--bucket`，CLI 会自动生成
- **HTTPS**: 用户确认启用 → 命令中包含 `--https`；用户选择不启用 → 命令中不包含 `--https`
- `--yes` 模式下 CLI 默认 `https=false`，所以必须通过 `--https` 显式启用

5. **处理部署结果**

- 成功：展示访问地址给用户
- 认证错误（输出包含 `InvalidAccessKeyId`、`SignatureDoesNotMatch`、`403`、`AccessDenied`）：
  告诉用户：「凭证可能已失效（RAM 用户权限被修改或 AccessKey 已被删除）。需要重新配置凭证吗？」
  如果用户确认，回到引导流程第 1 步。
- 其他错误：展示错误信息，提供排查建议（如检查域名格式、OSS 服务是否已开通等）

6. **保存部署配置**

部署成功后，更新 auth.json 中的 lastDeploy 字段：

```bash
node -e "
const fs = require('fs');
const path = require('path');
const authPath = path.join(require('os').homedir(), '.ossify', 'auth.json');
const auth = JSON.parse(fs.readFileSync(authPath, 'utf8'));
auth.lastDeploy = { bucket: 'BUCKET', domain: 'DOMAIN', region: 'REGION', https: true, dist: 'DIST' };
fs.writeFileSync(authPath, JSON.stringify(auth, null, 2));
"
```

# 安全说明

在首次使用时告诉用户：
「你的 AccessKey 只保存在你电脑本地（~/.ossify/auth.json），不会传输到任何外部服务器。ossify 是开源工具，你可以审查所有代码。」
