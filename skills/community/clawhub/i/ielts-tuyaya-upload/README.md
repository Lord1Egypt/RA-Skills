# IELTS Tuyaya Upload

把本地雅思阅读复盘 JSON 一键上传到 [www.liuxue.online](https://www.liuxue.online/ielts/)，告别手动拖文件。

## 🆕 v1.3.0 — 浏览器一键授权（告别 F12）

跟随 `ielts-reading-review` v5.4.0 同步升级，**绑定账号体验彻底重做**：

| 旧流程 (≤v1.2) | 新流程 (v1.3+) |
|---|---|
| 打开 www.liuxue.online 登录 | 同左 |
| F12 → Console → `localStorage.ielts_user_token` | ❌ 不再需要 |
| 手动复制 token 字符串 | ❌ 不再需要 |
| 打开 ~/.zshrc 手动 `export IELTS_USER_TOKEN=...` | ❌ 不再需要 |
| `source ~/.zshrc` | ❌ 不再需要 |
| —— | ✅ 浏览器弹授权页，点一下【授权】完事 |

**触发方式**：跑任何上传命令（如 `node scripts/upload.js --batch xxx`），脚本检测到没设 `IELTS_USER_TOKEN` 就会自动调起 `setup-client-mode.sh`，几秒后浏览器弹出 OAuth 风格的授权卡片。

**安全保障**：
- token 通过 `<img src=http://127.0.0.1:随机端口/cb?token=...>` 回传到本机，永远不离开你的电脑
- 回调地址白名单：仅接受 `127.0.0.1 / localhost / ::1`
- CSRF state 校验：每次启动随机生成 16 字节，防止跨站攻击
- token 不进浏览器 URL bar、不走第三方服务器

如果浏览器异常，可手动跑 `bash setup-client-mode.sh --manual` 走 F12 老流程兜底。

---

## 适合谁用？

- 用 `ielts-reading-review` skill 生成了一堆 JSON 复盘文件
- 想把成绩同步到 www.liuxue.online 云端，在任何设备打开网页查看
- 不想手动一个个拖到 submit 页面
- 有一堆旧笔记（HTML/Markdown/截图）想一次性导入成绩看趋势图

## 🚀 端到端一条龙（推荐）

如果你的复盘还是散在文件夹里的旧笔记，推荐配合 `ielts-reading-review` v3.4.0+ 一起用：**自动扫 → 生成 JSON → 自动上传**，一条 prompt 搞定。

### Step 1：装两个 skill（只做一次）

```bash
clawhub install ielts-reading-review
clawhub install ielts-tuyaya-upload
```

### Step 2：把下面这段 prompt 整段发给你的 AI Buddy

**不用改任何内容，复制粘贴直接发就行。**

```
帮我一条龙处理我的历史雅思复盘。

流程：

【A. 自动找复盘文件夹】
1. 用 ielts-reading-review skill 的 scan-legacy-reviews.js --auto 扫我电脑常见位置
2. 把推荐目录和其他候选报给我，让我确认用哪个

【B. 生成 JSON】
3. 对确认后的目录做深扫（--deep），列出识别到的篇目清单，让我再确认一次
4. 逐篇生成 v3.0 schema 的 JSON，输出到 ./batch-output/
5. 字段缺失的地方不要瞎编，缺就置空
6. 汇报成功几篇、数据缺失几篇

【C. 上传到 www.liuxue.online】
7. 用 ielts-tuyaya-upload skill 检查登录状态（--whoami）
   - 如果我还没账号：引导我 --register 注册（我会自己输入用户名密码）
   - 如果已登录：继续
8. 先跑 --diff ./batch-output/ 给我看差量（哪些是新的、哪些服务器已有）
9. 我确认后，跑 --batch ./batch-output/ 批量上传
10. 上传完告诉我成功几条，给我 https://www.liuxue.online/ielts/ 的链接让我去看成绩

规则：
- 每一步之间要停下来等我确认，别一口气全跑完
- 注册/登录时让我自己在终端输入密码，你不要替我生成
- 上传过程中有失败的，列出来让我决定要不要重试
```

### Step 3：按 Buddy 提示逐步确认

AI 会每一步停下来让你确认：路径对不对 → 篇目清单对不对 → 上传差量对不对 → 最后给你成绩链接。

### 全流程示意

```
  你      ─▶  我发 prompt
                │
                ▼
  Buddy   ─▶  🔍 auto 扫电脑
                │
                ▼
  你      ─▶  确认"用这个目录"
                │
                ▼
  Buddy   ─▶  📂 深扫列出所有篇目
                │
                ▼
  你      ─▶  确认"篇目没错"
                │
                ▼
  Buddy   ─▶  ✍️  逐篇生成 JSON 到 batch-output/
                │
                ▼
  Buddy   ─▶  🔑 检查 tuyaya 账号
                │
                ▼
  你      ─▶  （首次）注册账号 / 已有直接登录
                │
                ▼
  Buddy   ─▶  📊 diff 差量给你看
                │
                ▼
  你      ─▶  "上传吧"
                │
                ▼
  Buddy   ─▶  🚀 批量上传
                │
                ▼
  你      ─▶  🎯 去 www.liuxue.online 看成绩
```

### 各阶段预计耗时

| 阶段 | 时间 |
|------|------|
| 🔍 自动发现 | 3-5 秒 |
| 📂 深扫 + 确认篇目 | 10-30 秒 |
| ✍️ 生成 JSON（每篇） | 1-3 分钟 |
| 🔑 注册/登录（首次） | 30 秒 |
| 📊 diff | 5 秒 |
| 🚀 批量上传 | 每篇 1-2 秒 |

**实际示例**：20 篇老复盘，从头到尾约 30-50 分钟。

---

## 🔧 只用本 skill（已经有 JSON 了）

如果 `./batch-output/` 或 `./history-json/` 已经有生成好的 JSON，直接走这套：

### Step 1：绑定账号（首次）

**v1.3.0 推荐 — 浏览器一键授权**：

```bash
bash ~/.workbuddy/skills/ielts-reading-review/scripts/setup-client-mode.sh
```

脚本自动起本地服务 → 弹浏览器到授权页 → 点【授权】 → token 写入 `~/.zshrc`，30 秒搞定。

或直接跑上传命令，没 token 时会自动触发授权流：

```bash
bash ~/.workbuddy/skills/ielts-tuyaya-upload/scripts/sync-review.sh data.json
```

**老流程（兜底）— CLI 注册/登录**：

```bash
node scripts/upload.js --register   # 全新注册
node scripts/upload.js --login      # 已有账号
```

按提示输入用户名、密码、昵称。注册成功后自动登录。

### Step 2：批量上传

```bash
node scripts/upload.js --batch ./batch-output/
```

脚本会自动跳过服务器上已有的记录，只上传新的。

### Step 3：查看成绩

打开 https://www.liuxue.online/ielts/ 登录，所有成绩已在云端。

---

## 所有命令

```
node scripts/upload.js --register        # 注册新账号
node scripts/upload.js --login           # 登录
node scripts/upload.js --logout          # 退出
node scripts/upload.js --whoami          # 查看当前账号

node scripts/upload.js --batch <dir>     # 批量上传目录下所有 JSON
node scripts/upload.js <file.json>       # 上传单个 JSON
node scripts/upload.js --diff <dir>      # 对比本地和服务器差量
node scripts/upload.js --status          # 查看服务器上的成绩
```

---

## 踩坑提示

### 🟢 AI Buddy 能自动搞定

- 自动找到你的复盘文件夹（不管在桌面、文档、下载还是 iCloud）
- 识别篇目（文件名有"剑X-TestX-PassageX"就能认出来）
- 正确答案核验（查本地答案库）
- 多文件合并（同一篇有 HTML + 截图 + MD，会合并读）
- 注册登录（你跟着提示输入就行）
- 差量上传（服务器已有的不会重复上传）

### 🟡 它可能搞不定的（需要你补充）

- **文件名没有篇目信息**：比如 `笔记-20260315.docx`，会标为 "__unknown__" 让你分配
- **答案是手写拍照**：AI 识别手写可能有误，生成后扫一眼 JSON 里的 `score.correct` 对不对
- **错题分析太简略**：老笔记只写了 "Q3错了" 没写原因，`wrongQuestions[].analysis` 会是空的（成绩单数据不受影响）

### 🔴 一定不能干的

- 不要一口气喂超过 50 篇，容易超时。分批跑，每次 10-20 篇
- AI 问你确认时**别秒回 yes**，扫一眼清单对不对
- 注册密码别用 123456，≥6 位就行但别太水

---

## 常见问题

**Q: Token 过期了怎么办？**
A: Token 有效期 10 年（v5.1+），过期后重跑 `bash setup-client-mode.sh` 浏览器授权一下即可。

**Q: 每台电脑都要授权一次吗？**
A: 是的。token 只存本机 `~/.zshrc`，换电脑重跑一次 setup-client-mode.sh 就好。授权流支持记住浏览器登录态，所以二次授权基本是「点一下按钮」的事。

**Q: 浏览器授权安全吗？token 会泄漏到第三方吗？**
A: 不会。技术细节：
- 本机起 HTTP 服务监听 `127.0.0.1:随机端口`，授权页通过 `<img>` 请求把 token 回传
- 回调白名单：服务端校验 callback 必须是 127.0.0.1 / localhost / ::1
- CSRF state 校验：每次会话生成 16 字节随机串，防止跨站攻击
- token 不进 URL bar、不走任何第三方服务器，全程仅你浏览器 ↔ 本机进程

**Q: 数据存在哪？**
A: Token 存在 `~/.ielts-tuyaya-token`（权限 0600，只有自己可读）。成绩数据存在 www.liuxue.online 服务器。

**Q: 可以多账号切换吗？**
A: 可以。`--logout` 退出后 `--login` 另一个账号即可。

**Q: 忘记密码？**
A: 目前暂不支持找回，用 `--register` 注册新账号。

**Q: 换电脑了，token 还有效吗？**
A: token 只在本机保存。换电脑跑一次 `--login` 重新登录就行。

**Q: 注册 tuyaya 账号要手机号/邮箱吗？**
A: 不要。就用户名 + 密码，完全独立于其他平台。

**Q: 上传过程中失败了会重试吗？**
A: 同一篇重复上传会自动覆盖。失败的 buddy 会列给你，你说"重试失败的"就行。

**Q: 笔记里只写了错题编号（比如 "Q3/Q7 错了"），没详细分析，能用吗？**
A: 能。JSON 会生成基础成绩单（对 X 道/共 Y 道/band 分数），错题分析留空。以后想补细节，再拿着这篇原文找 AI 重新做。

**Q: 批量跑完，哪些数据会显示在网站上？**
A: 成绩单（每篇对多少道、分数）、错题列表、词汇、同义替换——全部同步。进度图、历史趋势图自动刷新。

---

## 依赖

- Node.js ≥ 18（有原生 fetch）
- 无需 npm install，纯 Node 标准库

## 相关

- [www.liuxue.online/ielts](https://www.liuxue.online/ielts/) — 你的雅思进度可视化主页
- `ielts-reading-review` skill — 生成复盘 JSON 的配套工具（配合用最爽）

---

祝复盘愉快 🎯
