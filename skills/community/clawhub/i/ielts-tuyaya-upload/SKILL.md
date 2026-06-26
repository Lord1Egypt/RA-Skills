---
name: ielts-tuyaya-upload
description: "上传雅思阅读复盘文件到服务器，支持 token 模式（进个人主页）和匿名模式。当用户想要上传已有的复盘 JSON、查看个人复盘仪表板时使用。触发词：上传复盘、上传复盘文件、sync review、upload review、查看我的复盘记录、我的仪表板、dashboard、tuyaya 上传、批量同步。"
---

# IELTS Review Upload Skill

## Purpose

把已有的雅思阅读复盘 JSON 上传到 www.liuxue.online。支持两种通道：

| 模式 | 触发条件 | 通道 | 数据落点 | 适用 |
|---|---|---|---|---|
| **Token 模式（推荐）** | 设置了 `IELTS_USER_TOKEN` 环境变量 | `POST /api/ielts {action:'batchImport', token}` | 主库 + **进个人主页进度图/词汇本** | 登录用户（dengjiawei / lishuzhuo / 其他注册账号） |
| **匿名模式（兜底）** | 没有 token | `POST /ielts-api/skill-review` (x-api-key) | 匿名 dashboard 表 | 访客试用、未注册账号 |

**默认走 token 模式**。脚本会自动检测 `IELTS_USER_TOKEN`，没设置时 v1.3.0 起会**直接弹起浏览器授权页**让用户一键完成绑定（OAuth 风格），完全无需 F12。

## What's New in v1.3.2 — 域名迁移到 liuxue.online

**⚠️ v1.3.2（2026-06-23）**：旧域名 `tuyaya.online` 因 ICP 备案审核已全站 403 不可用，所有默认 API/授权/登录地址迁移到 `www.liuxue.online`。`sync-review.sh` / `upload.js` / `setup-client-mode.sh`（含 CORS Allow-Origin）默认值全部更新。**老用户必须 `clawhub install ielts-tuyaya-upload --force` 更新**，否则上传会撞旧域名 403 失败。已存的 token 仍有效，无需重新授权。

## What's New in v1.3.0 — 浏览器授权流

跟随 ielts-reading-review v5.4.0 升级：

- ❌ **告别 F12 复制 token**：不再需要打开 DevTools → Console 手动 `localStorage.ielts_user_token`
- ✅ **一键浏览器授权**：缺 token 时 `sync-review.sh` 自动调起 `setup-client-mode.sh` → 浏览器弹 `www.liuxue.online/authorize.html` → 点【授权】完事
- 🔒 **token 全程在本机**：通过 `<img src=http://127.0.0.1:port/cb?token=...>` 回传，不进 URL bar，不走第三方
- 🛡️ **CSRF 防护**：state 随机串 + 回调白名单（仅 127.0.0.1/localhost）
- 🪟 **三系统支持**：macOS `open` / Linux `xdg-open` / 兜底打印链接手动粘贴

## When to Activate

- 用户说"上传复盘"、"上传复盘文件"
- 用户说 "sync review"、"upload review"
- 用户想查看个人复盘仪表板
- 用户说"查看我的复盘记录"、"我的仪表板"

## Workflow

### Step 0: 确认 token 是否就位

第一步先检查 `IELTS_USER_TOKEN`：

```bash
echo "${IELTS_USER_TOKEN:0:20}..."  # 只显示前 20 位避免泄漏
```

- **有输出** → 走 token 模式，数据进个人主页 ✅
- **没输出** → 走 v1.3.0 浏览器授权流（OAuth 风格，30 秒搞定）：

```
你还没配置 IELTS_USER_TOKEN，上传后数据不会进个人主页进度图。

🔧 一键授权（推荐）：
bash ~/.workbuddy/skills/ielts-reading-review/scripts/setup-client-mode.sh

脚本会：
1. 在本机起一个随机端口的 HTTP 服务监听回调
2. 自动唤起浏览器到 www.liuxue.online/authorize.html
3. 你在网页点【授权】按钮，token 通过 <img> 请求回传到本机
4. 校验通过后写入 ~/.zshrc 并 source 生效
5. token 永远不离开你的电脑（不进 URL bar、不走第三方）

兜底（浏览器/网络异常时）：
bash setup-client-mode.sh --manual    # 走 F12 复制 token 老流程

要不要现在跑一下，还是先走匿名模式？
```

**v1.3.0 起 sync-review.sh 自动检测 token，没设置时直接调起 setup-client-mode.sh，全程不用手动复制。**

### Step 1: 收集 JSON 文件路径

询问用户要上传的 JSON 文件路径。

**JSON 格式支持两种**：

**扁平格式（最简）**：
```json
{
  "book": 5,
  "test": 4,
  "passage": 1,
  "score": 11,
  "total": 13,
  "date": "2026-04-09",
  "duration": 2050,
  "wrongQuestions": [3, 7, 12]
}
```

**v4.0 富格式（推荐，复盘 skill 直接产出）**：
```json
{
  "version": "4.0.0",
  "source": {"book": 5, "test": 4, "passage": 1, "title": "...", "titleCN": "..."},
  "score": {"correct": 11, "total": 13, "band": "6.5-7.0"},
  "timing": {"minutes": 34.2, "formatted": "34:10"},
  "date": "2026-04-09",
  "wrongQuestions": [...],
  "synonyms": [...],
  "vocabulary": [...]
}
```

服务端 schemaUpgrader 会自动识别富格式，无需手动转换。

### Step 2: 跑上传脚本

```bash
bash ~/.workbuddy/skills/ielts-review-upload/scripts/sync-review.sh <path-to-data.json>
```

**脚本行为**：
- 自动检测 `IELTS_USER_TOKEN`，决定走 token 还是匿名通道
- token 模式：包装成 batchImport payload，POST 到 `/api/ielts`
- 匿名模式：用 hostname+username SHA256 生成稳定 user id，POST 到 `/ielts-api/skill-review`
- 失败时打印明确错误（token 过期 / 字段缺失 / HTTP 错误）

**强制覆盖通道**：
```bash
bash sync-review.sh data.json --token-mode    # 强制走 token，没 token 直接报错
bash sync-review.sh data.json --anon-mode     # 强制走匿名（即使有 token）
```

### Step 3: 上传后告知查看入口

**Token 模式成功**：
```
✅ 上传成功！数据已进入你的个人主页。

📊 查看：https://www.liuxue.online/ielts/reading.html
（登录后能看到进度图、词汇本、错题本同步更新）
```

**匿名模式成功**：
```
✅ 上传成功（匿名）。

📊 你的专属看板：
https://www.liuxue.online/ielts-api/web/?user=<USER_ID>&key=<API_KEY>

⚠️ 此数据不在主站个人主页中。建议下次配置 IELTS_USER_TOKEN 以同步到主页。
```

### Step 4: 入库回查（仅 token 模式，可选但推荐）

```bash
curl -s https://www.liuxue.online/api/ielts \
  -H 'Content-Type: application/json' \
  -d "{\"action\":\"getReviews\",\"token\":\"$IELTS_USER_TOKEN\",\"book\":5,\"test\":4}" \
  | python3 -m json.tool
```

确认返回的 data 数组里有刚上传的篇目。

## Configuration

### Token（推荐，token 模式）

- 浏览器 `localStorage.token` 取，写入 `~/.zshrc`：
  ```bash
  export IELTS_USER_TOKEN='eyJ1Ijoi...'
  ```
- 也可以用 `~/.workbuddy/skills/ielts-reading-review/scripts/get-token.sh` 一键签发（如已部署）

### API Key（匿名模式 fallback）

脚本内置默认 API key：`ielts_8b0832b3cfd38884e44ab26ee68acaeed294623ef8da9b201871a7768b072606`

如需更换：
```bash
export IELTS_API_KEY='your_key_here'
```

### Backend URL

```bash
export IELTS_API_BASE='https://www.liuxue.online/api/ielts'        # token 模式
export IELTS_LEGACY_BASE='https://www.liuxue.online/ielts-api'     # 匿名模式
```

## Reference Files

| File | Purpose |
|------|---------|
| `scripts/sync-review.sh` | 双通道上传脚本（token + 匿名 fallback） |

## Troubleshooting

### "token 过期 / 401"

重新登录 www.liuxue.online 拿新 token，更新 `IELTS_USER_TOKEN`。

### "缺少 book/test/passage"

JSON 必须包含 `source.book`/`source.test`/`source.passage`（v4.0）或顶层 `book`/`test`/`passage`（扁平）。

### "Upload failed (HTTP 5xx)"

后端服务异常，先 ping 健康检查：
```bash
curl https://www.liuxue.online/api/health
```

### 数据没进个人主页

检查：
1. `echo $IELTS_USER_TOKEN` 是否真的有值（可能 `.zshrc` 没 source）
2. 脚本输出有没有 `Mode: token`，如果是 `Mode: anon` 则数据在匿名表里

## Style Guidelines

- 简洁直接，不要多余包装
- 默认推荐 token 模式，仅在用户明确要匿名或没条件配 token 时走 fallback
- 上传完成后必须打印查看入口
