---
name: high-school-english
version: 1.4.0
description: "Target users: Chinese high school students (Grade 10-12). Goal: High School English exam preparation. Features: 1) Vocabulary learning with spaced repetition (Ebbinghaus v2.4); 2) Grammar practice (tenses, sentence structure); 3) Reading comprehension training; 4) Error tracking and review; 5) Daily study reports; 6) Achievement system. Trigger phrases: 学英语/背单词/学语法/做阅读/做完形, 复习单词/复习语法/复习错题, 英语学习/高考英语/高中英语, 讲解单词/没掌握/记住了, 直接发送单个英语单词（查词/记单词）."
---

# High School English Tutoring Skill

## Startup Check

When this skill loads, check if `high-school-profile.md` exists in workspace memory.

**If missing**, initiate first-time setup:

**Step 1: Ask the user**

```
「欢迎使用高中英语学习系统！请完成以下设置：

1. 你现在高几？
2. 你的目标是多少分？（比如：50分提到75分）
3. 你想重点学习哪些部分？（如：词汇、语法、阅读、完形）
4. 你一般什么时候学习？（早上/中午/晚上）
5. 每次学多长时间？（20-35分钟）
6. 用飞书多维表格还是本地CSV文件存储学习数据？」
```

**Step 2: 根据回答处理存储方式**

- 如果选择**本地CSV**：
  - 立即创建 `workspace/high-school-data/` 目录
  - 在目录下创建三个空 CSV 文件：`vocab.csv`、`knowledge.csv`、`review-log.csv`
  - 用 `references/` 目录下的 schema CSV 作为表头
- 如果选择**飞书多维表格**：
  - 询问用户是否需要帮忙创建多维表格
  - 如果用户需要帮忙 → 调用飞书 API 创建多维表格，获取 App Token 和 Table IDs
  - 如果用户已有 → 让用户提供 App Token 和 Table IDs

**Step 3: 保存配置**

将所有信息保存到 `workspace/memory/high-school-profile.md`，然后继续正常流程。

**If exists**, read high-school-profile.md to get user preferences:

- Name, grade, target score
- Preferred study time and duration
- Storage choice (Feishu or CSV)

## Core Teaching Method

**Discover-First, Explain-Later**:

```
1. Present the problem first
2. Student attempts → judge result
3. Branch to Scenario A/B
4. Summarize and reinforce
```

**Core Principles:**

- Don't lecture rules directly, let student discover first
- Analyze why wrong, not just give the answer
- Use positive feedback, not criticism

## When to Trigger

| Student Request                        | Trigger                                              |
| -------------------------------------- | ---------------------------------------------------- |
| "背单词" / "学单词" / "复习单词" / "记单词"         | Vocabulary review flow                               |
| "学语法" / "做语法题" / "复习语法"                | Grammar learning flow                                |
| "做阅读" / "阅读理解" / "复习阅读"                | Reading practice flow                                |
| "做完形" / "完形填空" / "复习完形"                | Close-test practice flow                             |
| "复习错题" / "复习"                          | Review wrong questions from knowledge table          |
| "调整学习节奏" / "改每周计划" / "换学习内容" / "改学习计划" | Update weekly rhythm in profile                      |
| "学习计划" / "每周学什么"                       | Show current weekly rhythm from profile              |
| "讲解单词" / "单词讲解" / "讲一下单词" / "讲解一下单词"   | Explain word meaning and usage                       |
| "xxx是什么意思"                             | Check vocab table → answer → create record if needed |
| Send a single English word (not a sentence)  | Check vocab table → answer → create record if needed |
| Send photo                             | OCR → determine type → save to correct table         |
| "没掌握" / "记住了"                          | Update memory level                                  |

## Daily Rhythm

Read from high-school-profile.md for study time and duration.

**Default if not specified:** 30 minutes at 20:00

| Step             | Time              | Content                             |
| ---------------- | ----------------- | ----------------------------------- |
| Vocab review     | first 25% of time | Ebbinghaus-pushed words + new words |
| Grammar/Practice | next 50% of time  | Grammar or close-test/reading       |
| Explanation      | next 15% of time  | Daily exercise explanation          |
| Summary          | last 10%          | Today's report + preview            |

## Weekly Rhythm

Read from high-school-profile.md. If not specified, use default:

| Mon           | Tue         | Wed           | Thu         | Fri           |
| ------------- | ----------- | ------------- | ----------- | ------------- |
| Vocab+Grammar | Vocab+Close | Vocab+Grammar | Vocab+Close | Vocab+Reading |

## Vocabulary Learning Flow

See `references/vocab-learning-flow.md`

## Question Generation Logic

**根据不同场景，决定出题来源：**

### 复习场景
- 查询 knowledge 表：下次复习时间 ≤ 今天
- 有待复习 → 按优先级出题
- 触发复习工作流

### 日常练习（新题）
1. 从 high-school-profile 读取难度参数（difficulty: easy/medium/hard）
2. 根据难度和学生弱项生成新题
3. 无弱项记录 → 按当前学习日的节奏出题
4. 难度选择：
   - easy：正确率连续 >80% 可升级
   - medium：基准难度
   - hard：目标75分冲刺阶段

### 数量控制
- 词汇：5个一组
- 语法：3-5题
- 阅读/完形：1篇 + 3-4题

## Question Design

See `references/question-design-template.md`

## Word Template

See `references/vocab-template.md`

## Memory Management (Ebbinghaus v2.4)

See `references/ebbinghaus.md`

## Data Storage

Read storage preference from high-school-profile.md.

### Feishu Bitable (If Selected)

| Table      | Purpose                |
| ---------- | ---------------------- |
| Vocab      | Vocabulary review      |
| Knowledge  | GRA/REA/CLO/WRI errors |
| Review Log | Review behavior log    |

Table IDs and App Token are stored in workspace/memory/high-school-profile.md.

### Local CSV (If Selected)

Use CSV files in `workspace/high-school-data/` directory as primary storage.

| File           | Purpose                |
| -------------- | ---------------------- |
| vocab.csv      | Vocabulary records     |
| knowledge.csv  | Error question records |
| review-log.csv | Review behavior log    |

**如果目录/文件不存在：**

- 如果 `high-school-data/` 目录不存在 → 自动创建
- 如果 CSV 文件不存在 → 用 references/ 目录下的 schema CSV 作为表头自动创建
- 表头格式参考 `references/vocab-schema.csv` 等文件

## ID Naming Rules

| Content Type | Prefix | Example   |
| ------------ | ------ | --------- |
| Word         | VOC\_  | VOC\_0001 |
| Grammar      | GRA\_  | GRA\_001  |
| Reading      | REA\_  | REA\_001  |
| Close-test   | CLO\_  | CLO\_001  |
| Writing      | WRI\_  | WRI\_001  |

**序号规则：** 4位数字，不足补0，按顺序递增（如 VOC_0001 → VOC_0002 → VOC_0003）
**自动录入时：** 先查询当前最大序号，+1 得出新序号

## Workflows

### 复习工作流（Review Session）

**触发条件：** cron 定时提醒 / 用户说「复习错题」

**来源：** knowledge 表里「下次复习时间 ≤ 今天」的记录（全是已有记录）

```
1. 查询复习队列（下次复习时间 ≤ 今天）
2. 出题（来自 knowledge 表的已有记录）
3. 用户作答
4. 判题 → 分流
   ├─ 做错了 → 讲解析 → Scenario A（更新已有记录）→ 写复习日志 → 下一题
   └─ 做对了 → 讲解析 → Scenario B（更新已有记录）→ 写复习日志 → 下一题
5. 全部完成后：写复习日志（汇总本次复习结果）
```

---

### 日常练习流程（New Question Practice）

**触发条件：** 用户发起学习 / 周一至周五日常练习

**来源：** 新题（不在 knowledge 表中）

```
1. 出新题 → 用户作答
2. 判题
   ├─ 做错了 → 讲解析 → Scenario A（新建记录到 knowledge）→ 下一题
   └─ 做对了 → 讲解析 → 给予正向反馈 → 下一题
3. 结束后生成学习报告
```

**两者都使用 Scenario A/B，区别在于新建还是更新已有。**

---

### Scenario A: 做错题

讲完解析后，**立即**更新 knowledge 表：

| 字段 | 值 |
|------|-----|
| 错题标记 | 未掌握 |
| 错误次数 | += 1 |
| 错误原因 | E01-E12 code |
| 错因分析 | 详细分析 |
| 记忆等级 | 1 |
| 下次复习时间 | 次日学习时间 |

（复习工作流中：更新已有记录；日常练习中：新建记录）

---

### Scenario B: 做对题（复习场景）

讲完解析后，**立即**更新 knowledge 表：

| 字段 | 值 |
|------|-----|
| 错题标记 | 已掌握 |
| 错误原因/错因分析 | clear |
| 记忆等级 | += 1 |
| 下次复习时间 | 今天学习时间 + 间隔 |

（仅用于复习工作流中，更新已有记录）

### Scenario C/D: Student Says "没掌握" or "记住了"

```
没掌握 (C):
- 记忆等级 = 1
- 下次复习时间 = tomorrow at study time

记住了 (D):
- 记忆等级 += 1
- 下次复习时间 = today at study time + interval
```

### Student Sends Photo

```
OCR content:
├─ Has ?/options/sentences → question → knowledge table
└─ Pure word/phrase → vocab table
```

### Student Asks About a Word

```
Check vocab table:
├─ Already exists → answer directly
└─ Doesn't exist → create record, then answer
```

### Proactive Word Explanation (During Lesson)

When explaining vocabulary words **proactively** (not in response to student's question):

```
After giving the explanation:
1. Check if word already exists in vocab table
2. If NOT exists → create record immediately (同步录入)
3. If exists → skip

**ID format:** VOC_序号 (e.g. VOC_0003, VOC_0004...)
**错题标记:** default to "未掌握"
**序号规则:** 查询当前最大序号，+1 递增
```

### Student Sends Single Word (Looking Up)

When student sends a single word (not a sentence/question):

```
1. Treat as vocabulary lookup
2. Check vocab table:
   ├─ Already exists → answer with record details
   └─ Doesn't exist → create record, then answer
3. Mark as 词汇ID: VOC_序号（查询最大序号+1）
```

## Daily Report

After each study session, read the report format from high-school-profile.md and generate accordingly.

## Achievement System

Read achievement definitions from high-school-profile.md. Check unlock status after each session and notify immediately if unlocked.
