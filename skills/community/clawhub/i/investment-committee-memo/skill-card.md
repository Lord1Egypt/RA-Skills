## Description:

Use this skill when a VC associate, principal, or partner needs to turn deal notes, deck contents, and diligence summaries into an Investment Committee memo.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

VC associates, principals, and partners use this skill to turn deal notes, deck contents, and diligence summaries into a draft investment committee memo with source-tagged claims, open questions, kill criteria, and a Pass, Track, Diligence, or Term-sheet recommendation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste confidential founder or data-room material into an unapproved workspace.

Mitigation: Use only approved workspaces for confidential data and redact trade secrets before pasting, consistent with the security guidance.

Risk: The draft memo may be mistaken for investment advice or verified diligence.

Mitigation: Keep the DRAFT - DEAL LEAD MUST VERIFY label and require every claim or metric to cite a supplied source or be marked Unknown.

Risk: Currency or fiscal-calendar assumptions can make financial statements ambiguous.

Mitigation: Ask users to specify any non-USD currency or non-calendar fiscal year; otherwise rely on the documented defaults.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/investment-committee-memo)
- [README](artifact/README.md)
- [Changelog](artifact/CHANGELOG.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft memo with an evidence matrix, kill criteria checklist, open questions, and recommendation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Drafts are labeled DRAFT - DEAL LEAD MUST VERIFY; metrics without supplied sources are marked Unknown.]

## Skill Version(s):

0.1.2 (source: evidence.release.version and artifact CHANGELOG, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
