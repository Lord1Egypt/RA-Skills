# MBTI Personality Test Skill - Design Document v2

## 1. Overview

**Skill Name:** MBTI Personality Analyzer
**Purpose:** Interactive personality test with detailed analysis
**Output:** 16 personality types with comprehensive reports

---

## 2. Test Versions

| Version | Questions | Time | Use Case |
|---------|----------|------|----------|
| Quick | 70 | ~10 min | Fast assessment |
| Standard | 93 | ~15 min | Formal testing |
| Extended | 144 | ~25 min | Deep analysis |
| Professional | 200 | ~35 min | Clinical use |

---

## 3. MBTI Theory

### 4 Dimensions

| Dimension | Preference A | Preference B |
|-----------|--------------|--------------|
| Energy | E (Extraversion) | I (Introversion) |
| Information | S (Sensing) | N (Intuition) |
| Decisions | T (Thinking) | F (Feeling) |
| Structure | J (Judging) | P (Perceiving) |

### 16 Personality Types

| Type | Name | E/I | S/N | T/F | J/P |
|------|------|------|-----|-----|-----|
| ISTJ | 物流师 | I | S | T | J |
| ISFJ | 守卫者 | I | S | F | J |
| INFJ | 提倡者 | I | N | F | J |
| INTJ | 建筑师 | I | N | T | J |
| ISTP | 鉴赏家 | I | S | T | P |
| ISFP | 探险家 | I | S | F | P |
| INFP | 调停者 | I | N | F | P |
| INTP | 逻辑学家 | I | N | T | P |
| ESTP | 企业家 | E | S | T | P |
| ESFP | 表演者 | E | S | F | P |
| ENFP | 竞选者 | E | N | F | P |
| ENTP | 辩论家 | E | N | T | P |
| ESTJ | 经理 | E | S | T | J |
| ESFJ | 执政官 | E | S | F | J |
| ENFJ | 主人公 | E | N | F | J |
| ENTJ | 指挥官 | E | N | T | J |

---

## 4. Question Distribution

### Version 1: Quick (70 questions)
- E/I: 17 questions
- S/N: 18 questions
- T/F: 18 questions
- J/P: 17 questions

### Version 2: Standard (93 questions)
- E/I: 23 questions
- S/N: 23 questions
- T/F: 24 questions
- J/P: 23 questions

### Version 3: Extended (144 questions)
- E/I: 36 questions
- S/N: 36 questions
- T/F: 36 questions
- J/P: 36 questions

### Version 4: Professional (200 questions)
- E/I: 50 questions
- S/N: 50 questions
- T/F: 50 questions
- J/P: 50 questions

---

## 5. Question Format

Each question includes:
- Scenario description
- Two forced choices (A and B)
- Clear wording
- No double negatives

Example:
```
问题 1/93

在社交聚会中，你通常是：

A) 和很多人热烈交谈，从不同的人那里获得能量
B) 只和一两个熟悉的人深聊，独处时更自在

请输入 A 或 B
```

---

## 6. Scoring Algorithm

### Step 1: Count Preferences
```
for each dimension:
    A_count = number of A answers
    B_count = number of B answers
```

### Step 2: Calculate Index
```
index = (A_count / total) × 100
```

### Step 3: Determine Type
```
type = 
    (E_index > 50 ? E : I) +
    (S_index > 50 ? S : N) +
    (T_index > 50 ? T : F) +
    (J_index > 50 ? J : P)
```

### Step 4: Calculate Clarity
```
clarity = |index - 50| × 2  (0-100%)
```

### Clarity Levels
- 0-25%: Slight preference
- 26-50%: Moderate preference
- 51-75%: Clear preference
- 76-100%: Very clear preference

---

## 7. Report Structure

### Section 1: Your Type
- 4-letter type (e.g., INFP)
- Type name (e.g., 调停者)
- Overall clarity percentage
- Brief summary (100 words)

### Section 2: Dimension Breakdown
For each dimension:
- Your preference
- Score (0-100 for each side)
- Clarity level
- Interpretation (50 words)

### Section 3: Personality Profile
- Strengths (5 items)
- Weaknesses (5 items)
- How others perceive you
- Communication style
- Ideal work environment

### Section 4: Relationships
- Compatible types (top 3)
- Challenging types (top 3)
- Relationship tips
- Communication strategies

### Section 5: Career Guide
- Best matching careers (5)
- Work style
- Leadership approach
- Stress responses
- Growth recommendations

### Section 6: Deep Analysis
- Decision-making pattern
- Information processing style
- Energy management
- Personal development plan

---

## 8. Interaction Flow

### Start
```
用户: MBTI测试
助手: "欢迎来到MBTI人格测试！🏠

请选择测试版本：
1. 快速版 (70题 ~10分钟)
2. 标准版 (93题 ~15分钟)
3. 扩展版 (144题 ~25分钟)
4. 专业版 (200题 ~35分钟)

输入数字选择版本。"
```

### Question Flow
```
助手: "问题 1/93

[题目内容]

A) [选项A]
B) [选项B]

请输入 A 或 B"

用户: A
助手: ✓ 已记录

(每10题显示进度: "进度: 10/93 (11%)")
```

### Result
```
助手: "🎉 测试完成！

你的MBTI类型是: INFP (调停者)
清晰度: 78%

类型简介: [50字简介]

输入数字查看详情：
1. 维度分析
2. 性格特征
3. 人际关系
4. 职业发展
5. 完整报告"
```

---

## 9. Project Structure

```
mbti-skill/
├── SKILL.md              # Skill documentation
├── _meta.json           # Metadata
├── mbti.py              # Main entry point
├── lib/
│   ├── questions/       # Question banks
│   │   ├── v70.py      # 70 questions
│   │   ├── v93.py       # 93 questions
│   │   ├── v144.py      # 144 questions
│   │   └── v200.py      # 200 questions
│   ├── scorer.py        # Scoring algorithm
│   ├── types.py         # 16 types data
│   ├── reports.py       # Report generator
│   └── conversation.py   # Interaction logic
└── data/
    └── results/         # Stored results
```

---

## 10. Technical Requirements

- Python 3.8+
- JSON data storage
- Conversation state management
- Markdown report generation

---

## 11. Version Features

### Quick (70)
- Fast completion
- Good accuracy
- Entry-level testing

### Standard (93)
- Official MBTI Form M equivalent
- Balanced depth
- Most popular

### Extended (144)
- Higher accuracy
- More nuanced results
- For serious users

### Professional (200)
- Maximum accuracy
- Clinical-level
- Comprehensive analysis
