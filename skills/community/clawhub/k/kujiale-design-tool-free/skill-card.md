## Description:

分步式室内设计工具,完成户型确认到渲染出图,适合个人用户快速生成装修方案。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide an agent through a Chinese-language interior design workflow, including floor plan lookup or upload, style selection, automated layout, rendering, and panorama link generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run local scripts that are not bundled in the artifact.

Mitigation: Review the local ./scripts/*.js files before installation or execution, and use the skill only in a clean project where those scripts are trusted.

Risk: The workflow requires an access token and mentions a local .kjlconfig.json file.

Mitigation: Prefer a managed secret or environment variable, add local config files to .gitignore, restrict file permissions, and avoid passing long-lived tokens as command-line arguments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/kujiale-design-tool-free)
- [Publisher profile](https://clawhub.ai/user/thcjp)
- [Kujiale skills page](https://www.kujiale.com/skills)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to call local Node.js scripts and handle access tokens for the Kujiale design workflow.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
