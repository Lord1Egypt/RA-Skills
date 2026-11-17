## Description:

Coordinates an OpenClaw multi-model coding workflow where Claude Code plans and reviews, Codex handles backend and infrastructure implementation, and Gemini handles frontend work through staged artifacts and a local orchestrator.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shennng](https://clawhub.ai/user/shennng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to coordinate full-stack implementation work across Claude Code, Codex, and Gemini while preserving staged plans, logs, test matrices, and review artifacts. It is intended for OpenClaw workflows that require OPSX or specification alignment before local code changes are made.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow asks users to persist API keys and run powerful model CLIs with access to the local repository, environment variables, and user credentials.

Mitigation: Use temporary or secret-manager based API keys, run the workflow in a dedicated workspace or container, and avoid storing secrets in .claude artifacts or commits.

Risk: Model-generated commands or diffs may modify sensitive files or introduce unintended behavior before review.

Mitigation: Review dry-run output, generated plans, diffs, and test results before execution or merge, and require explicit approval for destructive commands.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/shennng/skills/openclaw-claude-codex-workflow)
- [Model Routing Guide](references/model-routing.md)
- [Workflow Checklist](references/workflow-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and generated workflow artifact files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces staged planning, execution, verification, and review artifacts under .claude/ when used as documented.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
