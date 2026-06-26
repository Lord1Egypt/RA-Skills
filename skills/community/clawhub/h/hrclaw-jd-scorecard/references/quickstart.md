# Quickstart

This skill has two flows:

- `JD -> scorecard`
- `Resume PDF/text -> score against a scorecard`

## Use it

1. Paste a JD to generate a scorecard.
2. Paste a resume together with a JD or scorecard to score the resume.
3. Ask for `chat` output if you want Feishu/DingTalk-friendly markdown.

## Expected outputs

- `scorecard.json` for integrations
- `scorecard.md` for human review
- `chat-scorecard.md` for team chat
- `resume-score.json` for resume scoring
- `chat-resume-score.md` for team chat

## Good prompts

- `把这段 JD 转成招聘评分卡，输出纯 JSON`
- `用这份 PDF 简历按下面评分卡打分，输出纯 JSON`
- `用飞书版输出这份评分卡`

## Resume scoring

- Give the skill both the resume and a scorecard or JD.
- If the PDF has no text layer, the flow should return `needs_ocr`.
- Do not ask it to guess missing resume text.
