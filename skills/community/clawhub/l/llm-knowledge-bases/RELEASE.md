# LLM Knowledge Bases Release Notes

## Short Description

Inspired by a public workflow shared by Andrej Karpathy (@karpathy).
From raw text, PDFs, images, and structured data to a living Markdown wiki that compounds with every question.

## Marketplace Card Copy

Title:
- LLM Knowledge Bases

Slug:
- llm-knowledge-bases

Short description:
- Inspired by a public workflow shared by Andrej Karpathy (@karpathy).

Install hook:
- From raw text, PDFs, images, and structured data to a living Markdown wiki that compounds with every question

## Announcement Copy

`LLM Knowledge Bases` skill `1.2.2` stays on top of runtime `0.4.1`, but makes the workflow much easier to invoke through short natural-language requests:

- inspect a wiki with short prompts like "检查一下我的 wiki，先别改"
- continue book-review ingestion with prompts like "补书评前 10 个"
- run focused cleanup passes with prompts like "整理一下 AI 相关内容"
- add durable derived pages with prompts like "补 3 个 concept pages"
- repair source-id drift with prompts like "修一下 source id 漂移，先 dry run"
- continue a living wiki with prompts like "继续推进我的这份库"

The workflow remains local-first and Markdown-first. This release improves the skill layer, not the runtime contract: it teaches the agent how to map compact English and Chinese requests onto the existing `kb_*` workflows without making users spell out the full operator prompt every time.

This release is still explicitly inspired by a public workflow shared by Andrej Karpathy ([@karpathy](https://x.com/karpathy)) around using LLMs to maintain personal knowledge bases built from Markdown, images, and accumulated outputs. That attribution helps position the skill in a recognizable lineage without implying endorsement.

The current release focuses on:

- stronger natural-language routing in `SKILL.md`, `agents/openai.yaml`, and `agents/codex-AGENTS.md`
- explicit Chinese intent hints for inspection, cleanup, gap mapping, source-id repair, and continuation requests
- scenario presets for AI-topic cleanup, book-review batch ingest, and continuing this specific library incrementally
- compact one-line prompt packs so users can omit long operator instructions and often omit the explicit `$llm-knowledge-bases` prefix too
- release metadata that matches skill `1.2.2` and runtime `0.4.1`

It works especially well with Obsidian, while staying portable because everything remains plain Markdown.

## Suggested Tags

- knowledge-base
- research
- markdown
- wiki
- obsidian
- multimodal
- pdf
- image
- data
- local-first

## Suggested Repo Name

- `openclaw-skill-llm-knowledge-bases`

## Publish Command

```bash
  clawhub publish /absolute/path/to/llm-knowledge-bases \
  --slug llm-knowledge-bases \
  --name "LLM Knowledge Bases" \
  --version "1.2.2" \
  --changelog "Add stronger natural-language routing and compact Chinese one-line prompts for common wiki workflows." \
  --tags "knowledge-base,research,markdown,wiki,obsidian,multimodal,pdf,image,data,local-first"
```
