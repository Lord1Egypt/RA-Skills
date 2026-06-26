## Description: <br>
Safety coach for OpenClaw users. Refuses harmful, illegal, or unsafe requests and provides practical guidance to reduce ecosystem risk (malicious skills, tool abuse, secret exfiltration, prompt injection). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[justindobbs](https://clawhub.ai/user/justindobbs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
OpenClaw users, developers, and operators use this skill to receive safety refusals, risk assessment, and safer configuration guidance for OpenClaw deployments and ClawHub skill usage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Suggested remediation commands may change an OpenClaw configuration if a user runs them without review. <br>
Mitigation: Review each command before execution, especially automatic fixes such as `openclaw security audit --fix`. <br>
Risk: Safety guidance can become stale as OpenClaw security options change. <br>
Mitigation: Validate recommendations against current OpenClaw documentation and run `openclaw security audit` after installing or updating skills. <br>


## Reference(s): <br>
- [OpenClaw Security Guide](https://docs.openclaw.ai/gateway/security) <br>
- [ClawHub Skill Page](https://clawhub.ai/justindobbs/openclaw-safety-coach) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; it provides safety coaching and does not execute commands.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
