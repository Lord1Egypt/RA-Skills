---
name: peen
description: Configure and operate Peen, the durable coding-agent backend. Use when setting up a provider and Docker workspace, sending work over WebSocket, adding project harness rules, or inspecting and controlling durable sessions.
homepage: https://github.com/psyb0t/peen
user-invocable: true
permissions:
  filesystem:
    read:
      - "README.md"
      - "docs/**"
      - ".env.example"
    write:
      - ".env"
      - "AGENTS.md"
      - ".agents/**"
  shell:
    - "peen *"
    - "docker run *"
    - "curl *"
metadata:
  openclaw:
    emoji: "🧰"
    requires:
      bins:
        - docker
---

# Peen

Peen is a durable coding-agent backend. It works in a real project directory, starts turns over WebSocket, and stores the conversation, tools, model rounds, compactions, child-agent work, and process jobs in SQLite.

## Security and safety

Treat a Peen workspace as direct shell and filesystem access for the model. Open only a project the operator is willing to let the agent change. The installer's default gives each workspace's agent its own container that sees that project and Peen's configuration directory read-only. The controller itself gets the host Docker socket in that setup, which is host root for Peen but not for the agent. Do not give an agent the Docker socket, an SSH directory, or a directory with credentials unless the operator asks for that. Tool output is stored in the transcript and sent to connected clients, so do not let the agent read or print secrets.

Keep provider credentials in `.env` or a deployment secret store. Set a real `PEEN_API_TOKEN` and use `wss://` before exposing Peen beyond a trusted local network.

## When to use

- Installing Peen and opening a project with the `peen` command.
- Adding project rules, skills, agents, events, or hooks to a workspace.
- Building a WebSocket client that starts turns and follows live events.
- Reading a stored session, cancelling a turn, or inspecting jobs, model calls, compactions, and child-agent runs.

## When NOT to use

- Editing Peen's own Go code. Use the repository's development docs and Make targets instead.
- Assuming a session is sandboxed. The agent space the operator gave it decides that. The `control` agent space runs tools with the controller's own access, and only a `docker:<profile>` agent space runs the agent in its own container. See [where it runs](https://github.com/psyb0t/peen/blob/main/docs/where-it-runs.md).

## Start Peen

Install the `peen` command, configure one provider, then open a project. Delete the provider entries you do not use, together with their key variables. `PEEN_UPSTREAMS` is raw JSON for Docker, so do not source `.env` in Bash.

```bash
curl -fsSL https://raw.githubusercontent.com/psyb0t/peen/main/install.sh | bash
peen config edit
cd ~/work/my-app
peen
```

By default Peen runs in a container and each workspace's agent runs in its own container. `--control-space host` and `--agent-space control` change that, and [where it runs](https://github.com/psyb0t/peen/blob/main/docs/where-it-runs.md) says what the agent can touch in each of the four combinations. The configuration lives in `~/.config/peen`. It holds `.env`, the `config/` directory with the trusted base harness, which every Docker worker reads read-only, and the `state/` directory with SQLite, logs, and worker sockets, which no Docker worker receives. The workspace root is the home directory unless the installer got `--workspace-root`. Peen refuses a workspace that contains its state or configuration directory, or sits inside the state directory. `peen` prints a link to the session it opened. `peen status`, `peen logs`, `peen doctor`, `peen stop`, and `peen upgrade` manage the controller. [Setup](references/setup.md) also points to the manual `docker run` route.

## Send and follow work

Peen starts with no sessions. Open a workspace with `POST /api/v1/sessions/open` and a body of `{"workspace":"<workspace_root>/my-app"}`, using the absolute host path. It returns the session, creating it the first time that directory is opened and resuming it afterwards. Never invent a session ID, because Peen refuses an unknown one and starts no turn.

Send the returned ID as `metadata.sessionId` in a `message.send` WebSocket event, and reuse it to continue the conversation. A normal connection gets live events for every session, so the client builds tabs by filtering event metadata. `?sessionId=<uuid>` only filters what one socket receives; it does not keep a session's work running, and closing every connection for a session does not pause it either. Only `POST /api/v1/session/cancel`, cancelling a child, stopping the controller, or an embedded `Close` pauses or stops work, along with a failed turn or a crash. A client that reconnects replays whatever it missed from [`GET /api/v1/session/feed`](https://github.com/psyb0t/peen/blob/main/docs/http-api.md#get-apiv1sessionfeed) instead of losing it. Every sent message still needs `metadata.sessionId`.

`GET /api/v1/sessions` lists what exists and needs no session header.

Use REST to read stored state and control work. A message for the agent goes over the WebSocket. Send `X-Session-ID` to the session endpoints. For example, list messages with `GET /api/v1/messages` and ask a turn to stop with `POST /api/v1/session/cancel`. The [API reference](https://github.com/psyb0t/peen/blob/main/docs/http-api.md) has every frame and endpoint.

## Inspect and continue retained work

Stop pauses unfinished workflows and interrupts current activities. Reconnect does not resume them. Ask the agent to use `searchExecutions` and `readExecution` to find retained tasks, ancestry, context and activity history without starting work. After inspecting the workspace, it can use `resolveExecutionActivity` for uncertain tool outcomes and `resumeExecution` for explicit continuation. Completed results are reused after a crash. See [recovery and continuation](https://github.com/psyb0t/peen/blob/main/docs/agents.md#recovery-after-a-crash).

## Teach it the project

Put always-on project instructions in `AGENTS.md` and topic rules in `.agents/rules/<name>.md`. A rule whose frontmatter has `paths:` globs, the Claude Code format, loads only when the agent reads or changes a matching file; `examples/rules/` in the repository has a starter pack. Add named procedures under `.agents/skills/<name>/SKILL.md`, child-agent definitions for bounded jobs under `.agents/agents/`, outside-event handlers under `.agents/events/`, and mechanical guards in `.agents/hooks.yaml`.

Peen reads the configuration directory first, then every directory from `/` down to the agent's current directory, at the start of every turn and on each `changeDirectory` call. A layer closer to that directory is more specific. Descendant definitions load when the agent enters their directory. Root hops persist across turns; children change independently. The model sees each skill's name and description, and loads the full skill only when it decides to use it. Hooks work differently. They run mechanically and can add context, deny an action, run a command, or post a session notice.

## References

- [Setup, providers, WebSocket, and REST](references/setup.md)
- [Configuration](https://github.com/psyb0t/peen/blob/main/docs/configuration.md)
- [Deployment](https://github.com/psyb0t/peen/blob/main/docs/deployment.md)
- [Where it runs](https://github.com/psyb0t/peen/blob/main/docs/where-it-runs.md)
- [The harness](https://github.com/psyb0t/peen/blob/main/docs/harness.md)
- [AGENTS.md and rules](https://github.com/psyb0t/peen/blob/main/docs/rules.md)
- [Skills](https://github.com/psyb0t/peen/blob/main/docs/skills.md)
- [Named agents](https://github.com/psyb0t/peen/blob/main/docs/agents.md)
- [Session events](https://github.com/psyb0t/peen/blob/main/docs/events.md)
- [Hooks](https://github.com/psyb0t/peen/blob/main/docs/hooks.md)
- [API reference](https://github.com/psyb0t/peen/blob/main/docs/http-api.md)
