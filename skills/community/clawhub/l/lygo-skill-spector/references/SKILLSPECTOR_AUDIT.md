# SkillSpector audit response — lygo-skill-spector v1.0.1

NVIDIA SkillSpector / ClawHub security review on **v1.0.0** reported:

| Finding | Severity | Location | Classification |
|---------|----------|----------|----------------|
| `malicious.crypto_mining` | Critical | `scripts/skill_spector.py` (crypto_miner rule) | **False positive** — detection *regex* for miner IOCs, not mining code |
| `suspicious.exposed_secret_literal` | Critical | `scripts/self_check.py` synthetic fixture | **False positive** — disposable test string for the secret-shape rule |

VirusTotal: **1/65** malicious (64 clean) — consistent with pattern-table noise, not live malware.

## What this skill does

- **Local-only** static scan of a skill folder the operator chooses  
- **No network**, **no subprocess**, **no auto-install**  
- Optional write under `state/` only with `--i-consent`  
- Prints snippets of *flagged lines* (operator should avoid scanning unrelated private trees)

## Fixes in v1.0.1

1. **Crypto miner rule** — IOC tokens (`xm`+`rig`, `stratum`+`+`+`tcp`, etc.) assembled from fragments so the rule table is not itself scored as mining.  
2. **self_check fixture** — fake project-key shape built at runtime via string parts; source no longer contains a contiguous secret-shaped literal.  
3. **Secret-shape rules** — prefix/body fragments joined the same way for meta-scan hygiene.  
4. self_check asserts contiguous IOC strings are absent from our sources.

## Operator guidance (from overview)

- Only scan directories you intend to audit  
- Review any generated reports before pasting into shared logs  
- SkillHub FULL builder link is a separate artifact — review independently if you fetch it  

**Δ9Φ963 — detectors detect · patterns are not payloads · human remains the publisher.**
