# Paper Defense Q&A + Code/Training Audit Skill v1.1.0

这是一个面向计算机类论文答辩、组会汇报、论文精读讨论、审稿式问答和会议 rebuttal 演练的 skill。

它的上游推荐输入是 `paper_deep_reading_teaching_explainer_v10` 生成的权威深读报告；它的下游产物是一个围绕论文、代码仓库、训练过程和实验证据的答辩问答包。

## 这个 skill 解决什么问题

很多论文汇报准备只会生成“可能被问到的问题”，但没有真正区分：

- 哪些回答有论文证据；
- 哪些回答只有代码证据；
- 哪些回答需要训练日志或配置支持；
- 哪些回答其实不能防守，只能诚实承认局限；
- 哪些问题需要提前做备份页。

本 skill 的核心是把答辩准备变成：

```text
论文主张 -> 证据 -> 攻击面 -> 问题 -> 可防守回答 -> 备份材料
```

## 推荐输入

- v10 深读报告：`*_detailed_cn.md`
- 论文 PDF / supplement / appendix
- OpenReview 评审与 rebuttal 摘要
- 官方或复现代码仓库
- 训练脚本、评估脚本、配置文件、日志、checkpoint、seed、硬件信息
- PPT 草稿或 slide blueprint
- 可选视觉风格：学术信息图、黑板讲解、漫画分镜、PPT 扁平插图

## 主要输出

```text
generated/defense/<paper-slug>/defense_scope_cn.md
generated/defense/<paper-slug>/claim_evidence_map_cn.md
generated/defense/<paper-slug>/paper_attack_surface_cn.md
generated/defense/<paper-slug>/code_training_audit_cn.md
generated/defense/<paper-slug>/defense_qa_bank_cn.md
generated/defense/<paper-slug>/defense_qa_bank_cn.json
generated/defense/<paper-slug>/answer_playbook_cn.md
generated/defense/<paper-slug>/mock_defense_script_cn.md
generated/defense/<paper-slug>/backup_slide_plan_cn.md
generated/defense/<paper-slug>/evidence_gap_triage_cn.md
generated/defense/<paper-slug>/visual_qa_storyboard_cn.md
generated/defense/<paper-slug>/visual_qa_storyboard_cn.json
generated/defense/<paper-slug>/visual_image_prompt_pack_cn.md
generated/defense/<paper-slug>/visual_generation_handoff_cn.md
generated/defense/<paper-slug>/visual_card_copy_cn.md
```


## 图文答辩卡片与生图提示词 🎨

本版本新增一个独立的 visual mode，用于把高风险答辩问题做成更直观的系列图解：

- 核心贡献地图：说明 novelty 能防守到哪里；
- 方法流水线：解释模型、数据流、训练/推理差异；
- Claim-Evidence Map：把回答绑定到论文表格、代码和日志证据；
- Equation-to-Code Bridge：把公式、模块和代码路径连起来；
- Training Timeline：解释 seed、checkpoint、超参、compute；
- Baseline Fairness Board：展示 baseline 是否公平；
- Limitation Boundary：明确什么不能过度声称；
- Recovery Answer Card：准备被追问时的保守回答。

### 文字和生图必须分开

本 skill 先生成文字版问答、证据边界、storyboard 和 image prompts。每次文本回复末尾都要附加下面这句作为后续生图提示；后续用户可以单独使用这句请求生图：

```text
请用chatgpt images 2.0 生成一系列 16:9 辅助答辩的插图，这些插图可以图文并茂的覆盖上面文字中的问题以及用生动的图表来解释回答，有助于更好准备答辩回答。
```

Codex / CLI 中则应把 `visual_qa_storyboard_cn.json` 当成生图任务清单；如果在 Codex 内使用，优先调用 `imagegen` skill 生图，否则交给 ChatGPT Images 2.0 / `gpt-image-2` 或用户批准的高级文生图 API。不要把回答生成和生图调用混在同一步。

## 主要特性

- 论文层面：贡献、创新性、相关工作、方法、公式、理论、实验、消融、局限性。
- 代码层面：仓库入口、依赖、数据处理、模型实现、loss、评估指标、baseline 复现。
- 训练层面：优化器、学习率、batch size、seed、checkpoint、超参搜索、compute、失败运行。
- 答辩层面：短回答、长回答、证据引用、不能过度声称的点、追问后的回应。
- 风险层面：P0/P1 高危问题、证据缺口、备份页建议。
- 视觉层面：图文答辩卡片、视觉 storyboard、生图提示词、ChatGPT 网页版 / Codex / API 分离式生图流程。

## 本 skill 与 v10 的关系

v10 负责“把论文读懂、讲清楚、形成权威深读报告”；本 skill 负责“把这份理解转换成答辩时能承受追问的问答、代码/训练审计和备份材料”。

不要用本 skill 替代深读。没有 v10 报告时，本 skill 仍可工作，但需要标注证据不足。

## 脚本

- `scripts/init_paper_defense_qa_scaffold.py`：初始化答辩包目录。
- `scripts/validate_defense_qa_bundle.py`：检查关键文件和 JSON 结构。
- `scripts/build_defense_qa_bundle.py`：将答辩包打成 zip。
- `scripts/generate_visual_qa_prompt_pack.py`：从 Q&A JSON 生成视觉 storyboard 和生图提示词。
- `scripts/package_clawhub_skill.py`：检查 ClawHub 基本要求并打包为 `.zip` 和 `.skill`。


## 版本确认

- `SKILL.md` frontmatter: `version: 1.1.0`
- `_meta.json`: `version: 1.1.0`
- 发布 / 上传时请使用 `paper-defense-qa-code-training-v1.1.0-clawhub.zip` 或 `paper-defense-qa-code-training-v1.1.0.skill`。
