# 语言工具箱（Verb Tenses, Linking Phrases, Contribution Markers）

## 一、动词时态选择指南

### 1.1 领域重要性 / "Recent attention"

| 情景 | 推荐时态 | 示例 |
|---|---|---|
| 强调"近年来 / in recent years / over the past decade" | **Present Perfect** | Much study in recent years **has focused on**... |
| 强调"目前 / currently / today" | **Present Simple** | There **are** substantial benefits to... |
| 强调具体年份（一次性事件） | **Past Simple** | In 2019, a study **revealed**... |
| 希望论文在 5 年后仍然相关 | 用**具体时间点**（since 2018）而非 recent years |

### 1.2 背景事实（已被广泛接受）

时态：**Present Simple**（陈述事实）

- Biomass-derived PLA **is produced** from renewable feedstocks such as corn and sugar cane.
- Hematite **has** a variety of applications including pigments, gas sensors, and catalysts.
- SVMs **are** among the most popular general-purpose learning methods in use today.

**演化规律**（从研究发现到事实）：

```
阶段 1（新发现）：Lawrence et al. have found that X can be obtained from Y.          [Present Perfect]
阶段 2（较新）：Lawrence et al. (2000) found that X can be obtained from Y.          [Past Simple]
阶段 3（普遍）：X is produced from Y (Lawrence et al., 2000).                         [Present Simple + citation]
阶段 4（事实）：X is produced from Y.                                                  [Present Simple, no citation]
```

### 1.3 前人研究综述

| 情景 | 推荐时态 | 示例 |
|---|---|---|
| 描述单个研究 / 作者做了什么 | **Past Simple** | Penney et al. (2012) **showed** that... |
| 研究贡献的持续效应 | **Present Perfect** | Several authors **have proposed** that... |
| 一般化结论 / 现在被认为... | **Present Simple** | It **is believed** that triboemission **initiates**... |
| 对比多项研究 | 混合时态 | Early work **assumed**...; more recently, however, studies **have shown**... |

### 1.4 Gap / Problem 陈述

| 情景 | 推荐时态 | 示例 |
|---|---|---|
| "很少有人关注 / little attention has been paid to" | **Present Perfect** | Little attention **has been paid to** the selection of... |
| "仍不清楚 / it remains unclear" | **Present Simple** | It **is** not clear how these effects... |
| "尚未被完全理解 / is not fully understood" | **Present Simple (passive)** | The mechanisms... **are** as yet poorly understood. |
| "很少有研究 / few studies have" | **Present Perfect** | Few studies **have simultaneously recorded**... |

### 1.5 本文（present paper）描述

| 情景 | 推荐时态 | 示例 |
|---|---|---|
| 描述本文做了什么（静态） | **Present Simple** | This paper **presents**... / This study **focuses on**... |
| 描述研究的目标（已完成的研究） | **Past Simple** | The aim of this project **was** to... |
| 研究正在进行/目标未完全达到 | **Present Simple** | The aim of this study **is**... |
| 报告本文方法/结果 | **Past Simple** | We **obtained** simultaneous recordings... / We **find** that... |
| 描述论文组织（CS/工程常用） | **Present Simple** | The remainder of this paper **is organized** as follows... |

### 1.6 贡献标记词（Contribution Markers）

通常嵌入 Past Simple 或 Present Simple，取决于是结果还是一般陈述。贡献词的强度必须与用户提供的数据、引用或实验结果匹配：
- This combination **formed** a **lightweight** copolymer in which X **increased** Y while retaining Z. [Past Simple + calibrated contribution marker]
- Our implementation **is** orders of magnitude **faster** than existing CPU implementations. [Present Simple + strong marker; requires benchmark support]

---

## 二、Linking Phrases（连接前人研究的短语）

### 2.1 引入前人研究的短语

```
[ref] also observed that…
[ref] resolved this by…
[ref] were the first to…
A pioneering study by [ref] demonstrated…
A similar approach was used by [ref], who…
An alternative approach was proposed by [ref], who…
According to [ref], it is highly likely that…
Importantly, [ref] noted that…
In order to resolve this, [ref] analysed/developed...
In that study, although…
In their recent work, [ref] has suggested that…
It was later shown by [ref] that…
One [potential] implication of [ref]'s results is that…
Other studies have focused on…, for example, [ref] and [ref] attempted to…
Recently, it has been shown/suggested that…
Soon after, [ref] proposed…
Subsequently,…
Taken together, these studies suggest that…
The most systematic review is that in/of [ref]…
These findings challenge the work of [ref], who…
This approach was further developed by [ref], who…
This methodology was adapted by…
To address this issue, [ref]…
To overcome these problems, a different approach was used by/in [ref].
Within five years, [ref] developed a…
```

### 2.2 Reporting Verbs（描述前人做了什么）

- **发现/观察类**：observed, found, showed, revealed, demonstrated, identified, confirmed
- **提出类**：proposed, suggested, introduced, put forward, advocated
- **分析类**：analyzed, examined, investigated, studied, explored, evaluated
- **开发类**：developed, designed, constructed, implemented, created
- **证明类**：established, proved, verified, validated
- **争论类**：argued, contended, maintained, claimed
- **综述类**：reviewed, summarized, discussed

### 2.3 Gap 信号词

| 类别 | 短语 |
|---|---|
| 对比信号 | However, Although, Despite, Yet, Nevertheless, Nonetheless, In contrast, Unlike |
| 缺失信号 | Little is known about..., Few studies have..., Little attention has been paid to..., There is a paucity of... |
| 不足信号 | remain(s) unclear, is not fully understood, has not been systematically investigated, has been limited |
| 局限信号 | suffer from, is limited by, is restricted to, is constrained by, falls short of |
| 矛盾信号 | discrepancy, inconsistency, contradicts, conflicts with |
| 机会信号 | offers an opportunity, provides a pathway, opens the possibility, could enable |

### 2.4 本文引入 / Motivation 短语

```
To address this issue / gap / question, we...
To overcome this limitation, we...
To fill this gap, we propose...
To resolve this, we...
Motivated by this, we...
Building on this work, we...
In this paper / study, we...
The present paper / study presents / reports / describes...
Here, we...
This work aims to...
The objective of this study is / was to...
We propose a new approach that...
```

### 2.5 结果预告短语（贡献标记锚定）

```
Our results reveal...
We find that...
Our findings suggest that...
This approach / method / system achieves...
The proposed method outperforms...
To our knowledge, this is the first demonstration of...
Overall, our implementation is orders of magnitude faster than...
This work offers a...
```

---

## 三、贡献标记词库

按使用位置分类：

### 3.1 描述贡献/创新
- novel, new, original, innovative, first (demonstration of)
- unique, unprecedented, pioneering

使用规则：`first / novel / unprecedented / state-of-the-art / best-in-class` 属于强断言，只有在用户材料、真实引用或明确基准结果支持时使用；信息不足时改用 `new, proposed, systematic, practical, evaluates, provides` 等稳健表达。

### 3.2 描述性能/效果
- efficient, effective, high-performance, robust, reliable, accurate
- powerful, scalable, flexible, versatile, lightweight, compact
- fast, rapid, real-time, scalable

### 3.3 描述改进程度
- significant(ly), substantial(ly), considerable, remarkable, notable
- substantial improvement, marked enhancement, dramatic reduction
- orders of magnitude, several-fold

### 3.4 描述通用性/广泛性
- general, universal, broadly applicable, widely applicable
- comprehensive, thorough, systematic

### 3.5 描述优越性（谨慎使用）
- superior, outperforms, surpasses, exceeds, better than
- state-of-the-art, best-in-class

### 3.6 常见组合
- "a new [X] that achieves [Y]"
- "significantly improves [X] while retaining [Y]"
- "to our knowledge, this is the first [X]"
- "orders of magnitude faster than existing methods"
- "a substantial improvement over [X]"

---

## 四、Passive vs. Active 选择

| 情景 | 推荐 | 示例 |
|---|---|---|
| 突出作者团队 | Active | We obtained simultaneous recordings... |
| 突出方法/过程 | Passive | Simultaneous recordings were obtained... |
| 生科/医学领域 | 多用 Passive | Samples were analysed using SIMS... |
| CS/工程领域 | 常用 Active "we" | In this paper we discuss how... |
| 避免主语重复 | 灵活切换 | — |

**默认建议**：CS、工程、物理更自由用 "we"；化学、生科、医学传统上多用被动语态。查目标期刊风格。

---

## 五、引用位置决策

| 位置 | 何时使用 |
|---|---|
| 句末 | 引文支持整句内容 |
| 句中 | 引文只支持句子的某一部分，需明确区分 |
| 句首（如 Penney et al. (2012) showed...） | 强调作者，或把作者作为主题 |

**误区**：不要把多个无关文献堆在句末——会让读者误以为整句都来自这些文献。

---

## 六、常见句首开场（按组件）

### 组件 1 开场
- [Topic] has received much attention in recent years due to...
- [Topic] is widely used in / for / as...
- Considerable / Much effort has been devoted to...
- There is considerable / growing interest in...
- [Topic] plays a major role / critical role / key role in...

### 组件 2 开场（进入综述）
- Numerous studies have examined...
- Several approaches have been proposed to...
- Previous research has focused on...
- Early work by [ref] established that...

### 组件 3 开场（gap）
- However, these approaches / methods / studies...
- Although considerable efforts have been focused on..., [gap]
- Despite this progress, [gap]
- Yet, little is known about...

### 组件 4 开场（本文）
- In this paper / study, we...
- The present paper reports...
- Here, we present / propose / describe...
- To address this [gap/issue], we...
- This work aims to...
