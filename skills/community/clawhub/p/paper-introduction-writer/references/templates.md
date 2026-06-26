# 按学科分类的引言模板（Templates）

本文件提供 **6 个学科模板 + 1 个通用模板** 的骨架，用方括号 `[...]` 标记占位字段，用 `{...}` 标记条件选项。生成引言时，匹配最接近的模板，再用用户提供的内容替换占位符。

模板结构都采用**四组件**骨架，但在组件比重、连接语和贡献标记词上做了学科化调整。

注意：模板中的 `[ref]` 只是引用槽位标记。真实投稿稿件中，应优先替换为用户提供的真实引用；若用户未提供引用，输出时改用语义化占位符（如 `[REF: closest prior method]`），不要创造看似真实的作者年份。

---

## 通用模板（General Template）—— 所有领域

### Component 1 · 第 1 段（3-5 句）

```
[TOPIC] has received considerable attention in recent years due to [REASON_1] and [REASON_2]. 
[TOPIC] is [DEFINITION/BACKGROUND FACT] [ref]. 
{Additional background fact linking TOPIC to its broader context.}
{It has [outstanding/desirable properties] for use in [APPLICATIONS].}
However, [GENERAL PROBLEM IN THE FIELD] has limited its [applicability/use/effectiveness].
```

### Component 2 · 第 2 段（4-6 句）

```
Several approaches have been proposed to address [GENERAL PROBLEM].
For example, [AUTHOR1 et al.] [showed/demonstrated/proposed] [CONTRIBUTION_1] [ref].
A similar approach was used by [AUTHOR2 et al.], who [CONTRIBUTION_2] [ref].
Subsequently, [AUTHOR3 et al.] extended this by [CONTRIBUTION_3] [ref].
{Alternative approaches include [APPROACH_X] [ref] and [APPROACH_Y] [ref].}
Taken together, these studies have improved our understanding of [SUBFIELD].
```

### Component 3 · 第 3 段（2-4 句）

```
However, [CRITICAL GAP or LIMITATION of prior work].
{In particular, little attention has been paid to [SPECIFIC GAP].}
{Moreover, existing methods suffer from [LIMITATION_1] and [LIMITATION_2].}
This leaves open the question of [THE SPECIFIC QUESTION THIS PAPER ADDRESSES].
```

### Component 4 · 第 4 段（3-5 句）

```
In this paper, we [DESCRIBE THE PAPER]. 
To [AIM], we [METHOD OUTLINE]. 
{We [WHAT WE DID: acquired / developed / designed / evaluated...]}
Our results reveal [MAIN FINDING, with calibrated contribution marker].
{If supported by the literature, To our knowledge, this is the first [X].}
{The remainder of this paper is organized as follows: ...}
```

---

## 模板 1：材料科学 / 化学 / 纳米材料

**特点**：漏斗铺得较长；大量背景化学/结构事实；gap 常常是"性能-成本-稳定性"之间的矛盾；在证据充分时可强调 "first synthesis / first demonstration"。

### 骨架

```
[MATERIAL/COMPOUND] has received much attention in recent years due to its [PROPERTY_1] and [PROPERTY_2] [ref]. 
[MATERIAL] is [CHEMICAL DEFINITION OR COMPOSITION], [STRUCTURAL DETAIL]. 
It has [outstanding / remarkable / tunable] [PROPERTY_3] for use in [APPLICATION_1] and [APPLICATION_2] [ref, ref].

Among the various classes of [MATERIAL FAMILY], [SUBTYPE_1] has emerged as particularly promising [ref]. 
Several [synthesis / fabrication / deposition] methods have been reported, including [METHOD_1] [ref], [METHOD_2] [ref], and [METHOD_3] [ref]. 
For example, [AUTHOR et al.] achieved [RESULT] using [METHOD] [ref]. 
A related approach by [AUTHOR2 et al.] demonstrated [RESULT2] [ref].

However, [LIMITATION OF PRIOR WORK — e.g., low yield / poor stability / high cost / lack of scalability]. 
In particular, [SPECIFIC ISSUE]. 
To our knowledge, no prior work has [WHAT IS MISSING].

In this paper, the [synthesis / preparation / characterization] of [NEW MATERIAL / NEW STRUCTURE] is reported. 
[MATERIAL/STRUCTURE] was prepared by [METHOD]. 
The following questions are addressed: (a) [QUESTION_1]; (b) [QUESTION_2]; (c) [QUESTION_3]. 
{Our findings demonstrate a [calibrated contribution marker] [X] that [OUTCOME supported by the data].}
```

### 可选贡献标记词组合
- new synthesis route; high-yield; air-stable; earth-abundant; catalytically active; thermally robust
- use `novel` or `first demonstration` only when the manuscript can substantiate the claim

---

## 模板 2：生命科学 / 医学 / 细胞生物学

**特点**：开头常强调生物系统的重要性；大量机制性背景；gap 往往是"机制不清 / 发育阶段不可及 / 缺乏模型"；结尾侧重"揭示机制 / 提供新模型"。

### 骨架

```
[BIOLOGICAL PROCESS / DISEASE / TISSUE] plays an essential / critical role in [BROADER PHYSIOLOGICAL CONTEXT] [ref]. 
[BACKGROUND FACT about cell type / pathway / molecular players]. 
{For example, [SPECIFIC MECHANISM]}. 
This process is [regulated / orchestrated / controlled] by [REGULATORS — signalling pathways, transcription factors, etc.] [ref, ref].

Although considerable efforts have been focused on [SUBFIELD], [CURRENT LIMITATIONS]. 
This is largely due to [UNDERLYING DIFFICULTY — e.g., lack of adequate tissues, limited model systems, ethical constraints]. 
{[AUTHOR et al.] demonstrated [RESULT] [ref], and [AUTHOR2 et al.] further showed [RESULT2] [ref].}
{Together, these findings suggest [CURRENT UNDERSTANDING].}

Human [embryonic / induced pluripotent / primary] [CELL TYPE] offer a [valuable / promising] platform to [STUDY THE QUESTION] because they [PROPERTY_1] and [PROPERTY_2] [ref]. 
{Although [CURRENT METHODS] do not fully recapitulate [IN VIVO PROCESS], increasing evidence demonstrates that [SUPPORTING FACT] [ref].}

However, little is known about [THE SPECIFIC GAP THIS PAPER ADDRESSES]. 
It is not clear whether [THE SPECIFIC QUESTION]. 
{The [EARLY / INTERMEDIATE / LATE] [PROCESS / POPULATION] has not been [characterized / isolated / identified].}

In this study, we [CAREFULLY/SYSTEMATICALLY] [identified / isolated / characterized / tracked] [TARGET POPULATION / PHENOMENON], and demonstrated that [KEY FINDING]. 
{Our results reveal [FINDING_1] and [FINDING_2].}
{The identification of [X] will provide a valuable [resource / model / tool] to elucidate the molecular mechanisms that regulate [PROCESS].}
```

### 可选贡献标记词组合
- first identification; distinct from; intermediate features; valuable in vitro model; systematic characterization

---

## 模板 3：计算机科学 / 机器学习 / 人工智能

**特点**：更直接；背景短；较早进入 prior work 综述；gap 多为"算法慢/精度低/内存爆/不 scalable"；结尾常包含论文组织与贡献列表。

### 骨架

```
[PROBLEM / METHOD] is among the most [popular / widely used / well-studied] [approaches / tasks / models] in [FIELD] today. 
[BRIEF TECHNICAL BACKGROUND — what the problem/method is]. 
{This approach has been extended to various tasks, including [TASK_1] [ref], [TASK_2] [ref], and [TASK_3] [ref].}

[TRAINING / SOLVING / DEPLOYING] [METHOD] amounts to [UNDERLYING COMPUTATIONAL PROBLEM]. 
Although general-purpose solvers can handle small-scale instances, much effort has been devoted to designing specialized solvers for [LARGE-SCALE / STRUCTURED] instances. 
For example, [METHOD_1] [ref] and [METHOD_2] [ref] have recently been established as effective for [SCENARIO_1]. 
For [SCENARIO_2], most leading solvers are based on [APPROACH] [ref, ref]. 
{Such approaches can handle fairly large problems, provided that [CONDITION], but [LIMITATION REMAINS].}
There is therefore still a strong need for [IMPROVED DIMENSION — faster / more accurate / lower-memory / more general].

One attractive possibility for enabling [IMPROVEMENT] is to leverage [NEW RESOURCE / TECHNIQUE / INSIGHT]. 
[JUSTIFICATION for why NEW RESOURCE is promising]. 
In this paper we discuss how [METHOD] can be efficiently implemented via [RESOURCE], and present such an implementation for [SCENARIOS].

Several authors have recently proposed [RELATED WORK SIMILAR TO OURS] [ref, ref]. 
These previous approaches, however, [LIMITATION — e.g., focused only on X, did not consider Y, assumed Z]. 
We study various [algorithmic / architectural / training] choices in the context of [RESOURCE], discuss how the optimal choices differ from [PRIOR SETTING], and arrive at an implementation specifically designed for [TARGET SETTING].

{One particularly significant drawback of prior [X] is [LIMITATION_Z]. In contrast to prior work, our implementation [HOW WE ADDRESS LIMITATION_Z].}

Overall, our implementation is [CALIBRATED MARKER — orders of magnitude faster / substantially more accurate / memory-efficient] than existing [CPU/baseline/prior] implementations. 
{The remainder of this paper is organized as follows. Section 2 [...]. Section 3 [...]. Section 4 [...]. Section 5 concludes.}
```

### 可选贡献标记词组合
- orders of magnitude faster; scalable; memory-efficient; robust; practical
- use `state-of-the-art`, `novel architecture`, or `first demonstration` only with benchmark or literature support

---

## 模板 4：工程学 / 结构健康监测 / 机械工程

**特点**：强调"工业/安全关键"重要性；在"工业应用"和"学术研究"间建立桥梁；gap 多为"受环境影响/泛化性差/只在受控实验"；结尾常含实验平台细节。

### 骨架

```
Considerable effort has been expended on the development of [SYSTEM / TECHNOLOGY] [ref, ref], because these are widely regarded as capable of [KEY BENEFIT — e.g., significantly reducing inspection costs / improving safety] of [CRITICAL STRUCTURES] in industries such as [INDUSTRY_1], [INDUSTRY_2], and [INDUSTRY_3]. 
Successful [SYSTEMS] can be considered as those which combine [CAPABILITY_1], [CAPABILITY_2], and [CAPABILITY_3].

[TECHNIQUE_CATEGORY] systems based on [UNDERLYING PHYSICAL PRINCIPLE] have been applied to [APPLICATION] [ref, ref]. 
These systems take advantage of [PHYSICAL PROPERTY]. 
Recently, focus has shifted to the development of [NEW VARIANT] [ref, ref], where [DESIGN FEATURE] would allow [BENEFIT].

So far, effective [commercial / industrial] applications [ref, ref] have been achieved only when [FAVORABLE CONDITION]. 
[DESCRIBE TYPICAL CHALLENGE — e.g., coherent noise, signal interference]. 
In these cases, it is necessary to use [STANDARD MITIGATION — e.g., baseline subtraction, calibration]. 
{This [MITIGATION] controls the [PERFORMANCE METRIC — e.g., sensitivity, accuracy, throughput].}

It is well known that [ENVIRONMENTAL / OPERATING CONDITIONS] affect [SYSTEM BEHAVIOR] [ref, ref, ref]. 
Of these effects, [MOST COMMON ONE] is the most commonly encountered, and several authors have developed compensation techniques. 
These are usually based on [APPROACH_1] [ref] or [APPROACH_2] [ref]. 
The advantages and limitations of each technique have been evaluated by different authors, and it has been shown that [COMBINED / IMPROVED STRATEGY] results in a promising [CAPABILITY] [ref, ref].

This paper demonstrates results obtained when [SYSTEM] was applied to [TEST OBJECT] subjected to [REAL-WORLD CONDITIONS]. 
Initially, [STEP_1 — feasibility / mode evaluation]. 
Baselines were acquired from [SENSOR SETUP] over [TIME PERIOD] and the stability of [METHODS] was assessed. 
Defects of different [PARAMETER] were machined in the structure and the detection capability of the system was verified.
```

### 可选贡献标记词组合
- robust; reliable; real-world conditions; comprehensive evaluation; practical applicability

---

## 模板 4B：工程 / 交通 / 设计短引言（§1.6 练习模式）

**特点**：适合 250-350 words 的短 Introduction、课程练习、letter-style 工程设计论文。采用紧凑 3 段式：C1 单独一段，C2 与 C3 合并一段，C4 可压缩为 1-2 句。典型题目：SPPPV / bicycle cover / commuter vehicle / protective design。

### 骨架

```
[BROAD ISSUE] has become a central issue in [POLICY / INDUSTRY / SOCIETY].
[BACKGROUND FACT] is linked to [CAUSE / DRIVER] [ref], and [POLICY / MARKET GOAL] aims to [TARGET] within [TIME FRAME] [ref].
As a result, much research has focused on developing [ENVIRONMENTALLY FRIENDLY / SAFETY-CRITICAL / LOW-COST] [SYSTEMS] such as [SPECIFIC SYSTEM].
However, although [POSITIVE TREND], [SAFETY / COMFORT / RELIABILITY] issues need to be addressed if [LARGER ADOPTION OR IMPACT GOAL] is to be achieved.

Researchers have studied and improved many [SAFETY / PERFORMANCE] aspects of [SPECIFIC SYSTEM].
In [YEAR], [AUTHOR] responded to the need for [NEED] by designing [FEATURE_1] [ref], and in [YEAR] [AUTHOR] introduced [FEATURE_2] to [PURPOSE] [ref].
The issue of [COMFORT / PROTECTION / USABILITY] has also been addressed; in [YEAR] [AUTHOR] introduced [FEATURE_3] [ref], and more recently [AUTHOR] added [FEATURE_4] to [PURPOSE] [ref].
However, it has been suggested that [FEATURE_3] and [FEATURE_4] negatively affect [PERFORMANCE METRIC] [ref].

In this study, we [MODEL / SIMULATE / EVALUATE] the [PERFORMANCE] effect of these [SAFETY / COMFORT] features and use the data thus obtained to propose a new design which balances [DESIGN PARAMETERS] with optimum [PERFORMANCE].
```

### 使用规则

- 目标长度：约 250-350 words，通常 8-12 句、3 段。
- 必须保留四组件；不要因为短而删除 C2 或 C3。
- 允许使用 fake references 仅限课程练习；真实稿件使用用户引用或语义化占位符（如 `[REF: prior comfort design]`）。
- 若题目就是 "A cover for the single-person pedal-powered vehicle"，同时读取 `writing-practice.md` 与 `examples.md` 的样例 7。

### 可选贡献标记词组合
- new design; balanced; optimum aerodynamic performance; lightweight; protective; practical; user-centred

---

## 模板 5：物理学 / 光学 / 神经科学（系统层面）

**特点**：背景极其细致，常包含多层次事实；literature review 可能非常长；gap 通常是"不同尺度/不同方法的统合"；结尾常预告多个 finding。

### 骨架

```
[PHENOMENON / STATE] is [FUNDAMENTAL DEFINITION] [ref]. 
[IMPORTANT CONTEXTUAL FACT — why it matters scientifically or clinically]. 
One of the most [widely studied / commonly used] [SYSTEMS / DRUGS / MATERIALS] in this area is [SPECIFIC INSTANCE], which [MECHANISM OF ACTION] [ref, ref]. 
Despite [WHAT IS ALREADY UNDERSTOOD], it is not clear how [LEVEL_1 EFFECTS] give rise to [LEVEL_2 OBSERVATIONS].

The effects on [SCALE_A — macroscopic / behavioral / electrical] have been extensively characterized. 
These include [PHENOMENON_1] [ref], [PHENOMENON_2] [ref], and [PHENOMENON_3] [ref, ref]. 
{In addition, [PHENOMENON_4] has been documented in [SYSTEM] and is associated with [FURTHER MECHANISM] [ref, ref].}

Although these [patterns / signatures] are observed consistently, it is unclear how they are [functionally / causally] related to [TARGET STATE]. 
Most studies have focused on [STEADY STATE / LIMITED CONDITION] and have not [CRITICAL MISSING STEP — e.g., tracked transitions, measured multi-scale dynamics, related levels]. 
[TARGET STATE] can occur [ON FAST TIMESCALE] [ref], but many [VARIABLES] continue to [DO SOMETHING] for [LONGER] and are highly variable between different levels of [CONDITION] [ref, ref]. 
Therefore, identifying the specific [DYNAMICS / MECHANISMS] associated with [TARGET] requires [WHAT IS NEEDED]. 
In addition, [SECONDARY GAP — e.g., dynamic interactions between regions] are not well understood, because [REASON]. 
Consequently, how [DRUG / STIMULUS] acts on [SYSTEM] to produce [OUTCOME] remains unclear.

To address this question, we investigated [MULTI-LEVEL OBSERVATIONS] during [CRITICAL TRANSITION]. 
We obtained [MEASUREMENTS — simultaneous recordings / high-resolution imaging / multi-modal data], enabling us to examine [DYNAMICS] at multiple [spatial / temporal / organizational] scales. 
We used [REFERENCE TASK OR METRIC] to identify [CRITICAL EVENT].

Our results reveal a set of [FEATURES] that accompany [EVENT] that, together with previously reported effects [ref, ref, ref], enable a multi-scale account of this profound shift in [STATE]. 
We find that [FINDING_1 WITH CALIBRATED CONTRIBUTION MARKER]. 
{We further observe that [FINDING_2].}
{These results demonstrate that [INTERPRETATION].}
We conclude that [BIG-PICTURE CONCLUSION], marking a [NEW UNDERSTANDING].
```

### 可选贡献标记词组合
- multi-scale account; profound shift; fundamental component; simultaneous recordings

---

## 模板 6：交叉学科 / 新兴领域 / 综述式引言

**特点**：两个以上领域的 bridge；需要为不同读者解释更多术语；gap 可能是"两个领域之间尚未连接"；结尾常强调"integration / unified framework"。

### 骨架

```
[BROAD PHENOMENON / GRAND CHALLENGE] has emerged as a central problem in [FIELD_A] and [FIELD_B] [ref, ref]. 
[DEFINITION / CONTEXT making the phenomenon accessible to both audiences].
Understanding [PHENOMENON] requires insights from both [FIELD_A, where X is well-developed] and [FIELD_B, where Y is well-developed].

In [FIELD_A], significant progress has been made in [SUBDOMAIN_A]. 
{For example, [AUTHOR et al.] demonstrated [CONTRIBUTION_A1] [ref], and [AUTHOR2 et al.] extended this with [CONTRIBUTION_A2] [ref].}
Similarly, [FIELD_B] has advanced our understanding of [SUBDOMAIN_B], with [AUTHOR3 et al.] showing [CONTRIBUTION_B1] [ref] and [AUTHOR4 et al.] showing [CONTRIBUTION_B2] [ref].

However, these two [lines of research / communities] have developed largely independently. 
Approaches from [FIELD_A] often [LIMITATION when applied to FIELD_B's questions], while methods from [FIELD_B] [LIMITATION when applied to FIELD_A's questions]. 
As a result, [THE UNIFIED QUESTION / INTEGRATIVE CHALLENGE] remains largely unexplored. 
{A unified framework that combines [INSIGHTS_A] with [INSIGHTS_B] could enable [NEW CAPABILITIES].}

In this paper, we propose [A UNIFIED / INTEGRATIVE / BRIDGING] approach that [HOW IT BRIDGES THE TWO]. 
Specifically, we [METHOD COMBINING ELEMENTS FROM BOTH FIELDS]. 
We evaluate our approach on [BENCHMARK / DATASET / SYSTEM] and demonstrate that [MAIN FINDING WITH CALIBRATED CONTRIBUTION MARKER]. 
{If supported by the literature, To our knowledge, this is the first [X that integrates Y and Z].}
The remainder of this paper is organized as follows. [...]
```

### 可选贡献标记词组合
- unified framework; integrative approach; bridges; first integration; significantly broadens

---

## 模板选择决策表

| 用户所在领域 | 推荐模板 |
|---|---|
| 材料科学、纳米、催化、化学合成 | 模板 1 |
| 细胞生物学、干细胞、基因、医学研究、免疫 | 模板 2 |
| 机器学习、AI、算法、分布式系统、数据库、NLP、CV | 模板 3 |
| 结构健康监测、机械工程、传感器网络、土木工程、航空航天 | 模板 4 |
| 交通工具设计、SPPPV、自行车罩、250-350 词短引言练习 | 模板 4B |
| 神经科学（系统层面）、物理（光学/凝聚态）、天文 | 模板 5 |
| 生物信息学、计算化学、计算神经、HCI、neuro-symbolic | 模板 6 |
| 都不完全匹配 | 通用模板 |

---

## 如何使用模板

1. **确认模板**：用上面的决策表选好模板。
2. **逐占位符替换**：用用户提供的内容替换 `[...]`。
3. **处理条件选项**：`{...}` 中的内容按用户材料的丰富度决定是否保留。
4. **调整句长/段落**：若用户材料少，保留核心；若材料丰富，展开到 4-5 段。
5. **自然化润色**：模板生成的句子需要自然化——去重复、调节奏。
6. **插入引用**：用户提供的引用放到对应位置；未提供的用语义化占位符（如 `[REF: closest prior method]`）占位。
7. **核查四组件完整性**：生成后用组件清单对照，确保没有缺失。
