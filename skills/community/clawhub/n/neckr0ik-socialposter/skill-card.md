## Description:

Automates social media posting across Twitter/X, LinkedIn, Facebook, and Instagram, including scheduled posts, engagement tracking, and auto-replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neckr0ik](https://clawhub.ai/user/neckr0ik)

### License/Terms of Use:


## Use Case:

External users and social media operators use this skill to plan, publish, and monitor posts across multiple social platforms. It also supports automatic replies and analytics workflows for managing an online presence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to connect posting credentials for social media accounts.

Mitigation: Use least-privilege and short-lived tokens where possible, and avoid entering secrets directly on the command line.

Risk: Automatic public replies can post unintended content if they are enabled without adequate controls.

Mitigation: Scope auto-replies by platform and account, test templates before use, apply rate limits, keep logs, and maintain an easy disable path.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/neckr0ik/skills/neckr0ik-socialposter)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Markdown, Guidance]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that configure social media API credentials, schedule posts, export analytics, and define auto-reply templates.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
