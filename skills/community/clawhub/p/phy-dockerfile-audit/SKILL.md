---
name: Dockerfile Audit
description: Dockerfile static security auditor. Scans any Dockerfile for 10 security issues — running as root, unpinned base images, secrets in ENV/ARG, remote ADD fetch, shell-form ENTRYPOINT, sudo installed, missing .dockerignore, privileged port EXPOSE, apt-get without --no-install-recommends, and hardcoded ARG defaults. Zero external dependencies (no hadolint, no Docker daemon, no network). Maps to CIS Docker Benchmark and CWE. CI fail-gate included.
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
tags:
  - security
  - docker
  - container
  - dockerfile
  - static-analysis
  - cis-benchmark
  - devops
---

# phy-dockerfile-audit — Dockerfile Security Auditor

Scans Dockerfiles for security misconfigurations without requiring Docker, hadolint, or any external tool. Zero external dependencies — pure Python stdlib.

## Quick Start

```bash
# Scan a single Dockerfile
python3 ~/.claude/skills/phy-dockerfile-audit/scripts/dockerfile_audit.py Dockerfile

# Scan entire project (finds all Dockerfiles recursively)
python3 ~/.claude/skills/phy-dockerfile-audit/scripts/dockerfile_audit.py .

# CI mode — exits 1 on any CRITICAL or HIGH finding
python3 ~/.claude/skills/phy-dockerfile-audit/scripts/dockerfile_audit.py . --ci

# GitHub Actions annotation format
python3 ~/.claude/skills/phy-dockerfile-audit/scripts/dockerfile_audit.py . --format github

# JSON output (for SARIF / dashboards)
python3 ~/.claude/skills/phy-dockerfile-audit/scripts/dockerfile_audit.py . --format json

# Run one specific check
python3 ~/.claude/skills/phy-dockerfile-audit/scripts/dockerfile_audit.py . --check DF003
```

## The 10 Checks

| ID | Severity | Issue | CWE | What it detects |
|----|----------|-------|-----|-----------------|
| DF001 | **CRITICAL** | Running as root | CWE-250 | No `USER` instruction, or `USER root` |
| DF002 | HIGH | Unpinned base image | CWE-1395 | `:latest` tag or no tag on `FROM` |
| DF003 | **CRITICAL** | Secret in ENV | CWE-312 | `ENV PASSWORD=...` — baked into image layer |
| DF004 | HIGH | ADD with remote URL | CWE-494 | `ADD https://...` — no integrity check |
| DF005 | MEDIUM | Shell form ENTRYPOINT/CMD | CWE-755 | Signal handling failure — PID 1 won't get SIGTERM |
| DF006 | HIGH | sudo installed | CWE-250 | `apt-get install sudo` — privilege escalation |
| DF007 | MEDIUM | Missing .dockerignore | CWE-552 | `.env`, `.git`, `node_modules` sent to build context |
| DF008 | MEDIUM | Privileged port exposed | CWE-284 | `EXPOSE < 1024` requires root or CAP_NET_BIND_SERVICE |
| DF009 | LOW | apt-get bloat | CWE-1395 | Missing `--no-install-recommends` |
| DF010 | **CRITICAL** | Secret ARG default | CWE-312 | `ARG PASSWORD=value` — in docker history |

## Pass / Fail Criteria

### DF001 — Running as root
- **FAIL (CRITICAL)**: No `USER` instruction in the Dockerfile, OR explicit `USER root` / `USER 0`.
- **PASS**: `USER nonroot`, `USER appuser`, `USER 1001`, or any non-root user. Docker 25+ supports `USER --uid 1001`.
- **Note**: Fires once per Dockerfile. If last `USER` before `CMD` is non-root, passes.

### DF002 — Unpinned base image
- **FAIL (HIGH)**: `FROM ubuntu:latest`, `FROM node` (no tag), `FROM python:latest`.
- **PASS**: `FROM ubuntu:22.04`, `FROM node:20-slim`, `FROM python@sha256:abc123...` (digest pin).
- **Note**: `FROM scratch` is exempt.

### DF003 — Secret in ENV
- **FAIL (CRITICAL)**: `ENV PASSWORD=actual_value`, `ENV API_KEY=sk-abc123`, `ENV DB_PASSWORD=prod_pass`.
- **PASS**: `ENV API_KEY=""`, `ENV API_KEY=placeholder`, `ENV API_KEY=${SECRET}` (uses build arg or runtime var).
- **Detection**: Key name must match: `password|passwd|secret|api_key|token|auth|credential|private_key|db_pass|jwt_secret|signing_key|encryption_key|smtp_pass`.

### DF004 — ADD with remote URL
- **FAIL (HIGH)**: `ADD https://get.example.com/install.sh /tmp/install.sh` — fetched at build time with no hash verification.
- **PASS**: `COPY local_file.sh /tmp/` or `RUN curl -fsSL https://... | sha256sum --check`.

### DF005 — Shell form ENTRYPOINT/CMD
- **FAIL (MEDIUM)**: `ENTRYPOINT service nginx start`, `CMD python app.py` (no brackets).
- **PASS**: `ENTRYPOINT ["nginx", "-g", "daemon off;"]`, `CMD ["python", "app.py"]` (exec form with JSON array).

### DF006 — sudo installed
- **FAIL (HIGH)**: `RUN apt-get install -y sudo`, `RUN apt install sudo vim`.
- **PASS**: sudo not installed anywhere. Specific commands needing elevation should use `gosu` or capability grants.

### DF007 — Missing .dockerignore
- **FAIL (MEDIUM)**: No `.dockerignore` file in the same directory as the Dockerfile.
- **PASS**: `.dockerignore` exists alongside the Dockerfile.
- **Recommended .dockerignore**:
  ```
  .git
  .env*
  node_modules
  *.log
  coverage/
  .DS_Store
  **/__pycache__
  ```

### DF008 — Privileged port
- **FAIL (MEDIUM)**: `EXPOSE 80`, `EXPOSE 443`, `EXPOSE 22` — ports below 1024.
- **PASS**: `EXPOSE 8080`, `EXPOSE 3000` — use `docker run -p 80:8080` to map at runtime.

### DF009 — apt-get without --no-install-recommends
- **FAIL (LOW)**: `RUN apt-get install -y curl` (no flag).
- **PASS**: `RUN apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*`.
- **Impact**: `--no-install-recommends` typically reduces image size by 20-40%.

### DF010 — Secret ARG with hardcoded default
- **FAIL (CRITICAL)**: `ARG DB_PASSWORD=mysecret` — the default appears in `docker history --no-trunc`.
- **PASS**: `ARG DB_PASSWORD` (no default) — pass at build time with `--build-arg DB_PASSWORD=$SECRET`.

## CI Integration

```yaml
# GitHub Actions
- name: Dockerfile Security Audit
  run: python3 scripts/dockerfile_audit.py . --format github --ci

# GitLab CI
dockerfile-audit:
  script:
    - python3 scripts/dockerfile_audit.py . --ci
  allow_failure: false
```

```bash
# Pre-commit hook
#!/bin/sh
python3 ~/.claude/skills/phy-dockerfile-audit/scripts/dockerfile_audit.py . --ci
```

## Example Output

```
======================================================================
  phy-dockerfile-audit — Dockerfile Security Report
======================================================================
  Total: 6  |  Critical: 3  |  High: 2
======================================================================

🔴 [DF001] CRITICAL — Running as root (no USER instruction) (CWE-250)
   File : ./Dockerfile
   Code : (no USER directive in file)
   Fix  : Add 'USER nonroot' or: RUN useradd -r -u 1001 appuser && USER appuser

🔴 [DF003] CRITICAL — Secret-like value in ENV instruction (CWE-312)
   File : ./Dockerfile:5
   Code : ENV API_KEY=sk-prod-abc123xyz
   Fix  : Pass secrets at runtime via --env-file or Docker secrets.

🔴 [DF010] CRITICAL — Secret-like ARG with hardcoded default (CWE-312)
   File : ./Dockerfile:2
   Code : ARG DB_PASSWORD=supersecret123
   Fix  : Remove the default: ARG DB_PASSWORD (pass via --build-arg at build time)

🟠 [DF002] HIGH — Base image unpinned (latest / no tag) (CWE-1395)
   File : ./Dockerfile:1
   Code : FROM ubuntu:latest
   Fix  : Pin to a specific version: ubuntu:22.04 or use a SHA digest.

🟠 [DF004] HIGH — ADD with remote URL (arbitrary fetch) (CWE-494)
   File : ./Dockerfile:6
   Code : ADD https://example.com/script.sh /setup.sh
   Fix  : Use RUN curl -fsSL <url> | sha256sum -c <hash> instead.

🟡 [DF005] MEDIUM — Shell form ENTRYPOINT / CMD (no signal pass) (CWE-755)
   File : ./Dockerfile:7
   Code : ENTRYPOINT service nginx start
   Fix  : Use exec form: ENTRYPOINT ["service", "nginx", "start"]
```

## Supported Dockerfile Variants

| Pattern | Detected as |
|---------|-------------|
| `Dockerfile` | ✅ |
| `Dockerfile.dev`, `Dockerfile.prod` | ✅ |
| `api.dockerfile`, `worker.Dockerfile` | ✅ |
| `docker-compose.yml` | ❌ (separate tool needed) |

## Technical Notes

- **Zero external dependencies** — pure Python 3.7+ stdlib
- **Line continuation handling** — `\` continuations joined before analysis
- **Comment stripping** — `#` comments ignored
- **Multi-stage builds** — scans all `FROM` stages for unpinned tags
- **Skips**: `.git/`, `node_modules/`, `dist/`, `build/`, `vendor/`
- **DF007** checks for `.dockerignore` relative to each Dockerfile found

## Differentiation vs Existing Docker Skills

| Skill | Focus |
|-------|-------|
| `phy-dockerfile-audit` | **Static security analysis** — finds vulnerabilities in Dockerfile source |
| `docker-essentials` | Operational guide — `docker run`, `docker ps`, commands |
| `doro-docker-essentials` | Operational guide — same as above |
| `xcloud-docker-deploy` | Deployment tool — compose templates, deployment workflows |

This is the **only static Dockerfile security scanner** on ClawHub. No hadolint required, no Docker daemon needed — works in any CI environment with Python 3.7+.

## Companion Skills

| Skill | Relationship |
|-------|-------------|
| `phy-k8s-security-audit` | Kubernetes manifest security (DF checks the image source, K8s checks the deployment) |
| `phy-iac-sec-audit` | Terraform/CloudFormation security |
| `phy-env-doctor` | Discovers env vars in source code |
| `phy-secret-scan` | Broader secret detection (if installed) |

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
