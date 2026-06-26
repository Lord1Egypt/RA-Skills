# Example: Close-Reading Mode Output

## Trigger

User says: "逐句拆解" / "完整精读" / "用于汇报" / "做 PPT"

## What You Get

Full Study Profile + Module A–G with maximum depth. Module C: sentence-level annotation (every sentence). Module D: full-image analysis for core figures + caption mode for supplementary. Module F: complete verbatim PPT scripts + Q&A + backup slides. May use phased execution for long papers.

## Example Output (Partial)

```markdown
# 论文 Results 反向拆解

## Metadata
| 字段 | 值 |
|------|----|
| Paper | Dimsdale-Zucker et al. (2018) |
| Year | 2018 |
| Journal | Journal of Neuroscience |
| Analysis Mode | close-reading (full validation) |
| Branch | F. Cognitive Neuroscience / fMRI |

### 三轴分类
| 轴 | 类别 | 值 |
|----|------|----|
| Axis 1 | Article Type | Empirical experiment (within-subject fMRI) |
| Axis 2 | Substantive Domain | Cognitive Neuroscience / Memory / fMRI |
| Axis 3 | Data/Method Modality | fMRI RSA, behavioral accuracy, item memory, spatial memory |
| Primary Branch | F. Cognitive Neuroscience / fMRI |

## Study Profile
[Complete profile with split hypothesis fields, task terminology verified against Methods]

---

## Module C: Results 逐句拆解（Close-Reading）

### ¶1: ROIs responded differentially to spatial context — Label distribution

功能标签说明：**1** 重提研究目的/假设 | **2** 重提关键方法 | **3** 总述结果趋势 | **4** 邀请查看图表 | **5** 报告具体结果 | **6** 报告统计证据 | **7** 评价性强调 | **8** 与既有研究比较 | **9** 与预测/模型/理论比较 | **10** 解释结果原因 | **11** 指出不显著/不一致 | **12** 承认限制/异常 | **13** 提示结果意义 | **14** 过渡到 Discussion

> S1: "Our fMRI representational similarity analyses revealed that hippocampal subfields responded differentially to the reinstatement of episodic context."
- **Label 3 (总述结果趋势)** + **Label 2 (重提关键方法: "fMRI representational similarity analyses")**
- 🔍 此句为整个 ROI analysis 段落的 topic sentence，同时重提方法和总述趋势

> S2: "As can be seen in Fig. 2, neither CA23DG (χ²(1)=0.08, p=0.78) nor CA1 (χ²=0.03, p=0.86) systematically differed in their response to same-video vs. different-video items."
- **Label 4 (邀请查看图表: "As can be seen in Fig. 2")** + **Label 11 (指出不显著)** + **Label 6 (报告统计证据)**
- 🔍 两个 χ² 都极不显著→subfields 不编码 simple video match；这是重要的 null result

> S3: "In contrast, the subiculum showed a significant difference between same-video and different-video items (χ²(1)=6.50, p=0.01), with greater pattern similarity for same-video items."
- **Label 6 (报告统计证据)** + **Label 5 (报告具体结果 — "greater pattern similarity")**
- 🔍 subiculum 是唯一显示 video context sensitivity 的区域

[Sentence-by-sentence annotation for entire Results section...]

---

## Module D: 表格/图表讲解（Close-Reading Depth）

### Figure 2 — ROI RSA Results (Full Image Mode)
[Full vision-model analysis: axes, bars, error bars, colors, pattern description]

### Figure 3 — RSA Brain Maps (Full Image Mode)
[Detailed spatial pattern analysis]

---

## Module F: PPT / 汇报讲解版本（Close-Reading Full Script）

### 总时长建议：15–18 分钟

| 页码 | 内容 | 时长 | 讲法 |
|------|------|------|------|
| 1–2 | 研究背景与问题 | 2 min | ... |
| 3 | 实验设计与方法 | 3 min | ... |
| 4–6 | 行为结果 | 4 min | ... |
| 7–9 | fMRI RSA 结果 | 5 min | ... |
| 10 | 讨论与限制 | 3 min | ... |

### Slide 7: ROI RSA 结果

**逐字讲稿：**
> "接下来我们进入核心的 fMRI 结果。这里我们使用了 Representational Similarity Analysis——多元模式分析的一种——来考察海马子区如何编码空间情境。
>
> 这张图展示的是四个海马子区的模式相似性。横轴是四个子区——CA1、CA23DG、subiculum 和 entorhinal cortex。纵轴是 Fisher Z-transformed pattern similarity。深蓝色是 same-video 条件，浅蓝色是 different-video 条件。
>
> 先看 CA23DG 和 CA1——两者在 same-video 和 different-video 条件下的模式相似性没有显著差异。也就是说，CA1 和 CA23DG 并不简单地区分同一个视频还是不同视频。
>
> 但注意看 subiculum——same-video 条件下的模式相似性显著高于 different-video。统计学上，χ²(1)=6.50, p=0.01。这意味着 subiculum 对 video context 有敏感——它"知道"这些物体是由同一个视频编码的。
>
> 作者在 Discussion 中进一步解释：subiculum 可能在 retrieve 已建立的 episodic representation，而 CA23DG 在面临 conflicting spatial context 时——即 different house 条件——drives 一个新的 distinct representation。这是他们在全文讨论中阐述的 pattern completion vs. pattern separation 互补分工模型。
>
> 但我需要强调：'pattern completion' 和 'pattern separation' 是作者的 Discussion 解释，不是 Results 的直接结果宣读。我们在汇报论文时需要严格分开'数据显示了什么'和'作者如何解释'。数据显示的是 CA1 和 CA23DG 在 same-video vs. different-video 条件下呈现反向分离的交互模式，以及 subiculum 的 video context sensitivity。至于这一模式背后是不是 computable as pattern completion / separation，这是需要更多 computational modeling 来检验的。"

### 预计 Q&A

**Q: CA1 是否真的在做 pattern completion？**
A: "数据显示 CA1 对 same-video 项目的 similarity 更高，对 different-video 项目的 similarity 更低，形成了一个交互模式。这与 pattern completion framework 的预测一致——即同一 episode 内的物体被 reactivated 为同一 pattern——但 pattern completion 是一个计算框架的术语，不是数据本身的宣读。我们的数据为这个框架提供了 behavior-level and neural-level consistency，但 definitive proof 需要额外的 modeling 证据。"

### 备用 Slide

[Additional backup slides for deeper technical discussion]

---

## Module G: 自检（Close-Reading Mode）

[All G0–G8 checks performed against original paper source]

**G0 Source Verification (selected fields):**
- Claim: N=28
- Exact source phrase: "Twenty-eight healthy right-handed volunteers (14 female)..." (Methods, Participants)
- Interpretation: ✅ N correctly reported
- Confidence: high
- Needs manual check: no

[Additional verification items...]

**G3 反模板污染检查：** ✅ 无跨论文模板污染

---

当前使用 close-reading / full validation mode。若只需要快速版，可使用 quick mode；若需要一般精读版，可使用 standard mode。
```
