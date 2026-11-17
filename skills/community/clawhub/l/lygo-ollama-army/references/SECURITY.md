# Security — LYGO Ollama Army v0.9.0

## Defaults (honest)

| Capability | Status |
|------------|--------|
| Network | **localhost Ollama only** (`http://localhost:11434`) |
| Public HTTPS | **None** in this package |
| Subprocess / shell | **None** |
| Desktop installers | **Not shipped** |
| Planting / social / publish | **Not shipped** |
| Queue roles | Hard allowlist `SAFE_ROLES` |

## Threat model

1. **Queue injection** — Only `SAFE_ROLES` execute; other roles are refused and logged.  
2. **Outbound exfil** — No webhook POST; no public probe modules in package.  
3. **Process spawn** — No PS1 launchers; in-process threads only.  
4. **Ollama host** — Fixed to localhost (not user-configurable remote URL).

## Dual channel

| Channel | Surface |
|---------|---------|
| ClawHub public | This package (local Ollama army) |
| SkillHub FULL | Optional operator automation (separate zip) |

**Δ9Φ963 — local flame only on ClawHub.**
