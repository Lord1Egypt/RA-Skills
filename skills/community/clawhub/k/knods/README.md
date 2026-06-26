# openclaw-skill-knods

`knods` is an OpenClaw skill for working with Creative NodeFlow / Knods in two modes:

- polling gateway mode for Iris-style canvas chat
- headless API mode for listing flows, inspecting inputs, running flows, polling runs, cancelling runs, and retrieving outputs

## Included Files

- [SKILL.md](./SKILL.md): operational instructions used by OpenClaw
- [scripts/knods_iris_bridge.py](./scripts/knods_iris_bridge.py): polling bridge runtime
- [scripts/knods_headless.py](./scripts/knods_headless.py): headless flow client
- [scripts/install_local.sh](./scripts/install_local.sh): local installer for the Iris bridge service
- [references/protocol.md](./references/protocol.md): polling gateway protocol notes
- [references/headless-api.md](./references/headless-api.md): headless execution API reference

## What It Can Do

### Polling Gateway

Use when Knods sends a chat envelope with fields like `messageId`, `message`, and `history`.

The skill can:

- parse Knods chat payloads
- emit `[KNODS_ACTION]...[/KNODS_ACTION]` blocks for canvas mutations
- build `addNode` and `addFlow` payloads
- stream responses back to the same Knods message

### Headless API

Use when you want to drive flows programmatically.

The skill can:

- list flows
- search flows by name/description
- inspect a flow's input schema
- start a run with `text`, `image`, `video`, or `audio` inputs
- poll or wait for completion
- cancel a running job
- retrieve final outputs

## Environment

Typical env vars in `~/.openclaw/.env`:

- `KNODS_BASE_URL`
- `KNODS_GATEWAY_TOKEN`
- `KNODS_API_BASE_URL`
- `KNODS_API_KEY`
- `OPENCLAW_AGENT_ID`

## Example Commands

```bash
python3 scripts/knods_headless.py list
python3 scripts/knods_headless.py resolve --query "product photo"
python3 scripts/knods_headless.py get --flow-id "<flow-id>"
python3 scripts/knods_headless.py run --flow-id "<flow-id>" --inputs-json '[{"nodeId":"n1","content":"hello","type":"text"}]'
python3 scripts/knods_headless.py wait --run-id "<run-id>"
```

## Install Bridge

```bash
bash scripts/install_local.sh
systemctl --user status knods-iris-bridge.service
```

## Release Notes

Recent changes include:

- headless API support
- flow inspection and execution commands
- run polling / waiting / cancellation
- packaged API reference for the headless flow execution API
