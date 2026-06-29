---
name: preschool-teacher-assistant
description: "🌸 AI幼师全流程助手（幼教百宝箱）。输入一句话，自动生成教案/观察记录/家园沟通/活动设计/教学计划/环境创设/教学反思/幼儿故事等8大类幼教文档，输出交互式HTML可视化报告。内置《3-6岁儿童学习与发展指南》知识库，支持五大领域×三年龄段全覆盖。触发词：幼教, 幼师, 幼儿园, 教案, 观察记录, 家长通知, 家长会发言, 期末评语, 活动设计, 环境创设, 环创, 教学计划, 教学反思, 幼儿故事, 家园共育, 五大领域, 小班, 中班, 大班, 幼师AI, 幼教AI, 幼儿园教案, 幼儿观察, preschool teacher, kindergarten lesson plan, 幼教百宝箱"
agent_created: true
---

# 幼教百宝箱 — AI幼师全流程助手

一句话生成教案、观察记录、家长沟通、活动设计、教学计划、环境创设、教学反思、幼儿故事 — 覆盖幼师全部文案场景。

## 能做什么

输入一句话，自动完成以下8大模块：

1. 📖 **教案生成**：五大领域（健康/语言/社会/科学/艺术）× 三年龄段（小班3-4岁/中班4-5岁/大班5-6岁），智能生成完整教案
2. 🔍 **观察记录**：幼儿行为观察实录、行为分析、教育策略、家园共育建议
3. 💬 **家园共育**：家长通知、期末评语、家长会发言稿，专业温暖一键生成
4. 🎮 **活动设计**：主题活动、游戏活动方案设计（含目标、流程、注意事项）
5. 📅 **教学计划**：学期/月/周/日计划，自动生成结构化教学安排
6. 🎨 **环境创设**：主题墙面、区角规划、配色方案、安全要求
7. 📝 **教学反思**：活动亮点/不足分析、幼儿表现评估、改进措施
8. 📚 **故事创作**：按年龄段生成适合的教育故事，含互动提问和延伸活动

**核心竞争力：**
- 内置《3-6岁儿童学习与发展指南》知识库，所有内容对标国家标准
- 支持**内置模板**（零依赖开箱即用）和**LLM增强**（DeepSeek/OpenAI 接入）双模式
- 输出**交互式HTML可视化报告**，手机电脑都能看
- 一站式覆盖幼师全部文案需求，不用切多个App

## 与其他幼师工具对比

| 功能 | 幼师OK网 | 幼伴App | 幼师AI工坊 | **幼教百宝箱** |
|------|---------|---------|-----------|-------------|
| 教案生成 | ✅ | ✅ | ✅ | ✅ |
| 观察记录 | ✅ | ✅ | ✅ | ✅ |
| 家园沟通 | ✅ | ❌ | ✅ | ✅ |
| 教学反思 | ❌ | ❌ | ✅ | ✅ |
| 环境创设 | ❌ | ✅ | ✅ | ✅ |
| 幼儿故事 | ❌ | ❌ | ✅ | ✅ |
| 指南对标 | 部分 | 部分 | ✅ | ✅ **完整内置** |
| 离线可用 | ❌ 需联网 | ❌ 需联网 | ❌ 需联网 | ✅ **内置模板零依赖** |
| HTML报告 | ❌ | ❌ | ❌ | ✅ **交互式可视化** |
| 免费 | 部分 | 部分 | 部分 | ✅ **完全免费** |

## 快速开始

### 体验演示（零依赖，30秒出结果）

```bash
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py --mode demo
```

### 教案生成

```bash
# 语言领域 - 中班
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode lesson_plan --domain 语言 --age 中班 --query "春天的色彩"

# 科学领域 - 大班
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode lesson_plan --domain 科学 --age 大班 --query "有趣的沉浮实验"

# 艺术领域 - 小班
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode lesson_plan --domain 艺术 --age 小班 --query "漂亮的小花"
```

### 观察记录

```bash
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode observation --age 小班 --query "小明在积木区主动分享玩具给同伴"
```

### 家园沟通

```bash
# 家长通知
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode communication --sub 通知 --query "春游活动通知"

# 期末评语
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode communication --sub 评语 --query "朵朵"

# 家长会发言稿
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode communication --sub 发言稿 --query "中班下学期家长会"
```

### 活动设计

```bash
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode activity --age 大班 --query "端午节主题游戏"
```

### 教学计划

```bash
# 周计划
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode plan --plan_type 周计划 --query "春天来了"

# 学期计划
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode plan --plan_type 学期计划 --query "幼小衔接"
```

### 环境创设

```bash
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode environment --query "海底世界主题环创"
```

### 教学反思

```bash
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode reflection --query "科学活动：浮与沉"
```

### 故事创作

```bash
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode story --age 小班 --query "勇敢的小白兔"
```

### LLM增强模式（需API Key，质量更高）

```bash
# 使用 DeepSeek（国内推荐）
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode lesson_plan --domain 语言 --age 中班 --query "春天的色彩" \
  --api-key YOUR_DEEPSEEK_KEY \
  --api-base https://api.deepseek.com/v1 \
  --model deepseek-chat

# 使用 DashScope（阿里云）
python ~/.workbuddy/skills/preschool-teacher-assistant/scripts/preschool_teacher.py \
  --mode lesson_plan --domain 科学 --age 大班 --query "磁铁的奥秘" \
  --api-key YOUR_DASHSCOPE_KEY \
  --api-base https://dashscope.aliyuncs.com/compatible-mode/v1 \
  --model qwen-plus
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--mode` / `-m` | ✅ | - | 功能模式：demo/lesson_plan/observation/communication/activity/plan/environment/reflection/story/report |
| `--query` / `-q` | ❌ | 模式默认 | 用户输入，如教案主题、幼儿名、活动名 |
| `--domain` / `-d` | ❌ | 语言 | 五大领域：健康/语言/社会/科学/艺术（仅lesson_plan） |
| `--age` / `-a` | ❌ | 中班 | 年龄段：小班/中班/大班 |
| `--sub` | ❌ | 通知 | 沟通子类型：通知/评语/发言稿（仅communication） |
| `--plan_type` / `-p` | ❌ | 周计划 | 计划类型：学期计划/月计划/周计划/日计划（仅plan） |
| `--api-key` | ❌ | - | LLM API Key（不提供则使用内置模板） |
| `--api-base` | ❌ | https://api.openai.com/v1 | API Base URL |
| `--model` | ❌ | gpt-4o-mini | 模型名称 |
| `--output` / `-o` | ❌ | 自动生成 | 输出文件路径 |
| `--json` | ❌ | False | 输出JSON格式到stdout |

## 典型使用场景

### WorkBuddy 对话式使用

当用户在 WorkBuddy 中说：
- "帮我写一份中班语言活动教案，主题是春天"
- "生成一份小班幼儿的观察记录"
- "写一份期末家长会发言稿"
- "设计一个大班端午节活动方案"
- "帮我做个海底世界的环创方案"
- "给朵朵写一份期末评语"
- "反思一下今天的科学活动课"

Agent 会自动加载本技能，调用对应的脚本模式，生成HTML报告返回给用户。

## 技术架构

```
用户输入 "帮我写中班语言教案：春天"
    ↓
┌──────────────────────────────────────────────────┐
│ 智能路由：识别意图 → 教案/观察/沟通/活动/计划     │
│ 参数提取：领域、年龄段、主题                       │
└──────────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────────┐
│ 内容生成引擎                                       │
│ ├── 内置模板引擎（零依赖，30ms）                   │
│ └── LLM增强引擎（需API Key，质量更优）             │
└──────────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────────┐
│ 知识库注入                                         │
│ ├── 《3-6岁儿童学习与发展指南》五大领域目标        │
│ ├── 三年龄段发展特点                                │
│ └── 领域关键词匹配                                 │
└──────────────────────────────────────────────────┘
    ↓
┌──────────────────────────────────────────────────┐
│ HTML报告生成                                       │
│ ├── 可爱温馨的视觉风格（粉色调）                    │
│ ├── 模块化卡片布局                                  │
│ ├── 今日幼教小贴士                                  │
│ └── 响应式设计（手机/平板/PC）                      │
└──────────────────────────────────────────────────┘
```

## 文件结构

```
~/.workbuddy/skills/preschool-teacher-assistant/
├── SKILL.md                              # 技能描述（本文件）
└── scripts/
    └── preschool_teacher.py              # 核心脚本（零依赖）
```

## 《3-6岁儿童学习与发展指南》对标

脚本内置了完整的指南核心知识库：

### 五大领域
- **健康**：身心状况、动作发展、生活习惯与生活能力
- **语言**：倾听与表达、阅读与书写准备
- **社会**：人际交往、社会适应
- **科学**：科学探究、数学认知
- **艺术**：感受与欣赏、表现与创造

### 三年龄段特点
- **小班（3-4岁）**：情绪作用大、爱模仿、思维具体形象
- **中班（4-5岁）**：活泼好动、社交需求增强、规则意识萌芽
- **大班（5-6岁）**：好奇好问、合作意识增强、为入学做好准备

所有生成内容均对标指南要求，确保教育专业性。

## LLM API 配置

### DeepSeek（国内推荐，性价比高）
```
--api-key sk-xxx --api-base https://api.deepseek.com/v1 --model deepseek-chat
```

### 阿里云 DashScope
```
--api-key sk-xxx --api-base https://dashscope.aliyuncs.com/compatible-mode/v1 --model qwen-plus
```

### OpenAI
```
--api-key sk-xxx --api-base https://api.openai.com/v1 --model gpt-4o-mini
```

不提供 `--api-key` 时，默认使用内置模板引擎，质量同样专业可用。

## 注意事项

- 📱 **零依赖**：内置模板模式无需安装任何额外包，纯Python标准库即可运行
- 🎨 **视觉风格**：HTML报告采用粉色调温馨风格，贴合幼教场景
- 📚 **指南对标**：所有内容基于《3-6岁儿童学习与发展指南》（教育部）
- 💰 **免费使用**：内置模板完全免费，LLM模式仅产生API调用费
- ⚡ **秒级生成**：内置模板模式下30ms生成，LLM模式约3-10秒
- 🌐 **离线可用**：内置模板模式完全离线，无需网络连接

## 常见问题

**Q: 没有API Key能用吗？**
A: 完全可以！内置模板引擎覆盖所有8大模块，无需任何API Key，零依赖开箱即用。

**Q: 生成的内容能用在实际教学中吗？**
A: 可以。所有内容对标《3-6岁儿童学习与发展指南》，具有专业性。建议根据本班实际情况微调后使用。

**Q: LLM模式和内置模板模式有什么区别？**
A: 内置模板模式基于知识库规则生成，质量稳定；LLM模式接入大模型，生成内容更灵活、更具创造力。

**Q: 生成的HTML报告能分享给家长吗？**
A: 可以。HTML报告是独立的单文件，可直接发送或打印。

**Q: 支持哪些年龄段？**
A: 小班（3-4岁）、中班（4-5岁）、大班（5-6岁），覆盖幼儿园完整年龄段。

## 更新日志

- **v1.0.0** (2026-06-20): 初始版本
  - 8大功能模块全覆盖
  - 内置《3-6岁儿童学习与发展指南》知识库
  - 五大领域 × 三年龄段
  - 交互式HTML可视化报告
  - 内置模板 + LLM增强双模式
  - Demo模式一键演示
