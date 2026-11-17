## Description:

Mmx helps agents use the MiniMax CLI for text chat, image and video generation, speech synthesis, music composition, vision analysis, web search, and related configuration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ariffazil](https://clawhub.ai/user/ariffazil)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use Mmx to generate and analyze multimodal content with the MiniMax CLI after authenticating with a MiniMax API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive prompts, private media, or paid API credentials may be sent through MiniMax workflows if users run commands without review.

Mitigation: Review prompts and media before use, prefer secret-safe authentication instead of putting API keys in shell commands, and avoid sending private content unless approved.

Risk: Generated media outputs may overwrite or mix with existing local files when output paths are reused.

Mitigation: Direct generated media to a dedicated output folder and use unique filenames for image, video, speech, and music commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ariffazil/skills/mmx)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the mmx CLI and MiniMax authentication; generated media and files are written by the CLI according to command options.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
