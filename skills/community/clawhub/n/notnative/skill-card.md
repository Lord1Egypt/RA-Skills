## Description:

Use Notnative MCP server for complete AI assistant integration with notes, calendar, tasks, Python, canvas, and permanent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[k4ditano](https://clawhub.ai/user/k4ditano)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to connect an assistant to a Notnative instance for notes, persistent memory, tasks, calendar data, canvas state, web tools, and Python execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages broad persistent storage of personal facts, preferences, notes, profile data, tasks, and calendar data.

Mitigation: Confirm user consent and retention expectations before storing personal information, periodically review stored memory, and delete stale or sensitive memories when they are no longer needed.

Risk: Remote or unauthenticated WebSocket endpoints may expose personal data and tool authority beyond the local machine.

Mitigation: Prefer a local endpoint or an authenticated wss:// endpoint, and avoid remote ws:// URLs for sensitive use.

Risk: The install script can add a shell environment entry and create a command symlink, which may persist after the skill is no longer used.

Mitigation: During uninstall or review, remove the NOTNATIVE_WS_URL entry from .bashrc and the notnative symlink from $HOME/.local/bin if they are no longer desired.

Risk: The Notnative integration exposes Python execution through the connected server.

Mitigation: Review code before execution and restrict server access to trusted users and trusted workloads.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/k4ditano/skills/notnative)
- [Project homepage](https://github.com/k4ditano/notnative-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON command results from the Notnative tool client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node, curl, and a configured local or remote Notnative WebSocket endpoint.]

## Skill Version(s):

1.0.1 (source: server release evidence; package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
