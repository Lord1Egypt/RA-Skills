#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Memory Retriever Hook for OpenClaw
Automatically retrieve relevant memories before responding
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'skills'))

from rag_search.src.search import search_memories

def retrieve_context(query: str, k: int = 3, min_similarity: float = 0.7):
    """
    Retrieve relevant memories for a query
    
    Args:
        query: User's message/question
        k: Number of memories to retrieve
        min_similarity: Minimum similarity threshold
    
    Returns:
        Formatted context string for LLM
    """
    try:
        results = search_memories(query, k=k)
        
        if not results:
            return None
        
        # Filter by similarity
        good_results = [r for r in results if r.get('similarity', 0) >= min_similarity]
        
        if not good_results:
            return None
        
        # Format context
        context_parts = []
        for i, r in enumerate(good_results, 1):
            source = r.get('source', 'Unknown')
            content = r.get('content', '')[:500]  # Limit length
            context_parts.append(f"[Memory {i} from {source}]\n{content}")
        
        context = "\n\n".join(context_parts)
        
        return f"""
[Relevant Memories Retrieved]
{context}

[End of Memories]
"""
    
    except Exception as e:
        print(f"[WARN] Memory retrieval failed: {e}")
        return None


def enhance_prompt(user_message: str, conversation_history: list = None, use_smart_trigger: bool = True) -> str:
    """
    Enhance user prompt with retrieved memories
    
    Args:
        user_message: User's current message
        conversation_history: Previous conversation turns (optional)
        use_smart_trigger: Whether to use smart retrieval trigger (default: True)
    
    Returns:
        Enhanced prompt with memory context
    """
    # Smart retrieval trigger
    if use_smart_trigger:
        from smart_retrieval_trigger import should_retrieve
        
        should_retrieve_mem = should_retrieve(user_message)
        
        if not should_retrieve_mem:
            # Skip retrieval, return original message
            return user_message
    
    # Build search query from user message + context
    search_query = user_message
    
    if conversation_history:
        # Add last 2 turns for context
        recent = conversation_history[-2:]
        context = [turn.get('content', '') for turn in recent if turn.get('role') == 'user']
        if context:
            search_query = f"{' '.join(context)} {user_message}"
    
    # Retrieve memories
    memory_context = retrieve_context(search_query, k=3)
    
    if memory_context:
        # Inject memories into prompt
        enhanced = f"""{memory_context}

[User's Current Message]
{user_message}

[Instructions]
Use the retrieved memories above if they are relevant to the user's current message.
If memories are not relevant, respond naturally without referencing them.
"""
        return enhanced
    else:
        # No relevant memories, return original message
        return user_message


# CLI interface for testing
if __name__ == "__main__":
    test_queries = [
        "瀑布",
        "TTS 使用规范",
        "阿里云 Embedding",
        "记忆向量化"
    ]
    
    print("=" * 60)
    print("Memory Retriever Hook Test")
    print("=" * 60)
    
    for query in test_queries:
        print(f"\n{'='*60}")
        print(f"Query: '{query}'")
        print(f"{'='*60}")
        
        enhanced = enhance_prompt(query)
        print(enhanced[:1000])  # Limit output
    
    print("\n" + "=" * 60)
    print("Test Complete!")
    print("=" * 60)
