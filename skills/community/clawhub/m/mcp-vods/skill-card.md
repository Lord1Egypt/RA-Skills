## Description:

用于追剧/追番的技能，为AI提供搜索影视播放地址的能力，并支持在小米电视上直接播放。当用户想搜索影视、动漫、短剧、综艺等节目信息或更新进度时使用此技能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[al-one](https://clawhub.ai/user/al-one)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to search video, anime, short-drama, and variety-show sources, check update status, and prepare playback commands. When configured with local TV addresses, it can cast media URLs to Xiaomi TV or Android TV/TvBox devices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill instructs agents to auto-download and run unpinned third-party packages.

Mitigation: Use pinned, reviewed versions of `mcporter` and `mcp-vods`, and run them in a sandbox where practical.

Risk: Searches and playback commands may expose viewing interests, media URLs, and local TV addresses.

Mitigation: Use trusted networks and devices, avoid sensitive queries where privacy matters, and share local TV addresses only with tooling you trust.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/al-one/skills/mcp-vods)
- [Project homepage](https://github.com/aahl/mcp-vods)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search and casting actions depend on external packages, source sites, local-network device configuration, and command execution by the host agent.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
