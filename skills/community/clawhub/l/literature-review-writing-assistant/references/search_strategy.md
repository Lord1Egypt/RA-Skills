# 搜索策略指南（基于 Hempel Chapter 3）

## 1. PICO 框架

### 定义
PICO 是构建系统综述问题的框架：

| 元素 | 全称 | 说明 | 示例 |
|------|------|------|------|
| P | Population | 研究人群 | 高中生、大学生 |
| I | Intervention | 干预措施 | 动机访谈、认知行为疗法 |
| C | Comparator | 对照组 | 无干预、常规处理 |
| O | Outcome | 结局指标 | 学业成绩、心理健康 |

### 自然语言转换
```
P: 学生
I: 动机访谈
O: 学业成绩
↓
搜索词: "motivational interviewing" AND student* AND academic achievement
```

## 2. 布尔搜索

### 基本操作
```python
# AND: 同时包含两个词
"motivation interviewing" AND school

# OR: 包含任一词
depression OR anxiety OR mental health

# NOT: 排除词
animal NOT pet
```

### 优先级
```python
# 使用括号分组
("cognitive behavioral therapy" OR CBT) AND adolescent*
```

## 3. 通配符和截词

```python
# * 截词（任意后缀）
student* → student, students, student's

# ? 单字符替代
wom?n → woman, women
```

## 4. 邻近搜索

```python
# adjective 在名词前
behavior N/2 change

# 同一句中
"stress" ADJ3 "coping"
```

## 5. 索引词（MeSH）

### PubMed MeSH
```python
# 主要 MeSH
"Motor Activity"[Mesh]

# 限定词
"Depression"[Mesh] AND "Therapy"[Mesh:Subheading]
```

### 字段搜索
```python
# 标题中搜索
ti:intervention

# 摘要中搜索
ab:random*

# 关键词
kw:machine learning
```

## 6. 过滤器

### 研究类型
```python
# 随机对照试验
randomized controlled trial[pt]

# 综述
review[pt] AND systematic[sbbb]

# 元分析
meta-analysis[pt]
```

### 日期范围
```python
# 最近5年
"2019/01/01"[PDAT] : "2024/12/31"[PDAT]

# 特定年份
2024[dp]
```

### 物种
```python
# 只 Human
humans[mesh]

# 只 animals
animals[mesh]
```

## 7. 数据库特定语法

### PubMed
```python
# 简单搜索
"motivational interviewing"[Title/Abstract]

# MeSH 术语
"Motor Activity"[Mesh] AND "Adolescent"[Mesh]

# 组合
("Anxiety"[Mesh] OR "Anxiety Disorders"[Mesh]) 
AND ("Cognitive Therapy"[Mesh] OR "Behavior Therapy"[Mesh])
AND 2020:2024[dp]
```

### PsycINFO (OVID)
```python
# 关键词加字段
motivation interview*.tw

# MeSH
exp Motivational Interviewing/

# 组合
(exp Motivation/ OR exp Motivation Techniques/)
AND (exp Intervention/ OR exp Treatment/)
AND adolescent*.mp
```

### Web of Science
```python
# 主题搜索
TS=("motivational interviewing" AND school*)

# 复合查询
TS=(cognitive AND ("behavior therapy" OR CBT))
PY=2020-2024
```

## 8. 搜索策略开发流程

### 步骤
1. **确定核心概念** → 从 PICO 提取关键词
2. **列出同义词** → synonym, hyphenated, alternate spelling
3. **构建搜索块** → 每个概念单独的搜索
4. **组合** → 用 AND 连接搜索块
5. **测试** → 调整搜索词数量（目标：100-500 篇）
6. **记录** → 保存最终搜索策略

### 示例：动机访谈
```
核心概念1: motivation* interview*
  - "motivational interviewing"
  - "motivational interview"
  - MI

核心概念2: school*
  - school
  - schools
  - school*

核心概念3: adolescent*
  - adolescent
  - adolescents
  - teen
  - teenager
  - youth

搜索策略:
("motivational interviewing" OR "motivational interview" OR MI) 
AND (school OR schools) 
AND (adolescent OR teen OR teenager OR youth)
```

## 9. 搜索优化

### 结果太少？
- 移除 AND 连接的一个概念
- 改为 OR 连接同义词
- 放宽日期限制
- 移除 NOT 排除词

### 结果太多？
- 添加更多 AND 概念
- 缩小日期范围
- 添加强制性过滤器（human, English）
- 使用更具体的术语

## 10. 搜索策略记录模板

```markdown
## 搜索策略记录

### 日期
2024-XX-XX

### 数据库
PubMed, PsycINFO, Web of Science

### 搜索策略
| 数据库 | 搜索策略 | 结果数 |
|---------|----------|--------|
| PubMed | (1) AND (2) | XX |
| PsycINFO | ... | XX |

### 策略详情
- (1) = "motivational interviewing"[tiab] OR MI[tiab]
- (2) = adolescent*[tiab] OR teen*[tiab]

### 修改历史
- 初始搜索: 
- 修改1:
- 最终:
```