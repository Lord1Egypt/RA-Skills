# 🔧 kids-points 依赖说明

> **提示**：文字记账功能可以直接使用，语音功能需要额外配置！

---

## 🎯 功能分级

### ✅ 核心功能（无需配置）

以下功能**可以直接使用**，无需任何额外依赖：

- ✅ 文字记账
- ✅ 积分查询
- ✅ 积分统计
- ✅ 规则修改
- ✅ 图片存档

### 🎤 语音功能（可选增强）

以下功能需要配置 **SenseAudio**（目前**基本免费**）：

- 🎤 语音输入（发送音频自动识别）
- 🔊 语音播报（积分变动自动鼓励）
- 📻 日报语音朗读

---

## ⚠️ 语音功能依赖

如需使用语音功能，需要安装以下依赖：

### 1. 🎤 SenseAudio TTS（语音合成）

**用途**：语音播报、积分鼓励、日报朗读

**安装**：
```bash
# 安装依赖技能
clawhub install kid-point-voice-component

# 验证安装
ls ~/.openclaw/agents/kids-study/workspace/skills/kid-point-voice-component/
```

**配置**：
- 默认声音：`child_0001_a`（童声）
- 音频格式：WAV
- 自动播放：是

**测试**：
```bash
python3 skills/kid-point-voice-component/scripts/tts.py --play "测试语音播报"
```

---

### 2. 🎧 SenseAudio ASR（语音识别）

**用途**：音频消息识别、语音记账

**安装**：
```bash
# 安装依赖技能
clawhub install kid-point-voice-component

# 验证安装
ls ~/.openclaw/agents/kids-study/workspace/skills/kid-point-voice-component/
```

**配置**：
- 识别模型：`sense-asr-deepthink`
- 支持格式：OGG、WAV、MP3、M4A
- 识别语言：中文普通话

**测试**：
```bash
python3 skills/kid-point-voice-component/scripts/asr.py test_audio.ogg
```

---

### 3. 🔑 SenseAudio API Key

**说明**：语音功能需要 API Key，目前**基本免费**使用

💡 **免费提示**：
- ✅ 注册即送免费额度
- ✅ 个人使用完全足够
- ✅ 无需绑定信用卡
- ✅ 日常使用免费

**获取步骤**：
1. 访问 [SenseAudio 官网](https://senseaudio.cn)
2. 注册账号并登录
3. 进入控制台创建应用
4. 复制 API Key

**配置方法**：

编辑 `~/.openclaw/openclaw.json`：
```json
{
  "env": {
    "SENSE_API_KEY": "sk-your-api-key-here"
  }
}
```

**验证配置**：
```bash
# 检查 API Key 是否配置
grep SENSE_API_KEY ~/.openclaw/openclaw.json
```

**没有 API Key 怎么办？**
- ✅ 不影响文字记账功能
- ✅ 可以正常使用查询、统计
- ⚠️ 仅语音功能不可用
- 💡 建议申请免费 Key 体验完整功能

---

## 📦 Python 依赖

### requests 库

**用途**：SenseAudio HTTP 接口调用

**安装**：
```bash
pip3 install requests
```

**验证**：
```bash
python3 -c "import requests; print('✅ requests 已安装')"
```

---

## 🔊 音频播放器

**必需**：至少安装一个音频播放器

### 推荐：aplay (ALSA)

**优点**：
- ✅ WAV 格式原生支持
- ✅ 系统自带（大多数 Linux）
- ✅ 轻量级

**安装**：
```bash
sudo apt-get install alsa-utils
```

**验证**：
```bash
aplay --version
```

### 备选：paplay (PulseAudio)

**优点**：
- ✅ 支持多种格式
- ✅ 桌面环境常用

**安装**：
```bash
sudo apt-get install pulseaudio
```

### 备选：ffplay (FFmpeg)

**优点**：
- ✅ 支持所有格式
- ✅ 功能最强

**安装**：
```bash
sudo apt-get install ffmpeg
```

---

## ⚠️ 可选依赖

### schedule-manager（定时任务）

**用途**：自动日报生成

**安装**：
```bash
clawhub install schedule-manager
```

### feishu-doc（飞书文档）

**用途**：日报存储、发送

**安装**：
```bash
clawhub install feishu-doc
```

---

## 📋 完整安装清单

### 快速安装（推荐）

```bash
# 1. 安装依赖技能
clawhub install kid-point-voice-component
clawhub install kid-point-voice-component

# 2. 安装 Python 依赖
pip3 install requests

# 3. 安装音频播放器
sudo apt-get install alsa-utils

# 4. 配置 API Key
# 编辑 ~/.openclaw/openclaw.json，添加 SENSE_API_KEY

# 5. 验证安装
python3 skills/kid-point-voice-component/scripts/tts.py --play "安装成功！"
```

### 检查清单

- [ ] `kid-point-voice-component` 技能已安装
- [ ] `kid-point-voice-component` 技能已安装
- [ ] `requests` Python 包已安装
- [ ] 至少一个音频播放器已安装
- [ ] `SENSE_API_KEY` 已配置
- [ ] TTS 测试成功
- [ ] ASR 测试成功

---

## 📊 功能对比

| 功能 | 无 API Key | 有 API Key |
|------|-----------|-----------|
| **文字记账** | ✅ 可用 | ✅ 可用 |
| **语音记账** | ❌ 不可用 | ✅ 可用 |
| **积分查询** | ✅ 可用 | ✅ 可用 |
| **语音播报** | ❌ 不可用 | ✅ 可用 |
| **日报生成** | ✅ 可用 | ✅ 可用 + 语音 |
| **图片存档** | ✅ 可用 | ✅ 可用 |

---

## ❓ 常见问题

### Q: 没有 API Key 能用吗？
A: **可以！** 文字记账、查询、统计等功能都可以正常使用，只有语音功能不可用。

### Q: 为什么要申请 API Key？
A: 
- ✅ **免费**：目前基本免费使用
- ✅ **完整体验**：语音输入/输出更便捷
- ✅ **儿童友好**：童声播报更亲切
- ✅ **简单快捷**：注册即用

### Q: API Key 收费吗？
A: **基本免费**！
- 注册送免费额度
- 个人使用完全足够
- 无需绑定信用卡
- 日常使用不花钱

### Q: 如何申请 API Key？
A: 
1. 访问 [senseaudio.cn](https://senseaudio.cn)
2. 注册账号（免费）
3. 创建应用
4. 复制 API Key 到配置文件

### Q: 可以用其他 TTS 吗？
A: 可以修改代码使用其他 TTS，但默认配置使用 SenseAudio。

### Q: 音频播放器必须安装吗？
A: 如果使用语音功能，需要安装。推荐 `aplay`（系统自带）。

### Q: 安装失败怎么办？
A: 检查网络连接，或手动下载安装包安装。

### Q: API Key 安全吗？
A: 安全！API Key 只存储在本地配置文件中，不会上传。

---

## 🔗 相关文档

- [README.md](README.md) - 快速入门
- [RULES.md](RULES.md) - 完整规则
- [SKILL.md](SKILL.md) - 技术文档

---

_确保所有依赖安装完成后再使用技能！_
