## Description: <br>
Set up an AI agent as an Overnight Software Factory operator that receives support-ticket assignments, analyzes issues, dispatches coding subagents, opens pull requests, and notifies a human reviewer. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[z-team-alpha](https://clawhub.ai/user/z-team-alpha) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to configure an OpenClaw agent as an autonomous support ticket-to-PR operator. It helps set up cron-based ticket intake, GitHub polling, subagent dispatch, pull-request creation, and human review notification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recurring agents can receive broad repository, email, and credential authority. <br>
Mitigation: Use a dedicated isolated bot workspace, a separate low-privilege GitHub account, fine-grained tokens, a dedicated inbox, and repository allowlists. <br>
Risk: Credential setup examples include plaintext global credential storage and token-in-URL Git commands. <br>
Mitigation: Avoid plaintext global credential storage and token-in-URL Git commands; prefer scoped secrets and credential handling that can be rotated or revoked quickly. <br>
Risk: Autonomous ticket-to-PR operation can create unintended code changes if merged without review. <br>
Mitigation: Require branch protections, mandatory PR review, and non-production testing before allowing the workflow to process real tickets. <br>
Risk: A recurring cron job can continue acting after misconfiguration or unexpected behavior. <br>
Mitigation: Keep an easy way to disable the cron and monitor dispatch logs, delivery status, and consecutive error counts. <br>


## Reference(s): <br>
- [Overnight Factory ClawHub Page](https://clawhub.ai/z-team-alpha/overnight-factory) <br>
- [Cron Job Prompt Template](references/cron-prompt.md) <br>
- [Ticket Pipeline: Subagent Instructions](references/ticket-pipeline.md) <br>
- [Lessons Learned in Production](references/lessons-learned.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration snippets, API call examples, and JSON state examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup instructions and prompt templates for an agent-operated ticket pipeline; it does not itself execute the pipeline.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
