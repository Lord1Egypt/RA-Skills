"""
CVF Open Access 会议论文爬虫模板

从 CVF 官方网站 (openaccess.thecvf.com) 爬取会议论文元数据，
并深入 PDF 内部提取作者的真实邮箱和机构信息。

基于 CVPR 2025 实战代码 (2,871 篇论文全量爬取, 耗时约 85 分钟)。

适用会议: CVPR, ICCV, WACV 等所有在 thecvf.com 上发布的会议。

依赖:
    pip install requests beautifulsoup4 PyMuPDF pandas tqdm

    ⚠️ 关键陷阱: 必须安装 PyMuPDF，不要安装 fitz!
    PyPI 上有一个废弃的同名山寨包 `fitz` (版本 0.0.1dev2)，
    会导致 `ModuleNotFoundError: No module named 'tools'`。
    如果误装了，需要:
        pip uninstall -y fitz PyMuPDF && pip install PyMuPDF

使用示例:
    from cvf_paper_scraper import CVFPaperScraper

    scraper = CVFPaperScraper()
    scraper.scrape_conference('CVPR2025')
    scraper.save_to_csv('cvpr2025_papers.csv')
"""

import re
import io
import time
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, field, asdict
from urllib.parse import urljoin

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    raise ImportError("请安装依赖: pip install requests beautifulsoup4")

try:
    import fitz  # PyMuPDF — 导入名是 fitz，但安装包是 PyMuPDF
except ImportError:
    raise ImportError(
        "请安装 PyMuPDF: pip install PyMuPDF\n"
        "⚠️ 不要 pip install fitz (那是个废弃的山寨包)!"
    )


# ==================== 数据模型 ====================

@dataclass
class PaperInfo:
    """论文及其作者联系信息"""
    paper_title: str = ""
    authors: str = ""          # 逗号分隔的作者列表
    paper_link: str = ""       # 论文详情页链接
    pdf_link: str = ""         # PDF 下载链接
    emails: str = ""           # 从 PDF 中提取的邮箱 (逗号分隔)
    institutions: str = ""     # 从邮箱域名推断的机构 (逗号分隔)
    extraction_status: str = ""  # 提取状态: success / not_found / error


# ==================== 邮箱提取引擎 ====================

# 标准邮箱正则
EMAIL_REGEX_STD = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')

# 花括号缩写邮箱正则
# 匹配: {user1, user2}@domain.com  以及  {user1@ece., user2@}domain.edu
EMAIL_REGEX_BRACKET = re.compile(
    r'\{([^}]+)\}\s*@?\s*([a-zA-Z0-9.-]*\.[a-zA-Z]{2,})'
)

# 邮箱最终验证正则
EMAIL_VALIDATE = re.compile(r'^[^@]+@[^@]+\.[^@]+$')


def extract_emails_from_text(text: str) -> List[str]:
    """
    从文本中提取所有邮箱地址 (双策略)

    策略 1: 标准邮箱匹配 (如 user@domain.edu)
    策略 2: 花括号缩写解析 (如 {user1@ece., user2}ucr.edu)

    这是 CVPR 2025 实战中最核心的技术突破 —— CS 论文中极其常见的
    LaTeX 排版宏包会将多个作者邮箱缩写为花括号格式。

    Args:
        text: PDF 首页提取的纯文本 (已去除换行符)

    Returns:
        去重后的邮箱列表 (全小写)
    """
    extracted = []

    # === 策略 1: 标准邮箱 ===
    std_emails = EMAIL_REGEX_STD.findall(text)
    extracted.extend(std_emails)

    # === 策略 2: 花括号缩写邮箱 ===
    bracket_matches = EMAIL_REGEX_BRACKET.findall(text)

    for inside_text, domain_suffix in bracket_matches:
        users = inside_text.split(',')
        for user in users:
            # 清洗: 去除 LaTeX 角标符号 (*, †, ‡) 和空格
            user = re.sub(r'[^a-zA-Z0-9_.@+-]', '', user)
            clean_suffix = re.sub(r'[^a-zA-Z0-9_.@+-]', '', domain_suffix)

            if not user:
                continue

            # === 智能拼接逻辑 ===
            # Case 1: user 自带 @ (如 "bguler@ece.")
            #   → 直接拼接后缀 → "bguler@ece.ucr.edu"
            if '@' in user:
                email = user + clean_suffix
            # Case 2: suffix 自带 @ (极罕见)
            elif '@' in clean_suffix:
                email = user + clean_suffix
            # Case 3: 普通情况，两者之间加 @
            else:
                email = user + '@' + clean_suffix

            # 修复双点错误: user@.edu → user@edu
            email = email.replace('@.', '@')

            # 最终合法性验证
            if EMAIL_VALIDATE.match(email):
                extracted.append(email)

    # 去重 + 全小写
    return list(set(e.lower() for e in extracted))


def infer_institutions(emails: List[str]) -> List[str]:
    """
    从邮箱域名推断学术机构

    只保留包含 .edu 或 .ac 的域名 (学术机构)

    Args:
        emails: 邮箱列表

    Returns:
        去重后的学术机构域名列表
    """
    institutions = set()
    for email in emails:
        domain = email.split('@')[-1]
        if '.edu' in domain or '.ac' in domain:
            institutions.add(domain)
    return list(institutions)


# ==================== CVF 爬虫类 ====================

class CVFPaperScraper:
    """
    CVF Open Access 会议论文爬虫

    基于 CVPR 2025 实战验证，支持:
    - 从 thecvf.com 爬取会议全部论文元数据
    - 下载 PDF 到内存流 (无需落盘) 提取首页文本
    - 双策略邮箱提取 (标准 + 花括号缩写)
    - 从邮箱域名推断作者机构

    支持的会议 (所有在 thecvf.com 上发布的):
    - CVPR (2013-2025+)
    - ICCV (2013-2025+)
    - WACV (2020-2025+)
    """

    BASE_URL = "https://openaccess.thecvf.com"

    # 常用会议 URL 路径
    CONFERENCE_PATHS = {
        # CVPR
        'CVPR2025': '/CVPR2025?day=all',
        'CVPR2024': '/CVPR2024?day=all',
        'CVPR2023': '/CVPR2023?day=all',
        # ICCV
        'ICCV2023': '/ICCV2023?day=all',
        'ICCV2021': '/ICCV2021?day=all',
        # WACV
        'WACV2025': '/WACV2025',
        'WACV2024': '/WACV2024',
    }

    def __init__(self, base_url: str = "https://openaccess.thecvf.com"):
        """
        初始化爬虫

        Args:
            base_url: CVF 网站根 URL (通常不需要修改)
        """
        self.base_url = base_url.rstrip('/')
        self.results: List[PaperInfo] = []
        self._session = requests.Session()
        self._session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36'
        })

    def get_paper_metadata(self, conference_path: str) -> List[Dict]:
        """
        第一阶段: 从 CVF 网页提取论文元数据

        CVF 网页是纯静态 HTML，结构为:
            <dt class="ptitle"><a href="...">论文标题</a></dt>
            <dd><a>作者1</a>, <a>作者2</a></dd>     ← 兄弟节点
            <dd><a>pdf</a> <a>supp</a></dd>          ← 再下一个兄弟

        核心技巧: BeautifulSoup 兄弟节点漫游法 (find_next_sibling)

        Args:
            conference_path: 会议页面路径 (如 '/CVPR2025?day=all')

        Returns:
            论文元数据字典列表
        """
        url = f"{self.base_url}{conference_path}"
        print(f"正在访问 CVF 网页: {url}")

        try:
            response = self._session.get(url, timeout=15)
            response.raise_for_status()
        except Exception as e:
            print(f"网页请求失败: {e}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')

        # 定位所有论文标题节点
        paper_nodes = soup.find_all('dt', class_='ptitle')
        print(f"网页解析成功! 共发现 {len(paper_nodes)} 篇论文。")

        papers = []

        for dt in paper_nodes:
            try:
                # 标题
                title = dt.text.strip()
                paper_a = dt.find('a')
                paper_rel_link = paper_a['href'] if paper_a else ''
                paper_link = urljoin(self.base_url + '/', paper_rel_link)

                # 作者 (标题节点的下一个兄弟 <dd>)
                author_dd = dt.find_next_sibling('dd')
                if not author_dd:
                    continue
                authors = [a.text.strip() for a in author_dd.find_all('a') if a.text.strip()]

                # PDF 链接 (作者节点的下一个兄弟 <dd>)
                pdf_dd = author_dd.find_next_sibling('dd')
                if not pdf_dd:
                    continue
                pdf_a_tag = pdf_dd.find('a', string='pdf')
                if not pdf_a_tag:
                    continue
                pdf_rel_link = pdf_a_tag['href']
                pdf_link = urljoin(self.base_url + '/', pdf_rel_link)

                papers.append({
                    'title': title,
                    'authors': ", ".join(authors),
                    'paper_link': paper_link,
                    'pdf_link': pdf_link
                })

            except (AttributeError, KeyError):
                continue

        return papers

    def extract_info_from_pdf(self, pdf_url: str) -> Dict:
        """
        第二阶段: 下载 PDF 到内存流，提取首页邮箱和机构

        性能优化: 使用 io.BytesIO 内存流，不落盘。
        2,871 篇论文无需任何磁盘写入。

        邮箱提取双策略:
        1. 标准正则: user@domain.edu
        2. 花括号解析: {user1@sub., user2}domain.edu

        关键细节:
        - replace('\\n', ' '): PDF 换行可能截断邮箱
        - MuPDF 非致命警告 (Screen annotations) 可以忽略
        - 只解析第一页 (邮箱和机构通常在此)

        Args:
            pdf_url: PDF 下载链接

        Returns:
            {'emails': str, 'institutions': str, 'status': str}
        """
        try:
            response = self._session.get(pdf_url, timeout=20)
            response.raise_for_status()

            # 内存流处理: 不落盘，直接从 bytes 解析
            pdf_stream = io.BytesIO(response.content)
            doc = fitz.open(stream=pdf_stream, filetype="pdf")

            # 提取第一页文本，去换行防止邮箱被截断
            first_page_text = doc[0].get_text("text").replace('\n', ' ')
            doc.close()

            # 双策略邮箱提取
            emails = extract_emails_from_text(first_page_text)

            if emails:
                institutions = infer_institutions(emails)
                return {
                    'emails': ", ".join(emails),
                    'institutions': ", ".join(institutions),
                    'status': 'success'
                }
            else:
                return {
                    'emails': 'Not Found',
                    'institutions': '',
                    'status': 'not_found'
                }

        except Exception as e:
            return {
                'emails': 'PDF Parsing Error',
                'institutions': '',
                'status': 'error'
            }

    def scrape_conference(
        self,
        conference: str,
        max_papers: Optional[int] = None,
        delay: float = 1.0,
        extract_pdf: bool = True
    ) -> List[PaperInfo]:
        """
        端到端爬取会议论文

        Args:
            conference: 会议名称 (如 'CVPR2025') 或自定义路径 (如 '/CVPR2025?day=all')
            max_papers: 限制论文数量 (用于调试，如 10)
            delay: 每次 PDF 请求后的延迟秒数 (默认 1.0，礼貌爬虫)
            extract_pdf: 是否解析 PDF 提取邮箱 (关闭则仅获取元数据)

        Returns:
            PaperInfo 列表
        """
        # 解析会议路径
        if conference in self.CONFERENCE_PATHS:
            path = self.CONFERENCE_PATHS[conference]
        elif conference.startswith('/'):
            path = conference
        else:
            # 尝试推断: CVPR2025 → /CVPR2025?day=all
            path = f"/{conference}?day=all"
            print(f"未找到预定义路径，尝试: {self.base_url}{path}")

        # 第一阶段: 获取元数据
        papers = self.get_paper_metadata(path)
        if not papers:
            print("未能获取到论文数据。")
            return []

        if max_papers:
            papers = papers[:max_papers]
            print(f"调试模式: 只处理前 {max_papers} 篇论文")

        self.results = []

        # 第二阶段: PDF 解析 (可选)
        if extract_pdf:
            print("\n开始深度解析 PDF 文件提取邮箱...")
            from tqdm import tqdm

            for paper_dict in tqdm(papers, desc="解析 PDF"):
                pdf_info = self.extract_info_from_pdf(paper_dict['pdf_link'])

                info = PaperInfo(
                    paper_title=paper_dict['title'],
                    authors=paper_dict['authors'],
                    paper_link=paper_dict['paper_link'],
                    pdf_link=paper_dict['pdf_link'],
                    emails=pdf_info['emails'],
                    institutions=pdf_info['institutions'],
                    extraction_status=pdf_info['status']
                )
                self.results.append(info)

                if delay > 0:
                    time.sleep(delay)
        else:
            for paper_dict in papers:
                info = PaperInfo(
                    paper_title=paper_dict['title'],
                    authors=paper_dict['authors'],
                    paper_link=paper_dict['paper_link'],
                    pdf_link=paper_dict['pdf_link'],
                    extraction_status='skipped'
                )
                self.results.append(info)

        self._print_stats()
        return self.results

    def _print_stats(self):
        """打印爬取统计信息"""
        if not self.results:
            print("没有数据。")
            return

        total = len(self.results)
        has_email = sum(1 for r in self.results
                        if r.emails and r.emails not in ('Not Found', 'PDF Parsing Error'))
        has_institution = sum(1 for r in self.results if r.institutions)
        errors = sum(1 for r in self.results if r.extraction_status == 'error')

        print(f"\n{'='*50}")
        print(f"爬取完成")
        print(f"{'='*50}")
        print(f"论文总数: {total}")
        print(f"成功提取邮箱: {has_email} ({has_email*100//total}%)")
        print(f"推断出机构: {has_institution} ({has_institution*100//total}%)")
        print(f"PDF 解析错误: {errors} ({errors*100//total}%)")
        print(f"{'='*50}")

    def save_to_csv(self, filename: str):
        """
        保存结果到 CSV

        使用 utf-8-sig 编码 (带 BOM)，确保 Excel 打开不乱码。

        Args:
            filename: 输出文件路径
        """
        import pandas as pd
        if not self.results:
            print("没有数据可保存。")
            return

        df = pd.DataFrame([asdict(r) for r in self.results])
        df.to_csv(filename, index=False, encoding='utf-8-sig')
        print(f"已保存到: {filename}")


# ==================== 命令行入口 ====================

if __name__ == "__main__":
    scraper = CVFPaperScraper()

    # 调试模式: 只处理 10 篇
    scraper.scrape_conference('CVPR2025', max_papers=10)
    scraper.save_to_csv('cvpr2025_test.csv')

    # 全量模式 (注释掉上面，启用下面):
    # scraper.scrape_conference('CVPR2025')
    # scraper.save_to_csv('CVPR2025_Papers_Emails.csv')
