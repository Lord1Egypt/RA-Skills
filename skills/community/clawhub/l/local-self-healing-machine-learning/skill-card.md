## Description: <br>
A fully local machine learning engine that makes an OpenClaw agent smarter over time by learning from runtime failures, clustering similar errors, and evolving fix strategies without default outbound telemetry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[josephtandle](https://clawhub.ai/user/josephtandle) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to run a local self-healing loop that analyzes OpenClaw runtime history, proposes or applies code fixes, validates outcomes, and records lessons in local memory. It is aimed at local automation workflows where auditability and offline operation are important. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read recent OpenClaw sessions, persist learning state, and spawn or drive executor agents that change code. <br>
Mitigation: Run it only in a controlled workspace, review proposed changes before accepting them, and keep human review mode enabled for sensitive projects. <br>
Risk: Optional bridge, hub task, auto-update, remote Ollama, and publishing paths can introduce network or executor behavior beyond the default local posture. <br>
Mitigation: Keep EVOLVE_BRIDGE, EVOLVE_HUB_TASKS, auto-update, remote OLLAMA_URL values, and asset publishing disabled unless explicitly required. <br>
Risk: The local dashboard can expose diagnostics and local state if reachable from shared or networked machines. <br>
Mitigation: Bind or firewall the dashboard and avoid exposing the configured dashboard port outside the local machine. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/josephtandle/local-self-healing-machine-learning) <br>
- [Publisher profile](https://clawhub.ai/user/josephtandle) <br>
- [Author site from clawdis metadata](https://mastermindshq.business) <br>
- [Ollama installation documentation](https://ollama.com/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions, console text, local JSON/JSONL state files, and generated code changes when execution is enabled] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local audit artifacts, feedback records, embeddings cache, knowledge base entries, and optional dashboard data.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release evidence; artifact package.json reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
