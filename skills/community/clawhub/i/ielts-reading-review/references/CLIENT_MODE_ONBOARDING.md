# 👩‍🎓 给老婆/外部用户：跑通整套 Skill 复盘流程

这份文档教你怎么把 `ielts-reading-review` + `ielts-review-upload` 两个 Skill 跑成「客户端模式」，让 AI 帮你做完整复盘后**自动同步到你 www.liuxue.online 账号下的进度图、词汇本、错题本**。

> 不是给作者本人用的——作者机直接走 SSH 部署链路。这份文档专门给**没有 openclaw-tunnel SSH 凭据**的机器准备。

## 你能得到什么

- ✅ 发截图给 AI → AI 自动识别错题、生成富 JSON 复盘
- ✅ 复盘自动入库 → 网站首页进度图实时更新
- ✅ 词汇/错题/同义替换 → 自动同步到你账号下的复习本
- ✅ 不需要任何 SSH 知识、不需要碰服务器

## 前置条件

1. 已在 https://www.liuxue.online/ielts/login.html 注册账号（如 lishuzhuo）
2. 本机装了 WorkBuddy / CodeBuddy（能用 `Skill` 工具）
3. 装好 `ielts-reading-review` + `ielts-review-upload` 这两个 Skill

## 一次性配置（30 秒搞定）

```bash
bash ~/.workbuddy/skills/ielts-reading-review/scripts/setup-client-mode.sh
```

**这是浏览器授权流（v5.4 新版）**：
1. 脚本启动一个本地随机端口的 HTTP 服务（监听本机回调）
2. 自动打开浏览器到 `www.liuxue.online/authorize.html`
3. 在页面看到客户端信息卡片，点击 **「授权」**
4. token 经浏览器以 `<img>` 请求方式回传到本机（**永远不离开你的电脑**）
5. 脚本自动校验 + 写入 `~/.zshrc`，显示绑定的账号名

> 网络/浏览器异常时可手动跑兜底模式：`bash setup-client-mode.sh --manual`
> 这种情况下需要 F12 → Console → 输入 `localStorage.ielts_user_token` 复制 token 粘贴到终端。

完成后重开终端或 `source ~/.zshrc`。

**验证成功标志**：
```bash
echo "${IELTS_USER_TOKEN:0:20}..."   # 应该看到 eyJ1Ijoi... 之类的前缀
```

## 日常用法

直接对 AI 说：

```
复盘剑8 Test1 Passage2，错题截图：[贴图]，用时 32:15
```

AI 会自动：
1. 检测到客户端模式
2. 读截图识别错题（先报清单等你确认）
3. 生成富 JSON 复盘到本地（默认 `~/Documents/雅思复盘/`）
4. 通过 HTTPS batchImport 上传到你账号
5. 回查 getReviews 确认入库
6. 给你主页链接：`https://www.liuxue.online/ielts/reading.html`

## 数据归属

- 上传通道：`POST https://www.liuxue.online/api/ielts {action:'batchImport', token}`
- 数据落点：主库 `ielts_reviews` 表，`username` 字段 = 你的登录账号
- 主页效果：登录后能看到进度图、词汇本、错题本同步更新（和作者本人完全同等待遇）

## 限制（客户端模式做不到的）

- ❌ 不能部署复盘 JSON 文件到服务器，所以「复盘详情页」`review.html?file=...` 可能 404
  - **绕过**：把复盘 JSON 发给作者人工部署，或继续在本地查看
- ❌ 不能扩展词库（dict_full.json）/双语数据（bilingual_data.json）
  - **绕过**：作者机已预置 C4-C20 全量数据，C21+ 才需要扩展

但**首页进度图、词汇本、错题本完全可用**——这些数据都从数据库读，不依赖文件部署。

## 出问题怎么办

| 症状 | 解决 |
|---|---|
| `echo $IELTS_USER_TOKEN` 没输出 | `source ~/.zshrc` 或重开终端 |
| AI 说"token 过期" | 重新登录 www.liuxue.online，重跑 setup-client-mode.sh |
| 主页看不到新复盘 | 确认 AI 输出里有 `imported:1, upgraded:1`，没有就是 batchImport 没调通 |
| AI 误走 SSH 部署 | 检查 Step 0a 模式横幅，应该是「客户端模式」，否则升级 Skill |

## Token 安全

- token 默认有效期 10 年
- 写在本地 `~/.zshrc`，不要发到群里/截图给别人
- 怀疑泄漏可以登录后端管理页面手动重置（联系作者）
