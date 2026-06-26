## Description: <br>
Precision decisioning, agentic trust, and verifiable identity for autonomous agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[knuckles-stack](https://clawhub.ai/user/knuckles-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers using OpenClaw use this plugin to route high-risk tool calls through Kevros governance for pre-execution verification and post-execution attestation. Agents can also call registered tools to verify an action or look up an agent trust passport. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-risk tool inputs and execution summaries may be sent to an external governance service by default. <br>
Mitigation: Configure an explicit API key and non-identifying agentId, avoid sending secrets or private file contents through governed tools, narrow highRiskTools to the intended scope, and consider disabling autoAttest in sensitive workspaces. <br>
Risk: Remote governance decisions can block high-risk tool use. <br>
Mitigation: Choose the enforcement mode deliberately, test policies in advisory mode before enforcing them, and document operator approval or rollback procedures for blocked workflows. <br>
Risk: CLAMP decisions should not be assumed to rewrite tool actions unless independently confirmed. <br>
Mitigation: Treat CLAMP as a constrained decision that requires caller-side validation of the applied action before execution. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/knuckles-stack/openclaw-plugin) <br>
- [Artifact README](README.md) <br>
- [Kevros governance gateway](https://governance.taskhawktech.com) <br>
- [Kevros agent discovery card](https://governance.taskhawktech.com/.well-known/agent.json) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Configuration, JSON, Guidance] <br>
**Output Format:** [OpenClaw hook decisions, JSON API responses, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May block, allow, or log high-risk tool calls depending on enforcement mode and gateway response.] <br>

## Skill Version(s): <br>
0.3.9 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
