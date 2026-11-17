## Description:

Search Pinterest for images and pins using keyword queries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikehankk](https://clawhub.ai/user/mikehankk)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to search Pinterest by keyword, collect structured pin metadata, save result files, and optionally download matching images for visual inspiration workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Pinterest session cookies and proxy settings.

Mitigation: Avoid using a real Pinterest session cookie with this version, and review any cookie or proxy values before use.

Risk: The configuration helper can print shell export commands from provided values.

Mitigation: Do not copy generated export commands containing untrusted values; set environment variables manually after review.

Risk: The documented setup installs Bun through a shell installer.

Mitigation: Install Bun through a pinned or otherwise verifiable method before running the skill.

Risk: The optional download mode writes remote image content to disk.

Mitigation: Use --download only in a sandboxed environment with limited network and disk access.

## Reference(s):

- [Pinterest Search ClawHub listing](https://clawhub.ai/mikehankk/skills/pinterest-search)
- [Bun runtime](https://bun.sh)

## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Configuration instructions]

**Output Format:** [JSON arrays, saved JSON result files, optional downloaded image files, and shell export commands for configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Searches can use optional cookie and proxy configuration, pagination, incremental cache filtering, custom output directories, and optional image downloads.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
