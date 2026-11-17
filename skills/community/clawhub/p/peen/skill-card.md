## Description:

Configure and operate Peen, the durable coding-agent backend. Use when setting up a provider and Docker workspace, sending work over WebSocket, adding project harness rules, or inspecting and controlling durable sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to install and configure Peen, open project workspaces, and manage durable coding-agent sessions. It also guides them in connecting WebSocket clients, controlling retained work, and adding project harness rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup pipes a changing online installer directly into Bash, and the default controller setup uses the host Docker socket.

Mitigation: Review and verify the installer and host configuration before installing, and proceed only if you are comfortable with the Docker access it requires.

Risk: Workspace agents can read and change their project files, and session output can include sensitive data.

Mitigation: Open only projects you are willing to let the agent change; keep credentials out of accessible workspaces and transcripts.

Risk: Exposing Peen outside a trusted local network can expose its session API.

Mitigation: Set a real PEEN_API_TOKEN and use wss:// when exposing Peen beyond a trusted local network.

## Reference(s):

- [Peen on ClawHub](https://clawhub.ai/psyb0t/skills/peen)
- [Peen project site](https://github.com/psyb0t/peen)
- [Setup, providers, WebSocket, and REST](artifact/references/setup.md)
- [Deployment guide](https://github.com/psyb0t/peen/blob/main/docs/deployment.md)
- [Where Peen and its agents run](https://github.com/psyb0t/peen/blob/main/docs/where-it-runs.md)
- [HTTP API reference](https://github.com/psyb0t/peen/blob/main/docs/http-api.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, API calls]

**Output Format:** [Markdown with inline shell, JSON, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.49.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
