---
name: kids-points
description: 儿童积分管理助手 - 语意识别，自动记账，跨 Session 数据一致
metadata: {"openclaw":{"emoji":"📚","requires":{"env":["SENSE_API_KEY"]}}}
---

# kids-points - 积分助手 📚

> **版本**: 1.3.0 | **最后更新**: 2026-05-01 | **作者**: 老王

简单、灵活的儿童积分管理工具。

---

## ✨ 核心特性

| 特性 | 说明 |
|------|------|
| ✅ **语意识别** | 不需要固定格式，理解各种说法 |
| ✅ **自动记账** | 自动写入 balance.md + input.log |
| ✅ **防重复** | 自动检测重复输入 |
| ✅ **跨 Session 一致** | 每次读取 balance.md，数据始终最新 |
| ✅ **手动可修正** | 直接编辑 balance.md 即可 |

---

## 🎯 使用方式

### 积分记录

```
今天完成了汉字抄写 2 课，口算题卡 2 篇全对
```

### 积分消费

```
积分消费 买零食花了 20 分
```

### 余额查询

```
现在多少分？
今日积分
```

---

## 📊 数据管理

### 唯一数据源

`kids-points/balance.md` - 所有积分记录

### 审计日志

`kids-points/logs/input.log` - 每次输入记录

### 手动修正

直接编辑 `balance.md` 文件，下次查询自动生效。

---

## 🔧 技术架构

### 三层架构

```
┌─────────────────────────────────────┐
│  Agent (LLM) - 语义理解层            │
│  - 理解用户意图                      │
│  - 提取任务数据                      │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│  技能代码 - 操作层                   │
│  - 防重复检查                        │
│  - 写入 balance.md                   │
│  - 写入 input.log                    │
└─────────────────────────────────────┘
                ↓
┌─────────────────────────────────────┐
│  文件系统 - 存储层                   │
│  - balance.md                        │
│  - input.log                         │
└─────────────────────────────────────┘
```

### 职责分工

| 组件 | 职责 |
|------|------|
| **Agent (LLM)** | 语义理解，提取任务数据 |
| **技能代码** | 确定性操作（记账、防重复、写日志） |

---

## 📁 文件结构

```
skills/kids-points/
├── agent-handler.js          # 技能入口
├── scripts/
│   ├── handler.js            # 核心处理（记账操作）
│   ├── parse-input.js        # 输入验证
│   ├── handle-image.js       # 图片存档（可选）
│   └── install-dependencies.js # 依赖检查
├── README.md                 # 快速入门
├── SKILL.md                  # 本文档
└── package.json              # 包配置
```

---

## 🔌 依赖

### 必需

- Node.js v14+
- OpenClaw

### 可选（语音功能）

- SenseAudio API Key（语音识别 + 语音播报）
- Python 3.8+（运行 ASR/TTS 脚本）
- 音频播放器（aplay/paplay/ffplay）

---

## 🚀 安装

```bash
# ClawHub 安装（推荐）
clawhub install kids-points

# 或手动安装
git clone <repo> ~/.openclaw/agents/kids-study/workspace/skills/kids-points
```

### 配置语音功能（可选）

```json
// ~/.openclaw/openclaw.json
{
  "env": {
    "SENSE_API_KEY": "sk-xxx..."
  }
}
```

获取 API Key：https://senseaudio.cn

---

## 📝 开发说明

### 添加新任务类型

不需要改代码！Agent (LLM) 会自动理解新说法。

### 修改计分规则

灵活计分，不需要固定规则。如需调整，修改 Agent 提示词即可。

### 调试

查看日志文件：
```bash
cat kids-points/logs/input.log
```

---

## 🎯 设计原则

1. **简单** - 文件少，代码少，易维护
2. **灵活** - 语意识别，不僵化
3. **可靠** - 确定性操作，数据一致
4. **透明** - 数据可见，可手动修正

---

_用心记录每一次进步。_ 🌟
