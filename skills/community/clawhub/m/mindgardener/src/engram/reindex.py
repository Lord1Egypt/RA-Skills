"""Reindex — rebuild graph.jsonl from entity files.

Solves state drift: when users manually edit entity files,
the graph can become stale. Reindex scans all entity files,
parses wikilinks and relations, and rebuilds the graph.

No LLM calls — pure regex parsing. Fast and free.
"""

import json
import re
from datetime import datetime
from pathlib import Path

from .config import EngramConfig


def extract_relations_from_entity(filepath: Path) -> list[dict]:
    """Parse an entity file and extract all relationships."""
    content = filepath.read_text()
    name = filepath.stem.replace("-", " ")
    
    relations = []
    
    # Extract wikilinks from timeline entries
    # Pattern: "verb → [[Target]]: detail" or "[[Source]] verb → this: detail"
    for match in re.finditer(r'(\w[\w\s]*?)\s*→\s*\[\[([^\]]+)\]\](?::\s*(.*))?', content):
        predicate = match.group(1).strip()
        target = match.group(2).strip()
        detail = match.group(3).strip() if match.group(3) else ""
        
        # Skip date links
        if re.match(r'^\d{4}-\d{2}-\d{2}$', target):
            continue
        
        relations.append({
            "subject": name,
            "predicate": predicate,
            "object": target,
            "detail": detail,
        })
    
    # Extract "[[Source]] verb → this" patterns
    for match in re.finditer(r'\[\[([^\]]+)\]\]\s+(\w[\w\s]*?)\s*→\s*this(?::\s*(.*))?', content):
        source = match.group(1).strip()
        predicate = match.group(2).strip()
        detail = match.group(3).strip() if match.group(3) else ""
        
        if re.match(r'^\d{4}-\d{2}-\d{2}$', source):
            continue
        
        relations.append({
            "subject": source,
            "predicate": predicate,
            "object": name,
            "detail": detail,
        })
    
    # Extract simple wikilinks from Relations section
    in_relations = False
    for line in content.split("\n"):
        if line.strip() == "## Relations":
            in_relations = True
            continue
        if line.startswith("## ") and in_relations:
            break
        if in_relations:
            for link in re.findall(r'\[\[([^\]]+)\]\]', line):
                if not re.match(r'^\d{4}-\d{2}-\d{2}$', link):
                    # Check if this relation already exists
                    exists = any(
                        r["object"] == link or r["subject"] == link 
                        for r in relations
                    )
                    if not exists:
                        relations.append({
                            "subject": name,
                            "predicate": "related_to",
                            "object": link,
                            "detail": "",
                        })
    
    return relations


def extract_dates_from_entity(filepath: Path) -> list[str]:
    """Extract all timeline dates from an entity file."""
    content = filepath.read_text()
    return re.findall(r'### \[\[(\d{4}-\d{2}-\d{2})\]\]', content)


def reindex(config: EngramConfig) -> dict:
    """Rebuild graph.jsonl from entity files.
    
    Returns stats dict with counts.
    """
    if not config.entities_dir.exists():
        return {"entities": 0, "triplets": 0, "error": "No entities directory"}
    
    all_triplets = []
    seen = set()
    entity_count = 0
    
    for filepath in sorted(config.entities_dir.glob("*.md")):
        entity_count += 1
        relations = extract_relations_from_entity(filepath)
        dates = extract_dates_from_entity(filepath)
        
        # Use the most recent date, or today
        date_str = dates[-1] if dates else datetime.now().strftime("%Y-%m-%d")
        
        for rel in relations:
            key = (rel["subject"], rel["predicate"], rel["object"])
            if key not in seen:
                seen.add(key)
                rel["date"] = date_str
                rel["timestamp"] = datetime.now().isoformat()
                rel["source"] = "reindex"
                all_triplets.append(rel)
    
    # Write new graph file (backup old one first)
    if config.graph_file.exists():
        backup = config.graph_file.with_suffix(".jsonl.bak")
        config.graph_file.rename(backup)
    
    with open(config.graph_file, "w") as f:
        for t in all_triplets:
            f.write(json.dumps(t) + "\n")
    
    return {
        "entities": entity_count,
        "triplets": len(all_triplets),
    }
