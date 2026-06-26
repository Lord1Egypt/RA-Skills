# ZeeLin Music 🎵

**用一句话创作完整歌曲** - 由 AI 驱动的音乐创作工具，接入智灵计费平台

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://clawhub.ai/skills/melodylab-ai-song)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-Skill-orange.svg)](https://openclaw.ai)

## ✨ 功能特性

### 💰 智灵计费体系
- 每次生成音乐消耗 **200 额度**，生成歌词**免费**
- 用户使用自己的智灵 App-Key，各自独立计费
- 前往 [skills.zeelin.cn](https://skills.zeelin.cn) 注册账号并充值

### 🤖 AI 全自动模式
让 AI 随机为你创作惊喜歌曲：
- 自动选择主题、风格、情绪
- 完全随机，给你意想不到的创意

### 🎨 自定义创作模式
完全控制你的音乐：
- 自定义主题和故事
- 选择音乐风格（流行/摇滚/民谣/电子等）
- 设定情绪基调（甜蜜/悲伤/激昂/平静等）
- 决定人声或纯音乐

### 🎼 生成流程
1. **验证智灵 App-Key** - 校验余额（必须）
2. **DeepSeek AI** 生成高质量歌词（免费）
3. **可编辑确认** - 修改直到满意
4. **Suno V5** 一次性生成 2 首完整歌曲（消耗 200 额度）

## 🚀 快速开始

### 前置条件

1. 前往 [skills.zeelin.cn](https://skills.zeelin.cn) 注册账号
2. 创建应用，获取 App-Key
3. 充值额度（每首歌消耗 200 额度）

### 使用示例

```
你: 帮我生成一首歌
AI: 请先提供你的智灵 App-Key...
你: sdpj2syPCFOcYiBWBy328W6gxoSbUosi
AI: ✅ 验证通过！余额 800 额度，可生成 4 首歌曲
    请选择：1️⃣ AI全自动  2️⃣ 自定义创作
你: 写一首关于毕业离别的民谣，要悲伤又有期许
AI: [生成歌词并等待确认]
你: 确认
AI: ✅ 已生成两个版本，消耗 200 额度，剩余 600 额度
    🎵 v1: https://cdn.suno.ai/xxx.mp3
    🎵 v2: https://cdn.suno.ai/yyy.mp3
```

## 📋 技术架构

```
用户输入 + 智灵 App-Key
   ↓
① 智灵平台余额校验（skills.zeelin.cn）
   ↓
② MelodyLab API (https://melodylab.top)
   ↓
┌─────────────┬─────────────┐
│ DeepSeek AI │   Suno V5   │
│  (歌词生成)  │  (音乐合成)  │
└─────────────┴─────────────┘
   ↓
③ 智灵平台扣减 200 额度
   ↓
返回 2 首完整歌曲 + 封面
```

## 🔑 API 接口说明

### 额度校验
```
POST https://skills.zeelin.cn/v2/api/skill/detail
Header: app-key: <your_app_key>
Body: { "query": "生成AI音乐: xxx", "skill-id": "zeelin_ParDdTaM9W81iKiRZndwSCXW0" }
```

### 生成音乐
```
POST https://melodylab.top/api/generate-music
Body: {
  "lyrics": "...",
  "title": "歌曲名",
  "zeelin_app_key": "<your_app_key>"
}
```

### 超时扣费确认
```
POST https://melodylab.top/api/zeelin-confirm
Body: { "pre_order_id": "...", "zeelin_app_key": "<your_app_key>" }
```

## 🔒 隐私与安全

- ✅ **不存储用户输入** - 创意描述仅用于实时生成
- ✅ **HTTPS 加密传输** - 所有数据通过 TLS 1.2+ 加密
- ✅ **用户各自计费** - App-Key 不共享，互相隔离
- ✅ **7 天日志保留** - 仅用于故障排查，之后自动删除

## ⚠️ 使用限制

- 每次生成音乐消耗 **200 额度**
- 生成时间：歌词 30-90 秒，音乐 60-300 秒
- 音乐生成失败不扣费

## 🎯 支持的风格

**音乐风格**: 流行 | 摇滚 | 民谣 | 电子 | 说唱 | 古风 | 爵士 | R&B | 乡村 | 金属

**情绪基调**: 甜蜜 | 悲伤 | 激昂 | 平静 | 怀旧 | 欢快 | 深沉 | 浪漫 | 治愈

## 📊 版本历史

### v1.2.0 (2026-03-11)
- 💰 接入智灵 Skill 计费平台，每次生成消耗 200 额度
- 🔑 用户使用自己的 App-Key，各自独立计费
- 🔄 完整的校验→生成→扣费事务流程
- ⏱️ 超时异步扣费机制（/api/zeelin-confirm）
- 🛡️ 修复并发场景下的 appKey 隔离问题

### v1.1.0 (2026-03-11)
- ⚡ 初步接入智灵计费框架

### v1.0.6 (2026-03-05)
- 🏷️ 更新技能名称为 "ZeeLin Music"

### v1.0.5 (2026-03-04)
- ✨ 新增 AI 全自动创作模式

## 🤝 贡献与支持

- **项目主页**: https://melodylab.top
- **智灵平台**: https://skills.zeelin.cn
- **ClawHub**: [@dongjiangliu9-tech](https://clawhub.ai/users/dongjiangliu9-tech)
- **Issues**: 通过 ClawHub 技能页面反馈

## 📄 许可证

MIT License

## 👤 作者

**刘东江** (@lidngjing317853) - https://melodylab.top

---

**免责声明**: 本技能生成的音乐内容版权归属请遵守 Suno AI 的许可协议。
