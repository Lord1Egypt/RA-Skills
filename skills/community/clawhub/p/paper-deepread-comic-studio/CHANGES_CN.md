# 更新记录

## v1.2.0 - 精读质量与连续多图生图增强版

- 将技能包版本统一为 `v1.2.0`（ClawHub/semver 字段使用 `1.2.0`）。
- 强化精读报告标准：避免泛泛总结，要求解释到可复现、可答辩、可讲给别人听。
- 新增关键概念讲解顺序：`直觉 -> 数学公式或 formal definition -> 具体例子 -> 局限 / failure case`。
- 新增复杂模块细节要求：输入、输出、符号、维度、训练参数、固定超参、训练数据流、推理数据流都要说明。
- 强制区分证据层级：论文明确写明、论文没写但合理推测、参考相近工作推测、缺失 / 未报告。
- 强化实验部分：数据集规模、标签定义、baseline 来源与是否重跑/重构、指标含义、结果例外、消融逻辑和复现风险都要写清楚。
- 要求最后给出完整数字例子，把训练和推理串起来；若只能做 toy simplification，必须明确标注。
- 强化连续卡通图生图提示：每次连续生图必须写明“生成多张连续的卡通图”，考虑运镜、风格一致性、逻辑连续性、前后批次一致性和证据核对。
- 明确不同论文部分必须拆成多张或多批图片，不得压缩合并到一张图中。
- 移除回答页脚中的 `Recommended Next Skill`，只保留状态和下一步用户输入建议。

## v1.1.0 - ClawHub/MIT-0 发布版

### 命名更新

- 技能展示名更新为 `Paper DeepRead Comic Studio`。
- 中文宣传名更新为 `论文精读漫画工坊`。
- Skill slug 更新为 `paper-deepread-comic-studio`。


### ClawHub validation fix

- 移除 `.clawhubignore` 与无扩展名 `LICENSE` 文件，避免 ClawHub 将其判定为 non-text files。
- MIT-0 许可仍在 `SKILL.md` frontmatter、`README.md`、`_meta.json` 与发布页信息中声明。
- 补充 Codex 类环境的生图优先级：若 `imagegen` skill 可用，生图阶段应优先使用 `imagegen` skill；仅当 `imagegen` 不可用或能力不足时，再回退到 ChatGPT Images 2.0 API 或其他用户批准的生图 API。

- 将技能包版本统一为 `v1.1.0`（ClawHub/semver 字段使用 `1.1.0`）。
- 保留完整论文精读、研究生成、教学讲解、答辩准备能力。
- 固化分阶段卡通漫画 storyboard 工作流：首次启动只输出 plan + 完整精读报告，不能生图；后续步骤逐段生成统一风格、连续逻辑的卡通图。
- 明确文字报告与生图不能在同一次回答中混合。
- 明确生图可基于 PDF、LaTeX 源码，或 PDF + LaTeX 交叉核对。
- 明确平台使用方式：ChatGPT 网页版/App 使用 Create image；Codex/Claude Code 等环境优先使用 `imagegen` skill，必要时回退到 ChatGPT Images 2.0 API 或其他可用生图 API；不使用 SVG 替代卡通漫画分镜。
- 新增最终步骤：将所有已确认图像合成为 16:9 PDF。
- 完成 ClawHub 封装：`SKILL.md` YAML frontmatter、`_meta.json`、发布页信息与安全隐私说明；移除无扩展名辅助文件以通过 ClawHub 文本文件校验。
- License: MIT-0。
