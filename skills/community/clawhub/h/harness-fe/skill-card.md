## Description: <br>
Debug, inspect, and drive frontend apps instrumented with the Harness-FE Vite/Webpack plugin. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paul-leo](https://clawhub.ai/user/paul-leo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to connect an agent to a Harness-FE MCP daemon, inspect live browser state and telemetry, correlate behavior with frontend source files, and guide fixes for UI bugs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can expose development browser telemetry, screenshots, recordings, storage changes, network traces, and source metadata to the Harness-FE daemon and connected agent. <br>
Mitigation: Use it only on projects and sessions where that visibility is acceptable, and avoid shared machines or sensitive browser sessions. <br>
Risk: Captured Harness-FE data can include sensitive values in local storage, network traces, replay data, or non-password form fields. <br>
Mitigation: Treat data under ~/.harness/ as confidential and avoid pasting recordings or trace excerpts into untrusted contexts. <br>
Risk: The skill includes page evaluation workflows that can run JavaScript in the user's browser page. <br>
Mitigation: Do not evaluate untrusted code from console output, network responses, user input, or third-party sources. <br>


## Reference(s): <br>
- [Harness-FE documentation](https://harness-fe.com/) <br>
- [Harness-FE documentation (Simplified Chinese)](https://harness-fe.com/zh/) <br>
- [Harness-FE integrations](https://harness-fe.com/integrations/) <br>
- [ClawHub package page](https://clawhub.ai/paul-leo/harness-fe) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, configuration snippets, and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include browser telemetry summaries, source references, screenshot observations, and replay guidance when the Harness-FE daemon is connected.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
