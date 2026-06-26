#!/usr/bin/env python3
"""
Ézekiel Memory System — L4 Qdrant Integration
Gère les vecteurs sémantiques pour similarité (PAS les faits)
"""

import requests
import json
from datetime import datetime
from pathlib import Path

QDRANT_URL = "http://localhost:6333"

COLLECTIONS = {
    "pkm_memory": "Mémoire principale — faits générales",
    "vault_brain": "Connaissances crystallisées — leçons apprises",
    "stc_feedback": "Feedback émotionnel STC — état d'esprit",
    "merlin_knowledge": "Savoir de Merlin — connaissances distantes"
}

def get_collection_points(collection: str, limit: int = 10):
    """Récupère les points d'une collection"""
    url = f"{QDRANT_URL}/collections/{collection}/points"
    params = {"limit": limit}
    
    try:
        response = requests.get(url, params=params)
        if response.status_code == 200:
            return response.json().get("result", {}).get("points", [])
        return []
    except Exception as e:
        return {"error": str(e)}

def search_similar(collection: str, query: str, limit: int = 5):
    """Recherche sémantique dans une collection"""
    # Note: Sans modèle d'embedding local, on utilise une approcherudimentaire
    # Pour full embedding, utiliser openclaw memory ou Ollama
    url = f"{QDRANT_URL}/collections/{collection}/points/search"
    
    payload = {
        "query": query,
        "limit": limit
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            return response.json().get("result", [])
        return []
    except Exception as e:
        return {"error": str(e)}

def list_collections():
    """Liste les collections disponibles"""
    try:
        response = requests.get(f"{QDRANT_URL}/collections")
        if response.status_code == 200:
            data = response.json()
            return data.get("result", {}).get("collections", [])
        return []
    except Exception as e:
        return {"error": str(e)}

def get_collection_info(collection: str):
    """Info détaillée sur une collection"""
    try:
        response = requests.get(f"{QDRANT_URL}/collections/{collection}")
        if response.status_code == 200:
            return response.json().get("result", {})
        return {}
    except Exception as e:
        return {"error": str(e)}

def index_fact(collection: str, content: str, tags: list = None, metadata: dict = None):
    """Index un fait dans une collection (utilise openclaw memory pour l'embedding)"""
    # Note: L'embedding réel nécessite un modèle
    # Ce script prépare le payload pour plus tard
    payload = {
        "content": content,
        "tags": tags or [],
        "metadata": metadata or {},
        "indexed_at": datetime.utcnow().isoformat(),
        "agent": "ezekiel"
    }
    
    print(f"[L4 Qdrant] Prepared payload for {collection}:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    
    return payload

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        cmd = sys.argv[1]
        
        if cmd == "list":
            collections = list_collections()
            print(f"Collections disponibles ({len(collections)}):")
            for c in collections:
                print(f"  - {c['name']}")
        
        elif cmd == "info" and len(sys.argv) > 2:
            collection = sys.argv[2]
            info = get_collection_info(collection)
            print(json.dumps(info, indent=2, ensure_ascii=False))
        
        elif cmd == "search" and len(sys.argv) > 3:
            collection = sys.argv[2]
            query = sys.argv[3]
            results = search_similar(collection, query)
            print(f"Résultats pour '{query}' dans {collection}:")
            print(json.dumps(results, indent=2, ensure_ascii=False))
        
        elif cmd == "index" and len(sys.argv) > 3:
            collection = sys.argv[2]
            content = sys.argv[3]
            tags = sys.argv[4:] if len(sys.argv) > 4 else []
            result = index_fact(collection, content, tags)
            print("Payload indexé:")
            print(json.dumps(result, indent=2))
        
        else:
            print("Usage: python3 ezekiel_qdrant.py list")
            print("       python3 ezekiel_qdrant.py info <collection>")
            print("       python3 ezekiel_qdrant.py search <collection> <query>")
            print("       python3 ezekiel_qdrant.py index <collection> <content> [tags...]")
    else:
        # Test: lister les collections
        print("=== Ézekiel Qdrant L4 Integration ===")
        collections = list_collections()
        print(f"\nCollections actives: {len(collections)}")
        for c in collections:
            info = get_collection_info(c['name'])
            vectors = info.get("vectors", {})
            print(f"  {c['name']}: {vectors.get('points', 'N/A')} points")