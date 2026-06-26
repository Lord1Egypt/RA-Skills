"""
OpenReview 会议论文爬虫模板

从 OpenReview 平台爬取会议论文和作者信息，支持华人作者识别。
基于 ICML 2025 实战代码 (3,257 篇论文, 8,221 条华人作者记录, 11min29s)。

依赖:
    pip install openreview-py pandas tqdm

使用示例:
    from openreview_scraper import OpenReviewScraper

    scraper = OpenReviewScraper(username, password)
    scraper.scrape_conference('ICML.cc/2025/Conference')
    scraper.save_to_csv('icml2025_chinese.csv')
"""

import time
from typing import List, Dict, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from tqdm import tqdm

try:
    import openreview
    import openreview.api
except ImportError:
    raise ImportError("请安装 openreview-py: pip install openreview-py")


# ==================== 数据模型 ====================

@dataclass
class AuthorInfo:
    """作者信息"""
    paper_title: str = ""
    paper_link: str = ""
    author_name: str = ""
    author_id: str = ""
    email: str = ""
    homepage: str = ""
    google_scholar: str = ""
    dblp: str = ""
    orcid: str = ""
    github: str = ""
    linkedin: str = ""
    profile_link: str = ""
    is_chinese: bool = False
    chinese_confidence: float = 0.0


# ==================== 华人姓氏数据库 ====================

CHINESE_SURNAMES: Set[str] = {
    # Top 20
    'li', 'wang', 'zhang', 'liu', 'chen', 'yang', 'huang', 'zhao', 'wu', 'zhou',
    'xu', 'sun', 'ma', 'zhu', 'hu', 'guo', 'he', 'gao', 'lin', 'luo',
    # 21-40
    'cheng', 'zheng', 'xie', 'tang', 'deng', 'feng', 'han', 'cao', 'zeng', 'peng',
    'xiao', 'cai', 'pan', 'tian', 'dong', 'yuan', 'jiang', 'ye', 'wei', 'su',
    # 41-70
    'lu', 'ding', 'ren', 'tan', 'jia', 'liao', 'yao', 'xiong', 'jin', 'wan',
    'xia', 'fu', 'fang', 'bai', 'zou', 'meng', 'qin', 'qiu', 'hou',
    'shi', 'xue', 'mu', 'gu', 'du', 'qian', 'song', 'dai', 'fan',
    # 港台拼音变体
    'tsai', 'chang', 'chien', 'chung', 'hsu', 'hsieh', 'liang',
    'wong', 'chan', 'cheung', 'leung', 'kwong', 'tse', 'ng',
}


# ==================== OpenReview 爬虫类 ====================

class OpenReviewScraper:
    """
    OpenReview 会议论文爬虫

    基于 ICML 2025 实战验证，支持：
    - 获取会议全部论文
    - 提取作者 Profile 链接（Email, Homepage, Scholar, DBLP, ORCID, GitHub, LinkedIn）
    - 华人作者识别（姓氏匹配）
    - 作者 Profile 缓存（避免重复 API 调用）
    """

    VENUE_IDS = {
        'ICML 2025': 'ICML.cc/2025/Conference',
        'ICML 2024': 'ICML.cc/2024/Conference',
        'NeurIPS 2024': 'NeurIPS.cc/2024/Conference',
        'NeurIPS 2023': 'NeurIPS.cc/2023/Conference',
        'ICLR 2025': 'ICLR.cc/2025/Conference',
        'ICLR 2024': 'ICLR.cc/2024/Conference',
    }

    def __init__(self, username: str, password: str, baseurl: str = 'https://api2.openreview.net'):
        """
        初始化爬虫

        Args:
            username: OpenReview 注册邮箱
            password: OpenReview 密码
            baseurl: API 地址 (必须用 api2.openreview.net)
        """
        print("正在登录 OpenReview...")
        try:
            self.client = openreview.api.OpenReviewClient(
                baseurl=baseurl,
                username=username,
                password=password
            )
            print("✅ 登录成功！")
        except Exception as e:
            print(f"❌ 登录失败: {e}")
            raise

        self.results: List[AuthorInfo] = []
        self._profile_cache: Dict[str, Optional[Dict]] = {}

    def get_all_papers(self, venue_id: str) -> List:
        """
        获取会议所有论文

        Args:
            venue_id: 会议 ID (如 'ICML.cc/2025/Conference')

        Returns:
            论文 Note 对象列表
        """
        print(f"正在获取 {venue_id} 的所有论文 (可能需要 1-2 分钟)...")
        submissions = self.client.get_all_notes(content={'venueid': venue_id})
        print(f"✅ 共获取到 {len(submissions)} 篇论文")
        return submissions

    def is_chinese_author(self, name: str) -> Tuple[bool, float]:
        """
        判断是否为华人作者（简单姓氏匹配法）

        实测 ICML 2025: 3,257 篇论文中识别出 8,221 条华人作者记录

        Args:
            name: 英文姓名 (如 "San Zhang")

        Returns:
            (is_chinese, confidence) 元组
        """
        if not name:
            return False, 0.0

        parts = name.strip().lower().split()
        if len(parts) < 2:
            return False, 0.0

        # 假设姓在最后（英文格式：FirstName LastName）
        last_name = parts[-1]
        if last_name in CHINESE_SURNAMES:
            return True, 0.8
        return False, 0.0

    def extract_profile_links(self, profile) -> Dict[str, str]:
        """
        从 OpenReview Profile 对象提取各种链接

        关键踩坑点：
        1. email: preferredEmail 可能为空，需要回退到 emails 列表
        2. google_scholar: 字段名不统一，可能叫 gscholar 或 google_scholar
        3. orcid: 有时只存 ID，需要拼接完整 URL

        Args:
            profile: OpenReview Profile 对象

        Returns:
            链接信息字典
        """
        data = {
            'email': '',
            'homepage': '',
            'google_scholar': '',
            'dblp': '',
            'orcid': '',
            'github': '',
            'linkedin': '',
            'profile_link': ''
        }

        if not profile or not hasattr(profile, 'content'):
            return data

        content = profile.content

        # ---- 邮箱提取（三级回退） ----
        preferred = content.get('preferredEmail', '')
        emails = content.get('emails', [])
        if preferred:
            data['email'] = preferred
        elif emails:
            data['email'] = emails[0]
        else:
            data['email'] = 'Hidden'

        # ---- 个人主页 ----
        data['homepage'] = content.get('homepage', '')

        # ---- Google Scholar (字段名不统一！) ----
        data['google_scholar'] = (
            content.get('gscholar', '') or content.get('google_scholar', '')
        )

        # ---- DBLP ----
        data['dblp'] = content.get('dblp', '')

        # ---- ORCID (可能只有 ID，需要拼 URL) ----
        orcid = content.get('orcid', '')
        if orcid and 'http' not in orcid:
            data['orcid'] = f"https://orcid.org/{orcid}"
        else:
            data['orcid'] = orcid

        # ---- GitHub & LinkedIn ----
        data['github'] = content.get('github', '')
        data['linkedin'] = content.get('linkedin', '')

        # ---- Profile 链接 ----
        if hasattr(profile, 'id'):
            data['profile_link'] = f"https://openreview.net/profile?id={profile.id}"

        return data

    def _get_cached_profile(self, author_id: str) -> Optional[Dict]:
        """获取作者 Profile（带缓存）"""
        if author_id in self._profile_cache:
            return self._profile_cache[author_id]

        try:
            profile = self.client.get_profile(author_id)
            links = self.extract_profile_links(profile)
            self._profile_cache[author_id] = links
            return links
        except Exception:
            self._profile_cache[author_id] = None
            return None

    def scrape_conference(
        self,
        venue_id: str,
        chinese_only: bool = True,
        delay: float = 0.0,
        max_papers: Optional[int] = None,
        use_cache: bool = True
    ) -> List[AuthorInfo]:
        """
        爬取会议论文和作者信息

        Args:
            venue_id: 会议 Venue ID (如 'ICML.cc/2025/Conference')
            chinese_only: 是否只提取华人作者 (默认 True)
            delay: 每次 Profile 查询后的延迟秒数 (默认 0，实测不加也能跑通)
            max_papers: 限制论文数量 (用于调试，如 50)
            use_cache: 是否启用作者 Profile 缓存 (默认 True)

        Returns:
            AuthorInfo 列表
        """
        papers = self.get_all_papers(venue_id)
        if max_papers:
            papers = papers[:max_papers]
            print(f"⚠️ 调试模式：只处理前 {max_papers} 篇论文")

        self.results = []
        if not use_cache:
            self._profile_cache = {}

        print("开始遍历论文并爬取作者 Profile...")

        for note in tqdm(papers, desc="处理论文"):
            try:
                title = note.content.get('title', {}).get('value', '')
                authors = note.content.get('authors', {}).get('value', [])
                author_ids = note.content.get('authorids', {}).get('value', [])
                paper_link = f"https://openreview.net/forum?id={note.id}"

                # 对齐作者和 ID（有时长度不一致）
                if len(authors) != len(author_ids):
                    author_ids = author_ids + [''] * (len(authors) - len(author_ids))

                for name, uid in zip(authors, author_ids):
                    # 1. 华人筛选
                    is_chinese, confidence = self.is_chinese_author(name)
                    if chinese_only and not is_chinese:
                        continue

                    author_info = AuthorInfo(
                        paper_title=title,
                        paper_link=paper_link,
                        author_name=name,
                        author_id=uid,
                        is_chinese=is_chinese,
                        chinese_confidence=confidence
                    )

                    # 2. Email ID → 直接用作邮箱，跳过 Profile 查询
                    if '@' in uid:
                        author_info.email = uid
                        author_info.profile_link = 'N/A (Email User)'
                        self.results.append(author_info)
                        continue

                    # 3. Profile ID → 查询 Profile 获取详情
                    if uid:
                        if use_cache:
                            links = self._get_cached_profile(uid)
                        else:
                            try:
                                profile = self.client.get_profile(uid)
                                links = self.extract_profile_links(profile)
                            except Exception:
                                links = None

                        if links:
                            for k, v in links.items():
                                if hasattr(author_info, k) and v:
                                    setattr(author_info, k, v)
                        else:
                            author_info.email = 'Error Fetching Profile'
                            author_info.profile_link = f"https://openreview.net/profile?id={uid}"

                    self.results.append(author_info)

                    if delay > 0:
                        time.sleep(delay)

            except Exception:
                continue

        self._print_stats()
        return self.results

    def _print_stats(self):
        """打印爬取统计信息"""
        if not self.results:
            print("没有找到符合条件的数据。")
            return

        total = len(self.results)
        has_email = sum(1 for r in self.results if r.email and r.email not in ('Hidden', 'Error Fetching Profile'))
        has_homepage = sum(1 for r in self.results if r.homepage)
        has_scholar = sum(1 for r in self.results if r.google_scholar)
        has_github = sum(1 for r in self.results if r.github)
        has_dblp = sum(1 for r in self.results if r.dblp)

        print(f"\n{'='*50}")
        print(f"爬取完成")
        print(f"{'='*50}")
        print(f"总计华人作者记录: {total} 条")
        print(f"包含 Email: {has_email} ({has_email*100//total}%)")
        print(f"包含 Homepage: {has_homepage} ({has_homepage*100//total}%)")
        print(f"包含 Google Scholar: {has_scholar} ({has_scholar*100//total}%)")
        print(f"包含 GitHub: {has_github} ({has_github*100//total}%)")
        print(f"包含 DBLP: {has_dblp} ({has_dblp*100//total}%)")
        print(f"Profile 缓存命中: {len(self._profile_cache)} 位唯一作者")
        print(f"{'='*50}")

    def save_to_csv(self, filename: str):
        """
        保存结果到 CSV

        Args:
            filename: 输出文件路径
        """
        import pandas as pd
        if not self.results:
            print("没有数据可保存。")
            return

        df = pd.DataFrame([asdict(r) for r in self.results])
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

    username = os.getenv("OPENREVIEW_USER", "")
    password = os.getenv("OPENREVIEW_PASSWORD", "")

    if not username or not password:
        print("请设置环境变量 OPENREVIEW_USER 和 OPENREVIEW_PASSWORD")
        print("或创建 .env 文件:")
        print("  OPENREVIEW_USER=your_email@example.com")
        print("  OPENREVIEW_PASSWORD=your_password")
        exit(1)

    scraper = OpenReviewScraper(username, password)

    # 调试模式: 只处理 50 篇论文
    scraper.scrape_conference('ICML.cc/2025/Conference', max_papers=50)
    scraper.save_to_csv('icml2025_test.csv')

    # 全量模式 (注释掉上面两行，启用下面):
    # scraper.scrape_conference('ICML.cc/2025/Conference')
    # scraper.save_to_csv('ICML2025_Chinese_Authors.csv')
