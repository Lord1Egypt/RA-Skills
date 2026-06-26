# Security Checklist Before Install

Use this checklist before installing or running any external package for this skill.

## 1) Verify package provenance
- Confirm package identity on PyPI and GitHub:
  - Package name: opendataloader-pdf
  - Homepage/repository must match official project metadata.
- Review maintainers, release history, and recent activity.
- Prefer install instructions that point to a verified repository and pinned versions.
- Reject installation if homepage/repository metadata is missing or inconsistent.

## 2) Isolate execution
- Do not install globally.
- Use one of these isolation options:
  - Python venv
  - Container
  - Disposable VM

## 3) Audit dependencies
- Inspect dependency tree before production use.
- Treat unknown transitive dependencies as risk until reviewed.
- Keep a lock file or pinned requirements for reproducible installs.
- Prefer pinned installs, for example:
  - pip install "opendataloader-pdf==<version>"
  - pip install "opendataloader-pdf[hybrid]==<version>"

## 4) Network exposure controls
- Ensure hybrid backend is local-only.
- Prefer explicit localhost binding when available.
- Validate active listeners before processing sensitive PDFs.
- If supported by the backend CLI, bind explicitly:
  - opendataloader-pdf-hybrid --host 127.0.0.1 --port 5002
- Verify listeners:
  - Windows: netstat -ano | findstr 5002
  - Linux/macOS: ss -ltnp | grep 5002

## 5) Privacy and safety guarantees
- If privacy guarantees are required, request an explicit install spec from skill owner:
  - Source/homepage URL
  - Required runtimes (Java/Python versions)
  - Expected network behavior (local only)
  - Verified install command with pinned versions

## 6) Operational policy
- Treat any unverified pip install as potentially risky.
- Run security review before first install and after major upgrades.

## Quick verification commands
- python -m venv .venv
- .venv\Scripts\activate
- pip install --upgrade pip
- pip index versions opendataloader-pdf
- pip show opendataloader-pdf

## Minimal safe install template
1) Create isolated environment (venv/container/VM).
2) Verify package metadata (PyPI + homepage + repository).
3) Install pinned version (avoid unpinned -U in production).
4) Freeze dependencies to a lock file.
5) Run hybrid backend with localhost binding and verify active listeners.

Note: These checks reduce risk but do not eliminate supply-chain risk.