---
name: murasame-feishu-voice
description: Feishu 语音气泡技能：使用丛雨（Murasame）语音包发送语音；若可表达则按标签发送语音并同步发送中文文本；支持开关控制、标签映射与关键词回退。
---

# Murasame Feishu Voice

## 能做什么
- 当回复适合用丛雨语音表达时，给文本加上标签（如 `[agree]` / `[thanks]` / `[greet_night]`）
- 发送 **飞书语音气泡**，并**同步发送原本的中文回复**（文字先到，语音异步）
- 若未匹配合适标签，输出 `NO_VOICE`，由上层改为仅发文本
- 支持手动开关语音：`/murasame on` 或 `/murasame off`

## 适用场景（触发建议）
- 飞书对话里希望用丛雨语音气泡表达情绪（称赞/问候/道歉/同意等）
- 想在语音之外保留可读的中文文本
- 需要可控开关，随时暂停语音发送

## 运行流程
1. 解析标签/关键词 → 选取对应语音文件
2. 先发送中文文本
3. 异步发送语音气泡

## 开关控制
- 发送 `/murasame off` 关闭语音（写入状态文件）
- 发送 `/murasame on` 开启语音
- 环境变量也可覆盖：`MURASAME_VOICE=off`

## 环境与依赖
- Feishu 凭证：`FEISHU_APP_ID` / `FEISHU_APP_SECRET`
- 接收者 OpenID：`FEISHU_RECEIVER`（**仅环境变量**）
- `ffmpeg` + `ffprobe`
- 丛雨语音包路径：`C:\Users\chenxun\.nanobot\workspace\murasame-voice\audios`

## 使用方式
### 发送带标签的回复
```
python scripts/send_murasame_voice.py "[thanks] 谢谢你"
```

### 返回值
- `OK: sent text+voice (async) for <category>` → 已发送文字，语音异步发送中
- `NO_VOICE` → 未匹配，改用纯文本
- `VOICE_DISABLED` → 被开关关闭

## 标签与映射
- 标签与音频文件在 `references/mapping.json`
- 默认标签：
  - greetings: greet_morning / greet_noon / greet_evening / greet_night
  - basic: agree / thanks / apology / refuse / wait / rest
  - care: encourage / care / compliment / explain

## 备注
- 若你想新增标签或替换音频文件，只需编辑 `mapping.json`
- 建议由上层对话逻辑判断是否加标签（即“能用丛雨语音表达就发语音”）
