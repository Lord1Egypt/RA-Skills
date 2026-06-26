## Description: <br>
GPU monitoring with risk intelligence. Local + cloud fleet monitoring, health tracking, proactive alerts, and AI-powered fleet analytics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horne-ra](https://clawhub.ai/user/horne-ra) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
Developers, operators, and hardware users use this skill to install, configure, and query Keldron Agent for GPU telemetry, risk scores, cost estimates, dashboards, fleet health, history, and alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download and run an external monitoring agent or Docker container. <br>
Mitigation: Confirm before downloads or Docker runs, install only when a real monitoring agent is intended, and prefer reviewed release artifacts. <br>
Risk: Local monitoring endpoints and Docker examples can expose ports for metrics, health checks, and dashboards. <br>
Mitigation: Keep services bound to localhost by default; bind to other interfaces or open firewall access only when network exposure is intentional. <br>
Risk: Cloud setup can persist Keldron API keys in environment variables, credentials files, or YAML. <br>
Mitigation: Prefer interactive login, use a revocable key, avoid echoing full keys, and store credentials with restricted permissions. <br>
Risk: Watch and alert workflows can create long-running polling loops, and management commands can stop or restart local agent processes. <br>
Mitigation: Confirm the intended duration and scope before watch loops, set a maximum check count when practical, and confirm before process kill or restart commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/horne-ra/keldron-agent) <br>
- [Publisher profile](https://clawhub.ai/user/horne-ra) <br>
- [Keldron Agent homepage](https://github.com/keldron-ai/keldron-agent) <br>
- [Keldron Agent releases](https://github.com/keldron-ai/keldron-agent/releases) <br>
- [Docker Linux post-install](https://docs.docker.com/engine/install/linux-postinstall/) <br>
- [Keldron Cloud](https://app.keldron.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets, API calls, configuration examples, and concise status summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose downloads, Docker runs, process management, local HTTP endpoints, cloud API calls, and long-running watch loops when the user asks for setup or monitoring.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter says 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
