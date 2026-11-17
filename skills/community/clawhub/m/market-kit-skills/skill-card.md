## Description:

Use when the user needs marketing deliverables such as campaign plans, Xiaohongshu notes, audience positioning, selling-point refinement, reference-grounded copy, or marketing images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinshimeng18](https://clawhub.ai/user/qinshimeng18)

### License/Terms of Use:

MIT-0

## Use Case:

Marketing, brand, content, and growth teams use this skill to turn campaign ideas, product material, and reference context into deliverable marketing plans, Xiaohongshu notes, selling-point positioning, copy, image-linked results, and follow-up iterations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist a bearer API key in local shell and configuration files.

Mitigation: Install only when local token persistence is acceptable; prefer a credential manager or remove persisted tokens after use.

Risk: The skill sends marketing prompts, identifiers, and user content to JustAI's remote service.

Mitigation: Avoid submitting sensitive project data unless that service is approved for the data; review the API origin and destination before use.

Risk: The security verdict is suspicious because credential storage and configurable remote transmission need review before installation.

Mitigation: Review the security summary and guidance before deployment, and require confirmation before persisting tokens or transmitting sensitive content.

## Reference(s):

- [Market Kit Skills ClawHub page](https://clawhub.ai/qinshimeng18/skills/market-kit-skills)
- [JustAI marketing result service](https://justailab.com/marketing)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON results from the bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include conversation identifiers, structured marketing results, image URLs, and a web result URL.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
