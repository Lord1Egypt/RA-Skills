# LLM Wiki Karpathy Release Notes

## Short Description

Inspired by a public workflow shared by Andrej Karpathy (@karpathy).
From raw text, PDFs, images, and structured data to a living Markdown wiki that compounds with every question.

## Marketplace Card Copy

Title:
- LLM Wiki Karpathy

Slug:
- llm-wiki-karpathy

Short description:
- Inspired by a public workflow shared by Andrej Karpathy (@karpathy).

Install hook:
- From raw text, PDFs, images, and structured data to a living Markdown wiki that compounds with every question

## Announcement Copy

`LLM Wiki Karpathy` skill `1.2.3` now ships alongside runtime `0.4.4` and republishes the workflow under a cleaner public identity:

- the skill slug is now `llm-wiki-karpathy`
- the npm runtime is now `@harrylabs/llm-wiki-karpathy`
- the ClawHub code plugin is now `llm-wiki-karpathy-plugin`
- legacy `llm-knowledge-bases` and `llm-kb` command aliases are still available during the transition

The workflow remains local-first and Markdown-first. This release is mostly about shipping the same wiki workflow under a tighter, Karpathy-attributed name while keeping the underlying `kb_*` contract intact.

This release is still explicitly inspired by a public workflow shared by Andrej Karpathy ([@karpathy](https://x.com/karpathy)) around using LLMs to maintain personal knowledge bases built from Markdown, images, and accumulated outputs. That attribution helps position the skill in a recognizable lineage without implying endorsement.

The current release focuses on:

- renaming the skill, runtime package, code plugin, and publish scripts to `llm-wiki-karpathy`
- preserving the existing `kb_*` runtime contract and transition aliases for the old command names
- refreshing release metadata so npm, ClawHub skill publishing, and ClawHub code-plugin publishing all point at the new identity

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

- `openclaw-skill-llm-wiki-karpathy`

## Publish Command

```bash
  clawhub publish /absolute/path/to/llm-wiki-karpathy \
  --slug llm-wiki-karpathy \
  --name "LLM Wiki Karpathy" \
  --version "1.2.3" \
  --changelog "Rebrand the skill and plugin under the new llm-wiki-karpathy identity and refresh the publish workflow." \
  --tags "knowledge-base,research,markdown,wiki,obsidian,multimodal,pdf,image,data,local-first"
```
