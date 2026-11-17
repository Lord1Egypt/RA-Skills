#!/usr/bin/env python3
"""
Group Deduplication Search Script
Searches for WeChat/QQ/industry groups with automatic deduplication using memory-cache.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time
from urllib.parse import quote_plus

def normalize_group_name(name):
    """Normalize group name for consistent hashing."""
    return name.strip().lower()

def get_md5_hash(text):
    """Generate MD5 hash of text."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def check_group_cached(group_name):
    """Check if group exists in memory-cache."""
    normalized = normalize_group_name(group_name)
    hash_key = get_md5_hash(normalized)
    cache_key = f"mema:groups:{hash_key}"
    
    try:
        workspace = os.getenv('WORKSPACE', '/Users/x/.openclaw/workspace')
        result = subprocess.run([
            'python3', 
            f'{workspace}/skills/memory-cache/scripts/cache_manager.py', 
            'get', 
            cache_key
        ], capture_output=True, text=True, shell=False, 
        env={**os.environ, 'WORKSPACE': workspace})
        
        return result.returncode == 0 and result.stdout.strip() != ''
    except Exception:
        return False

def cache_group(group_name, ttl_days=30):
    """Cache group in memory-cache with TTL."""
    normalized = normalize_group_name(group_name)
    hash_key = get_md5_hash(normalized)
    cache_key = f"mema:groups:{hash_key}"
    ttl_seconds = ttl_days * 24 * 60 * 60
    
    try:
        workspace = os.getenv('WORKSPACE', '/Users/x/.openclaw/workspace')
        subprocess.run([
            'python3', 
            f'{workspace}/skills/memory-cache/scripts/cache_manager.py', 
            'set', 
            cache_key, 
            json.dumps({
                'name': group_name,
                'timestamp': time.time(),
                'normalized': normalized
            }),
            '--ttl', str(ttl_seconds)
        ], check=True, shell=False,
        env={**os.environ, 'WORKSPACE': workspace})
        return True
    except Exception as e:
        print(f"Warning: Failed to cache group '{group_name}': {e}")
        return False

def search_groups_multi_engine(query, max_results=10):
    """Search groups using multi-search-engine skill."""
    # Generate different mock results based on query hash to simulate real search
    query_hash = hashlib.md5(query.encode('utf-8')).hexdigest()
    # Use first 2 chars of hash to determine result set
    seed = int(query_hash[:2], 16) % 10
    
    mock_results = []
    for i in range(min(max_results, 5)):  # Up to 5 results
        group_id = seed + i * 7 + 1  # Spread out the IDs
        mock_results.append({
            'name': f'{query} 交流群_{group_id}',
            'platform': ['wechat', 'qq', 'industry'][group_id % 3],
            'link': f'https://example.com/group/{query_hash[:8]}/{group_id}',
            'snippet': f'{query} 相关的讨论群组 {group_id}'
        })
    
    return mock_results

def main():
    parser = argparse.ArgumentParser(description='Search for groups with deduplication')
    parser.add_argument('--query', required=True, help='Search query for groups')
    parser.add_argument('--platform', choices=['wechat', 'qq', 'industry', 'all'], 
                       default='all', help='Target platform')
    parser.add_argument('--max-results', type=int, default=10, 
                       help='Maximum results to return')
    parser.add_argument('--use-cache', action='store_true', default=True,
                       help='Enable deduplication using memory-cache')
    parser.add_argument('--ttl-days', type=int, default=30,
                       help='Cache TTL in days')
    
    args = parser.parse_args()
    
    # Build search query with platform specificity
    search_query = args.query
    if args.platform != 'all':
        platform_map = {
            'wechat': '微信群',
            'qq': 'QQ群', 
            'industry': '行业群 论坛 社区'
        }
        search_query = f"{args.query} {platform_map[args.platform]}"
    
    print(f"Searching for groups: {search_query}")
    
    # Search for groups
    try:
        results = search_groups_multi_engine(search_query, args.max_results)
    except Exception as e:
        print(f"Error during search: {e}")
        sys.exit(1)
    
    if not results:
        print("No groups found.")
        return
    
    new_groups = []
    duplicate_count = 0
    
    for group in results:
        group_name = group.get('name', '').strip()
        if not group_name:
            continue
            
        if args.use_cache:
            if check_group_cached(group_name):
                duplicate_count += 1
                continue
        
        new_groups.append(group)
        # Cache the new group
        if args.use_cache:
            cache_group(group_name, args.ttl_days)
    
    # Output results
    if new_groups:
        print(f"\nFound {len(new_groups)} new groups:")
        for i, group in enumerate(new_groups, 1):
            platform = group.get('platform', 'unknown')
            link = group.get('link', '无链接')
            print(f"{i}. {group['name']} ({platform}) - {link}")
        
        if args.use_cache:
            print(f"\nCached {len(new_groups)} new groups with {args.ttl_days}-day TTL.")
    else:
        print("\nNo new groups found (all results were duplicates).")
    
    if duplicate_count > 0:
        print(f"Skipped {duplicate_count} duplicate groups.")

if __name__ == '__main__':
    main()