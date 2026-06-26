#!/usr/bin/env python3
"""
Ézekiel Memory System — L6 GNN Pattern Detector
Détecte les clusters de nœuds froids qui se RAPPROCHENT
Simule un "Graph Neural Network" léger pour anticipation
"""

import json
from datetime import datetime, timezone
from pathlib import Path
from collections import defaultdict

NEBULA_FILE = Path.home() / ".openclaw" / "nebula" / "nebula.json"

def load_nebula():
    if NEBULA_FILE.exists():
        with open(NEBULA_FILE, "r") as f:
            return json.load(f)
    return {"clusters": {}, "nodes": {}}

def detect_approaching_clusters(nebula, threshold: int = 3):
    """
    Détecte les clusters où des nœuds froids se rapprochent
    Simule GNN: "Ces points commencent à se rapprocher"
    
    LOGIQUE:
    - Si cluster a 2+ nœuds froids qui n'ont pas été vus récemment
    - Et qu'ils ont des tags/intents similaires
    - → Le cluster "monte" vers tiède (anticipation)
    
    threshold: nombre minimum de nœuds froids dans un cluster pour alerter
    """
    approaching = []
    
    for cluster_key, cluster_data in nebula.get("clusters", {}).items():
        cold_nodes = []
        for node_key in cluster_data.get("nodes", []):
            node = nebula["nodes"].get(node_key, {})
            if node.get("status") == "froid":
                cold_nodes.append(node_key)
        
        if len(cold_nodes) >= threshold:
            # Calculer la "distance" moyenne entre nœuds froids
            # Simulé: si même intent prefix = proximité
            intents = set()
            for node_key in cold_nodes:
                node = nebula["nodes"].get(node_key, {})
                intent = node.get("intent", "")
                if "_" in intent:
                    intents.add(intent.split("_")[0])
            
            if len(intents) <= 2:  # Mêmes intents = cluster qui approche
                approaching.append({
                    "cluster": cluster_key,
                    "cold_nodes": len(cold_nodes),
                    "intents": list(intents),
                    "gravity": cluster_data.get("gravity", "stable"),
                    "signal": "APPROACHING"
                })
    
    return approaching

def predict_brisants(days_ahead: int = 7):
    """
    Prédit quels clusters vont devenir brillants dans les N jours
    Basé sur: fréquence croissante + cluster en "rising"
    """
    nebula = load_nebula()
    predictions = []
    
    for node_key, node in nebula.get("nodes", {}).items():
        status = node.get("status", "froid")
        frequency = node.get("frequency", 0)
        gravity = nebula["clusters"].get(node.get("intent", "").split("_")[0], {}).get("gravity", "stable")
        
        if status == "tiede" and gravity == "rising" and frequency >= 2:
            # Will likely become brillant soon
            predictions.append({
                "node": node_key,
                "current_status": status,
                "frequency": frequency,
                "gravity": gravity,
                "prediction": "LIKELY_BRILLANT",
                "content": node.get("content", "")[:50]
            })
        elif status == "froid" and frequency >= 2 and gravity == "rising":
            # Could become tiède soon
            predictions.append({
                "node": node_key,
                "current_status": status,
                "frequency": frequency,
                "gravity": gravity,
                "prediction": "POSSIBLE_TIEDE",
                "content": node.get("content", "")[:50]
            })
    
    return predictions

def get_intuition_report():
    """
    Génère un rapport d'intuition complet
    Ce que GNN-lite "sent" sans que l'utilisateur ait demandé
    """
    nebula = load_nebula()
    
    approaching = detect_approaching_clusters(nebula)
    predictions = predict_brisants()
    
    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "approaching_clusters": approaching,
        "predictions": predictions,
        "total_cold_nodes": len([n for n in nebula.get("nodes", {}).values() if n.get("status") == "froid"]),
        "total_tiede_nodes": len([n for n in nebula.get("nodes", {}).values() if n.get("status") == "tiede"]),
        "total_brillant_nodes": len([n for n in nebula.get("nodes", {}).values() if n.get("status") == "brillant"])
    }

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        if sys.argv[1] == "approaching":
            nebula = load_nebula()
            result = detect_approaching_clusters(nebula)
            print(json.dumps(result, indent=2, ensure_ascii=False))
        
        elif sys.argv[1] == "predict":
            predictions = predict_brisants()
            print(json.dumps(predictions, indent=2, ensure_ascii=False))
        
        elif sys.argv[1] == "intuition":
            report = get_intuition_report()
            print(json.dumps(report, indent=2, ensure_ascii=False))
        
        else:
            print("Usage: python3 ezekiel_gnn.py approaching")
            print("       python3 ezekiel_gnn.py predict")
            print("       python3 ezekiel_gnn.py intuition")
    else:
        # Default: intuition report
        report = get_intuition_report()
        print(f"=== GNN Intuition Report ===")
        print(f"Cold: {report['total_cold_nodes']} | Tiede: {report['total_tiede_nodes']} | Brillant: {report['total_brillant_nodes']}")
        
        if report['approaching_clusters']:
            print(f"\n📡 Approaching clusters: {len(report['approaching_clusters'])}")
            for c in report['approaching_clusters']:
                print(f"  → {c['cluster']}: {c['cold_nodes']} cold nodes")
        
        if report['predictions']:
            print(f"\n🔮 Predictions: {len(report['predictions'])}")
            for p in report['predictions'][:3]:
                print(f"  → {p['prediction']}: {p['content']}...")