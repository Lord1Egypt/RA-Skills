## Description:

Lets agents ask Perplexity through a logged-in browser without a Perplexity API key and returns the extracted answer with run checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mfang0126](https://clawhub.ai/user/mfang0126)

### License/Terms of Use:

MIT

## Use Case:

Developers and other agent users can research questions through their existing Perplexity web session, collect answers and run receipts, and review citation and model-label checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Autonomous clicks and typing can change data or settings in logged-in accounts.

Mitigation: Use a dedicated browser profile or low-risk sites; avoid accounts where a click can purchase, delete, publish, or change permissions.

Risk: Page labels, field values, goals, and action history may reach external model services.

Mitigation: Use only a model endpoint you trust and avoid exposing sensitive pages or account data.

## Reference(s):

- [ClawHub release](https://clawhub.ai/mfang0126/skills/perplexity-web-bridge)
- [Perplexity usage playbook](references/perplexity-playbook.md)
- [Coverage and capability matrix](docs/COVERAGE.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON result containing an answer, status, and site checks; optional JSONL run receipts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May flag weak citation coverage or a changed model label; check cited claims before relying on them.]

## Skill Version(s):

1.1.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
