## Description:

Prompt Alchemist optimizes user prompts with a four-part distillation framework that diagnoses prompt quality, restructures prompts, adds reasoning guidance when needed, and returns refined prompt text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cherish133](https://clawhub.ai/user/cherish133)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and AI writers use this skill to turn rough prompts into structured, higher-quality prompts while preserving the original intent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation wording can cause pasted sensitive prompt text to be processed by the optimization workflow.

Mitigation: Avoid pasting sensitive or confidential text unless the intent is to have the agent optimize that prompt.

## Reference(s):

- [Server-resolved source repository](https://github.com/Cherish133/prompt-alchemist)
- [ClawHub skill page](https://clawhub.ai/cherish133/skills/prompt-alchemist)
- [ClawHub publisher profile](https://clawhub.ai/user/cherish133)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured diagnostic sections and optimized prompt text, often including XML-style prompt blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapts output depth to prompt complexity; no code execution or external data access.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
