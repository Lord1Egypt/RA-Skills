## Description:

PathClaw 病理助手 helps agents submit user-selected .svs pathology slides to 华银康集团 PathClaw for AI-assisted analysis after confirming the slide path and supported analysis type.

This skill is ready for commercial/non-commercial use.

## Publisher:

[t-programmer](https://clawhub.ai/user/t-programmer)

### License/Terms of Use:

MIT-0

## Use Case:

External users and clinical support teams can use this skill to validate a readable .svs pathology slide, choose one supported PathClaw analysis category, submit the slide, and receive returned analysis status and results. The skill is intended for AI-assisted pathology workflow support, not standalone medical diagnosis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pathology slide files may contain patient data and are uploaded to the PathClaw service.

Mitigation: Confirm authorization, consent, retention, and compliance requirements before submitting any .svs file.

Risk: The workflow and prompts are primarily in Chinese, which can cause misunderstanding for non-Chinese readers.

Mitigation: Have the prompts reviewed or translated before relying on the workflow.

Risk: AI-assisted pathology output could be mistaken for a final diagnosis.

Mitigation: Use the returned result as reference only and require qualified physician review with clinical context and other examinations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, API calls, guidance]

**Output Format:** [Markdown text with tables, status summaries, diagnostic result summaries, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a readable non-empty .svs file and one supported PathClaw pathology category; successful results may include slide_id, diagnostic text, and a heatmap link.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
