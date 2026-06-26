#!/usr/bin/env python3
"""
Multi-agent memory sync for MindGardener.

Per-agent memories merged with conflict resolution.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

from .conflicts import detect_conflict, log_conflict, resolve_conflict
from .filelock import file_lock


def get_agent_memory_dir(workspace: Path, agent_id: str) -> Path:
    """Get memory directory for a specific agent."""
    return workspace / "memory" / "agents" / agent_id


def list_agents(workspace: Path) -> list[str]:
    """List all agents with memory directories."""
    agents_dir = workspace / "memory" / "agents"
    if not agents_dir.exists():
        return []
    return [d.name for d in agents_dir.iterdir() if d.is_dir()]


def merge_graphs(
    source_graphs: list[Path],
    target_graph: Path,
    conflicts_file: Path,
    strategy: str = "latest_wins",
    dry_run: bool = True,
) -> dict:
    """
    Merge multiple graph.jsonl files into one.
    
    Returns stats: {added, conflicts, skipped}
    """
    # Load all existing facts from target
    existing = {}
    if target_graph.exists():
        for line in target_graph.read_text().strip().split('\n'):
            if not line:
                continue
            try:
                fact = json.loads(line)
                key = (fact.get("subject"), fact.get("predicate"), fact.get("object"))
                existing[key] = fact
            except:
                continue
    
    # Collect all facts from sources
    to_add = []
    conflicts = []
    skipped = 0
    
    for source in source_graphs:
        if not source.exists():
            continue
        
        for line in source.read_text().strip().split('\n'):
            if not line:
                continue
            try:
                fact = json.loads(line)
                key = (fact.get("subject"), fact.get("predicate"), fact.get("object"))
                
                if key in existing:
                    # Same fact exists, check for conflict
                    old = existing[key]
                    if old.get("object") != fact.get("object"):
                        # Value conflict
                        conflict = detect_conflict(target_graph, fact, fact.get("provenance", {}))
                        if conflict:
                            conflicts.append(conflict)
                            log_conflict(conflicts_file, conflict)
                    skipped += 1
                else:
                    to_add.append(fact)
                    existing[key] = fact
                    
            except:
                continue
    
    # Write merged graph
    if not dry_run and to_add:
        with file_lock(target_graph):
            with open(target_graph, "a") as f:
                for fact in to_add:
                    f.write(json.dumps(fact) + "\n")
    
    return {
        "added": len(to_add),
        "conflicts": len(conflicts),
        "skipped": skipped,
    }


def sync_agent_to_shared(
    workspace: Path,
    agent_id: str,
    dry_run: bool = True,
) -> dict:
    """Sync one agent's memory to shared memory."""
    agent_dir = get_agent_memory_dir(workspace, agent_id)
    shared_dir = workspace / "memory"
    
    if not agent_dir.exists():
        return {"error": f"Agent {agent_id} has no memory directory"}
    
    agent_graph = agent_dir / "graph.jsonl"
    shared_graph = shared_dir / "graph.jsonl"
    conflicts_file = shared_dir / "conflicts.md"
    
    return merge_graphs(
        [agent_graph],
        shared_graph,
        conflicts_file,
        dry_run=dry_run,
    )


def sync_all_agents(
    workspace: Path,
    dry_run: bool = True,
) -> dict:
    """Sync all agent memories to shared memory."""
    agents = list_agents(workspace)
    
    if not agents:
        return {"agents": 0, "total_added": 0, "total_conflicts": 0}
    
    total_added = 0
    total_conflicts = 0
    
    for agent_id in agents:
        result = sync_agent_to_shared(workspace, agent_id, dry_run=dry_run)
        total_added += result.get("added", 0)
        total_conflicts += result.get("conflicts", 0)
    
    return {
        "agents": len(agents),
        "total_added": total_added,
        "total_conflicts": total_conflicts,
    }
