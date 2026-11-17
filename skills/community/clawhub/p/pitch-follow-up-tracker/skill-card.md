## Description:

Pitch Follow-Up Tracker monitors an outreach pipeline, checks Gmail for replies, and drafts contextual follow-up emails that reference the original pitch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexa853](https://clawhub.ai/user/alexa853)

### License/Terms of Use:

MIT-0

## Use Case:

External outreach teams use this skill to review a Google Sheet or markdown pitch tracker, check Gmail for replies, classify pitch status, and prepare tiered follow-up drafts for user review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect Gmail, pitch trackers, and broader local or remembered context while verifying replies.

Mitigation: Constrain use to a specific Gmail account, tracker, date range, thread, or contact, and avoid broad mailbox or memory searches unless explicitly approved.

Risk: Generated follow-up drafts may contain incorrect context, inappropriate tone, or unapproved outreach content.

Mitigation: Review and personalize every generated draft before creating or sending any email.

Risk: Installing gog through an unpinned global npm command may introduce supply-chain uncertainty.

Mitigation: Install gog from a trusted source and pin the version used in the agent environment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/alexa853/skills/pitch-follow-up-tracker)
- [Artifact README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown outreach report with draft email text and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces status classifications, tiered follow-up drafts, and Gmail draft commands only after explicit user approval.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
