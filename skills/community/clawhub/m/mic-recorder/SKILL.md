---
name: mic-recorder
description: 麦克风录音并发送音频到飞书。涵盖语音和背景音。
emoji: 🎙
---

# MIC Recorder Skill

录音并发送音频到飞书。

## 方案对比

| 方案 | 成功率 | 说明 |
|------|--------|------|
| **Automator 应用** ✅ | 100% | 通过 Automator 创建 RecordMic.app，已验证可用 |
| 语音备忘录 | 100% | macOS 系统应用，可靠 |
| FFmpeg 命令行 | 0% | 受 macOS 权限限制，只能录静音 |
| Python/sounddevice | 0% | 受 macOS 权限限制 |
| Swift/AVAudioRecorder | 0% | 受 macOS 权限限制 |

## 方案一：Automator 应用（推荐）✅

### 配置（用户已完成）

1. 用 Automator 创建 RecordMic.app
   - 新建 → 应用程序
   - 添加"运行 Shell 脚本"
   - 写入 FFmpeg 命令

2. 应用位置：`~/.openclaw/tools/RecordMic.app`

3. 已授权麦克风权限

### 使用方法

**录制：**
```bash
# 启动应用录音（默认 20 秒）
open ~/.openclaw/tools/RecordMic.app

# 或使用 wait 命令等待完成
open -W ~/.openclaw/tools/RecordMic.app
```

**发送录音：**
```python
# 发送到飞书（RecordMic.app 自动复制到 workspace）
# ✅ 正确：workspace 路径，使用 media 参数
message(action="send", channel="feishu", media="~/.openclaw/workspace/recording_latest.wav", caption="录音已降噪处理")

# ✅ file_path 参数也行
message(action="send", channel="feishu", file_path="~/.openclaw/workspace/recording_latest.wav", caption="录音已降噪处理")

# ✅ path 参数也行
message(action="send", channel="feishu", path="~/.openclaw/workspace/recording_latest.wav", caption="录音已降噪处理")
```

**修改录制时长：**

编辑 RecordMic.app：
1. 右键 → 显示包内容
2. Contents/document.wflow
3. 找到 `-t 20` 改为所需秒数

## 关键要点

### Automator 应用方案

- **应用位置**：`~/.openclaw/tools/RecordMic.app`
- **录音输出**：`/tmp/openclaw_recording.wav`
- **默认时长**：20 秒
- **格式**：WAV (16-bit PCM, 48kHz, 单声道)
- **已授权麦克风权限**
- **默认降噪**：Gemini 方案（仅FFT降噪，无噪声门，高通200Hz + 低通3000Hz + afftdn=nr=10:nf=-25:tn=1）
- **最终输出**：`/tmp/openclaw_recording_denoised.wav` + 自动复制到 `~/.openclaw/workspace/recording_latest.wav`

### 发送规则

- **文件必须在 workspace 目录**（安全策略 CVE-2026-26321）
- **不要用 /tmp/ 路径发送**，先复制到 workspace
- **使用飞书发送**：`channel="feishu"`

## 降噪处理（2026-03-09 更新）

### ⭐ 当前默认（Gemini 方案，仅FFT降噪，无噪声门）
```bash
ffmpeg -y -i /tmp/openclaw_recording.wav -af "highpass=f=200,lowpass=f=3000,afftdn=nr=10:nf=-25:tn=1" /tmp/openclaw_recording_denoised.wav
```
- 高通 200Hz + 低通 3000Hz
- FFT 降噪 afftdn=nr=10:nf=-25:tn=1
- **无噪声门**：保留完整人声，包括尾段轻声
- 2026-03-09 更新：替代 v7 为默认方案
- 人声最清晰，沙沙声抑制良好（2-4kHz RMS -67.4 dB）

### 历史方案（v7，小波降噪，保留人声和键盘声）
```bash
ffmpeg -y -i /tmp/openclaw_recording.wav -af "highpass=f=100,lowpass=f=4500,afwtdn=sigma=0.35:percent=90" /tmp/openclaw_recording_denoised.wav
```
- 沙沙声（2-4kHz）降低 91%
- RMS 噪声底降低 77-94%
- 人声频段保留良好
- **注意**：v7 仍有 Mac mini 硬件底噪（RMS -59 dB），无法完全消除

### 替代方案（v8，超强降噪，沙沙声基本消除但人声略损失）
```bash
ffmpeg -y -i /tmp/openclaw_recording.wav -af "highpass=f=100,lowpass=f=4500,afwtdn=sigma=0.4:percent=95" /tmp/openclaw_recording_denoised.wav
```
- 沙沙声降低 87%
- RMS 噪声底降低 71%
- 人声中高频略损失

### 旧参数（v1，轻度降噪，已不推荐）
```bash
ffmpeg -y -i /tmp/openclaw_recording.wav -af "highpass=f=80,lowpass=f=8000,afftdn=nf=-25:nr=12" /tmp/openclaw_recording_denoised.wav
```

### 测试结果对比
| 版本 | 2-3kHz 幅度 | 3-4kHz 幅度 | RMS | 说明 |
|------|------------|------------|-----|------|
| 原始 | 237,534 | 183,332 | 674 | - |
| v1 | 82,671 | 70,594 | 462 | 沙沙声仍明显 |
| v7 | 21,394 | 21,643 | 198 | 小波降噪，已验证 |
| v8 | 10,683 | 10,825 | 191 | 沙沙声最低，人声略损 |
| Gemini ⭐ | - | - | - | 当前默认，FFT降噪 |

## 完整代码示例

```python
import subprocess
import os

def record_audio(duration=20):
    """使用 Automator 应用录音（Gemini 进阶方案）"""
    # 启动应用（等待完成）
    subprocess.run(['open', '-W', '~/.openclaw/tools/RecordMic.app'])

    # RecordMic.app 已自动复制到 workspace
    # 发送到飞书
    # message(action="send", channel="feishu", media="~/.openclaw/workspace/recording_latest.wav", caption="录音已降噪处理")
```

## 故障排除

### RecordMic.app 无法录音

- 检查麦克风权限：系统设置 → 隐私与安全性 → 麦克风
- 确认 RecordMic.app 已勾选
- 如果未勾选，重新添加并授权

### 录音文件不存在

- 检查应用是否执行完成
- 查看输出路径：`/tmp/openclaw_recording.wav`
- 应用路径：`~/.openclaw/tools/RecordMic.app`

### 发送失败

- 检查文件是否在 workspace 目录
- 不要用 /tmp/ 路径
- 文件大小是否合理（> 1KB）

## 更新日志

- 2026-03-04: 创建 skill
- 2026-03-04: **验证 Automator 应用方案，100% 成功！**
- 2026-03-09: **v7 参数确认为最佳方案**（高通100Hz + 低通4500Hz + 小波降噪 sigma=0.35 percent=90）
- 2026-03-09: 默认录音时长更新为 20 秒，RecordMic.app 自动执行 v7 降噪
- 2026-03-09: 新录音测试验证，沙沙声降低 91%，RMS 噪声底降低 77-94%
- 2026-03-09: **更新为 Gemini 进阶方案**（高通200Hz + 低通3000Hz + afftdn=nr=10:nf=-25:tn=1），替代 v7 为当前默认方案
- 2026-03-09: **RecordMic.app 自动复制到 workspace**（安全策略要求），发送前无需手动复制
