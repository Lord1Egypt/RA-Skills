## Description: <br>
OC-Flow gives OpenClaw agents deterministic workflow control with YAML playbooks for conditional branches, loops, waits, state management, scripts, LLM calls, skill calls, subagents, HTTP requests, and messaging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wlmh110](https://clawhub.ai/user/wlmh110) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to define, validate, execute, resume, and monitor deterministic YAML automation workflows for office, operations, assistant, research, notification, and integration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workflow YAML can run local code, make network requests, send messages, and access OpenClaw session files with the user's permissions. <br>
Mitigation: Install and run only trusted workflows; review every script, code, HTTP, message, agent, skill, and subagent step before execution. <br>
Risk: Workflows may expose sensitive environment variables or session data to scripts, network calls, agents, or messages. <br>
Mitigation: Avoid running third-party YAML with sensitive environment variables or private session data available, and treat workflow files like executable code. <br>
Risk: The security verdict is suspicious because this is a real automation skill with broad workflow actions and limited containment. <br>
Mitigation: Use the skill only in environments where the workflow actions are expected, auditable, and acceptable for the user's data and account permissions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wlmh110/openclaw-workflow) <br>
- [OpenClaw Workflow reference](artifact/references/readme.md) <br>
- [Basic workflow example](artifact/references/examples/basic_test.yaml) <br>
- [Comprehensive workflow example](artifact/references/examples/comprehensive_test.yaml) <br>
- [OpenClaw integration example](artifact/references/examples/openclaw_integration.yaml) <br>
- [Subagent workflow example](artifact/references/examples/subagent_test.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, YAML workflow configuration, shell commands, terminal progress logs, and JSON run records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Run records include run_id, flow_id, status, step results, timings, retry counts, and start and finish timestamps.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
