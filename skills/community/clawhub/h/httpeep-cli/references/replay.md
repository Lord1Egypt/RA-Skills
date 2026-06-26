<!-- GENERATED FILE: DO NOT EDIT DIRECTLY. -->
<!-- Source of truth: docs.httpeep.com/content/docs/cli/replay.mdx -->
<!-- Generate with: node scripts/generate-httpeep-cli-skill-reference.mjs <references-dir> -->

# Replay

The `replay` subcommand re-sends a previously captured request. You can replay a specific session by ID, replay from a recorded script file, or replay the last captured request. The replayed request appears as a new session in the session list.

## replay --id

Replay a specific session by its ID. This is the most common replay mode.

```bash
httpeep-cli replay --id <session_id>
```

### Retry strategy

Add automatic retry for flaky endpoints:

```bash
httpeep-cli replay --id <session_id> \
  --retry-times 3 \
  --retry-interval-ms 800
```

| Flag | Description | Default |
|---|---|---|
| `--retry-times <n>` | Maximum total attempts | — |
| `--retry-interval-ms <ms>` | Interval between retries in milliseconds | — |

### Temporary rules during replay

Overlay temporary rules on the replay without modifying the global ruleset:

```bash
httpeep-cli replay --id <session_id> \
  --rule-file ./rule.yaml

httpeep-cli replay --id <session_id> \
  --map-remote "api.example.com=http://127.0.0.1:3000"
```

All shortcut rule parameters are supported. See the [Rules](/cli/rules) page for details.

## replay file

Replay requests from a previously recorded script file.

```bash
httpeep-cli replay file ./recording.httpeep
```

Each request in the file is re-sent through the proxy in the original order.

## replay last

Replay the most recently captured request.

```bash
httpeep-cli replay last
```

> **Note:**
> Temporary rule parameters are only valid with `--id` mode. `replay file` and `replay last` do not accept `--rule`, `--map-remote`, or other temporary rule flags.
