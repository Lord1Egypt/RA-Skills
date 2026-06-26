# Paper DeepRead Comic Studio Skill v1.2.0

**中文名：论文精读漫画工坊**

**中文名：论文精读漫画工坊**

A ClawHub-ready MIT-0 skill for rigorous paper deep reading and coherent cartoon-comic storyboard generation, ending with final image-PDF assembly.

## Core workflow

1. **Text-only deep read**: start with a plan, then directly display the full deep-reading report. Do not generate images in this step.
2. **Staged visual storyboards**: generate one coherent cartoon-comic section at a time as multiple separate continuous images, preserving camera movement, style, evidence grounding, and narrative continuity.
3. **Final image-PDF assembly**: combine all confirmed storyboard images into one 16:9 PDF.

## Visual steps

- Step 1: Background, prior-method defects, paper problem, and inspiration.
- Step 2: Algorithm overview and modules.
- Step 3: Experiment section.
- Step 4: Limitations and defense.
- Step 5: Future directions and innovation graph.
- Step 6: Cover, summary, and Q&A backup visuals.
- Step 7: Final image-PDF assembly.

## Source grounding

Storyboard and report content may be grounded in the uploaded PDF, LaTeX source, or both. When both are present, cross-check captions, figures, tables, formulas, and claims. Do not invent missing details. Image prompts must keep paper-explicit facts, reasonable inferences, nearby-work inferences, and missing details separate.

## Platform guidance

- ChatGPT web/app: use **Create image** for cartoon storyboard generation.
- Codex / Claude Code / coding-agent environments: prefer the `imagegen` skill when available. If it is unavailable or insufficient, use **ChatGPT Images 2.0 API** or another approved image-generation API.
- Do not substitute SVG diagrams for the requested cartoon-comic storyboard images.
- For continuous cartoon generation, ask for `生成多张连续的卡通图`; split different paper parts into separate images or batches instead of compressing them into one image.

## Resume prompts

```text
使用这个skill，根据状态，执行第X步：<要执行的阶段>。
```

```text
使用这个skill，根据状态，告知下一步应该问什么。
```

## License

MIT-0
