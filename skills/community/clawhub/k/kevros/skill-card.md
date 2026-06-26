## Description: <br>
Precision decisioning, agentic trust, and verifiable identity for autonomous agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[knuckles-stack](https://clawhub.ai/user/knuckles-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this OpenClaw plugin to route high-risk tool calls through Kevros governance checks before execution and to query verification or trust-passport data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin sends tool-call data to a third-party governance service by default. <br>
Mitigation: Use only after reviewing the gateway's retention, access, and compliance posture; avoid secrets, customer data, private file contents, and regulated workloads unless approved. <br>
Risk: The third-party service can block local high-risk tool actions in enforcement mode. <br>
Mitigation: Use advisory mode during evaluation and explicitly configure enforcement behavior before production use. <br>
Risk: Post-execution attestation may include sensitive information from truncated tool output summaries. <br>
Mitigation: Disable autoAttest where sensitive outputs may appear, or sanitize outputs before attestation. <br>
Risk: The plugin may auto-provision a free-tier API key if KEVROS_API_KEY is not set. <br>
Mitigation: Set an explicit non-sensitive agentId and API key to avoid implicit signup behavior. <br>


## Reference(s): <br>
- [ClawHub package page](https://clawhub.ai/knuckles-stack/kevros) <br>
- [Kevros governance gateway](https://governance.taskhawktech.com) <br>
- [Kevros MCP endpoint](https://governance.taskhawktech.com/mcp/) <br>
- [TaskHawk pricing](https://www.taskhawktech.com/pricing) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, API calls, Configuration, Guidance] <br>
**Output Format:** [JSON responses and OpenClaw hook allow/block results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May send tool inputs and up to 500 characters of tool output summary to the Kevros governance gateway when attestation is enabled.] <br>

## Skill Version(s): <br>
0.4.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
