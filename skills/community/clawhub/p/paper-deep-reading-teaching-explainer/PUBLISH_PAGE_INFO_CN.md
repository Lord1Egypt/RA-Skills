# ClawHub 发布页信息：paper-deep-reading-teaching-explainer v10.1.8

| Field | Value |
|---|---|
| Name / Slug | `paper-deep-reading-teaching-explainer` |
| Display name | Paper Deep Reading Teaching Explainer |
| Version | `10.1.8` |
| License | `MIT-0` |
| Emoji | 📚 |
| Category | Research / Education / Paper Reading / Visualization |
| Primary metadata source | `SKILL.md` YAML frontmatter |

## 一句话简介

把论文精读变成完整的中文权威报告、教学讲解材料、研究方向挖掘结果，以及分阶段统一风格卡通图与最终图片 PDF 合成流程。

## Short description / Summary

Deep-read research papers into authoritative teaching reports, innovation-mining artifacts, staged cartoon storyboard image workflows, and final 16:9 image-PDF assembly guidance.

## 适用场景

- 论文精读、组会汇报、课程讲解、答辩准备；
- 从论文中挖掘新研究方向和创新点；
- 把论文内容拆成连续、统一风格、逻辑清晰的卡通漫画式分镜；
- 将所有生成图最终合成为一个 PDF handoff。

## 核心功能

1. 首次启动时先给 plan，然后只生成完整精读报告；这一步不生图。
2. 报告后提供状态、产出和下一步可用提问方式。
3. 后续按阶段生成统一风格的连续卡通图：背景/缺陷、算法、实验、局限、未来方向、封面/总结等。
4. 生图阶段可以基于 PDF、LaTeX 源码，或二者结合；PDF 用于渲染视觉证据，LaTeX 用于精确 caption、label、公式、figure 路径和上下文。
5. 最后单独执行 PDF 合成步骤，把所有图按顺序合成为一个 16:9 PDF。
6. 每次状态回复都提醒用户如何在无状态会话中继续.

## 用户触发示例

```text
请使用这个skill精读这篇论文，直接显示完整报告。
```

```text
使用这个skill，根据状态，执行第1步：生成背景、旧方法缺陷、问题与灵感来源的连续卡通图。
```

```text
使用这个skill，根据状态，执行第2步：生成算法整体流程与各模块解释的连续卡通图。
```

```text
使用这个skill，根据状态，执行第3步：生成实验部分的连续卡通图。
```

```text
使用这个skill，根据状态，执行最后一步：把所有已经生成的图合成一个PDF。
```

```text
使用这个skill，根据状态，告知下一步应该问什么。
```

## 生图平台说明

- ChatGPT 网页版 / App：使用 Create image。
- Codex / Claude Code / coding-agent 环境：优先使用 `imagegen` skill；如果不可用或能力不足，再使用 ChatGPT Images 2.0 API 或其他用户批准的生图 API。
- 不要用 SVG 图替代用户要求的卡通漫画分镜。
- 文字报告和生图不能在同一次回答里混合。
- 生图可以基于 PDF 或 LaTeX 源码；若二者同时存在，应交叉核对。

## v10.1.3 上传包说明

- ClawHub 上传包不再包含 `.clawhubignore` 和 `LICENSE`，避免被 ClawHub non-text-file 校验拒绝。
- MIT-0 授权信息仍保留在元数据与 README 中。

## v10.1.4 质量增强说明

- 报告和卡通图都必须达到能复现、能答辩、能讲给别人听的深度。
- 关键概念按 `直觉 -> 数学公式 -> 具体例子 -> 局限` 讲。
- 复杂模块必须交代输入、输出、符号、维度、参数和数据流。
- 实验部分必须细化数据集、标签、baseline、指标、例外结果和复现风险。
- 缺失的硬件、耗时、超参数、数据划分等信息要明确写“未报告”，不得编造。

## 最终 PDF 说明

最终 PDF 合成阶段只处理已经生成、已确认的图片，不再生成新图。推荐输出：

```text
paper_storyboard_all_images.pdf
paper_storyboard_images_and_pdf.zip
```

## v10.1.8 reply and next-prompt note

- Removes the fixed next-skill recommendation footer requirement.
- Status replies should focus on current status and possible user inputs for the next stage.
- When suggesting a cartoon-generation command, explicitly tell the user to say `生成多张连续的卡通图`.

## v10.1.7 multi-image decomposition note

- Each requested visual part should be generated as several continuous 16:9 cartoon images by default.
- Each image should have one main teaching point and one prompt; dense sections should be split rather than merged.
- Background, algorithm, experiments, limitations, and future directions should not be compressed into one all-in-one picture.
- A single image is treated only as an explicitly requested compact overview, not the recommended teaching output.

## v10.1.6 visual source-grounding anti-hallucination note

- Before writing image prompts or generating cartoon storyboard images, the assistant must check the prompt against the original PDF/LaTeX and the authoritative deep-reading report.
- Unsupported facts must be removed, marked `not reported` / `未报告`, or sent back to the user for missing evidence.
- If the report conflicts with the original paper, the original paper has priority and the conflict should be flagged.
- Generated images must be inspected before PDF assembly; images with invented numbers, wrong module names, unsupported claims, wrong arrows, or unreported details drawn as facts must be revised or regenerated.

## v10.1.5 continuity / cinematography quality note

- Every text answer that writes prompts for multiple continuous cartoon images must include a continuity/cinematography block.
- Prompt batches should specify image order, shot/framing, camera movement, transition logic, style bible, symbol bible, and how each image connects to the previous and next image.
- Later storyboard batches must preserve the established protagonist, palette, typography, visual metaphors, data-flow direction, evidence labels, and page numbering unless the user explicitly asks for a reset.
- Prompts should optimize teaching expression: one core idea per image, readable labels, stable data flow, clear evidence status, experiment clarity, accessibility, and PDF-safe margins.

## Tags

`paper-reading`, `research`, `education`, `teaching`, `visual-storyboard`, `cartoon-infographic`, `image-prompt`, `pdf-assembly`, `deep-reading`, `clawhub`, `mit-0`

## Release notes

v10.1.5 adds continuity and cinematography controls for multi-image cartoon prompt batches while keeping the v10.1.4 reproducibility / defense / teaching-quality requirements.

v10.1.6 adds source-grounding anti-hallucination checks for storyboard image prompts and generated images.

v10.1.7 adds a multi-image decomposition rule so each visual section is split into readable continuous images instead of one dense collage.

v10.1.8 removes the fixed next-skill recommendation footer and clarifies that cartoon-generation next prompts should say `生成多张连续的卡通图`.

v10.1.4 在 v10.1.3 的 ClawHub 上传包修复基础上，新增复现、答辩和教学质量增强规则，强化报告和分阶段卡通图的具体性、证据分层、实验审计和完整数字例子。
