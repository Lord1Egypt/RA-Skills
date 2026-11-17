## Description:

剪贴板历史 helps an agent provide Python guidance for saving, searching, and restoring a local clipboard history of up to 50 copied text entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help implement and operate a lightweight local clipboard-history utility for recovering recently copied text, searching saved entries, and optionally monitoring clipboard changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local clipboard history can retain sensitive copied text in plaintext when monitoring is enabled.

Mitigation: Avoid monitoring while copying passwords, API keys, private links, or confidential documents, and clear the stored history regularly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/534422530/skills/laosi-clipboard-history)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with Python and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides local clipboard-history sample code and optional polling-mode guidance; no API calls.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
