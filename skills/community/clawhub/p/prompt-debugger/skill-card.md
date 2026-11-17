## Description:

Debug prompts that produce unexpected AI outputs - diagnose failure modes, identify ambiguity and conflicting instructions, test variations, compare model responses, and iteratively improve prompt quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, prompt authors, and AI application teams use this skill to diagnose prompts that produce unexpected model outputs, compare prompt variations, and produce clearer rewritten prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate for broad prompt-improvement requests and produce reasoning-heavy prompt patterns.

Mitigation: Review generated prompts before use and prefer concise justification wording when hidden reasoning disclosure is not desired.

Risk: Prompt examples supplied for debugging may contain sensitive content.

Mitigation: Remove secrets, personal data, and confidential business context before sharing prompts for analysis.

## Reference(s):

- [Prompt Debugger ClawHub release](https://clawhub.ai/charlie-morrison/skills/prompt-debugger)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown or JSON diagnostic reports with rewritten prompt text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Static prompt analysis only; no prompt execution or external tool access is described.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
