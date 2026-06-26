# MBTIClaude

[中文](#中文版) | [English](#english-version)

## English Version

Infer MBTI personality types by analyzing user prompts across multiple AI tools (Claude Code, Codex, Gemini, OpenCode, OpenClaw).

### Introduction

MBTIClaude is an innovative MBTI personality analysis tool that doesn't rely on traditional questionnaires. Instead, it infers your MBTI personality type by analyzing your prompt patterns when using AI tools in daily work.

### Features

- 🔍 **Multi-tool Support**: Analyzes history data from Claude Code, Codex, Gemini, OpenCode, and OpenClaw
- 🧠 **Intelligent Analysis**: Deep behavioral pattern analysis based on four MBTI dimensions
- 📊 **Detailed Reports**: Provides complete data statistics and dimension analysis results
- 🚀 **Ready to Use**: No configuration needed, automatically extracts local history data

### Supported AI Tools

| Tool | Data Path | Description |
|------|-----------|-------------|
| Claude Code | `~/.claude/history.jsonl` | Official Claude CLI tool |
| Codex | `~/.codex/history.jsonl` | OpenAI Codex CLI |
| Gemini | `~/.gemini/tmp/*/chats/*.json` | Google Gemini CLI |
| OpenCode | `~/.local/state/opencode/prompt-history.jsonl` | OpenCode tool |
| OpenClaw | `~/.openclaw/agents/*/sessions/*.jsonl` | OpenClaw multi-agent system |

### Installation

#### Method 1: Using npx skills add (Recommended)

```bash
# Install from GitHub
npx skills add xmanrui/mbtiClaude

# Or use full URL
npx skills add https://github.com/xmanrui/mbtiClaude
```

#### Method 2: Using npx directly

```bash
# One-click install
npx github:xmanrui/mbtiClaude

# View help
npx github:xmanrui/mbtiClaude --help
```

#### Method 3: Manual installation

```bash
# Using curl
curl -fsSL https://raw.githubusercontent.com/xmanrui/mbtiClaude/main/SKILL.md -o ~/.claude/skills/mbticlaude.md

# Or using git clone
git clone https://github.com/xmanrui/mbtiClaude.git /tmp/mbtiClaude
cp /tmp/mbtiClaude/SKILL.md ~/.claude/skills/mbticlaude.md
rm -rf /tmp/mbtiClaude
```

### Usage

#### In Claude Code

```bash
/mbticlaude
```

#### Direct execution

```bash
python3 mbti_analyzer.py
```

### Analysis Dimensions

MBTIClaude analyzes your MBTI type based on the following four dimensions:

#### 1. Communication Style (E vs I)
- **E (Extrovert)**: Detailed prompts, includes background information, tends to elaborate
- **I (Introvert)**: Concise prompts, task-oriented, direct instructions

**Analysis Metrics:**
- Average prompt length
- Ratio of short instructions (<20 characters)
- Frequency of social expressions

#### 2. Information Processing (S vs N)
- **S (Sensing)**: Focuses on concrete details, implementation steps, visible results
- **N (Intuition)**: Focuses on abstract concepts, system architecture, innovative ideas

**Analysis Metrics:**
- Frequency of abstract concept keywords (concept, system, architecture, solution)
- Frequency of concrete detail keywords (specific, implementation, details, button)

#### 3. Decision Making (T vs F)
- **T (Thinking)**: Logic-oriented, focuses on efficiency, technical language
- **F (Feeling)**: Emotion-oriented, considers interpersonal relationships, emotional expression

**Analysis Metrics:**
- Frequency of logical keywords (optimize, efficiency, performance, analysis)
- Frequency of emotional keywords (feel, like, hope, thank)

#### 4. Lifestyle (J vs P)
- **J (Judging)**: Strong planning, structured, systematic planning
- **P (Perceiving)**: Flexible, exploratory, rapid iteration

**Analysis Metrics:**
- Frequency of planning keywords (plan, solution, design, PRD)
- Frequency of flexibility keywords (try, test, optimize, adjust)

### Example Output

```
🔍 Extracting user prompts...

📊 Data Statistics:
  Claude Code: 100 entries
  Codex: 100 entries
  Gemini: 62 entries
  OpenCode: 2 entries
  OpenClaw: 100 entries
  Total: 364 entries

🧠 Analyzing MBTI dimensions...

==================================================
🎯 Your MBTI Type: INTP
==================================================

Type Name: Logician

📋 Dimension Analysis:
  I - Introvert: Concise and efficient communication
  N - Intuition: Abstract thinking, systematic solutions
  T - Thinking: Pure rationality, focus on efficiency
  P - Perceiving: Flexible exploration, rapid iteration

⚠️  Important Reminders:
  1. Based on work scenario behavior inference, may not reflect true personality
  2. MBTI itself has scientific controversies, for reference only
  3. This is behavioral pattern inference, not professional psychological assessment
```

### MBTI Type Descriptions

| Type | Name | Characteristics |
|------|------|-----------------|
| INTJ | Architect | Strategic thinking, independent, perfectionist |
| INTP | Logician | Innovative thinking, rational analysis, flexible exploration |
| ENTJ | Commander | Strong leadership, decisive, goal-oriented |
| ENTP | Debater | Good at debating, innovative, challenges tradition |
| INFJ | Advocate | Idealistic, insightful, caring for others |
| INFP | Mediator | Value-driven, creative, empathetic |
| ENFJ | Protagonist | Charismatic leader, good at motivating, focuses on growth |
| ENFP | Campaigner | Enthusiastic, creative, strong social skills |
| ISTJ | Logistician | Reliable, practical, detail-oriented |
| ISFJ | Defender | Loyal, careful, helpful |
| ESTJ | Executive | Strong organizational skills, practical, traditional |
| ESFJ | Consul | Warm-hearted, cooperative, focuses on harmony |
| ISTP | Virtuoso | Strong practical skills, flexible, calm |
| ISFP | Adventurer | Artistic temperament, flexible, gentle |
| ESTP | Entrepreneur | Action-oriented, adaptable, good at improvising |
| ESFP | Entertainer | Energetic, enjoys the moment, social butterfly |

### How It Works

1. **Data Extraction**: Extracts user prompts from local AI tool history records
2. **Data Cleaning**: Filters system messages, metadata, and other non-user input content
3. **Feature Analysis**: Analyzes behavioral patterns based on keyword frequency, prompt length, and other metrics
4. **Type Inference**: Infers MBTI type based on analysis results from four dimensions
5. **Result Display**: Generates detailed analysis report

### Important Notes

⚠️ **Important Reminders:**

1. **Scenario Limitations**: Analysis is based on AI tool usage behavior in work scenarios, may not fully reflect true personality
2. **Scientific Controversy**: MBTI itself is controversial in psychology, results are for reference only
3. **Non-professional Assessment**: This is behavioral pattern inference, cannot replace professional psychological assessment
4. **Data Requirements**: Requires sufficient historical data (at least 50 prompts recommended) for accurate conclusions
5. **Privacy Protection**: All analysis is performed locally, no data is uploaded

### Tech Stack

- Python 3.x
- JSON data processing
- Natural language analysis
- Behavioral pattern recognition

### Contributing

Issues and Pull Requests are welcome!

#### Improvement Directions

- [ ] Support more AI tools
- [ ] Optimize analysis algorithms
- [ ] Add more analysis dimensions
- [ ] Provide visualization reports
- [ ] Support multilingual analysis

### License

MIT License

### Acknowledgments

Thanks to all AI tool developers for providing powerful tools that made this project possible.

---

## 中文版

# MBTIClaude

通过分析用户在多个 AI 工具（Claude Code、Codex、Gemini、OpenCode、OpenClaw） 的提示词来推测 MBTI 性格类型。

## 简介

MBTIClaude 是一个创新的 MBTI 性格分析工具，它不依赖传统的问卷测试，而是通过分析你在日常使用 AI 工具时的提示词模式来推测你的 MBTI 性格类型。

## 特性

- 🔍 **多工具支持**：支持分析 Claude Code、Codex、Gemini、OpenCode、OpenClaw 五种 AI 工具的历史数据
- 🧠 **智能分析**：基于四个 MBTI 维度进行深度行为模式分析
- 📊 **详细报告**：提供完整的数据统计和维度分析结果
- 🚀 **即开即用**：无需配置，自动提取本地历史数据

## 支持的 AI 工具

| 工具 | 数据路径 | 说明 |
|------|---------|------|
| Claude Code | `~/.claude/history.jsonl` | Claude 官方 CLI 工具 |
| Codex | `~/.codex/history.jsonl` | OpenAI Codex CLI |
| Gemini | `~/.gemini/tmp/*/chats/*.json` | Google Gemini CLI |
| OpenCode | `~/.local/state/opencode/prompt-history.jsonl` | OpenCode 工具 |
| OpenClaw | `~/.openclaw/agents/*/sessions/*.jsonl` | OpenClaw 多 agent 系统 |

## 安装

### 方法一：使用 npx skills add（推荐）

```bash
# 从 GitHub 安装
npx skills add xmanrui/mbtiClaude

# 或使用完整 URL
npx skills add https://github.com/xmanrui/mbtiClaude
```

### 方法二：使用 npx 直接安装

```bash
# 一键安装
npx github:xmanrui/mbtiClaude

# 查看帮助
npx github:xmanrui/mbtiClaude --help
```

### 方法三：手动安装

```bash
# 使用 curl
curl -fsSL https://raw.githubusercontent.com/xmanrui/mbtiClaude/main/SKILL.md -o ~/.claude/skills/mbticlaude.md

# 或使用 git clone
git clone https://github.com/xmanrui/mbtiClaude.git /tmp/mbtiClaude
cp /tmp/mbtiClaude/SKILL.md ~/.claude/skills/mbticlaude.md
rm -rf /tmp/mbtiClaude
```

## 使用方法

### 在 Claude Code 中使用

```bash
/mbticlaude
```

### 直接运行

```bash
python3 mbti_analyzer.py
```

## 分析维度

MBTIClaude 基于以下四个维度分析你的 MBTI 类型：

### 1. 沟通风格 (E vs I)
- **E (外向)**：提示词详细、包含背景说明、倾向于长篇表达
- **I (内向)**：提示词简洁、任务导向、直接指令

**分析指标：**
- 平均提示词长度
- 简短指令（<20字符）占比
- 社交性表达频率

### 2. 信息处理 (S vs N)
- **S (感觉)**：关注具体细节、实现步骤、可见的结果
- **N (直觉)**：关注抽象概念、系统架构、创新思路

**分析指标：**
- 抽象概念关键词频率（概念、系统、架构、方案）
- 具体细节关键词频率（具体、实现、细节、按钮）

### 3. 决策方式 (T vs F)
- **T (思考)**：逻辑导向、关注效率、技术语言
- **F (情感)**：情感导向、考虑人际关系、情感表达

**分析指标：**
- 逻辑性关键词频率（优化、效率、性能、分析）
- 情感性关键词频率（感觉、喜欢、希望、谢谢）

### 4. 生活方式 (J vs P)
- **J (判断)**：计划性强、结构化、系统规划
- **P (知觉)**：灵活性强、探索性、快速迭代

**分析指标：**
- 计划性关键词频率（计划、方案、设计、PRD）
- 灵活性关键词频率（试试、测试、优化、调整）

## 示例输出

```
🔍 正在提取用户提示词...

📊 数据统计：
  Claude Code: 100 条
  Codex: 100 条
  Gemini: 62 条
  OpenCode: 2 条
  OpenClaw: 100 条
  总计: 364 条

🧠 正在分析 MBTI 维度...

==================================================
🎯 你的 MBTI 类型：INTP
==================================================

类型名称：逻辑学家

📋 维度分析：
  I - 内向：简洁高效沟通
  N - 直觉：抽象思维，系统化方案
  T - 思考：纯理性，关注效率
  P - 知觉：灵活探索，快速迭代

⚠️  重要提醒：
  1. 基于工作场景的行为推测，可能不反映真实性格
  2. MBTI 本身科学性存疑，仅供参考
  3. 这是基于行为模式的推测，非专业心理测评
```

## MBTI 类型说明

| 类型 | 名称 | 特征 |
|------|------|------|
| INTJ | 建筑师 | 战略思维、独立、追求完美 |
| INTP | 逻辑学家 | 创新思维、理性分析、灵活探索 |
| ENTJ | 指挥官 | 领导力强、果断、目标导向 |
| ENTP | 辩论家 | 善于辩论、创新、挑战传统 |
| INFJ | 提倡者 | 理想主义、洞察力强、关心他人 |
| INFP | 调停者 | 价值观驱动、创造力、同理心 |
| ENFJ | 主人公 | 魅力领袖、善于激励、关注成长 |
| ENFP | 竞选者 | 热情洋溢、创造力、社交能力强 |
| ISTJ | 物流师 | 可靠、务实、注重细节 |
| ISFJ | 守卫者 | 忠诚、细心、乐于助人 |
| ESTJ | 总经理 | 组织能力强、务实、传统 |
| ESFJ | 执政官 | 热心、合作、关注和谐 |
| ISTP | 鉴赏家 | 实践能力强、灵活、冷静 |
| ISFP | 探险家 | 艺术气质、灵活、温和 |
| ESTP | 企业家 | 行动派、适应力强、善于应变 |
| ESFP | 表演者 | 活力四射、享受当下、社交达人 |

## 工作原理

1. **数据提取**：从本地 AI 工具的历史记录中提取用户提示词
2. **数据清洗**：过滤系统消息、元数据等非用户输入内容
3. **特征分析**：基于关键词频率、提示词长度等指标分析行为模式
4. **类型推测**：根据四个维度的分析结果推测 MBTI 类型
5. **结果展示**：生成详细的分析报告

## 注意事项

⚠️ **重要提醒：**

1. **场景局限性**：分析基于工作场景下的 AI 工具使用行为，可能不完全反映真实性格
2. **科学性争议**：MBTI 本身在心理学界存在争议，结果仅供参考
3. **非专业测评**：这是基于行为模式的推测，不能替代专业心理测评
4. **数据要求**：需要足够的历史数据（建议至少 50 条提示词）才能得出较准确的结论
5. **隐私保护**：所有分析在本地进行，不会上传任何数据

## 技术栈

- Python 3.x
- JSON 数据处理
- 自然语言分析
- 行为模式识别

## 贡献

欢迎提交 Issue 和 Pull Request！

### 改进方向

- [ ] 支持更多 AI 工具
- [ ] 优化分析算法
- [ ] 增加更多分析维度
- [ ] 提供可视化报告
- [ ] 支持多语言分析

## 许可证

MIT License

## 致谢

感谢所有 AI 工具开发者为我们提供了强大的工具，让这个项目成为可能。

---

**Made with ❤️ by xmr**
