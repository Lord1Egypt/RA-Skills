# 四组件模型与十一句式详解

## 一、Generic Introduction Model（四组件模型）

Glasman-Deal 通过逆向工程（reverse-engineering）大量已发表论文，归纳出研究论文引言的**通用四组件结构**。把它想象成一个**菜单**：并非每一项都必须用，但每个组件的功能都不能完全缺席。

### 组件 1 — 建立背景（wide end of the funnel）

三个可选子功能，至少用一到两个：

- **ESTABLISH THE IMPORTANCE OF THE TOPIC/FIELD**（确立主题/领域的重要性）
  - 典型句式：Much attention has been focused on... / X has received considerable interest in recent years... / X plays a major role in... / X is widely used in...
  - 时态：Present Perfect（"in recent years / over the past decade"）或 Present Simple（强调现状）
  - 避坑：不要用"since 1995"这种过于遥远的时间标记；建议使用"in recent years"或具体近期时间点。

- **PROVIDE BACKGROUND FACTUAL INFORMATION**（提供背景事实）
  - 典型句式：X is a Y that consists of Z... / X is produced from... / X has properties including...
  - 时态：Present Simple（已被接受的事实）
  - 提示：读者可能跨学科，宁可多提供一点背景，也不要过于简略。

- **PRESENT THE GENERAL PROBLEM AREA / CURRENT RESEARCH FOCUS**（引出一般问题或当前研究焦点）
  - 典型句式：However, its Y has significantly limited its use... / The main challenge facing this field is... / Recent research has focused on...
  - 此处的"问题"仍是**宽泛**的领域焦点，不是本文具体要解决的问题。

### 组件 2 — 研究地图（literature & contributions review）

功能：
- 综述前人与当前研究、贡献。
- 给读者一张"地图"，让他们看到本研究在该领域的坐标。
- 为组件 3 的 gap/问题做铺垫。

**组织模式**（三选一，或混合）：

1. **General-to-specific（最常见）**：先综述类总结/综述文章，逐步聚焦到最接近本文问题的研究。
2. **Different approaches/theories/models**：按方法/理论分组，避免 "tennis match effect"（来回反驳的疲惫感）。
3. **Chronological order**：按时间顺序，适合领域发展与政策/立法紧密相关的情形。

**选择文献的原则**：
- **Relevance is crucial**：每个被提及的研究都必须与本研究的动机直接相关。
- 不是 reading list，而是一条 **精心叙述的旅程**（carefully-narrated journey）。
- 叙述应该**通往本文的动机**。

### 组件 3 — 锁定空白（narrowing focus）

四个可选子功能：

- **LOCATE A GAP IN THE RESEARCH**（定位研究空白）
- **DESCRIBE THE PROBLEM YOU WILL ADDRESS**（描述本文要解决的具体问题）
- **PRESENT YOUR MOTIVATION AND/OR HYPOTHESIS**（提出动机/假设）
- **IDENTIFY A RESEARCH OPPORTUNITY**（指出研究机会）

**关键信号词**：
- However, Although, Despite, Yet, Nevertheless, Nonetheless
- little attention has been paid to..., few studies have..., it remains unclear..., it has yet to be...
- 以**prediction / suggestion / hypothesis** 形式陈述，避免问句。

**注意**：
- 有时 gap 不显式出现——可能是因为本文只是 extend previous research，或 gap 已隐含在本研究目的中。

### 组件 4 — 介绍本研究（narrow end of the funnel）

五个可选子功能（通常组合使用）：

- **DESCRIBE THE PRESENT PAPER**（描述本文）
  - This paper/study presents/proposes/reports...
  - In this paper we...
  - The aim of this study is/was to...

- **STATE THE AIM/PURPOSE**（陈述目的）
  - 时态：Present Simple（aim 仍未完成时）或 Past Simple（aim 已完成时）

- **OUTLINE THE METHOD**（简述方法——不过于详细）

- **(Optional) MENTION MAIN RESULT**（预告主要结果，通常伴随贡献标记词）

- **(Optional) GIVE THE STRUCTURE OF THE PAPER**（介绍论文组织——在 CS 和理科论文中常见，在生科论文中较少）

**贡献标记词（Contribution Markers）示例**：
new, systematic, efficient, robust, lightweight, accurate, reliable, scalable, flexible, versatile。`novel / first demonstration / significant / state-of-the-art` 等强表达只在用户材料或真实引用能支撑时使用。

---

## 二、十一句式详解（Sentence-by-Sentence Template）

把四组件再展开为句子级别的模板——**不是强制**，而是一把尺子，便于对照检查。以下基于 p1.txt 中 chitin-PLA 示例的逆向工程结果。

| # | 句子功能 | 对应组件 | 典型句式 | 时态 |
|---|---|---|---|---|
| S1 | establishes the importance of the research topic | 1 | X has received much attention in recent years due to... | Present Perfect |
| S2 | provides background factual information for the reader | 1 | X is produced from Y such as... | Present Simple |
| S3 | elaborates on S1/S2 with more detail + citations | 1 | X has outstanding properties for use in Z [ref]. | Present Simple |
| S4 | describes the general problem area / current research focus of the field | 1 | However, its Y has significantly limited its use. | Present Perfect |
| S5 | extends the problem area / current focus | 1 | Applications require materials with the lowest possible Y, so although Z has been used [ref], these are not appropriate for... [ref]. | mixed |
| S6 | links the general problem area to published research and refers to other studies | 2 | One way to address X is to incorporate Y [ref, ref, ref]. | Present Simple / Perfect |
| S7 | mentions a key research study in this area | 2 | For example, Penney et al. (2012) showed that... [ref]. | Past Simple（对 reporting verb）|
| S8 | identifies a problem or gap in the research | 3 | However, although the effect of X was demonstrated over two years ago [ref], Y adds considerably to Z, and little attention has been paid to... | Past Simple + Present Perfect |
| S9 | describes the present paper or study | 4 | The present paper presents a set of criteria for selecting such a component. | Present Simple |
| S10 | outlines the method reported in the paper | 4 | On the basis of these criteria, it then describes the preparation of... | Present Simple |
| S11 | announces the main result, using contribution markers | 4 | This combination formed a lightweight copolymer in which X increased Y while retaining Z. | Past Simple |

### 使用十一句式的注意事项

- **S1-S5 都属于组件 1**：可见组件 1 通常最长，铺垫最充分。
- **S6-S7 才进入组件 2**：只是示例数；复杂话题可能有 S6a, S6b, S7a, S7b 等。
- **S8 是过渡**：从 review 转入 gap，用 However / Although 显式标注。
- **S9-S11 都属于组件 4**：分别描述 paper / method / result。
- 并不需要严格 11 句——**长论文或综合性论文可能到 20-30 句**；短论文（letter）可能只有 8-12 句。

---

## 三、典型段落切分方案

实际论文中引言通常 2-5 段。常见切分方式：

### 方案 A（4 段式，最常见）
- 第 1 段 = 组件 1（importance + background + general focus）
- 第 2 段 = 组件 2（literature review）
- 第 3 段 = 组件 3（gap + problem + motivation）
- 第 4 段 = 组件 4（present paper + aim + method + result）

### 方案 B（3 段式，短论文）
- 第 1 段 = 组件 1（有时可带少量组件 2 前半）
- 第 2 段 = 组件 2 + 组件 3
- 第 3 段 = 组件 4
- §1.6 SPPPV / bicycle cover 练习是这一方案的典型短版本：第 1 段 4 句（C1），第 2 段 4 句（C2+C3），第 3 段 1 句（C4），总长约 250-350 words。

### 方案 C（5 段式，长论文或跨学科论文）
- 第 1 段 = 组件 1（importance + broadest background）
- 第 2 段 = 组件 1 细化（更专一的背景）
- 第 3 段 = 组件 2 第一部分（某一研究方向的综述）
- 第 4 段 = 组件 2 第二部分 + 组件 3（另一方向综述 + gap）
- 第 5 段 = 组件 4

### 方案 D（"问题驱动"变体，常见于工程/CS）
- 第 1 段 = 组件 1（importance + context）
- 第 2 段 = 组件 2（现有方法综述）
- 第 3 段 = 组件 3（现有方法的不足/gap）
- 第 4 段 = 组件 4（本文的方法 + 贡献 + 组织）

---

## 四、漏斗形信息流（Information Flow）

```
    ┌──────────────────────────────────────────┐
    │  WIDE: general importance & facts        │  ← Component 1 (wide end)
    └────────────┬─────────────────────────────┘
                 │
        ┌────────▼─────────┐
        │  literature map  │                     ← Component 2
        └────────┬─────────┘
                 │
           ┌─────▼──────┐
           │ gap/problem│                         ← Component 3
           └─────┬──────┘
                 │
              ┌──▼──┐
              │ this │                             ← Component 4 (narrow end)
              │paper │
              └─────┘
```

- 永远**先展示墙，再谈砖**（show the wall before the bricks）。
- Discussion 做相反方向的逆行（从 narrow 回到 wide）。

---

## 五、常见错误清单

| 错误 | 解决 |
|---|---|
| 开头直接描述具体问题 | 先建立领域重要性/背景，再逐步聚焦 |
| literature review 变成 reading list | 加入叙述主线，让每篇引文都指向本文动机 |
| gap 用问句表述 | 改用 prediction/suggestion/hypothesis 形式 |
| 引言过短（<10 句）导致铺垫不足 | 至少 15 句以上，分 3-5 段 |
| 方法描述过详 | 引言只给轮廓，细节留给 Methods |
| 贡献不清楚 | 在 S11 或末段加入证据强度匹配的贡献标记词；不要无证据使用 novel / significant / first |
| 跨学科读者不友好 | 增加对关键术语的简要解释 |
