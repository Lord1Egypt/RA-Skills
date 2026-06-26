# Running Agents

## Procedure

1. **Get agent graph:** `GET /agent/{agent_id}` to find `agent_node_id` values.
2. **Start run:** `POST /agent/{agent_id}/run` with video input payload.
3. **Poll status:** `GET /agent_run/{run_id}` until `status` is `completed` or `failed`.
4. **Inspect nodes:** `GET /agent_run/{run_id}/nodes` for per-node status on failure.
5. **Credit-block handling:** if run/node has `needs_credits: true` (or `needsCredits: true`), follow the required flow in [credits-and-billing.md](credits-and-billing.md) before resuming.
6. **Resume:** `POST /agent_run/{run_id}/resume` to retry failed/blocked nodes.
7. **Cancel:** `POST /agent_run/{run_id}/cancel` to abort a running agent.

## Run payload templates

### Single-input (URL)

```json
{
  "video_urls": ["https://example.com/video.mp4"],
  "callback_url": "https://your-webhook.com/callback"
}
```

### Single-input (uploaded asset)

```json
{
  "video_ids": ["aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"]
}
```

`video_ids` come from the Uploads API — see [uploading-assets.md](uploading-assets.md).

### Single-input (chain from prior run)

```json
{
  "node_render_ids": ["7ba7b810-9dad-11d1-80b4-00c04fd430c8"]
}
```

`node_render_ids` come from prior run outputs (`GET /agent_run/{run_id}` → `outputs[].id`).

### Multi-input (canonical)

Use when the agent has multiple input nodes:

```json
{
  "video_inputs": [
    { "agent_node_id": "NODE_ID_1", "video_urls": ["https://..."] },
    { "agent_node_id": "NODE_ID_2", "node_render_ids": ["PRIOR_OUTPUT_ID"] }
  ],
  "callback_url": "https://your-webhook.com/callback"
}
```

## Overriding node parameters

Pass `update_params` to override node settings at run time:

```json
{
  "video_urls": ["https://..."],
  "update_params": {
    "AGENT_NODE_ID": {
      "param_key": "value"
    }
  }
}
```

Keys in `update_params` must be `agent_node_id` values from `GET /agent/{agent_id}`. Invalid keys return `400`.

## Credit-blocked runs (`needs_credits`)

If `GET /agent_run/{run_id}` or `GET /agent_run/{run_id}/nodes` indicates the run is credit-blocked:

1. Check current plan with `GET /plan`.
2. If user is free/no paid plan, list options via `GET /plan/list` and run `POST /plan/upgrade`.
3. Optionally enable auto top-ups via `POST /credits/settings`.
4. Resume with `POST /agent_run/{run_id}/resume`.

For the full required sequence and user-prompt behavior, use [credits-and-billing.md](credits-and-billing.md).

## Listing runs

- By agent: `GET /agent/{agent_id}/runs` — [Docs](https://docs.mosaic.so/api/agent-runs/get-agent-runs)
- All runs: `GET /agent_runs` — [Docs](https://docs.mosaic.so/api/agent-runs/get-all-agent-runs)
- By trigger: `GET /trigger/{trigger_id}/runs` — [Docs](https://docs.mosaic.so/api/agent-runs/get-trigger-runs)

## Docs

- [Run Agent](https://docs.mosaic.so/api/agent-runs/post-agent-run)
- [Get Run](https://docs.mosaic.so/api/agent-runs/get-agent-run)
- [Get Run Nodes](https://docs.mosaic.so/api/agent-runs/get-agent-run-nodes)
- [Resume Run](https://docs.mosaic.so/api/agent-runs/post-agent-run-resume)
- [Cancel Run](https://docs.mosaic.so/api/agent-runs/post-agent-run-cancel)
