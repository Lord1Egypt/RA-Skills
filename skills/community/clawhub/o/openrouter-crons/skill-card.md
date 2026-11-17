## Description:

Collaboratively migrate specific OpenClaw cron jobs onto popular OpenRouter models. Audit cron usage, fetch the current OpenRouter rankings via curl, propose top 4 cheap models, edit the chosen crons, and verify by running them plus checking OpenRouter usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrmps](https://clawhub.ai/user/mrmps)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to audit OpenClaw cron usage, choose cheaper popular OpenRouter models with user approval, update selected cron jobs, and verify each migration with live runs and cost checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenRouter API keys can be exposed in command output, chat transcripts, shell history, or logs during setup and credential checks.

Mitigation: Use presence-only credential checks, avoid pasting API keys into chat, and avoid passing secrets directly as command-line arguments.

Risk: Cron model edits can disrupt scheduled jobs or reduce output quality if the replacement model is unsuitable.

Mitigation: Approve each cron edit only after confirming the old model, new model, intended outcome, verification run, and rollback path.

Risk: Model recommendations can become stale because the skill relies on current OpenRouter rankings and pricing.

Mitigation: Fetch live OpenRouter model rankings before recommending models and present multiple inexpensive options with trade-offs.

## Reference(s):

- [OpenClaw cron CLI](https://docs.openclaw.ai/cli/cron)
- [OpenClaw cron concepts](https://docs.openclaw.ai/automation/cron-jobs)
- [OpenClaw and OpenRouter integration](https://openrouter.ai/docs/guides/coding-agents/openclaw-integration)
- [OpenRouter rankings API](https://openrouter.ai/api/v1/models?orderby=rank)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cron model mappings, verification results, rollback notes, and OpenRouter cost observations.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
