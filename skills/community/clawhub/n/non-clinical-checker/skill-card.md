## Description:

Helps medical-device teams assess non-clinical research needs and produces structured determination guidance in JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Medical-device developers and regulatory teams use this skill to review proposed non-clinical studies and existing data before clinical or registration submissions. Its recommendations require verification against current official requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad execution, file-writing, and web access exceeds the stated documentation-focused purpose.

Mitigation: Remove or tightly scope those permissions before use.

Risk: Regulatory determinations may be unreliable without the referenced rule library or approved official sources.

Mitigation: Supply and verify current official rules, and require qualified human and regulatory review of every conclusion.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhaoxinghua09-cell/skills/non-clinical-checker)

## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Proposed determinations, cited clauses, and risk notes; decision support only.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
