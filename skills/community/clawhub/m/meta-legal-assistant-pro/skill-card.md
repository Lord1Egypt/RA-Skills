## Description:

Meta Legal Assistant Pro is a distilled Chinese-law assistant skill for contract review, rights-protection guidance, legal-rule lookup, and arbitration or litigation process guidance with self-verification and safety-boundary checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill for China-law information workflows such as contract review, labor and consumer disputes, family and property issues, debt matters, online-rights disputes, traffic matters, and procedural guidance. Its outputs are informational and include guardrails to avoid formal legal opinions or litigation representation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist legal-use notes, preferences, or case-related details in plaintext learning records.

Mitigation: Review before installing; avoid storing confidential case facts, identity details, contract terms, or dispute notes unless plaintext local retention is acceptable.

Risk: The learner utility can write state into arbitrary skill directories.

Mitigation: Scope learning to the intended skill directory, ask before saving data, and provide practical inspect and delete controls for retained records.

Risk: Legal information may be outdated because the skill says current legal developments require online verification.

Mitigation: Require source and article-level verification for cited legal rules, and mark unsupported or stale legal claims as needing verification.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qq435912743/skills/meta-legal-assistant-pro)
- [Distillation report](artifact/distillation_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands, configuration]

**Output Format:** [Markdown or plain text guidance, with optional JSON learning records and shell commands for the learner utility]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Legal guidance must remain informational, cite or flag legal sources for verification, and avoid formal legal opinions or litigation representation.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
