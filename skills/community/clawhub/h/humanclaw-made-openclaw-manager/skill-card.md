## Description: <br>
Install or operate a standalone local OpenClaw manager skill that adds shadow-first thread observation, durable session/run state, a loopback-only sidecar, attention management, snapshots, connector normalization, and capability reports for real work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZephyrChen0754](https://clawhub.ai/user/ZephyrChen0754) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users, developers, and teams use this skill to run a local workflow control plane for real work threads, durable session state, checkpoints, attention views, connector normalization, and local reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs an unauthenticated local sidecar that can read and change durable work data. <br>
Mitigation: Keep the sidecar bound to 127.0.0.1, avoid remote bind settings, and review the local state directory before deployment. <br>
Risk: The skill creates persistent local workflow state and may retain sensitive work context. <br>
Mitigation: Use it only when durable local retention is acceptable, and avoid routing sensitive threads through it unless local storage controls match the use case. <br>
Risk: Autostart can keep a local control plane available after initial setup. <br>
Mitigation: Enable autostart only after explicit consent and periodically review autostart settings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZephyrChen0754/humanclaw-made-openclaw-manager) <br>
- [Architecture](docs/architecture.md) <br>
- [Security Model](SECURITY.md) <br>
- [Session Model](docs/session-model.md) <br>
- [Event Schema](docs/event-schema.md) <br>
- [Connector Protocol](docs/connector-protocol.md) <br>
- [Capability Facts](docs/capability-facts.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, code, JSON files, HTML snapshots] <br>
**Output Format:** [Markdown or text responses with shell command snippets, configuration values, and local JSON, Markdown, or HTML artifacts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may describe or create durable local state under the configured OpenClaw Manager state root.] <br>

## Skill Version(s): <br>
0.3.2 (source: evidence.release.version, skill.yaml, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
