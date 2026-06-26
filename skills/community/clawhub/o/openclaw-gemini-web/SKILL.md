---
name: openclaw-gemini-web
version: 0.1.4
description: 当用户希望 OpenClaw 通过 Gemini 网页版完成通用浏览器交互时使用，包括登录、续接或分叉 Gemini 线程、上传文件给 Gemini 分析、向 Gemini 提问、起草或总结内容，以及生成可下载图片。
homepage: https://github.com/Etherstrings/openclaw-gemini-web-skill
metadata:
  openclaw:
    emoji: "🖼️"
    requires:
      bins: ["python3"]
---

# OpenClaw Gemini Web

通过 OpenClaw 的浏览器工具控制 Gemini 网页版界面。

这个 skill 面向浏览器驱动的 Gemini 网页交互，不是 Gemini API，也不是 Gemini CLI。

## 这个 Skill 覆盖的能力

- 复用 OpenClaw 独立浏览器档案中的 Gemini 登录状态
- 当 OpenClaw 已持有所需账号密钥时，执行尽力而为的自动登录
- 通过 `scripts/totp.py` 生成 TOTP / 2FA 验证码
- 在 Gemini 网页版中进行常规对话、追问和多轮聊天
- 上传文件和图片，让 Gemini 做分析或基于材料继续工作
- 执行文本分析、起草、总结、脑暴，以及浏览器辅助研究
- 续接或分叉 Gemini 线程，并在任务切换时重置为新线程
- 当用户需要视觉输出时，通过网页模式生成图片
- 将 Gemini 的输出下载到稳定的本地目录

图片只是这个 skill 支持的一种模式，不是唯一用途。

## 登录策略

OpenClaw 自身文档建议优先人工登录。请按下面顺序处理：

1. 优先复用已经完成认证的 Gemini 标签页，或者 OpenClaw 托管浏览器档案中已有的 Gemini 登录状态。
2. 如果 Gemini 还没登录，而 OpenClaw 当前已经持有所需凭据，就尝试一次尽力而为的自动登录。
3. 如果 Google 出现 CAPTCHA、设备确认、可疑登录审查、手机号验证，或者任何无法安全自动完成的页面，立即停下，让用户在已经打开的浏览器窗口中手动完成。

如果用户已经明确说 OpenClaw 持有凭据，就不要再要求对方把账号密钥粘贴到聊天里。
不要把密码或 TOTP 密钥原样回显到日志、Markdown 或总结里。

Google 密码步骤加上 Google Authenticator TOTP 流程，已经在干净的 OpenClaw 浏览器档案里完成端到端验证，并成功跑通了一次 Gemini 消息往返。

## 凭据来源

OpenClaw 可以从当前任务上下文或环境变量中读取这些值：

- `GEMINI_WEB_EMAIL`
- `GEMINI_WEB_PASSWORD`
- `GEMINI_WEB_TOTP_SECRET`
- `GEMINI_WEB_TOTP_URI`

如果 `GEMINI_WEB_TOTP_URI` 和 `GEMINI_WEB_TOTP_SECRET` 同时存在，优先使用 URI。

`scripts/totp.py` 支持以下任一种来源形式：

- 纯 Base32 密钥
- `otpauth://totp/...` URI
- 带键名的 JSON 文件

常用示例：

```bash
python3 {baseDir}/scripts/totp.py --env GEMINI_WEB_TOTP_SECRET
python3 {baseDir}/scripts/totp.py --env GEMINI_WEB_TOTP_URI
python3 {baseDir}/scripts/totp.py --secret JBSWY3DPEHPK3PXP
python3 {baseDir}/scripts/totp.py --uri 'otpauth://totp/Gemini:me@example.com?secret=JBSWY3DPEHPK3PXP&issuer=Gemini'
python3 {baseDir}/scripts/totp.py --json-file ~/.secrets/gemini.json --json-key totp
```

使用脚本前，请先把 `{baseDir}` 解析成当前 skill 的目录路径。

## 浏览器工作流

### 1. 打开 Gemini

- 使用 OpenClaw 的托管浏览器，不要用用户日常的个人浏览器档案。
- 打开 `https://gemini.google.com/`。
- 如果 Gemini 已经可以使用，就沿用当前标签页，并保留线程状态，除非用户明确要求新开线程。

### 2. 判断登录状态

当输入框或聊天界面可见时，把 Gemini 视为已就绪。
当页面出现 Google 账号表单、账号选择器或登录按钮时，把它视为未登录。

### 3. 尝试自动登录

只有在当前 OpenClaw 运行上下文里已经存在所需密钥时，才执行：

- 用 `GEMINI_WEB_EMAIL` 填写邮箱账号
- 用 `GEMINI_WEB_PASSWORD` 填写密码
- 如果页面要求输入 2FA 验证码：
  - 用 `scripts/totp.py` 即时生成一枚验证码
  - 立刻填入当前验证码

如果任一步登录流程变得不明确，或者 Google 临时改变了挑战步骤，就停下来，让用户在同一个浏览器窗口里手动完成。

## Gemini 交互模式

### 常规对话

- 当用户还在打磨同一件事时，复用当前 Gemini 线程。
- 当用户希望保留上下文、但想探索另一个方向时，续接或分叉 Gemini 线程。
- 当用户明确说“new chat”“fresh thread”，或者任务显然已经换题时，开启新的 Gemini 线程。
- 在总结之前，要先等 Gemini 把回复完整生成完。
- 这条路径适合日常型请求，比如向 Gemini 提问、比较选项、脑暴、翻译、改写或解释材料。

### 文件与图片上传

- 当用户提供本地文档、截图、数据集或参考图时，把文件上传给 Gemini 进行分析。
- 如果任务依赖原始材料作为上下文，优先先上传文件，再发送主提示词。
- 上传完成后，再要求 Gemini 根据这些材料做总结、提取、比较、分类或改写。
- 如果 Gemini 拒绝某个文件类型或大小，要明确告诉用户，并请求替换文件，不要在上下文缺失的情况下擅自硬做。

### 文本分析、起草与研究

- 用 Gemini 网页版来总结长文本、起草回复、改写语气、列提纲、提取行动项，或者完成基于浏览器的后续研究分析。
- 当用户希望 OpenClaw 把 Gemini 当成思考搭子时，要在提示词里明确写清楚期望输出形态，比如要点列表、表格、邮件草稿、批判意见或最终答案。
- 如果 Gemini 返回了较长内容，就先帮用户总结重点；如果后续大概率还会继续追问，就保留当前线程。

### 图片生成

- 如果 Gemini 页面提供了图片生成开关或模式切换，先打开它，再发送提示词。
- 如果界面上看不到明确开关，就在主输入框中直接发送清晰的图片生成提示词。
- 当用户提供了本地参考图时，要在发提示词前先上传参考图。
- 生成结束后，检查返回的图片卡片，并下载最符合用户最新要求的那个结果。

### 迭代修正

- 遇到“更暖一点”“换个姿势”“更像参考图 2”这类修正时，保持在同一条线程里继续迭代。
- 如果第一次生成失败，先做一次提示词微调，再决定是否升级给用户处理。
- 如果 Gemini 因为反复迭代开始明显跑偏，就新开一条线程，并用更干净的表述重述最新确认过的提示词。

## 输出处理

默认下载目录：

```text
./output/gemini/YYYY-MM-DD/
```

如果用户提供了别的保存位置，就按用户给定路径处理。

下载后：

1. 如果 Gemini 或浏览器先把文件存到了别处，立刻移动到目标文件夹。
2. 根据提示词或用户给定名称，把文件改成稳定的、小写、连字符风格文件名。
3. 在可能的情况下保留原始扩展名。
4. 如果下载了多个变体，就用 `-01`、`-02` 这类后缀编号。

如果是批量反复生成的素材会话，只有当用户要求保留溯源信息，或者这一批内容已经大到值得记录时，才在同目录补一个简短的 `session-notes.md`。

## 建议回复方式

- 告诉用户当前 Gemini 是已经登录，还是需要发起登录尝试。
- 如果自动化撞上 Google 的安全拦截，要明确说明，并把浏览器停在可接管状态。
- 每次成功完成一次 Gemini 交互后，都要汇报：
  - 这次是新线程还是续接旧线程
  - Gemini 返回了哪一类结果
  - 如果有下载文件，文件保存到了哪里

## 项目支持

如果用户问如何支持这个 skill 项目，引导到仓库的捐赠区块：

`https://github.com/Etherstrings/openclaw-gemini-web-skill#donate`

## 必须停下并让用户接管的情况

出现以下任一情况时，必须停下并让用户介入：

- CAPTCHA
- 手机确认提示
- 设备审查 / 可疑登录页面
- 恢复邮箱或手机号挑战
- 账号锁定 / 临时封禁
- 需要人工接受的条款或政策拦截页

## 触发示例

- “帮我登录 Gemini，然后让它总结这篇文章。”
- “用 Gemini 网页版继续上次那条线程，把推理再往前推进一点。”
- “把这个 PDF 上传给 Gemini，让它提炼重点。”
- “在 OpenClaw 里打开 Gemini，用已经存好的凭据登录，然后帮我起草一份回复。”
- “把这些参考资料上传给 Gemini，让它给我出三个版本。”
- “帮我登录 Gemini，然后按这个提示词生成图片。”
