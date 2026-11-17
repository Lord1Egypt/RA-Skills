## Description:

Audits brand narrative truth, message-system consistency, landing alignment, and measured effectiveness as separate TALE profiles without averaging them into a composite score.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaron-he-zhu](https://clawhub.ai/user/aaron-he-zhu)

### License/Terms of Use:

MIT-0

## Use Case:

Brand, marketing, product, and launch teams use this skill to audit whether positioning, canon, flagship surfaces, or message experiments are truthful, internally consistent, and supported by evidence. It is intended for narrative review and evidence-integrity checks, not launch readiness or social operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit conclusions can be incomplete when relevant canon, claims, surfaces, or experiment evidence are unavailable.

Mitigation: Require missing qualified items to be reported as unknown before findings, and avoid gate verdicts when deterministic scoring inputs are unavailable.

Risk: Saved audit artifacts may contain sensitive brand narrative, claims, surface, or experiment details.

Mitigation: Persist audit artifacts only after explicit authorization and only when an audit record should be retained.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aaron-he-zhu/skills/narrative-quality-auditor)
- [Project homepage](https://github.com/aaron-he-zhu/aaron-marketing-skills)
- [Standalone Auditor Runtime](references/auditor-runtime.md)
- [Distribution Manifest](distribution-manifest.json)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown audit report with typed verdict, score state, evidence, Unknowns, and fixes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist permissioned audit artifacts only after explicit authorization.]

## Skill Version(s):

19.0.0 (source: server evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
