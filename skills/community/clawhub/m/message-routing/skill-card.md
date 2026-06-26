## Description: <br>
Manage how OpenClaw routes Telegram messages to different Claude model backends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josephtandle](https://clawhub.ai/user/josephtandle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect and change OpenClaw Telegram routing between Claude CLI and API model providers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Changing the routing model can persist in the OpenClaw config and affect Telegram message handling. <br>
Mitigation: Check current routing status, confirm the intended backend/provider, and verify gateway logs after changes. <br>
Risk: Restarting the gateway while switching providers may briefly interrupt message processing. <br>
Mitigation: Plan routing changes during an acceptable maintenance window and use fallback or restore commands when needed. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe persistent OpenClaw config changes and gateway restart or log-verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
