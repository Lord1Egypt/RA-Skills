## Description:

Browse, read, and manage Miniflux feed articles, including listing unread articles, reading article content, marking articles as read, and managing feeds and categories through a CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shekohex](https://clawhub.ai/user/shekohex)

### License/Terms of Use:

MIT

## Use Case:

Developers, feed maintainers, and agent users use this skill to browse, search, read, and update RSS/Atom feed state in a Miniflux server from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a Miniflux API key that can read and modify feed state.

Mitigation: Install only when that access is acceptable, and prefer MINIFLUX_URL and MINIFLUX_API_KEY environment variables over command-line API key flags.

Risk: When CLI credential flags are used, the skill can store the API key in ~/.local/share/miniflux/config.json.

Mitigation: Avoid CLI credential flags in shared environments and check or restrict permissions on the config file if it is created.

Risk: The configured Miniflux endpoint receives authenticated API requests from the skill.

Mitigation: Use an HTTPS Miniflux URL that you control.

## Reference(s):

- [ClawHub Miniflux skill page](https://clawhub.ai/shekohex/skills/miniflux)
- [Publisher profile](https://clawhub.ai/user/shekohex)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands; CLI responses may be plain text, tab-separated text, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires uv, Python >= 3.12, a Miniflux server URL, and a Miniflux API key.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
