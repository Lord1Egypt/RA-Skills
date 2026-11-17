## Description:

Controls Jellyfin media playback and supported TVs so an agent can search content, resume playback, manage sessions, and launch Jellyfin through Home Assistant, WebOS, or Android TV backends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[titunito](https://clawhub.ai/user/titunito)

### License/Terms of Use:

ISC

## Use Case:

Developers and home media server operators use this skill to let an agent control Jellyfin playback, pick up the next episode or resume a movie, send playback commands, and coordinate TV power or app launch across supported local backends.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The Android TV ADB path can turn user-controlled device or app values into host shell commands.

Mitigation: Review ADB_DEVICE and TV_JELLYFIN_APP before enabling direct ADB, restrict values to expected device addresses and app IDs, or change ADB execution to argument-based process calls before deployment.

Risk: Examples show Jellyfin and Home Assistant endpoints using plaintext HTTP while API keys, passwords, tokens, and TV pairing keys are sensitive.

Mitigation: Use HTTPS or a trusted encrypted tunnel, store secrets only in the skill environment configuration, and use dedicated least-privileged Jellyfin and Home Assistant credentials.

Risk: ADB and WebOS pairing grant broad control over a TV on the local network.

Mitigation: Enable these backends only on trusted networks, accept pairing prompts intentionally, and treat TV_CLIENT_KEY and ADB access as sensitive control credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/titunito/skills/jellyfin-control)
- [Artifact README](artifact/README.md)
- [Artifact SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, Guidance]

**Output Format:** [Markdown and terminal text with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires JF_URL and JF_API_KEY; optional TV and Home Assistant settings enable WebOS, Android TV, Wake-on-LAN, and Home Assistant control.]

## Skill Version(s):

1.3.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
