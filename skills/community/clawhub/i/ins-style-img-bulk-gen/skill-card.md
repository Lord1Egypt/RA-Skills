## Description:

Generate batches of Instagram-aesthetic images by composing prompts from an element library, dispatching them to configured image-generation skills, and optionally post-processing outputs into collages or social-cover layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mebusw](https://clawhub.ai/user/mebusw)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, marketers, and agent users can use this skill to generate batches of INS-style lifestyle, Xiaohongshu, WeChat cover, flat-lay, and scene-based marketing visuals. Developers can also use its scripts to compose 2x2 collages and add text overlays to generated images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be sent to configured image-generation tools or providers.

Mitigation: Confirm provider credentials, privacy expectations, and generation costs before running batches.

Risk: The workflow can create timestamped image folders under Downloads and generate multiple outputs per run.

Mitigation: Confirm output count and destination path before large batches, and review generated files before sharing.

Risk: The post-processing scripts may require Pillow to be installed locally.

Mitigation: Install dependencies in a virtual environment when possible and review package installation commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mebusw/skills/ins-style-img-bulk-gen)
- [Server-resolved GitHub source](https://github.com/mebusw/ins-style-img-bulk-gen)
- [README](README.md)
- [INS style elements](references/ins-style-elements.md)
- [Skill/script handoff playbook](HANDOFF-PLAYBOOK.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with prompt text, shell commands, and generated local image files from configured tools]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create timestamped image folders under Downloads and use Pillow-based scripts for collage composition and text overlays.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
