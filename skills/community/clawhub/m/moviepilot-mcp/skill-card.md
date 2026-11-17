## Description:

MoviePilot MCP helps agents automate a MoviePilot media library by searching movies, TV, anime, and documentaries; managing subscriptions, downloads, library transfers, PT sites, and plugins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yangyangupday](https://clawhub.ai/user/yangyangupday)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers who operate a MoviePilot instance use this skill to search media, manage subscriptions and downloads, organize library files, maintain PT sites, and administer plugins or system settings through MoviePilot's MCP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can exercise broad administrative control over MoviePilot, including subscriptions, downloads, file transfer, plugins, system settings, browser actions, and persistent agent behavior.

Mitigation: Install only for trusted MoviePilot instances, use the least-privileged token available, and manually confirm deletion, file transfer, plugin, system setting, persona, slash-command, browser, and local-file-send operations.

Risk: MoviePilot API tokens and site credentials may be exposed through command lines, chat logs, or local configuration files.

Mitigation: Prefer HTTPS, avoid sharing tokens in command lines or chat logs, restrict config.json permissions, and rotate credentials if exposure is suspected.

## Reference(s):

- [MoviePilot MCP Skill Page](https://clawhub.ai/yangyangupday/skills/moviepilot-mcp)
- [MoviePilot Configuration Guide](references/setup-guide.md)
- [MoviePilot MCP Tool Reference](references/tools.md)
- [MoviePilot Workflow Guide](references/workflows.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API Calls]

**Output Format:** [Markdown guidance with shell commands, JSON arguments, and MoviePilot API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create a local config.json containing the MoviePilot server URL and API token.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
