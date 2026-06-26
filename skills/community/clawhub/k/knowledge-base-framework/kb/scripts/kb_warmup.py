#!/usr/bin/env python3
"""
KB Warmup – Preloads ChromaDB model

Runtime: At server start (via systemd or OpenClaw init)
Purpose: First query should not be 8s slow
"""

import sys
from pathlib import Path
# Add project root to path (portable)
script_dir = Path(__file__).resolve().parent
project_root = script_dir.parent.parent
sys.path.insert(0, str(project_root))

from kb.framework.chroma_integration import get_chroma

def warmup():
    print("Warming up ChromaDB model...")
    chroma = get_chroma()
    
    # Preload model
    _ = chroma.model
    print("Model loaded")
    
    # Get collection reference (initializes ChromaDB internally)
    _ = chroma.sections_collection
    print("ChromaDB Collection ready")
    
    print("KB Warmup complete")

if __name__ == "__main__":
    warmup()
