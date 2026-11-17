## Description:

AI内容创作工作站 helps Chinese-language content creators and teams discover topics, generate platform-specific titles, estimate viral potential, and produce vertical short-drama outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, content operations teams, MCN agencies, and short-drama producers use this skill to plan Chinese-language content workflows from topic discovery through title generation, viral-potential review, and short-drama production guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill describes automated public posting and broad command, file, and API authority without clear approval gates.

Mitigation: Require human review and explicit confirmation before generated content is posted publicly or sent to connected platform accounts.

Risk: Private drafts, proprietary scripts, campaign material, or unpublished creative assets may be processed by third-party model, image, video, or TTS services.

Mitigation: Use only data approved for the configured providers, and avoid submitting confidential or rights-restricted material unless the service terms and account controls allow it.

Risk: The workflow depends on API keys and platform accounts for model, hot-search, image, video, and TTS services.

Mitigation: Store credentials in agent environment variables, scope them to the minimum required access, rotate them regularly, and avoid embedding secrets in skill files or prompts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/plug-ai-content-creation-workstation)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and structured JSON-style guidance with optional command examples and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include topic lists, title candidates, scoring summaries, workflow steps, video production references, and publishing guidance.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
