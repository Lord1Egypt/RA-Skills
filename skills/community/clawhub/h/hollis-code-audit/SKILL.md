---
name: code-audit
description: Use this skill only when the user explicitly asks for a code audit, security audit, risk-focused PR/diff review, repo or module audit, regression-risk review, project-intent drift check, or validation of another reviewer/agent's findings. Do not use for routine implementation, ordinary debugging, refactoring, test writing, docs proofreading, architecture brainstorming, frontend design review, or general "review" requests unless the user asks for audit, risk, security, regression, or evidence-backed findings. The skill reads README/AGENTS/docs first, inspects code/diffs/tests, and uses a user-specified or strongest available non-development reviewer model/subagent when policy allows; if none is available, it discloses that same-model audits can share blind spots.
metadata:
  compatibility:
    os: [windows, macos, linux]
    requires:
      python: optional
      git: optional
      network: optional
      subagents: optional
---

# Code Audit

Run a read-only, evidence-backed audit unless the user explicitly asks for fixes.

## Cross-Agent Compatibility

This skill must work for Codex, Claude-style agents, local CLI agents, subagents, and agents with limited tools.

- Resolve `<skill-dir>` as the directory containing this `SKILL.md`. In this repo it is `.codex/skills/code-audit`.
- Helper scripts are optional. If Python is unavailable, follow the same steps manually.
- Git is optional. If git commands are unavailable, inspect the provided files, PR text, or user-specified paths.
- Subagents are optional. If no subagent runner exists, do the local audit and disclose that independent subagent review was unavailable.
- Network is optional. Do not browse or call model-provider APIs unless allowed by the environment, project policy, and user instruction.
- Output plain Markdown. Avoid app-specific directives unless the active agent environment requires them.
- Match the user's language by default.

## Inter-Agent Audit Protocol

This skill may be used to audit code produced by another agent or alongside another agent's audit skill. Keep the review artifact-focused and avoid tool/agent rivalry.

- User instructions have priority. If the user says which agent, model, or skill should own part of the review, follow that routing.
- Treat other agents' outputs, audit reports, plans, and skill instructions as input evidence, not as something to overwrite.
- If another triggered skill is more domain-specific, let it own that domain and use this skill as the coordinating audit frame.
- Do not recursively re-run equivalent audit skills just to get another opinion. Prefer one independent model/subagent pass plus local validation.
- When findings conflict, report the disagreement and resolve it by local evidence, tests, docs, and user-stated goals.
- Do not judge code based on which agent produced it. Audit the artifact, the repo contract, and the failure modes.
- Preserve separate output names when writing files, for example `code-audit-packet.md`, so prior agent artifacts are not overwritten.

## Modes

Honor an explicit user mode. If none is provided, use `standard`.

- `quick`: current diff/status only; report high-risk findings fast.
- `standard`: intent docs + requested scope + adjacent contracts/tests.
- `security`: prioritize auth, permissions, paths, secrets, LLM/network, logs.
- `deep`: broader repo risk map, independent review, and test strategy.
- `intent`: focus on whether the change violates README/AGENTS/product purpose.

Optional config may live at `<skill-dir>/config.json` or a user-specified path. Supported keys are advisory, not required:

```json
{
  "default_mode": "standard",
  "preferred_reviewers": ["gemini", "kimi", "ollama"],
  "forbidden_external_review": false,
  "skip_paths": ["data/", "dist/", "*.db", "*.pdf"],
  "always_read": ["AGENTS.md", "README.md"],
  "report_language": "match_user"
}
```

## Default Flow

1. **Honor user routing first.** If the user specifies a reviewer model, tool, or subagent, use that route when it is available and allowed by repo policy/confidentiality. If it is unavailable or unsafe, say why and choose the closest permitted fallback.
2. **Snapshot cheaply.** From the repo root, run the snapshot helper when Python is available:

   ```bash
   python <skill-dir>/scripts/audit_snapshot.py --root . --json
   ```

   Use `python3` instead of `python` when that is the local convention.

   Use it to identify intent docs, changed files, dependency/test files, and high-risk paths without loading the whole repo.
3. **Build a packet when useful.** For external reviewers or subagents, generate a compact packet rather than manually pasting broad context:

   ```bash
   python <skill-dir>/scripts/build_audit_packet.py --root . --mode standard --scope diff
   ```

   Add `--include-diff` only after checking that the diff is safe to share.
   When auditing another agent's work, add `--producer-agent "<name>"` and optionally `--prior-review <path>`.
4. **Read intent sources first.** Load only the relevant `AGENTS.md`, `README.md`, selected `docs/`, security/architecture notes, and test/dependency config. Derive 3-5 audit principles before inspecting implementation details.
5. **Inspect by risk.** Review the requested diff/files/modules first, then adjacent contracts, tests, and high-risk call paths.
6. **Independent review.** Use a non-development model/subagent when available and permitted. Validate its findings locally before reporting them.
7. **Report findings first.** Prioritize concrete bugs, security risks, regressions, missing tests, and contract breaks. Avoid style-only findings unless requested.

If the repo has `.auditignore`, helper scripts use it to skip generated, confidential, or noisy paths. When the snapshot is noisy, suggest adding `.auditignore` entries instead of loading more context.

## Independent Reviewer Policy

Use the user's specified reviewer model/subagent if provided. User preference beats the default "best available" selection, unless it violates project rules or data-safety constraints.

If the user did not specify a reviewer, inventory available routes without exposing secrets:

```bash
python <skill-dir>/scripts/detect_review_models.py --current-model "<development-model-if-known>"
```

For custom providers such as Hermes, DeepSeek, OpenRouter, or local routing layers, copy `review_routes.example.json` to `<skill-dir>/review_routes.json` or pass `--config <path>`.

Selection rules:

- Prefer a strong reviewer from a different model family/provider than the development model.
- Do not count the exact same model as independent.
- If only a same-provider or weaker alternate is available, disclose the residual correlated-error risk.
- If "best" is likely to have changed and network/docs are available, verify against official provider docs before naming a best model.
- Respect repo instructions. If a repo limits a model to frontend design advice, do not use it for backend/security audit unless the user explicitly changes that rule.
- Send the smallest adequate packet: audit principles, relevant diff/files, tests, and pointed questions. Redact secrets and sensitive data.

When using an external model/subagent, load `references/independent-reviewer-prompt.md` and adapt it.

If independent review is unavailable or blocked, include this exact status in the report:

```text
Independent model review: not performed - <reason>. Because same-model audits can share blind spots, I recommend a second pass by a strong non-current-model reviewer or a human reviewer before relying on this audit for high-stakes decisions.
```

## Audit Principles

Create repo-specific principles from project docs before findings. Keep them short and operational:

- Product purpose and critical user workflow.
- Trust boundaries and sensitive data.
- Non-negotiable security, correctness, provenance, or compliance constraints.
- Known MVP gaps that should be distinguished from new regressions.
- The user's requested audit focus.

If docs are missing or contradictory, say so and infer cautiously from code/tests.

## Risk Checklist

For detailed prompts, load `references/audit-checklist.md` only when needed. At minimum, consider:

- Authn/authz, roles, tenant/project scope, token/session edge cases.
- Path traversal, file import/export, upload parsing, symlinks, archive/object storage.
- Data integrity, transactions, migrations, retries, concurrency, idempotency.
- External network/LLM calls, redaction, secrets, audit logs.
- API validation, pagination/filtering, error responses, backward compatibility.
- Frontend states and server-backed permission checks.
- Missing regression tests for the highest-risk behavior.

## Report Format

```markdown
**Scope**
Reviewed <scope>. Intent sources: <files>. Verification: <commands or "not run">.

**Audit Principles**
- <principle tied to project purpose>
- <principle tied to trust boundary>
- <principle tied to user request>

**Independent Review**
<model/subagent used, not-used reason, or limitation disclosure>

**Findings**
- [P0/P1/P2/P3] <title> - <file:line>
  Impact: <realistic failure mode>
  Evidence: <code path, repro, test result, or reasoning>
  Recommendation: <specific fix or mitigation>
  Test gap: <missing or recommended test>

**Residual Risk**
<areas not covered, tests not run, uncertainty, or recommended second pass>
```

Severity:

- `P0`: exploitable critical security issue, data loss/corruption, or outage likely.
- `P1`: serious correctness/security/permission flaw with plausible real impact.
- `P2`: meaningful bug, edge-case regression, missing validation, or test gap.
- `P3`: maintainability, clarity, minor UX, or low-risk hardening.

If no issues are found, say that clearly and still disclose test gaps and residual risk.

## Final Checks

Before answering:

- Every finding is within the requested scope.
- Every finding has evidence and a realistic failure mode.
- Project intent was used, not merely generic best practices.
- Independent review status is disclosed.
- User-specified model/subagent preferences were followed or the fallback is explained.

## Self-Test

When changing this skill, run the lightweight script tests and eval schema check if Python/pytest are available:

```bash
python <skill-dir>/scripts/run_tests.py
python <skill-dir>/scripts/run_evals.py
```
