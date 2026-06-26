---
name: portable-deployment-audit
description: Read-only security auditing for OpenClaw deployments, repositories, and local project directories. Scan an explicit target directory for exposed credentials, risky configuration, explicit port exposure hints, Dockerfile and compose issues, Git exposure, and Unix permission problems. Uses file inspection only. Use when reviewing a deployment, server checkout, workspace, or repo before release, after setup, during periodic hardening checks, or in CI.
---

# Portable Deployment Audit

Run a read-only security review against a chosen directory.

## Rules

- Treat this skill as read-only.
- Do not use it to modify files automatically.
- Pass `--target <dir>` when auditing something other than the current directory.
- Use `--format json` for machine-readable output; stdout will contain pure JSON only.
- Use `--strict` when you want a non-zero exit on HIGH findings in CI.
- Use `--exclude-dir` to skip bulky or irrelevant directories in mixed repos.
- Use `--allow-port` to suppress expected configured/published ports in local or staged environments.
- This version uses file inspection only and does not invoke external binaries such as `git`, `ss`, or `netstat`.
- Expect limited permission analysis on Windows; Unix mode-bit checks only run on Unix-like systems.

## Commands

### Quick audit of current directory

```bash
node skills/portable-deployment-audit/scripts/audit.cjs --target .
```

### Audit another directory

```bash
node skills/portable-deployment-audit/scripts/audit.cjs --target /path/to/project
```

### JSON report

```bash
node skills/portable-deployment-audit/scripts/audit.cjs --target . --format json > audit-report.json
```

### CI-style run

```bash
node skills/portable-deployment-audit/scripts/audit.cjs --target . --format json --strict
```

### Ignore expected noise

```bash
node skills/portable-deployment-audit/scripts/audit.cjs --target . --exclude-dir vendor,tmp --allow-port 3000,8080
```

### Specific checks only

```bash
node skills/portable-deployment-audit/scripts/audit.cjs --target . --check credentials,configs
node skills/portable-deployment-audit/scripts/audit.cjs --target . --ports
node skills/portable-deployment-audit/scripts/audit.cjs --target . --docker
```

## Checks

- `credentials`: scan env/config/code files for likely secrets and hardcoded credentials
- `ports`: inspect explicit port exposure hints from config and compose files, respect `--allow-port`, and warn more strongly on commonly exposed service ports
- `configs`: flag risky debug logging, wildcard CORS, and obvious placeholder/default secrets
- `permissions`: inspect Unix mode bits on sensitive files; Windows reports limitations instead of guessing
- `docker`: inspect Dockerfile and compose files for root/privileged runtime, host networking, published ports, missing `HEALTHCHECK`, and floating tags
- `git`: flag repository exposure indicators such as exposed `.git` directories and missing `.gitignore`

## Notes

- `--fix` is intentionally disabled in this version.
- Findings are advisory and should be reviewed before making changes.
- Text output includes short remediation recommendations derived from the findings.
- The script performs file inspection only; no shell commands or external binaries are executed.
- For automation, prefer `--format json` and parse the structured report.
