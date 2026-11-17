## Description:

Helps developers train and explore a small local character-level GPT, with optional web search, coding evaluations, and handwritten-digit recognition exercises.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yifanqqmc](https://clawhub.ai/user/yifanqqmc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and learners use this skill to train a small text model on local or downloaded corpora, generate sample text, and explore optional search, code evaluation, and digit recognition workflows. It is not intended to run pretrained large language models or serve production-grade NLP tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional search or corpus downloads can contact public websites and expose search terms.

Mitigation: Do not put secrets or private text in search queries; use network features only when appropriate.

Risk: Training and dataset workflows write checkpoints and generated data to disk.

Mitigation: Specify output directories within the user's workspace and review downloaded data before use.

## Reference(s):

- [Local MiniGPT on ClawHub](https://clawhub.ai/yifanqqmc/skills/local-minigpt)
- [Chinese Poetry public corpus](https://github.com/chinese-poetry/chinese-poetry)

## Skill Output:

**Output Type(s):** [Text, Code, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance and commands; generated text and optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Training and evaluation can save checkpoints, tokenizer settings, corpora, and sample images to disk.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
