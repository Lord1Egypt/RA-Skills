## Description:

xurl CLI for authenticated X posts, replies, reads/search, DMs, media upload, followers, auth status, or raw v2 API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use Xurl to interact with the X API from an agent workflow, including publishing and managing posts, searching and reading content, sending direct messages, handling media, and managing authentication or app settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change authentication defaults or remove registered apps, beyond the capabilities described to users.

Mitigation: Before using authentication or app-management commands, confirm those changes are intended; check the current setup with `xurl auth status` and avoid `--verbose` when output could expose authentication headers.

## Reference(s):

- [Xurl on ClawHub](https://clawhub.ai/hillstreet-ph/skills/oc-xurl)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, JSON, Guidance]

**Output Format:** [Markdown command examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands can read, publish, modify, or delete X content and manage authentication or app settings.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
