# inference-aiops setup & security guide

> Not yet validated against a live cluster — see `docs/VERIFICATION.md`.

## 1. Install

```bash
uv tool install inference-aiops
```

## 2. (Optional) create a bearer token

A bearer token is **optional** — many vLLM / Ray stacks run open. Only create
one if your API requires it (e.g. vLLM started with `--api-key`, or an
authenticating proxy in front of the Ray dashboard). inference-aiops sends it as
`Authorization: Bearer <token>` to both the Ray dashboard and vLLM.

## 3. Onboard

```bash
inference-aiops init
```

The wizard collects (non-secret) connection details into
`~/.inference-aiops/config.yaml`: the **serving engine** (`vllm` / `sglang` /
`tgi`), a **host**, the engine's **port**, and the **scheme** (http/https). For
the vLLM engine it also collects the **Ray dashboard port** (default 8265) — its
control plane. A bearer token is stored **encrypted** into
`~/.inference-aiops/secrets.enc` **only if the API requires one**. Example config:

```yaml
targets:
  - name: prod                 # vLLM + Ray Serve control plane
    host: 10.0.0.20
    engine: vllm
    scheme: http
    ray_port: 8265
    vllm_port: 8000            # vLLM engine port (legacy key; == engine_port)
    verify_ssl: false          # self-signed lab certs only
  - name: sg                    # SGLang (single-process, no Ray)
    host: 10.0.0.21
    engine: sglang
    engine_port: 30000         # SGLang default
  - name: edge                  # TGI (single-process, no Ray)
    host: 10.0.0.22
    engine: tgi
    engine_port: 8080          # TGI default
```

Default engine ports: **vLLM 8000, SGLang 30000, TGI 8080**. `engine_port` (or the
legacy `vllm_port`) sets the engine's HTTP port. Only the **vLLM** engine uses
`ray_port`; SGLang and TGI are single-process servers with no Ray dashboard, so
their scale/drain writes raise a teaching error rather than issuing an impossible
control-plane call.

## 4. Non-interactive use (MCP server / CI / cron)

If a token is stored, export the master password so the encrypted store unlocks
without a prompt (no token stored → nothing to export):

```bash
export INFERENCE_AIOPS_MASTER_PASSWORD='your-master-password'
```

## 5. Laptop self-test (~80% of the tool, free)

Most of the tool self-tests on a laptop with no cloud GPUs:

- **vLLM** — run on a single GPU, or use a CPU-mock, exposing the OpenAI API and
  Prometheus `/metrics` (default port 8000).
- **Ray** — one local head node: `ray start --head` (Ray dashboard on 8265),
  serving a small Serve app.

Point a target at `host: 127.0.0.1` with `ray_port: 8265` / `vllm_port: 8000`
and run `inference-aiops doctor`. Reads, RCA, and most scaling ops exercise
end-to-end. Still unverified: multi-GPU tensor/pipeline-parallel deployments,
real GPU thermal/throttle telemetry, and multi-node drain (see
`docs/VERIFICATION.md`).

## Credential security (when a token is used)

- The token is **never** written to disk in plaintext. It lives only in
  `~/.inference-aiops/secrets.enc`, encrypted with Fernet (AES-128-CBC + HMAC),
  the key derived from your master password via scrypt. Only a per-store random
  salt and the ciphertext are on disk (chmod 600); the master password is never
  stored.
- A legacy plaintext env var `INFERENCE_<TARGET_NAME_UPPER>_TOKEN` is still
  honoured as a fallback with a deprecation warning — migrate with
  `inference-aiops secret migrate`.
- The token is held only in memory during a session and is never logged or
  echoed; exception text and tracebacks are scrubbed of secret-shaped strings
  before being written to the audit log.

## Optional audit annotations

The tool does not require an approver — whether a high-risk write (scale-down,
scale-to-zero, drain, LoRA unload, hot-swap, replica restart, undeploy, redeploy)
should happen is the agent's decision or the connecting environment's permission.
If you want the audit row to carry who ran a change and why, set these; they are
recorded when present and never required:

```bash
export INFERENCE_AUDIT_APPROVED_BY='you'
export INFERENCE_AUDIT_RATIONALE='off-peak cost save'
```

## Governance harness state

State lives under `~/.inference-aiops/` (relocate with `INFERENCE_AIOPS_HOME`):

- `audit.db` — every tool call (SQLite), with the risk tier (a descriptive
  label, not a gate) and any approver/rationale annotation
- `undo.db` — inverse descriptors for reversible writes (scale, autoscale-config,
  routing, hot-swap, LoRA load)
- budget / runaway guard — a safety backstop (not authorization): caps cumulative
  tool calls and wall-time; trips on tight poll/retry loops

## Verify

```bash
inference-aiops doctor
```

`doctor` checks the config file, the encrypted store and its permissions (if a
token is configured), and — unless `--skip-auth` — connectivity. For a **vLLM**
target it probes the **Ray dashboard** and **vLLM** independently, so a half-up
cluster is reported precisely; for a **SGLang / TGI** target it probes the
engine's health endpoint and running-model inventory (no Ray).
