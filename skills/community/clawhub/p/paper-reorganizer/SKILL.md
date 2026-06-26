---
name: paper-reorganizer
description: >
  This skill should be used when the user wants to reorganize and deepen a journal paper based on
  given requirements. It guides WorkBuddy through a structured six-phase workflow: (1) parsing the
  paper and extracting the core thesis, (2) extracting and rebuilding the outline, (3) reviewing
  and critiquing the outline, (4) splitting the paper by chapters, (5) iteratively deepening each
  chapter through multi-round argumentation with Chinese and foreign literature support, and (6)
  integrating and performing a final consistency check. The skill enforces strict rules: each
  chapter must be deepened independently with repeated argumentation, must stay connected to the
  overall core thesis, must not go off-topic, and must not repeat content from other chapters.
  Literature search covers CNKI, Web of Science, Google Scholar and other databases. Trigger
  phrases include "整理论文大纲", "深化论文章节", "重新归纳期刊论文", "对论文进行分章深化",
  "帮我整理这篇论文", "按大纲深化论文", "搜集文献".
---

# Paper Reorganizer — 期刊论文重组深化工作流

## 概述

本技能针对期刊论文提供系统性重组与深化服务，分七个阶段顺序执行，全程遵守"聚焦本章、反复论证、联系核心要义、不跑题、不重复"五大铁律。

---

## 使用前提

用户需提供以下内容之一：
- 论文全文（粘贴文本）
- 论文主要内容摘要（如提供部分内容，标明来源章节）
- 明确的改写需求（例如：调整结构重点、补充某章论据）

---

## 七阶段工作流

### Phase 1 — 论文解析与核心命题提炼

读取用户提供的论文内容，完成以下任务：

1. 识别**核心研究问题**（一句话）
2. 识别**研究方法**（简要）
3. 识别**主要结论**（简要）
4. 提炼**全文核心命题**（一句话，用于后续深化阶段的锚点）

> 参考：`references/workflow_prompts.md` → Phase 1 提示词模板

输出后询问用户是否确认核心命题，若有偏差则修正后继续。

---

### Phase 2 — 大纲提取与重组

基于论文内容，提取并**重新整理**大纲：

- 大纲层级不超过三级（章 > 节 > 小节）
- 遵循学术论文规范结构：摘要 / 引言 / 文献综述 / 方法 / 结果 / 讨论 / 结论
- 每个标题后附一句话说明该部分的**核心功能**

> 参考：`references/workflow_prompts.md` → Phase 2 提示词模板

---

### Phase 3 — 大纲评审与改进意见

对重组后的大纲进行批判性评审，从以下维度提出具体意见：

| 评审维度 | 要点 |
|----------|------|
| 结构合理性 | 层级是否清晰，比例是否均衡 |
| 逻辑一致性 | 各章是否服务于核心命题，衔接是否自然 |
| 学术规范性 | 是否符合期刊论文写作规范 |
| 创新性体现 | 研究贡献在大纲中是否充分展示 |

> 详细评审标准见：`references/outline_criteria.md` → 第一节"大纲质量评审维度"

评审后给出**建议修订大纲**，等待用户确认后进入下一阶段。

---

### Phase 4 — 章节分割

根据用户确认的大纲，将论文原文**按章节拆分为独立处理单元**：

- 以一级标题（章）为基本分割单位
- 若某章超过 1500 字，按二级标题进一步细分
- 为每个单元标注：编号、标题、字数估算、章节功能

输出分割清单，等待用户确认后进入深化阶段。

> 参考：`references/workflow_prompts.md` → Phase 4 提示词模板

---

### Phase 5 — 分章节逐步深化（循环执行）

**按章节顺序逐一深化**，每次只处理一个章节，完成后询问用户是否继续下一章节。

#### 深化前必须确认

- 全文核心命题（来自 Phase 1）
- 本章在大纲中的功能（来自 Phase 2/3）
- 本章当前内容的要点摘要

#### 四大铁律（每章深化严格遵守）

1. **聚焦本章、反复论证**  
   将注意力完全集中于本章标题范畴内，通过多轮迭代深化本章内容：  
   - 第一轮：梳理本章现有论点，识别论证缺口  
   - 第二轮：针对每个缺口，搜集中外文献（CNKI、Web of Science、Google Scholar 等）进行理论支撑  
   - 第三轮：整合文献与本章论点，反复论证、层层递进  
   - 第四轮：凝练总结，形成闭环  
   - **禁止引入其他章节的具体论点或结论**，本章独立完成深化。

2. **联系全文核心命题**  
   本章每个核心论点须与 Phase 1 提炼的全文核心命题建立显式联系。  
   段末可用过渡句点明本章与整体论证的关系。

3. **不跑题**  
   所有内容须在本章标题范畴内。举例、引用文献须与本章主题直接相关。  
   若引入背景信息，需简短且标注"仅作背景"。

4. **不重复**  
   同一论点、数据、案例在全文只出现一次。  
   若本章需引用已在其他章节论证过的内容，用"如前所述"简短带过，不重复展开。  
   换词重述（paraphrase 重复）也视为重复，须替换为新的论证角度。

#### 文献搜集与理论支撑

在 Phase 5 深化过程中，针对本章核心论点进行**中外文献搜集**：

- **中文文献**：CNKI（中国知网）、万方、维普等
- **外文文献**：Web of Science、Scopus、Google Scholar、PubMed、arXiv 等
- 优先选取与本章主题高度相关的**近 5 年高质量期刊论文**和**经典文献**
- 文献用于：
  - 提供理论依据和实证支持
  - 引用前人研究方法和结论作为参照
  - 对比分析，说明本研究与既有文献的关系
- 引用格式符合目标期刊要求（APA、GB/T 7714 等）

#### 深化后自查清单

深化完成后，必须逐项自查并在输出中附自查报告：

```
□ 跑题检查：本章所有内容在标题范畴内
□ 重复检查：无与其他章节重复的论点或数据
□ 命题联系：核心命题已在本章明确呼应
□ 过渡检查：段落间过渡自然
□ 语言规范：符合学术写作规范
```

> 详细规范见：`references/outline_criteria.md` → 第二节"章节深化规范"  
> 操作提示：`references/workflow_prompts.md` → Phase 5 提示词模板

---

### Phase 6 — 全文整合与一致性检查

所有章节深化完毕后，进行全文整合与最终检查：

1. **论点一致性**：全文核心命题是否贯穿始终
2. **重复内容扫描**：标记重复出现的论点、数据、案例及其位置
3. **章节衔接检查**：相邻章节过渡是否自然
4. **摘要与结论一致性**：摘要中的结论与结论章节是否匹配
5. **引言与结论呼应**：引言中的研究 Gap 是否在结论中得到回应

输出整合检查报告及建议修订项。

> 参考：`references/workflow_prompts.md` → Phase 6 提示词模板

---

### Phase 7 — 章节合并与 Word 输出

所有章节深化完成并通过一致性检查后，将各章内容**按大纲顺序合并**为完整论文，并输出为 **Word 文档（.docx）**。

#### 合并流程

1. **检查各章状态**：确认所有章节已完成深化并通过自查
2. **按大纲排序**：依据 Phase 2/3 确认后的大纲，依次排列各章
3. **添加必要元素**：
   - 论文标题
   - 摘要（如需更新）
   - 关键词
   - 作者信息（根据用户提供）
   - 参考文献（统一格式）
4. **格式排版**：
   - 标题层级清晰（一级/二级/三级）
   - 段落格式规范（首行缩进、行距）
   - 图表编号（如有）
   - 页眉页脚（如需要）

#### Word 输出规范

- 文件格式：`.docx`（Microsoft Word 2007 及以上）
- 编码：UTF-8
- 页面设置：A4 纸，上下页边距 2.54cm，左右页边距 3.17cm
- 字体：中文宋体，英文 Times New Roman
- 标题字号：一级标题 16pt 加粗，二级标题 14pt 加粗，三级标题 12pt 加粗
- 正文字号：小四（12pt），行距 1.5 倍
- 引用格式：符合目标期刊要求（APA 或 GB/T 7714）

#### 输出交付

- 询问用户目标期刊的引用格式要求
- 生成 `.docx` 文件后，使用 `open_result_view` 工具向用户展示
- 如用户有其他格式要求（如 LaTeX、PDF），可额外支持

> 使用 `docx` skill 生成 Word 文档

---

## 交互规范

- **每个阶段结束后暂停**，向用户展示输出，确认是否继续下一阶段。
- 若用户在任意阶段要求修改，完成修改后重新确认，再继续。
- 若用户跳过某阶段，记录跳过并在后续阶段中补充必要上下文。
- 全程保持学术、专业的语言风格。

---

## 参考资源

| 文件 | 用途 |
|------|------|
| `references/outline_criteria.md` | 大纲评审标准与深化规范（Phase 3、5 核心参考） |
| `references/workflow_prompts.md` | 各阶段标准提示词模板（全流程使用） |
