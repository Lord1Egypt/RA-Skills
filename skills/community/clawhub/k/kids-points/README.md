# kids-points - 儿童积分语音助手 🎤

> **会说话的积分管理助手** - 支持语音记账、语音播报、音频识别

[![Version](https://img.shields.io/badge/version-1.2.0-blue.svg)](https://clawhub.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Voice](https://img.shields.io/badge/voice-KidPointVoice-orange.svg)](https://senseaudio.cn)

---

## ✨ 核心特性

### 🎤 语音交互
- **语音输入** - 发送音频消息自动识别并记账
- **语音输出** - 积分变动自动语音播报鼓励
- **童声播报** - 使用亲切活泼的童声 `child_0001_a`

### 📊 积分管理
- **自动统计** - 实时生成积分报表
- **每日日报** - 自动生成 + 语音播报
- **正反馈强化** - 语音鼓励增强学习动力

### 🔧 智能识别
- **SenseAudio ASR** - 高精度语音识别
- **SenseAudio TTS** - 高质量语音合成
- **多格式支持** - OGG、WAV、MP3、M4A

---

## ⚠️ 依赖说明

### 核心功能（无需额外依赖）

✅ **文字记账、查询、统计**等功能可以**直接使用**，无需额外配置！

### 语音功能（可选增强）

🎤 **语音输入/输出**功能需要配置 SenseAudio，目前**基本免费**：

| 依赖 | 用途 | 必需 | 说明 |
|------|------|------|------|
| **kid-point-voice-component** | TTS/ASR 语音组件 | ⚠️ 可选 | 语音播报、语音识别 |
| **SENSE_API_KEY** | API 密钥 | ⚠️ 可选 | [免费申请](https://senseaudio.cn) |

**快速安装（如需语音功能）**：
```bash
# 安装依赖技能
clawhub install kid-point-voice-component

# 配置 API Key（编辑 ~/.openclaw/openclaw.json）
```

📋 **详细依赖说明**：查看 [DEPENDENCIES.md](DEPENDENCIES.md)

💡 **提示**：没有 API Key 也可以使用所有文字功能，语音功能需要单独配置。

---

## 🚀 快速开始

### 1. 确认依赖已安装

```bash
# Node.js 依赖
cd skills/kids-points && npm install

# Python 依赖
pip3 install requests

# 音频播放器（至少一个）
sudo apt-get install alsa-utils    # aplay (推荐)
sudo apt-get install pulseaudio    # paplay
```

### 2. 配置 API Key

编辑 `~/.openclaw/openclaw.json`：

```json
{
  "env": {
    "SENSE_API_KEY": "sk-your-api-key-here"
  }
}
```

### 3. 使用技能

#### 文字记账
```
学习积分 今天完成了汉字抄写 2 课，口算题卡 2 篇全对
```

#### 🎤 语音记账
```
[发送音频消息]
"学习积分 今天完成了汉字抄写 2 课，口算题卡 2 篇全对"
→ 自动识别 → ✅ 添加积分 → 🔊 语音鼓励
```

#### 查询积分
```
今日积分
本周积分
本月积分
```

---

## 📖 使用场景

### 场景 1: 音频记账
```
[用户发送 5 秒音频]
🎤 "学习积分 今天完成了汉字抄写 2 课，口算题卡 2 篇全对"
        ↓
🤖 ASR 识别 → 解析 → 添加积分
        ↓
✅ 获得 4 积分
🔊 "太棒啦！获得 4 积分，继续加油哦！"（童声）
```

### 场景 2: 日报播报
```
每天 07:00 自动发送：
📤 飞书消息：积分日报（图文）
🔊 语音消息："2026-03-14 积分日报。今天收入 15 分..."
```

### 场景 3: 语音查询
```
[用户发送音频]
🎤 "今天多少分了？"
        ↓
🤖 识别 → 查询 → 回复
        ↓
🔊 "今天已经获得了 12 积分，当前余额 116.3 分！"
```

---

## 🎯 积分规则（默认）

### 🎒 学习任务
| 任务 | 分数 |
|------|------|
| 汉字抄写 | 1 分/课 |
| 口算题卡 | 1 分/篇（全对 +1） |
| ABC Reading | 3 分/日 |
| 跳绳 | 最多 3 分 |

### 🏠 生活习惯
| 任务 | 分数 |
|------|------|
| 自主洗澡 | 1 分 |
| 整理书包 | 1 分 |
| 主动洗漱 | 1 分 |

### ⚠️ 限制
- 每月上限：400 分
- 1 分 = 1 元
- 随时得分随时花

### 📝 记账与调账

**记账方式**:
- ✅ 文字："学习积分 今天完成了..."
- ✅ 语音：发送音频消息自动识别
- ✅ 智能解析：自动提取任务名称和数量

**调账规则**:
- 💰 **余额只增不减** - 历史数据永不删除
- 📊 **消费单独记录** - "积分消费 买零食..."
- 🔧 **错误修正** - 通过调账记录，不删除原数据
- 📁 **余额追踪** - `balance.md` 是最准确的余额来源

---

## 🔧 技术细节

### 语音能力

| 能力 | 技术 | 说明 |
|------|------|------|
| **TTS** | SenseAudio HTTP TTS | 语音合成、播报 |
| **ASR** | SenseAudio HTTP ASR | 语音识别、输入 |
| **声音** | `child_0001_a` | 童声、亲切活泼 |
| **格式** | WAV | 系统原生支持 |

### 依赖技能

- ✅ `kid-point-voice-component` - TTS 语音合成
- ✅ `kid-point-voice-component` - ASR 语音识别
- ⚠️ `schedule-manager` - 定时任务（可选）
- ⚠️ `feishu-doc` - 飞书文档（可选）

### 文件结构

```
kids-points/
├── scripts/
│   ├── handler.js              # 主处理器
│   ├── parse-input.js          # 输入解析
│   ├── generate-daily-report.js # 日报生成（含 TTS）
│   └── send-daily-report.sh    # 定时任务
├── config/
│   └── rules.json              # 积分规则
└── README.md                   # 本文档
```

---

## 📚 文档

| 文档 | 用途 | 说明 |
|------|------|------|
| **[DEPENDENCIES.md](DEPENDENCIES.md)** | ⚠️ **依赖说明** | 必需安装的依赖和配置 |
| **[RULES.md](RULES.md)** | 📋 **完整规则说明** | 包含所有积分规则、记账规则、调账规则 |
| **[SKILL.md](SKILL.md)** | 🔧 技能技术文档 | 技能架构、API、配置 |
| **[README.md](README.md)** | 🚀 本文档 | 快速入门 |
| **[USAGE.md](USAGE.md)** | 📖 使用指南 | 详细使用说明 |

---

## 🎉 更新日志

### v1.2.0 (2026-03-14)
- ✅ 使用 SenseAudio TTS/ASR
- ✅ 支持语音输入（音频消息识别）
- ✅ 默认童声 `child_0001_a`
- ✅ 优化语音交互体验

### v1.1.0 (2026-03-13)
- ✅ TTS 语音播报优化
- ✅ 分离阅读文案和语音文案
- ✅ 解决长文本截断问题

---

## 📄 许可证

MIT License

---

## 👨‍💻 作者

老王

---

**让孩子在语音互动中快乐学习！** 🌟
