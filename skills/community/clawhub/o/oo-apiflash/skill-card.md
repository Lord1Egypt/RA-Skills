## Description:

Use ApiFlash through the OOMOL-connected account to capture website screenshots, check quota, and retrieve screenshot metadata.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to capture website screenshots with ApiFlash, check screenshot quota and reset time, and retrieve metadata for previously generated screenshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The CLI may automatically install additional agent skills that are not described by this skill.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 for every invocation when only ApiFlash is intended, and review any skills installed by the CLI.

Risk: The automatic download-and-execute fallback and remote connector implementations are unverified.

Mitigation: Prefer a reviewed, pinned CLI installation and review the remote components before use.

Risk: Screenshot requests may use account quota or incur costs.

Mitigation: Connect only the intended account and check screenshot quota before making requests.

## Reference(s):

- [ApiFlash homepage](https://apiflash.com)
- [ApiFlash API documentation](https://apiflash.com/documentation)
- [OOMOL oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [JSON action responses with screenshot URLs, quota details, or screenshot HTTP metadata, plus concise usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The available actions capture screenshots, retrieve quota and reset information, and read metadata for previously returned screenshot URLs.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
