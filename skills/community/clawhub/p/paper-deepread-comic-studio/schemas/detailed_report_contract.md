# Detailed Report Contract

Produce one authoritative detailed report per paper.

Preferred paths inside the uploaded or regenerated bundle:

- `reports/per_paper/<paper-slug>/<paper-slug>_detailed_cn.md`
- `reports/per_paper/<paper-slug>/<paper-slug>_detailed_cn.pdf`

Legacy-compatible fallback:

- `reports/<paper-slug>_detailed_cn.md`
- `reports/<paper-slug>_detailed_cn.pdf`

The detailed report must be at least as rich as the accepted-paper examples under:

- `E:/论文调研/reports/accepted_papers/*.md`

and must also include the additional graph-ready and direction-mining items required by this stage.

## Teaching-Explanation Mandatory Overlay

In addition to all sections below, the report must explicitly include a teaching-explainer layer. This layer is not a replacement for technical depth; it is a second pass that turns the same evidence into an explanation another person can understand, discuss, and challenge.

Minimum teaching-explainer outputs:

- `面向讲解的受众画像与讲解目标`: identify the default or user-specified audience, likely confusions, prerequisite concepts, math depth, and evidence needed.
- `3 层讲解摘要：30 秒 / 3 分钟 / 10 分钟`: provide three talk lengths without losing the central caveat.
- `讲解主线 Story Spine`: before -> pain -> broken assumption -> key replacement -> mechanism -> evidence -> caveat -> next idea.
- `听众先修知识与概念铺垫`: define the task, notation, assumptions, datasets, benchmarks, and field conventions needed before the method makes sense.
- `公式 / 图表 / 实验的讲解脚本`: say how to explain core formulas, visuals, and experiment blocks aloud.
- `板书推导与小例子演示`: walk through at least one central formula/update/mechanism with a concrete mini-case.
- `角色扮演式讨论问题`: build prompts for Archaeologist, Bug Hunter, Researcher, Industry Practitioner, Social Impact Assessor, Author Defender, and Teacher roles.
- `可能被问到的问题与回答证据`: create a Q&A bank for beginner, peer, advisor/reviewer, and practitioner questions.
- `易误解点与纠偏`: state what the paper does not claim, which analogy can mislead, and which result should not be overgeneralized.
- `PPT / 分享稿结构草案`: provide a slide/talk blueprint as a derivative of the authoritative report.
- `听众可带走的三句话`: three accurate takeaways.

If any teaching simplification conflicts with the rigorous reading, include the simplification and then immediately state its limits.

## Research-Generative Mandatory Overlay

In addition to all sections below, the report must explicitly include a research-generative reading layer. This layer is not a replacement for formula preservation, proof explanation, experiment analysis, reviewer audit, or graph-ready appendices; it is an extra idea-generation pass.

Minimum research-generative outputs:

- `研究方程与缺失机制替代`: express the paper as `Important Setting + Broken Assumption + Borrowed Tool + New Constraint + Surrogate Mechanism`, then identify the unavailable ideal mechanism `Y` and the constructed replacement `Z`.
- `作者可能如何发现这个方向`: reconstruct a plausible author-side discovery chain: valuable field, painful assumption, emerging tool, unserved setting, blocking constraint, replacement mechanism.
- `论文故事线如何搭建`: map challenge -> failure mode -> design principle -> module -> evidence, and judge whether the method is additive or closed-loop.
- `模块级作者思路深读`: for each key module, record failure, ideal unavailable solution, available proxy, design choice, hidden assumption, risk, and future research point.
- `关键引用的叙事功能与 Citation-to-Module Map`: explain why key citations appear as narrative functions, not merely as bibliography.
- `实验作为故事证据`: read each experiment as claim + counterfactual + metric + stress condition.
- `可复用的论文造故事模式`: extract the reusable paper-making pattern taught by the paper.
- `从隐藏假设生成新 idea`: convert hidden assumptions and fragile proxy mechanisms into concrete new research ideas, with boundary-pushing directions separated from ordinary engineering follow-up.

If any of these overlaps with an existing section, keep both lenses: the original deep-reading lens explains what the paper did and whether it is well supported; the research-generative lens explains how the paper could have been invented and how to generate the next paper from its fragile assumptions.

## Top-Conference Deepread Rule

The main body must explicitly cover the same kinds of sections that already appear in:

- `E:/论文调研/reports/accepted_papers/CoLoRA_detailed_cn.md`
- `E:/论文调研/reports/accepted_papers/FedDAG_detailed_cn.md`
- `E:/论文调研/reports/accepted_papers/LPSFed_detailed_cn.md`
- `E:/论文调研/reports/accepted_papers/pFedMMA_detailed_cn.md`

Do not stop at a short summary plus a graph appendix.
The authoritative report has two layers:

1. a top-conference-grade main narrative
2. a stage-specific structured appendix for graph building and innovation mining

The report should also be useful at four reading depths:

1. beginner depth: symbols, definitions, and setting are explained without assuming prior familiarity
2. reviewer depth: the report reconstructs what scientific gap is claimed, what evidence supports it, and where the paper still looks weak
3. downstream-builder depth: the report states literature relations, borrowed method families, exact improvements, proof roles, and graph-ready takeaways explicitly
4. innovation-auditor depth: the report judges claim support, innovation type, boundary crossing, and plausible future research directions explicitly
5. teaching-explainer depth: the report can be turned into a talk, Q&A, role-play discussion, and slide blueprint without losing rigorous caveats

## v1.2.0 Deep Explanation And Reproducibility Rule

The report must explain the paper deeply enough that the reader can reproduce the core method, defend it in a skeptical discussion, and teach it to someone else. Do not write broad generic summaries when the paper contains concrete symbols, formulas, modules, figures, data, or experimental protocols.

Use this order unless the paper's own structure makes a different dependency order clearer:

1. symbols, definitions, assumptions, labels, and task setting
2. data, inputs, preprocessing, and source evidence
3. model and modules
4. training objectives, trainable parameters, hyperparameters, and data flow
5. inference/deployment path and outputs
6. experiments, exceptions, reproducibility risks, and limitations

Every key concept must be explained as:

```text
直觉 -> 数学公式或 formal definition -> 具体例子 -> 局限 / failure case
```

Every complex module must state input, output, symbols, dimensions, trainable parameters, fixed hyperparameters, objective terms, training-time data flow, inference-time data flow, and what fails without the module.

Strictly separate evidence levels:

- `论文明确写明`: directly stated in the paper/PDF/LaTeX/rebuttal source.
- `论文没写但合理推测`: inferred from formulas, algorithm structure, tables, or surrounding text.
- `参考相近工作推测`: inferred from standard practice in cited or neighboring methods.
- `缺失 / 未报告`: not available in the provided sources.

When details are missing, list the gap instead of inventing it. This includes hardware, runtime, memory, optimizer, learning rate, seeds, early stopping, hyperparameter search, data split, label definition, preprocessing, baseline source, whether baselines were rerun or reconstructed, code availability, and compute budget.

The experiment section must include dataset scale, label definition, split protocol, baseline genealogy, whether baselines were rerun/reconstructed/imported, metric meanings, headline results, exceptions, ablation interpretation, qualitative evidence, and reproduction risk.

The technical explanation must include a complete numeric toy example that connects training and inference. Define tiny inputs, run the method through at least one training update or loss computation, identify which parameters are learned, then show one inference pass. If the paper does not provide enough detail, mark the example as simplified and state which parts are not paper-explicit.

## Figure And Experiment Evidence Rule

Do not skip figure interpretation. Whether the source is PDF or LaTeX, the report must explicitly explain important architecture figures, pipeline figures, qualitative examples, tables, charts, and curves. For each important visual, state:

- what it is trying to show
- which claim or sub-claim it is supposed to support
- whether the visual evidence really supports that claim, only partially supports it, or conflicts with it
- what remains unclear, visually misleading, or under-explained
- plausible reasons for any mismatch between the visual/data evidence and the paper's stated claims


The detailed report length is not capped. When the paper is dense, controversial, or theoretically layered, prefer a longer report rather than compressing away the reasoning chain.

The report must preserve and explain key formulas, key figures from both PDF and LaTeX sources, and the theory-to-practice relation instead of compressing them away.

The report must preserve key formulas instead of paraphrasing them away. When theory is present, the report must explain why the proof exists, what practical concern it addresses, and whether the implemented method is identical to the proved object, a local approximation, or only loosely motivated by it.

The report should also import extra reviewer concerns from strong GitHub paper-review / peer-review skills as an auxiliary audit target: novelty, significance, soundness, methodology rigor, reproducibility, results-claims alignment, missing baselines or controls, figure/table clarity, and honest limitation disclosure. When LaTeX sources are available, important figures must still be explained via figure environments, captions, labels, and referenced text rather than being silently skipped. The experiment section must explicitly explain key tables, curves, charts, and numeric comparisons, check whether they support the paper's claims, and analyze any inconsistency or partial mismatch.

## Mandatory Section Order

1. 论文信息
2. 论文标题解读
3. 这篇论文真正解决的是什么
4. 论文中提到的其他论文做了什么、留下了什么空白、与本文是什么关系
5. 核心方法到底在干什么
6. 公式保留与逐式解释
7. 具体公式、模块与设计假设的不足及可改进空间
8. 创新点、核心主张与证据逐条核对
9. 这篇论文为什么重要 / 为什么值得被接收
10. 实验是如何被设计出来的
11. 倒推作者怎么想到这个 idea
12. 研究方程与缺失机制替代
13. 作者可能如何发现这个方向
14. 论文故事线如何搭建
15. 模块级作者思路深读
16. 关键引用的叙事功能与 Citation-to-Module Map
17. 实验作为故事证据
18. 可复用的论文造故事模式
19. 从隐藏假设生成新 idea
20. 作者主观判断与研究风格关联分析
21. 报告具体性要求：必须紧扣论文中的公式、模块、图表、实验与措辞
22. 审稿人最关注什么
23. 额外审稿视角审计（借鉴 GitHub 热门审稿 skill 的 reviewer 关注点）
24. 作者是怎么回复的
25. 审稿人是否认同作者回复
26. 审稿意见回复覆盖核对
27. 这篇论文最强的地方
28. 这篇论文的弱点 / 不足
29. 作者团队近年的相关延续
30. 从这篇论文出发，最值得突破的未来边界
31. 创新类型判断：这是增量创新、交叉创新，还是边界突破
32. 对选题的直接启示
33. 可能的新研究方向或新创新点（尤其是可能推动科学边界的方向）
34. 面向讲解的受众画像与讲解目标
35. 3 层讲解摘要：30 秒 / 3 分钟 / 10 分钟
36. 讲解主线 Story Spine
37. 听众先修知识与概念铺垫
38. 公式 / 图表 / 实验的讲解脚本
39. 板书推导与小例子演示
40. 角色扮演式讨论问题
41. 可能被问到的问题与回答证据
42. 易误解点与纠偏
43. PPT / 分享稿结构草案
44. 听众可带走的三句话
45. 最后一段通俗故事总结
46. 参考来源
47. 结构化补充附录
48. Routing Appendix

## Structured Appendix Minimum

Inside `结构化补充附录`, include at least:

- 上位科学问题定位的三条证据链
- 统一后的更高层 AI/ML 问题
- 借鉴算法所属上位问题
- 新算法遇到的问题所对应的上位问题
- 模块到问题、算法与瓶颈的映射
- 知识图谱节点与关系候选
- 提出算法的模型、架构、训练与推理流程
- 关键概念的直觉 -> 数学公式 -> 具体例子 -> 局限解释
- 复杂模块的输入、输出、符号、维度、训练参数和数据流
- 公式保留与逐式解释
- 理论、证明与实现步骤对照
- 具体公式、模块与设计假设的不足及可改进空间
- 相关论文与关联理由
- 论文中反复提到的关键文献及其未解空白
- 创新点与主张的证据审计表
- 符号、定义与核心概念入门解释
- 带具体例子的算法步骤演示
- 完整数字例子：训练和推理串联
- 实验设置与比较算法谱系对应表
- 各实验环节的目的、支撑主张与现象总结
- 实验细节、例外结果与复现风险清单
- 借鉴 GitHub 热门审稿 skill 的额外审稿视角审计
- 创新类型与学科边界判断
- 审稿覆盖核对
- 架构图 / 模型图 / 结果图补充（含 LaTeX figure 环境解释）
- 架构图 / 模型图设计方案
- 实验图表设计可借鉴点
- 可继续追的创新点
- 研究方程与缺失机制替代
- challenge -> failure mode -> design principle -> module -> evidence 映射
- module -> unavailable ideal -> available proxy -> hidden assumption -> new idea 映射
- Citation-to-Module Map
- experiments-as-story-evidence matrix
- reusable story-making pattern
- hidden-assumption-to-boundary-direction table
- teaching story spine
- audience prerequisite map
- formula / visual / experiment teaching scripts
- role-play discussion prompts
- Q&A and defense bank
- slide / talk blueprint
- teachback self-test

## 新增刚性要求（作者主观关联与具体性）

- 在介绍 idea、理论证明、具体算法或模块时，若这些设计明显带有作者的主观判断、经验偏好、启发式选择、研究风格或工程取舍，应显式指出，并区分“客观上必须如此”与“作者选择这样做”。
- 报告不得停留在空泛抽象层面。必须结合论文本身的具体公式、符号、模块名、假设、数据集、baseline、图表、定理对象、实验现象与原文措辞做展开说明。
- 当推测作者主观动机时，要区分有文本证据支撑的判断与基于研究史/写作风格的合理推测。
