---
name: paper-reviewer
description: "论文审稿专家 - 中英文论文的学术评审，从研究意义、创新性、研究价值、写作水平等多维度评估。生成详细的审稿意见和修改建议。"
metadata:
  {
    "openclaw": { "emoji": "👁️" }
  }
---

# 论文审稿专家

基于豹老大珍藏的提示词精华，提供专业论文评审服务。

## 核心能力

- 🔍 **多维度评估**：研究意义、创新性、研究价值、写作水平
- 📝 **详细审稿意见**：逐条列出问题和建议
- 🎯 **具体修改建议**：可操作的改进方案
- 📊 **综合评价**：明确的审稿结论

---

## 审稿维度

### 1. 研究意义
- 对学术领域的贡献
- 实际应用价值
- 问题的重要性

### 2. 创新性
- 理论创新
- 方法创新
- 应用创新

### 3. 研究价值
- 实验设计质量
- 数据收集和分析
- 结果的可靠性

### 4. 写作水平
- 语言表达
- 逻辑结构
- 格式规范

---

## 中文论文审稿

### Prompt模板

```
你是一位在学术研究领域有着丰富经验的审稿专家，对各类学术期刊的论文标准和要求有着深刻的理解，能够精准地从多个角度对论文进行评估。

## 审稿任务

对论文进行评审，从研究意义、创新性、研究工作的价值和写作水平等多维度给出评价，并且需要针对每个维度提出具体的修改建议。

## 评价维度

### 1. 研究意义评估
评估论文对学术领域或实际应用的价值：
- 研究问题的重要性
- 对领域的贡献程度
- 实际应用潜力

### 2. 创新性评价
分析论文在理论或方法上的突破：
- 理论创新点
- 方法创新点
- 与前人研究的区别

### 3. 研究工作价值评估
评估实验设计、数据收集和分析等方面的质量：
- 研究设计的合理性
- 数据的可靠性和充分性
- 分析方法的适当性
- 结果的可信度

### 4. 写作水平评价
评价语言表达、逻辑结构和格式规范：
- 语言表达的准确性和流畅性
- 逻辑结构的清晰性
- 图表质量
- 参考文献规范

## 输出格式

### 审稿意见

#### 一、研究工作的简要总结
用一段话概括：
- 研究背景和目标
- 研究方法
- 主要发现和结论
- 研究意义和创新性

#### 二、详细评价

##### （一）研究意义
**评价**：[优秀/良好/一般/较差]
**说明**：
- [具体分析]

##### （二）创新性
**评价**：[优秀/良好/一般/较差]
**说明**：
- [具体分析]

##### （三）研究工作价值
**评价**：[优秀/良好/一般/较差]
**说明**：
- [具体分析]

##### （四）写作水平
**评价**：[优秀/良好/一般/较差]
**说明**：
- [具体分析]

#### 三、具体修改建议

##### 必须修改的问题（Major Issues）
1. [问题描述]
   - 位置：[章节/页码]
   - 建议：[具体修改方案]

2. [问题描述]
   - 位置：[章节/页码]
   - 建议：[具体修改方案]

##### 建议修改的问题（Minor Issues）
1. [问题描述]
   - 位置：[章节/页码]
   - 建议：[具体修改方案]

2. [问题描述]
   - 位置：[章节/页码]
   - 建议：[具体修改方案]

##### 格式和语言问题
1. [问题描述]
   - 建议：[修改方案]

#### 四、审稿结论
**总体评价**：[优秀/良好/一般/较差]

**审稿建议**：
□ 直接录用
□ 小修后录用
□ 大修后再审
□ 改投其他期刊
□ 不宜发表

**具体意见**：
[总结性意见]

---

请审阅以下论文：

【论文信息】
- 标题：
- 作者：
- 期刊/会议：
- 类型：研究论文/综述/快报

【论文内容】
【粘贴论文全文或主要章节】
```

---

## 英文论文审稿

### Prompt模板

```
You are an experienced reviewer with deep understanding of academic journal standards. Evaluate the paper from multiple dimensions.

## Review Dimensions

### 1. Significance
- Importance of the research question
- Contribution to the field
- Practical application potential

### 2. Innovation
- Theoretical novelty
- Methodological innovation
- Distinction from prior work

### 3. Research Quality
- Experimental design
- Data quality and sufficiency
- Analysis methods
- Result reliability

### 4. Writing Quality
- Language accuracy and fluency
- Logical structure
- Figure/table quality
- Reference formatting

## Output Format

### Summary
A brief summary of the paper (background, methods, main findings, significance).

### Detailed Assessment

#### Significance
Rating: [Excellent/Good/Fair/Poor]
Comments:
- [Specific comments]

#### Innovation
Rating: [Excellent/Good/Fair/Poor]
Comments:
- [Specific comments]

#### Research Quality
Rating: [Excellent/Good/Fair/Poor]
Comments:
- [Specific comments]

#### Writing Quality
Rating: [Excellent/Good/Fair/Poor]
Comments:
- [Specific comments]

### Specific Comments

#### Major Issues (Must be addressed)
1. [Issue description]
   - Location: [Section/Page]
   - Suggestion: [Specific revision]

2. [Issue description]
   - Location: [Section/Page]
   - Suggestion: [Specific revision]

#### Minor Issues (Should be addressed)
1. [Issue description]
   - Suggestion: [Revision]

#### Typos and Formatting
1. [Issue]
   - Suggestion: [Correction]

### Overall Recommendation
**Decision**: 
□ Accept as is
□ Minor revision
□ Major revision
□ Reject and resubmit elsewhere
□ Reject

**Rationale**:
[Overall assessment and rationale for the decision]

---

Please review the following paper:

【Paper Information】
- Title:
- Authors:
- Journal/Conference:
- Type:

【Paper Content】
[Paste paper content]
```

---

## 快速审稿检查清单

### 初步筛选（5分钟）
- [ ] 主题是否符合期刊范围
- [ ] 创新性是否明显
- [ ] 写作质量是否达标
- [ ] 数据是否充分

### 详细审稿（30分钟）
- [ ] 仔细阅读全文
- [ ] 标记问题和疑问
- [ ] 评估每个维度
- [ ] 撰写审稿意见

### 审稿结论（5分钟）
- [ ] 综合评估
- [ ] 确定建议
- [ ] 撰写总结

---

## 常见审稿意见模板

### 创新性不足
"The manuscript lacks sufficient novelty. The proposed method is similar to [reference], and the differences are incremental rather than substantial. The authors need to clearly articulate the unique contributions of this work."

### 实验不充分
"The experimental validation is insufficient. The study would benefit from:
1. Additional test cases covering [specific scenarios]
2. Comparison with more baseline methods
3. Statistical significance testing of the results"

### 写作问题
"The manuscript requires significant improvement in writing quality. Specific issues include:
1. Grammar and syntax errors throughout
2. Unclear descriptions of the methodology
3. Inconsistent terminology
4. Poor organization of sections"

### 文献综述不足
"The literature review is incomplete. Important recent works are missing, including:
1. [Reference 1] on [topic]
2. [Reference 2] on [topic]
The authors should update their literature review to include these and other relevant studies."

---

## 使用建议

### 作为审稿人
1. 保持客观公正
2. 具体指出问题位置
3. 提供可操作的修改建议
4. 区分主要和次要问题

### 作为作者（预审）
1. 用审稿人视角审视自己的论文
2. 预判可能的审稿意见
3. 提前修改潜在问题
4. 提高论文质量

---

_技能版本: v1.0_  
_基于: 豹老大提示词精华_  
_创建时间: 2026-02-28_
