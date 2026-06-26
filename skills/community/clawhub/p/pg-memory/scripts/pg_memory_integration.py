#!/usr/bin/env python3
"""
OpenClaw PostgreSQL Memory Integration
Patches pre-compaction and post-compaction to use PostgreSQL
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

# Add pg-memory to path - works regardless of install location
PG_MEMORY_PATH = str(Path(__file__).parent)
sys.path.insert(0, PG_MEMORY_PATH)

def get_session_context():
    """Extract current session context from OpenClaw environment"""
    # This would be populated by OpenClaw runtime
    # For now, we construct from available context
    
    context = {
        'session_key': os.environ.get('OPENCLAW_SESSION_ID', 'unknown'),
        'agent_id': 'arty',
        'provider': os.environ.get('OPENCLAW_PROVIDER', 'unknown'),
        'channel_id': os.environ.get('OPENCLAW_CHANNEL_ID'),
        'user_id': os.environ.get('OPENCLAW_USER_ID'),
        'user_label': os.environ.get('OPENCLAW_USER_LABEL', 'unknown'),
        'group_name': os.environ.get('OPENCLAW_GROUP_NAME'),
        'started_at': datetime.now().isoformat(),
    }
    
    return context

def pre_compaction_save(exchanges, observations):
    """
    Call this BEFORE OpenClaw context reset.
    
    Args:
        exchanges: List of exchange dicts with user_message, assistant_response, tool_calls
        observations: List of observation dicts with type, title, content, importance, tags
    
    Returns:
        bool: True if saved successfully
    """
    try:
        from pg_memory_v2 import AgentMemory
        
        # Get session context
        ctx = get_session_context()
        session_key = ctx.get('session_key', 'unknown')
        
        # Initialize memory
        mem = AgentMemory()
        
        # Ensure session exists
        mem.start_session(
            session_key=session_key,
            provider=ctx.get('provider'),
            channel_id=ctx.get('channel_id'),
            user_id=ctx.get('user_id'),
            user_label=ctx.get('user_label'),
            group_name=ctx.get('group_name'),
            summary=f"Session {session_key[:8]}..."
        )
        
        # Save exchanges
        for i, ex in enumerate(exchanges):
            mem.save_exchange(
                session_key=session_key,
                exchange_number=i + 1,
                user_message=ex.get('user_message', ''),
                assistant_response=ex.get('assistant_response', ''),
                assistant_thinking=ex.get('thinking', ''),
                tool_calls=ex.get('tool_calls', []),
                context_tokens=ex.get('context_tokens'),
                model_version=ex.get('model_version', 'unknown'),
                user_metadata=ex.get('metadata', {})
            )
        
        # Save observations
        for obs in observations:
            mem.capture_observation(
                session_key=session_key,
                obs_type=obs.get('type', 'note'),
                title=obs.get('title', 'Observation'),
                content=obs.get('content', ''),
                importance=obs.get('importance', 0.5),
                tags=obs.get('tags', []),
                related_files=obs.get('related_files', []),
                related_urls=obs.get('related_urls', []),
                user_requested=obs.get('user_requested', False),
                derived_from_exchanges=obs.get('derived_from', [])
            )
        
        # Mark session as ended for compaction
        mem.end_session(session_key)
        
        # Prune old markdown files
        pruned = mem.prune_old_markdown()
        if pruned > 0:
            print(f"   Pruned {pruned} old markdown files")
        
        mem.close()
        
        # Write compaction marker (for post-compaction verification)
        marker_path = '/tmp/last_compaction_marker.json'
        with open(marker_path, 'w') as f:
            json.dump({
                'session_key': session_key,
                'timestamp': datetime.now().isoformat(),
                'exchanges_saved': len(exchanges),
                'observations_saved': len(observations),
                'source': 'postgresql'
            }, f, indent=2)
        
        return True
        
    except Exception as e:
        print(f"⚠️  PostgreSQL save failed: {e}")
        print("   Falling back to markdown-only...")
        return _fallback_markdown_save(exchanges, observations)

def _fallback_markdown_save(exchanges, observations):
    """Emergency fallback when PostgreSQL is down"""
    try:
        import yaml
        
        config_path = os.path.expanduser('~/.openclaw/workspace/config/memory.yaml')
        if os.path.exists(config_path):
            with open(config_path) as f:
                config = yaml.safe_load(f)
            markdown_dir = config.get('memory', {}).get('markdown_dir', '~/.openclaw/workspace/memory')
        else:
            markdown_dir = '~/.openclaw/workspace/memory'
        
        markdown_dir = os.path.expanduser(markdown_dir)
        os.makedirs(markdown_dir, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        filepath = os.path.join(markdown_dir, f"{date_str}_emergency.md")
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"\n## EMERGENCY BACKUP ({datetime.now().strftime('%H:%M:%S')})\n\n")
            f.write(f"**Status**: PostgreSQL unavailable\n\n")
            
            for obs in observations:
                f.write(f"### {obs.get('title', 'Observation')}\n\n")
                f.write(f"Type: {obs.get('type', 'note')}\n")
                f.write(f"Importance: {obs.get('importance', 0.5)}\n\n")
                f.write(f"{obs.get('content', '')}\n\n")
                if obs.get('tags'):
                    f.write(f"Tags: {', '.join(obs['tags'])}\n\n")
                f.write("---\n\n")
        
        print("   ✅ Fallback save to markdown successful")
        return True
        
    except Exception as e2:
        print(f"   ❌ Fallback save also failed: {e2}")
        return False

def post_compaction_restore(session_key=None, hours=24):
    """
    Call this AFTER OpenClaw context reset.
    Restores context from PostgreSQL.
    
    Args:
        session_key: Specific session to restore (optional)
        hours: How far back to look for context
    
    Returns:
        dict: Restored context with recent observations
    """
    try:
        from pg_memory_v2 import AgentMemory
        
        mem = AgentMemory()
        
        result = {
            'session_key': session_key or 'new_session',
            'recent_observations': [],
            'recent_exchanges': [],
            'high_importance': [],
            'status': 'ok'
        }
        
        # Get high-importance recent observations
        observations = mem.get_recent_observations(
            hours=hours,
            min_importance=0.6
        )
        result['recent_observations'] = observations[:10]  # Top 10
        
        # Get high-importance only (critical context)
        high_imp = [o for o in observations if o.get('importance_score', 0) > 0.8]
        result['high_importance'] = high_imp[:5]
        
        # If specific session requested
        if session_key:
            exchanges = mem.search_exchanges('', days=1, limit=20)
            # Filter to specific session
            result['recent_exchanges'] = [
                ex for ex in exchanges 
                if ex.get('session_id') == session_key
            ]
        
        # Get stats
        result['stats'] = mem.stats()
        
        mem.close()
        
        return result
        
    except Exception as e:
        print(f"⚠️  PostgreSQL restore failed: {e}")
        return {
            'session_key': session_key or 'new_session',
            'recent_observations': [],
            'recent_exchanges': [],
            'high_importance': [],
            'status': 'fallback',
            'error': str(e),
            'message': 'Started new session with no prior context'
        }

def proactive_search(query, days=7, min_importance=0.3):
    """
    Proactive search during conversation.
    Call this when user asks about past work.
    
    Args:
        query: Search string
        days: How far back to search
        min_importance: Minimum importance threshold
    
    Returns:
        list: Matching observations
    """
    try:
        from pg_memory_v2 import AgentMemory
        
        mem = AgentMemory()
        
        # Search observations
        results = mem.search(query, days=days, min_importance=min_importance)
        
        # If few results, also search raw exchanges
        if len(results) < 3:
            exchanges = mem.search_exchanges(query, days=days, limit=5)
            # Add to results (marking as "from_exchange")
            for ex in exchanges:
                results.append({
                    'id': ex.get('id'),
                    'obs_type': 'exchange_context',
                    'title': f"Exchange #{ex.get('exchange_number')}",
                    'content': f"User: {ex.get('user_message', '')[:100]}... Assistant: {ex.get('assistant_response', '')[:100]}...",
                    'importance_score': 0.4,  # Lower than curated observations
                    'created_at': ex.get('created_at'),
                    'source': 'raw_exchange'
                })
        
        mem.close()
        return results
        
    except Exception as e:
        print(f"Search failed: {e}")
        return []

# ========================================================================
# OPENCLAW INTEGRATION POINTS
# ========================================================================

if __name__ == '__main__':
    """
    Can be called directly by OpenClaw:
    
    # Pre-compaction:
    python3 pg_memory_integration.py pre-compact context.json
    
    # Post-compaction:
    python3 pg_memory_integration.py post-compact [session_key]
    
    # Search:
    python3 pg_memory_integration.py search "query"
    """
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  pre-compact <context.json>")
        print("  post-compact [session_key]")
        print("  search \"query\" [days]")
        print("  test")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == 'pre-compact':
        if len(sys.argv) < 3:
            print("Usage: pre-compact <context.json>")
            sys.exit(1)
        
        with open(sys.argv[2]) as f:
            data = json.load(f)
        
        success = pre_compaction_save(
            exchanges=data.get('exchanges', []),
            observations=data.get('observations', [])
        )
        sys.exit(0 if success else 1)
    
    elif cmd == 'post-compact':
        session_key = sys.argv[2] if len(sys.argv) > 2 else None
        result = post_compaction_restore(session_key)
        print(json.dumps(result, indent=2, default=str))
        sys.exit(0)
    
    elif cmd == 'search':
        query = sys.argv[2] if len(sys.argv) > 2 else ''
        days = int(sys.argv[3]) if len(sys.argv) > 3 else 7
        results = proactive_search(query, days=days)
        print(json.dumps(results, indent=2, default=str))
        sys.exit(0)
    
    elif cmd == 'test':
        # Run integration test
        print("🧪 Testing PostgreSQL Integration")
        print("=" * 40)
        
        # Test pre-compaction
        test_exchanges = [
            {
                'user_message': 'What is the memory system?',
                'assistant_response': 'PostgreSQL-based Agent Memory v2.0',
                'tool_calls': []
            }
        ]
        test_observations = [
            {
                'type': 'milestone',
                'title': 'Integration test',
                'content': 'Testing pre-compaction save',
                'importance': 0.9,
                'tags': ['test', 'integration']
            }
        ]
        
        success = pre_compaction_save(test_exchanges, test_observations)
        print(f"1. Pre-compaction: {'✅' if success else '❌'}")
        
        # Test proactive search
        results = proactive_search("integration", days=7)
        print(f"2. Search: {'✅' if results else '❌'} ({len(results)} results)")
        
        # Test post-compaction
        restored = post_compaction_restore(hours=1)
        print(f"3. Post-compaction: {'✅' if restored.get('status') == 'ok' else '❌'}")
        print(f"   Observations: {len(restored.get('recent_observations', []))}")
        
        print("\n🎉 Integration test complete!")

    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)
