# Candidate Classifier (候选人分类器)

本文档定义了候选人类型分类规则，用于根据候选人的个人信息判断其职业身份（PhD 学生、博士后、教授、工业界等）。

## 候选人类型

| 类型 | 英文标识 | 说明 | 典型特征 |
|-----|---------|------|---------|
| PhD 学生 | `PhD` | 博士研究生 | "PhD student", "PhD candidate", "博士生" |
| 博士后 | `PostDoc` | 博士后研究员 | "Postdoc", "Post-doctoral", "博士后" |
| 教授 | `Professor` | 教授/研究员 | "Professor", "Associate Professor", "教授" |
| 工业界 | `Industry` | 企业研究人员/工程师 | "Engineer", "Research Scientist at [公司]" |
| 硕士生 | `Master` | 硕士研究生 | "Master student", "硕士生" |
| 未知 | `Unknown` | 无法确定 | 缺少身份信息 |

---

## 分类关键词

### PhD 学生关键词

```
英文:
phd student, phd candidate, doctoral student, graduate student, graduate researcher
ph.d. student, doctor of philosophy

中文:
博士生, 博士研究生, 博士生在读, 攻读博士, 博士候选
```

### 博士后关键词

```
英文:
postdoc, post-doc, postdoctoral, post-doctoral
postdoctoral researcher, postdoctoral fellow
research associate (academic context)

中文:
博士后, 博士后研究员, 博后
```

### 教授关键词

```
英文:
professor, prof., associate professor, assistant professor
full professor, tenured, tenure-track, faculty, lecturer
principal investigator, pi, group leader

中文:
教授, 副教授, 助理教授, 讲师, 研究员
博导, 博士生导师, 实验室主任, 课题组长
```

### 工业界关键词

```
英文:
engineer, developer, scientist, researcher at [company]
staff, principal, senior, lead, manager, director
software engineer, research scientist, ml engineer, data scientist

中文:
工程师, 算法工程师, 研发, 技术专家
研究员(企业), 科学家(企业)
```

---

## 分类逻辑

### 优先级顺序

按以下优先级判断（优先匹配更具体的身份）：

```
PhD > PostDoc > Professor > Industry > Master > Unknown
```

### 分类算法

```python
def classify_candidate(candidate: dict) -> str:
    """
    根据候选人信息推断其类型

    Args:
        candidate: 候选人档案，包含 name, headline, summary, experience 等字段

    Returns:
        候选人类型: "PhD", "PostDoc", "Professor", "Industry", "Master", "Unknown"
    """
    # 收集所有可能包含身份信息的文本
    text_sources = [
        candidate.get("headline", ""),
        candidate.get("summary", ""),
        " ".join(candidate.get("experience", [])),
        " ".join(candidate.get("education", []))
    ]
    combined_text = " ".join(text_sources).lower()

    # 按优先级检查

    # 1. PhD 学生 (优先)
    if contains_any(combined_text, PHD_KEYWORDS):
        # 排除已毕业情况
        if not contains_any(combined_text, ["ph.d.", "doctor of philosophy", "博士学位"]):
            return "PhD"

    # 2. 博士后
    if contains_any(combined_text, POSTDOC_KEYWORDS):
        return "PostDoc"

    # 3. 教授
    if contains_any(combined_text, PROFESSOR_KEYWORDS):
        return "Professor"

    # 4. 工业界
    if contains_any(combined_text, INDUSTRY_KEYWORDS):
        # 进一步确认是企业而非学术机构
        if contains_any(combined_text, COMPANY_INDICATORS):
            return "Industry"
        if not contains_any(combined_text, ACADEMIC_INDICATORS):
            return "Industry"

    # 5. 硕士生
    if contains_any(combined_text, MASTER_KEYWORDS):
        return "Master"

    return "Unknown"
```

---

## 学术 vs 企业判断

### 学术机构标识

```
university, college, institute, lab, research group
大学, 学院, 研究所, 实验室
```

### 企业标识

```
inc, corp, company, ltd, llc, technologies, tech
google, meta, microsoft, amazon, apple, nvidia
bytedance, tencent, alibaba, baidu, huawei
openai, anthropic, deepmind
```

### 判断规则

```
if (职位关键词 in [engineer, scientist] and 企业标识 in 文本):
    return "Industry"
elif (职位关键词 in [professor, phd] and 学术机构标识 in 文本):
    return "Academic"  # 进一步细化为 Professor/PhD
```

---

## 分类示例

### 示例 1: PhD 学生

```
姓名: Wei Zhang
Headline: PhD Student at Tsinghua University
Summary: Researching Reinforcement Learning

分类结果: PhD
依据: "PhD Student" 明确标识
```

### 示例 2: 博士后

```
姓名: Li Wang
Headline: Postdoctoral Researcher at Stanford AI Lab
Summary: Working on Multimodal Learning

分类结果: PostDoc
依据: "Postdoctoral Researcher" 明确标识
```

### 示例 3: 教授

```
姓名: Ming Chen
Headline: Associate Professor at Peking University
Summary: Director of NLP Lab

分类结果: Professor
依据: "Associate Professor" + "Lab" (学术机构)
```

### 示例 4: 工业界

```
姓名: Hao Liu
Headline: Senior Research Scientist at Google DeepMind
Summary: Working on Large Language Models

分类结果: Industry
依据: "Google DeepMind" (企业) + "Research Scientist"
```

### 示例 5: 未知 (需要更多信息)

```
姓名: Xin Li
Headline: Software Engineer
Summary: Interested in AI

分类结果: Unknown (或 Industry after inference)
依据: "Software Engineer" 通常属于 Industry，但缺少明确机构信息
建议: 进一步查看 experience 或 education 字段
```

---

## 特殊情况处理

### 情况 1: PhD 已毕业

```
Headline: "PhD in Computer Science from Stanford"
Education: "Ph.D., Stanford University, 2023"

处理: 这是已毕业的 PhD，当前身份需要根据 experience 判断
- 如果是 "Postdoc at MIT" → PostDoc
- 如果是 "Professor at CMU" → Professor
- 如果是 "Research Scientist at Google" → Industry
```

### 情况 2: 兼职身份

```
Headline: "PhD Student | Research Intern at Google"

处理: 主要身份是 PhD，Industry 是实习/兼职
分类结果: PhD
```

### 情况 3: 企业研究员但有学术头衔

```
Headline: "Principal Scientist at OpenAI | Adjunct Professor at Stanford"

处理: 主要身份在企业
分类结果: Industry
```

---

## 批量分类

```python
def classify_all(candidates: list) -> list:
    """
    对所有候选人进行类型分类

    Args:
        candidates: 候选人列表

    Returns:
        添加了 candidate_type 字段的候选人列表
    """
    classifier = CandidateClassifier()
    results = []

    for candidate in candidates:
        # 如果已有类型且不是 Unknown，保持不变
        if candidate.get("candidate_type", "Unknown") != "Unknown":
            results.append(candidate)
        else:
            # 分类并更新
            candidate_type = classifier.classify(candidate)
            candidate["candidate_type"] = candidate_type
            results.append(candidate)

    return results
```

---

## 分类过滤器

### 只保留 PhD 学生

```python
def filter_phd_only(candidates: list) -> list:
    """只保留 PhD 学生"""
    return [c for c in candidates if c.get("candidate_type") == "PhD"]
```

### 保留 PhD 和博士后

```python
def filter_phd_and_postdoc(candidates: list) -> list:
    """保留 PhD 和 PostDoc"""
    return [c for c in candidates if c.get("candidate_type") in ["PhD", "PostDoc"]]
```

### 排除教授

```python
def exclude_professors(candidates: list) -> list:
    """排除教授"""
    return [c for c in candidates if c.get("candidate_type") != "Professor"]
```

### 只保留学术界

```python
def filter_academic_only(candidates: list) -> list:
    """只保留学术界（PhD、PostDoc、Professor）"""
    academic_types = ["PhD", "PostDoc", "Professor"]
    return [c for c in candidates if c.get("candidate_type") in academic_types]
```

---

## 分类准确率提升建议

1. **多字段综合判断**: 不要仅依赖 headline，同时检查 summary、experience、education
2. **机构优先**: 有明确机构名称时，机构类型（高校 vs 企业）权重更高
3. **人工审核**: 对于 "Unknown" 类型的候选人，建议人工审核
4. **持续更新**: 定期更新关键词列表，适应新的表达方式
5. **上下文理解**: 使用 LLM 进行语义理解，提高分类准确率
