## Description: <br>
Automatically updates Clawdbot and installed skills once daily, runs through cron, applies available updates, and reports what changed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muguozi1](https://clawhub.ai/user/muguozi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and ClawHub users use this skill to schedule routine maintenance for a Clawdbot installation and its installed skills. It is intended for users who intentionally want unattended update checks and a concise summary of applied changes or failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended daily updates can change the core agent and all installed skills without per-update review. <br>
Mitigation: Use dry-run or notification-only mode first, restrict updates to trusted skills where possible, and keep backups before enabling automatic updates. <br>
Risk: A scheduled updater can continue running after installation if the user forgets about the cron job. <br>
Mitigation: Confirm the cron schedule after setup and keep the removal command available: `clawdbot cron remove "Daily Auto-Update"`. <br>
Risk: Update failures, permission issues, package conflicts, or network problems can leave the environment partially updated. <br>
Mitigation: Review each update summary, run diagnostic commands after failures, and intervene manually when the report identifies errors. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/muguozi1/muguozi1-openclaw-auto-updater) <br>
- [Clawdbot Updating Guide](https://docs.clawd.bot/install/updating) <br>
- [ClawdHub CLI](https://docs.clawd.bot/tools/clawdhub) <br>
- [Cron Jobs](https://docs.clawd.bot/cron) <br>
- [Agent Implementation Guide](references/agent-guide.md) <br>
- [Update Summary Examples](references/summary-examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, markdown] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces cron setup guidance, update commands, and human-readable update summaries.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
