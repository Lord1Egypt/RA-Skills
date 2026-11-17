## Description:

Facebook browser automation skill for posting, reading comments, generating intelligent replies, and tracking comment threads for brand engagement and high-frequency community operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT-0

## Use Case:

External social-media operators and brand teams use this skill to automate Facebook posting, comment reading, reply generation, reply posting, and thread follow-up. It is suited to high-frequency community engagement where draft or query modes can keep sensitive responses under human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use a logged-in Facebook account to post or reply automatically, and approval defaults may be unclear.

Mitigation: Use draft or query mode by default, and require human approval for major announcements, sensitive replies, controversial threads, or unattended activity.

Risk: Browser profile and local style-file access can expose account state or private workspace content.

Mitigation: Isolate the Facebook browser profile and verify which local files the skill may read before installation.

Risk: Receipts, comment snapshots, and logs may retain full comment or reply text.

Mitigation: Store full text only when needed for audit records, and apply retention or redaction rules for routine operation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON receipt examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational receipts, comment snapshots, and error logs when actions run.]

## Skill Version(s):

1.0.1 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
