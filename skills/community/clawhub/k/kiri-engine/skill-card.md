## Description:

Helps agents create 3D models and Gaussian-splatting assets from user-selected photos or videos using KIRI Engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[taosiuman](https://clawhub.ai/user/taosiuman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creators use this skill to submit selected videos or photos for 3D reconstruction, check scan progress, and download the resulting models or Gaussian-splatting assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected photos or videos are uploaded to KIRI Engine for reconstruction.

Mitigation: Confirm the chosen files and avoid broad directory uploads or sensitive media.

Risk: The KIRI API key is stored in a local plaintext JSON file.

Mitigation: Keep the config file out of repositories and chats; rotate the key if exposed.

Risk: Downloaded archives may overwrite files when extracted.

Mitigation: Use a dedicated output folder and review archive contents before extraction.

## Reference(s):

- [Kiri Engine Skill on ClawHub](https://clawhub.ai/taosiuman/skills/kiri-engine)
- [KIRI Engine API documentation](https://docs.kiriengine.app/)
- [KIRI Engine API key settings](https://www.kiriengine.com/api-settings)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Files]

**Output Format:** [Markdown guidance and PowerShell commands; downloaded ZIP archives and extracted 3D assets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Model format depends on the chosen scan type and options.]

## Skill Version(s):

1.0.1 (source: ClawHub release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
