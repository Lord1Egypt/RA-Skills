## Description: <br>
Diagnoses OpenClaw node connection and pairing failures across QR, setup-code, manual connection, local Wi-Fi, VPS, tailnet, and public gateway routes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jackhua6](https://clawhub.ai/user/jackhua6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to diagnose OpenClaw companion-app connection failures, determine the intended node-to-gateway route, and resolve pairing or authentication problems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup-code JSON, tokens, URLs, and device identifiers may expose sensitive connection or pairing details. <br>
Mitigation: Treat diagnostic outputs as sensitive and avoid sharing them beyond the trusted troubleshooting context. <br>
Risk: Approving the wrong pending device could authorize an unintended client. <br>
Mitigation: Confirm the pending device is yours before approving it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May ask concise clarifying questions before giving a diagnosis when route or error details are ambiguous.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
