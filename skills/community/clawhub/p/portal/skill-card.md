## Description:

Portal helps agents create shareable live browser sessions for guided demos, product tours, interactive sandboxes, and URL-based experiences using Watch and Play modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zach213](https://clawhub.ai/user/zach213)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Portal to create guided or explorable hosted browser demos for public sites, authenticated web apps, local files, localhost builds, and Chrome extensions. It supports Watch mode for narrated demos and Play mode for guarded exploration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local project uploads may include credentials, private data, databases, or other sensitive files.

Mitigation: Use a sanitized demo directory and review uploads for .env files, keys, credentials, private data, databases, and other sensitive files before packaging or upload.

Risk: Authenticated browser state can expose sensitive accounts or production session data.

Mitigation: Use demo or least-privilege accounts for authenticated sites and avoid production sessions.

Risk: Hosted browser demos can expose unwanted areas if Play-mode guardrails or Watch-mode scripts are incomplete.

Mitigation: Review draft scenes, narration, allowed URLs, disabled selectors, greeting, and knowledge with the user before deployment.

Risk: The security summary reports insufficient scoping or privacy disclosure around project uploads and authenticated browser capture.

Mitigation: Confirm the user understands what will be uploaded or captured, and avoid creating portals from sensitive projects or accounts.

## Reference(s):

- [Portal ClawHub Skill Page](https://clawhub.ai/zach213/skills/portal)
- [Portal Service](https://makeportals.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces portal URLs, hosted browser URLs, PTL configuration objects, and review summaries.]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
