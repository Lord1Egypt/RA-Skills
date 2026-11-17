## Description:

Guide users to VideoAny Lip Sync Studio to create lip-sync videos from an image and audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gaoq1](https://clawhub.ai/user/gaoq1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to get practical guidance for creating lip-sync videos with VideoAny from a portrait image and an audio track. The skill explains supported models, input formats, resolution choices, quality tips, and responsible-use reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may upload sensitive or unauthorized images or audio to the third-party VideoAny website.

Mitigation: Use only content the user owns or has permission to use, and review VideoAny privacy and retention terms before uploading sensitive media.

Risk: Lip-sync videos can be used for deceptive impersonation or misleading edits.

Mitigation: Avoid deceptive impersonation, respect consent and applicable law, and disclose synthetic or edited media where appropriate.

Risk: The skill declares shell execution for a local helper.

Mitigation: Review the helper command before running it; evidence.security reports no hidden persistence, credential handling, destructive behavior, or third-party Python dependencies.

## Reference(s):

- [VideoAny Lip Sync Studio](https://videoany.io/lip-sync)
- [ClawHub Skill Page](https://clawhub.ai/gaoq1/skills/lip-sync-videoany)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance and plain CLI text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The local helper prints guidance only; actual lip-sync generation occurs on VideoAny web.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
