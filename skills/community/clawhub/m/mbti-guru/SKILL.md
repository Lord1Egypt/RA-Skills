# MBTI Guru - MBTI人格测试专家

## 简介 / Introduction

**MBTI Guru** 是一款专业的人格类型评估工具，基于迈尔斯-布里格斯类型指标（MBTI）理论，帮助用户发现自己的性格类型，并生成详尽的中英双语分析报告。

**MBTI Guru** is a professional personality assessment tool based on the Myers-Briggs Type Indicator (MBTI) theory. It helps users discover their personality type and generates detailed bilingual analysis reports in Chinese and English.

---

## 功能特点 / Features

### 1. 四个测试版本 / Four Test Versions

| 版本 | 题数 | 时长 | 适用场景 |
|------|------|------|----------|
| Quick / 快速版 | 70题 | ~10分钟 | 快速体验 |
| Standard / 标准版 | 93题 | ~15分钟 | 正式测试 |
| Extended / 扩展版 | 144题 | ~25分钟 | 深度分析 |
| Professional / 专业版 | 200题 | ~35分钟 | 临床级 |

---

### 2. MBTI四维度 / Four Dimensions

| 维度 | 中文名称 | English | 偏好倾向 |
|------|----------|---------|----------|
| **E/I** | 能量倾向 | Energy | Extraversion vs Introversion |
| **S/N** | 信息获取 | Information | Sensing vs Intuition |
| **T/F** | 决策方式 | Decisions | Thinking vs Feeling |
| **J/P** | 生活态度 | Structure | Judging vs Perceiving |

---

### 3. 16种人格类型 / 16 Personality Types

| 类型 | 中文名称 | English Name | 特点 |
|------|----------|--------------|------|
| ISTJ | 物流师 | The Logistician | 务实可靠 |
| ISFJ | 守卫者 | The Defender | 忠诚守护 |
| INFJ | 提倡者 | The Advocate | 理想洞察 |
| INTJ | 建筑师 | The Architect | 战略思维 |
| ISTP | 鉴赏家 | The Virtuoso | 实用灵活 |
| ISFP | 探险家 | The Adventurer | 艺术感性 |
| INFP | 调停者 | The Mediator | 理想同理 |
| INTP | 逻辑学家 | The Logician | 分析创新 |
| ESTP | 企业家 | The Entrepreneur | 冒险行动 |
| ESFP | 表演者 | The Entertainer | 热情社交 |
| ENFP | 竞选者 | The Campaigner | 热情创意 |
| ENTP | 辩论家 | The Debater | 智辩创新 |
| ESTJ | 经理 | The Executive | 执行管理 |
| ESFJ | 执政官 | The Consul | 关怀社交 |
| ENFJ | 主人公 | The Protagonist | 领导激励 |
| ENTJ | 指挥官 | The Commander | 战略领导 |

---

## 报告内容 / Report Contents

### 完整分析报告包含 / Full Report Includes:

1. **类型确认 / Type Confirmation**
   - MBTI类型代码（如 INFP）
   - 类型名称（中文+英文）
   - 综合清晰度指数（0-100%）

2. **维度分析 / Dimension Analysis**
   - 能量倾向 E/I 分析
   - 信息获取 S/N 分析
   - 决策方式 T/F 分析
   - 生活态度 J/P 分析

3. **性格特征 / Personality Traits**
   - 核心优势 Strengths（5项）
   - 潜在劣势 Weaknesses（5项）

4. **职业建议 / Career Recommendations**
   - 推荐职业（5项）
   - 发展建议

5. **人际关系 / Relationships**
   - 最佳匹配类型
   - 挑战类型

---

## 使用方法 / Usage

### 运行测试 / Run Test

```bash
cd mbti-guru
python3 mbti.py
```

### 选择版本 / Select Version

```
╭──────────────────────────────────────╮
│   MBTI Guru - Choose Your Test      │
╰──────────────────────────────────────╯

1. 快速版 (70题) ~10分钟
2. 标准版 (93题) ~15分钟  
3. 扩展版 (144题) ~25分钟
4. 专业版 (200题) ~35分钟

请输入数字选择 / Enter number: 
```

### 回答问题 / Answer Questions

```
╭──────────────────────────────────────╮
│   问题 1/70                          │
╰──────────────────────────────────────╯

在聚会中，你通常是：
A) 和很多人热烈交谈，从中获得能量
B) 只和一两个熟悉的人深聊

请输入 A 或 B:
```

---

## 机器人命令 / Bot Commands

### 交互功能 / Interactive Features

| 命令 | 功能 |
|------|------|
| `/start` | 开始新测试 |
| `/resume` | 继续未完成的测试 |
| `/history` | 查看测试历史 |
| `/status` | 查看当前状态 |
| `/cancel` | 取消当前测试 |
| `/progress` | 查看当前进度 |

### 进度保存与恢复 / Progress Save & Resume

- **自动保存**：每10题自动保存一次进度
- **随时恢复**：使用 `/resume` 继续未完成的测试
- **状态查询**：使用 `/status` 查看当前进度

### 实时反馈 / Real-time Feedback

- 每20题发送一次维度分析反馈
- 显示当前倾向和可能的类型变化

### 进度条 / Progress Bar

```
📝 问题 50/70
[████████░░] 71% (50/70)
```

---

## 报告示例 / Sample Report

```
┌─────────────────────────────────────────────────┐
│        MBTI PERSONALITY REPORT                  │
│        MBTI人格分析报告                         │
├─────────────────────────────────────────────────┤
│                                                  │
│              🧠 INFP                            │
│          The Mediator                           │
│            调停者                               │
│                                                  │
│  Overall Clarity / 综合清晰度: 78%              │
│                                                  │
│  Dimension Scores / 维度得分:                   │
│  EI: ████████░░ 82% I (内向)                  │
│  SN: ██████░░░░ 65% N (直觉)                  │
│  TF: ████████░░ 78% F (情感)                  │
│  JP: ███████░░░ 71% P (知觉)                  │
│                                                  │
│  Strengths / 优势:                             │
│  1. Idealistic and principled (理想主义)        │
│  2. Creative and expressive (创意表达)          │
│  3. Compassionate and caring (富有同情心)        │
│                                                  │
│  Weaknesses / 劣势:                             │
│  1. Overly trusting (过度信任)                  │
│  2. Self-critical (自我批评)                    │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 项目结构 / Project Structure

```
mbti-guru/
├── SKILL.md              # 本文档 / This file
├── CLAWHUB.md           # ClawHub元数据
├── mbti.py              # CLI主入口 / Main entry
├── bot.py               # OpenClaw集成入口
├── lib/
│   ├── __init__.py       # OpenClaw接口
│   ├── mbti_core.py      # 核心逻辑（平台无关）
│   ├── telegram_handler.py # Telegram适配器
│   ├── mbti_types.py     # 16种人格数据
│   ├── questions.py      # 题库
│   ├── question_pool.py  # 题库池
│   ├── scorer.py         # 评分算法
│   ├── session.py        # 进度保存/恢复
│   ├── history.py        # 历史记录
│   ├── pdf_generator.py # PDF报告生成
│   ├── pdf_page1.py      # PDF第一页
│   ├── pdf_page2.py      # PDF第二页
│   ├── pdf_combined.py   # PDF合并
│   ├── cognitive.py      # 认知功能分析
│   └── relationships.py  # 人际关系
└── data/
    ├── sessions/         # 进度数据
    └── history/          # 历史记录
```

---

## 技术规格 / Specifications

| 项目 | 说明 |
|------|------|
| **编程语言** | Python 3.8+ |
| **题库容量** | 200+ 题目 |
| **报告格式** | Markdown + PDF |
| **语言支持** | 中文 / English |
| **评分算法** | 标准MBTI计分系统 |
| **PDF生成** | Matplotlib + ReportLab |

## 环境依赖 / Dependencies

```
matplotlib>=3.5.0
reportlab>=4.0.0
numpy>=1.20.0
```

## 数据存储 / Data Storage

| 数据类型 | 存储位置 | 说明 |
|----------|----------|------|
| 测试进度 | `data/sessions/` | JSON文件，仅存储当前测试进度 |
| 测试历史 | `data/history/` | JSON文件，仅存储已完成结果 |
| 答题数据 | 会话目录 | 用户ID与答题答案分离存储 |

**隐私说明**：
- 所有数据存储在用户本地服务器
- 不上传任何数据到外部服务器
- 用户可随时删除 `data/` 目录清除所有数据
- 数据文件命名使用匿名会话ID，不关联用户身份

## 渠道配置 / Channel Configuration

### Telegram Bot (可选)
```
TELEGRAM_BOT_TOKEN=your_bot_token
```
在 OpenClaw 配置文件中设置 `channels.telegram.botToken`

### 其他渠道
OpenClaw 自动支持：Discord, 飞书, 微信, Slack 等

---

## 算法说明 / Algorithm

### 计分原理 / Scoring Method

MBTI使用偏好选择计分法：

1. 每个维度统计两种偏好的选择次数
2. 计算每个偏好的百分比
3. 百分比高的一方决定该维度的类型
4. 清晰度指数 = |偏好百分比 - 50%| × 2

### 维度计算 / Dimension Calculation

- **E/I**: 外向 vs 内向倾向
- **S/N**: 感觉 vs 直觉倾向  
- **T/F**: 思考 vs 情感倾向
- **J/P**: 判断 vs 知觉倾向

---

## 局限性说明 / Limitations

1. MBTI是一种自我报告测试，结果仅供参考
2. 人格是复杂的，不能简单地归类为16种之一
3. 测试结果可能受情绪、环境等因素影响
4. 不建议将测试结果用于重大人生决策

---

## 版本历史 / Changelog

| 版本 | 日期 | 说明 |
|------|------|------|
| v1.5.2 | 2026-03-27 | 修复ClawHub元数据，完善依赖和隐私说明 |
| v1.5.1 | 2026-03-27 | 补充Python依赖和数据存储说明 |
| v1.5.0 | 2026-03-27 | 平台无关架构重构，支持所有OpenClaw渠道 |
| v1.4.1 | 2026-03-27 | 修复跨进程session恢复bug |
| v1.4.0 | 2026-03-27 | 正式版 - 全部功能完成、PDF定版、测试通过 |
| v1.0.0 | 2026-03-26 | 初始版本 |

---

## 授权 / License

Apache License 2.0

---

## 联系方式 / Contact

**作者**: MBTI Guru Team  
**版本**: v1.5.2 (正式版)  
**更新**: 2026-03-27
