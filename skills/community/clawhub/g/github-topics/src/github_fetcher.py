"""
GitHub Fetcher - 从 GitHub API 获取仓库数据
使用 GitHub Search API 按话题获取仓库
"""
import time
import requests
from typing import Dict, List, Optional
from datetime import datetime, timedelta

from src.config import (
    GITHUB_TOKEN, TOPIC, GITHUB_API_BASE,
    GITHUB_PER_PAGE, GITHUB_MAX_PAGES, GITHUB_SEARCH_SORT,
    GITHUB_SEARCH_ORDER, FETCH_REQUEST_DELAY
)


class GitHubFetcher:
    """从 GitHub API 获取仓库数据"""

    def __init__(self, token: str = None, topic: str = None):
        """
        初始化

        Args:
            token: GitHub Personal Access Token
            topic: 要搜索的 GitHub Topic
        """
        self.token = token or GITHUB_TOKEN
        self.topic = topic or TOPIC
        self.api_base = GITHUB_API_BASE
        self.per_page = GITHUB_PER_PAGE
        self.max_pages = GITHUB_MAX_PAGES
        self.delay = FETCH_REQUEST_DELAY

        self.session = requests.Session()
        self.session.headers.update({
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Topics-Trending/1.0"
        })

        if self.token:
            self.session.headers.update({
                "Authorization": f"Bearer {self.token}"
            })

        self.rate_limit_remaining = 5000
        self.rate_limit_reset = None

    def fetch(self, sort_by: str = None, limit: int = None) -> List[Dict]:
        """
        获取指定话题下的仓库列表

        Args:
            sort_by: 排序方式 (stars, forks, updated)
            limit: 最大返回数量

        Returns:
            [
                {
                    "rank": 1,
                    "repo_name": "owner/repo",
                    "owner": "owner",
                    "stars": 1000,
                    "forks": 100,
                    "issues": 10,
                    "language": "Python",
                    "url": "https://github.com/owner/repo",
                    "description": "...",
                    "topics": ["topic1", "topic2"],
                    "created_at": "2024-01-01T00:00:00Z",
                    "updated_at": "2024-01-01T00:00:00Z"
                },
                ...
            ]
        """
        sort_by = sort_by or GITHUB_SEARCH_SORT
        limit = limit or (self.per_page * self.max_pages)

        print(f"📡 正在获取话题 '{self.topic}' 的仓库列表...")
        print(f"   排序方式: {sort_by}")

        repos = []
        page = 1

        while page <= self.max_pages and len(repos) < limit:
            # 检查速率限制
            if self.rate_limit_remaining < 10:
                self._wait_for_rate_limit()

            data = self._fetch_page(page, sort_by)

            if not data or "items" not in data:
                break

            items = data["items"]
            if not items:
                break

            for item in items:
                repo = self._parse_repo_item(item, len(repos) + 1)
                repos.append(repo)

                if len(repos) >= limit:
                    break

            # 更新速率限制信息
            self._update_rate_limit(data)

            print(f"   第 {page} 页: 获取 {len(items)} 个仓库 (累计 {len(repos)})")

            # 如果返回数量少于 per_page，说明已经到最后一页
            if len(items) < self.per_page:
                break

            page += 1

            # 请求间隔
            if page <= self.max_pages and len(repos) < limit:
                time.sleep(self.delay)

        print(f"✅ 成功获取 {len(repos)} 个仓库")
        return repos

    def _fetch_page(self, page: int, sort_by: str) -> Optional[Dict]:
        """
        获取单页数据

        Args:
            page: 页码
            sort_by: 排序方式

        Returns:
            API 响应数据
        """
        query = f"topic:{self.topic}"
        url = f"{self.api_base}/search/repositories"

        params = {
            "q": query,
            "sort": sort_by,
            "order": GITHUB_SEARCH_ORDER,
            "per_page": self.per_page,
            "page": page
        }

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print(f"   ⚠️ 请求失败 (页 {page}): {e}")
            return None

    def _parse_repo_item(self, item: Dict, rank: int) -> Dict:
        """
        解析仓库数据

        Args:
            item: GitHub API 返回的仓库项
            rank: 排名

        Returns:
            仓库信息字典
        """
        owner_data = item.get("owner") or {}
        owner = owner_data.get("login", "")
        name = item.get("name", "")
        repo_name = f"{owner}/{name}"

        return {
            "rank": rank,
            "repo_name": repo_name,
            "owner": owner,
            "name": name,
            "stars": item.get("stargazers_count", 0),
            "forks": item.get("forks_count", 0),
            "issues": item.get("open_issues_count", 0),
            "language": item.get("language", ""),
            "url": item.get("html_url", ""),
            "description": item.get("description", ""),
            "topics": item.get("topics", []),
            "created_at": item.get("created_at", ""),
            "updated_at": item.get("updated_at", ""),
            "pushed_at": item.get("pushed_at", ""),
            "homepage": item.get("homepage", ""),
            "archived": item.get("archived", False),
        }

    def _update_rate_limit(self, response_data: Dict):
        """
        更新速率限制信息

        Args:
            response_data: API 响应数据
        """
        # 注意：这些信息在实际请求中从响应头获取
        # 这里只是一个简化版本
        pass

    def _wait_for_rate_limit(self):
        """等待速率限制重置"""
        if self.rate_limit_reset:
            now = int(time.time())
            wait_time = self.rate_limit_reset - now + 1

            if wait_time > 0:
                print(f"⏳ 速率限制已用尽，等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)

    def fetch_new_repos(self, days: int = 7) -> List[Dict]:
        """
        获取最近创建的仓库

        Args:
            days: 最近多少天

        Returns:
            仓库列表
        """
        cutoff_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        query = f"topic:{self.topic} created:>{cutoff_date}"

        print(f"📡 正在获取最近 {days} 天创建的仓库...")

        repos = []
        page = 1

        while page <= self.max_pages:
            url = f"{self.api_base}/search/repositories"
            params = {
                "q": query,
                "sort": "stars",
                "order": "desc",
                "per_page": self.per_page,
                "page": page
            }

            try:
                response = self.session.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()

                if not data or "items" not in data:
                    break

                items = data["items"]
                if not items:
                    break

                for item in items:
                    repo = self._parse_repo_item(item, len(repos) + 1)
                    repos.append(repo)

                print(f"   第 {page} 页: 获取 {len(items)} 个仓库")

                if len(items) < self.per_page:
                    break

                page += 1
                time.sleep(self.delay)

            except requests.RequestException as e:
                print(f"   ⚠️ 请求失败: {e}")
                break

        print(f"✅ 获取到 {len(repos)} 个新仓库")
        return repos

    def fetch_repo_details(self, owner: str, repo: str) -> Optional[Dict]:
        """
        获取单个仓库的详细信息

        Args:
            owner: 仓库拥有者
            repo: 仓库名称

        Returns:
            仓库详细信息
        """
        url = f"{self.api_base}/repos/{owner}/{repo}"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            return response.json()

        except requests.RequestException as e:
            print(f"   ⚠️ 获取仓库详情失败 {owner}/{repo}: {e}")
            return None


def fetch_repos(sort_by: str = "stars", limit: int = 100) -> List[Dict]:
    """便捷函数：获取仓库列表"""
    fetcher = GitHubFetcher()
    return fetcher.fetch(sort_by=sort_by, limit=limit)
