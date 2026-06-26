# Changes

## v10.1.8 - Remove next-skill footer and clarify cartoon prompt wording

- Removes the fixed next-skill recommendation footer from substantive replies.
- Keeps `Current Status` and `Possible User Inputs For Next Stage` as the default handoff structure.
- Updates visual-step prompt examples so users are explicitly told to say `生成多张连续的卡通图` when they want continuous cartoon generation.
- Updates stateless recovery wording for cartoon-image continuation.

## v10.1.7 - Multi-image decomposition instead of one crowded image

- Adds a hard rule that every requested visual part should be generated as multiple continuous 16:9 cartoon images by default.
- Requires one prompt per image and one main teaching point per image.
- Explicitly prevents compressing background, algorithm, experiments, limitations, and future directions into one dense all-in-one picture.
- Adds a decomposition field to the continuity/cinematography prompt block so each image states what it explains and what adjacent ideas are left to other images.
- Keeps single-image output only as an explicitly requested compact overview, not the recommended teaching mode.

## v10.1.6 - Visual source-grounding anti-hallucination check

- Adds a mandatory source-grounding check before writing image prompts or directly generating cartoon storyboard images.
- Requires every paper-specific visual fact to trace back to the original PDF/LaTeX or to the authoritative deep-reading report, with the original paper taking priority when conflicts appear.
- Requires text prompt handoffs to include a compact anti-hallucination checklist: original paper checked, authoritative report checked, unsupported facts removed/marked not reported, and conflicts flagged.
- Requires generated images to be inspected before PDF assembly. Images with invented numbers, wrong module names, unsupported claims, wrong arrows, or unreported details drawn as facts must be revised or regenerated.
- Adds `schemas/visual_source_grounding_anti_hallucination_overlay.md`.

## v10.1.5 - Continuous cartoon storyboard continuity and cinematography

- Adds a continuity/cinematography rule for every text answer that writes image-generation prompts and every direct multi-image cartoon generation step.
- Requires each continuous cartoon batch to specify image order, camera/framing, transition logic, style bible, narrator/character consistency, symbol dictionary, color/typography continuity, and narrative relation across images.
- Requires follow-up batches to continue the established storyboard bible from previous images unless the user explicitly asks for a reset.
- Adds `schemas/cartoon_storyboard_continuity_quality_overlay.md` with extra checks for teaching suitability: one main idea per image, readable labels, stable data-flow direction, evidence honesty, experiment clarity, accessibility, and PDF-safe margins.

## v10.1.4 - 增强复现、答辩和教学质量要求

- 新增复现/答辩/教学质量 overlay，避免泛泛总结，要求报告达到能复现、能答辩、能讲给别人听的深度。
- 要求所有关键概念按 `直觉 -> 数学公式 -> 具体例子 -> 局限` 讲解。
- 要求复杂模块说明输入、输出、符号、维度、可训练参数、固定超参数和数据流。
- 要求严格区分论文明确写的、论文没写但可由本文合理推测的、参考相近工作推测的内容。
- 要求实验部分细化数据集规模、标签定义、划分协议、baseline 来源、是否重跑/重构、指标含义、例外结果和复现风险。
- 要求明确列出硬件、耗时、超参数、baseline 来源、数据划分、seed、预处理等缺失细节，不得编造。
- 要求加入一个完整的小数字例子，串联训练和推理。
- 要求讲解顺序遵守知识依赖：符号 -> 数据/输入 -> 模型/模块 -> 训练/推理 -> 实验/不足。
- 同步增强分阶段卡通图 workflow，要求漫画展示数据流、证据状态、缺失实验细节和小数字例子，而不是只做高层概念图。

## v10.1.3 - 移除 ClawHub 上传包中的 `.clawhubignore` 和 `LICENSE`

- 修复 ClawHub 提交 v10.1.2 时的校验报错：`Remove non-text files: .clawhubignore, LICENSE`。
- 发布 zip 不再包含 `.clawhubignore` 和 `LICENSE`，避免 ClawHub 将无扩展名文件或 dotfile 判为 non-text。
- MIT-0 授权信息仍保留在元数据、README 和发布说明中。
- 不改变 skill 主流程、分阶段卡通图生成规则或 imagegen 优先规则。

## v10.1.2 - Codex 生图优先使用 imagegen skill

- 确认 v10.1.1 已经说明 Codex / Claude Code / coding-agent 环境可以使用 ChatGPT Images 2.0 API 或其他可用生图 API。
- 补充 Codex 类环境的优先级：若 `imagegen` skill 可用，生图阶段应优先使用 `imagegen` skill。
- 仅当 `imagegen` 不可用或能力不足时，再回退到 ChatGPT Images 2.0 API 或其他用户批准的生图 API。
- 保留原约束：文字报告和生图分离，不用 SVG 替代卡通漫画分镜。

## v10.1.1 - 明确生图可基于 PDF / LaTeX / PDF+LaTeX

- 明确 storyboard 生图阶段可以基于上传 PDF、LaTeX 源码，或二者结合。
- 规定 PDF 用于 rendered pages、可见图表、caption、坐标轴与表格数值等视觉证据。
- 规定 LaTeX 用于 figure/table 环境、caption、label、includegraphics 路径、公式、正文引用与附录内容。
- 若 PDF 与 LaTeX 同时存在，要求交叉核对；冲突或缺失时不得编造，应在文字状态中说明或标记“未报告”。


## v10.1.0 - ClawHub packaging + final storyboard PDF assembly

- 将 skill 封装为 ClawHub/OpenClaw 友好的目录结构与元数据。
- 为 `SKILL.md` 添加 YAML frontmatter：name、description、version、metadata.openclaw。
- 新增 MIT-0 `LICENSE`、`.clawhubignore`、`_meta.json`、`PUBLISHING_CLAWHUB.md`、`PUBLISH_PAGE_INFO_CN.md`、`SECURITY_PRIVACY.md`。
- 新增最终步骤：把所有已生成、已确认的连续卡通图按顺序合成为一个 16:9 PDF。
- 新增 `workflow/09_storyboard_pdf_assembly.md` 和 `scripts/assemble_storyboard_pdf.py`。
- 明确要求：完整精读报告、图片生成、最终 PDF 合成分属不同阶段，不能在同一次回答中混合报告生成与生图。
- 明确平台说明：ChatGPT 网页版 / App 用 Create image；Codex / Claude Code 等优先使用 `imagegen` skill，必要时回退到 ChatGPT Images 2.0 API 或其他可用生图 API；不要用 SVG 替代卡通漫画分镜。

## Previous local visual-step update

- 新增分阶段卡通图生成 workflow：背景/旧方法缺陷、算法流程、实验部分、局限性与答辩、未来方向、封面总结等。
- 新增无状态恢复提示，要求每次状态回复提醒用户如何继续。

# v10：新增 Teaching-Explainer 讲解增强层，目标是把精读结果讲给别人听

- 在不削弱 v9 Research-Generative 与原始 deep-read 要求的前提下，新增 `Teaching-Explainer Paper Reading` 强制 overlay。
- 保留原有输入契约、公式保留、证明-实现映射、图表解释、审稿视角、OpenReview 处理、结构化附录、校验与交接规则；讲解层只增加约束，不替代原报告。
- 新增讲解主线：`Before -> Pain -> Broken Assumption -> Key Replacement -> Mechanism -> Evidence -> Caveat -> Next Idea`。
- 新增 11 个必填讲解章节：受众画像、30秒/3分钟/10分钟摘要、Story Spine、先修知识、公式/图表/实验讲解脚本、板书推导、小例子、角色扮演讨论、Q&A、易误解点、PPT/分享稿草案、三句带走信息。
- 引入公开最佳实践作为方法灵感：Keshav 三遍读论文法、Jacobson/Raffel 角色扮演式论文研讨、Stanford CS324 论文讨论角色、MIT EECS Communication Lab 的 problem/motivation/solution/contribution 叙事框架、AISTATS/ICLR 审稿与可复现性关注点、GitHub/ClawHub 上的 paper-reading / paper-review skill 结构。
- 新增 `schemas/teaching_explanation_overlay.md`、`schemas/teaching_explanation_spec.template.json`、`schemas/external_best_practices_sources.md`、`workflow/06_teaching_explainer_preparation.md`、`workflow/07_talk_qa_rehearsal.md`。
- 更新 `schemas/detailed_report_contract.md`、`schemas/detailed_report_required_sections.json`、`schemas/paper_focus_spec.template.json`、`scripts/init_paper_deep_reading_scaffold.py`、`schemas/per_paper_output_layout.md`、`schemas/sources_zip_layout.md` 与交付 manifest，支持可选的讲解衍生 sidecar。
- 明确：`generated/teaching/` 下的讲解、PPT、Q&A、角色扮演材料只是权威详细报告的衍生物，不能替代 `*_detailed_cn.md`。

# v9：融合 Research-Generative Paper Reading，用精读反推新 idea

- 将 `research_generative_paper_reading_skill.md` 的核心内容融入 `paper_deep_reading_skill`，作为强制 research-generative overlay，而不是替代原 deep-read 要求。
- 新增“非弱化规则”：不得删除或弱化原 skill 的输入契约、公式保留、证明-实现映射、图表解释、审稿视角、结构化附录、校验与交接要求；若与新 overlay 发生张力，以最有利于寻找新 idea 的解释为准。
- 新增 research equation：`Important Setting + Broken Assumption + Borrowed Tool + New Constraint + Surrogate Mechanism`，要求识别不可用理想机制 `Y` 与替代机制 `Z`。
- 新增作者侧方向发现重建、故事线搭建、模块级作者思路深读、Citation-to-Module Map、experiments-as-story-evidence、可复用论文造故事模式、隐藏假设到新 idea 转换等强制报告章节。
- 更新 `schemas/detailed_report_contract.md`、`schemas/detailed_report_required_sections.json`、`schemas/extended_deepread_checklist_cn.md`、`schemas/paper_focus_spec.template.json`、`schemas/motivation_bridge_analysis.md`、`workflow/02_extract_structure.md`、`workflow/04_gap_mining_and_graph.md`、`workflow/05_extended_argument_and_innovation_audit.md` 与相关脚本。
- 新增 `schemas/research_generative_overlay.md`，保留并改写 research-generative 方法论，作为配套规则文档。
- 清理 `__pycache__`，避免把运行缓存放进发布包。

# v8

- 新增“作者主观关联”要求：在介绍 idea、理论证明、具体算法或模块时，若设计与作者的主观判断、经验偏好、研究风格或工程取舍有关，必须显式说明，并区分客观必要性与作者选择。
- 新增“贴近论文具体内容”要求：禁止过于空泛抽象的总结，必须结合论文中的具体公式、模块、图表、数据、实验现象与原文措辞展开。

# 增强版变更说明

本增强版在原始 `chatgpt_paper_deep_reading_skill_source` 基础上，做了以下更新：

- 在 `SKILL.md` 中加入“扩展精读规则”，把标题解读、创新主张审计、实验谱系映射、创新类型判断、边界突破判断、新方向推测等变成显式要求。
- 明确“精读报告长度不受限制”，优先完整性。
- 更新 `schemas/detailed_report_contract.md`，把新增章节写入强制章节顺序。
- 更新 `schemas/detailed_report_required_sections.json`，让结构校验脚本也能检查新增标题。
- 更新 `scripts/init_paper_deep_reading_scaffold.py`，让初始化出来的报告模板直接包含新增章节。
- 新增 `schemas/extended_deepread_checklist_cn.md` 作为人工复核清单。
- 新增 `schemas/claim_support_audit.template.json` 作为“主张-证据审计表”模板。
- 新增 `workflow/05_extended_argument_and_innovation_audit.md` 作为二次审查步骤。

- 进一步强化“论文不足 / 未解决问题 / 结构性局限”的显式讨论要求。
- 进一步强化“哪些未来方向只是工程延展，哪些方向可能推动科学边界”的区分要求。

- 新增“公式保留与逐式解释”硬性要求：精读报告不得省略关键公式，必须逐式解释公式项、作用和对应算法位置。
- 新增“理论、证明与实现步骤对照”硬性要求：如果论文含有理论分析或证明，必须解释其意义，并明确理论对象与实际实现是严格一致、局部近似还是仅提供动机。
- 更新 `schemas/extended_deepread_checklist_cn.md`、`schemas/detailed_report_required_sections.json` 与 `scripts/init_paper_deep_reading_scaffold.py`，确保这些要求进入结构校验和初始化模板。

- 新增“具体公式、模块与设计假设的不足及可改进空间”硬性要求：不能只评价整篇论文，必须细到关键公式、关键模块与关键假设，判断其脆弱点、欠论证之处、优化与效率问题，以及可替代设计与 trade-off。
- 同步更新 `SKILL.md`、`schemas/detailed_report_contract.md`、`schemas/detailed_report_required_sections.json`、`schemas/extended_deepread_checklist_cn.md` 与 `scripts/init_paper_deep_reading_scaffold.py`，确保这项细粒度审计进入章节顺序、检查清单和初始化模板。

## v6：引入 GitHub 热门审稿 skill 的 reviewer 关注点，并增强图表一致性审计

- 新增“额外审稿视角审计（借鉴 GitHub 热门审稿 skill 的 reviewer 关注点）”主章节。
- 将 novelty、significance、technical soundness、methodology rigor、reproducibility、results-claims alignment、missing baselines/controls、figure/table clarity、limitations honesty 等列为强制审计维度。
- 明确：如果存在 LaTeX 源，必须基于 figure 环境、caption、label、正文引用来解释关键图，不能因为不是 PDF 就跳过。
- 明确：实验部分必须解释关键表格、曲线、图像和数字比较，指出它们支撑哪个主张，是否与主张一致，以及可能的不一致原因。
- 扩展结构化附录中的 visual / experiment 审计项，加入 figure-to-claim mapping、table/chart/data-to-claim mapping、possible causes of mismatch。

## v7：PDF 图解释与实验图表-主张一致性审计进一步强化

- 明确：不仅 LaTeX 源中的图要解释，PDF 版本中的关键图（结构图、流程图、定性图、实验曲线图等）也必须显式解释，不能只看正文和公式。
- 在 `workflow/03_figure_and_table_analysis.md` 中补充 PDF 图解释要求，并要求分析图的视觉结构、图到主张的映射、可能的歧义与误导。
- 在 `schemas/detailed_report_required_sections.json` 中为“核心方法到底在干什么”和“实验是如何被设计出来的”加入关键图解释、图表/数据到主张映射、不一致原因分析等必填项。
- 在 `scripts/init_paper_deep_reading_scaffold.py` 的中文报告模板里加入“关键结构图 / 流程图 / 定性图解释”和“图表坐标轴、图例、比较条件解释”等字段。
- 进一步强化实验图表与作者主张之间的一致性审计：必须指出哪些图表强支持、部分支持或不支持主张，并分析原因。

## v10 visual-step update — staged cartoon storyboard workflow

- 增加“分阶段卡通图生成”规则：首次启动 skill 只输出 plan、完整精读报告、当前状态和下一步提问方式，严禁同轮生图。
- 增加 Step 1+ 的可选后续流程：背景/旧方法缺陷、算法模块、实验部分、局限答辩、未来方向、封面总结等连续卡通图。
- 增加无状态提醒：用户应使用“使用这个skill，根据状态，执行第X步：...”来恢复或推进流程。
- 增加生图平台说明：ChatGPT 网页版/App 使用 Create image；Codex/Claude Code 等优先使用 `imagegen` skill，必要时回退到 ChatGPT Images 2.0 API 或其他可用生图 API；不生成 SVG 图替代卡通分镜。
- 增加硬性约束：文字报告和图片生成不能在同一次回答中同时给出。
