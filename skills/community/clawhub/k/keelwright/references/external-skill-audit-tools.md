# Auditing third-party skills & scanning your own code — an authoritative toolset

Two different jobs, two toolsets. All choices are community-respected (NVIDIA / Semgrep /
Gitleaks), not anonymous registry skills. Everything installs locally, $0, no Docker, no
mandatory API key. You run these tools; this skill does not bundle their code, so their licenses
do not attach to redistributing the skill.

## Job A — audit SOMEONE ELSE'S skill before installing (R11)

Agents install skills/MCP from registries — an attack surface: ~26% of community skills carry
vulnerabilities (NVIDIA), a large share have toxic data flows, some are outright malicious.

### NVIDIA SkillSpector — primary (Apache 2.0)

Install: `uv tool install skillspector`  (or `uv tool install git+https://github.com/NVIDIA/skillspector.git`)

```bash
skillspector scan ./skill-dir --no-llm            # static scan ($0)
skillspector scan https://github.com/owner/repo --no-llm   # git URL BEFORE install
skillspector scan ./skill --format sarif          # CI
skillspector scan ./skill --format json           # machine-readable
```

- **68 patterns / 17 categories:** prompt injection, data exfiltration, privilege escalation,
  supply chain, excessive agency, output handling, system-prompt leakage, memory poisoning,
  tool misuse, rogue agent, anti-refusal, trigger abuse, dangerous code (AST), taint tracking,
  YARA signatures, MCP least privilege, MCP tool poisoning.
- Formats: terminal / JSON / Markdown / SARIF. Risk score 0-100 + severity + remediation.
- Multi-input: git repo, URL, zip, dir, single file. Live-CVE via OSV.dev + offline fallback.
- Baseline suppression (fingerprint) — on re-scan only NEW findings surface.
- `--no-llm` = pure static (no API). Optional 2nd stage — LLM semantics (needs a key).

**Rule:** reject on a high risk score / CRITICAL-HIGH findings. When in doubt — ask the user.

## Job B — vulnerabilities in your OWN code (Gate 1)

### Gitleaks — secrets (MIT, gold standard)

```bash
gitleaks protect --staged --redact -v    # staged before commit (pre-commit gate)
gitleaks detect --redact -v              # whole repo/history
gitleaks detect --report-format sarif --report-path gl.sarif   # CI
```

### Semgrep — SAST (LGPL 2.1, industry standard)

```bash
semgrep scan --config=auto --error ./src
semgrep scan --config=auto --sarif -o sg.sarif ./src
```
`--config=auto` catches generic issues (secret/injection/crypto/path-traversal). Language your
SAST doesn't cover well → add a grep layer in your binding file.

## Wrapper/OS pitfalls (matters for Python-based CLI tools)

Some agent runtimes export a `PYTHONPATH` that points at the runtime's own venv and contaminates
any other Python process → `ModuleNotFoundError: pydantic_core._pydantic_core`. Fix: prefix the
command with an empty `PYTHONPATH=`. Go binaries (Gitleaks) are unaffected.

On Windows/MSYS shells, some scanners don't accept MSYS paths (`/tmp/x`, `/c/…`) → wrap paths in
`$(cygpath -w <path>)`. Semgrep also needs the `scan` subcommand when given an explicit path.

## A note on choosing tools

Prefer authoritative, actively maintained tools (NVIDIA, Semgrep, Gitleaks) over anonymous
registry skills with unclear provenance. A runtime "guard" that only exists as a registry skill
for another agent framework won't work in yours; a dedicated scanner (SkillSpector) covers the
same job with a clear license and a real maintainer.

Useful primitive kept from the research (not a skill): the OSV.dev query for auditing
dependencies in any ecosystem with no local tooling —
```bash
curl -s -X POST https://api.osv.dev/v1/query -H "Content-Type: application/json" \
  -d '{"package":{"name":"LIBRARY_NAME","ecosystem":"npm"}}'
```
