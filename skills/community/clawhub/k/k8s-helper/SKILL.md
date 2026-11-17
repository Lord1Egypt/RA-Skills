---
name: k8s
description: Operate Kubernetes clusters via kubectl with a user-supplied kubeconfig (local file path or remote URL). This skill should be used when users want to inspect or manage Kubernetes resources (pods, deployments, services, nodes, namespaces, logs, exec, apply, etc.) against an arbitrary cluster. The skill auto-downloads remote kubeconfigs to a cached location and auto-installs `kubectl` if it is missing.
---

# Kubernetes (k8s) Skill

Run `kubectl` against any cluster by pointing at a local kubeconfig file or a remote kubeconfig URL. Bootstrap (kubectl install + kubeconfig download) is handled automatically.

## When to Use

Use this skill whenever the user wants to:

- Inspect Kubernetes resources (e.g. `kubectl get pods -A`, `kubectl describe node ...`)
- Apply / delete / edit manifests (`kubectl apply -f`, `kubectl delete`, `kubectl rollout`)
- Stream logs, exec into pods, port-forward, or run any other `kubectl` subcommand
- Run against a one-off cluster whose kubeconfig is published at an HTTP(S) URL

## Usage

The main entry point is `scripts/k8s.sh`. It is a thin wrapper that:

1. Ensures `kubectl` is installed (downloads it via the DaoCloud mirror if missing).
2. Resolves the kubeconfig (downloads it to a cached path if a URL is given).
3. Invokes `kubectl --kubeconfig=<resolved-path> <your args...>`.

### Local kubeconfig

```bash
bash scripts/k8s.sh \
  --kubeconfig /path/to/kubeconfig.yaml \
  -- get pods -A
```

### Remote kubeconfig URL

```bash
bash scripts/k8s.sh \
  --kubeconfig-url https://example.com/kubeconfig.yaml \
  -- get nodes -o wide
```

### Via environment variables

`--kubeconfig` and `--kubeconfig-url` can also be supplied via env vars:

```bash
export KUBECONFIG_URL=https://example.com/kubeconfig.yaml
bash scripts/k8s.sh -- get ns
```

Or:

```bash
export KUBECONFIG_PATH=/path/to/kubeconfig.yaml
bash scripts/k8s.sh -- get ns
```

If both a URL and a local path are provided, the explicit CLI flag wins; otherwise local path takes precedence over URL.

### The `--` separator

Anything after `--` is forwarded verbatim to `kubectl`. The separator is recommended (especially when forwarded args start with `-`), but the script also tolerates omitting it when no flag ambiguity exists.

## Flags

| Flag | Env Var | Description |
|------|---------|-------------|
| `--kubeconfig <path>` | `KUBECONFIG_PATH` | Local kubeconfig file path. |
| `--kubeconfig-url <url>` | `KUBECONFIG_URL` | Remote kubeconfig URL (http/https). Downloaded once and cached. |
| `--cache-dir <dir>` | `K8S_SKILL_CACHE_DIR` | Cache directory for downloaded kubeconfigs and kubectl binary. Defaults to `$HOME/.cache/k8s-skill`. |
| `--refresh` | - | Force re-download of the remote kubeconfig even if cached. |
| `--kubectl <path>` | `KUBECTL_BIN` | Use a specific kubectl binary instead of auto-detect/install. |
| `--insecure` | - | Pass `-k` to `curl` when downloading the kubeconfig (use only for trusted self-signed endpoints). |
| `-h`, `--help` | - | Print usage. |

All other arguments (or anything after `--`) are passed straight through to `kubectl`.

## Examples

```bash
# List namespaces using a local kubeconfig
bash scripts/k8s.sh --kubeconfig ~/.kube/prod.yaml -- get ns

# Tail logs against a remote kubeconfig
bash scripts/k8s.sh \
  --kubeconfig-url https://example.com/kubeconfig.yaml \
  -- logs -n kube-system -l k8s-app=kube-dns --tail=100 -f

# Apply a manifest
bash scripts/k8s.sh \
  --kubeconfig-url https://example.com/kubeconfig.yaml \
  -- apply -f ./deploy.yaml

# Force a kubeconfig refresh (re-download)
bash scripts/k8s.sh \
  --kubeconfig-url https://example.com/kubeconfig.yaml --refresh \
  -- cluster-info
```

## Behavior Notes

- **kubectl auto-install:** When `kubectl` is missing and no `--kubectl`/`KUBECTL_BIN` override is given, the wrapper downloads a stable `kubectl` binary for the current OS/arch from the DaoCloud mirror (`https://files.m.daocloud.io/dl.k8s.io/...`) and caches it under `<cache-dir>/bin/kubectl`. The cache directory is added to `PATH` for the duration of the command.
- **Kubeconfig caching:** Remote kubeconfigs are hashed by URL (sha256) and stored at `<cache-dir>/kubeconfigs/<hash>.yaml`. Use `--refresh` to bypass the cache.
- **Secrets:** Downloaded kubeconfigs are written with `chmod 600`. Avoid logging the file contents.
- **Cross-platform:** The wrapper auto-detects Linux/macOS and amd64/arm64 for kubectl downloads.
- **Errors:** If both kubeconfig sources are missing the script exits with a clear error. Curl/network errors are surfaced verbatim.

## Quick Sanity Check

A no-op connectivity probe:

```bash
bash scripts/k8s.sh \
  --kubeconfig-url https://example.com/kubeconfig.yaml \
  -- version --short
```
