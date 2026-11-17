# LLM Wiki 健康评分维度设计依据

## 文件目的

本文件说明 `llm-wiki-health-score` v0.5 的维度为什么这样设计、每个维度对应哪些论文/理论/标准，以及哪些部分仍属于工程假设。

结论先行：

- 维度有论文、理论或标准支撑。
- 权重没有现成论文直接支撑，属于工程初始权重。
- 权重应通过个人知识库的历史任务表现继续校准。
- LLM 语义评分必须受 rubric、样本和文件证据约束，不能自由裁判。

## 设计原则

### 1. 架构不合格不等于无法评分

知识管理成熟度模型和 CMMI 都采用分层/分级成熟度诊断。低成熟度对象仍可被评估，只是得分较低。因此 v0.5 把“是否符合卡帕西式 LLM Wiki”放入 `llm_wiki_architecture_fit` 维度，而不是作为硬门槛。

### 2. 核心架构不能绑定到局部文件名

卡帕西式 LLM Wiki 的核心是 raw/source 原始资料层、wiki 综合层、schema/rules 规则层，以及 ingest/query/lint 维护循环。`index.md`、`log.md`、`核心文件索引.md` 可以是优秀实现的一部分，但不是所有知识库都必须采用这些文件名。因此它们只作为导航、检索和维护信号。

### 3. 结构化信号和语义抽样必须融合

结构化扫描能判断文件、目录、链接、marker、日志是否存在；但不能判断规则是否无歧义、沉淀是否忠实、回答是否真的有用。语义抽样能判断这些高阶质量，但有主观性和偏差。v0.4 采用脚本校验和维度级融合，降低两类方法的缺陷。

### 4. LLM 不能自由判定“等价协议”

LLM-as-a-Judge 研究明确讨论可靠性、偏差和一致性风险。因此本 skill 不让 LLM 单独判断“Core Notes 或等价协议是否通过”。脚本只采纳可观察证据；LLM 只评价证据的清晰度、覆盖范围和可执行性。

### 5. 语义抽样需要固定探针问题

RAG 和 LLM-as-a-Judge 评估都强调问题集、样本和评分细则会显著影响结果。为减少每轮评分随意换问题造成的漂移，本 skill 使用 `references/probe_questions.md` 作为固定探针问题集。评估者可以补充领域问题，但不能跳过标准问题。

### 6. 自动生成关系块不能替正文背书

`CORE_RELATIONSHIPS_V1` 等自动生成块主要服务图谱维护，不等于作者在正文中给出的来源证据。来源可追溯性统计先剥离 `CORE_*` 自动生成块，避免机器关系让 wiki 的证据支撑虚高。

### 7. 同名链接歧义应显式暴露

大型 Obsidian 库中常出现同名文件。若只按文件名覆盖索引，会把错误链接误判为可达。当前脚本把 Wiki 链接解析为 `resolved`、`ambiguous`、`dangling` 三态，歧义链接进入检索和维护健康信号。

## 维度与论文/理论映射

| 评分维度 | 主要支撑来源 | 映射关系 |
|---|---|---|
| `llm_wiki_architecture_fit` | Andrej Karpathy, "LLM Wiki"; Teah, Pee & Kankanhalli, "Development and Application of a General Knowledge Management Maturity Model"; CMMI capability/maturity levels | LLM Wiki 提供 raw/wiki/schema 和维护循环的架构原型；G-KMMM/CMMI 支撑用成熟度维度评估结构，而不是不满足即拒评。 |
| `source_traceability` | W3C PROV-O / PROV-DM; Wang & Strong, "Beyond Accuracy: What Data Quality Means to Data Consumers"; ISO/IEC 25012 | PROV-O 支撑 provenance/来源建模；Wang & Strong 支撑数据质量不止准确性，还包括可访问、可理解、上下文适配；ISO 25012 支撑完整性、一致性、当前性等数据质量特征。 |
| `schema_governance_quality` | ISO/IEC/IEEE 29148:2018; IEEE 830 SRS quality tradition; requirements-quality literature | Schema 层本质上是 agent 的操作需求和治理规则，因此用完整、一致、无歧义、可验证、可追溯、可维护来评估。 |
| `knowledge_sedimentation_effectiveness` | SummEval: "Re-evaluating Summarization Evaluation"; Wang & Strong data quality dimensions; Karpathy "LLM Wiki" compounding wiki idea | wiki 沉淀类似长期摘要和综合，需要忠实、完整、相关、连贯；同时要能把 raw 信息压缩成可复用知识，实现知识复利。 |
| `retrieval_answerability` | RAGAS: "Automated Evaluation of Retrieval Augmented Generation"; ARES: automated RAG evaluation; DeLone & McLean IS Success Model | 查询能力既涉及系统质量/使用效果，也涉及检索上下文相关性、回答忠实性和答案相关性。 |
| `maintenance_evolution` | G-KMMM; CMMI; Karpathy "LLM Wiki" ingest/query/lint loop; ISO 25012 currentness/consistency | 知识库不是静态文档堆，健康度取决于持续维护、日志、过期检测、冲突处理和修复流程。 |

## 细分指标映射

### LLM Wiki 架构符合度

| 细分项 | 支撑来源 |
|---|---|
| raw/wiki/schema 分层 | Karpathy "LLM Wiki" |
| ingest/query/lint 操作 | Karpathy "LLM Wiki" |
| agent 可操作性 | ISO/IEC/IEEE 29148 的需求过程和信息项思想 |
| 模块化和适配性 | Karpathy 对具体实现可选、模块化的思想；G-KMMM 的成熟度演进思想 |

### 来源可追溯性

| 细分项 | 支撑来源 |
|---|---|
| provenance 覆盖 | W3C PROV-O / PROV-DM |
| claim-source alignment | RAGAS faithfulness；SummEval consistency |
| 引用粒度 | PROV-O provenance modeling；ISO 25012 accuracy/completeness |
| source recoverability | Wang & Strong accessibility / representational quality；PROV-O provenance 可由 sidecar、manifest、正文引用、frontmatter scope、机器索引或外部索引 DB 承载 |

### Schema 治理质量

| 细分项 | 支撑来源 |
|---|---|
| 完整性 | ISO/IEC/IEEE 29148；IEEE 830 |
| 一致性 | ISO/IEC/IEEE 29148；IEEE 830 |
| 无歧义 | requirements-quality literature；IEEE 830 |
| 可验证 | ISO/IEC/IEEE 29148 |
| 可追溯 | ISO/IEC/IEEE 29148；PROV-O |
| 可维护 | IEEE 830；CMMI/G-KMMM |

### 知识沉淀有效性

| 细分项 | 支撑来源 |
|---|---|
| groundedness | RAGAS faithfulness；PROV-O |
| completeness | SummEval；Wang & Strong |
| relevance/actionability | SummEval relevance；DeLone & McLean net benefits |
| coherence/readability | SummEval coherence/fluency |
| source integration | Karpathy compounding wiki；SummEval consistency |
| freshness/conflict handling | ISO 25012 currentness/consistency；G-KMMM |

### 检索与回答可用性

| 细分项 | 支撑来源 |
|---|---|
| navigation findability | DeLone & McLean system quality/use；Wang & Strong accessibility |
| context precision | RAGAS context precision；ARES context relevance |
| answer faithfulness | RAGAS faithfulness；ARES answer faithfulness |
| answer relevance | RAGAS answer relevance；ARES answer relevance |

### 维护与演化健康度

| 细分项 | 支撑来源 |
|---|---|
| logging freshness | Karpathy lint/log loop；ISO 25012 currentness |
| staleness detection | ISO 25012 currentness；CMMI/G-KMMM |
| conflict handling | ISO 25012 consistency；Karpathy contradiction handling |
| repair workflow | CMMI process capability；Karpathy ingest/query/lint |

## LLM 语义评分误判控制

| 风险 | 控制方式 |
|---|---|
| LLM 把“看起来像规则”的文字误判为协议 | 只允许脚本采纳明确文件证据；LLM 只评价证据质量。 |
| LLM 高估自己没读到的内容 | 每个维度强制 evidence；没有 `file` 和 `note` 时脚本拒绝最终评分。 |
| LLM 对抽样页面偏差过大 | 样本优先取最新 wiki、schema、raw/source、导航和日志；必要时扩大样本。 |
| LLM 评分口径漂移 | 使用固定 0-5 criteria、0-100 dimension score 和固定探针问题集。 |
| LLM 给出细项低但维度总分高 | 脚本校验维度总分与细项均值，背离过大时拒绝合并。 |
| 结构化信号和语义判断冲突 | 脚本保留最终融合，但写入复核提示，要求回看样本和证据。 |
| LLM 偏好漂亮文风 | 评分细则优先看 groundedness、traceability、answer faithfulness，不把文风当核心价值。 |
| 自动生成关系块抬高来源分 | 统计前剥离 `CORE_*` 自动生成块，只让正文来源链接计入来源支撑。 |
| 同名文件导致链接误判 | Wiki 链接解析保留歧义状态，不把同名覆盖当作已解决链接。 |

## 权重说明

当前权重是工程初始权重：

| 维度 | 权重 | 理由 |
|---|---:|---|
| `knowledge_sedimentation_effectiveness` | 25% | wiki 沉淀是最终价值产物。 |
| `llm_wiki_architecture_fit` | 20% | 架构决定是否能持续复利。 |
| `source_traceability` | 20% | 来源链决定可信度。 |
| `schema_governance_quality` | 15% | Schema 决定 agent 行为稳定性。 |
| `retrieval_answerability` | 10% | 查询效果重要，但部分受工具和问题集影响。 |
| `maintenance_evolution` | 10% | 维护是长期护栏，需随使用数据校准。 |

建议后续校准数据：

- 抽样问题回答正确率。
- 答案来源引用正确率。
- 从问题到答案的时间。
- wiki 页面被复用次数。
- 新资料进入 raw 后完成沉淀的周期。
- 用户对回答有用性的人工评分。

## 参考来源

- Andrej Karpathy, "LLM Wiki": https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f
- Huan Ying Teah, Loo Geok Pee, Atreyi Kankanhalli, "Development and Application of a General Knowledge Management Maturity Model": https://aisel.aisnet.org/pacis2006/12/
- CMMI Institute, "Capability & Maturity Levels": https://cmmiinstitute.com/learning/appraisals/levels
- William H. DeLone, Ephraim R. McLean, "The DeLone and McLean Model of Information Systems Success: A Ten-Year Update": https://www.tandfonline.com/doi/abs/10.1080/07421222.2003.11045748
- Richard Y. Wang, Diane M. Strong, "Beyond Accuracy: What Data Quality Means to Data Consumers": https://www.tandfonline.com/doi/abs/10.1080/07421222.1996.11518099
- ISO/IEC 25012:2008, Software engineering -- Software product Quality Requirements and Evaluation (SQuaRE) -- Data quality model: https://www.iso.org/standard/35736.html
- W3C, "PROV-O: The PROV Ontology": https://www.w3.org/TR/prov-o/
- ISO/IEC/IEEE 29148:2018, Systems and software engineering -- Life cycle processes -- Requirements engineering: https://www.iso.org/standard/72089.html
- Alexander R. Fabbri et al., "SummEval: Re-evaluating Summarization Evaluation": https://arxiv.org/abs/2007.12626
- Shahul Es et al., "RAGAS: Automated Evaluation of Retrieval Augmented Generation": https://arxiv.org/abs/2309.15217
- Saad-Falcon et al., "ARES: An Automated Evaluation Framework for Retrieval-Augmented Generation Systems": https://arxiv.org/abs/2311.09476
- Yang Liu et al., "G-Eval: NLG Evaluation using GPT-4 with Better Human Alignment": https://aclanthology.org/2023.emnlp-main.153/
- Seungone Kim et al., "Prometheus: Inducing Fine-grained Evaluation Capability in Language Models": https://arxiv.org/abs/2310.08491
- Jiawei Gu et al., "A Survey on LLM-as-a-Judge": https://arxiv.org/abs/2411.15594
