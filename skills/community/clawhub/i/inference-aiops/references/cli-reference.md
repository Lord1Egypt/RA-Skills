# inference-aiops CLI reference

> Serving engines: vLLM (OpenAI API + Prometheus `/metrics`,
> default 8000) with its Ray dashboard control plane (Serve + Jobs, default 8265),
> plus single-process SGLang (default 30000) and TGI (default 8080); endpoints
> need live verification.
>
> The CLI is a convenience subset. The full 35-tool surface — including the
> engine-agnostic reads (`engine_health`, `engine_inventory`,
> `engine_request_metrics`, `engine_queue_depth`, `diagnose_engine_latency`) that
> cover SGLang/TGI — is via the MCP server (`inference-aiops mcp`).

## Setup & diagnostics

```bash
inference-aiops init                      # interactive wizard: engine (vllm/sglang/tgi) + host + port
inference-aiops doctor [--skip-auth]      # config + secret store + connectivity — vLLM: Ray + vLLM; SGLang/TGI: engine health + inventory
inference-aiops mcp                       # start the MCP server (stdio transport)
```

## Secrets (encrypted store ~/.inference-aiops/secrets.enc — only if a token is used)

```bash
inference-aiops secret set <target> [--value <token>]  # store a bearer token (hidden prompt if no --value)
inference-aiops secret list                            # names only — values never shown
inference-aiops secret rm <target>
inference-aiops secret migrate                         # import legacy plaintext env (INFERENCE_<T>_TOKEN)
inference-aiops secret rotate-password                 # re-encrypt under a new master password
```

## Read commands

```bash
inference-aiops overview [--target <t>]        # Serve deployments + total replicas + queue backpressure
inference-aiops serve list                     # Ray Serve deployments + replica counts
inference-aiops serve status <application> <deployment>   # one deployment's status + replica count
inference-aiops metrics requests               # TTFT / TPOT / e2e latency + token totals (from vLLM /metrics)
inference-aiops metrics queue                  # running vs waiting requests (backpressure)
inference-aiops metrics diagnose               # flagship RCA: ranked cause of a latency spike + the knob to turn
```

## Write commands (governed; risk tier in parentheses)

```bash
inference-aiops serve scale <application> <deployment> <num_replicas>   # (med) reversible
inference-aiops serve scale-to-zero <application> <deployment> [--dry-run]   # (high) --dry-run + double confirm; strands ingress
```

> The remaining writes — `scale_replicas_down`, `drain_replica`,
> `autoscale_config_update`, `lora_load` / `lora_unload`, `model_sleep` /
> `model_wake` (dev-mode servers only),
> `ray_job_cancel`, `replica_restart`, `model_deploy` / `model_undeploy`,
> `deployment_redeploy`, `routing_policy_update` — are exposed via the MCP
> server. High-risk ones support a dry-run preview.

## Common options

- `--target, -t <name>` — target name from `config.yaml` (omit to use the default/first target)
- `--dry-run` — print the API call that would be made, change nothing
- State-changing commands (e.g. `serve scale-to-zero`) require two confirmations
