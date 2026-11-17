## Description:

Pre-install security scanner for ClawHub skills that reviews SKILL.md content for prompt injection, data exfiltration patterns, malicious commands, typosquatting, and quality red flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and security reviewers use this skill to audit ClawHub and OpenClaw skill files before installation or team deployment. It produces a structured security score, issue table, verdict, and recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scanner output is advisory and may miss obfuscated payloads or malicious linked URLs.

Mitigation: Use it as one layer of review alongside ClawHub's built-in scanning and manual inspection before installation.

Risk: A clean result could be over-relied on when evaluating unfamiliar skills.

Mitigation: Treat scores as guidance, prefer explicit /skill-scanner invocations, and verify findings before team or enterprise deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/phy041/skills/phy-skill-scanner)
- [Canlah AI Homepage](https://canlah.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown report with a score table, verdict, findings, and recommendation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes quick-scan and batch-scan report variants when requested.]

## Skill Version(s):

1.0.3 (source: server release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
