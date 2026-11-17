#!/usr/bin/env python3
"""
Cache Manager for Group Deduplication Skill
Handles memory-cache operations for storing and retrieving group information.
"""

import argparse
import hashlib
import json
import os
import subprocess
import sys
import time

def normalize_group_name(name):
    """Normalize group name for consistent hashing."""
    return name.strip().lower()

def get_md5_hash(text):
    """Generate MD5 hash of text."""
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def get_cache_key(group_name):
    """Get cache key for a group name."""
    normalized = normalize_group_name(group_name)
    hash_key = get_md5_hash(normalized)
    return f"mema:groups:{hash_key}"

def cache_get(cache_key):
    """Get value from memory-cache."""
    try:
        workspace = os.getenv('WORKSPACE', '/Users/x/.openclaw/workspace')
        result = subprocess.run([
            'python3', 
            f'{workspace}/skills/memory-cache/scripts/cache_manager.py', 
            'get', 
            cache_key
        ], capture_output=True, text=True, shell=False, 
        env={**os.environ, 'WORKSPACE': workspace})
        
        if result.returncode == 0 and result.stdout.strip():
            return json.loads(result.stdout.strip())
        return None
    except Exception:
        return None

def cache_set(cache_key, value, ttl_seconds=None):
    """Set value in memory-cache."""
    workspace = os.getenv('WORKSPACE', '/Users/x/.openclaw/workspace')
    cmd = [
        'python3', 
        f'{workspace}/skills/memory-cache/scripts/cache_manager.py', 
        'set', 
        cache_key, 
        json.dumps(value)
    ]
    
    if ttl_seconds:
        cmd.extend(['--ttl', str(ttl_seconds)])
    
    try:
        subprocess.run(cmd, check=True, shell=False,
        env={**os.environ, 'WORKSPACE': workspace})
        return True
    except Exception:
        return False

def cache_delete(cache_key):
    """Delete key from memory-cache."""
    workspace = os.getenv('WORKSPACE', '/Users/x/.openclaw/workspace')
    try:
        subprocess.run([
            'python3', 
            f'{workspace}/skills/memory-cache/scripts/cache_manager.py', 
            'delete', 
            cache_key
        ], check=True, shell=False,
        env={**os.environ, 'WORKSPACE': workspace})
        return True
    except Exception:
        return False

def cache_scan(pattern="*"):
    """Scan for keys matching pattern in memory-cache."""
    workspace = os.getenv('WORKSPACE', '/Users/x/.openclaw/workspace')
    try:
        result = subprocess.run([
            'python3', 
            f'{workspace}/skills/memory-cache/scripts/cache_manager.py', 
            'scan', 
            pattern
        ], capture_output=True, text=True, shell=False,
        env={**os.environ, 'WORKSPACE': workspace})
        
        if result.returncode == 0:
            # Parse the scan output (assuming it returns keys line by line)
            keys = [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
            return keys
        return []
    except Exception:
        return []

def list_groups():
    """List all cached groups."""
    print("Cached groups:")
    print("-" * 50)
    
    # Scan for group cache keys
    keys = cache_scan("mema:groups:*")
    
    if not keys:
        print("No groups cached.")
        return
    
    groups = []
    for key in keys:
        value = cache_get(key)
        if value:
            groups.append((key, value))
    
    if not groups:
        print("No valid group entries found.")
        return
    
    # Sort by timestamp (newest first)
    groups.sort(key=lambda x: x[1].get('timestamp', 0), reverse=True)
    
    for i, (key, value) in enumerate(groups, 1):
        name = value.get('name', 'Unknown')
        timestamp = value.get('timestamp', 0)
        normalized = value.get('normalized', '')
        # Calculate TTL remaining (approximate)
        age = time.time() - timestamp
        print(f"{i}. {name}")
        print(f"   Normalized: {normalized}")
        print(f"   Cached: {time.ctime(timestamp)} ({int(age/86400)} days ago)")
        print(f"   Key: {key}")
        print()

def check_group(group_name):
    """Check if a specific group exists in cache."""
    cache_key = get_cache_key(group_name)
    value = cache_get(cache_key)
    
    if value:
        print(f"✓ Group '{group_name}' found in cache:")
        print(f"  Name: {value.get('name')}")
        print(f"  Normalized: {value.get('normalized')}")
        print(f"  Timestamp: {time.ctime(value.get('timestamp', 0))}")
        return True
    else:
        print(f"✗ Group '{group_name}' not found in cache.")
        return False

def add_group(group_name, ttl_days=30):
    """Manually add a group to cache."""
    cache_key = get_cache_key(group_name)
    ttl_seconds = ttl_days * 24 * 60 * 60
    
    value = {
        'name': group_name,
        'normalized': normalize_group_name(group_name),
        'timestamp': time.time(),
        'added_manually': True
    }
    
    if cache_set(cache_key, value, ttl_seconds):
        print(f"✓ Added group '{group_name}' to cache with {ttl_days}-day TTL.")
        return True
    else:
        print(f"✗ Failed to add group '{group_name}' to cache.")
        return False

def remove_group(group_name):
    """Remove a group from cache."""
    cache_key = get_cache_key(group_name)
    
    if cache_delete(cache_key):
        print(f"✓ Removed group '{group_name}' from cache.")
        return True
    else:
        print(f"✗ Failed to remove group '{group_name}' from cache (may not exist).")
        return False

def cleanup_expired():
    """Clean up expired cache entries."""
    # Note: memory-cache handles TTL automatically, but we can do a manual cleanup
    # by scanning and checking timestamps if needed
    print("Cache cleanup: memory-cache handles TTL automatically.")
    print("Expired entries will be removed automatically by Redis.")
    
    # Optional: we could implement a more aggressive cleanup here
    keys = cache_scan("mema:groups:*")
    expired_count = 0
    current_time = time.time()
    
    for key in keys:
        value = cache_get(key)
        if value:
            timestamp = value.get('timestamp', 0)
            # If older than 35 days (5 days grace period), consider expired
            if current_time - timestamp > (35 * 24 * 60 * 60):
                if cache_delete(key):
                    expired_count += 1
    
    if expired_count > 0:
        print(f"✓ Cleaned up {expired_count} expired entries.")
    else:
        print("✓ No expired entries found.")

def show_stats():
    """Show cache statistics."""
    keys = cache_scan("mema:groups:*")
    total_keys = len(keys)
    
    valid_count = 0
    total_size_estimate = 0
    
    for key in keys:
        value = cache_get(key)
        if value:
            valid_count += 1
            # Rough size estimate
            total_size_estimate += len(json.dumps(value))
    
    print("Group Cache Statistics:")
    print("-" * 30)
    print(f"Total cache keys: {total_keys}")
    print(f"Valid group entries: {valid_count}")
    print(f"Estimated cache size: {total_size_estimate} bytes")
    print(f"Default TTL: 30 days")

def main():
    parser = argparse.ArgumentParser(description='Manage group deduplication cache')
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List all cached groups')
    
    # Check command
    check_parser = subparsers.add_parser('check', help='Check if group exists in cache')
    check_parser.add_argument('group_name', help='Group name to check')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add group to cache')
    add_parser.add_argument('group_name', help='Group name to add')
    add_parser.add_argument('--ttl-days', type=int, default=30, help='Cache TTL in days')
    
    # Remove command
    remove_parser = subparsers.add_parser('remove', help='Remove group from cache')
    remove_parser.add_argument('group_name', help='Group name to remove')
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser('cleanup', help='Clean up expired entries')
    
    # Stats command
    stats_parser = subparsers.add_parser('stats', help='Show cache statistics')
    
    args = parser.parse_args()
    
    if args.command == 'list':
        list_groups()
    elif args.command == 'check':
        check_group(args.group_name)
    elif args.command == 'add':
        add_group(args.group_name, args.ttl_days)
    elif args.command == 'remove':
        remove_group(args.group_name)
    elif args.command == 'cleanup':
        cleanup_expired()
    elif args.command == 'stats':
        show_stats()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()