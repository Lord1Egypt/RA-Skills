## Description:

Provides local GDPR compliance checks, DPIA drafting, data subject rights review, cross-border transfer assessment, and multi-format compliance reports for EU data protection workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwumit](https://clawhub.ai/user/wwumit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, privacy teams, and compliance reviewers use this skill to run local GDPR self-checks, generate draft DPIA and data subject rights materials, and produce reports for human legal or DPO review.

### Deployment Geography for Use:

EU/EEA and UK

## Known Risks and Mitigations:

Risk: The main GDPR check command can load a parent-directory compliance_core dependency outside the skill package.

Mitigation: Review or remove that dependency before installation, use a trusted compliance_core source, and run the skill in an isolated virtual environment with pinned dependencies.

Risk: Generated reports may contain sensitive business, privacy, or compliance information.

Mitigation: Keep generated reports local, restrict access to the output files, and avoid HTML or CSV output when processing untrusted content.

Risk: The skill produces compliance drafts that may be incomplete or unsuitable for a specific legal situation.

Mitigation: Use outputs as review drafts only and have major GDPR decisions reviewed by qualified counsel or a data protection officer.

## Reference(s):

- [GDPR Regulation Summary](references/gdpr-regulation.md)
- [Security Check Guide](SECURITY_CHECK_GUIDE.md)
- [ClawHub Skill Page](https://clawhub.ai/wwumit/skills/gdpr-compliance)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON, Markdown, HTML, or CSV report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports are generated locally and should be treated as sensitive drafts for professional review.]

## Skill Version(s):

1.1.0 (source: server release evidence, package.json, and CHANGELOG, released 2026-07-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
