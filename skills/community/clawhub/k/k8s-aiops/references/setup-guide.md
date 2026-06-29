# k8s-aiops Setup Guide

## Install

```bash
uv tool install k8s-aiops
k8s-aiops doctor
```

`k8s-aiops` requires Python ≥ 3.11. If `uv` picked an older interpreter:

```bash
uv python install 3.12
uv tool install --python 3.12 --force k8s-aiops
```

## Connecting to a cluster

k8s-aiops reads your **kubeconfig** — the same one `kubectl` uses
(`KUBECONFIG` env var, else `~/.kube/config`). Out of the box it talks to your
current kube-context, so a fresh install needs no config file:

```bash
k8s-aiops pod list
```

### Named targets (multiple clusters)

The fastest way is the interactive wizard, which discovers the contexts in your
kubeconfig and registers the ones you pick (writing `config.yaml`, dir chmod 700):

```bash
k8s-aiops init
```

Or create `~/.k8s-aiops/config.yaml` by hand to give contexts friendly names:

```yaml
targets:
  - name: prod
    context: prod-eks            # a context from `kubectl config get-contexts`
    namespace: default           # optional default namespace
    # kubeconfig: /path/to/kubeconfig   # optional, overrides KUBECONFIG/~/.kube/config
  - name: lab
    context: k3s-lab
```

Then select with `-t`:

```bash
k8s-aiops -t prod pod list -n payments
```

No secrets are stored here — authentication lives entirely in the kubeconfig.

### Works with

Standard Kubernetes, k3s, EKS, GKE, AKS, kind, minikube. For managed clusters
(EKS/GKE/AKS) the kubeconfig uses an exec plugin (`aws`/`gcloud`/`az`); make sure
that CLI is installed and logged in.

## Security

> **Disclaimer**: This is a community-maintained open-source project and is **not affiliated with, endorsed by, or sponsored by the Cloud Native Computing Foundation, the Kubernetes project, or k3s/Rancher.** "Kubernetes" and "k3s" are trademarks of their respective owners. Source is auditable at [github.com/AIops-tools/K8s-AIops](https://github.com/AIops-tools/K8s-AIops) under the MIT license.

1. **Source code** — [github.com/AIops-tools/K8s-AIops](https://github.com/AIops-tools/K8s-AIops), MIT.
2. **Config file contents** — `config.yaml` holds only target names, kube context
   names, and optional namespaces/paths. No credentials.
3. **Credentials** — delegated to the kubeconfig; never read, logged, or echoed by
   k8s-aiops. Keep `~/.k8s-aiops` owner-only (`chmod 700`).
4. **TLS verification** — follows the kubeconfig (`certificate-authority` /
   `insecure-skip-tls-verify`); the skill does not weaken it.
5. **Prompt-injection protection** — all API-returned text (names, log lines, event
   messages) is run through `sanitize()` (truncation + control-character stripping).
6. **Least privilege** — bind the kube context to a ServiceAccount/user with only the
   RBAC verbs you need (read-only needs `get`/`list`/`watch`; writes add
   `patch`/`delete`).

## Governance harness

Bundled under `k8s_aiops.governance` — no external dependency. State lives under
`~/.k8s-aiops/` (override with `K8S_AIOPS_HOME`):

- `audit.db` — every tool call (skill, tool, params, status, duration, agent).
- `rules.yaml` — policy deny rules, maintenance windows, risk tiers.
- Token/runaway budget guard (`K8S_MAX_TOOL_CALLS`, `K8S_MAX_TOOL_SECONDS`,
  `K8S_RUNAWAY_MAX`, `K8S_RUNAWAY_WINDOW_SEC`).
- Undo store — inverse descriptors for reversible writes.
- Accountability: set `K8S_AUDIT_APPROVED_BY` / `K8S_AUDIT_RATIONALE` to record who
  authorized a high-tier operation and why.

## MCP client config

```jsonc
{
  "command": "k8s-aiops",
  "args": ["mcp"],
  "env": { "K8S_AIOPS_CONFIG": "~/.k8s-aiops/config.yaml" }
}
```

Fallback (no `uv tool install`): `uvx --from k8s-aiops k8s-aiops-mcp`. Prefer the
installed entry point — it does not re-resolve PyPI at launch.

## Static analysis

```bash
uvx bandit -r k8s_aiops/ mcp_server/
```
