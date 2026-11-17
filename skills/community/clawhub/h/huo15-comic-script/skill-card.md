## Description:

Generates structured Chinese comic storyboard script JSON from a one-line theme, including characters, scenes, dialogue, camera direction, and mood for genres such as xianxia, palace intrigue, wuxia, and zhiguai.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and agent operators use this skill to turn a brief Chinese-language story premise into a structured script.json for short-form guofeng comic or video production. Developers can also run the included CLI as a fallback generator and validator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared media-production helpers can send prompts or local media to external APIs when used.

Mitigation: Review the package before installing and remove or disable the shared media modules unless the broader media pipeline is intended.

Risk: The fallback script-generation path can call Anthropic when API credentials are configured.

Mitigation: Use direct agent-mode JSON generation or validation-only mode when external model calls are not intended, and provide ANTHROPIC_API_KEY only for approved use.

Risk: Cost and checkpoint helpers may write local tracking files during broader pipeline use.

Mitigation: Run the skill in a controlled project directory and review generated checkpoint or cost files when using the bundled pipeline helpers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zhaobod1/skills/huo15-comic-script)
- [Volcengine Seedance Documentation](https://www.volcengine.com/docs/82379/1520757)
- [Volcengine TTS Documentation](https://www.volcengine.com/docs/6561/97465)

## Skill Output:

**Output Type(s):** [Text, JSON, Code, Shell commands, Guidance]

**Output Format:** [Structured JSON script files and concise agent guidance, with optional CLI commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces script.json with title, style, genre, duration, characters, scenes, dialogue, camera, and mood; the fallback CLI may call Anthropic when ANTHROPIC_API_KEY is configured.]

## Skill Version(s):

0.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
