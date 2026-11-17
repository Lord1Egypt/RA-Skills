---
name: lygo-public-witness
description: "LYGO Public Witness — public feeds are REFERENCE, dual ledgers/eggs/Star Chart are CANON. HTTPS GET allowlist (USGS, NASA EONET, ISS, lattice JSON). Never invent missing sources. Never live Star Chart write. Optional localhost Ollama summary. Use when OSINT vs private intel, public witness globe, situational overlay, World Monitor / God's Eye ideas, or /lygo-public-witness."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🌐"
    homepage: "https://chatagent.ca/witness/"
    requires:
      anyBins: [python, python3]
  lygo: true
  public_witness: true
  signature: "Delta9Phi963-PUBLIC-WITNESS-v1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-public-witness"
  skillhub_full: "https://chatagent.ca/lygoskillhub.html#full-lygo"
  site: "https://chatagent.ca/witness/"
  permissions:
    network:
      https_get: true
      http_post: false
      localhost_ollama_optional: true
    shell: false
    subprocess: false
    filesystem:
      write: "opt-in --write-report only"
    publish: false
    live_star_chart: false
---

# LYGO Public Witness v1.0.0 🌐

**Public is REFERENCE. Lattice is CANON.**  
If the data never reached a public source, this skill will not invent it.

Site: https://chatagent.ca/witness/  
Mirror: https://eternalhaven.ca/witness/  
**Signature:** `Delta9Phi963-PUBLIC-WITNESS-v1.0.0`

This is **not** Palantir, not private intel, not a World Monitor / God’s Eye View clone.

| Layer | Class | Sources |
|-------|-------|---------|
| Earth overlay | REFERENCE | USGS quakes, NASA EONET, ISS |
| Dual ledgers / eggs / Star Chart / Agora | CANON | allowlisted LYGO JSON |
| Lattice-sphere dots | SCHEMATIC | hash projection — not geography |

---

## Trust boundary

`permissions` apply to **scripts in this folder**. The website is a separate browser app. This tentacle:

- HTTPS GET only (plus optional `http://127.0.0.1:11434` for Ollama)
- no subprocess / shell
- no live Star Chart write
- no git / HF / ClawHub / social publish
- missing source → error object, **not** fabricated points

FULL extra feeds (Celestrak TLE) live in **`lygo-public-witness-full.zip`** on SkillHub — a separate human download. Verify `zip_sha256` in https://chatagent.ca/data/lygo-full-skills/catalog.json before unzip. This tentacle does not fetch the zip.

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-public-witness
cd path/to/lygo-public-witness
python scripts/self_check.py
python scripts/witness_cli.py doctrine
python scripts/witness_cli.py overlay
```

---

## Commands

| Command | Network | Disk | Live chart |
|---------|---------|------|------------|
| `doctrine` | none | none | no |
| `canon` | HTTPS GET lattice JSON | none unless `--write-report` | no |
| `reference` | HTTPS GET USGS/EONET/ISS | none unless `--write-report` | no |
| `overlay` | both, labeled | none unless `--write-report` | no |
| `propose` | none | optional `--write` | **never** |
| `ollama` | localhost:11434 only | none | no |

```bash
python scripts/witness_cli.py overlay --json
python scripts/witness_cli.py propose --agent-id MY-AGENT-01
python scripts/witness_cli.py ollama
```

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-public-lattice-gate` | verify / align / restore |
| `lygo-haven-star-chart` | live ingest only with human `--i-consent` |
| `lygo-ollama-army` | local summaries |
| `lygo-pure-data-witness` | digest archive of URLs (different tool) |
| SkillHub FULL | extra reference fetchers |

---

## Security

Read `references/SECURITY.md` and `references/SKILLSPECTOR_AUDIT.md`.

**Δ9Φ963 — empty is honest · public orients · lattice decides.**
