## Description:

Prepare local documents for OpenClaw review without losing source anchors, redaction notes, or validation checkpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiepu110](https://clawhub.ai/user/jiepu110)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to plan local document conversion into reviewable Markdown while preserving source anchors, redaction notes, and validation checkpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may select documents they are not authorized to process.

Mitigation: Confirm authorization before using the skill on local documents.

Risk: Public output may expose sensitive local file paths or personal data if redaction is skipped.

Mitigation: Apply the skill's redaction and path-suppression checks before sharing generated Markdown.

Risk: Converted sections may become hard to audit if source anchors are missing or uncertain extraction is filled in silently.

Mitigation: Preserve source anchors for every section and mark uncertain extraction results instead of filling gaps.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiepu110/skills/oc-document-preflight)
- [Support repository referenced by the skill](https://github.com/Star-Ring-Protocol/openclaw-gateway-guardian)

## Skill Output:

**Output Type(s):** [Markdown, guidance]

**Output Format:** [Markdown plan with source-anchor maps, redaction notes, and validation checklist]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only workflow guidance; no upload, login, remote storage, or persistent memory behavior is described.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
