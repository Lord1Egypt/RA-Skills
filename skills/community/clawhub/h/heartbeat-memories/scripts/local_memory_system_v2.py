#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Local Memory System v2
Lightweight semantic search system for Heartbeat-Memories
"""

import os
import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings

class LocalMemorySystem:
    """Local memory system using ChromaDB"""
    
    def __init__(self, memory_path: str = "memory"):
        """
        Initialize the memory system
        
        Args:
            memory_path: Path to memory directory (relative to skill root)
        """
        self.memory_path = Path(memory_path)
        self.vector_db_path = self.memory_path / "vector_db"
        self.config_path = Path("config") / "hbm_config.json"
        
        # Load configuration
        self.config = self.load_config()
        
        # Initialize ChromaDB client
        self.chroma_client = None
        self.collection = None
        
        print(f"🧠 Local Memory System v2")
        print(f"📁 Memory path: {self.memory_path}")
        print(f"📁 Vector DB: {self.vector_db_path}")
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Default configuration
            return {
                "semantic_search": {
                    "enabled": True,
                    "model_name": "all-MiniLM-L6-v2",
                    "max_results": 5,
                    "similarity_threshold": 0.7
                }
            }
    
    def initialize_database(self):
        """Initialize ChromaDB database"""
        if not self.config.get("semantic_search", {}).get("enabled", True):
            print("⚠️ Semantic search disabled in config")
            return False
        
        try:
            # Create persistent ChromaDB client
            self.chroma_client = chromadb.PersistentClient(
                path=str(self.vector_db_path),
                settings=Settings(anonymized_telemetry=False)
            )
            
            # Get or create collection
            collection_name = "hbm_memories"
            try:
                self.collection = self.chroma_client.get_collection(collection_name)
                print(f"✅ Loaded existing collection: {collection_name}")
            except:
                self.collection = self.chroma_client.create_collection(collection_name)
                print(f"✅ Created new collection: {collection_name}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize ChromaDB: {e}")
            return False
    
    def add_memory(self, content: str, metadata: Dict[str, Any], id: Optional[str] = None):
        """Add a memory to the vector database"""
        if not self.collection:
            if not self.initialize_database():
                return False
        
        try:
            if id is None:
                id = f"memory_{int(time.time())}_{hash(content) % 10000}"
            
            self.collection.add(
                documents=[content],
                metadatas=[metadata],
                ids=[id]
            )
            
            print(f"✅ Added memory: {id}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to add memory: {e}")
            return False
    
    def search_memories(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search memories by semantic similarity"""
        if not self.collection:
            if not self.initialize_database():
                return []
        
        try:
            results = self.collection.query(
                query_texts=[query],
                n_results=limit
            )
            
            # Format results
            formatted_results = []
            if results['documents']:
                for i in range(len(results['documents'][0])):
                    formatted_results.append({
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i] if results['metadatas'] else {},
                        'distance': results['distances'][0][i] if results['distances'] else 0.0,
                        'id': results['ids'][0][i] if results['ids'] else f"result_{i}"
                    })
            
            print(f"🔍 Found {len(formatted_results)} results for query: {query[:50]}...")
            return formatted_results
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []
    
    def list_collections(self):
        """List all collections in the database"""
        if not self.chroma_client:
            if not self.initialize_database():
                return []
        
        try:
            collections = self.chroma_client.list_collections()
            return [col.name for col in collections]
        except Exception as e:
            print(f"❌ Failed to list collections: {e}")
            return []
    
    def get_stats(self):
        """Get database statistics"""
        if not self.collection:
            if not self.initialize_database():
                return {"status": "not_initialized"}
        
        try:
            count = self.collection.count()
            return {
                "status": "active",
                "collection_count": count,
                "vector_db_path": str(self.vector_db_path),
                "config": self.config.get("semantic_search", {})
            }
        except Exception as e:
            return {"status": f"error: {str(e)}"}

def main():
    """Command-line interface"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Local Memory System v2")
    parser.add_argument("--init", action="store_true", help="Initialize database")
    parser.add_argument("--search", help="Search query")
    parser.add_argument("--add", help="Add memory content")
    parser.add_argument("--stats", action="store_true", help="Show statistics")
    parser.add_argument("--list", action="store_true", help="List collections")
    
    args = parser.parse_args()
    
    memory_system = LocalMemorySystem()
    
    if args.init:
        print("🚀 Initializing database...")
        success = memory_system.initialize_database()
        print("✅ Initialization successful" if success else "❌ Initialization failed")
    
    elif args.search:
        print(f"🔍 Searching for: {args.search}")
        results = memory_system.search_memories(args.search)
        for i, result in enumerate(results, 1):
            print(f"\n[{i}] {result['content'][:100]}...")
            print(f"   Distance: {result['distance']:.4f}")
            if result['metadata']:
                print(f"   Metadata: {result['metadata']}")
    
    elif args.add:
        print(f"➕ Adding memory: {args.add[:50]}...")
        metadata = {
            "type": "manual_add",
            "timestamp": time.time(),
            "source": "cli"
        }
        success = memory_system.add_memory(args.add, metadata)
        print("✅ Added successfully" if success else "❌ Failed to add")
    
    elif args.stats:
        stats = memory_system.get_stats()
        print("📊 Database Statistics:")
        for key, value in stats.items():
            print(f"  {key}: {value}")
    
    elif args.list:
        collections = memory_system.list_collections()
        print("📁 Collections:")
        for col in collections:
            print(f"  • {col}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()