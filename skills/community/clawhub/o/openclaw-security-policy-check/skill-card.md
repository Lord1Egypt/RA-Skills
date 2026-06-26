## Description: <br>
Automates security audits for OpenClaw gateway configurations by checking key security settings and running the OpenClaw deep security audit. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ASantsSec](https://clawhub.ai/user/ASantsSec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect OpenClaw gateway configuration before deployment or during routine security checks, identify risky settings, and review audit findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads local OpenClaw gateway configuration and invokes the OpenClaw CLI from PATH, so audit output may contain sensitive local security context. <br>
Mitigation: Install only when the local OpenClaw CLI is trusted, run it in an appropriate terminal environment, and treat terminal audit output as potentially sensitive. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text report with configuration findings and recommended actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only audit helper; does not automatically modify OpenClaw configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
