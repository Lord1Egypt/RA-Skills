#!/usr/bin/env python3
"""
save_memory.py - Updated for MARRS dedicated collection
"""
import json
import requests
from datetime import datetime
from config import RAG_URL, DEFAULT_COLLECTION

def save_memory(content, collection=None, source="agent"):
    """Save content to your configured RAG system."""
    if collection is None:
        collection = DEFAULT_COLLECTION
    
    print(f"[{datetime.now()}] Saving to collection: {collection} (source: {source})")
    
    payload = {
        "collection": collection,
        "text": str(content),
        "metadata": {
            "source": source,
            "timestamp": datetime.now().isoformat()
        }
    }
    
    try:
        resp = requests.post(f"{RAG_URL}/ingest", json=payload, timeout=30)
        if resp.status_code in (200, 201):
            print(f"  → Successfully saved to {collection}")
            return {"status": "success", "collection": collection}
        else:
            print(f"  → Warning: HTTP {resp.status_code}")
            return {"status": "warning", "code": resp.status_code}
    except Exception as e:
        print(f"  → Error: {e}")
        return {"status": "error", "message": str(e)}


def quick_save(text, agent_name="unknown"):
    """Convenience function."""
    return save_memory(text, source=agent_name)


if __name__ == "__main__":
    print("save_memory helper loaded.")
    print("Edit config.py with your own RAG details before use.")
