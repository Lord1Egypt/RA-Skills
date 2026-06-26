## Description: <br>
Provides periodic progress self-checks with Feishu notifications, task ledger management, auto-reactivation of stale tasks, and summary reporting for OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ulquoirra](https://clawhub.ai/user/Ulquoirra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to schedule progress checks, maintain a local task ledger, send Feishu progress updates, and expose Markdown self-check artifacts for Webchat pull workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled background automation can run stored local commands without an interactive prompt. <br>
Mitigation: Enable cron jobs only when this behavior is intended, keep auto-reactivation disabled or tightly limited, and review every stored next command before marking a task auto=true. <br>
Risk: Progress summaries and task details may be sent to the configured Feishu recipient. <br>
Mitigation: Verify the Feishu account and target before enabling notifications, and avoid storing sensitive task details or commands in the ledger. <br>
Risk: Auto-reactivation includes weak safeguards and may execute overly broad local commands. <br>
Mitigation: Use narrow commands, keep max_reactivate_per_run low, and inspect the ledger and generated artifacts regularly. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Ulquoirra/progress-selfcheck) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Configuration defaults](artifact/config/progress_selfcheck_config.json) <br>
- [Cron job snippet](artifact/templates/cron_jobs_snippet.json) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown status summaries, JSONL task ledger entries, shell command invocations, and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes progress self-check Markdown artifacts under the configured output directory and can send configured Feishu messages.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
