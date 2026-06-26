"""
README Fetcher - 获取仓库 README 内容
使用 GitHub API 获取仓库的 README 文件
"""
import time
import re
import requests
from typing import Dict, List, Optional

from src.config import GITHUB_TOKEN, GITHUB_API_BASE, FETCH_REQUEST_DELAY


class ReadmeFetcher:
    """获取仓库 README 内容"""

    def __init__(self, token: str = None):
        """
        初始化

        Args:
            token: GitHub Personal Access Token
        """
        self.token = token or GITHUB_TOKEN
        self.api_base = GITHUB_API_BASE
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

    def fetch_readme(self, owner: str, repo: str, html: bool = False) -> Optional[str]:
        """
        获取仓库 README 内容

        Args:
            owner: 仓库拥有者
            repo: 仓库名称
            html: 是否返回 HTML 格式

        Returns:
            README 内容
        """
        url = f"{self.api_base}/repos/{owner}/{repo}/readme"

        if html:
            self.session.headers["Accept"] = "application/vnd.github.html"

        try:
            response = self.session.get(url, timeout=30)
            response.raise_for_status()

            # GitHub 返回的是 base64 编码的内容
            data = response.json()

            if data.get("encoding") == "base64":
                import base64
                content = base64.b64decode(data.get("content", "")).decode("utf-8", errors="ignore")
                return content
            else:
                return data.get("content", "")

        except requests.RequestException as e:
            print(f"   ⚠️ 获取 README 失败 {owner}/{repo}: {e}")
            return None

    def fetch_readme_summary(self, owner: str, repo: str, max_length: int = 500) -> Optional[str]:
        """
        获取 README 摘要

        Args:
            owner: 仓库拥有者
            repo: 仓库名称
            max_length: 最大长度

        Returns:
            README 摘要文本
        """
        readme = self.fetch_readme(owner, repo)

        if not readme:
            return None

        # 移除 Markdown 标记，提取纯文本
        summary = self._extract_text_from_markdown(readme)

        # 截断到指定长度
        if len(summary) > max_length:
            summary = summary[:max_length].rsplit(" ", 1)[0] + "..."

        return summary

    def _extract_text_from_markdown(self, markdown: str) -> str:
        """
        从 Markdown 中提取纯文本

        Args:
            markdown: Markdown 内容

        Returns:
            纯文本
        """
        # 移除代码块
        markdown = re.sub(r'```.*?```', '', markdown, flags=re.DOTALL)
        markdown = re.sub(r'`.*?`', '', markdown)

        # 移除链接
        markdown = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', markdown)

        # 移除图片
        markdown = re.sub(r'!\[([^\]]*)\]\([^\)]+\)', '', markdown)

        # 移除标题标记
        markdown = re.sub(r'^#+\s+', '', markdown, flags=re.MULTILINE)

        # 移除加粗/斜体
        markdown = re.sub(r'\*\*([^*]+)\*\*', r'\1', markdown)
        markdown = re.sub(r'\*([^*]+)\*', r'\1', markdown)
        markdown = re.sub(r'__([^_]+)__', r'\1', markdown)
        markdown = re.sub(r'_([^_]+)_', r'\1', markdown)

        # 移除水平线
        markdown = re.sub(r'^---+$', '', markdown, flags=re.MULTILINE)
        markdown = re.sub(r'^\*\*\*+$', '', markdown, flags=re.MULTILINE)

        # 移除多余的空行
        lines = [line.strip() for line in markdown.split('\n')]
        lines = [line for line in lines if line]

        return ' '.join(lines)

    def batch_fetch_readmes(self, repos: List[Dict], delay: float = None) -> Dict[str, str]:
        """
        批量获取 README 内容

        Args:
            repos: 仓库列表
            delay: 请求间隔

        Returns:
            {repo_name: readme_summary} 字典
        """
        delay = delay if delay is not None else self.delay
        summaries = {}

        print(f"📥 开始批量获取 README...")

        for i, repo in enumerate(repos, 1):
            repo_name = repo.get("repo_name") or repo.get("name", "")

            if not repo_name or "/" not in repo_name:
                continue

            owner, name = repo_name.split("/", 1)

            print(f"  [{i}/{len(repos)}] {repo_name}")

            summary = self.fetch_readme_summary(owner, name)
            if summary:
                summaries[repo_name] = summary

            # 请求间隔
            if i < len(repos):
                time.sleep(delay)

        print(f"✅ 成功获取 {len(summaries)} 个 README 摘要")
        return summaries

    def fetch_from_github_raw(self, owner: str, repo: str, branch: str = "main") -> Optional[str]:
        """
        直接从 GitHub raw 内容获取 README

        Args:
            owner: 仓库拥有者
            repo: 仓库名称
            branch: 分支名

        Returns:
            README 内容
        """
        # 尝试常见的 README 文件名
        readme_names = ["README.md", "README.markdown", "README.rst", "README.txt"]

        for name in readme_names:
            url = f"https://raw.githubusercontent.com/{owner}/{repo}/{branch}/{name}"

            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    return response.text
            except requests.RequestException:
                continue

        # 尝试 master 分支
        if branch == "main":
            return self.fetch_from_github_raw(owner, repo, "master")

        return None


def fetch_readme_summary(owner: str, repo: str) -> Optional[str]:
    """便捷函数：获取 README 摘要"""
    fetcher = ReadmeFetcher()
    return fetcher.fetch_readme_summary(owner, repo)


def batch_fetch_readmes(repos: List[Dict]) -> Dict[str, str]:
    """便捷函数：批量获取 README"""
    fetcher = ReadmeFetcher()
    return fetcher.batch_fetch_readmes(repos)
