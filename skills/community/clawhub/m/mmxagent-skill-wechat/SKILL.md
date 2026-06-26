---
name: mmxagent-skill-wechat
description: 连接个人微信（不是企业微信）。用户说"连接个人微信"、"接入个人微信"、"绑定个人微信"、"个人微信扫码"时使用本 skill。注意：如果用户说的是"企业微信"或"企微"，本 skill 不适用，请使用 wecom-connect skill。一旦匹配本 skill，必须严格按流程执行到底，不得跳步或自由发挥。
---

# 个人微信 Connect Skill

## ⚠️ 匹配规则（严格区分，不得混淆）

**本 skill 仅适用于个人微信，以下关键词触发：**
- "连接个人微信" / "接入个人微信" / "绑定个人微信"
- "个人微信扫码" / "微信扫码登录"
- "连接微信"（未带"企业"二字时，默认为个人微信）

**以下关键词不属于本 skill，禁止触发：**
- "企业微信" / "企微" / "wecom" / "WeCom" → 使用 wecom-connect skill

**一旦读取本 skill，必须严格按下方流程从第 0 步执行到底，不得跳步、不得自由发挥、不得读取其他文档。**

## 核心原则

- **严格按步骤走，不要加戏，不要自作聪明加额外命令。**
- **二维码相关步骤（第 2-3 步）速度优先！** 二维码有效期仅约 1 分钟，获取和生成二维码的命令用 `&&` 链起来一次执行。其他步骤（版本检测、插件安装、凭证写入等）可以分步执行，便于用户检查中间输出。
- **`qrcode_img_content` 是一个 URL 字符串，必须用 `qrcode` npm 库把它编码成 PNG 图片。** 这个 URL 指向的是网页不是图片，绝对禁止用 `curl -o` 直接下载。
- **二维码展示以本地 workspace 文件为主。** 优先引导用户打开 `~/workspace/weixin_qr.png`。如果用户环境不便打开本地文件，可使用 `upload_to_cdn` 作为辅助手段（注意：CDN 上传会将一次性授权二维码暴露到外部，仅在必要时使用）。
- **凭证写入前必须展示并确认。** 写入 token 等敏感信息到磁盘前，必须先向用户展示即将写入的内容（accountId、token 前 8 位 + 掩码、baseUrl、userId），等用户确认后再执行写入。
- **不要自动轮询。** 给完二维码等用户说"扫完了"再轮询。
- **不要手动改写 `openclaw.json`。**
- **运行时安装的包说明：** 本 skill 会在运行时通过 npm/npx 安装以下包：① `openclaw`（OpenClaw CLI 工具）来源 registry.npmmirror.com ② `@tencent-weixin/openclaw-weixin-cli`（腾讯官方微信插件）③ `qrcode`（二维码生成库，仅安装在 /tmp 临时目录）。执行前应确认用户信任这些包来源。

## 执行流程

### 第 0 步：检测 openclaw 版本，决定安装路径

```bash
openclaw --version 2>&1 | head -1
```

从输出中提取版本号（格式：`OpenClaw 2026.X.Y`），按以下规则分支：

| 条件 | 路径 |
|---|---|
| 版本 ≤ 2026.3.x（含 3.13） | **路径 A**：先升级插件，再升级 openclaw |
| 版本 > 2026.3.13（如 2026.3.23 及以上） | **路径 B**：先升级插件，再更新 openclaw 版本 |
| 未安装 / 命令不存在 | 告诉用户先安装 openclaw：`npm install -g openclaw@latest --registry=https://registry.npmmirror.com`，然后重新从第 0 步开始 |

---

### 第 1 步：安装插件（根据路径分支）

#### 路径 A：旧版本（≤ 2026.3.13）→ 先删旧插件，再装新插件，最后升级 openclaw

**1a. 检测并删除旧版微信插件（1 次 exec）：**

先检查是否已安装旧版微信插件，如果存在则必须先删除，否则新版插件安装会冲突：

```bash
openclaw plugin list 2>&1 | grep -i weixin
```

如果输出中包含 weixin 相关插件，则执行卸载：

```bash
openclaw plugin uninstall openclaw-weixin 2>&1
```

如果未检测到旧插件，跳过卸载直接进入 1b。

**1b. 安装最新版微信插件（1 次 exec）：**

```bash
npx -y @tencent-weixin/openclaw-weixin-cli@latest install 2>&1
```

**1c. 升级 openclaw 到最新版（1 次 exec）：**

```bash
npm install -g openclaw@latest --registry=https://registry.npmmirror.com 2>&1 | tail -3
```

升级完成后告知用户："旧插件已清理，新插件已安装，openclaw 已更新到最新版。"

#### 路径 B：较新版本（> 2026.3.13）→ 先升级插件，再更新 openclaw

**1a. 先安装/升级微信插件（1 次 exec）：**

```bash
npx -y @tencent-weixin/openclaw-weixin-cli@latest install 2>&1
```

**1b. 再升级 openclaw 到最新版（1 次 exec）：**

```bash
npm install -g openclaw@latest --registry=https://registry.npmmirror.com 2>&1 | tail -3
```

升级完成后告知用户："插件已安装，openclaw 已更新到最新版。"

---

两条路径安装完成后，输出包含 `success` 或 `installed` 关键词则继续；否则告知用户安装失败，需人工排查。

### 第 2 步：获取二维码（1 次 exec）

```bash
curl -s "https://ilinkai.weixin.qq.com/ilink/bot/get_bot_qrcode?bot_type=3"
```

从返回 JSON 提取：
- `qrcode` — 保存，轮询用
- `qrcode_img_content` — **这是一个 URL 字符串**，下一步用 `qrcode` npm 库将它编码为 PNG 图片

### 第 3 步：生成 PNG 并保存到 workspace

**二维码相关步骤需要快速完成（有效期约 1 分钟）。**

```bash
cd /tmp && npm install qrcode 2>/dev/null | tail -1
```

```bash
cd /tmp && node -e "const qr=require('qrcode'); qr.toFile('/tmp/weixin_qr.png','<qrcode_img_content>',{width:400,margin:2},(e)=>{if(e)console.error(e);else console.log('saved');})"
```

**保存到 workspace（必须执行）：**

```bash
cp /tmp/weixin_qr.png ~/workspace/weixin_qr.png
```

**CDN 上传（可选，仅在用户无法打开本地文件时使用）：**

⚠️ 注意：CDN 上传会将一次性授权二维码暴露到外部网络。仅在用户明确表示无法打开本地文件、或处于纯远程 chat 环境时才使用。

```
upload_to_cdn /tmp/weixin_qr.png
```

CDN 上传失败不阻塞流程，直接用 workspace 本地文件。

### 第 4 步：展示二维码，等用户扫码

**默认展示方式（本地文件优先）：**

---

## 微信扫码登录

二维码已生成并保存到 `~/workspace/weixin_qr.png`，请打开文件后用**微信**扫码。

**操作步骤：**
1. 打开 `~/workspace/weixin_qr.png` 文件
2. 用手机**微信** App 扫一扫
3. 在手机上确认登录
4. 扫完告诉我"ok"，我会继续后续步骤

⏱ 有效期：约 1 分钟，如果过期了告诉我"过期了"，我会立即生成新的二维码。

如果打开本地文件不方便，告诉我，我可以通过 CDN 上传后提供在线链接（注意：二维码会短暂暴露到外部网络）。

---

**如果用户要求 CDN 链接（已通过 upload_to_cdn 上传成功）：**

---

## 微信扫码登录

用**微信**扫一扫下面的二维码：

<CDN 图片 URL>

（本地备份：~/workspace/weixin_qr.png）

扫完告诉我"ok"，我会继续后续步骤。

⏱ 有效期：约 1 分钟，如果过期了告诉我"过期了"，我会立即生成新的二维码。

---

然后**停下来，等用户确认**。

### 第 5 步：用户确认后 → 轮询 + 写凭证 + 重启

**5a. 轮询状态（必须加 `--max-time 10`，此 API 是长轮询）：**

```bash
curl -s --max-time 10 "https://ilinkai.weixin.qq.com/ilink/bot/get_qrcode_status?qrcode=<qrcode>"
```

| status | 处理 |
|---|---|
| 超时（exit code 28）或 `wait` | 等 3 秒再 poll |
| `scaned` | 告诉用户"已扫码，请在手机上确认登录" |
| `confirmed` | 成功！提取 `ilink_bot_id`、`bot_token`、`baseurl`、`ilink_user_id` |
| `expired` | 从第 2 步重来（不需要重新装插件） |

**5b. 展示凭证并等待用户确认（confirmed 后必须执行）：**

将 `ilink_bot_id` 中的 `@` → `-`、`.` → `-` 得到 `accountId`（例：`a34b410e2e6f@im.bot` → `a34b410e2e6f-im-bot`）。

⚠️ **API 返回的 `bot_token` 已包含 `ilink_bot_id:` 前缀，直接用 `bot_token` 的值作为 token，不要再拼接 `ilink_bot_id:`，否则 token 双重前缀、认证失败（errcode -14）。**

**先向用户展示即将写入的凭证信息，等待确认：**

---

## 即将写入以下凭证

| 字段 | 值 |
|---|---|
| accountId | `<accountId>` |
| token | `<bot_token 前 8 位>****（已脱敏）` |
| baseUrl | `<baseurl>` |
| userId | `<ilink_user_id>` |

写入位置：`~/.openclaw/openclaw-weixin/accounts/<accountId>.json`

确认写入请回复"ok"，如有疑问请告诉我。

---

**用户确认后，执行写入：**

```bash
cat > /tmp/write_weixin_account.js << 'SCRIPT'
const fs = require('fs');
const path = require('path');
const home = process.env.HOME;

const accountId = '<accountId>';
const data = {
  token: '<bot_token>',
  savedAt: new Date().toISOString(),
  baseUrl: '<baseurl>',
  userId: '<ilink_user_id>'
};

const accountsDir = path.join(home, '.openclaw/openclaw-weixin/accounts');
fs.mkdirSync(accountsDir, { recursive: true });

const accountFile = path.join(accountsDir, accountId + '.json');
fs.writeFileSync(accountFile, JSON.stringify(data, null, 2));
fs.chmodSync(accountFile, 0o600);

const indexPath = path.join(home, '.openclaw/openclaw-weixin/accounts.json');
let existing = [];
try { existing = JSON.parse(fs.readFileSync(indexPath, 'utf-8')); } catch {}
if (!existing.includes(accountId)) existing.push(accountId);
fs.writeFileSync(indexPath, JSON.stringify(existing, null, 2));

console.log('凭证 + 索引写入成功');
SCRIPT
node /tmp/write_weixin_account.js
```

⚠️ `<accountId>`、`<bot_token>`、`<baseurl>`、`<ilink_user_id>` 是占位符，写入脚本时必须替换为 5a 步 confirmed 返回的真实值。

**5c. 重启 Gateway：**

```bash
openclaw gateway restart
```

### 成功回复

---

## 微信连接结果

- ✅ 状态：已绑定成功
- ✅ Gateway：已重启
- ilink_bot_id: `<ilink_bot_id>`
- ilink_user_id: `<ilink_user_id>`

现在可以直接在微信里发消息了 🎉

---

到此为止。不要再做任何额外操作。不要读文档。

## 二维码过期处理

用户说"过期了" → 只需从第 2 步重新获取二维码，**不需要重新执行第 0、1 步**。

## 绝对禁止

- ❌ **禁止用 `curl -o` / `curl --output` / `wget` 下载 `qrcode_img_content` URL** — 这个 URL 指向的是 HTML 网页不是 PNG 图片，下载得到的是一堆 HTML 代码。必须用 `qrcode` npm 库的 `toFile()` 将 URL 字符串编码为 PNG
- ❌ **禁止用 canvas、browser、Generate Images、Image Understanding、MEDIA: 语法、终端字符渲染等方式展示二维码**
- ❌ 禁止自动开轮询（等用户说"扫完了 / ok"）
- ❌ 禁止手动改写 `openclaw.json`
- ❌ 禁止跳过写凭证步骤（不写凭证插件无法连接）
- ❌ 禁止给用户 `qrcode_img_content` 原始 URL
- ❌ 禁止使用第三方上传服务（0x0.st、catbox、imgbb 等），CDN 仅限 `upload_to_cdn`
- ❌ 禁止在 token 前拼接 `ilink_bot_id:`（bot_token 已包含前缀）
- ❌ 禁止在 PNG 生成成功后再用 curl 下载覆盖文件
- ❌ 禁止跳过第 0 步版本检测直接进第 1 步
- ❌ 禁止跳过凭证展示确认步骤直接写入磁盘

## 一句话总结

检测版本（第 0 步）→ 先删旧插件（如有）再装新插件再更新 openclaw（第 1 步）→ curl 拿二维码（第 2 步）→ npm install qrcode + 生成 PNG → 保存到 workspace（+ 可选 CDN 上传）（第 3 步）→ 展示二维码等用户扫（第 4 步）→ 轮询确认 → 展示凭证等用户确认 → 写凭证 → 重启 gateway（第 5 步）→ 完成。
