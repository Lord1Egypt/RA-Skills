---
name: group-deduplicate
description: "Search for WeChat/QQ/industry groups with automatic deduplication using memory-cache. Finds new groups only, avoids pushing duplicates, and caches discovered groups for 30 days. Use when you need to discover and track unique community groups without repetition."
---

# Group Deduplication Skill

Automatically searches for community groups (WeChat, QQ, industry groups) and filters out duplicates using memory-cache with MD5-based keys and 30-day TTL.

## Workflow
1. **Search**: Find groups using multi-search-engine across platforms
2. **Deduplicate**: Check memory-cache for existing group records using MD5 hashes
3. **Filter**: Return only new groups not previously discovered
4. **Push**: Output new groups for user consumption
5. **Cache**: Automatically store discovered groups in memory-cache with TTL 30 days

## Key Features
- **MD5-based deduplication**: Uses `mema:groups:{群名MD5}` key format
- **30-day TTL**: Cached entries automatically expire after 30 days
- **Zero duplicates**: Only returns genuinely new group discoveries
- **Multi-platform**: Searches WeChat, QQ, and industry groups
- **Memory efficient**: Uses existing memory-cache skill for storage

## Requirements
- memory-cache skill must be installed
- REDIS_URL environment variable configured for memory-cache
- multi-search-engine skill available (bundled with OpenClaw)

## Usage

### Basic Search
Search for new groups in a specific industry or topic:
```
# Search for new AI industry groups
python3 $WORKSPACE/skills/group-deduplicate/scripts/search_groups.py --query "AI 人工智能 群" --max-results 10

# Search for new WeChat groups about blockchain
python3 $WORKSPACE/skills/group-deduplicate/scripts/search_groups.py --query "区块链 区块链技术 微信群" --platform wechat --max-results 5
```

### Check Cache Status
View current cached groups or clear cache:
```
# See all cached groups
python3 $WORKSPACE/skills/group-deduplicate/scripts/cache_manager.py list

# Clear expired cache entries
python3 $WORKSPACE/skills/group-deduplicate/scripts/cache_manager.py cleanup

# Check specific group existence
python3 $WORKSPACE/skills/group-deduplicate/scripts/cache_manager.py check "群名称"
```

## Installation
This skill assumes memory-cache is already installed. If not:
```
openclaw clawhub install memory-cache
```

## Scripts Included

### `scripts/search_groups.py`
Main search script with deduplication logic:
- `--query`: Search query (required)
- `--platform`: Target platform (wechat, qq, industry, all) - default: all
- `--max-results`: Maximum results to return - default: 10
- `--use-cache`: Enable deduplication (default: true)
- `--ttl-days`: Cache TTL in days (default: 30)

### `scripts/cache_manager.py`
Cache management interface:
- `list`: Show all cached groups
- `check <group-name>`: Check if group exists in cache
- `add <group-name>`: Manually add group to cache
- `remove <group-name>`: Remove group from cache
- `cleanup`: Remove expired entries
- `stats`: Show cache statistics

## Technical Details

### Cache Key Format
```
mema:groups:{md5_hash_of_group_name}
```
- Uses MD5 hash of normalized group name for consistent keys
- TTL defaults to 30 days (2592000 seconds)
- Stored in memory-cache namespace

### Search Process
1. Normalize group name (trim whitespace, lowercase for hashing)
2. Generate MD5 hash for cache key lookup
3. Check memory-cache for existing entry
4. If not found, return as new group and cache it
5. If found, skip as duplicate

### Supported Platforms
- **WeChat**: Searches WeChat groups/channels
- **QQ**: Searches QQ groups
- **Industry**: Searches industry forums, Tieba, professional networks
- **All**: Searches across all platforms (default)

## Example Output
When running a search, you'll get:
```
Found 3 new groups:
1. AI技术交流群 (WeChat) - https://...
2. Machine Learning论坛 (Industry) - https://...
3. Deep Learning实战QQ群 (QQ) - https://...

Cached 3 new groups with 30-day TTL.
```

## Notes
- The skill respects search engine rate limits (1-2 second delays)
- Only session cookies are used temporarily (no persistence)
- Results include group name, platform, and link when available
- Cache survives OpenClaw restarts via Redis persistence
- Manual cache management available for administrative control

## Troubleshooting
If you see "Redis connection failed":
1. Ensure REDIS_URL is set in your environment
2. Verify Redis server is running
3. Check memory-cache skill installation

If searches return no results:
1. Try broader or different search queries
2. Verify multi-search-engine skill is functional
3. Check network connectivity to search engines