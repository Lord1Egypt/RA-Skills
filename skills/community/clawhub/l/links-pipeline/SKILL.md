---
name: links-pipeline
description: 链接全自动处理管线。识别链接类型（抖音/小红书/B站视频、公众号/网页文章），自动下载、转录/提取正文、识别内容主题、路由到对应知识库收件箱。
description_zh: 链接内容自动处理管线。收到链接后，按类型自动走下载→转文字→内容识别→入库全流程，无需手动操作。
description_en: Automated link processing pipeline. Detects link type (Douyin/Xiaohongshu/Bilibili video, WeChat/web article), auto-downloads, transcribes/extracts text, identifies content topic, and routes to the correct knowledge base inbox.
homepage: https://clawhub.ai/packages/links-pipeline
allowed-tools: Read,Write,Bash,Process,Grep,Glob
created: 2026-05-22
updated: 2026-05-22
---

# Links Pipeline Skill — 链接自动处理管线

> 收到任意链接 → 自动识别类型 → 完整下载/转录 → 路由入库

---

## 触发指令

- 用户发送任何链接（抖音/B站/小红书/公众号/网页）
- 用户说"处理这个链接"
- 用户说"存这个视频/文章"

## 工作流程

### 步骤一：链接类型判断

| 特征 | 类型 | 走哪条管线 |
|------|------|-----------|
| `douyin.com` / `v.douyin.com` | 抖音视频 | video pipeline |
| `xiaohongshu.com` / `xhslink.com` | 小红书图文或视频 | video 或 article 管线 |
| `bilibili.com` / `b23.tv` | B站视频 | video pipeline |
| `mp.weixin.qq.com` | 公众号文章 | article pipeline |
| 其他网页链接 | 网页文章 | article pipeline |
| 难以判断 | — | 询问用户 |

### 步骤二：按管线处理

**视频管线（Video Pipeline）：**
```bash
yt-dlp <url> -o video.mp4
ffmpeg -i video.mp4 -vn -acodec pcm_s16le -ar 16000 -ac 1 audio.wav
whisper audio.wav --model base --language zh -f txt > raw.txt
# 调用 DeepSeek API 清洗转录稿
```

**文章管线（Article Pipeline）：**
```python
requests.get(url) → bs4/readability 提取正文
→ 转为结构化 Markdown
```

### 步骤三：内容主题识别 → 路由入库

通过 Skill 同目录下的 `config.yaml` 配置路由规则，示例：

```yaml
routing:
  rules:
    - topics: ["AI工具", "AI编程", "技术教程"]
      target: "快速入门/示例/AI知识库/"
  fallback: ask
```

- 匹配到规则 → 直接存入 + 告知用户
- 匹配不到 → 询问用户
- 用户指定去处 → 执行

### 步骤四：结果确认

处理完成后输出：
```
✅ 处理完毕
来源：xxx
类型：抖音视频
时长：9:03
转录字数：3066字
已存入：您的AI知识库（自动识别）
```
