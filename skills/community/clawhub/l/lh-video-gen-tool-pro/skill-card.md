## Description:

企业级竖版短视频批量生成系统，支持多模板、多语言、品牌定制、团队协作与自动化工作流，提升内容生产效率。

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, content teams, and automation teams use this skill to plan and run batch vertical short-video production workflows with templates, multilingual voice/text handling, brand assets, quality checks, and CI/CD-style automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad read, write, and command-execution authority for local video-production workflows.

Mitigation: Use it only for explicit video-production tasks in a prepared workspace, and review generated shell commands before execution.

Risk: Video generation may involve local project assets, output files, TTS services, and platform credentials.

Mitigation: Store credentials in environment variables or a secret manager, avoid hardcoding secrets, and keep generated outputs free of tokens or sensitive data.

Risk: Setup and automation examples may include privileged or CI commands that can affect the host environment.

Mitigation: Run setup commands only in isolated CI or a prepared environment, and avoid privileged package installation unless explicitly approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/lh-video-gen-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code, shell commands, configuration snippets, and JSON-style status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or modify local video project files and propose commands for Python, FFmpeg, batch generation, quality checks, and CI/CD workflows.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
