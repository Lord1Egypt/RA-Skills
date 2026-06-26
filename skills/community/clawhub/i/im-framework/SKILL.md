---
name: im-framework
version: "1.5"
description: |
  Reference, explain, and apply the Immanent Metaphysics (IM) framework by Forrest Landry.
  Uses a structured ontology of 767 entities as an index into the live source text at mflb.com.
  Use when asked to explain IM concepts, apply the framework to a situation, trace derivation
  chains, or find source references. Triggers on: "immanent metaphysics", "IM framework",
  modality questions, axiom references, ICT, symmetry/continuity ethics, effective choice,
  path of right action, or any request to ground claims in the framework.
---

# Immanent Metaphysics Framework

Source: **https://mflb.com/8192** — Forrest Landry's whitebook. This is the canonical text.
The ontology in `references/graph.jsonl` is an index into it. Always fetch the source URL and quote exactly.

## Reference Files

All files are in `references/` (relative to this skill directory):

| File | Contents |
|------|----------|
| `graph.jsonl` | 767 entities — Concepts, Axioms, Theorems, Aphorisms, Implications + relations |
| `whitebook-map.jsonl` | 73-entry structural map of whitebook chapters/sections with URLs |
| `schema.yaml` | Type definitions and relation types |
| `section-anchors.json` | Anchor-level URL map for fine-grained source links |

## Workflow

1. **Search the graph** — find the relevant entity in `references/graph.jsonl`
2. **Get the URL** — use the `location` field from the entity's properties
3. **Fetch the source** — `web_fetch(location_url)` to get exact text
4. **Quote verbatim** — cite with URL

## Graph Query Examples

```bash
# Set path relative to skill dir (resolve from dirname of SKILL.md)
GRAPH="$(dirname $(realpath ~/Tillerman/Eitan/skills/im-framework/SKILL.md))/references/graph.jsonl"

# Search by concept name
grep -i '"name": "symmetry"' "$GRAPH"

# Search by keyword across names and definitions
python3 << 'EOF'
import json
GRAPH = "/Users/Jared/Tillerman/Eitan/skills/im-framework/references/graph.jsonl"
TERM = "symmetry"  # change this
for line in open(GRAPH):
    d = json.loads(line)
    if d.get('op') != 'put':
        continue
    e = d.get('entity', {})
    p = e.get('properties', {})
    name = p.get('name', p.get('word', p.get('text', '')))
    defn = p.get('definition', '')
    loc = p.get('location', '')
    if TERM.lower() in (name + defn).lower():
        print(f"{e['type']}: {name}")
        print(f"  URL: {loc}")
        print(f"  Def: {defn[:300]}")
        print()
EOF

# List all entity types and counts
python3 << 'EOF'
import json
from collections import Counter
GRAPH = "/Users/Jared/Tillerman/Eitan/skills/im-framework/references/graph.jsonl"
types = Counter()
for line in open(GRAPH):
    d = json.loads(line)
    if d.get('op') == 'put':
        types[d['entity']['type']] += 1
print(types)
EOF

# Search section anchors for a chapter
python3 << 'EOF'
import json
ANCHORS = "/Users/Jared/Tillerman/Eitan/skills/im-framework/references/section-anchors.json"
anchors = json.load(open(ANCHORS))
# anchors is a dict of {anchor_id: {title, url, ...}}
TERM = "ethics"
for k, v in anchors.items():
    if TERM.lower() in str(v).lower():
        print(k, "->", v.get('url', ''), "|", v.get('title', ''))
EOF
```

## Quoting Rules (MANDATORY)

- **Always use exact quotes from the source at mflb.com.** Never paraphrase when the original is available.
- **Every quote must include the direct URL** from the entity's `location` field.
- **Quote format:**
  > "[exact text from mflb.com]"
  > — *An Immanent Metaphysics*, [section], [URL]
- **If the exact wording isn't in the ontology:** `web_fetch` the URL directly — get the real text.
- **Aphorisms:** use the `text` field from `graph.jsonl` verbatim. Do not alter.
- **Definitions:** use the `definition` field verbatim when citing what a term means.
- **Label synthesis clearly:** if applying the framework to a new situation, say so — don't present inference as direct quote.

## Ontology Contents (`references/graph.jsonl`)

767 entities across 5 types:

| Type | Count | Description |
|------|-------|-------------|
| Concept | 134 | Named ideas — modality, domain, definition, source URL |
| Axiom | 3 | Foundational axioms — statement, implications, source URL |
| Theorem | 11 | ICT, Symmetry Ethics, Continuity Ethics, Bell's/Godel mappings |
| Aphorism | 147 | From *Effective Choice* — exact text, themes, source URL |
| Implication | 4 | Cross-domain applications (physics, logic, ethics, consciousness) |

Relations: `implies`, `paired_with`, `contrasts_with`, `depends_on`, `has_modality`, `illuminates`, `defined_in`

## Chapter URLs

| Topic | URL |
|-------|-----|
| Entry point | https://mflb.com/8192 |
| Three Modalities | https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch1.htm#1_modalities |
| Axioms | https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch1.htm#1_axioms |
| ICT | https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch3.htm#1_ict |
| Symmetry / Continuity | https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch3.htm#1_symmetry |
| Ethics | https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch6.htm |
| Path of Right Action | https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch6.htm#2_path |
| Basal Motivations | https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch6.htm#2_basal |
| Aphorisms of Effective Choice | https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch5.htm |
| Mind | https://mflb.com/dvol/control/pcore/own_books/white_1/wb_web_2/zout/upmp_ch8.htm |

## Attribution

Always attribute to Forrest Landry's *An Immanent Metaphysics*. Distinguish:
1. **Direct citation** — exact quote with source URL
2. **Close paraphrase** — labeled as paraphrase with source URL
3. **Agent synthesis** — labeled as your own application

Do not invent positions. Do not imply Forrest's endorsement of claims not grounded in the source text.
