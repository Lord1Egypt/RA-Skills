# Group Deduplication Skill

A skill for searching WeChat/QQ/industry groups with automatic deduplication using memory-cache.

## Features

- 🔍 Search for groups across multiple platforms (WeChat, QQ, Industry)
- 🛡️ Automatic deduplication using MD5-based cache keys
- ⏰ Configurable TTL (default 30 days)
- 📊 Cache management tools for viewing/cleaning cached groups
- 🔗 Integration with existing memory-cache and multi-search-engine skills

## Installation

1. Ensure memory-cache skill is installed:
   ```bash
   openclaw clawhub install memory-cache
   ```

2. Install Redis and start the service:
   ```bash
   brew install redis
   brew services start redis
   ```

3. Configure Redis connection:
   ```bash
   echo "REDIS_URL=redis://localhost:6379/0" > /Users/x/.openclaw/workspace/skills/memory-cache/.env
   ```

4. Install dependencies:
   ```bash
   pip3 install -r /Users/x/.openclaw/workspace/skills/memory-cache/requirements.txt
   ```

## Usage

### Search for New Groups
```bash
# Search for AI industry groups
python3 $WORKSPACE/skills/group-deduplicate/scripts/search_groups.py --query "AI 人工智能 群" --max-results 10

# Search for WeChat groups only
python3 $WORKSPACE/skills/group-deduplicate/scripts/search_groups.py --query "区块链 技术" --platform wechat --max-results 5
```

### Cache Management
```bash
# List all cached groups
python3 $WORKSPACE/skills/group-deduplicate/scripts/cache_manager.py list

# Check if a specific group exists
python3 $WORKSPACE/skills/group-deduplicate/scripts/cache_manager.py check "群名称"

# Show cache statistics
python3 $WORKSPACE/skills/group-deduplicate/scripts/cache_manager.py stats

# Clean up expired entries
python3 $WORKSPACE/skills/group-deduplicate/scripts/cache_manager.py cleanup
```

## How It Works

1. **Search**: Uses multi-search-engine to find groups based on your query
2. **Normalize**: Group names are normalized (trimmed, lowercased) for consistent hashing
3. **Hash**: Creates MD5 hash of normalized name for cache key: `mema:groups:{hash}`
4. **Check**: Looks up key in memory-cache to see if group was previously discovered
5. **Filter**: Returns only groups not found in cache (new discoveries)
6. **Cache**: Automatically stores new groups in memory-cache with TTL
7. **Output**: Displays new groups with platform info and links

## Cache Key Format
```
mema:groups:{md5_hash_of_normalized_group_name}
```
- TTL: 30 days by default (configurable)
- Namespace: `mema:groups:` prevents key collisions

## Example Workflow
```
First search for "AI 群":
  → Found 3 new groups
  → Cached 3 new groups with 30-day TTL

Second search for "AI 群":
  → No new groups found (all results were duplicates)
  → Skipped 3 duplicate groups

Search for "机器学习 群":
  → Found 2 new groups (different query)
  → Cached 2 new groups with 30-day TTL
```

## Files
- `SKILL.md` - Skill documentation and metadata
- `scripts/search_groups.py` - Main search script with deduplication logic
- `scripts/cache_manager.py` - Cache management interface
- `requirements.txt` - Python dependencies (inherited from memory-cache)

## Notes
- Requires Redis server running (via memory-cache skill)
- Respects search engine rate limits (1-2 second delays)
- Only session cookies used temporarily (no persistence)
- Results include group name, platform, and example links
- Manual cache management available for administrative control