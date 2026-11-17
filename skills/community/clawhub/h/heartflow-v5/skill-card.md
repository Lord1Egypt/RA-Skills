## Description: <br>
HeartFlow is a local cognitive engine for AI agent pipelines that transforms user input into structured cognition, memory, emotion, psychology, philosophy, self-healing, decision, code, and consciousness signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yun520-1](https://clawhub.ai/user/yun520-1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to add a local cognitive preprocessing layer, MCP tools, memory retrieval, self-healing, reasoning, and decision-routing support to AI assistant workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports a broad local agent engine that under-discloses external API use, local server behavior, and privileged runtime features. <br>
Mitigation: Install only in an isolated test environment until the operator has reviewed the package behavior and intended runtime capabilities. <br>
Risk: The skill can persist memory and expose a localhost MCP HTTP service. <br>
Mitigation: Use a dedicated workspace, set MCP authentication intentionally, and avoid exposing localhost services beyond trusted local clients. <br>
Risk: Optional code execution, self-modification, environment-variable access, and external API paths can increase execution and data-exposure risk. <br>
Mitigation: Do not set HEARTFLOW_API_KEY, HEARTFLOW_MCP_TOKEN, HEARTFLOW_CODE_EXECUTOR_ENABLED, HEARTFLOW_ENABLE_SELF_MODIFICATION, or local API-key files unless those capabilities are explicitly required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yun520-1/skills/heartflow-v5) <br>
- [npm package](https://www.npmjs.com/package/@yun520-1/heartflow) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, structured text, JSON-like analysis objects, JavaScript code snippets, shell commands, and MCP tool responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist local memory/state, expose localhost MCP HTTP/SSE tools, and optionally use code execution or external API features when configured.] <br>

## Skill Version(s): <br>
5.8.6 (source: server release metadata, created 2026-07-08T08:35:57Z) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
