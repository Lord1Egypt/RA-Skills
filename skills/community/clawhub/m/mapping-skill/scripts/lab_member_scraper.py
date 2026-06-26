"""
实验室成员批量爬取模板

从实验室人员页面批量爬取成员信息，适用于学术实验室网站。
基于 LAMDA (南大)、TongClass (清华-北大)、PKU.AI (北大)、清华 MediaLab 实战验证。

实战案例:
- LAMDA: 108 名博士生，URL 格式 /Name/ (ASP.NET .ashx 页面)，两阶段爬取
- TongClass: 154 名成员，URL 格式 /author/Name/ (Hugo Academic)，两阶段爬取
- PKU.AI: 65 名成员，单页卡片提取 (.people-person + Cloudflare 解密)
- 清华 MediaLab: 39 名成员，邮箱反向定位法 (无固定 CSS 类名)

支持三种爬取模式:
- 两阶段模式: scrape_lab() — 列表页 → 详情页 (适用于 LAMDA 等)
- 卡片模式: scrape_card_page() — 单页卡片提取 (适用于 Hugo Academic/Wowchemy)
- 邮箱反向定位: scrape_by_email_anchor() — 通过邮箱文本节点反向查找人员容器 (适用于自定义 HTML)

依赖:
    pip install requests beautifulsoup4

使用示例:
    from lab_member_scraper import LabMemberScraper

    # 两阶段模式 (LAMDA 等)
    scraper = LabMemberScraper()
    members = scraper.scrape_lab("https://www.lamda.nju.edu.cn/CH.PhD_student.ashx")

    # 卡片模式 (PKU.AI、Hugo Academic 等)
    scraper = LabMemberScraper(base_url="https://pku.ai")
    members = scraper.scrape_card_page("https://pku.ai/people/")

    # 邮箱反向定位模式 (清华 MediaLab 等自定义 HTML)
    scraper = LabMemberScraper(base_url="https://media.au.tsinghua.edu.cn")
    members = scraper.scrape_by_email_anchor("https://media.au.tsinghua.edu.cn/Team.htm")

    for member in members:
        print(f"{member.name}: {member.email}")
"""

import re
import time
import requests
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Set
from dataclasses import dataclass, field, asdict
from urllib.parse import urljoin
import json


# ==================== 数据模型 ====================

@dataclass
class MemberProfile:
    """实验室成员资料"""
    name: str = ""           # 英文名或拼音名
    name_cn: str = ""        # 中文名
    role: str = ""           # PhD, PostDoc, Professor, etc.
    email: str = ""
    affiliation: str = ""
    research_interests: List[str] = field(default_factory=list)
    bio: str = ""            # 个人介绍
    homepage: str = ""
    google_scholar: str = ""
    github: str = ""
    linkedin: str = ""
    zhihu: str = ""
    bilibili: str = ""
    twitter: str = ""
    publications: List[str] = field(default_factory=list)
    education: List[str] = field(default_factory=list)
    source_url: str = ""

    def to_dict(self) -> Dict:
        """转换为字典"""
        return asdict(self)


# ==================== 爬虫类 ====================

class LabMemberScraper:
    """
    实验室成员爬虫

    支持多种常见的学术网站模板:
    - Hugo Academic / Wowchemy (TongClass 等)
    - Jekyll Scholar
    - 自定义 PHP/HTML/ASP.NET 页面 (LAMDA 等)

    实战踩坑总结:
    1. 列表页的导航链接会混入成员链接 → 需要中文名长度过滤 + URL 关键词排除
    2. 中国高校邮箱常用 [at] 混淆 → 需要正则匹配
    3. .edu.cn 域名常有 SSL 握手失败 → 需要异常捕获
    4. 论文列表通常在 "Publications" 标题下的 ul/ol 中
    """

    # Hugo Academic / Wowchemy 模板的 CSS 选择器
    # 用于 scrape_card_page() 单页卡片模式
    CARD_SELECTORS = ['.people-person', '.media.stream-item']
    NAME_SELECTORS = ['.portrait-title h2', 'h2', 'h3']
    ROLE_SELECTORS = ['.portrait-title h3', '.portrait-subtitle', 'p']
    LINK_SELECTORS = ['.network-icon a', '.social-links a', '.links-icon a']

    # 机构关键词 (用于从卡片文本中提取所属机构)
    INSTITUTION_KEYWORDS = [
        'PKU', 'Peking University', 'Tsinghua', 'NJU', 'ZJU', 'SJTU',
        'University', 'Institute', 'School', 'Lab', 'Center',
        '北京大学', '清华大学', '南京大学', '浙江大学', '上海交通大学',
    ]

    # 列表页中需要排除的 URL 关键词（导航链接噪声）
    EXCLUDE_URL_KEYWORDS = [
        'login', 'sign', 'admin', 'contact', 'about',
        'research', 'publication', 'project', 'avatar', 'image', 'photo',
        'MainPage', 'Pub.ashx', 'App.ashx', 'Data.ashx', 'Lib.ashx',
        'Seminar', 'Link.ashx', 'Album', 'index',
    ]

    # 已知有 SSL 问题的域名
    SSL_PROBLEM_DOMAINS = ['www.nju.edu.cn', 'www.tsinghua.edu.cn']

    def __init__(self, delay: float = 0.5, base_url: str = ""):
        """
        初始化爬虫

        Args:
            delay: 请求之间的延迟 (秒)
            base_url: 网站根 URL (用于拼接相对链接)
        """
        self.delay = delay
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })

    def scrape_lab(self, lab_url: str, max_members: Optional[int] = None) -> List[MemberProfile]:
        """
        爬取实验室成员列表（两阶段：列表页 → 详情页）

        Args:
            lab_url: 实验室人员页面 URL
            max_members: 限制爬取数量 (用于调试)

        Returns:
            成员资料列表
        """
        # 自动推断 base_url
        if not self.base_url:
            self.base_url = '/'.join(lab_url.split('/')[:3])

        print(f"正在获取成员列表: {lab_url}")

        # 阶段 1: 获取成员链接列表
        member_entries = self._get_member_entries(lab_url)
        print(f"初步提取到 {len(member_entries)} 名成员")

        if max_members:
            member_entries = member_entries[:max_members]
            print(f"⚠️ 调试模式：只处理前 {max_members} 名")

        # 阶段 2: 逐个爬取详情页
        members = []
        for i, entry in enumerate(member_entries, 1):
            print(f"[{i}/{len(member_entries)}] {entry.get('name', 'Unknown')} ({entry['url'][:60]}...)")

            member = self._scrape_detail_page(entry)
            if member.name or member.name_cn:
                members.append(member)

            time.sleep(self.delay)

        print(f"\n成功爬取 {len(members)} 名成员信息")
        return members

    def scrape_card_page(self, page_url: str, max_members: Optional[int] = None) -> List[MemberProfile]:
        """
        单页卡片模式：从一个页面中提取所有人员卡片

        适用于 Hugo Academic / Wowchemy 等模板网站，人员信息以卡片形式
        排列在同一页面，每个卡片包含姓名、职位、社交链接等。
        不需要访问详情页，一次请求即可提取所有信息。

        实战案例:
        - PKU.AI: 65 名成员，成功解密 30+ 个 Cloudflare 保护邮箱
        - Hugo Academic 模板网站: .people-person 卡片 + .network-icon 社交链接

        CSS 选择器层级:
        ```
        .people-person (或 .media.stream-item)
        ├── .portrait-title h2  → 姓名
        ├── .portrait-title h3  → 职位
        ├── .portrait-subtitle  → 机构
        └── .network-icon a     → 社交链接 (含 Cloudflare 加密邮箱)
        ```

        Args:
            page_url: 人员列表页 URL
            max_members: 限制提取数量 (用于调试)

        Returns:
            成员资料列表
        """
        # 自动推断 base_url
        if not self.base_url:
            self.base_url = '/'.join(page_url.split('/')[:3])

        print(f"正在爬取卡片页面: {page_url}")

        try:
            response = self.session.get(page_url, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"页面请求失败: {e}")
            return []

        # 查找人员卡片 (尝试多个选择器)
        cards = []
        for selector in self.CARD_SELECTORS:
            cards = soup.select(selector)
            if cards:
                print(f"使用选择器 '{selector}' 找到 {len(cards)} 个人员卡片")
                break

        if not cards:
            print("未找到人员卡片，请检查页面结构")
            return []

        if max_members:
            cards = cards[:max_members]
            print(f"调试模式：只处理前 {max_members} 个")

        # 逐卡片提取
        members = []
        email_count = 0
        for card in cards:
            profile = self._extract_from_card(card)
            if profile.name or profile.name_cn:
                members.append(profile)
                if profile.email:
                    email_count += 1

        print(f"\n成功提取 {len(members)} 名成员")
        print(f"邮箱覆盖: {email_count}/{len(members)} ({email_count*100//max(len(members),1)}%)")
        return members

    def _extract_from_card(self, card) -> MemberProfile:
        """
        从单个人员卡片中提取所有信息

        处理流程:
        1. 姓名 (.portrait-title h2)
        2. 职位/机构 (.portrait-title h3, .portrait-subtitle)
        3. 社交链接 (.network-icon a)，含 Cloudflare 邮箱解密

        特殊处理:
        - Cloudflare 加密邮箱: 检测 /cdn-cgi/l/email-protection# 链接，
          提取 # 后的加密字符串，XOR 解密
        - 相对 URL: 以 / 开头的链接自动补全为绝对 URL
        """
        profile = MemberProfile()

        # 1. 姓名提取
        for selector in self.NAME_SELECTORS:
            name_tag = card.select_one(selector)
            if name_tag:
                full_name = name_tag.get_text(strip=True)
                if self._is_chinese(full_name):
                    profile.name_cn = full_name
                else:
                    profile.name = full_name
                # 如果同时有中英文名，尝试拆分
                if not profile.name and profile.name_cn:
                    profile.name = profile.name_cn  # 保底
                break

        # 2. 职位/机构提取
        role_texts = []
        for selector in self.ROLE_SELECTORS:
            elements = card.select(selector)
            role_texts = [t.get_text(strip=True) for t in elements if t.get_text(strip=True)]
            if role_texts:
                break

        if role_texts:
            profile.role = self._extract_role(' '.join(role_texts))
            # 机构提取
            for text in role_texts:
                if any(kw in text for kw in self.INSTITUTION_KEYWORDS):
                    profile.affiliation = text
                    break

        # 3. 社交链接 + 邮箱提取
        links = []
        for selector in self.LINK_SELECTORS:
            links = card.select(selector)
            if links:
                break

        for link in links:
            href = link.get('href', '')
            if not href:
                continue

            # Cloudflare 加密邮箱检测 (必须在 URL 补全之前处理)
            if 'email-protection' in href:
                encoded_hash = href.split('#')[-1]
                decoded_email = self._decode_cloudflare_email(encoded_hash)
                if decoded_email:
                    profile.email = decoded_email
                    print(f"  [CF解密] {profile.name or profile.name_cn}: {decoded_email}")
                continue  # 处理完加密邮箱，跳过后续链接分类

            # 相对 URL → 绝对 URL
            if href.startswith('/'):
                href = self.base_url + href

            # 常规链接分类
            href_lower = href.lower()
            if 'mailto:' in href_lower:
                if not profile.email:
                    profile.email = href.replace('mailto:', '').strip()
            elif 'github.com' in href_lower and 'wowchemy' not in href_lower:
                if not profile.github:
                    profile.github = href
            elif 'scholar.google' in href_lower:
                if not profile.google_scholar:
                    profile.google_scholar = href
            elif 'linkedin.com' in href_lower:
                if not profile.linkedin:
                    profile.linkedin = href
            elif 'zhihu.com' in href_lower:
                if not profile.zhihu:
                    profile.zhihu = href
            elif 'bilibili.com' in href_lower:
                if not profile.bilibili:
                    profile.bilibili = href
            elif 'twitter.com' in href_lower or 'x.com' in href_lower:
                if not profile.twitter:
                    profile.twitter = href
            else:
                # 其余链接作为个人主页
                if not profile.homepage:
                    profile.homepage = href

        return profile

    @staticmethod
    def _decode_cloudflare_email(encoded: str) -> str:
        """
        内联 Cloudflare XOR 解密

        Cloudflare 邮箱保护: 第一个字节 (2 hex chars) 为密钥，
        后续每个字节与密钥 XOR 得到原始字符。

        PKU.AI 实测: 65 人中成功解密 30+ 个邮箱 (成功率 ~95% 对加密邮箱)

        Args:
            encoded: # 后的十六进制字符串

        Returns:
            解密后的邮箱，失败返回空字符串
        """
        try:
            r = int(encoded[:2], 16)
            email = ''.join(
                chr(int(encoded[i:i+2], 16) ^ r)
                for i in range(2, len(encoded), 2)
            )
            if '@' in email and '.' in email:
                return email
            return ''
        except Exception:
            return ''

    def scrape_by_email_anchor(self, page_url: str, max_members: Optional[int] = None) -> List[MemberProfile]:
        """
        邮箱反向定位模式：通过搜索邮箱文本节点，向上回溯 DOM 树找到人员卡片容器

        适用于无固定 CSS 类名、自定义 HTML 结构的学术网站。
        当页面结构混乱、无法通过 CSS 选择器定位时，使用此防御性策略。

        实战案例:
        - 清华 MediaLab: 39 名成员，通过 @tsinghua.edu.cn 反向定位人员卡片
        - 适用于自定义 HTML、无模板、结构不规范的学术网站

        核心策略:
        1. 搜索所有包含 @ 的文本节点 (邮箱特征)
        2. 向上回溯 DOM 树 (最多 4 层)，寻找人员卡片容器
        3. 容器识别启发式规则:
           - 必须是 div 或 li 标签
           - 文本长度在 20-3000 字符之间 (单人卡片范围)
           - 去重：同一容器只处理一次
        4. 从容器中提取姓名、邮箱、头衔、社交链接
        5. 可选：访问详情页获取更多信息

        Args:
            page_url: 人员列表页 URL
            max_members: 限制提取数量 (用于调试)

        Returns:
            成员资料列表
        """
        # 自动推断 base_url
        if not self.base_url:
            self.base_url = '/'.join(page_url.split('/')[:3])

        print(f"正在使用邮箱反向定位法爬取: {page_url}")

        try:
            response = self.session.get(page_url, timeout=15, verify=False)
            response.encoding = response.apparent_encoding or 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"页面请求失败: {e}")
            return []

        # 查找所有包含 @ 的文本节点
        email_nodes = soup.find_all(string=re.compile(r'@'))
        print(f"发现 {len(email_nodes)} 个潜在的邮箱节点，正在解析人员结构...")

        processed_containers = []  # 去重：防止同一容器被多次处理
        members = []
        email_count = 0

        for node in email_nodes:
            # 向上回溯，找到人员卡片容器
            container = node.parent
            found_card = False

            # 向上找 4 层
            for _ in range(4):
                if container and (container.name == 'div' or container.name == 'li'):
                    # 容器识别启发式规则
                    txt_len = len(container.get_text())
                    if 20 < txt_len < 3000:  # 单人卡片文本长度范围
                        if container not in processed_containers:
                            processed_containers.append(container)

                            # 解析该卡片
                            profile = self._extract_from_email_card(container)

                            # 过滤无效数据
                            if profile.name or profile.name_cn:
                                # 排除页脚联系方式 (通常包含 Address, Mailbox 等关键词)
                                if any(kw in (profile.name + profile.name_cn) for kw in ['Address', 'Mailbox', 'Contact', 'Office']):
                                    continue

                                # 如果有详情页链接，深入抓取
                                if profile.source_url and profile.source_url != page_url:
                                    print(f"  -> 深入抓取详情页: {profile.source_url}")
                                    try:
                                        sub_soup = self._get_soup_safe(profile.source_url)
                                        if sub_soup:
                                            more_text = sub_soup.get_text(separator='\n')
                                            profile.bio = more_text[:3000]
                                            # 提取额外的社交链接
                                            self._extract_all_links(sub_soup, profile)
                                    except:
                                        pass

                                members.append(profile)
                                if profile.email:
                                    email_count += 1
                                print(f"  ✅ 提取成功: {profile.name or profile.name_cn} ({profile.email or 'No Email'})")

                            found_card = True
                            break

                if container.parent:
                    container = container.parent
                else:
                    break

            if max_members and len(members) >= max_members:
                break

        print(f"\n成功提取 {len(members)} 名成员")
        print(f"邮箱覆盖: {email_count}/{len(members)} ({email_count*100//max(len(members),1)}%)")
        return members

    def _extract_from_email_card(self, card_tag) -> MemberProfile:
        """
        从邮箱反向定位到的卡片容器中提取信息

        处理流程:
        1. 提取所有文本行
        2. 提取邮箱 (必定存在，因为是通过邮箱定位到的)
        3. 提取姓名 (通常是第一行，过滤掉头衔词)
        4. 提取头衔 (包含 Professor, PhD, Master 等关键词的行)
        5. 提取详情页链接 (相对路径或本站链接)
        6. 提取社交链接 (GitHub, Scholar, LinkedIn 等)
        """
        profile = MemberProfile()

        # 1. 提取所有文本行
        lines = [line.strip() for line in card_tag.get_text(separator="\n").split('\n') if line.strip()]

        # 2. 提取邮箱
        email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}')
        for line in lines:
            if "@" in line:
                match = email_pattern.search(line)
                if match:
                    profile.email = match.group(0)
                    break

        # 3. 提取姓名 (第一行，过滤掉头衔词)
        raw_name_line = lines[0] if lines else ""
        # 过滤掉常见的页面标题
        if raw_name_line in ["All Faculty", "Postdoctoral Fellow", "Team", "Principal Investigator", "Members"]:
            raw_name_line = lines[1] if len(lines) > 1 else ""

        # 分离中英文名
        cn_name = "".join(re.findall(r'[\u4e00-\u9fa5]+', raw_name_line))
        en_name = re.sub(r'[\u4e00-\u9fa5]+', '', raw_name_line).strip()

        if cn_name:
            profile.name_cn = cn_name
        if en_name:
            profile.name = en_name

        # 4. 提取头衔
        for line in lines:
            if any(kw in line for kw in ["Professor", "Researcher", "Fellow", "Ph.D", "PhD", "Master", "Student"]):
                if len(line) < 50:  # 头衔通常不长
                    profile.role = self._extract_role(line)
                    break

        # 5. 提取详情页链接
        links = card_tag.find_all('a', href=True)
        for a in links:
            href = a['href']
            # 排除 mailto 和外部链接
            if "mailto:" not in href:
                if "http" not in href:
                    # 相对路径
                    full_link = urljoin(self.base_url, href)
                    profile.source_url = full_link
                    break
                elif self.base_url in href:
                    # 本站链接
                    profile.source_url = href
                    break

        # 6. 提取社交链接
        for link in links:
            href = link.get('href', '')
            if not href:
                continue

            href_lower = href.lower()
            if 'github.com' in href_lower and 'wowchemy' not in href_lower:
                if not profile.github:
                    profile.github = href
            elif 'scholar.google' in href_lower:
                if not profile.google_scholar:
                    profile.google_scholar = href
            elif 'linkedin.com' in href_lower:
                if not profile.linkedin:
                    profile.linkedin = href

        return profile

    def _get_soup_safe(self, url: str):
        """安全地获取 BeautifulSoup 对象，处理异常"""
        try:
            response = self.session.get(url, timeout=10, verify=False)
            response.encoding = response.apparent_encoding or 'utf-8'
            return BeautifulSoup(response.text, 'html.parser')
        except:
            return None

    def _get_member_entries(self, lab_url: str) -> List[Dict]:
        """
        从实验室页面提取成员条目 (名字 + URL)

        实战踩坑:
        - LAMDA 的列表页混入了大量导航链接 (MainPage, Pub, App 等)
        - 用中文名长度 (2-5字) 过滤可以去除大部分噪声
        - 需要同时支持 /author/Name/ 和 /Name/ 两种 URL 模式
        """
        try:
            response = self.session.get(lab_url, timeout=15)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')

            # 缩小搜索范围：优先从 content div 中查找
            content_div = soup.find('div', id='content') or soup.body
            if not content_div:
                return []

            entries = []
            seen_urls: Set[str] = set()

            for link in content_div.find_all('a', href=True):
                href = link.get('href', '')
                name = self._clean_text(link.get_text())

                # 基本验证
                if not href or not name:
                    continue

                # 排除导航链接
                if self._is_excluded_url(href):
                    continue

                # 中文名过滤：2-5 个字符（中文名通常 2-4 个字）
                # 英文名过滤：至少 2 个字符
                if self._is_chinese(name):
                    if len(name) < 2 or len(name) > 5:
                        continue
                else:
                    if len(name) < 2 or len(name) > 40:
                        continue

                # 拼接完整 URL
                full_url = urljoin(self.base_url, href)

                # 去重
                if full_url in seen_urls:
                    continue
                seen_urls.add(full_url)

                # 检测该链接是否可能跳到外部 (排除外部链接)
                if not full_url.startswith(self.base_url) and '.edu' not in full_url:
                    continue

                entries.append({
                    'name': name,
                    'url': full_url,
                })

            return entries

        except Exception as e:
            print(f"获取成员列表失败: {e}")
            return []

    def _scrape_detail_page(self, entry: Dict) -> MemberProfile:
        """
        爬取单个成员的详情页

        提取顺序: 姓名 → 邮箱 → 研究方向 → 社交链接 → 论文 → Bio
        """
        url = entry['url']
        name_from_list = entry.get('name', '')

        profile = MemberProfile(source_url=url)

        # 预设列表页获取的名字
        if self._is_chinese(name_from_list):
            profile.name_cn = name_from_list
        else:
            profile.name = name_from_list

        try:
            response = self.session.get(url, timeout=10)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            text_content = soup.get_text()

            # 1. 姓名提取 (补充详情页信息)
            if not profile.name:
                profile.name = self._extract_name(soup, url)

            # 2. 邮箱提取 (支持多种混淆方式)
            profile.email = self._extract_email(soup, text_content)

            # 3. 研究方向
            profile.research_interests = self._extract_interests(soup, text_content)

            # 4. 角色/职位
            profile.role = self._extract_role(text_content)

            # 5. 社交链接 (一次遍历提取全部)
            self._extract_all_links(soup, profile)

            # 6. 论文列表
            profile.publications = self._extract_publications(soup)

            # 7. 个人介绍
            profile.bio = self._extract_bio(soup, text_content)

            # 8. 教育背景
            profile.education = self._extract_education(soup, text_content)

        except requests.exceptions.SSLError:
            print(f"    [!] SSL 错误，跳过: {url}")
        except requests.exceptions.Timeout:
            print(f"    [!] 超时，跳过: {url}")
        except Exception as e:
            print(f"    [!] 爬取失败: {e}")

        return profile

    # ==================== 提取方法 ====================

    def _extract_name(self, soup: BeautifulSoup, url: str) -> str:
        """
        提取英文名

        优先级:
        1. <title> 标签 (通常是 "Name - Lab")
        2. <h1> 标签
        3. URL 路径 (如 /zhangzn/ → zhangzn，作为保底)
        """
        # 尝试 title 标签
        title = soup.find('title')
        if title:
            name = title.get_text().split('-')[0].split('|')[0].strip()
            if name and 2 <= len(name) <= 50:
                return name

        # 尝试 h1 标签
        h1 = soup.find('h1')
        if h1:
            name = h1.get_text(strip=True)
            if name and 2 <= len(name) <= 50:
                return name

        # 从 URL 提取 (保底方案)
        url_name = url.strip('/').split('/')[-1]
        if url_name and url_name.isalpha() and len(url_name) >= 2:
            return url_name

        return ''

    def _extract_email(self, soup: BeautifulSoup, text: str) -> str:
        """
        综合邮箱提取，支持多种混淆方式

        优先级:
        1. mailto: 链接 (最可靠)
        2. Cloudflare XOR 加密
        3. [at] / (at) 文本混淆 (中国高校常见)
        4. 纯文本正则匹配 (最后手段)
        """
        # 1. mailto 链接
        mailto = soup.select_one('a[href^="mailto:"]')
        if mailto:
            return mailto['href'].replace('mailto:', '').strip()

        # 2. Cloudflare 保护
        cf_link = soup.select_one('a[href*="/cdn-cgi/l/email-protection"]')
        if cf_link:
            try:
                from cloudflare_email_decoder import extract_cloudflare_email
                email = extract_cloudflare_email(cf_link['href'])
                if email:
                    return email
            except ImportError:
                pass

        # 3. [at] / (at) 混淆 (LAMDA 等中国高校常见)
        at_pattern = r'([a-zA-Z0-9._-]+)\s*(?:\[at\]|\(at\))\s*([a-zA-Z0-9._-]+\.[a-zA-Z]{2,})'
        match = re.search(at_pattern, text, re.IGNORECASE)
        if match:
            return f"{match.group(1)}@{match.group(2)}"

        # 4. 纯文本正则
        email_pattern = r'[\w.-]+@[\w.-]+\.\w+'
        match = re.search(email_pattern, text)
        if match:
            email = match.group()
            # 排除常见的非个人邮箱
            if not any(x in email for x in ['example.com', 'noreply', 'contact@']):
                return email

        return ''

    def _extract_role(self, text: str) -> str:
        """提取角色/职位"""
        text_lower = text.lower()

        roles = {
            'PhD': ['phd student', 'ph.d. student', 'doctoral student', '博士生', 'ph.d. candidate'],
            'PostDoc': ['postdoc', 'post-doctoral', 'postdoctoral', '博士后'],
            'Professor': ['professor', 'associate professor', 'assistant professor', '教授', '副教授', '助理教授'],
            'Master': ['master student', "master's student", '硕士生'],
            'Researcher': ['research scientist', 'researcher', '研究员', '研究助理']
        }

        for role, keywords in roles.items():
            for kw in keywords:
                if kw in text_lower:
                    return role

        return ''

    def _extract_interests(self, soup: BeautifulSoup, text: str) -> List[str]:
        """
        提取研究方向

        策略:
        1. 查找 "Research Interests:" 后的文本
        2. 查找 "Interests" 标题下的列表
        3. 关键词匹配 (保底)
        """
        # 策略 1: "Research Interests: xxx"
        interest_match = re.search(r'Research\s*Interests?:?\s*(.{10,200})', text, re.IGNORECASE)
        if interest_match:
            raw = interest_match.group(1).split('\n')[0].strip()
            interests = [s.strip() for s in re.split(r'[,;，；、]', raw) if s.strip()]
            if interests:
                return interests

        # 策略 2: "Interests" 标题后的列表 (Hugo Academic)
        interests_match = re.search(r'Interests\s*\n([\s\S]*?)(?=Education|Publications|$)', text)
        if interests_match:
            raw = interests_match.group(1).strip()
            interests = [s.strip() for s in raw.split('\n') if s.strip() and s.strip() not in ['•', '*', '-']]
            if interests:
                return interests

        return []

    def _extract_all_links(self, soup: BeautifulSoup, profile: MemberProfile):
        """
        一次遍历提取所有社交/学术链接

        排除已知的模板链接 (wowchemy, academic-theme 等)
        """
        for link in soup.find_all('a', href=True):
            href = link.get('href', '')
            href_lower = href.lower()

            # 排除无效链接
            if '%e6%97%a0' in href:  # URL 编码的"无"
                continue

            if 'github.com' in href_lower and 'wowchemy' not in href_lower and 'academic' not in href_lower:
                if not profile.github:
                    profile.github = href
            elif 'scholar.google' in href_lower:
                if not profile.google_scholar:
                    profile.google_scholar = href
            elif 'linkedin.com' in href_lower:
                if not profile.linkedin:
                    profile.linkedin = href
            elif 'zhihu.com' in href_lower:
                if not profile.zhihu:
                    profile.zhihu = href
            elif 'bilibili.com' in href_lower:
                if not profile.bilibili:
                    profile.bilibili = href
            elif 'twitter.com' in href_lower or 'x.com' in href_lower:
                if not profile.twitter:
                    profile.twitter = href

    def _extract_publications(self, soup: BeautifulSoup) -> List[str]:
        """
        提取论文列表

        策略: 找 "Publications/Conference/Journal" 标题后的 ul/ol 列表
        LAMDA 经验: 标题可能是 h1-h4/strong/b，列表可能在 div 内嵌套

        Returns:
            论文标题列表 (最多 5 篇)
        """
        # 查找包含 Publication 关键词的标题标签
        headers = soup.find_all(
            ['h1', 'h2', 'h3', 'h4', 'strong', 'b'],
            string=re.compile(r'Publication|Conference|Journal|Selected\s+Paper', re.IGNORECASE)
        )

        for header in headers:
            # 寻找标题后的 ul/ol/div
            next_elem = header.find_next_sibling(['ul', 'ol', 'div'])
            if not next_elem:
                continue

            target_list = None
            if next_elem.name in ['ul', 'ol']:
                target_list = next_elem
            elif next_elem.name == 'div':
                inner_ul = next_elem.find(['ul', 'ol'])
                if inner_ul:
                    target_list = inner_ul

            if not target_list:
                continue

            pubs = []
            for item in target_list.find_all('li'):
                text = self._clean_text(item.get_text())
                link_tag = item.find('a')
                link = urljoin(self.base_url, link_tag['href']) if link_tag else ''

                # 过滤太短的条目（不太可能是论文标题）
                if len(text) > 20:
                    if link:
                        pubs.append(f"{text} [{link}]")
                    else:
                        pubs.append(text)

                if len(pubs) >= 5:
                    break

            if pubs:
                return pubs

        return []

    def _extract_bio(self, soup: BeautifulSoup, text: str) -> str:
        """
        提取个人简介

        策略: 查找 "Biography/Introduction/About" 标题后的第一个 <p>
        """
        bio_header = soup.find(string=re.compile(r'Biography|Introduction|About\s+Me', re.IGNORECASE))
        if bio_header:
            parent = bio_header.find_parent()
            if parent:
                bio_p = parent.find_next_sibling('p')
                if bio_p:
                    return self._clean_text(bio_p.get_text())

        return ''

    def _extract_education(self, soup: BeautifulSoup, text: str) -> List[str]:
        """提取教育背景"""
        edu_match = re.search(r'Education\s*\n([\s\S]*?)(?=Research|Experience|Publications|$)', text)

        if edu_match:
            edu_text = edu_match.group(1)
            lines = [l.strip() for l in edu_text.split('\n') if l.strip()]
            return [l for l in lines if len(l) > 10]

        return []

    # ==================== 工具方法 ====================

    @staticmethod
    def _clean_text(text: str) -> str:
        """清洗文本：去除多余空格、换行"""
        if not text:
            return ""
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def _is_chinese(text: str) -> bool:
        """检测文本是否包含中文字符"""
        return bool(re.search(r'[\u4e00-\u9fff]', text))

    def _is_excluded_url(self, href: str) -> bool:
        """检测 URL 是否应该被排除"""
        href_lower = href.lower()

        # 已知排除关键词
        for kw in self.EXCLUDE_URL_KEYWORDS:
            if kw.lower() in href_lower:
                return True

        # SSL 问题域名
        for domain in self.SSL_PROBLEM_DOMAINS:
            if domain in href_lower:
                return True

        return False


# ==================== 保存工具 ====================

def save_to_json(members: List[MemberProfile], filepath: str):
    """保存到 JSON 文件"""
    data = [m.to_dict() for m in members]
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✅ 已保存 {len(members)} 名成员到 {filepath}")


def save_to_csv(members: List[MemberProfile], filepath: str):
    """保存到 CSV 文件 (Excel 兼容)"""
    import csv

    fieldnames = [
        'name', 'name_cn', 'role', 'email', 'affiliation',
        'research_interests', 'bio', 'homepage', 'google_scholar',
        'github', 'linkedin', 'zhihu', 'bilibili', 'twitter',
        'publications', 'education', 'source_url'
    ]

    with open(filepath, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction='ignore')
        writer.writeheader()

        for member in members:
            row = member.to_dict()
            row['research_interests'] = ', '.join(row['research_interests'])
            row['publications'] = ' | '.join(row['publications'])
            row['education'] = ' | '.join(row['education'])
            writer.writerow(row)

    print(f"✅ 已保存 {len(members)} 名成员到 {filepath}")


# ==================== 使用示例 ====================

if __name__ == "__main__":
    # === 模式 1: 两阶段爬取 (列表页 → 详情页) ===
    # 适用于: LAMDA、自定义 HTML/ASP.NET 页面

    # 示例: 爬取 LAMDA 博士生
    # scraper = LabMemberScraper(delay=1.0, base_url="https://www.lamda.nju.edu.cn")
    # members = scraper.scrape_lab("https://www.lamda.nju.edu.cn/CH.PhD_student.ashx")

    # 示例: 爬取 TongClass 成员
    # scraper = LabMemberScraper(delay=0.3, base_url="https://tongclass.ac.cn")
    # members = scraper.scrape_lab("https://tongclass.ac.cn/people/")

    # === 模式 2: 卡片模式 (单页提取) ===
    # 适用于: Hugo Academic / Wowchemy 模板网站

    # 示例: 爬取 PKU.AI 成员 (含 Cloudflare 邮箱解密)
    # scraper = LabMemberScraper(base_url="https://pku.ai")
    # members = scraper.scrape_card_page("https://pku.ai/people/", max_members=5)

    # === 模式 3: 邮箱反向定位 (防御性策略) ===
    # 适用于: 无固定 CSS 类名、自定义 HTML 结构

    # 示例: 爬取清华 MediaLab 成员 (邮箱反向定位)
    scraper = LabMemberScraper(base_url="https://media.au.tsinghua.edu.cn")
    members = scraper.scrape_by_email_anchor("https://media.au.tsinghua.edu.cn/Team.htm", max_members=5)

    # 全量模式:
    # members = scraper.scrape_by_email_anchor("https://media.au.tsinghua.edu.cn/Team.htm")

    # 打印结果
    print(f"\n=== 共 {len(members)} 名成员 ===")
    for member in members:
        name = member.name_cn or member.name
        print(f"  {name} ({member.role})")
        if member.email:
            print(f"    Email: {member.email}")
        if member.research_interests:
            print(f"    Interests: {', '.join(member.research_interests)}")

    # 保存结果
    # save_to_json(members, "lab_members.json")
    # save_to_csv(members, "lab_members.csv")
