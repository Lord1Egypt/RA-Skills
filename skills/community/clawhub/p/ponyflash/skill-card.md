## Description:

Generate images, videos, speech audio, and music through the PonyFlash Python SDK, and guide local FFmpeg editing for clips, transcoding, audio extraction, frames, subtitles, and final renders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leothebravest](https://clawhub.ai/user/leothebravest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to route agent requests for AI media generation, model and account operations, file handling, and local FFmpeg-based media editing. It supports single-step generation or editing requests and multi-step production workflows that combine generated assets with local assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys could be exposed if entered into chat or stored in shared logs.

Mitigation: Configure PONYFLASH_API_KEY through a secret manager or local terminal and avoid pasting production credentials into agent conversations.

Risk: Sensitive media may be uploaded to PonyFlash for processing during cloud generation, file management, or reference-image workflows.

Mitigation: Use only media the user intends PonyFlash to process, and confirm consent before uploading private, regulated, or third-party content.

Risk: The skill can guide recharge actions, cloud file deletion, and local output overwrites.

Mitigation: Require explicit user approval before spending credits, deleting cloud files, or overwriting local files.

Risk: Runtime SDK installation, FFmpeg execution, and subtitle font downloads add local environment and supply-chain review requirements.

Mitigation: Use an isolated environment with a pinned PonyFlash SDK version, run dependency checks before FFmpeg work, and approve font downloads deliberately.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leothebravest/skills/ponyflash)
- [Publisher Profile](https://clawhub.ai/user/leothebravest)
- [PonyFlash](https://ponyflash.com)
- [Agent Skills Specification](https://agentskills.io/specification)
- [Operation Strategy](reference/operations.md)
- [Examples](reference/examples.md)
- [Available Models](reference/models/INDEX.md)
- [Files API Reference](reference/files.md)
- [Account API Reference](reference/account.md)
- [Subtitle Fonts](assets/fonts.md)
- [Default Subtitle Style](assets/subtitle-style.md)
- [Creative Playbooks](playbooks/INDEX.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with Python and shell command blocks, plus generated media file outputs when tasks complete]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May trigger PonyFlash API calls for cloud generation and local FFmpeg commands for media processing; generated outputs depend on user prompts, model parameters, API credits, and local FFmpeg capabilities.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter metadata says 0.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
