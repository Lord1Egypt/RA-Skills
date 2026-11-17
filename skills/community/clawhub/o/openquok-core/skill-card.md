## Description:

Helps agents authenticate to OpenQuok, upload media, draft and schedule social posts, manage engagement plugs, and view channel analytics through the OpenQuok CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ratimon](https://clawhub.ai/user/ratimon)

### License/Terms of Use:

MIT-0

## Use Case:

Social media teams and their agents use this skill to prepare, schedule, update, and analyze posts across connected OpenQuok channels, including automated follow-up engagement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent can schedule, modify, delete, or automate social posts in connected channels.

Mitigation: Confirm target integrations, post and plug IDs, scheduled times, and privacy changes before approving write actions.

Risk: OpenQuok credentials may be exposed in chat or logs.

Mitigation: Prefer device OAuth, keep tokens out of chat and logs, and rotate any token that may have been exposed.

## Reference(s):

- [OpenQuok Core on ClawHub](https://clawhub.ai/ratimon/skills/openquok-core)
- [OpenQuok CLI package](https://www.npmjs.com/package/@openquok/auto-cli)
- [OpenQuok command reference](artifact/resources/command-reference.md)
- [OpenQuok Bluesky integration documentation](https://www.openquok.com/docs/social-integration/bluesky)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with CLI commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the separately installed OpenQuok CLI and access to an OpenQuok workspace.]

## Skill Version(s):

1.0.9 (source: ClawHub release metadata; packaged frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
