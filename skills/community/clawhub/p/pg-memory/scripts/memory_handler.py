#!/usr/bin/env python3
"""
OpenClaw Agent Memory Integration
Pre-compaction and Post-compaction handlers

Usage:
    # Pre-compaction (before context reset):
    python3 memory_handler.py pre-compaction
    
    # Post-compaction (after context reset):
    python3 memory_handler.py post-compaction [session_key]
    
    # Get context for a query:
    python3 memory_handler.py retrieve "what port is Rasa on?"
    
Configure with ~/.openclaw/workspace/config/memory.yaml
"""

import sys
import os
import json
import yaml
from datetime import datetime, timedelta
from typing import List, Dict, Optional
from pathlib import Path

# Add to path - works regardless of install location
script_dir = Path(__file__).parent
sys.path.insert(0, str(script_dir))

from pg_memory_v2 import AgentMemory

# Default config path - override with MEMORY_CONFIG_PATH env var
CONFIG_PATH = os.environ.get('MEMORY_CONFIG_PATH', 
                              str(Path.home() / '.openclaw' / 'workspace' / 'config' / 'memory.yaml'))

def load_config() -> Dict:
    """Load memory configuration"""
    defaults = {
        'memory': {
            'primary_backend': 'postgresql',
            'markdown_backup': True,
            'retention_days': 7,
            'agent_id': 'arty',
            'fallback_on_pgdb_down': True
        },
        'postgresql': {
            'host': 'localhost',
            'port': 5432,
            'database': 'openclaw_memory',
            'user': 'postgres'
        }
    }
    
    try:
        if os.path.exists(CONFIG_PATH):
            with open(CONFIG_PATH, 'r') as f:
                config = yaml.safe_load(f)
                # Merge with defaults
                merged = defaults.copy()
                merged.update(config)
                return merged
    except Exception as e:
        print(f"Config load failed: {e}, using defaults")
    
    return defaults

def get_memory() -> AgentMemory:
    """Get configured memory instance"""
    config = load_config()
    
    return AgentMemory(
        host=config['postgresql'].get('host', 'localhost'),
        port=config['postgresql'].get('port', 5432),
        database=config['postgresql'].get('database', 'openclaw_memory'),
        user=config['postgresql'].get('user', 'postgres'),
        password=config['postgresql'].get('password'),
        agent_id=config['memory'].get('agent_id', 'arty'),
        markdown_backup=config['memory'].get('markdown_backup', True),
        retention_days=config['memory'].get('retention_days', 7)
    )

def pre_compaction(context_data: Dict) -> bool:
    """
    Called before OpenClaw context reset.
    Saves current session state to PostgreSQL.
    
    context_data should contain:
    {
        'session_key': 'uuid',
        'exchanges': [{
            'user_message': '...',
            'assistant_response': '...',
            'thinking': '...',
            'tool_calls': [...],
            'timestamp': '...'
        }],
        'observations': [{
            'type': 'decision',
            'title': '...',
            'content': '...',
            'importance': 0.9,
            'tags': [...]
        }],
        'metadata': {
            'provider': 'discord',
            'channel_id': '...',
            'user': {...}
        }
    }
    """
    try:
        mem = get_memory()
        
        session_key = context_data.get('session_key', 'unknown')
        
        # Start session if not exists
        mem.start_session(
            session_key=session_key,
            provider=context_data.get('metadata', {}).get('provider'),
            channel_id=context_data.get('metadata', {}).get('channel_id'),
            user_id=context_data.get('metadata', {}).get('user', {}).get('id'),
            user_label=context_data.get('metadata', {}).get('user', {}).get('label')
        )
        
        # Save all exchanges
        for i, ex in enumerate(context_data.get('exchanges', [])):
            mem.save_exchange(
                session_key=session_key,
                exchange_number=i + 1,
                user_message=ex.get('user_message', ''),
                assistant_response=ex.get('assistant_response', ''),
                assistant_thinking=ex.get('thinking', ''),
                tool_calls=ex.get('tool_calls', []),
                user_metadata=ex.get('metadata', {})
            )
        
        # Save observations
        for obs in context_data.get('observations', []):
            mem.capture_observation(
                session_key=session_key,
                obs_type=obs.get('type', 'note'),
                title=obs.get('title', 'Observation'),
                content=obs.get('content', ''),
                importance=obs.get('importance', 0.5),
                tags=obs.get('tags', [])
            )
        
        # Prune old markdown
        pruned = mem.prune_old_markdown()
        if pruned > 0:
            print(f"   Pruned {pruned} old markdown files")
        
        mem.end_session(session_key)
        mem.close()
        
        print("✅ Pre-compaction: Session saved to PostgreSQL")
        
        # Also write minimal context marker (for post-compaction verification)
        marker_path = '/tmp/last_compaction_marker.json'
        with open(marker_path, 'w') as f:
            json.dump({
                'session_key': session_key,
                'timestamp': datetime.now().isoformat(),
                'agent': context_data.get('metadata', {}).get('user', {}).get('label', 'unknown')
            }, f)
        
        return True
        
    except Exception as e:
        print(f"⚠️  Pre-compaction failed: {e}")
        # Fallback to just markdown write
        return _emergency_markdown_write(context_data)

def _emergency_markdown_write(context_data: Dict) -> bool:
    """Emergency fallback when PostgreSQL is down"""
    try:
        config = load_config()
        markdown_dir = os.path.expanduser(
            config['memory'].get('markdown_dir', '~/.openclaw/workspace/memory')
        )
        
        if not os.path.exists(markdown_dir):
            os.makedirs(markdown_dir, exist_ok=True)
        
        date_str = datetime.now().strftime('%Y-%m-%d')
        filepath = os.path.join(markdown_dir, f"{date_str}.md")
        
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(f"\n## EMERGENCY BACKUP ({datetime.now().strftime('%H:%M:%S')})\n")
            f.write(f"Session: {context_data.get('session_key', 'unknown')}\n\n")
            
            for obs in context_data.get('observations', []):
                f.write(f"### {obs.get('title', 'Observation')}\n")
                f.write(f"{obs.get('content', '')}\n\n")
        
        print("   ✅ Emergency save to markdown successful")
        return True
        
    except Exception as e2:
        print(f"   ❌ Emergency save failed: {e2}")
        return False

def post_compaction(session_key: Optional[str] = None) -> Dict:
    """
    Called after OpenClaw context reset.
    Retrieves context to restore session state.
    
    Returns:
    {
        'session_key': 'uuid',  # Current or recent
        'recent_exchanges': [...],  # Recent conversation for context
        'observations': [...],  # Important things to remember
        'last_session_summary': '...',
        'status': 'ok' | 'fallback'
    }
    """
    try:
        mem = get_memory()
        
        result = {
            'session_key': session_key or 'new_session',
            'recent_exchanges': [],
            'observations': [],
            'last_session_summary': None,
            'status': 'ok'
        }
        
        # If session_key provided, get that session
        if session_key:
            # Get recent exchanges from this session
            exchanges = mem.search_exchanges('', days=1, limit=20)
            # Filter to this session (will need session_id lookup)
            result['recent_exchanges'] = exchanges
        else:
            # Get recent exchanges across all sessions
            exchanges = mem.search_exchanges('', days=1, limit=10)
            result['recent_exchanges'] = exchanges
        
        # Get high-importance recent observations
        obs = mem.get_recent_observations(hours=24, min_importance=0.7)
        result['observations'] = obs[:10]  # Top 10
        
        # Get stats
        result['stats'] = mem.stats()
        
        mem.close()
        
        print(f"✅ Post-compaction: Loaded {len(result['observations'])} observations")
        return result
        
    except Exception as e:
        print(f"⚠️  Post-compaction failed: {e}")
        # Return minimal fallback
        return {
            'session_key': session_key or 'new_session',
            'recent_exchanges': [],
            'observations': [],
            'last_session_summary': None,
            'status': 'fallback',
            'error': str(e)
        }

def retrieve_context(query: str, days: int = 7) -> List[Dict]:
    """
    Proactive context retrieval during conversation.
    Called when user asks about past information.
    """
    try:
        mem = get_memory()
        
        # Search for relevant observations
        results = mem.search(query, days=days, min_importance=0.3)
        
        if not results or len(results) < 3:
            # Also search raw exchanges for full context
            exchanges = mem.search_exchanges(query, days=days, limit=5)
            results.extend(exchanges)
        
        mem.close()
        return results
        
    except Exception as e:
        print(f"Context retrieval failed: {e}")
        return []

def main():
    if len(sys.argv) < 2:
        print("Usage: memory_handler.py [pre-compaction|post-compaction|retrieve] [args...]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'pre-compaction':
        # Read context data from stdin (JSON)
        try:
            context_data = json.load(sys.stdin) if not sys.stdin.isatty() else {}
        except:
            context_data = {}
        
        success = pre_compaction(context_data)
        sys.exit(0 if success else 1)
    
    elif command == 'post-compaction':
        session_key = sys.argv[2] if len(sys.argv) > 2 else None
        result = post_compaction(session_key)
        print(json.dumps(result, indent=2, default=str))
        sys.exit(0)
    
    elif command == 'retrieve':
        query = ' '.join(sys.argv[2:]) if len(sys.argv) > 2 else ''
        days = 7
        
        # Parse --days if provided
        for i, arg in enumerate(sys.argv):
            if arg == '--days' and i + 1 < len(sys.argv):
                try:
                    days = int(sys.argv[i + 1])
                except:
                    pass
        
        results = retrieve_context(query, days=days)
        print(json.dumps(results, indent=2, default=str))
        sys.exit(0)
    
    elif command == 'stats':
        mem = get_memory()
        stats = mem.stats()
        print(json.dumps(stats, indent=2, default=str))
        mem.close()
        sys.exit(0)
    
    elif command == 'prune':
        mem = get_memory()
        pruned = mem.prune_old_markdown()
        print(f"Pruned {pruned} old markdown files")
        mem.close()
        sys.exit(0)
    
    else:
        print(f"Unknown command: {command}")
        print("Commands: pre-compaction, post-compaction, retrieve, stats, prune")
        sys.exit(1)

if __name__ == '__main__':
    main()
