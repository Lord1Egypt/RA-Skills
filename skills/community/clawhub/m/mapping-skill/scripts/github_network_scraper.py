"""
GitHub 社交网络爬虫模板

通过 GitHub API 遍历目标用户的 Following/Followers 关系图，
提取研究者的联系方式和社交链接。

实战案例: 从 AmandaXu97 的 Following 列表中提取 926 名用户的详细信息

三层数据拼装:
1. GitHub API Profile: name, bio, email, company, location, blog, twitter
2. Social Accounts API: 用户设置的社交链接 (较新的端点)
3. Profile README: 同名仓库的 README.md 中提取 Scholar/LinkedIn/知乎 等链接

依赖:
    pip install requests pandas openpyxl

使用示例:
    from github_network_scraper import GitHubNetworkScraper

    scraper = GitHubNetworkScraper(token="ghp_xxx")
    users = scraper.scrape_following("AmandaXu97")
    scraper.save_to_excel(users, "output.xlsx")
"""

import re
import time
import requests
from typing import List, Dict, Optional
from dataclasses import dataclass, field, asdict


# ==================== 数据模型 ====================

@dataclass
class GitHubUserProfile:
    """GitHub 用户详细资料"""
    github_id: str = ""
    name: str = ""
    github_url: str = ""
    company: str = ""
    bio: str = ""
    location: str = ""
    email: str = ""
    blog: str = ""
    twitter: str = ""
    google_scholar: str = ""
    linkedin: str = ""
    zhihu: str = ""
    bilibili: str = ""
    readme_snippet: str = ""

    def to_dict(self) -> Dict:
        return asdict(self)


# ==================== 链接提取正则 ====================

# 从 README 或 bio 文本中提取社交链接的正则表达式
LINK_PATTERNS = {
    'google_scholar': re.compile(
        r'(https?://scholar\.google\.[\w.]+/citations\?user=[\w-]+)', re.IGNORECASE
    ),
    'linkedin': re.compile(
        r'(https?://(?:www\.)?linkedin\.com/in/[\w\-%]+)', re.IGNORECASE
    ),
    'zhihu': re.compile(
        r'(https?://(?:www\.)?zhihu\.com/people/[\w\-%]+)', re.IGNORECASE
    ),
    'bilibili': re.compile(
        r'(https?://space\.bilibili\.com/\d+)', re.IGNORECASE
    ),
}


# ==================== 爬虫类 ====================

class GitHubNetworkScraper:
    """
    GitHub 社交网络爬虫

    通过 GitHub REST API 遍历用户的 Following/Followers，
    结合 Profile README 提取完整的联系方式。

    API 端点:
    - GET /users/{user}/following  — 关注列表 (分页, 100/页)
    - GET /users/{user}/followers  — 粉丝列表 (分页, 100/页)
    - GET /users/{user}            — 用户基础信息
    - GET /users/{user}/social_accounts — 社交链接 (较新端点)
    - raw.githubusercontent.com/{user}/{user}/{branch}/README.md — Profile README

    速率限制:
    - 有 Token: 5,000 请求/小时
    - 无 Token: 60 请求/小时
    - 每个用户需要 ~3 次 API 调用 (profile + social + README)
    - 926 用户 ≈ 2,778 次调用，约需 30-40 分钟
    """

    API_BASE = "https://api.github.com"
    RAW_BASE = "https://raw.githubusercontent.com"

    def __init__(self, token: str):
        """
        初始化爬虫

        Args:
            token: GitHub Personal Access Token (必需，否则速率限制太低)
                   创建: https://github.com/settings/tokens
                   所需权限: 无需特殊权限 (public_repo 即可)
        """
        if not token:
            raise ValueError("GitHub Token 是必需的 (无 Token 限制 60 请求/小时)")

        self.headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json"
        }
        self._check_rate_limit()

    def _check_rate_limit(self):
        """检查当前 API 速率限制状态"""
        resp = requests.get(f"{self.API_BASE}/rate_limit", headers=self.headers)
        if resp.status_code == 200:
            limit = resp.json()['resources']['core']
            print(f"GitHub API 速率限制: {limit['remaining']}/{limit['limit']} (重置于 {limit['reset']})")
        else:
            print(f"⚠️ 无法检查速率限制: {resp.status_code}")

    def get_following(self, username: str) -> List[Dict]:
        """
        获取目标用户的关注列表

        GitHub API 分页: 每页最多 100 条，需要循环获取

        Args:
            username: GitHub 用户名

        Returns:
            用户基础信息列表 [{login, id, avatar_url, ...}]
        """
        users = []
        page = 1
        print(f"正在获取 {username} 的关注列表...")

        while True:
            url = f"{self.API_BASE}/users/{username}/following?per_page=100&page={page}"
            resp = requests.get(url, headers=self.headers)

            if resp.status_code != 200:
                print(f"❌ 获取失败: {resp.status_code} - {resp.text[:100]}")
                break

            data = resp.json()
            if not data:
                break

            users.extend(data)
            print(f"  已获取第 {page} 页，累计: {len(users)} 人")
            page += 1

        return users

    def get_followers(self, username: str) -> List[Dict]:
        """获取目标用户的粉丝列表 (同 get_following 逻辑)"""
        users = []
        page = 1
        print(f"正在获取 {username} 的粉丝列表...")

        while True:
            url = f"{self.API_BASE}/users/{username}/followers?per_page=100&page={page}"
            resp = requests.get(url, headers=self.headers)

            if resp.status_code != 200:
                break

            data = resp.json()
            if not data:
                break

            users.extend(data)
            print(f"  已获取第 {page} 页，累计: {len(users)} 人")
            page += 1

        return users

    def get_user_detail(self, username: str) -> GitHubUserProfile:
        """
        获取单个用户的完整信息 (三层数据拼装)

        Layer 1: GitHub API Profile (bio, email, company, blog, twitter)
        Layer 2: Social Accounts API (专用社交链接端点)
        Layer 3: Profile README (同名仓库的 README.md)

        Args:
            username: GitHub 用户名

        Returns:
            GitHubUserProfile 对象
        """
        profile = GitHubUserProfile(github_id=username)

        # ---- Layer 1: 基础 Profile ----
        resp = requests.get(f"{self.API_BASE}/users/{username}", headers=self.headers)
        if resp.status_code != 200:
            return profile

        data = resp.json()
        profile.name = data.get('name') or ''
        profile.github_url = data.get('html_url') or ''
        profile.company = data.get('company') or ''
        profile.bio = data.get('bio') or ''
        profile.location = data.get('location') or ''
        profile.email = data.get('email') or ''
        profile.blog = data.get('blog') or ''
        if data.get('twitter_username'):
            profile.twitter = f"https://twitter.com/{data['twitter_username']}"

        # ---- Layer 2: Social Accounts API ----
        social_resp = requests.get(
            f"{self.API_BASE}/users/{username}/social_accounts",
            headers=self.headers
        )
        social_urls = []
        if social_resp.status_code == 200:
            for s in social_resp.json():
                url = s.get('url', '')
                social_urls.append(url)
                # 直接匹配已知平台
                self._match_social_url(profile, url)

        # ---- Layer 3: Profile README ----
        readme_text = self._get_profile_readme(username)
        if readme_text:
            profile.readme_snippet = readme_text[:200].replace('\n', ' ')

        # ---- 合并搜索：从所有文本中提取链接 ----
        full_text = ' '.join([
            profile.bio or '',
            readme_text or '',
            ' '.join(social_urls)
        ])
        self._extract_links_from_text(profile, full_text)

        return profile

    def _get_profile_readme(self, username: str) -> str:
        """
        获取用户同名仓库的 README.md

        GitHub 的 Profile README 机制: 用户创建与自己同名的仓库，
        其 README.md 会显示在 Profile 页面。很多研究者在此放置
        Scholar、LinkedIn、个人主页等链接。

        尝试 main 和 master 两个分支名。
        """
        for branch in ["main", "master"]:
            url = f"{self.RAW_BASE}/{username}/{username}/{branch}/README.md"
            try:
                resp = requests.get(url, timeout=5)
                if resp.status_code == 200:
                    return resp.text
            except Exception:
                pass
        return ""

    def _match_social_url(self, profile: GitHubUserProfile, url: str):
        """将已知的社交链接直接赋值到 profile"""
        url_lower = url.lower()
        if 'scholar.google' in url_lower and not profile.google_scholar:
            profile.google_scholar = url
        elif 'linkedin.com' in url_lower and not profile.linkedin:
            profile.linkedin = url
        elif 'zhihu.com' in url_lower and not profile.zhihu:
            profile.zhihu = url
        elif 'bilibili.com' in url_lower and not profile.bilibili:
            profile.bilibili = url

    def _extract_links_from_text(self, profile: GitHubUserProfile, text: str):
        """从合并文本中用正则提取社交链接 (仅填充尚未赋值的字段)"""
        if not text:
            return

        for field_name, pattern in LINK_PATTERNS.items():
            if not getattr(profile, field_name):
                match = pattern.search(text)
                if match:
                    setattr(profile, field_name, match.group(1))

    def scrape_following(
        self,
        username: str,
        max_users: Optional[int] = None
    ) -> List[GitHubUserProfile]:
        """
        爬取目标用户的 Following 列表中所有用户的详细信息

        Args:
            username: 目标 GitHub 用户名
            max_users: 限制处理数量 (调试用)

        Returns:
            GitHubUserProfile 列表
        """
        following = self.get_following(username)
        total = len(following)
        print(f"\n共找到 {total} 个关注账号")

        if max_users:
            following = following[:max_users]
            print(f"⚠️ 调试模式：只处理前 {max_users} 个")

        results = []
        for i, user in enumerate(following):
            login = user['login']
            if i % 10 == 0:
                print(f"  处理进度: {i}/{len(following)} ({login})")

            detail = self.get_user_detail(login)
            results.append(detail)

        self._print_stats(results)
        return results

    def scrape_followers(
        self,
        username: str,
        max_users: Optional[int] = None
    ) -> List[GitHubUserProfile]:
        """爬取目标用户的 Followers 列表 (同 scrape_following 逻辑)"""
        followers = self.get_followers(username)
        total = len(followers)
        print(f"\n共找到 {total} 个粉丝")

        if max_users:
            followers = followers[:max_users]

        results = []
        for i, user in enumerate(followers):
            login = user['login']
            if i % 10 == 0:
                print(f"  处理进度: {i}/{len(followers)} ({login})")

            detail = self.get_user_detail(login)
            results.append(detail)

        self._print_stats(results)
        return results

    def _print_stats(self, results: List[GitHubUserProfile]):
        """打印统计信息"""
        total = len(results)
        if total == 0:
            return

        has_email = sum(1 for r in results if r.email)
        has_scholar = sum(1 for r in results if r.google_scholar)
        has_linkedin = sum(1 for r in results if r.linkedin)
        has_blog = sum(1 for r in results if r.blog)
        has_bio = sum(1 for r in results if r.bio)

        print(f"\n{'='*50}")
        print(f"爬取完成: {total} 个用户")
        print(f"{'='*50}")
        print(f"有邮箱: {has_email} ({has_email*100//total}%)")
        print(f"有 Scholar: {has_scholar} ({has_scholar*100//total}%)")
        print(f"有 LinkedIn: {has_linkedin} ({has_linkedin*100//total}%)")
        print(f"有 Blog: {has_blog} ({has_blog*100//total}%)")
        print(f"有 Bio: {has_bio} ({has_bio*100//total}%)")
        print(f"{'='*50}")

    def save_to_excel(self, results: List[GitHubUserProfile], filename: str):
        """保存到 Excel 文件"""
        import pandas as pd

        if not results:
            print("没有数据可保存。")
            return

        df = pd.DataFrame([r.to_dict() for r in results])

        # 列重排: 重要字段在前
        priority_cols = [
            'github_id', 'name', 'company', 'email',
            'google_scholar', 'linkedin', 'zhihu', 'bilibili',
            'bio', 'blog', 'github_url', 'readme_snippet'
        ]
        existing = [c for c in priority_cols if c in df.columns]
        remaining = [c for c in df.columns if c not in priority_cols]
        df = df[existing + remaining]

        df.to_excel(filename, index=False)
        print(f"✅ 已保存到: {filename}")

    def save_to_csv(self, results: List[GitHubUserProfile], filename: str):
        """保存到 CSV 文件 (Excel 兼容)"""
        import pandas as pd

        if not results:
            return

        df = pd.DataFrame([r.to_dict() for r in results])
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"✅ 已保存到: {filename}")


# ==================== 命令行入口 ====================

if __name__ == "__main__":
    import os

    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    token = os.getenv("GITHUB_TOKEN", "")
    if not token:
        print("请设置环境变量 GITHUB_TOKEN")
        print("创建 Token: https://github.com/settings/tokens")
        exit(1)

    scraper = GitHubNetworkScraper(token=token)

    # 调试模式: 只处理前 10 个用户
    results = scraper.scrape_following("AmandaXu97", max_users=10)
    scraper.save_to_excel(results, "github_following_test.xlsx")

    # 全量模式 (注释掉上面两行，启用下面):
    # results = scraper.scrape_following("AmandaXu97")
    # scraper.save_to_excel(results, "AmandaXu97_following.xlsx")
