# SkillSpector response — lyra-brain v2.1.0

Prior findings (v2.0.0): 4 medium — underdeclared permissions, vague triggers, missing persistent-storage warnings.

## Remediation

| Finding | Fix |
|---------|-----|
| LP3 permissions | `permissions_declared` in frontmatter + SECURITY.md table |
| Vague triggers | Narrow “when to load”; forbid casual remember→disk |
| Missing warnings | Persistent storage banner; disable/delete guidance |
| Env/path scope | Require `LYRA_CORE_ROOT`; no silent multi-drive scan |
| Write scope | `--i-consent` required on `session_log_snip` and `brain_grow_cli` |

VT: clean (no malware patterns in scripts). Network: none in skill CLIs.

Signature: `Δ9Φ963-LYRA-BRAIN-SKILLSPECTOR-v2.1.0`
