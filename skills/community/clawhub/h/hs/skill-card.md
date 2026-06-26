## Description: <br>
HardStop helps agents review shell commands and sensitive file reads, blocking dangerous actions and requiring confirmation for risky ones. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[frmoretto](https://clawhub.ai/user/frmoretto) <br>

### License/Terms of Use: <br>
CC-BY-4.0 <br>


## Use Case: <br>
Developers and agent operators use HardStop as a pre-execution safety layer for shell commands, package operations, infrastructure commands, and credential-adjacent file reads. It is intended to reduce accidental destructive actions and prompt explicit user decisions before high-risk operations proceed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may interrupt normal command execution and file-read workflows because it applies conservative checks. <br>
Mitigation: Install only when conservative guardrails are desired, and review blocked or warned actions before deciding whether to proceed. <br>
Risk: Using skip or off controls temporarily reduces or disables protection. <br>
Mitigation: Treat /hs skip and /hs off as sensitive actions and use them only after explicit user intent and risk review. <br>
Risk: Hook-based blocking depends on the separate local Hardstop plugin when deterministic enforcement is required. <br>
Mitigation: Review and install the Hardstop plugin before relying on hook behavior; use this skill as the instruction-layer guidance for agent reasoning. <br>


## Reference(s): <br>
- [HardStop on ClawHub](https://clawhub.ai/frmoretto/hs) <br>
- [Publisher profile](https://clawhub.ai/user/frmoretto) <br>
- [Hardstop plugin](https://github.com/frmoretto/hardstop) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands] <br>
**Output Format:** [Markdown with inline shell commands and decision prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May instruct the agent to stop, explain risk, request confirmation, suggest safer alternatives, or run local Hardstop plugin control commands after explicit user invocation.] <br>

## Skill Version(s): <br>
1.4.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
