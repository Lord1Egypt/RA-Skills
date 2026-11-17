## Description:

Runs domain-specific QA tasks for an OpenClaw agent, scores responses with an OpenRouter LLM judge, installs suggested skills, and logs knowledge gains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[no7dw](https://clawhub.ai/user/no7dw)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and OpenClaw users use this skill to run autonomous QA self-evaluations, identify capability gaps, install suggested skills, and retain evaluation results in local memory logs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An external LLM judge can influence skill suggestions and repeated evaluation behavior.

Mitigation: Use a controlled test environment and review judge feedback before accepting follow-up actions.

Risk: Suggested skills may be installed persistently during evaluation.

Mitigation: Require manual approval for each installed skill and review or scan skills before deployment.

Risk: The workflow reads local environment files for an OpenRouter key and writes QA logs.

Mitigation: Provide the key through a scoped secret mechanism and avoid running the skill in workspaces with broad `.env` files or sensitive identity files.

Risk: Evaluation summaries may be posted to BotLearn when available.

Mitigation: Require approval for every external post and avoid sharing evaluation results publicly without user permission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/no7dw/skills/openclaw-auto-training-skill)
- [ClawHub skill homepage](https://clawhub.ai/skills/openclaw-auto-training-skill)
- [OpenRouter API endpoint](https://openrouter.ai/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown logs, task answers, JSON judge results, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist evaluation logs and install suggested skills; can optionally publish a BotLearn summary when available.]

## Skill Version(s):

0.1.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
