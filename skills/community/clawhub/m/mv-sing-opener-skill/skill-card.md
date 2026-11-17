## Description:

Guides an agent to plan and produce a 9:16 rap lip-sync video from one character image and a user-provided vocal track.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kongzichixiangjiao](https://clawhub.ai/user/kongzichixiangjiao)

### License/Terms of Use:

MIT-0

## Use Case:

External creators use the skill to plan a short rap concept, write lyrics and generation prompts, and assemble a portrait-format lip-sync video from their own image and recording.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploads can expose local media publicly, including unrelated files if upload paths are not constrained.

Mitigation: Use an isolated project workspace, constrain upload paths to that project, and stage only media approved for public access.

Risk: Uploader defaults can replace destination directories or delete source material, including on failed transfers.

Mitigation: Keep backups, disable directory replacement and source deletion, and restrict hosting-directory permissions. For the standalone uploader, use --keep-source; --no-purge-project alone does not preserve source files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kongzichixiangjiao/skills/mv-sing-opener-skill)
- [Prompting and video production guidance](references/06-提示词与出片.md)
- [Image, likeness, and copyright boundaries](references/合规红线.md)
- [Material uploader behavior and options](scripts/material-uploader/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, JSON configuration, Shell commands, Video file]

**Output Format:** [Markdown, JSON, shell commands, and a vertical video file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Short-form 9:16 video; each shot is limited to 30 seconds and longer vocals are split at phrase boundaries without speeding up the audio.]

## Skill Version(s):

3.1.4 (source: frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
