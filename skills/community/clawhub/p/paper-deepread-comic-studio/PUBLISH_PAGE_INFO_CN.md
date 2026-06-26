# ClawHub 发布页信息：Paper DeepRead Comic Studio v1.2.0

| 字段 | 内容 |
|---|---|
| Slug | `paper-deepread-comic-studio` |
| Display name | `Paper DeepRead Comic Studio` |
| 中文名 | `论文精读漫画工坊` |
| Version | `v1.2.0` |
| ClawHub semver | `1.2.0` |
| License | `MIT-0` |
| Emoji | 📚🎨 |
| Category | Research / Education / Paper Reading / Cartoon Storyboard / Presentation Visuals |

## 一句话简介

精读论文到可复现、可答辩、可讲解的程度，并将论文背景、方法、实验、局限与未来方向转化为统一风格、运镜连续、证据可追溯的多张卡通分镜图，最后可合成为 16:9 PDF。

## 适合谁使用

- 需要精读论文并准备汇报、答辩、组会或课程讲解的研究者。
- 需要将论文方法、实验、局限和未来方向做成可视化分镜的人。
- 需要把 PDF / LaTeX 中的公式、图表、实验和叙事整理为教学材料的人。

## 核心能力

1. **完整论文精读报告**：先给 plan，再直接显示完整精读报告；关键概念按“直觉 -> 公式 -> 例子 -> 局限”解释。
2. **研究生成分析**：抽取问题、动机、隐藏假设、缺口和可追方向。
3. **教学讲解转化**：输出适合讲给别人听的故事线、公式讲法、图表讲法、Q&A。
4. **分阶段多张连续卡通图生成工作流**：背景缺陷、算法流程、实验部分、局限答辩、未来方向等分步生成，不能压缩合并到一张图里。
5. **PDF/LaTeX 证据对齐**：生图可基于 PDF、LaTeX 源码或二者交叉核对。
6. **最终图像 PDF 合成**：将确认后的连续分镜图按顺序合成为一个 16:9 PDF。

## 重要工作流约束

- 启动 skill 后，第一步只生成文字：plan + 完整精读报告 + 当前状态 + 下一步提问建议，**不能生图**。
- 文字报告和生图不能在同一次回答中混合。
- 生图步骤应分阶段进行，每次只生成一个部分，并拆成多张连续 16:9 卡通图。
- 文本里的生图提示必须考虑运镜、风格一致、逻辑连续、与前面已生成图片的设定一致，并先核对原文和精读报告以避免幻觉。
- ChatGPT 网页版/App 使用 **Create image**。
- Codex / Claude Code / coding-agent 环境优先使用 **`imagegen` skill**；当 `imagegen` 不可用或能力不足时，再使用 **ChatGPT Images 2.0 API** 或其他可用生图 API。
- 不使用 SVG 图替代用户要求的卡通漫画分镜。

## 推荐用户触发语

```text
请使用 Paper DeepRead Comic Studio v1.2.0 精读这篇论文，先不要生图。
```

```text
使用这个skill，根据状态，执行第1步：生成多张连续的卡通图，展示背景、旧方法缺陷、论文问题和灵感来源。
```

```text
使用这个skill，根据状态，执行第2步：生成多张连续的卡通图，展示算法整体流程与各模块。
```

```text
使用这个skill，根据状态，执行第3步：生成多张连续的卡通图，展示实验部分。
```

```text
使用这个skill，根据状态，执行第7步：把所有已确认图片合成为一个16:9 PDF。
```

```text
使用这个skill，根据状态，告知下一步应该问什么。
```

## Search keywords

`paper deep reading`, `paper comic`, `cartoon storyboard`, `visual explainer`, `research paper teaching`, `paper defense`, `PPT illustrations`, `论文精读`, `论文漫画`, `答辩插图`

## Release notes

`v1.2.0` 是增强版 ClawHub/MIT-0 发布版，强化可复现精读、实验细节审计、证据层级标注、训练到推理数字例子，以及多张连续卡通图的运镜、风格、逻辑和前后批次一致性规则。
