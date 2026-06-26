---
name: pharmaclaw-ip-expansion-agent
description: >-
  Intellectual Property Expansion Agent for pharma drug discovery/development teams.
  Proactively manages/expands IP portfolios by analyzing SMILES/molecules from other agents
  (Drug Discovery/Synthesis), performing infringement/FTO analyses via RDKit similarity & patent APIs,
  mining prior art for novelty suggestions (bioisosteres/derivatives), and recommending strategic claims.
  Triggers on: IP/patent/FTO/infringement/novelty/prior art queries for molecules/SMILES/therapeutics;
  portfolio tracking; chaining with chemistry-query/Tox/Safety agents.
  Use for patentable derivative ideas, risk matrices, white space identification, expiration monitoring.
---

# Pharma IP Expansion Agent

Specialized agent extending pharma team agents (Drug Discovery, Synthesis via chemistry-query, Patent/Literature/Tox/Safety).
Analyzes inputs (SMILES, keywords, profiles) for actionable IP insights: portfolio mgmt, infringement/FTO, prior art novelty,
strategic expansion. Outputs JSON/MD reports + RDKit viz (PNG/SVG).

## Core Capabilities

Follow workflow: Parse input → Analyze → Generate report → Log to portfolio DB.

1. **Portfolio Management**: Track assets (patents/apps), monitor expirations. Use `scripts/agent.py track`.
2. **Infringement Analysis**: RDKit Morgan FP Tanimoto (>0.8 flag risk) vs patent compounds.
3. **FTO Assessments**: USPTO/PubChem searches for blocking patents in area.
4. **Prior Art Mining/Novelty**: NLP extract claims/chemicals → suggest RDKit bioisosteres evading art.
5. **Strategic Expansion**: Recommend continuations/repurposing based on trends.

## Quick Start

Exec main agent:
```
python3 scripts/agent.py --mode analysis --input '{"smiles": ["CCO"], "from_agent": "synthesis", "therapeutic": "pain"}'
```
Output: JSON report w/ risks, suggestions, viz saved to assets/.

For multi-agent chaining (OpenClaw): Spawn sub-session w/ this skill active, pass JSON from chemistry-query.

## Workflow Decision Tree

- **Input JSON/SMILES?** → RDKit parse → Fingerprint → Compare patents (scripts/rdkit_utils.py)
- **Portfolio query?** → SQLite query (self.db)
- **FTO/Prior art?** → API fetch → NLP parse (references/nlp_patterns.md) → Similarity
- **Strategic?** → Market trends via PubChem stats + derivatives
- **Edge: Intl/PCT/AI-inv?** → Note variations, flag enablement risks.

Always output structured JSON: `{"risks": [...], "suggestions": [...], "viz_path": "report.png", "recommendations": {...}}` + MD report.

## Multi-Agent Integration (OpenClaw)

- Input from Synthesis/chemistry-query: `{"smiles": [...], "reactions": [...]}` → Auto infringement check.
- Chain w/ Tox/Safety: Incorporate ADMET/safety to prioritize claims.
- Spawn: `sessions_spawn task="IP expand this SMILES from synth: ..."`
- Autonomous: Cron portfolio checks.

## Resources

### scripts/
- `agent.py`: Main class IPExpansionAgent w/ all methods. Exec directly or import.
- `rdkit_utils.py`: FP/similarity/bioisosteres.
- `patent_fetch.py`: USPTO/PubChem APIs.
- `nlp_extract.py`: Claims/chem names (spaCy).

Test: `python3 scripts/agent.py --help`

### references/
- `apis.md`: USPTO/EPO/PubChem endpoints.
- `rdkit_guide.md`: FP radii, Tanimoto thresholds.
- `ip_strategies.md`: Claims types, FTO best practices.
- `pharma_trends.md`: AI-IP, PCT notes.

Load via `read references/apis.md` for API details.

### assets/
- `report_template.md`: MD report format.
- `portfolio_schema.sql`: DB init.
- `risk_matrix_template.svg`: Editable viz.

Copy to outputs.

## Implementation Notes
- DB: SQLite `ip_portfolio.db` (assets/portfolio_schema.sql).
- Thresholds: Tanimoto>0.85 high risk; configurable.
- Viz: RDKit PNG/SVG to current dir.
- Deps: `pip install rdkit-pypi requests pandas sqlite3 spacy scispacy` (assume chemistry env).
- Logging: To `logs/ip_expansion.log`.
- OpenClaw: Use `exec` on scripts/ for analysis; `write` reports.

For updates, edit class methods.
