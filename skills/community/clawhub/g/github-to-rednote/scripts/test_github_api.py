#!/usr/bin/env python3
"""
Test script for GitHub API with various repository types.
Tests: large repos, small repos, different languages, error handling.
"""

import sys
import os
import time

# Add script directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from github_api import GitHubAPI, GitHubAPIError, GitHubCache


# Test repositories of different types
TEST_REPOS = [
    # Large, popular repos
    ("https://github.com/microsoft/vscode", "Large JS/TS editor"),
    ("https://github.com/torvalds/linux", "Huge C kernel"),
    ("https://github.com/python/cpython", "Large Python interpreter"),
    
    # Medium repos
    ("https://github.com/pallets/flask", "Medium Python web framework"),
    ("https://github.com/expressjs/express", "Medium Node.js framework"),
    
    # Small repos
    ("https://github.com/karpathy/nanoGPT", "Small ML project"),
    ("https://github.com/tj/commander.js", "Small CLI tool"),
    
    # Different languages
    ("https://github.com/golang/go", "Go language"),
    ("https://github.com/rust-lang/rust", "Rust language"),
    ("https://github.com/JetBrains/kotlin", "Kotlin language"),
]


def test_repo(api: GitHubAPI, url: str, description: str) -> dict:
    """Test fetching a single repository."""
    print(f"\n{'='*60}")
    print(f"Testing: {description}")
    print(f"URL: {url}")
    print('='*60)
    
    start_time = time.time()
    try:
        summary = api.get_repo_summary(url)
        elapsed = time.time() - start_time
        
        print(f"✓ Success ({elapsed:.2f}s)")
        print(f"  Name: {summary['full_name']}")
        print(f"  Stars: {summary['stars']:,}")
        print(f"  Forks: {summary['forks']:,}")
        print(f"  Language: {summary['language']}")
        print(f"  Topics: {len(summary['topics'])} topics")
        print(f"  README: {len(summary['readme']):,} chars")
        print(f"  Releases: {len(summary['releases'])} found")
        print(f"  Contributors: {len(summary['contributors'])} found")
        print(f"  Recent Commits: {len(summary['recent_commits'])} found")
        
        return {
            'success': True,
            'url': url,
            'data': summary,
            'elapsed': elapsed,
            'error': None
        }
        
    except Exception as e:
        elapsed = time.time() - start_time
        print(f"✗ Failed ({elapsed:.2f}s)")
        print(f"  Error: {e}")
        
        return {
            'success': False,
            'url': url,
            'data': None,
            'elapsed': elapsed,
            'error': str(e)
        }


def test_error_handling():
    """Test error handling for invalid inputs."""
    print(f"\n{'='*60}")
    print("Testing Error Handling")
    print('='*60)
    
    api = GitHubAPI()
    
    test_cases = [
        ("invalid-url", "Invalid URL format"),
        ("https://github.com/nonexistent-user-12345/nonexistent-repo-67890", "Non-existent repo"),
    ]
    
    for url, description in test_cases:
        print(f"\n  Test: {description}")
        print(f"  URL: {url}")
        try:
            result = api.get_repo_summary(url)
            print(f"  ✗ Unexpected success")
        except ValueError as e:
            print(f"  ✓ ValueError (expected): {e}")
        except GitHubAPIError as e:
            print(f"  ✓ GitHubAPIError (expected): {e.status_code} - {e}")


def test_caching():
    """Test cache functionality."""
    print(f"\n{'='*60}")
    print("Testing Cache Functionality")
    print('='*60)
    
    # Clear cache first
    cache = GitHubCache()
    cache.clear()
    print("  Cache cleared")
    
    api = GitHubAPI(cache=cache)
    url = "https://github.com/pallets/flask"
    
    # First fetch (should hit API)
    print(f"\n  First fetch (API call):")
    start = time.time()
    result1 = api.get_repo_summary(url)
    elapsed1 = time.time() - start
    print(f"    Time: {elapsed1:.2f}s")
    
    # Second fetch (should hit cache)
    print(f"\n  Second fetch (cache):")
    start = time.time()
    result2 = api.get_repo_summary(url)
    elapsed2 = time.time() - start
    print(f"    Time: {elapsed2:.2f}s")
    
    # Verify results match
    if result1['stars'] == result2['stars']:
        print(f"\n  ✓ Results match (stars: {result1['stars']:,})")
    else:
        print(f"\n  ✗ Results don't match!")
    
    # Show speedup
    if elapsed2 > 0:
        speedup = elapsed1 / elapsed2
        print(f"  ✓ Cache speedup: {speedup:.1f}x faster")
    
    # Cache stats
    stats = cache.stats()
    print(f"\n  Cache stats: {stats['file_count']} files, {stats['total_size_bytes']:,} bytes")


def test_rate_limit():
    """Test rate limit handling."""
    print(f"\n{'='*60}")
    print("Testing Rate Limit Info")
    print('='*60)
    
    api = GitHubAPI()
    try:
        rate_limit = api.get_rate_limit_info()
        print(f"  Rate limit: {rate_limit['limit']}")
        print(f"  Remaining: {rate_limit['remaining']}")
        print(f"  Used: {rate_limit['used']}")
        print(f"  Reset: {rate_limit['reset']}")
        print(f"\n  ✓ Rate limit info retrieved")
    except GitHubAPIError as e:
        print(f"  ✗ Error: {e}")


def main():
    """Run all tests."""
    print("="*60)
    print("GitHub API Test Suite")
    print("="*60)
    
    # Check token
    if not os.environ.get("GITHUB_TOKEN"):
        print("\n⚠️  Warning: GITHUB_TOKEN not set!")
        print("   Some tests may fail due to rate limiting.")
        print("   Set GITHUB_TOKEN for better results.\n")
    
    results = []
    api = GitHubAPI()
    
    # Test various repositories
    print("\n" + "="*60)
    print("Repository Tests")
    print("="*60)
    
    for url, description in TEST_REPOS:
        result = test_repo(api, url, description)
        results.append(result)
        
        # Small delay to be nice to the API
        time.sleep(0.5)
    
    # Test error handling
    test_error_handling()
    
    # Test caching
    test_caching()
    
    # Test rate limit
    test_rate_limit()
    
    # Summary
    print(f"\n{'='*60}")
    print("Test Summary")
    print('='*60)
    
    successful = sum(1 for r in results if r['success'])
    failed = sum(1 for r in results if not r['success'])
    total_time = sum(r['elapsed'] for r in results)
    
    print(f"  Total: {len(results)} repos tested")
    print(f"  Successful: {successful}")
    print(f"  Failed: {failed}")
    print(f"  Total time: {total_time:.2f}s")
    print(f"  Avg time per repo: {total_time/len(results):.2f}s")
    
    # Show failures
    if failed > 0:
        print(f"\n  Failed repositories:")
        for r in results:
            if not r['success']:
                print(f"    - {r['url']}: {r['error'][:60]}")
    
    print(f"\n{'='*60}")
    print("Test suite complete!")
    print('='*60)
    
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
