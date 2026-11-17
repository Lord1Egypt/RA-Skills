# Set up and use Peen

## Install with the peen command

```bash
curl -fsSL https://raw.githubusercontent.com/psyb0t/peen/main/install.sh | bash
peen config edit
cd ~/work/my-app
peen
```

The installer pins the newest release and writes `~/.config/peen`. Its defaults run Peen in a container with the host Docker socket and give each workspace's agent its own container. Pass flags after `bash -s --`, such as `--control-space host`, `--agent-space control`, or `--workspace-root DIR`. `peen` starts the controller when needed, opens the session for the current directory, and prints its link. [Deployment](https://github.com/psyb0t/peen/blob/main/docs/deployment.md#install) lists every flag and command, and [where it runs](https://github.com/psyb0t/peen/blob/main/docs/where-it-runs.md) explains the combinations.

## Configure a provider

`peen config edit` opens `~/.config/peen/.env`. Keep only the upstreams you intend to use, delete the key variables of the others, set `PEEN_DEFAULT_MODEL` and `PEEN_COMPACTION_MODEL` to models of a provider you kept, and set the matching credential variable. A compaction model that still names a deleted provider stops startup. Provider credentials belong in the named environment variable, never inside `PEEN_UPSTREAMS`.

```dotenv
PEEN_UPSTREAMS=[{"name":"aigate","type":"openai","baseUrl":"https://aigate.example/v1","apiKeyEnv":"AIGATE_TOKEN"}]
PEEN_DEFAULT_MODEL=aigate/your-model-id
PEEN_COMPACTION_MODEL=aigate/your-model-id
AIGATE_TOKEN=your-token-here
PEEN_API_TOKEN=
```

`openai`, `anthropic`, and `zai-coding` are the supported upstream types. Peen checks that the configured model is available when it starts. Set `PEEN_API_TOKEN` before running Peen anywhere other than a local machine where no one else can reach it. `peen doctor` checks the configuration.

## Run the image by hand

The manual route is the [Docker section of deployment](https://github.com/psyb0t/peen/blob/main/docs/deployment.md#docker). It creates the configuration, state, and workspace root directories, lets the image write `.env` with `config init`, and runs the controller with each directory mounted at its literal host path. Pin a release tag such as `psyb0t/peen:v0.20.0` rather than `latest`, publish the API on `127.0.0.1` only unless `PEEN_API_TOKEN` is set, and do not publish the metrics listener. Without the Docker socket the controller runs the `control` agent space, so the agent can read and change the state directory with every session's transcript. With the socket mounted, Peen refuses `control` and runs each workspace in its own container.

## Send a turn

A message for the agent goes over the WebSocket only. REST reads stored state and controls work, and the one REST call that can start a turn is a posted notice that an event handler lets wake an idle session.

```js
const opened = await (await fetch("http://127.0.0.1:8080/api/v1/sessions/open", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ workspace: "/abs/path/to/project" }),
})).json();
const sessionId = opened.session.id;
const socket = new WebSocket(
  `ws://127.0.0.1:8080/ws/v1?sessionId=${encodeURIComponent(sessionId)}`,
  "peen.v1",
);

socket.addEventListener("message", ({ data }) => console.log(JSON.parse(data)));
socket.addEventListener("open", () => {
  socket.send(JSON.stringify({
    id: crypto.randomUUID(),
    type: "message.send",
    data: { message: "Read the project, then explain the first safe change." },
    timestamp: Math.floor(Date.now() / 1000),
    metadata: { sessionId },
    triggeredBy: null,
  }));
});
```

Keep `sessionId`. Never invent one, because Peen refuses an unknown session ID and starts no turn. Sending another `message.send` with that ID starts or queues new work in the session. It does not resume an earlier paused task. Session work keeps running with no client connected; closing every socket for a session does not pause it. Only `POST /api/v1/session/cancel`, cancelling a child, stopping the controller, an embedded `Close`, a failed turn, or a crash stop it. Each accepted event carries `metadata.sessionId`, so clients sharing a global socket can render only the session tab they need, and a client that reconnects catches up from [`GET /api/v1/session/feed`](https://github.com/psyb0t/peen/blob/main/docs/http-api.md#get-apiv1sessionfeed) instead of missing frames. A `message.completed` event means that submitted message is done. It does not close the socket.

With `PEEN_API_TOKEN` set, browser clients authenticate through the `peen.v1` and `peen.bearer.<base64url-token>` WebSocket subprotocols. Other clients can send the usual `Authorization: Bearer <token>` header with the upgrade request. Never put a token in the URL.

## Inspect and control stored work

REST reads the state stored in SQLite. Send `X-Session-ID` to the session endpoints, and `Authorization: Bearer <token>` when `PEEN_API_TOKEN` is set.

```bash
curl "http://127.0.0.1:8080/api/v1/messages?limit=50&order=asc" \
  -H "X-Session-ID: <session-id>"

curl -X POST "http://127.0.0.1:8080/api/v1/session/cancel" \
  -H "X-Session-ID: <session-id>"
```

With the installer, `peen session list` and `peen session attach <session-id>` do the same from the command line. `peen session attach` reconnects automatically after an unexpected drop and catches up from the session feed; add `--cursor <n>` to replay from sequence `n` first. `peen --prompt "<task>"` runs one turn in the current directory's session and exits when the turn ends, writing every frame to stdout as JSONL, or the reply text with `--output text`. Its exit status is 0 when the turn completed, 1 when it failed, and 130 when it was cancelled. The [command line guide](https://github.com/psyb0t/peen/blob/main/docs/command-line.md) lists its flags. The API also lists protocol events, context and prompt snapshots, compaction lineage, model runs and calls, process jobs and output, child-agent runs, and outside notices. Use `wss://` and HTTPS when Peen is not local. The [API reference](https://github.com/psyb0t/peen/blob/main/docs/http-api.md) has every request and frame.

Stop interrupts current activities and retains unfinished workflows as paused. The agent can inspect history with `searchExecutions` and `readExecution`, resolve inspected uncertain effects with `resolveExecutionActivity`, and explicitly continue with `resumeExecution`. See [retained work](https://github.com/psyb0t/peen/blob/main/docs/agents.md#inspecting-retained-work).

## Add a harness layer

```text
workspace/
  AGENTS.md
  .claude/
    rules/<rule-name>.md
    skills/<skill-name>/SKILL.md
  .agents/
    rules/<rule-name>.md
    skills/<skill-name>/SKILL.md
    agents/<agent-name>.md
    events/<event-type>.md
    hooks.yaml
```

`AGENTS.md` gives the model standing project instructions. Rules are topic files that join them on every turn, or, with `paths:` frontmatter, reach the model when it reads or changes a matching file. Skills are procedures the model loads when a task needs them. Named agents handle bounded jobs the main agent hands off. Event handlers tell Peen how to handle an outside notice. Hooks enforce mechanical behavior around turn and tool events. Hooks from every layer run, so only open workspaces whose hooks you trust.
