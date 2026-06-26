## Description: <br>
OptimoClaw analyzes OpenClaw configuration and session usage data to recommend cost-effective token usage and model tuning changes with clear trade-offs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marc4211](https://clawhub.ai/user/marc4211) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to inspect OpenClaw agent configuration and session usage, estimate token costs, and prepare user-reviewed configuration changes that reduce spend while preserving needed capability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to inspect OpenClaw configuration and usage output that may include profile names, model identifiers, gateway connection details, token counts, and session metadata. <br>
Mitigation: Use it only where sharing that operational data with the agent is acceptable, and avoid including unrelated secrets or credentials. <br>
Risk: Suggested openclaw config set commands can change agent cost, quality, or behavior if executed without review. <br>
Mitigation: Review each command and trade-off before running it, especially in shared or production OpenClaw environments. <br>


## Reference(s): <br>
- [OptimoClaw on ClawHub](https://clawhub.ai/marc4211/optimoclaw-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with cost analysis, trade-offs, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommendations are advisory and require user review before execution.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence, released 2026-04-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
