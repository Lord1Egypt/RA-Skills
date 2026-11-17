## Description:

Reviews outward-facing prose for privacy and infrastructure leaks, then applies writing conventions before publication.

This skill is ready for commercial/non-commercial use.

## Publisher:

[solomonneas](https://clawhub.ai/user/solomonneas)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and other authors use this skill to review a single public-facing draft for identity or infrastructure leaks and writing-convention issues before publishing. It reports findings and proposed replacements for confirmation before edits are applied.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Proposed edits, especially attribution removals, could remove intended content or misrepresent the author's intent.

Mitigation: Review each finding and confirm changes before applying them.

Risk: Sensitive draft content could be left in temporary files during review.

Mitigation: Prefer inline scanning to avoid storing sensitive drafts in temporary files.

Risk: Installing an optional scanning dependency introduces a separate dependency decision.

Mitigation: Evaluate brigade-cli independently before installing it.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/solomonneas/skills/plate)
- [Publisher profile](https://clawhub.ai/user/solomonneas)

## Skill Output:

**Output Type(s):** [Analysis, Markdown]

**Output Format:** [Markdown findings table with locations and proposed replacements]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requests confirmation before applying edits.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
