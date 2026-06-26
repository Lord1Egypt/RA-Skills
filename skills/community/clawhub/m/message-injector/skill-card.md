## Description: <br>
OpenClaw plugin that prepends custom text to every user message before it reaches the agent. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Harukaon](https://clawhub.ai/user/Harukaon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and workspace operators use this skill to enforce persistent context, reminders, or policy text before agent replies across OpenClaw channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently add operator-chosen instructions to every user message across a workspace. <br>
Mitigation: Install only in controlled workspaces, keep injected text visible to affected users, and confirm a disable or rollback path before enabling it on shared channels. <br>
Risk: Injected text could override user intent or weaken expected safeguards if misconfigured. <br>
Mitigation: Avoid content that overrides user intent or disables safeguards, and review configured prependText before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Harukaon/message-injector) <br>
- [Publisher profile](https://clawhub.ai/user/Harukaon) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Prepended text context configured through JSON and applied to user messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Applies only when enabled and prependText is configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
