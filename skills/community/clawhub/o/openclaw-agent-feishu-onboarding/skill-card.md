## Description: <br>
Create OpenClaw agents and onboard Feishu routing with explicit multi-step confirmations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AbsoLinS](https://clawhub.ai/user/AbsoLinS) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to create OpenClaw agents, bind them to precise Feishu routes, validate local routing configuration, and prepare rollback steps after confirmed changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can read and update local OpenClaw and Feishu routing configuration. <br>
Mitigation: Run it only on machines where the user is authorized to manage OpenClaw and Feishu routing. <br>
Risk: Incorrect agentId, accountId, peer.kind, or peer.id values can route Feishu messages to the wrong agent. <br>
Mitigation: Review the final binding object before approving writes and run the included Feishu binding validation checks after changes. <br>
Risk: Raw openclaw.json output may expose sensitive account configuration. <br>
Mitigation: Avoid sharing raw configuration output and summarize only the fields needed for review. <br>


## Reference(s): <br>
- [OpenClaw Agent + Feishu Routing Commands](references/commands.md) <br>
- [OpenClaw Agent Feishu Onboarding Chinese Runbook](references/usage-zh.md) <br>
- [Feishu Binding Validator](scripts/validate_feishu_bindings.py) <br>
- [ClawHub Skill Page](https://clawhub.ai/AbsoLinS/openclaw-agent-feishu-onboarding) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit confirmations before proposing writes to local OpenClaw and Feishu routing state.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
