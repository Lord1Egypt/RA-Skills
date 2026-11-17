## Description:

Uses Nano Banana 2 through AI Hive to generate character-consistent images for brand IP, mascots, virtual characters, picture books, social content, sticker sets, comics, and sequential scenes from reference images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, brand teams, and developers use this skill to turn approved character reference images into consistent asset sheets, social posts, sticker batches, outfit variations, and storyboard images while preserving identity cues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses an AI Hive API key and can send it to a base URL controlled by command-line flags, environment variables, or the local config file.

Mitigation: Use only trusted AI Hive endpoints, keep AI_HIVE_BASE_URL and ~/.ai-hive/config.json under user control, and prefer a dedicated API key with limited balance or permissions.

Risk: Installing dependencies into a shared Python environment can affect other local tools.

Mitigation: Install requests and run the skill inside a virtual environment.

Risk: Reference images are uploaded to AI Hive before generation.

Mitigation: Use approved, authorized source images and avoid uploading sensitive or unlicensed IP.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-character-consistency)
- [AI Hive access page](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance with bash commands; generated images are downloaded as PNG files or task JSON when downloads are disabled.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires at least one reference image for generation and supports batch size, routing mode, model parameters, output directory, and no-download options.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact CHANGELOG top entry lists 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
