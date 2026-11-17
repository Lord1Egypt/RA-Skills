## Description:

Generates prompt configuration files for Xiaohongshu-style lucky wallpapers, wealth avatars, healing cards, and career-themed image cards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhangxiaox101](https://clawhub.ai/user/zhangxiaox101)

### License/Terms of Use:

MIT

## Use Case:

External creators and developers use this skill to create structured prompt records for lucky, wealth, healing, and career-themed wallpaper or social image generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill description can imply complete image generation and automatic publishing, but the included script produces prompt configuration records.

Mitigation: Treat outputs as prompt/config inputs, review generated records, and require explicit confirmation before any external image API call or publishing action.

Risk: Batch generation count is not bounded by the included script.

Mitigation: Use conservative generation counts or add count limits before high-volume batch runs.

Risk: External image APIs and Xiaohongshu publishing may involve account, content, or compliance decisions.

Mitigation: Require account selection, content review, and user approval before connecting generated prompts to external services.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhangxiaox101/skills/lucky-wallpaper-generator)
- [Publisher profile](https://clawhub.ai/user/zhangxiaox101)

## Skill Output:

**Output Type(s):** [text, JSON, configuration, shell commands]

**Output Format:** [JSON configuration files with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces ready_for_generation prompt records for external image generation rather than finished image files.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
