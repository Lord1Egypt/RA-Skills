## Description:

像素级凝视指导具备视觉能力的 AI Agent 通过四层流程审看图片，以减少漏读数字、状态、小字和 UI 细节。

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilei0311](https://clawhub.ai/user/lilei0311)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, QA reviewers, and other external users use this skill to inspect images, screenshots, product labels, and UI renderings with a four-layer review process before answering or reporting defects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make image and screenshot reviews more deliberate and verbose.

Mitigation: Use it for precision-sensitive visual tasks and ask the publisher to clarify narrower trigger conditions when broad activation is not desired.

Risk: The source examples and primary skill prose are in Chinese, which may affect users expecting English-only guidance.

Mitigation: Confirm language expectations with the publisher or pair the skill with instructions for the target response language.

## Reference(s):

- [Agent front-end self-review case](references/case-agent-self-review.md)
- [Product label reading case](references/case-product-label.md)
- [ClawHub skill page](https://clawhub.ai/lilei0311/skills/pixel-gaze)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text visual-analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompt-only; no external API, OCR tool, code execution, persistence, credential use, or hidden data movement identified in server security evidence.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
