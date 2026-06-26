# 图文答辩卡片与生图提示词风格指南

## 目标

把论文答辩中的高风险问题转化为直观图解：问题、可防守回答、证据、边界、追问后的回应。视觉图不是装饰，而是帮助听众理解“这篇论文到底证明了什么、没证明什么”。

## 必须遵守

1. **先文字，后生图**：先完成 Q&A、证据标签、回答边界和图像提示词；只有用户单独要求时才进入生图。
2. **问题绑定**：每张图必须绑定 `Q_ID`，不能做无来源的泛泛插图。
3. **证据标签可见**：至少体现 `paper_grounded`、`code_grounded`、`experiment_log_grounded`、`missing_evidence` 等关键标签之一。
4. **安全边界明确**：每张图都要说明“不能过度声称什么”。
5. **一致风格**：同一篇论文的系列图保持一致的画幅、图标体系、线条粗细和术语。

## 推荐系列顺序

| 顺序 | 图类型 | 适合问题 |
|---|---|---|
| 1 | 核心贡献地图 | 论文贡献、novelty、closest prior work |
| 2 | 方法流水线 | 架构、算法流程、训练/推理差异 |
| 3 | Claim-Evidence Map | “证据在哪里？”、“哪张表支持这个结论？” |
| 4 | Equation-to-Code Bridge | 公式到代码实现是否一致 |
| 5 | Training Timeline | 训练流程、seed、checkpoint、compute |
| 6 | Baseline Fairness Board | baseline 是否公平、调参预算是否一致 |
| 7 | Limitation Boundary | 局限性、失败模式、不能过度声称 |
| 8 | Recovery Answer Card | 被追问时的保守回答模板 |

## 图像提示词模板

```text
Create a clean academic 16:9 infographic for a computer-science paper defense.
Purpose: [explain the defense question visually].
Main layout: [pipeline / map / radar / timeline / card].
Show: [question, claim, evidence, boundary, follow-up].
Style: calm, professional, PPT-friendly, high readability, minimal clutter.
Text policy: keep labels short; leave blank areas for exact paper-specific text overlays.
Avoid: fake citations, unreadable tiny text, exaggerated claims, decorative elements unrelated to the defense.
```

## ChatGPT 网页版使用提示

完成文字包或任意文本回复后，最后都要附加这句继续请求生图：

```text
请用chatgpt images 2.0 生成一系列 16:9 辅助答辩的插图，这些插图可以图文并茂的覆盖上面文字中的问题以及用生动的图表来解释回答，有助于更好准备答辩回答。
```


## Codex / CLI / API 使用提示

- 把 `visual_qa_storyboard_cn.json` 当成生图任务清单。
- 把 `visual_image_prompt_pack_cn.md` 当成可复制的 prompt 列表。
- 在 Codex 内实际生图时，优先调用 `imagegen` skill。
- 非 Codex 场景使用 ChatGPT Images 2.0 / `gpt-image-2` 或用户批准的高级文生图 API。
- 不要把回答生成和 API 生图混在一个步骤中。
- 生图后再把准确文本、公式、代码路径叠加到 PPT 或 SVG 中。
