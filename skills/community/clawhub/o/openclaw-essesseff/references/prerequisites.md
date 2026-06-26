# Prerequisites Reference

This document expands on the prerequisites listed in `SKILL.md`.

## System Binaries

| Binary | Min Version | Purpose |
|---|---|---|
| `bash` | 4.0 | Script runtime |
| `curl` | any | API calls |
| `git` | any | Repo cloning and pushing; a git profile with commit/push access to the argocd-env repos is also required for `--setup-argocd` |
| `jq` | any | JSON parsing |
| `kubectl` | any | Argo CD setup only |

Install on macOS via Homebrew:
```bash
brew install bash curl git jq kubectl
```

Install on Ubuntu/Debian:
```bash
sudo apt-get update && sudo apt-get install -y curl git jq
# kubectl: https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/
```

## GitHub PATs

### GitHub Org Admin PAT (non-subscriber `--create-app` only)

Used to create the 9 repos and push content (including `.github/workflows`).

**Classic PAT** — scopes needed:
- `repo` — create repos, push code
- `workflow` — create/update `.github/workflows` files

**Fine-grained PAT** — permissions needed (org-level or all repos):
- Contents: Read and write
- Metadata: Read
- Workflows: Read and write
- Token user must have permission to create repositories in the org.

> **Do not confuse** this with the Argo CD machine user token (`GITHUB_TOKEN`).

### Argo CD Machine User PAT (`GITHUB_TOKEN`)

A separate GitHub account dedicated to Argo CD. It needs:
- `repo` scope — pull config repos
- `read:packages` scope — pull container images from GHCR

Setup guide: https://www.essesseff.com/docs/deployment/github-argocd-machine-user-setup

## Kubernetes + Argo CD

- Any K8s cluster works, including a single-VM `k3s` setup.
- Argo CD must be installed. The `setup-argocd-cluster.sh` script in this repo provides an easy way to do this.
- `kubectl` must be configured (`~/.kube/config` or `KUBECONFIG` env var) and pointing at the correct cluster for each environment **before** running `--setup-argocd`.
- The destination K8s namespace defaults to the `GITHUB_ORG` string. If your org name isn't DNS compliant or is 63+ characters, set `K8S_NAMESPACE` in `.essesseff` to a valid override.

## essesseff API Key (subscribers only)

Available from your essesseff team settings page. Must belong to the account in `ESSESSEFF_ACCOUNT_SLUG`.
