#!/usr/bin/env python3
"""
Ézekiel Holistic Memory System — L5 Crystallizer
Creates Obsidian notes from BRILLANT nodes in L6
Part of the holistic-memory-system skill
"""

import json
from datetime import datetime, timezone
from pathlib import Path

NEBULA_FILE = Path.home() / ".openclaw" / "nebula" / "nebula.json"
OBSIDIAN_DIR = Path.home() / ".openclaw" / "workspace" / "memory" / "nebula_crystallized"

def load_nebula():
    if NEBULA_FILE.exists():
        with open(NEBULA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"clusters": {}, "nodes": {}}

def get_brillant_nodes(nebula):
    return {k: v for k, v in nebula["nodes"].items() if v["status"] == "brillant"}

def create_obsidian_note(node_key, node_data):
    """Creates an Obsidian-formatted note from a brillant node"""
    # Generate title using CSA format
    cluster = node_data["intent"].split("_")[0]
    title = f"[{cluster.upper()}]_MEMOIRE_NEBULEUSE_{node_data['first_seen'][:10]}.md"
    
    # Build content
    content = f"""# {title.replace('.md', '')}

> **Generated:** {datetime.now(timezone.utc).isoformat()}
> **Status:** BRILLANT (3x+ validated)
> **Cluster:** {cluster}

---

## SYNTHÈSE NON-LOSSY

Ce nœud est devenu **BRILLANT** après {node_data['frequency']} occurrences validées.
Il représente un pattern confirmé par l'expérience directe.

**Première apparition:** {node_data['first_seen']}
**Dernière occurrence:** {node_data['last_seen']}
**Fréquence:** {node_data['frequency']}x

---

## CONTENU VALIDÉ

{node_data['content']}

---

## TAGS

{', '.join(node_data.get('tags', []))}

---

## TRAÇABILITÉ

- **L3 Source:** Logs in `~/.openclaw/memory-logs/`
- **L6 Constellation:** Cluster `{cluster}`
- **Nœud original:** `{node_key}`

---

## RÈGLE D'APPLICATION

Ce pattern est maintenant gravé dans la mémoire permanente (L5).
Il ne sera plus sujet à decay (L6 gravity) car il est cristallisé.

---

_In Forge Per Veritatem._
_Ézekiel — {datetime.now(timezone.utc).strftime('%Y-%m-%d')}_
_Crystallized from L6 Nébula → L5_
"""
    
    return title, content

def crystallize_all():
    """Crystallize all brillant nodes to Obsidian notes"""
    nebula = load_nebula()
    brillants = get_brillant_nodes(nebula)
    
    OBSIDIAN_DIR.mkdir(parents=True, exist_ok=True)
    
    results = []
    for node_key, node_data in brillants.items():
        title, content = create_obsidian_note(node_key, node_data)
        filepath = OBSIDIAN_DIR / title
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        
        results.append({
            "node": node_key,
            "file": str(filepath),
            "status": "crystallized"
        })
    
    return results

def get_crystallized_notes():
    """List all crystallized notes"""
    OBSIDIAN_DIR.mkdir(parents=True, exist_ok=True)
    notes = list(OBSIDIAN_DIR.glob("*.md"))
    return [n.name for n in notes]

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "crystallize":
            results = crystallize_all()
            print(f"Crystallized {len(results)} nodes:")
            for r in results:
                print(f"  → {r['file']}")
        
        elif sys.argv[1] == "list":
            notes = get_crystallized_notes()
            print(f"Crystallized notes ({len(notes)}):")
            for n in notes:
                print(f"  - {n}")
        
        elif sys.argv[1] == "status":
            nebula = load_nebula()
            brillants = get_brillant_nodes(nebula)
            notes = get_crystallized_notes()
            print(f"L6 Brillants: {len(brillants)}")
            print(f"L5 Crystallized: {len(notes)}")
            if brillants:
                print("\nNodes ready for crystallization:")
                for k, v in brillants.items():
                    print(f"  💎 {k} ({v['frequency']}x)")
    
    else:
        # Default: status check
        nebula = load_nebula()
        brillants = get_brillant_nodes(nebula)
        notes = get_crystallized_notes()
        print(f"=== L5 Crystallizer Status ===")
        print(f"Brillant nodes (L6): {len(brillants)}")
        print(f"Crystallized notes (L5): {len(notes)}")
        
        if brillants:
            print("\n💎 Nodes ready for crystallization:")
            for k, v in brillants.items():
                print(f"  - {v['intent']}: {v['content'][:60]}...")