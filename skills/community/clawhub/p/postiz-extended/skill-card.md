## Description:

Schedule and manage social media posts through the Postiz API for self-hosted or cloud Postiz instances.

This skill is ready for commercial/non-commercial use.

## Publisher:

[coolmanns](https://clawhub.ai/user/coolmanns)

### License/Terms of Use:


## Use Case:

Social media managers, founders, and developers use this skill to schedule, draft, publish, and manage posts across Postiz-connected channels while adapting content for X/Twitter, LinkedIn, and Bluesky.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential and reusable session-cookie exposure may allow access to the configured Postiz account.

Mitigation: Use an HTTPS Postiz URL, avoid running the skill on shared machines, and clear /tmp/postiz-cookies.txt after use.

Risk: The skill can publish immediately, upload media, update schedules, or delete posts in connected social accounts.

Mitigation: Require explicit confirmation before immediate publishing, file uploads, updates, or deletions.

Risk: Duplicate or unintended public posts may be created because the API workflow does not deduplicate automatically.

Mitigation: Query existing QUEUE and PUBLISHED posts with the duplicate-checking workflow before creating new posts.

## Reference(s):

- [Postiz Extended on ClawHub](https://clawhub.ai/coolmanns/skills/postiz-extended)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and Python helper script usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can create or modify posts through Postiz when the agent executes provided API calls or helper scripts.]

## Skill Version(s):

1.3.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
