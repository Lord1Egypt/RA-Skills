## Description:

AI解说大师 Narrator AI Skill helps agents use narrator-ai-cli to create AI movie and drama narration videos, browse media, BGM, voice, and template resources, manage narration tasks, and automate the script-to-video workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[4myhime](https://clawhub.ai/user/4myhime)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to guide an AI agent through Narrator AI CLI workflows for movie or short-drama narration videos, including resource selection, script generation, clip preparation, video composition, and task management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and runs an external narrator-ai-cli package.

Mitigation: Prefer the pinned release install path and review the upstream CLI before using it with sensitive media or production workflows.

Risk: The CLI uses a Narrator AI API key and may perform account or key operations.

Mitigation: Keep NARRATOR_APP_KEY private and ask the agent to confirm account and key actions before executing them.

Risk: Selected media and subtitle files can be uploaded to the Narrator AI cloud service for processing.

Mitigation: Confirm uploads before running file or task commands and avoid submitting sensitive media unless the cloud-service trust model is acceptable.

Risk: Bulk generation, paid processing, deletes, and account operations can have cost or data-loss impact.

Mitigation: Ask the agent to confirm costs, bulk generation, deletes, and account operations before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/4myhime/skills/narrator-ai-cli-skill)
- [narrator-ai-cli release install source](https://github.com/GridLtd-ProductDev/narrator-ai-cli/archive/refs/tags/v1.0.0.zip)
- [narrator-ai-cli repository](https://github.com/GridLtd-ProductDev/narrator-ai-cli)
- [Narrator AI API endpoint](https://openapi.jieshuo.cn)
- [Narrator AI resource preview](https://ceex7z9m67.feishu.cn/wiki/WLPnwBysairenFkZDbicZOfKnbc)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, JSON, files]

**Output Format:** [Markdown guidance with CLI commands and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill guides agents to request user confirmation before resource selection and task creation, use JSON CLI output for parsing, and return task identifiers or generated video links when available.]

## Skill Version(s):

1.0.2 (source: server release metadata, target metadata, SKILL.md frontmatter, plugin.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
