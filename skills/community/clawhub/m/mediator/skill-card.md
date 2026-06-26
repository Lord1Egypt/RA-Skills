## Description: <br>
Intercept and filter communications from difficult contacts by stripping emotion, extracting facts, and drafting neutral responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dylntrnr](https://clawhub.ai/user/dylntrnr) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to configure mediated contacts, process incoming email or iMessage content, and produce facts-only summaries or neutral response drafts for difficult communications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private communications may be processed by external tools or an external LLM and retained in local plaintext configuration, state, or logs. <br>
Mitigation: Review the generated config before use, verify gog-read.sh, imsg, and llm are trusted and configured for the intended accounts, and limit processing to communications appropriate for those tools. <br>
Risk: Default configuration includes hard-coded Gmail account examples that may not belong to the installer. <br>
Mitigation: Remove or replace the hard-coded Gmail accounts before running checks or enabling scheduled monitoring. <br>
Risk: Automatic responses could send inappropriate replies in legal, financial, child-related, or otherwise sensitive matters. <br>
Mitigation: Keep response mode set to draft for sensitive matters and manually review messages and suggested responses before sending. <br>
Risk: Scheduled cron or heartbeat checks can create continuous monitoring of private communications. <br>
Mitigation: Enable cron or heartbeat monitoring only after the user intentionally confirms the accounts, contacts, notification channel, and retention behavior. <br>


## Reference(s): <br>
- [Mediator Prompts Reference](artifact/references/prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and command-line text with JSON summaries from message processing scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces summaries, action-required flags, suggested neutral responses, contact configuration guidance, and local CLI status output.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
