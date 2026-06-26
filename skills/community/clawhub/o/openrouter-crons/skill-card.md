## Description: <br>
Collaboratively migrate specific OpenClaw cron jobs onto popular OpenRouter models. Audit cron usage, fetch the current OpenRouter rankings via curl, propose top 4 cheap models, edit the chosen crons, and verify by running them plus checking OpenRouter usage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrmps](https://clawhub.ai/user/mrmps) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to review scheduled cron usage, choose approved OpenRouter model substitutions, update selected jobs, and verify runtime and cost impact. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: OpenRouter credentials or local OpenClaw auth data could be exposed while checking provider access. <br>
Mitigation: Confirm only whether credentials exist, avoid printing .env or auth profile contents, and use a secure secret entry method for API keys. <br>
Risk: Cron edits can change scheduled job behavior or move a job to an unsuitable model. <br>
Mitigation: Require explicit approval for each cron-to-model mapping, show the updated payload, run the job after editing, and revert if verification fails. <br>
Risk: Manual cron runs and OpenRouter API calls may execute real workflows or incur usage costs. <br>
Mitigation: Run only approved jobs, surface errors promptly, and review OpenRouter credits or activity after verification when cost visibility is needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrmps/openrouter-crons) <br>
- [OpenClaw cron CLI](https://docs.openclaw.ai/cli/cron) <br>
- [OpenClaw cron concepts](https://docs.openclaw.ai/automation/cron-jobs) <br>
- [OpenClaw and OpenRouter integration](https://openrouter.ai/docs/guides/coding-agents/openclaw-integration) <br>
- [OpenRouter model rankings API](https://openrouter.ai/api/v1/models?orderby=rank) <br>
- [OpenRouter credits API](https://openrouter.ai/api/v1/credits) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command blocks and migration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include approved cron-to-model mappings, verification results, and OpenRouter cost or activity summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
