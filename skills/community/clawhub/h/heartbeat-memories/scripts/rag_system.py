#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RAG System for Heartbeat-Memories
Retrieval Augmented Generation system with configurable switches
"""

import json
import time
from pathlib import Path
from typing import List, Dict, Any, Optional
from .local_memory_system_v2 import LocalMemorySystem

class RAGSystem:
    """RAG system with switch controls"""
    
    def __init__(self, config_path: str = "config/hbm_config.json"):
        """
        Initialize RAG system
        
        Args:
            config_path: Path to configuration file
        """
        self.config_path = Path(config_path)
        self.config = self.load_config()
        self.memory_system = None
        self.cache = {}
        
        print(f"🧠 RAG System Initialized")
        print(f"⚙️  Configuration: {self.config_path}")
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Default configuration with all switches OFF
            return {
                "rag_system": {
                    "enabled": False,
                    "enable_limit_and_dedupe": False,
                    "enable_cache": False,
                    "enable_log_compression": True,
                    "max_tokens": 1000,
                    "cache_ttl_seconds": 3600
                }
            }
    
    def get_rag_config(self) -> Dict[str, Any]:
        """Get RAG-specific configuration"""
        return self.config.get("rag_system", {})
    
    def is_enabled(self) -> bool:
        """Check if RAG system is enabled"""
        return self.get_rag_config().get("enabled", False)
    
    def initialize_memory_system(self):
        """Initialize memory system if needed"""
        if self.memory_system is None:
            self.memory_system = LocalMemorySystem()
            if not self.memory_system.initialize_database():
                print("⚠️ Memory system initialization failed")
                return False
        return True
    
    def retrieve(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve relevant memories for a query
        
        Args:
            query: Search query
            limit: Maximum number of results
        
        Returns:
            List of relevant memory items
        """
        # Check if RAG is enabled
        if not self.is_enabled():
            print("⚠️ RAG system is disabled (check config: rag_system.enabled)")
            return []
        
        # Check cache if enabled
        if self.get_rag_config().get("enable_cache", False):
            cache_key = f"retrieve:{query}:{limit}"
            if cache_key in self.cache:
                cache_entry = self.cache[cache_key]
                if time.time() - cache_entry['timestamp'] < self.get_rag_config().get("cache_ttl_seconds", 3600):
                    print(f"📦 Using cached results for: {query[:50]}...")
                    return cache_entry['data']
        
        # Initialize memory system
        if not self.initialize_memory_system():
            return []
        
        # Perform retrieval
        raw_results = self.memory_system.search_memories(query, limit * 2)  # Get more for processing
        
        # Process results based on configuration
        processed_results = self.process_results(raw_results, query)
        
        # Limit results if configured
        if self.get_rag_config().get("enable_limit_and_dedupe", False):
            final_results = self.limit_results(processed_results)
        else:
            final_results = processed_results[:limit]
        
        # Cache results if enabled
        if self.get_rag_config().get("enable_cache", False):
            cache_key = f"retrieve:{query}:{limit}"
            self.cache[cache_key] = {
                'data': final_results,
                'timestamp': time.time()
            }
        
        return final_results
    
    def process_results(self, results: List[Dict[str, Any]], query: str) -> List[Dict[str, Any]]:
        """
        Process retrieval results
        
        Args:
            results: Raw retrieval results
            query: Original query for context
        
        Returns:
            Processed results
        """
        processed = []
        
        for result in results:
            processed_result = {
                'content': result['content'],
                'metadata': result['metadata'],
                'distance': result['distance'],
                'id': result['id'],
                'relevance_score': self.calculate_relevance(result, query),
                'timestamp': result['metadata'].get('timestamp', time.time()) if result['metadata'] else time.time()
            }
            processed.append(processed_result)
        
        # Sort by relevance score (descending)
        processed.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return processed
    
    def calculate_relevance(self, result: Dict[str, Any], query: str) -> float:
        """
        Calculate relevance score for a result
        
        Args:
            result: Memory result
            query: Search query
        
        Returns:
            Relevance score (0.0 to 1.0)
        """
        # Base score from vector distance (invert distance)
        base_score = 1.0 - min(result.get('distance', 1.0), 1.0)
        
        # Boost for recent memories
        metadata = result.get('metadata', {})
        if 'timestamp' in metadata:
            age_days = (time.time() - metadata['timestamp']) / (24 * 3600)
            recency_boost = max(0.0, 1.0 - (age_days / 30))  # Linear decay over 30 days
            base_score *= (0.7 + 0.3 * recency_boost)
        
        return min(max(base_score, 0.0), 1.0)
    
    def limit_results(self, results: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Apply token limit and deduplication
        
        Args:
            results: Processed results
        
        Returns:
            Limited results
        """
        if not self.get_rag_config().get("enable_limit_and_dedupe", False):
            return results
        
        max_tokens = self.get_rag_config().get("max_tokens", 1000)
        
        # Simple deduplication by content hash
        seen_content = set()
        deduped_results = []
        
        for result in results:
            content_hash = hash(result['content']) % 1000000
            if content_hash not in seen_content:
                seen_content.add(content_hash)
                deduped_results.append(result)
        
        # Estimate tokens and limit
        estimated_tokens = 0
        limited_results = []
        
        for result in deduped_results:
            # Rough token estimation (4 chars per token)
            result_tokens = len(result['content']) // 4
            
            if estimated_tokens + result_tokens <= max_tokens:
                limited_results.append(result)
                estimated_tokens += result_tokens
            else:
                # Try to truncate if it's the first result
                if not limited_results:
                    truncated_content = result['content'][:max_tokens * 4]
                    limited_results.append({
                        **result,
                        'content': truncated_content + "... [truncated]",
                        'truncated': True
                    })
                break
        
        print(f"📏 Limited {len(results)} → {len(limited_results)} results, estimated tokens: {estimated_tokens}")
        return limited_results
    
    def format_context(self, results: List[Dict[str, Any]], query: str) -> str:
        """
        Format retrieval results as context for LLM
        
        Args:
            results: Retrieved memories
            query: Original query
        
        Returns:
            Formatted context string
        """
        if not results:
            return "No relevant memories found."
        
        context_parts = []
        context_parts.append(f"# Retrieved Memories for: {query}")
        context_parts.append("")
        
        for i, result in enumerate(results, 1):
            metadata = result.get('metadata', {})
            source = metadata.get('source', 'unknown')
            timestamp = metadata.get('timestamp', time.time())
            time_str = time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp))
            
            context_parts.append(f"## Memory {i}: {source} ({time_str})")
            context_parts.append(f"Relevance: {result.get('relevance_score', 0.0):.2f}")
            context_parts.append("")
            context_parts.append(result['content'])
            context_parts.append("")
        
        context_parts.append("---")
        context_parts.append(f"Total memories: {len(results)}")
        
        return "\n".join(context_parts)
    
    def clear_cache(self):
        """Clear the results cache"""
        self.cache.clear()
        print("🧹 Cache cleared")

def main():
    """Command-line interface for RAG system"""
    import argparse
    
    parser = argparse.ArgumentParser(description="RAG System CLI")
    parser.add_argument("--query", help="Search query")
    parser.add_argument("--limit", type=int, default=5, help="Maximum results")
    parser.add_argument("--format", action="store_true", help="Format results as context")
    parser.add_argument("--clear-cache", action="store_true", help="Clear cache")
    parser.add_argument("--config", help="Custom config file path")
    
    args = parser.parse_args()
    
    rag_system = RAGSystem(args.config if args.config else "config/hbm_config.json")
    
    if args.clear_cache:
        rag_system.clear_cache()
    
    elif args.query:
        print(f"🔍 Query: {args.query}")
        print(f"📏 Limit: {args.limit}")
        print(f"⚙️  RAG Enabled: {rag_system.is_enabled()}")
        print("=" * 50)
        
        results = rag_system.retrieve(args.query, args.limit)
        
        if not results:
            print("❌ No results found or RAG disabled")
            return
        
        if args.format:
            context = rag_system.format_context(results, args.query)
            print("\n📄 Formatted Context:")
            print("=" * 50)
            print(context)
        else:
            print(f"\n📊 Found {len(results)} results:")
            for i, result in enumerate(results, 1):
                print(f"\n[{i}] {result['content'][:100]}...")
                print(f"   Relevance: {result.get('relevance_score', 0.0):.2f}")
                print(f"   Source: {result['metadata'].get('source', 'unknown')}")
                if 'truncated' in result:
                    print(f"   ⚠️ Truncated due to token limit")
    
    else:
        # Show configuration
        rag_config = rag_system.get_rag_config()
        print("⚙️ RAG System Configuration:")
        for key, value in rag_config.items():
            print(f"  {key}: {value}")
        
        print("\n🔧 Commands:")
        print("  --query 'your question'       Search memories")
        print("  --query 'question' --format   Format as LLM context")
        print("  --clear-cache                 Clear cache")
        print("  --config path.json            Use custom config")

if __name__ == "__main__":
    main()