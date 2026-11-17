## Description:

Image Compress helps agents compress single images or folders, convert image formats, resize images, and choose output presets through a local Node.js and sharp workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[justzerox](https://clawhub.ai/user/justzerox)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to reduce image file size, convert JPG, PNG, WebP, AVIF, HEIC, and related formats, resize images, and batch-process folders for web, email, and sharing workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup path runs npm install for a local Node/sharp image tool and processes files or folders selected by the user.

Mitigation: Review dependencies, prefer a lockfile or pinned dependency versions, and run the skill only on intended local image paths.

Risk: The environment output includes Linux curl-to-sudo-bash Node installation commands.

Mitigation: Do not copy those privileged shell pipeline commands; install Node.js through official Node.js downloads or trusted operating-system package-manager instructions.

## Reference(s):

- [Image Compress technical reference](references/technical.md)
- [sharp documentation](https://sharp.pixelplumbing.com)
- [ClawHub skill page](https://clawhub.ai/justzerox/skills/image-compress)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration examples, and compression result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local file outputs in a configured compressed-images directory and reports original size, compressed size, savings, and output path.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
