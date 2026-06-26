## Description: <br>
Builds, approves, schedules, monitors, and reacts to multi-channel B2B outreach campaigns with per-touchpoint review, reply handling, campaign management, opt-out handling, and anti-spam caps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[milstan](https://clawhub.ai/user/milstan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Sales and growth users use this skill to plan, draft, approve, schedule, monitor, and revise B2B outreach across channels while preserving opt-out and anti-spam controls. Developers and operators may also use it to coordinate campaign state, response classification, and connected-channel execution in an OpenClaw environment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate outreach through connected business and messaging accounts. <br>
Mitigation: Install only when that behavior is intended, restrict connected-account scopes, and keep per-touchpoint review enabled unless scheduled sending is explicitly accepted. <br>
Risk: Recurring listeners and campaign actions can mutate campaign records, opt-outs, archives, and schedules. <br>
Mitigation: Regularly inspect active campaigns, listeners, opt-outs, archives, and connected-account permissions. <br>
Risk: The skill references local scripts and channel plugins that may affect campaign execution boundaries. <br>
Mitigation: Verify the referenced local scripts and channel plugins before use. <br>


## Reference(s): <br>
- [Outclaw Homepage](https://github.com/leadbay/outclaw) <br>
- [Campaign Engine Reference](references/campaign-engine.md) <br>
- [Channel Adapters Reference](references/channel-adapters.md) <br>
- [Response Listener Reference](references/response-listener.md) <br>
- [LinkedIn CLI Plugin](https://clawhub.ai/arun-8687/linkedin-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown plans and dashboards with inline shell commands and structured campaign data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create campaign records, scheduled task instructions, message drafts, reply classifications, opt-out updates, and approval prompts.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter version: 2.1.33) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
