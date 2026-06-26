#!/usr/bin/env python3
"""
GitHub API wrapper with retry logic, rate limit handling, and caching.
Uses GITHUB_TOKEN environment variable for authentication.
"""

import os
import re
import json
import time
import hashlib
from typing import Dict, Optional, List, Tuple
from datetime import datetime, timedelta
from pathlib import Path

# Try to use requests if available, fallback to urllib
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    import urllib.request
    import urllib.error
    HAS_REQUESTS = False


class GitHubAPIError(Exception):
    """GitHub API error with status code and message."""
    def __init__(self, message: str, status_code: int = None, response_body: str = None, 
                 rate_limit_reset: int = None, retry_after: int = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_body = response_body
        self.rate_limit_reset = rate_limit_reset
        self.retry_after = retry_after


class GitHubRateLimitError(GitHubAPIError):
    """Specific error for rate limit exceeded."""
    pass


class GitHubCache:
    """Simple file-based cache for GitHub API responses."""
    
    def __init__(self, cache_dir: Optional[str] = None, ttl_hours: int = 1):
        """
        Initialize cache.
        
        Args:
            cache_dir: Directory for cache files (default: ~/.cache/github-to-rednote)
            ttl_hours: Cache TTL in hours
        """
        if cache_dir is None:
            cache_dir = os.path.expanduser("~/.cache/github-to-rednote")
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_cache_key(self, endpoint: str) -> str:
        """Generate cache key from endpoint."""
        return hashlib.md5(endpoint.encode()).hexdigest()
    
    def _get_cache_path(self, endpoint: str) -> Path:
        """Get cache file path for endpoint."""
        key = self._get_cache_key(endpoint)
        return self.cache_dir / f"{key}.json"
    
    def get(self, endpoint: str) -> Optional[Dict]:
        """Get cached response if not expired."""
        cache_path = self._get_cache_path(endpoint)
        
        if not cache_path.exists():
            return None
        
        try:
            with open(cache_path, 'r', encoding='utf-8') as f:
                cached = json.load(f)
            
            # Check TTL
            cached_time = datetime.fromisoformat(cached.get('cached_at', '2000-01-01'))
            if datetime.now() - cached_time > self.ttl:
                cache_path.unlink()  # Delete expired cache
                return None
            
            return cached.get('data')
        except (json.JSONDecodeError, KeyError, OSError):
            # Invalid cache, delete it
            try:
                cache_path.unlink()
            except OSError:
                pass
            return None
    
    def set(self, endpoint: str, data: Dict):
        """Cache response data."""
        cache_path = self._get_cache_path(endpoint)
        
        try:
            with open(cache_path, 'w', encoding='utf-8') as f:
                json.dump({
                    'cached_at': datetime.now().isoformat(),
                    'data': data
                }, f, ensure_ascii=False)
        except OSError:
            pass  # Ignore cache write errors
    
    def clear(self):
        """Clear all cached data."""
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                cache_file.unlink()
            except OSError:
                pass
    
    def stats(self) -> Dict:
        """Get cache statistics."""
        total_size = 0
        file_count = 0
        
        for cache_file in self.cache_dir.glob("*.json"):
            try:
                total_size += cache_file.stat().st_size
                file_count += 1
            except OSError:
                pass
        
        return {
            'file_count': file_count,
            'total_size_bytes': total_size,
            'cache_dir': str(self.cache_dir)
        }


class GitHubAPI:
    """GitHub API client with retry logic and caching."""
    
    BASE_URL = "https://api.github.com"
    
    def __init__(self, token: Optional[str] = None, cache: Optional[GitHubCache] = None,
                 max_retries: int = 3, retry_delay: float = 1.0):
        """
        Initialize GitHub API client.
        
        Args:
            token: GitHub token (defaults to GITHUB_TOKEN env var)
            cache: Cache instance (defaults to new GitHubCache)
            max_retries: Maximum retry attempts for rate limits
            retry_delay: Base delay between retries (seconds)
        """
        self.token = token or os.environ.get("GITHUB_TOKEN")
        if not self.token:
            raise ValueError("GitHub token required. Set GITHUB_TOKEN environment variable.")
        
        self.cache = cache or GitHubCache()
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        
        # Rate limit tracking
        self.rate_limit_remaining = None
        self.rate_limit_reset = None
    
    def _get_headers(self, extra_headers: Optional[Dict] = None) -> Dict:
        """Build request headers."""
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "GitHub-to-RedNote/1.0"
        }
        if extra_headers:
            headers.update(extra_headers)
        return headers
    
    def _parse_rate_limit(self, headers: Dict) -> Tuple[Optional[int], Optional[int]]:
        """Extract rate limit info from response headers."""
        remaining = headers.get('x-ratelimit-remaining')
        reset = headers.get('x-ratelimit-reset')
        return (
            int(remaining) if remaining else None,
            int(reset) if reset else None
        )
    
    def _make_request_requests(self, endpoint: str, headers: Optional[Dict] = None,
                               use_cache: bool = True) -> Dict:
        """Make request using requests library with retry logic."""
        url = f"{self.BASE_URL}{endpoint}"
        
        # Check cache first
        if use_cache:
            cached = self.cache.get(endpoint)
            if cached is not None:
                return cached
        
        all_headers = self._get_headers(headers)
        
        for attempt in range(self.max_retries):
            try:
                response = requests.get(url, headers=all_headers, timeout=30)
                
                # Update rate limit tracking
                self.rate_limit_remaining, self.rate_limit_reset = \
                    self._parse_rate_limit(response.headers)
                
                # Handle rate limit
                if response.status_code == 403 and 'rate limit' in response.text.lower():
                    retry_after = response.headers.get('retry-after')
                    reset_time = self.rate_limit_reset
                    
                    if retry_after:
                        wait_time = int(retry_after)
                    elif reset_time:
                        wait_time = max(0, reset_time - int(time.time()) + 1)
                    else:
                        wait_time = 60
                    
                    if attempt < self.max_retries - 1:
                        print(f"  Rate limit hit. Waiting {wait_time}s...", flush=True)
                        time.sleep(min(wait_time, 60))  # Cap at 60s
                        continue
                    else:
                        raise GitHubRateLimitError(
                            f"GitHub rate limit exceeded. Reset at {reset_time}",
                            status_code=403,
                            rate_limit_reset=reset_time,
                            retry_after=retry_after
                        )
                
                # Handle other errors
                if response.status_code >= 400:
                    raise GitHubAPIError(
                        f"GitHub API error: {response.status_code} - {response.reason}",
                        status_code=response.status_code,
                        response_body=response.text
                    )
                
                data = response.json()
                
                # Cache successful response
                if use_cache:
                    self.cache.set(endpoint, data)
                
                return data
                
            except requests.exceptions.RequestException as e:
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)  # Exponential backoff
                    print(f"  Request failed, retrying in {delay}s... ({e})", flush=True)
                    time.sleep(delay)
                else:
                    raise GitHubAPIError(f"Network error: {e}")
        
        raise GitHubAPIError("Max retries exceeded")
    
    def _make_request_urllib(self, endpoint: str, headers: Optional[Dict] = None,
                             use_cache: bool = True) -> Dict:
        """Make request using urllib with retry logic."""
        url = f"{self.BASE_URL}{endpoint}"
        
        # Check cache first
        if use_cache:
            cached = self.cache.get(endpoint)
            if cached is not None:
                return cached
        
        all_headers = self._get_headers(headers)
        
        for attempt in range(self.max_retries):
            try:
                request = urllib.request.Request(url, headers=all_headers)
                
                with urllib.request.urlopen(request, timeout=30) as response:
                    # Update rate limit tracking
                    self.rate_limit_remaining, self.rate_limit_reset = \
                        self._parse_rate_limit(dict(response.headers))
                    
                    data = json.loads(response.read().decode('utf-8'))
                    
                    # Cache successful response
                    if use_cache:
                        self.cache.set(endpoint, data)
                    
                    return data
                    
            except urllib.error.HTTPError as e:
                body = e.read().decode('utf-8') if hasattr(e, 'read') else None
                
                # Handle rate limit
                if e.code == 403 and body and 'rate limit' in body.lower():
                    reset_time = int(dict(e.headers).get('x-ratelimit-reset', 0))
                    retry_after = dict(e.headers).get('retry-after')
                    
                    if retry_after:
                        wait_time = int(retry_after)
                    elif reset_time:
                        wait_time = max(0, reset_time - int(time.time()) + 1)
                    else:
                        wait_time = 60
                    
                    if attempt < self.max_retries - 1:
                        print(f"  Rate limit hit. Waiting {wait_time}s...", flush=True)
                        time.sleep(min(wait_time, 60))
                        continue
                    else:
                        raise GitHubRateLimitError(
                            f"GitHub rate limit exceeded",
                            status_code=403,
                            rate_limit_reset=reset_time,
                            retry_after=retry_after
                        )
                
                raise GitHubAPIError(
                    f"GitHub API error: {e.code} - {e.reason}",
                    status_code=e.code,
                    response_body=body
                )
                
            except urllib.error.URLError as e:
                if attempt < self.max_retries - 1:
                    delay = self.retry_delay * (2 ** attempt)
                    print(f"  Network error, retrying in {delay}s... ({e.reason})", flush=True)
                    time.sleep(delay)
                else:
                    raise GitHubAPIError(f"Network error: {e.reason}")
                    
            except json.JSONDecodeError as e:
                raise GitHubAPIError(f"Invalid JSON response: {e}")
        
        raise GitHubAPIError("Max retries exceeded")
    
    def _request(self, endpoint: str, headers: Optional[Dict] = None,
                 use_cache: bool = True) -> Dict:
        """Make authenticated request to GitHub API."""
        if HAS_REQUESTS:
            return self._make_request_requests(endpoint, headers, use_cache)
        else:
            return self._make_request_urllib(endpoint, headers, use_cache)
    
    @staticmethod
    def parse_github_url(url: str) -> Tuple[str, str]:
        """
        Parse GitHub URL to extract owner and repo.
        
        Supports:
        - https://github.com/owner/repo
        - https://github.com/owner/repo.git
        - github.com/owner/repo
        - owner/repo
        
        Returns: (owner, repo) tuple
        """
        # Remove protocol and .git suffix
        url = re.sub(r'^https?://', '', url)
        url = re.sub(r'\.git$', '', url)
        
        # Match github.com/owner/repo or just owner/repo
        patterns = [
            r'github\.com/([^/]+)/([^/]+)/?.*',
            r'^([^/]+)/([^/]+)$'
        ]
        
        for pattern in patterns:
            match = re.match(pattern, url)
            if match:
                return match.group(1), match.group(2)
        
        raise ValueError(f"Invalid GitHub URL format: {url}")
    
    def get_repo_info(self, owner: str, repo: str) -> Dict:
        """Get repository basic information."""
        from urllib.parse import quote
        return self._request(f"/repos/{quote(owner, safe='')}/{quote(repo, safe='')}")
    
    def get_readme(self, owner: str, repo: str) -> str:
        """Get repository README content (decoded)."""
        from urllib.parse import quote
        try:
            data = self._request(
                f"/repos/{quote(owner, safe='')}/{quote(repo, safe='')}/readme"
            )
            import base64
            content = base64.b64decode(data.get('content', '').replace('\n', ''))
            return content.decode('utf-8', errors='replace')
        except GitHubAPIError as e:
            if e.status_code == 404:
                return ""
            raise
    
    def get_languages(self, owner: str, repo: str) -> Dict[str, int]:
        """Get repository language statistics."""
        from urllib.parse import quote
        return self._request(
            f"/repos/{quote(owner, safe='')}/{quote(repo, safe='')}/languages"
        )
    
    def get_releases(self, owner: str, repo: str, limit: int = 5) -> List[Dict]:
        """Get recent releases for the repository."""
        from urllib.parse import quote
        try:
            releases = self._request(
                f"/repos/{quote(owner, safe='')}/{quote(repo, safe='')}/releases?per_page={limit}"
            )
            return releases if isinstance(releases, list) else []
        except GitHubAPIError as e:
            if e.status_code == 404:
                return []
            raise
    
    def get_contributors(self, owner: str, repo: str, limit: int = 10) -> List[Dict]:
        """Get top contributors for the repository."""
        from urllib.parse import quote
        try:
            contributors = self._request(
                f"/repos/{quote(owner, safe='')}/{quote(repo, safe='')}/contributors?per_page={limit}"
            )
            if not isinstance(contributors, list):
                return []
            return [{
                'login': c.get('login'),
                'contributions': c.get('contributions', 0),
                'avatar_url': c.get('avatar_url'),
                'html_url': c.get('html_url')
            } for c in contributors]
        except GitHubAPIError as e:
            if e.status_code == 404 or e.status_code == 403:
                return []
            raise
    
    def get_commits(self, owner: str, repo: str, limit: int = 10) -> List[Dict]:
        """Get recent commits for the repository."""
        from urllib.parse import quote
        try:
            commits = self._request(
                f"/repos/{quote(owner, safe='')}/{quote(repo, safe='')}/commits?per_page={limit}"
            )
            if not isinstance(commits, list):
                return []
            return [{
                'sha': c.get('sha', '')[:7],
                'message': c.get('commit', {}).get('message', '').split('\n')[0],
                'author': c.get('commit', {}).get('author', {}).get('name', 'Unknown'),
                'date': c.get('commit', {}).get('author', {}).get('date', '')
            } for c in commits]
        except GitHubAPIError:
            return []
    
    def get_repo_summary(self, url: str, include_releases: bool = True,
                        include_contributors: bool = True) -> Dict:
        """
        Get complete repository summary for article generation.
        Enhanced version with README features and selling points extraction.
        
        Returns dict with:
        - url: Original URL
        - owner: Repository owner
        - repo: Repository name
        - full_name: owner/repo
        - description: Repo description
        - stars: Star count
        - forks: Fork count
        - open_issues: Open issues count
        - watchers: Watchers count
        - language: Primary language
        - languages: All languages with bytes
        - topics: Repository topics
        - readme: README content
        - readme_features: Extracted features from README
        - selling_points: Key selling points
        - created_at: Creation date
        - updated_at: Last update date
        - pushed_at: Last push date
        - homepage: Project homepage
        - license: License info
        - size: Repository size (KB)
        - default_branch: Default branch name
        - releases: Recent releases (if include_releases=True)
        - latest_release: Latest release details
        - contributors: Top contributors (if include_contributors=True)
        - recent_commits: Recent commits
        - archived: Whether repo is archived
        - fork: Whether repo is a fork
        """
        owner, repo = self.parse_github_url(url)
        
        # Fetch basic info
        info = self.get_repo_info(owner, repo)
        
        # Fetch README (non-blocking if fails)
        try:
            readme = self.get_readme(owner, repo)
        except GitHubAPIError:
            readme = ""
        
        # Fetch languages
        try:
            languages = self.get_languages(owner, repo)
        except GitHubAPIError:
            languages = {}
        
        # Determine primary language
        primary_lang = max(languages, key=languages.get) if languages else info.get('language', 'Unknown')
        
        # Fetch releases
        releases = []
        latest_release = {}
        if include_releases:
            try:
                releases = self.get_releases(owner, repo, limit=5)
                if releases:
                    latest_release = releases[0]
            except GitHubAPIError:
                pass
        
        # Fetch contributors
        contributors = []
        if include_contributors:
            try:
                contributors = self.get_contributors(owner, repo, limit=10)
            except GitHubAPIError:
                pass
        
        # Fetch recent commits
        recent_commits = []
        try:
            recent_commits = self.get_commits(owner, repo, limit=5)
        except GitHubAPIError:
            pass
        
        # Extract features from README
        readme_features = self._extract_readme_features(readme)
        
        # Extract selling points
        selling_points = self._extract_selling_points(readme, info)
        
        return {
            'url': url,
            'html_url': info.get('html_url', url),
            'owner': owner,
            'repo': repo,
            'full_name': info.get('full_name', f"{owner}/{repo}"),
            'description': info.get('description', ''),
            'stars': info.get('stargazers_count', 0),
            'forks': info.get('forks_count', 0),
            'open_issues': info.get('open_issues_count', 0),
            'watchers': info.get('watchers_count', 0),
            'language': primary_lang,
            'languages': languages,
            'topics': info.get('topics', []),
            'readme': readme[:15000] if readme else '',  # Limit README size
            'readme_features': readme_features,
            'selling_points': selling_points,
            'created_at': info.get('created_at', ''),
            'updated_at': info.get('updated_at', ''),
            'pushed_at': info.get('pushed_at', ''),
            'homepage': info.get('homepage', ''),
            'license': info.get('license', {}).get('name', 'Unknown') if info.get('license') else 'Unknown',
            'license_spdx': info.get('license', {}).get('spdx_id', '') if info.get('license') else '',
            'size': info.get('size', 0),
            'default_branch': info.get('default_branch', 'main'),
            'releases': releases,
            'latest_release': latest_release,
            'contributors': contributors,
            'recent_commits': recent_commits,
            'archived': info.get('archived', False),
            'fork': info.get('fork', False),
            'private': info.get('private', False)
        }
    
    def _extract_readme_features(self, readme: str) -> List[str]:
        """Extract Features section from README (supports English and Chinese)."""
        if not readme:
            return []
        
        features = []
        
        # Common patterns for Features section (English + Chinese)
        patterns = [
            # English patterns
            r'##\s*Features?\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'##\s*Key\s+Features?\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'###\s*Features?\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'(?i)^\s*features?:\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            # Chinese patterns - 功能特点/功能特性/特性/功能 (with optional emoji)
            r'##\s*(?:✨\s*)?功能特点\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'##\s*(?:✨\s*)?功能特性\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'##\s*(?:✨\s*)?特性\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'##\s*(?:✨\s*)?功能\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'###\s*(?:✨\s*)?功能特点\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'###\s*(?:✨\s*)?功能特性\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'###\s*(?:✨\s*)?特性\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            r'###\s*(?:✨\s*)?功能\s*\n((?:[-*•]\s*[^\n]+\n?)+)',
            # Bullet pattern with Chinese feature descriptions
            r'(?i)^\s*[-*]\s*([^\n:]+):\s*[^\n]+\n((?:\s+[-*]\s*[^\n]+\n?)*)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, readme, re.MULTILINE)
            for match in matches:
                # match might be a string or tuple
                content = match[0] if isinstance(match, tuple) else match
                for line in content.strip().split('\n'):
                    line = line.strip().lstrip('-*•').strip()
                    if line and len(line) > 5 and len(line) < 200:
                        # Clean markdown links
                        line = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', line)
                        # Clean inline code markers
                        line = re.sub(r'`([^`]+)`', r'\1', line)
                        features.append(line)
                if features:
                    break
            if features:
                break
        
        return features[:10]  # Limit to 10 features
    
    def _extract_selling_points(self, readme: str, info: Dict) -> List[str]:
        """Extract key selling points from repo info and README."""
        points = []
        
        # 1. High stars count
        stars = info.get('stargazers_count', 0)
        if stars >= 10000:
            points.append(f"社区高度认可（{stars/1000:.0f}k+ stars）")
        elif stars >= 1000:
            points.append(f"获得广泛关注（{stars/1000:.1f}k stars）")
        
        # 2. Active development
        pushed_at = info.get('pushed_at', '')
        if pushed_at:
            try:
                from datetime import datetime
                push_date = datetime.fromisoformat(pushed_at.replace('Z', '+00:00'))
                days_since = (datetime.now().replace(tzinfo=push_date.tzinfo) - push_date).days
                if days_since < 7:
                    points.append("近期活跃维护（7天内更新）")
                elif days_since < 30:
                    points.append("持续维护（30天内更新）")
            except:
                pass
        
        # 3. Good documentation
        if readme and len(readme) > 2000:
            points.append("文档完善")
        
        # 4. Popular language
        lang = info.get('language', '')
        if lang:
            points.append(f"基于 {lang} 开发")
        
        # 5. Many contributors
        if info.get('forks_count', 0) > 100:
            points.append(f"Fork 数众多（{info['forks_count']}）")
        
        # 6. Stable releases
        if info.get('releases'):
            points.append("有稳定版本发布")
        
        # 7. License
        license_name = info.get('license', {}).get('spdx_id', '') if info.get('license') else ''
        if license_name in ['MIT', 'Apache-2.0', 'BSD-3-Clause']:
            points.append(f"宽松开源协议（{license_name}）")
        
        # 8. Topics indicate use cases
        topics = info.get('topics', [])
        if topics:
            # Extract meaningful topics
            use_case_topics = [t for t in topics[:3] if t not in ['python', 'javascript', 'go', 'rust', 'java']]
            if use_case_topics:
                points.append(f"适用场景: {', '.join(use_case_topics)}")
        
        return points
    
    def get_rate_limit_info(self) -> Dict:
        """Get current rate limit status."""
        data = self._request("/rate_limit", use_cache=False)
        return {
            'limit': data.get('resources', {}).get('core', {}).get('limit', 0),
            'remaining': data.get('resources', {}).get('core', {}).get('remaining', 0),
            'reset': data.get('resources', {}).get('core', {}).get('reset', 0),
            'used': data.get('resources', {}).get('core', {}).get('used', 0)
        }


def main():
    """CLI test for GitHub API."""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python3 github_api.py <github-url> [--no-cache]")
        print("\nExamples:")
        print("  python3 github_api.py https://github.com/torvalds/linux")
        print("  python3 github_api.py microsoft/vscode")
        sys.exit(1)
    
    url = sys.argv[1]
    no_cache = '--no-cache' in sys.argv
    
    try:
        cache = None if no_cache else GitHubCache()
        api = GitHubAPI(cache=cache)
        
        print(f"Fetching data for: {url}")
        if not no_cache:
            print(f"Cache dir: {api.cache.cache_dir}")
        
        start_time = time.time()
        summary = api.get_repo_summary(url)
        elapsed = time.time() - start_time
        
        print(f"\n✓ Repository: {summary['full_name']}")
        print(f"  Description: {summary['description']}")
        print(f"  Stars: {summary['stars']:,}")
        print(f"  Forks: {summary['forks']:,}")
        print(f"  Watchers: {summary['watchers']:,}")
        print(f"  Language: {summary['language']}")
        print(f"  All Languages: {', '.join(summary['languages'].keys())}")
        print(f"  Topics: {', '.join(summary['topics'])}")
        print(f"  License: {summary['license']}")
        print(f"  Size: {summary['size']:,} KB")
        print(f"  Default branch: {summary['default_branch']}")
        print(f"  Created: {summary['created_at']}")
        print(f"  Updated: {summary['updated_at']}")
        print(f"  Archived: {summary['archived']}")
        print(f"  README length: {len(summary['readme']):,} chars")
        
        if summary['releases']:
            print(f"\n  Recent Releases ({len(summary['releases'])}):")
            for rel in summary['releases'][:3]:
                print(f"    - {rel.get('tag_name', 'N/A')}: {rel.get('name', 'No name')}")
        
        if summary['contributors']:
            print(f"\n  Top Contributors ({len(summary['contributors'])}):")
            for c in summary['contributors'][:5]:
                print(f"    - {c['login']}: {c['contributions']} commits")
        
        if summary['recent_commits']:
            print(f"\n  Recent Commits ({len(summary['recent_commits'])}):")
            for c in summary['recent_commits'][:3]:
                print(f"    - {c['sha']}: {c['message'][:50]}")
        
        print(f"\n  Fetched in {elapsed:.2f}s")
        
        # Show rate limit
        try:
            rate_limit = api.get_rate_limit_info()
            print(f"\n  Rate Limit: {rate_limit['remaining']}/{rate_limit['limit']} remaining")
        except GitHubAPIError:
            pass
            
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except GitHubAPIError as e:
        print(f"GitHub API Error: {e}")
        if e.status_code:
            print(f"Status: {e.status_code}")
            if e.status_code == 401:
                print("Check your GITHUB_TOKEN environment variable.")
            elif e.status_code == 404:
                print("Repository not found. Check the URL.")
            elif e.status_code == 403:
                print("API rate limit exceeded or access forbidden.")
        sys.exit(1)


if __name__ == "__main__":
    main()
