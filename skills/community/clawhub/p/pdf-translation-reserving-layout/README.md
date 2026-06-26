# PDF Translate BabelOCR

Submission-ready export of the `pdf-translate-babelocr` skill.

## What This Skill Does

- treats user requests for `babelOCR` as related to the maintained `BabelDOC` ecosystem
- defaults to local page extraction plus agent-native translation in a fully local workflow
- uses `https://linnk.ai/doc-translator` only as a last-resort fallback for RTL, scanned, or digitally scrambled PDFs

## Repo Layout

- `SKILL.md` contains the skill instructions
- `agents/openai.yaml` contains UI metadata
- `scripts/extract_pdf_pages.py` extracts page text into JSONL
- `scripts/build_translation_batches.py` splits extracted pages into parallel translation batches
- `references/babeldoc-notes.md` contains upstream notes and fallback guidance
- `skill.json` is the Open Agent Skill manifest

## Before Publishing

1. Publish this directory as its own public GitHub repository.
2. Replace placeholder values in `skill.json`.
3. Submit the public repository URL to the target skill directories.

## Known Submission Constraints

- `Skills Directory` requires GitHub sign-in before submission.
- `Open Agent Skill` asks for a GitHub repository, category, and tags.
- `AI Skill Market` is a multi-step form.
- `SkillsLLM` exposes a submit URL, but no live form was visible to Playwright in this environment.
- The default packaged workflow stays fully local.
