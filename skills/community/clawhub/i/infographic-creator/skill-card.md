## Description:

Generate modern operator-style social-media infographics for Twitter, LinkedIn, and Instagram using OpenAI gpt-image-2.

This skill is ready for commercial/non-commercial use.

## Publisher:

[berthelol](https://clawhub.ai/user/berthelol)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, founders, and agent users use this skill to turn social-media ideas into branded infographic prompts, reusable prompt files, and rendered image assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompt files, logos, screenshots, and avatars can be uploaded to OpenAI, and the CLI can read a caller-provided prompt file.

Mitigation: Review prompt-file paths before execution, keep sensitive files out of prompt and asset directories, and only use assets that are acceptable to upload to OpenAI.

Risk: Image generation uses a billable API and can incur unexpected cost if rerun repeatedly.

Mitigation: Use a project-scoped OpenAI API key with spending limits and monitor usage during operational runs.

Risk: Dependencies are listed by package name without pinned versions.

Mitigation: Pin and review the openai and cairosvg dependency versions before operational use.

## Reference(s):

- [Infographic Skill Definition](artifact/SKILL.md)
- [Visual Style Guide](artifact/references/style-guide.md)
- [Prompt Templates](artifact/references/prompt-templates.md)
- [Style Tokens](artifact/references/style.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with shell and Python snippets, saved prompt files, configuration JSON, and generated PNG files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses OpenAI image APIs, supports 4:5, 1:1, and 16:9 formats, and stores prompts, assets, and outputs under an infographics workspace.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
