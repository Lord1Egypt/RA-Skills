## Description:

A Chinese-language administrative drafting assistant for government bodies and enterprises that helps prepare official memos, notices, meeting minutes, periodic reports, meeting briefs, cross-department communications, and compliance reminders without making professional judgments or inventing missing records.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chesaram](https://clawhub.ai/user/chesaram)

### License/Terms of Use:

MIT-0

## Use Case:

Administrative staff in public-sector and enterprise settings use this skill to draft, organize, track, and review routine administrative documents and process reminders. It is intended as a drafting aid, with missing facts marked for confirmation and generated records reviewed before filing, sending, or relying on them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated administrative records may contain unsupported details if users provide incomplete inputs.

Mitigation: Require source notes for dates, attendees, owners, deadlines, decisions, metrics, document numbers, and report claims, and review all outputs before filing, sending, or relying on them.

Risk: Users may over-rely on drafts for official decisions, signatures, filings, or compliance conclusions.

Mitigation: Use the skill only as a drafting aid; keep professional judgments, approvals, signatures, dispatch, stamping, and legal or financial conclusions with authorized personnel.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chesaram/skills/gov-entity-admin-1-0-0)
- [ClawHub publisher profile](https://clawhub.ai/user/chesaram)
- [artifact/SKILL.md](artifact/SKILL.md)
- [artifact/README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese plain text, Markdown, or XML-tagged document sections depending on the requested administrative document type]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided source facts for dates, attendees, owners, deadlines, decisions, metrics, document numbers, and report claims; missing fields should be marked as pending confirmation.]

## Skill Version(s):

1.0.0 (source: release evidence, SKILL.md frontmatter, manifest.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
