# SkillSpector — lygo-ollama-army v0.9.0 ground-up rebuild

**Source:** https://clawhub.ai/deepseekoracle/skills/lygo-ollama-army/security-audit

## Why rebuild

v0.8.x kept a large operator surface (plant, social, sentinel HTTPS, desktop installers, idle supervisors).  
SkillSpector correctly treated **config-gated high-impact paths** and **desktop consent injection** as residual risk.

## v0.9.0 public package

| Removed from ClawHub package | Reason |
|------------------------------|--------|
| Desktop `install_*.ps1` / full-capacity PS1 | Persistence + consent bypass patterns |
| Genesis collector + remote probes | Outbound HTTPS / status noise |
| Plant / registry / self-tune / social roles | High-impact stack & outbound actions |
| Stack-tool `runpy` allowlist for audits/pulses | Excessive agency via queue |
| `army_config` automation supervisors | Background high-impact loops |
| Raw `localhost` install-source style links in status artifacts | Static `install_untrusted_source` |

| Kept | Purpose |
|------|---------|
| `ollama_client.py` | localhost Ollama only |
| `ollama_daemon.py` | SAFE_ROLES only |
| `ollama_army_launcher.py` | In-process threads |
| `queue_task.py` | Explicit task drop |
| `scripts/self_check.py` | Policy tests |

## Residual

- Local Ollama still processes prompts you queue (expected).  
- FULL operator pack is **not** this slug’s public surface.

```bash
python scripts/self_check.py
```

**Δ9Φ963 — pass by removal of unsafe surface, not by comment gates alone.**
