## Description:

Enables AI agents to select and run local network tools for web fetching, downloads, media retrieval, proxy routing, and network diagnostics without API keys.

This skill is ready for commercial/non-commercial use.

## Publisher:

[savior-li](https://clawhub.ai/user/savior-li)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill when they need controlled web retrieval, file downloads, DNS and connectivity diagnostics, public IP checks, WHOIS lookups, or media downloads through locally installed command-line tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad network and proxy access can reach unintended or sensitive destinations.

Mitigation: Use only for explicit, user-approved network requests and avoid internal URLs, metadata endpoints, untrusted redirects, and sensitive resources.

Risk: Command-line headers can expose secrets.

Mitigation: Do not pass secrets in command-line headers; use safer secret handling outside this skill when authentication is required.

Risk: Downloads can write unsafe or unexpected files.

Mitigation: Keep downloads in a controlled directory and inspect filenames and content before processing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/savior-li/skills/network-tools)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples and text output from local network tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce downloaded files when download or media commands are used.]

## Skill Version(s):

2.0.0 (source: server release metadata, package.json, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
