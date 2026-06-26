#!/usr/bin/env python3
"""
Ézekiel Memory System — L6 Nebula Semantic Map
Gère les nœuds de la nébula sémantique (Froid/Tiède/Brillant)
"""

import json
import os
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

NEBULA_DIR = Path.home() / ".openclaw" / "nebula"
NEBULA_DIR.mkdir(parents=True, exist_ok=True)
NEBULA_FILE = NEBULA_DIR / "nebula.json"

GRAVITY_DECAY_DAYS = 180  # 6 mois = nœud s'enfonce

def load_nebula():
    """Charge la nébula depuis le fichier"""
    if NEBULA_FILE.exists():
        with open(NEBULA_FILE, "r") as f:
            return json.load(f)
    return {"clusters": {}, "nodes": {}}

def save_nebula(nebula):
    """Sauvegarde la nébula"""
    with open(NEBULA_FILE, "w") as f:
        json.dump(nebula, f, indent=2, ensure_ascii=False)

def now_iso():
    """Retourne l'heure UTC en ISO string"""
    return datetime.now(timezone.utc).isoformat()

def add_node(intent: str, content: str, tags: list = None):
    """Ajoute ou met à jour un nœud dans la nébula"""
    nebula = load_nebula()
    
    # Créer clé unique basée sur intent + contenu réduit
    node_key = f"{intent}_{content[:50]}"
    
    if node_key not in nebula["nodes"]:
        nebula["nodes"][node_key] = {
            "intent": intent,
            "content": content,
            "tags": tags or [],
            "frequency": 0,
            "first_seen": now_iso(),
            "last_seen": now_iso(),
            "status": "froid"  # ❄️
        }
    
    # Incrémenter fréquence
    nebula["nodes"][node_key]["frequency"] += 1
    nebula["nodes"][node_key]["last_seen"] = now_iso()
    
    # Mettre à jour statut selon fréquence
    freq = nebula["nodes"][node_key]["frequency"]
    if freq >= 3:
        nebula["nodes"][node_key]["status"] = "brillant"  # 💎
    elif freq == 2:
        nebula["nodes"][node_key]["status"] = "tiede"     # 🔥
    else:
        nebula["nodes"][node_key]["status"] = "froid"     # ❄️
    
    # Ajouter au cluster approprié (basé sur tags ou intent)
    cluster_key = intent.split("_")[0] if "_" in intent else "general"
    if cluster_key not in nebula["clusters"]:
        nebula["clusters"][cluster_key] = {"nodes": [], "gravity": "stable"}
    
    if node_key not in nebula["clusters"][cluster_key]["nodes"]:
        nebula["clusters"][cluster_key]["nodes"].append(node_key)
        nebula["clusters"][cluster_key]["gravity"] = "rising"
    
    save_nebula(nebula)
    
    return nebula["nodes"][node_key]

def get_cluster_status(cluster_key: str = None):
    """Retourne le statut d'un cluster ou de toute la nébula"""
    nebula = load_nebula()
    
    if cluster_key:
        return nebula["clusters"].get(cluster_key, {})
    
    # Retourner tous les nœuds brillants (pour cristallisation L5)
    brillants = {k: v for k, v in nebula["nodes"].items() if v["status"] == "brillant"}
    
    return {
        "total_nodes": len(nebula["nodes"]),
        "clusters": len(nebula["clusters"]),
        "brillants": brillants,
        "tiedes": {k: v for k, v in nebula["nodes"].items() if v["status"] == "tiede"},
        "froids": {k: v for k, v in nebula["nodes"].items() if v["status"] == "froid"}
    }

def apply_gravity_decay():
    """Applique la gravité sémantique (nœuds s'enfoncent après 6 mois)"""
    nebula = load_nebula()
    now = datetime.now(timezone.utc)
    
    for node_key, node in nebula["nodes"].items():
        last_seen = datetime.fromisoformat(node["last_seen"])
        # Handle timezone-aware vs naive datetime
        if last_seen.tzinfo is None:
            last_seen = last_seen.replace(tzinfo=timezone.utc)
        days_since = (now - last_seen).days
        
        if days_since > GRAVITY_DECAY_DAYS and node["status"] != "froid":
            node["status"] = "froid"
            node["gravity"] = "sinking"
    
    save_nebula(nebula)

def get_brillant_nodes():
    """Retourne les nœuds brillants prêts pour cristallisation L5"""
    nebula = load_nebula()
    return {k: v for k, v in nebula["nodes"].items() if v["status"] == "brillant"}

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "add" and len(sys.argv) > 3:
            intent = sys.argv[2]
            content = sys.argv[3]
            tags = sys.argv[4:] if len(sys.argv) > 4 else []
            result = add_node(intent, content, tags)
            print(f"Node updated: {result['status']} (freq: {result['frequency']})")
        
        elif sys.argv[1] == "status":
            cluster = sys.argv[2] if len(sys.argv) > 2 else None
            result = get_cluster_status(cluster)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif sys.argv[1] == "decay":
            apply_gravity_decay()
            print("Gravity decay applied")
        
        elif sys.argv[1] == "brillants":
            nodes = get_brillant_nodes()
            print(json.dumps(nodes, indent=2, ensure_ascii=False))
        
        else:
            print("Usage: python3 ezekiel_nebula.py add <intent> <content> [tags...]")
            print("       python3 ezekiel_nebula.py status [cluster]")
            print("       python3 ezekiel_nebula.py decay")
            print("       python3 ezekiel_nebula.py brillants")
    else:
        # Test: add a node
        result = add_node("test_session", "Test interaction for nebula", ["test"])
        print(f"Test node: {result['status']}")