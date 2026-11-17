## Description:

Provides 50 AI-assisted China legal compliance skills for contract review, legal Q&A, labor compliance, intellectual property, data protection, and corporate compliance workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daimingvip-a11y](https://clawhub.ai/user/daimingvip-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Legal, compliance, HR, privacy, and business teams working with China-law matters use this bundle to draft templates, review contracts and policies, generate checklists, and prepare preliminary legal and compliance analyses for lawyer review.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The legal Q&A feature can send user questions to DeepSeek when an API key is configured, despite local-processing claims.

Mitigation: Do not configure DEEPSEEK_API_KEY or pass --api-key unless third-party processing is approved; redact privileged or regulated data before any external submission.

Risk: The bundle may process confidential contracts, employee data, personal information, or legal strategy.

Mitigation: Use data minimization, redaction, access controls, and organizational approval before processing sensitive material.

Risk: Generated case-law and compliance outputs may be incomplete or mistaken if treated as authoritative legal research.

Mitigation: Treat outputs as drafts or samples and require qualified legal review before operational or legal reliance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/daimingvip-a11y/skills/legal-compliance-bundle)
- [Publisher Profile](https://clawhub.ai/user/daimingvip-a11y)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, plain text guidance, generated templates, structured summaries, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated legal and compliance outputs are drafts for professional review.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
