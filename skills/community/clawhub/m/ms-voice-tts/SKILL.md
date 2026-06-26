---
name: voice-tts
description: 使用 edge-tts 生成高质量中文语音消息并发送。当用户要求发语音、语音回复、TTS、文字转语音、语音播报、语音消息时使用。支持多种中文声音（男声/女声/方言），可调节语速音调，适用于飞书/Telegram/Discord 等渠道的语音消息发送。
---

# Voice TTS（edge-tts 语音合成）

使用 Microsoft edge-tts（免费）生成高质量中文语音，通过 `message` 工具发送语音消息。

## ⚠️ 安装（首次使用必读）

本 skill 依赖 **edge-tts**，需先全局安装。安装前请自查系统环境：

### 1. 检查是否已安装

```bash
which edge-tts
```

如果返回路径（如 `/usr/local/bin/edge-tts`），说明已安装，跳到「快速流程」。

### 2. 根据系统选择安装方式

**macOS（推荐 pipx，独立环境不污染系统）：**

```bash
# 先确认 pipx 是否已安装
which pipx
# 如果没有：brew install pipx
pipx install edge-tts
pipx ensurepath
```

> ⚠️ macOS 的 Homebrew Python 受 PEP 668 限制，禁止直接 `pip install`。
> 不要用 `pip install --break-system-packages`，会污染系统 Python。

**Linux（推荐 pipx，或用 --user 安装）：**

```bash
# 方式一：pipx（推荐）
pipx install edge-tts

# 方式二：pip --user（如果 pipx 不可用）
pip install --user edge-tts
# 安装后确保 ~/.local/bin 在 PATH 中
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && source ~/.bashrc
```

**Windows（PowerShell）：**

```powershell
pip install edge-tts
# 或
pipx install edge-tts
```

### 3. 验证安装

```bash
edge-tts --list-voices | head -5
```

看到语音列表即安装成功。

---

## 快速流程

1. 运行脚本生成语音 → 获取文件路径
2. 用 `message` 工具发送（`asVoice: true`，`filePath`）

## 生成语音

```bash
bash <skill_dir>/scripts/tts.sh "文本内容" [voice] [output_path]
```

**预期输出：**
- 返回生成的音频文件路径（如 `~/.openclaw/media/openclaw_voice_1710556800.opus`）
- 文件格式：opus（高质量，体积小）
- 文件大小：约 5-20 KB（取决于文本长度）

**参数说明：**
- 第 1 参数（必填）：文本内容，建议 50-300 字
- 第 2 参数（可选）：声音名称，默认 `zh-CN-YunxiNeural`
- 第 3 参数（可选）：输出路径，默认 `~/.openclaw/media/`

**示例：**
```bash
# 基础用法
bash <skill_dir>/scripts/tts.sh "你好，这是一条测试语音"

# 指定声音
bash <skill_dir>/scripts/tts.sh "你好" "zh-CN-XiaoxiaoNeural"

# 指定输出路径
bash <skill_dir>/scripts/tts.sh "你好" "zh-CN-YunxiNeural" "/tmp/test.opus"
```

## 发送语音

```json
{
  "action": "send",
  "asVoice": true,
  "filePath": "<脚本返回的路径>"
}
```

**预期结果：**
- 音频文件作为语音消息发送到指定渠道
- 消息格式：语音文件附件（非转文字）
- 发送时间：通常 1-3 秒（取决于文件大小和网络）

**参数说明：**
- `action`: 固定为 "send"
- `asVoice`: 必须为 `true`（触发语音消息发送）
- `filePath`: 语音文件的绝对路径（由 tts.sh 脚本返回）
- `channel`: 目标渠道（feishu/telegram/discord）

用 `message` 工具调用，`channel` 设为当前渠道（feishu/telegram/discord）。

## 可用中文声音

| Voice | 性别 | 风格 |
|-------|------|------|
| zh-CN-YunxiNeural | 男 | 活泼阳光 ⭐ 默认 |
| zh-CN-XiaoxiaoNeural | 女 | 温暖自然 |
| zh-CN-XiaoyiNeural | 女 | 活泼 |
| zh-CN-liaoning-XiaobeiNeural | 女 | 东北话 |
| zh-TW-HsiaoChenNeural | 女 | 台湾腔 |

---

## 完整场景示例

### 场景 1：飞书通知

```bash
# 1. 生成语音（会议提醒）
bash <skill_dir>/scripts/tts.sh "提醒：项目评审会议将在5分钟后开始，请做好准备"
# 输出：~/.openclaw/media/openclaw_voice_1710556800.opus

# 2. 发送到飞书群
{
  "action": "send",
  "channel": "feishu",
  "asVoice": true,
  "filePath": "~/.openclaw/media/openclaw_voice_1710556800.opus"
}
```

### 场景 2：Telegram 私信

```bash
# 1. 生成语音（客服回复）
bash <skill_dir>/scripts/tts.sh "zh-CN-XiaoxiaoNeural" "您好，您的问题已收到，我们会尽快处理"
# 输出：~/.openclaw/media/openclaw_voice_1710556900.opus

# 2. 发送到 Telegram
{
  "action": "send",
  "channel": "telegram",
  "asVoice": true,
  "filePath": "~/.openclaw/media/openclaw_voice_1710556900.opus"
}
```

### 场景 3：Discord 频道公告

```bash
# 1. 生成语音（系统公告，正式语速）
bash <skill_dir>/scripts/tts.sh "zh-CN-YunxiNeural" "服务器维护将于今晚23:00开始，预计2小时"
# 输出：~/.openclaw/media/openclaw_voice_1710557000.opus

# 2. 发送到 Discord 频道
{
  "action": "send",
  "channel": "discord",
  "asVoice": true,
  "filePath": "~/.openclaw/media/openclaw_voice_1710557000.opus"
}
```

### 场景 4：长文本分段生成

```bash
# 长文本（>500字）必须分段
TEXT_PART1="第一部分：今天天气晴朗，温度适宜，适合外出活动。"
TEXT_PART2="第二部分：请大家注意防晒，多喝水，保持良好的作息时间。"
TEXT_PART3="第三部分：祝大家度过美好的一天！"

# 分别生成
VOICE1=$(bash <skill_dir>/scripts/tts.sh "$TEXT_PART1")
VOICE2=$(bash <skill_dir>/scripts/tts.sh "$TEXT_PART2")
VOICE3=$(bash <skill_dir>/scripts/tts.sh "$TEXT_PART3")

# 依次发送（实际使用时可能需要根据渠道限制添加延迟）
echo "$VOICE1"  # 第一段语音路径
echo "$VOICE2"  # 第二段语音路径
echo "$VOICE3"  # 第三段语音路径
```

### 场景 5：定制参数（语速/音调/音量）

```bash
# 快节奏通知（语速 +20%）
edge-tts --voice zh-CN-YunxiNeural --rate +20% --text "紧急通知：服务器将在1分钟后重启" --write-media /tmp/emergency.opus

# 正式公告（语速 -10%，音量 +5%）
edge-tts --voice zh-CN-YunxiNeural --rate -10% --volume +5% --text "年度总结大会将于下周一举行" --write-media /tmp/announcement.opus

# 强调语气（音调 +5Hz）
edge-tts --voice zh-CN-YunxiNeural --pitch +5Hz --text "重要！" --write-media /tmp/emphasis.opus
```

查看全部中文声音：

```bash
edge-tts --list-voices | grep "zh-"
```

## 参数调节

通过 `--rate`（语速）、`--pitch`（音调）、`--volume`（音量）调节：

```bash
# 语速 +20%，音量 +10%
edge-tts --voice zh-CN-YunxiNeural --rate +20% --volume +10% --text "你好" --write-media ~/.openclaw/media/out.opus
```

## 注意事项

- 文本建议 1000 字以内，长文本分段生成
- 输出目录为 `~/.openclaw/media/`（确保 OpenClaw 有权限访问）
- 临时文件发送后可删除

---

## 💡 实用技巧

**文本长度优化：**
- 50-300 字最佳，语音质量最高
- 300-500 字可接受，建议用中性语速
- 超过 500 字必须分段，否则生成超时或质量下降

**声音选择建议：**
- 通知/提醒：`zh-CN-YunxiNeural`（男声，活泼阳光）⭐ 默认
- 客服/陪伴：`zh-CN-XiaoxiaoNeural`（女声，温暖自然）
- 互动娱乐：`zh-CN-XiaoyiNeural`（女声，活泼）
- 特定场景：方言声音增强亲和力，但通用场景慎用

**参数调节指南：**
```bash
# 快节奏通知：语速 +20%
edge-tts --voice zh-CN-YunxiNeural --rate +20% --text "提醒：会议将在5分钟后开始" --write-media out.opus

# 正式公告：语速 -10%，音量 +5%
edge-tts --voice zh-CN-YunxiNeural --rate -10% --volume +5% --text "系统维护通知" --write-media out.opus

# 嘈杂环境：音量 +10%
edge-tts --voice zh-CN-YunxiNeural --volume +10% --text "重要提醒" --write-media out.opus

# 强调语气：音调 +5Hz
edge-tts --voice zh-CN-YunxiNeural --pitch +5Hz --text "注意！" --write-media out.opus
```

**常见陷阱：**
- ❌ 文本过长：超过 1000 字会导致生成失败或超时
- ❌ 特殊符号：`<>{}|` 等符号可能被错误解析，建议使用全角符号
- ❌ 输出路径：确保 `~/.openclaw/media/` 目录存在且 OpenClaw 有写入权限
- ❌ 音调过高：超过 +10Hz 会明显失真，建议控制在 ±5Hz 范围内

**性能优化：**
- 临时文件建议在发送后立即清理，避免磁盘空间累积
- 批量生成时建议用异步脚本，避免阻塞主流程
- 缓存常用文本的语音文件，减少重复生成

**跨渠道适配：**
- **飞书**：支持 opus/mp3/wav，推荐 opus（体积小质量好）
- **Telegram**：支持 ogg/wav，推荐 ogg/opus
- **Discord**：支持多种格式，推荐 mp3（兼容性最好）
