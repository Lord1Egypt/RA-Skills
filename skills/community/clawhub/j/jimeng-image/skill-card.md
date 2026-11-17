## Description:

Generate images on Jimeng (即梦 / jimeng.jianying.com) through an OpenClaw-managed browser with prompt entry, ratio selection, result inspection, and local downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haohao-ui](https://clawhub.ai/user/haohao-ui)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to operate Jimeng image generation through an OpenClaw-managed browser, including prompt entry, ratio and option selection, generation monitoring, and local downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser operation can encounter login gates, approval prompts, payment prompts, or exhausted credits.

Mitigation: Stop and report the visible Jimeng state instead of retrying or switching services.

Risk: Generated images are saved to local storage.

Mitigation: Use a dedicated browser profile where possible, report saved paths clearly, and clean up files when directed.

Risk: Jimeng UI references can become stale during generation or navigation.

Mitigation: Take fresh browser snapshots before important interactions and use the current live labels.

## Reference(s):

- [ClawHub Jimeng Image skill page](https://clawhub.ai/haohao-ui/skills/jimeng-image)
- [Jimeng image generation entry page](https://jimeng.jianying.com/ai-tool/home/?workspace=0&type=image)

## Skill Output:

**Output Type(s):** [guidance, shell commands, files]

**Output Format:** [Markdown guidance with inline shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May download generated image files locally and report absolute paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
