# mbti-from-ai

分析用户与 AI 的聊天历史，根据沟通方式和思维模式推断 MBTI 人格类型，生成结构化 JSON 并在网页上展示可视化画像。

## 🔒 隐私与安全

### 数据流向

```
~/.openclaw/ 会话文件
        ↓ [本地读取]
_mbti_work/user_messages.txt（提取的用户消息）
        ↓ [Agent 的 LLM 后端分析]
_mbti_work/result.json（脱敏的结构化 JSON）
        ↓ [Base64 编码放入 URL Hash]
浏览器打开 https://www.mingxi.tech/#data=<base64>
        ↓ [浏览器本地 JS 解析渲染]
可视化 MBTI 画像
```

### 常见疑问

**Q: 脚本会上传我的对话到外部服务器吗？**

A: 不会。脚本只做本地文件读取和文本处理。没有任何 `curl POST`、`fetch`、`XMLHttpRequest` 等网络请求。你可以审查所有脚本源码确认。

**Q: 分析过程中我的消息会发送到哪里？**

A: MBTI 分析由你当前使用的 OpenClaw Agent 执行，消息会经过你 Agent 配置的 LLM 后端（如 Claude API）。这与你日常使用 OpenClaw 对话完全一致——本 skill 没有引入任何额外的数据发送路径。

**Q: 打开 `https://www.mingxi.tech/` 会泄露我的数据吗？**

A: 不会。原因如下：
- 数据放在 URL Hash（`#data=...`）中，**Hash 部分不会被浏览器发送到服务器**（这是 HTTP/HTTPS 协议规范，[RFC 3986 §3.5](https://datatracker.ietf.org/doc/html/rfc3986#section-3.5)）
- 该网页是**纯静态单文件 HTML**，无后端服务器、无数据库、无登录系统、无 cookie
- 页面仅包含 Google Analytics 用于匿名访问量统计，不采集 Hash 数据
- 页面的 JavaScript 只做一件事：从 `location.hash` 读取 Base64 → 解码为 JSON → 渲染图表
- 本 skill 的所有脚本源码完全开放，你可以审查每一行代码确认没有任何数据外传行为

**Q: `result.json` 里包含什么？**

A: 仅包含脱敏的结构化数据：MBTI 类型、维度得分、≤50 字的短引用、人格素描、相似名人等。**不包含用户真实姓名、项目名称、公司名称、完整对话内容等任何可识别信息。**

## 安装

将 `openclaw-skill/` 整个文件夹复制到 OpenClaw 的 skills 目录：

```bash
cp -r openclaw-skill/ ~/.openclaw/skills/mbti-from-ai/
```

或者创建符号链接：

```bash
ln -s /path/to/mbti-from-ai/openclaw-skill ~/.openclaw/skills/mbti-from-ai
```

## 使用

在 OpenClaw 中输入：

```
/mbti
```

## 文件结构

```
openclaw-skill/
├── SKILL.md              ← 主 Skill 定义（OpenClaw 读取的入口）
├── skill.json            ← Skill 元数据（名称、版本、触发词等）
├── README.md             ← 本文件
├── TESTING.md            ← 测试指南
└── scripts/
    ├── discover-sessions.sh   ← Step 1: 扫描会话文件
    ├── extract-messages.sh    ← Step 2: 提取用户消息（调用 Python 脚本）
    ├── extract_messages.py    ← Step 2: 实际的消息提取逻辑
    └── encode-and-open.sh     ← Step 4: 编码并打开浏览器
```

