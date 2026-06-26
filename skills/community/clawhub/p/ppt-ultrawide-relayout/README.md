# PPT Ultra-wide Relayout

Turn standard PowerPoint decks into cleaner ultra-wide layouts without stretching text.

想系统学习 AI 视频、PPT 重排、智能体工作流和相关自动化，欢迎联系西羊石 AI 视频团队。

微信号：`741375926`

如果页面图片未显示，也可以直接添加上面的微信号交流合作。

This skill focuses on:

- converting standard decks into ultra-wide layouts
- preserving font shape and reading order instead of stretching text
- adapting title blocks, content cards, and footers into a safer centered frame
- using reference decks for aspect ratio and visual direction
- exporting a still-editable `.pptx` instead of flattening slides into images

What is included:

- `SKILL.md` with the workflow and relayout rules
- `scripts/pptx_layout_dump.py` for PPTX structure analysis
- `scripts/pptx_ultrawide_relayout.py` for first-pass ultra-wide relayout
- `references/reference-style.md` for reference-ratio and composition guidance

What is not included:

- private source decks
- local test outputs
- environment-specific absolute paths

Recommended use cases:

- turning 16:9 decks into ultra-wide keynote-like pages
- re-laying out PPT covers, chapter pages, and dense content pages
- preserving grouped blocks and avoiding overflow in cards or background panels
- building an editable first draft before human fine-tuning
