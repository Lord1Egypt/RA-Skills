---
name: ZeeLin Music
slug: melodylab-ai-song
version: 1.2.0
description: AI 全自动音乐创作神器：一句话描述，瞬间生成完整歌曲，支持人声演唱/纯音乐、流行/摇滚/民谣等多种风格 - Powered by ZeeLin
author: 刘东江 (@lidngjing317853)
license: MIT
homepage: https://melodylab.top
tags: [music, ai-music, suno, lyrics, song-generation, zeelin]
requires:
  - capability: http
  - capability: audio-playback
---

## 📋 隐私与透明度

**服务提供商**: MelodyLab (https://melodylab.top)
**计费平台**: 智灵 Skill 平台 (https://skills.zeelin.cn)
**数据处理**:
- 用户提交的创意描述、歌词、风格偏好将发送至 melodylab.top API
- 后端集成 DeepSeek（生成歌词）和 Suno AI（生成音乐）
- 生成的音频文件托管在 cdn.suno.ai

**数据保留**:
- 不存储用户提交的创意/歌词到 MelodyLab 服务器
- 请求日志保留 7 天用于故障排查
- 生成的音频文件由 Suno 按其隐私政策处理

---

## 使用时机

当用户请求：
- 生成/写/创作/做一首歌、歌曲、音乐
- AI 作曲、自定义风格歌、带歌词的歌、纯音乐
- 任何带描述的音乐需求，如"失恋的民谣""赛博朋克纯音乐""励志摇滚"

不适合：生成图片、视频、代码、数学计算等。

---

## ⚡ 计费规则

- 每次成功生成音乐消耗 **200 额度**
- 生成歌词**不消耗**额度
- 音乐生成失败/超时未完成**不扣费**
- 用户需自行在 https://skills.zeelin.cn 注册账号并充值获取 App-Key

---

## 🔑 第一步（强制）：获取并验证用户 App-Key

**⚠️ 必须在任何创作操作之前完成此步骤，不得跳过！**

### 1-A. 检查是否已有 App-Key

Agent 应先询问或检查用户是否已配置智灵 App-Key：

> 🎵 **开始创作前，我需要验证你的智灵账户额度。**
>
> 请提供你的智灵 App-Key（前往 https://skills.zeelin.cn 注册并创建应用获取）。
>
> 📌 每次生成音乐消耗 **200 额度**，生成歌词免费。

### 1-B. 调用额度校验接口

用用户提供的 App-Key 调用校验接口：

```
POST https://skills.zeelin.cn/v2/api/skill/detail
Header: app-key: <用户的 zeelin_app_key>
Header: Content-Type: application/json
Body:
{
  "query": "生成AI音乐: <用户描述简述>",
  "skill-id": "zeelin_ParDdTaM9W81iKiRZndwSCXW0"
}
```

### 1-C. 处理校验结果

**成功（code: 200）：**
```json
{
  "code": 200,
  "data": {
    "pre_order_id": "2026038787913be67748...",
    "remain_calls": 800,
    "skill_id": "zeelin_ParDdTaM9W81iKiRZndwSCXW0"
  }
}
```
→ 保存 `pre_order_id`（2小时内有效），告知用户余额并继续：
> ✅ 验证通过！当前余额 **800 额度**，可生成 4 首歌曲。开始创作！

**余额不足（code: 402 或 remain_calls < 200）：**
→ 停止，提示用户充值：
> ❌ 你的智灵账户余额不足（当前剩余 XX 额度，生成一首歌需要 200 额度）。
> 请前往 https://skills.zeelin.cn 充值后再试。

**Key 不存在/无效（code: 404）：**
> ❌ App-Key 无效，请检查是否正确复制。前往 https://skills.zeelin.cn/console/apps 查看你的 Key。

---

## 🎵 第二步：选择创作模式

验证通过后，询问用户创作方式：

> 请选择创作模式：
> 1️⃣ **AI 全自动** 🤖 - AI 随机为你创作一首惊喜歌曲
> 2️⃣ **自定义创作** 🎨 - 你来指定主题、风格和情绪
>
> （回复 1/2 或直接说"全自动"/"自定义"）

---

## 🎼 第三步：生成歌词（免费，不扣额度）

**基础 URL**: `https://melodylab.top`

**POST** `/api/generate-lyrics`

```json
{
  "creativeIdea": "夏天海边浪漫的初恋回忆",
  "musicStyle": "流行 轻快",
  "emotionalStyle": "甜蜜 青春",
  "vocalMode": "人声"
}
```

成功返回：
```json
{
  "success": true,
  "lyrics": "[Verse 1] 阳光洒在沙滩上...",
  "title": "夏日心动",
  "tags": ["pop", "happy", "summer"]
}
```

→ 将歌词和标题展示给用户，让用户确认或修改后再继续。
→ 纯音乐模式跳过此步，直接进入第四步。

---

## 🎹 第四步：生成音乐（消耗 200 额度）

**注意：此步骤由网站后端自动完成余额扣费，Agent 无需手动调用扣费接口。**

将用户的 `zeelin_app_key` 一并传入请求，后端会用它来扣费：

**POST** `https://melodylab.top/api/create`

```json
{
  "action": "generate_music",
  "topic": "夏天海边的初恋",
  "customTitle": "夏日心动",
  "styleTags": "pop, happy, summer",
  "isInstrumental": false,
  "customLyrics": "[Verse 1] 阳光洒在沙滩上...",
  "zeelin_app_key": "<用户的 zeelin_app_key>"
}
```

纯音乐版：
```json
{
  "action": "generate_music",
  "topic": "雨夜霓虹赛博朋克城市",
  "customTitle": "Neon Rain",
  "styleTags": "synthwave, dark, cyberpunk",
  "isInstrumental": true,
  "zeelin_app_key": "<用户的 zeelin_app_key>"
}
```

**返回（55秒内完成）：**
```json
{
  "success": true,
  "taskId": "b482dd297ebe4f6e...",
  "zeelin_pre_order_id": null
}
```

**返回（超时，生成仍在进行）：**
```json
{
  "success": true,
  "taskId": "b482dd297ebe4f6e...",
  "zeelin_pre_order_id": "2026038787913be6..."
}
```
→ 保存 `zeelin_pre_order_id`，轮询完成后调用扣费确认接口。

---

## 🔄 第五步：轮询等待结果

**GET** `https://melodylab.top/api/status?taskId=<taskId>`

每 5 秒轮询一次，最长等待 5 分钟：

```json
{
  "status": "SUCCESS",
  "musicList": [
    {
      "id": "xxx",
      "title": "夏日心动",
      "audioUrl": "https://cdn.suno.ai/xxx.mp3",
      "imageUrl": "https://cdn.suno.ai/xxx.jpg",
      "duration": 185
    },
    {
      "id": "yyy",
      "title": "夏日心动",
      "audioUrl": "https://cdn.suno.ai/yyy.mp3",
      "imageUrl": "https://cdn.suno.ai/yyy.jpg",
      "duration": 182
    }
  ]
}
```

状态值：`SUCCESS` / `PENDING` / `FAILED`

---

## 💰 第六步：确认扣费（仅超时场景）

**仅当第四步返回了 `zeelin_pre_order_id` 时才需要执行！**
（55秒内完成的情况，后端已自动扣费，跳过此步）

轮询到 `status: "SUCCESS"` 后，调用：

**POST** `https://melodylab.top/api/zeelin-confirm`

```json
{
  "pre_order_id": "<zeelin_pre_order_id>",
  "zeelin_app_key": "<用户的 zeelin_app_key>"
}
```

成功返回：
```json
{
  "success": true,
  "cost_balance": 200,
  "remain_calls": 600
}
```

→ 告知用户：
> 💰 本次生成消耗 200 额度，剩余 600 额度。

---

## 📢 最终呈现给用户

```
✅ 已为你生成两个版本，点击试听：

🎵 夏日心动 - v1
▶ https://cdn.suno.ai/xxx.mp3

🎵 夏日心动 - v2
▶ https://cdn.suno.ai/yyy.mp3

💰 本次消耗 200 额度，剩余 600 额度
```

---

## 完整对话示例

### 示例一：用户首次使用（无 Key）

**用户**："帮我写一首关于毕业离别的歌"

**Agent**：
> 🎵 开始创作前，我需要验证你的智灵账户额度。
>
> 请提供你的智灵 App-Key（前往 https://skills.zeelin.cn 注册获取）。每次生成音乐消耗 200 额度，生成歌词免费。

**用户**："我的 key 是 sdpj2syPCFOcY..."

**Agent**：（调用校验接口）
> ✅ 验证通过！当前余额 800 额度，可生成 4 首歌曲。
>
> 请选择创作模式：
> 1️⃣ AI 全自动
> 2️⃣ 自定义创作（你的主题：毕业离别）

---

### 示例二：用户已有 Key，直接描述需求

**用户**："我的 key 是 xxx，帮我做一首赛博朋克纯音乐"

**Agent**：（直接用 key 校验，通过后）
> ✅ 余额充足（800 额度）。赛博朋克纯音乐，马上开始创作...

（跳过歌词步骤，直接生成音乐，轮询结果）

> 🎵 已生成两个版本：
> ▶ Neon Rain - v1: https://cdn.suno.ai/xxx.mp3
> ▶ Neon Rain - v2: https://cdn.suno.ai/yyy.mp3
> 💰 消耗 200 额度，剩余 600 额度

---

## ⚠️ 错误处理

| 错误 | 原因 | 处理方式 |
|------|------|----------|
| code: 402 | 余额不足 | 提示用户充值 https://skills.zeelin.cn |
| code: 404 | Key 不存在 | 提示用户检查 Key |
| HTTP 401 | 未传 zeelin_app_key | 要求用户提供 Key |
| HTTP 429 | 请求频率过高 | 等待 60 秒后重试 |
| status: FAILED | Suno 生成失败 | 告知用户稍后重试，不扣费 |
| pre_order_id 过期 | 超过 2 小时未确认 | 重新发起生成请求 |

---

## 支持与反馈

- **开发者**: 刘东江 (@lidngjing317853)
- **项目主页**: https://melodylab.top
- **智灵平台**: https://skills.zeelin.cn
- **问题反馈**: 通过 ClawHub 或项目主页联系
