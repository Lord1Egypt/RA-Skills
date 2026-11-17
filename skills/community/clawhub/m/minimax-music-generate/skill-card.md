## Description:

Generates MiniMax music and lyrics, supports structured lyric sections, and can save generated MP3 audio locally.

This skill is ready for commercial/non-commercial use.

## Publisher:

[silingyuan0](https://clawhub.ai/user/silingyuan0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to generate song lyrics, create music from lyrics and style descriptions, check generation status, and save MP3 output from the MiniMax API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The downloader can fetch arbitrary URLs and overwrite local files.

Mitigation: Run the skill in a low-permission workspace, save output under a dedicated folder, and avoid untrusted download URLs until downloads are restricted to MiniMax-generated media and overwrite protection is confirmed.

Risk: The skill requires a MiniMax API key.

Mitigation: Use only a MiniMax API key intended for this skill and avoid exposing broader credentials in the environment.

## Reference(s):

- [MiniMax Music API Reference](references/api.md)
- [ClawHub skill page](https://clawhub.ai/silingyuan0/skills/minimax-music-generate)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, files, guidance]

**Output Format:** [Markdown guidance with inline commands, generated lyric text, JSON task status, and MP3 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and supports MINIMAX_REGION for China or international API endpoints.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
