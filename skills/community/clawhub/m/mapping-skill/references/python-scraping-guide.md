# Python 爬虫技术指南

> 本文档提供免费的 Python 爬虫技术方案，作为 BrightData MCP 的替代选择。

---

## 概述

在进行 AI 人才搜索时，爬取 researcher 的个人主页、实验室页面等是获取联系方式的关键步骤。本指南总结了项目中积累的 Python 爬虫经验，提供可复用的代码模板和最佳实践。

---

## 技术选型对比

| 场景 | 推荐方案 | 优点 | 缺点 | 成本 |
|------|---------|------|------|------|
| 简单静态页面 | requests + BeautifulSoup | 快速、轻量、易调试 | 无法处理 JS 渲染 | 免费 |
| **Hugo Academic 卡片页** | **CSS 选择器 + CF 解密** | **单页提取、模板通用** | **仅限 Hugo 模板** | **免费** |
| **PDF 文本解析** | **PyMuPDF (fitz)** | **直接提取 PDF 内容、处理花括号邮箱** | **需注意包名冲突** | **免费** |
| 需要 JS 渲染 | Playwright / Selenium | 功能完整、支持复杂页面 | 较慢、资源消耗大 | 免费 |
| 高并发爬取 | httpx + asyncio | 异步高效、支持 HTTP/2 | 需要异步编程知识 | 免费 |
| **社交网络图谱** | **GitHub API** | **结构化数据、三层拼装** | **需要 Token** | **免费** |
| 高反爬网站 | BrightData MCP | 成功率高、支持 LinkedIn | 付费服务 | 付费 |

### 推荐策略

```
┌─────────────────────────────────────────────────────────────┐
│                    目标网站类型判断                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Hugo Academic 模板 (.people-person 卡片)                    │
│      │                                                       │
│      ▼                                                       │
│  使用 CSS 选择器 + CF 解密 (单页提取) ────> 免费            │
│                                                              │
│  学术网站 (.edu, .github.io)                                 │
│      │                                                       │
│      ▼                                                       │
│  使用 Python (requests/httpx) ──────────────> 免费          │
│                                                              │
│  GitHub 用户关系网络                                         │
│      │                                                       │
│      ▼                                                       │
│  使用 GitHub API (Token 必需) ──────────────> 免费          │
│                                                              │
│  LinkedIn / Twitter / Facebook                               │
│      │                                                       │
│      ▼                                                       │
│  使用 BrightData MCP ───────────────────────> 付费          │
│                                                              │
│  遇到 Cloudflare 保护？                                       │
│      │                                                       │
│      ├─> 仅邮箱加密 → 使用 XOR 解密 ─────────> 免费          │
│      │                                                       │
│      └─> 完整页面保护 → 使用 BrightData ────> 付费          │
│                                                              │
│  会议论文 PDF (CVPR/ICCV/WACV)                               │
│      │                                                       │
│      ▼                                                       │
│  使用 PyMuPDF 内存流 + 双策略邮箱提取 ────────> 免费          │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. requests + BeautifulSoup 方案

### 1.1 基础模板

适用于大多数学术网站和个人主页。

```python
import requests
from bs4 import BeautifulSoup
from typing import Dict, List

def scrape_profile(url: str) -> Dict:
    """
    爬取个人主页，提取结构化信息

    Args:
        url: 个人主页 URL

    Returns:
        包含提取信息的字典
    """
    # 创建 Session 复用连接
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    })

    try:
        response = session.get(url, timeout=15)
        response.encoding = 'utf-8'

        soup = BeautifulSoup(response.text, 'html.parser')

        profile = {
            'url': url,
            'email': extract_email(soup),
            'name': extract_name(soup),
            'affiliation': extract_affiliation(soup),
            'research_interests': extract_interests(soup),
            'links': extract_links(soup)
        }

        return profile

    except requests.RequestException as e:
        print(f"请求失败: {e}")
        return {'url': url, 'error': str(e)}


def extract_email(soup: BeautifulSoup) -> str:
    """提取邮箱地址"""
    # 方法 1: mailto 链接
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if 'mailto:' in href.lower():
            return href.replace('mailto:', '').strip()

        # 方法 2: Cloudflare 保护的邮箱
        if '/cdn-cgi/l/email-protection#' in href:
            encoded = href.split('#')[-1]
            return decode_cloudflare_email(encoded)

    # 方法 3: 页面文本中的邮箱
    import re
    text = soup.get_text()
    email_match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text)
    if email_match:
        return email_match.group()

    return ''


def extract_links(soup: BeautifulSoup) -> Dict[str, str]:
    """提取社交链接"""
    links = {}

    for link in soup.find_all('a', href=True):
        href = link.get('href', '').lower()

        if 'github.com' in href and 'wowchemy' not in href:
            links['github'] = link.get('href')
        elif 'scholar.google' in href:
            links['google_scholar'] = link.get('href')
        elif 'linkedin.com' in href:
            links['linkedin'] = link.get('href')
        elif 'twitter.com' in href or 'x.com' in href:
            links['twitter'] = link.get('href')

    return links


def extract_name(soup: BeautifulSoup) -> str:
    """提取姓名"""
    # 尝试 <title> 标签
    title = soup.find('title')
    if title:
        name = title.get_text().split('-')[0].split('|')[0].strip()
        if name:
            return name

    # 尝试 <h1> 标签
    h1 = soup.find('h1')
    if h1:
        return h1.get_text(strip=True)

    return ''


def extract_affiliation(soup: BeautifulSoup) -> str:
    """提取机构"""
    import re

    # 查找包含 .edu 的链接
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if '.edu' in href:
            text = link.get_text(strip=True)
            if text and len(text) < 50:
                return text

    # 查找页面文本
    text = soup.get_text()
    patterns = [
        r'(Stanford University)',
        r'(MIT)',
        r'(Carnegie Mellon)',
        r'(UC Berkeley)',
        r'(Tsinghua University)',
        r'(Peking University)'
    ]

    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1)

    return ''


def extract_interests(soup: BeautifulSoup) -> List[str]:
    """提取研究兴趣"""
    import re

    text = soup.get_text()

    # 常见的研究兴趣关键词
    keywords = [
        'machine learning', 'deep learning', 'reinforcement learning',
        'natural language processing', 'computer vision', 'robotics',
        'embodied AI', 'multimodal', 'LLM', 'transformer'
    ]

    found = []
    text_lower = text.lower()
    for kw in keywords:
        if kw in text_lower:
            found.append(kw)

    return found
```

### 1.2 Session 复用最佳实践

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

def create_session() -> requests.Session:
    """
    创建配置好的 Session，支持重试和连接池
    """
    session = requests.Session()

    # 配置重试策略
    retry_strategy = Retry(
        total=3,                    # 总重试次数
        backoff_factor=1,           # 指数退避因子
        status_forcelist=[429, 500, 502, 503, 504],  # 触发重试的状态码
    )

    adapter = HTTPAdapter(
        max_retries=retry_strategy,
        pool_connections=10,        # 连接池大小
        pool_maxsize=10
    )

    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # 设置默认 headers
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
    })

    return session


# 使用示例
session = create_session()
profiles = []

for url in urls:
    profile = scrape_profile(url)
    profiles.append(profile)
    time.sleep(0.5)  # 礼貌性延迟
```

---

## 2. Cloudflare 邮箱解密

### 2.1 问题背景

许多使用 Cloudflare CDN 的网站会启用邮箱保护功能，邮箱地址会被替换为加密字符串：

```html
<a href="/cdn-cgi/l/email-protection#f493919e85c6c5b499959d9887da80879d9a939c8195da919081da979a">
    [email protected]
</a>
```

### 2.2 解密算法

Cloudflare 使用简单的 XOR 加密：

1. 第一个字节（2 个字符）是密钥
2. 后续每个字节与密钥 XOR 得到原始字符

```python
def decode_cloudflare_email(encoded: str) -> str:
    """
    解码 Cloudflare 邮箱保护

    Args:
        encoded: 加密后的十六进制字符串 (如 "f493919e85c6c5...")

    Returns:
        解密后的邮箱地址

    Example:
        >>> decode_cloudflare_email("f493919e85c6c5b499959d9887da80879d9a939c8195da919081da979a")
        "gejq21@mails.tsinghua.edu.cn"
    """
    try:
        encoded = encoded.strip()

        # 第一个字节是密钥
        key = int(encoded[:2], 16)

        # XOR 解密
        decoded = ''
        for i in range(2, len(encoded), 2):
            char_code = int(encoded[i:i+2], 16) ^ key
            decoded += chr(char_code)

        return decoded

    except Exception:
        return ''


def extract_cloudflare_email(href: str) -> str:
    """
    从 Cloudflare 保护的链接中提取邮箱

    Args:
        href: 形如 "/cdn-cgi/l/email-protection#abc123def" 的链接

    Returns:
        解密后的邮箱地址
    """
    if '/cdn-cgi/l/email-protection#' in href:
        encoded = href.split('#')[-1]
        return decode_cloudflare_email(encoded)
    return ''


# 使用示例
href = "/cdn-cgi/l/email-protection#f493919e85c6c5b499959d9887da80879d9a939c8195da919081da979a"
email = extract_cloudflare_email(href)
print(email)  # 输出: gejq21@mails.tsinghua.edu.cn
```

### 2.3 解密原理图解

```
加密后: f4 93 91 9e 85 c6 c5 b4 99 95 9d 98 87 ...
       ↑↑
       密钥 (f4 = 244)

解密过程:
  0x93 ^ 0xf4 = 0x67 = 'g'
  0x91 ^ 0xf4 = 0x65 = 'e'
  0x9e ^ 0xf4 = 0x6a = 'j'
  0x85 ^ 0xf4 = 0x71 = 'q'
  0xc6 ^ 0xf4 = 0x32 = '2'
  0xc5 ^ 0xf4 = 0x31 = '1'
  ...

结果: gejq21@mails.tsinghua.edu.cn
```

---

## 3. httpx 异步爬虫方案

### 3.1 基础模板

适用于需要高并发爬取的场景。

```python
import asyncio
import httpx
from typing import List, Dict, Any

async def async_scrape(url: str, client: httpx.AsyncClient) -> Dict[str, Any]:
    """
    异步爬取单个页面

    Args:
        url: 目标 URL
        client: httpx 异步客户端

    Returns:
        包含状态和内容的字典
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    try:
        response = await client.get(url, headers=headers)

        if response.status_code == 200:
            return {
                "url": url,
                "status": "success",
                "content": response.text[:10000]  # 限制内容长度
            }
        else:
            return {
                "url": url,
                "status": "error",
                "error": f"HTTP {response.status_code}"
            }

    except Exception as e:
        return {
            "url": url,
            "status": "error",
            "error": str(e)
        }


async def batch_scrape(urls: List[str], max_concurrent: int = 5) -> List[Dict]:
    """
    并发爬取多个 URL

    Args:
        urls: URL 列表
        max_concurrent: 最大并发数

    Returns:
        爬取结果列表
    """
    semaphore = asyncio.Semaphore(max_concurrent)

    async def scrape_with_limit(url: str, client: httpx.AsyncClient):
        async with semaphore:
            result = await async_scrape(url, client)
            print(f"[{'✓' if result['status'] == 'success' else '✗'}] {url[:60]}...")
            return result

    async with httpx.AsyncClient(
        timeout=30.0,
        follow_redirects=True,
        limits=httpx.Limits(max_connections=max_concurrent)
    ) as client:
        tasks = [scrape_with_limit(url, client) for url in urls]
        results = await asyncio.gather(*tasks)

    return results


# 使用示例
async def main():
    urls = [
        "https://example.edu/~phd1/",
        "https://example.edu/~phd2/",
        # ...
    ]

    results = await batch_scrape(urls, max_concurrent=5)

    success_count = sum(1 for r in results if r.get("status") == "success")
    print(f"成功: {success_count}/{len(urls)}")


if __name__ == "__main__":
    asyncio.run(main())
```

### 3.2 智能爬取策略

根据目标域名选择爬取方式：

```python
async def smart_scrape(url: str, client: httpx.AsyncClient) -> Dict[str, Any]:
    """
    智能选择爬取方式：
    - LinkedIn/Twitter 等需要反爬的网站 → 提示使用 BrightData
    - 学术网站 → 使用 httpx 直接爬取
    """
    # 需要 BrightData 的域名
    brightdata_domains = ["linkedin.com", "twitter.com", "x.com", "facebook.com"]

    if any(domain in url.lower() for domain in brightdata_domains):
        return {
            "url": url,
            "status": "skipped",
            "reason": "此域名需要使用 BrightData MCP 服务"
        }

    return await async_scrape(url, client)
```

---

## 4. Serper API 搜索

### 4.1 基础模板

使用 Serper API 执行 Google 搜索：

```python
import httpx
from typing import List, Dict

async def serper_search(
    query: str,
    api_key: str,
    search_type: str = "google",
    num_results: int = 20
) -> Dict:
    """
    使用 Serper API 执行搜索

    Args:
        query: 搜索查询
        api_key: Serper API Key
        search_type: "google" 或 "google_scholar"
        num_results: 返回结果数量

    Returns:
        搜索结果 JSON
    """
    url = "https://google.serper.dev/scholar" if search_type == "google_scholar" else "https://google.serper.dev/search"

    async with httpx.AsyncClient(timeout=30.0) as client:
        response = await client.post(
            url,
            headers={
                "X-API-KEY": api_key,
                "Content-Type": "application/json"
            },
            json={"q": query, "num": num_results}
        )
        return response.json()


async def search_phd_students(
    research_area: str,
    api_key: str
) -> List[str]:
    """
    搜索特定领域的 PhD 学生

    Args:
        research_area: 研究领域 (如 "reinforcement learning")
        api_key: Serper API Key

    Returns:
        找到的 URL 列表
    """
    queries = [
        f'"{research_area}" PhD student site:*.edu',
        f'"{research_area}" "doctoral candidate" site:github.io',
        f'"{research_area}" researcher personal homepage'
    ]

    all_urls = set()

    for query in queries:
        results = await serper_search(query, api_key)

        for item in results.get("organic", []):
            link = item.get("link", "")
            if link and "google.com" not in link:
                all_urls.add(link)

        await asyncio.sleep(0.5)  # 避免限流

    return list(all_urls)
```

---

## 5. GitHub API 社交网络爬取

### 5.1 概述

GitHub API 提供了一种完全不同于 Web 爬虫的人才发现方式 —— **社交网络图谱遍历**：从一个已知研究者出发，通过 Following/Followers 关系发现整个圈子。

**实测案例**: 从 AmandaXu97 的 Following 列表中提取了 926 名用户的完整信息。

**核心优势**:
- 不需要搜索关键词 —— 通过人际关系发现
- API 直接返回结构化数据 —— 无需 HTML 解析
- 三层数据拼装 —— 覆盖率远超单一来源

### 5.2 认证与速率限制

```python
# GitHub Token (必须!)
# 无 Token: 60 请求/小时 (几乎无法使用)
# 有 Token: 5,000 请求/小时
# 创建: https://github.com/settings/tokens (无需特殊权限)

headers = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}
```

**速率估算**: 每个用户需要 ~3 次 API 调用 → 926 用户 ≈ 2,778 次 → 在 5,000/小时限制内。

### 5.3 三层数据拼装

```python
# Layer 1: 基础 Profile (GitHub API 直接返回)
resp = requests.get(f"https://api.github.com/users/{username}", headers=headers)
profile = resp.json()
# 字段: name, bio, email, company, location, blog, twitter_username

# Layer 2: Social Accounts API (较新端点，很多人不知道)
resp = requests.get(f"https://api.github.com/users/{username}/social_accounts", headers=headers)
# 返回: [{"provider": "linkedin", "url": "https://linkedin.com/in/xxx"}, ...]

# Layer 3: Profile README (同名仓库的 README.md)
# 很多研究者在此放 Scholar、LinkedIn、个人主页链接
for branch in ["main", "master"]:
    url = f"https://raw.githubusercontent.com/{username}/{username}/{branch}/README.md"
    resp = requests.get(url)
    if resp.status_code == 200:
        readme = resp.text
        break
```

### 5.4 从 README 文本提取社交链接

```python
import re

LINK_PATTERNS = {
    'scholar': re.compile(r'(https?://scholar\.google\.[\w.]+/citations\?user=[\w-]+)'),
    'linkedin': re.compile(r'(https?://(?:www\.)?linkedin\.com/in/[\w\-%]+)'),
    'zhihu': re.compile(r'(https?://(?:www\.)?zhihu\.com/people/[\w\-%]+)'),
    'bilibili': re.compile(r'(https?://space\.bilibili\.com/\d+)'),
}

def extract_links(text):
    results = {}
    for name, pattern in LINK_PATTERNS.items():
        match = pattern.search(text)
        if match:
            results[name] = match.group(1)
    return results
```

### 5.5 分页获取关注列表

```python
def get_all_following(username, headers):
    """GitHub API 分页: 每页最多 100 条"""
    users = []
    page = 1
    while True:
        url = f"https://api.github.com/users/{username}/following?per_page=100&page={page}"
        resp = requests.get(url, headers=headers)
        data = resp.json()
        if not data:
            break
        users.extend(data)
        page += 1
    return users
```

**完整参考脚本**: `scripts/github_network_scraper.py`

---

## 6. Hugo Academic / Wowchemy 模板卡片解析

### 6.1 概述

**Hugo Academic**（现称 Wowchemy）是学术圈最流行的个人/实验室网站模板。大量顶尖 AI 实验室使用它构建团队页面。该模板有固定的 HTML 结构，掌握其 CSS 选择器可以实现高效的**单页批量提取**。

**实测案例**: PKU.AI — 65 名成员，一次请求提取全部，成功解密 30+ 个 Cloudflare 邮箱。

**核心优势**:
- 单页提取，无需访问详情页 → 只需 1 次 HTTP 请求
- 结构固定，CSS 选择器通用性强
- 社交链接集中在 `.network-icon` 区域，分类方便

### 6.2 模板特征识别

如何判断一个网站使用了 Hugo Academic 模板：

```python
def is_hugo_academic(soup):
    """检测页面是否使用 Hugo Academic / Wowchemy 模板"""
    indicators = [
        soup.select('.people-person'),          # 人员卡片
        soup.select('.network-icon'),            # 社交链接图标区
        soup.select('.portrait-title'),          # 人物标题区
        soup.select('meta[name="generator"][content*="Hugo"]'),  # Hugo 标记
        soup.select('link[href*="wowchemy"]'),   # Wowchemy 样式表
    ]
    return any(indicators)
```

**常见 Hugo Academic 实验室网站**:

| 网站 | URL | 特点 |
|------|-----|------|
| PKU.AI | `pku.ai/people/` | Cloudflare 邮箱保护 |
| TongClass | `tongclass.ac.cn/people/` | 标准 Hugo Academic |
| 部分 .github.io | `xxx.github.io/people/` | 无反爬 |

### 6.3 CSS 选择器层级

```
页面结构:
├── .people-person (或 .media.stream-item)    ← 人员卡片容器
│   ├── .portrait-title
│   │   ├── h2                                 ← 姓名
│   │   └── h3                                 ← 职位/头衔
│   ├── .portrait-subtitle                     ← 机构/学校
│   └── .network-icon                          ← 社交链接区
│       ├── a[href*="email-protection"]        ← Cloudflare 加密邮箱
│       ├── a[href*="github.com"]              ← GitHub
│       ├── a[href*="scholar.google"]          ← Google Scholar
│       ├── a[href*="linkedin.com"]            ← LinkedIn
│       └── a[href*="zhihu.com"]               ← 知乎
```

### 6.4 完整卡片提取代码

```python
from bs4 import BeautifulSoup

def parse_hugo_academic_cards(html, base_url):
    """
    从 Hugo Academic 页面提取所有人员信息

    实测: PKU.AI 65 人，30+ 邮箱成功解密
    """
    soup = BeautifulSoup(html, 'html.parser')

    # 查找卡片 (两种常见选择器)
    cards = soup.select('.people-person') or soup.select('.media.stream-item')
    results = []

    for card in cards:
        person = {}

        # 姓名
        name_tag = card.select_one('.portrait-title h2') or card.select_one('h2')
        if name_tag:
            person['name'] = name_tag.get_text(strip=True)

        # 职位/机构
        texts = [t.get_text(strip=True)
                 for t in card.select('.portrait-title h3, .portrait-subtitle')]
        person['title'] = ' | '.join(texts)

        # 社交链接 (含 Cloudflare 解密)
        for link in card.select('.network-icon a'):
            href = link.get('href', '')
            if not href:
                continue

            # Cloudflare 加密邮箱
            if 'email-protection' in href:
                encoded = href.split('#')[-1]
                person['email'] = decode_cf_email(encoded)
                continue

            # 相对路径补全
            if href.startswith('/'):
                href = base_url + href

            # 链接分类
            href_lower = href.lower()
            if 'mailto:' in href_lower:
                person['email'] = href.replace('mailto:', '')
            elif 'github.com' in href_lower:
                person['github'] = href
            elif 'scholar.google' in href_lower:
                person['scholar'] = href
            elif 'linkedin.com' in href_lower:
                person['linkedin'] = href

        results.append(person)

    return results


def decode_cf_email(encoded):
    """Cloudflare XOR 邮箱解密"""
    try:
        r = int(encoded[:2], 16)
        return ''.join(chr(int(encoded[i:i+2], 16) ^ r) for i in range(2, len(encoded), 2))
    except:
        return ''
```

### 6.5 关键处理要点

1. **Cloudflare 邮箱必须在 URL 补全之前处理**: `/cdn-cgi/l/email-protection#...` 是相对路径，但不应补全为 `base_url + /cdn-cgi/...`，而应直接解密
2. **`continue` 跳过后续分类**: 解密邮箱后立即 `continue`，避免进入普通链接分类逻辑
3. **两组选择器的降级**: `.people-person` (新版) → `.media.stream-item` (旧版)
4. **排除模板链接**: `wowchemy` / `academic` 关键词过滤，避免把模板仓库链接当成个人 GitHub

**完整参考脚本**: `scripts/lab_member_scraper.py` (使用 `scrape_card_page()` 方法)

### 6.6 两阶段 Hugo Academic 变体 (列表页 → 个人页)

当 Hugo Academic 网站的卡片页只展示姓名和照片（无邮箱、无研究兴趣等详细信息）时，需要**两阶段爬取**：先从列表页提取成员 URL，再逐个访问个人页面。

**实测案例**: 清华-北大 TongClass — 154 名成员，94% 邮箱提取率。

**与卡片模式 (6.4) 的区别**:

| 维度 | 卡片模式 (PKU.AI) | 两阶段 Hugo Academic (TongClass) |
|------|-------------------|--------------------------------|
| HTTP 请求 | 1 次 | N+1 次 (1 列表 + N 详情) |
| 信息完整度 | 仅姓名/邮箱/社交链接 | 完整 (兴趣/教育/研究方向) |
| 速度 | 极快 (<1s) | 较慢 (约 0.2s × N) |
| 适用场景 | 卡片中已包含所有信息 | 卡片只有姓名，详情在个人页 |

#### 第一阶段: 列表页解析 (含分组标题)

TongClass 列表页的特殊结构: `h2` 年级标题和 `a[href*="/author/"]` 成员链接交替出现。

```python
def get_member_urls(list_url, base_url):
    """
    从 Hugo Academic 列表页提取成员 URL 和分组信息

    关键: h2 标题和 a 链接交替出现，用状态机记录当前年级
    """
    response = requests.get(list_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    members = []
    current_grade = ''
    seen_urls = set()

    for element in soup.find_all(['h2', 'a']):
        if element.name == 'h2':
            # 检测年级/分组标题 (如 "清华 23 级", "吉祥物")
            text = element.get_text(strip=True)
            if '级' in text or '吉祥物' in text:
                current_grade = text
        elif element.name == 'a':
            href = element.get('href', '')
            if '/author/' in href:
                name = element.get_text(strip=True)
                full_url = base_url + href if href.startswith('/') else href
                if name and name != 'Avatar' and full_url not in seen_urls:
                    seen_urls.add(full_url)
                    members.append({
                        'url': full_url,
                        'name': name,
                        'grade': current_grade
                    })

    return members
```

#### 第二阶段: 个人页面结构化提取

Hugo Academic 个人页面有固定的文本段落结构，可用正则提取:

```python
def extract_from_profile_page(html):
    """从 Hugo Academic 个人页面提取结构化信息"""
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()

    # --- 研究兴趣 (Interests 和 Education 之间) ---
    interests_match = re.search(
        r'Interests\s*\n([\s\S]*?)(?=Education|$)', text
    )
    if interests_match:
        raw = interests_match.group(1).strip()
        interests = ', '.join([
            s.strip() for s in raw.split('\n')
            if s.strip() and s.strip() not in ['•', '*']
        ])

    # --- 教育背景 (Education 到页脚) ---
    edu_match = re.search(
        r'Education\s*\n([\s\S]*?)(?=©|$)', text
    )
    if edu_match:
        raw = edu_match.group(1).strip()
        education = ' | '.join([
            s.strip() for s in raw.split('\n')
            if s.strip() and '©' not in s and 'Published' not in s
        ])

    # --- 大学检测 (通过 .edu 域名链接) ---
    uni_link = soup.find('a', href=re.compile(r'tsinghua\.edu|pku\.edu'))
    university = uni_link.get_text(strip=True) if uni_link else ''

    # --- 邮箱 + 社交链接 (含 Cloudflare 解密) ---
    # 复用 6.4 的链接提取逻辑
    ...
```

#### 关键处理要点

1. **URL 编码 "无" 占位符过滤**:
   ```python
   # 部分成员填写 "无" 作为社交链接
   # URL 编码后为 %e6%97%a0，需要过滤
   if '%e6%97%a0' not in href:
       profile['twitter'] = href
   ```

2. **去重 (Avatar 图片链接)**:
   ```python
   # Hugo Academic 列表页中每个人有两个 <a> 指向同一 URL
   # 一个是头像 (文本为 "Avatar")，一个是姓名
   if name and name != 'Avatar' and full_url not in seen_urls:
       ...
   ```

3. **段落终止符选择**:
   - `Interests` 段落终止于 `Education`
   - `Education` 段落终止于 `©` (Hugo 页脚版权符号)
   - 使用 `(?=...|$)` 确保即使没有终止符也能匹配到文件末尾

---

## 7. 邮箱反向定位法 (防御性爬虫策略)

### 7.1 概述

当目标网站使用**自定义 HTML**、**无固定 CSS 类名**、**结构不规范**时，传统的 CSS 选择器方法会失效。此时可以使用**邮箱反向定位法**：通过搜索邮箱文本节点（`@` 特征），向上回溯 DOM 树找到人员卡片容器。

**实测案例**: 清华 MediaLab — 39 名成员，通过 `@tsinghua.edu.cn` 反向定位人员卡片。

**核心优势**:
- 不依赖 CSS 类名 — 适用于任意 HTML 结构
- 邮箱是强特征 — 学术网站必定包含联系方式
- 防御性策略 — 当其他方法都失败时的最后手段

**适用场景**:
- 自定义 HTML 网站（非模板）
- 页面结构混乱、无规律
- CSS 类名动态生成或无意义（如 `.div1`, `.box2`）

### 7.2 核心策略

```
邮箱反向定位流程:
┌─────────────────────────────────────────────────────────────┐
│                                                              │
│  1. 搜索所有包含 @ 的文本节点                                 │
│      soup.find_all(string=re.compile(r'@'))                 │
│                                                              │
│  2. 对每个邮箱节点，向上回溯 DOM 树 (最多 4 层)              │
│      container = node.parent                                 │
│      for _ in range(4): container = container.parent        │
│                                                              │
│  3. 容器识别启发式规则                                       │
│      ├─ 必须是 div 或 li 标签                                │
│      ├─ 文本长度在 20-3000 字符之间                          │
│      └─ 去重：同一容器只处理一次                             │
│                                                              │
│  4. 从容器中提取信息                                         │
│      ├─ 姓名 (第一行，过滤头衔词)                            │
│      ├─ 邮箱 (正则匹配)                                      │
│      ├─ 头衔 (包含 Professor/PhD 等关键词的行)               │
│      └─ 社交链接 (GitHub, Scholar, LinkedIn)                │
│                                                              │
│  5. 可选：访问详情页获取更多信息                             │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### 7.3 完整实现代码

```python
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_by_email_anchor(page_url, base_url):
    """
    邮箱反向定位法：通过邮箱文本节点反向查找人员卡片

    清华 MediaLab 实测: 39 名成员，100% 提取成功
    """
    response = requests.get(page_url, timeout=15, verify=False)
    response.encoding = response.apparent_encoding or 'utf-8'
    soup = BeautifulSoup(response.text, 'html.parser')

    # 1. 查找所有包含 @ 的文本节点
    email_nodes = soup.find_all(string=re.compile(r'@'))
    print(f"发现 {len(email_nodes)} 个潜在的邮箱节点")

    processed_containers = []  # 去重
    members = []

    for node in email_nodes:
        # 2. 向上回溯，找到人员卡片容器
        container = node.parent

        # 向上找 4 层
        for _ in range(4):
            if container and (container.name == 'div' or container.name == 'li'):
                # 3. 容器识别启发式规则
                txt_len = len(container.get_text())
                if 20 < txt_len < 3000:  # 单人卡片文本长度范围
                    if container not in processed_containers:
                        processed_containers.append(container)

                        # 4. 解析该卡片
                        person = extract_from_email_card(container, base_url)

                        # 过滤无效数据
                        if person['name'] and 'Address' not in person['name']:
                            members.append(person)
                            print(f"  ✅ 提取成功: {person['name']} ({person['email']})")

                        break

            if container.parent:
                container = container.parent
            else:
                break

    return members


def extract_from_email_card(card_tag, base_url):
    """从邮箱反向定位到的卡片容器中提取信息"""
    # 提取所有文本行
    lines = [line.strip() for line in card_tag.get_text(separator="\n").split('\n') if line.strip()]

    # 提取邮箱
    email = None
    email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}')
    for line in lines:
        if "@" in line:
            match = email_pattern.search(line)
            if match:
                email = match.group(0)
                break

    # 提取姓名 (第一行，过滤掉头衔词)
    raw_name_line = lines[0] if lines else ""
    if raw_name_line in ["All Faculty", "Team", "Members"]:
        raw_name_line = lines[1] if len(lines) > 1 else ""

    # 分离中英文名
    cn_name = "".join(re.findall(r'[\u4e00-\u9fa5]+', raw_name_line))
    en_name = re.sub(r'[\u4e00-\u9fa5]+', '', raw_name_line).strip()

    # 提取头衔
    title = ""
    for line in lines:
        if any(kw in line for kw in ["Professor", "PhD", "Master", "Student"]):
            if len(line) < 50:
                title = line
                break

    # 提取详情页链接
    detail_url = None
    links = card_tag.find_all('a', href=True)
    for a in links:
        href = a['href']
        if "mailto:" not in href:
            if "http" not in href:
                detail_url = urljoin(base_url, href)
                break
            elif base_url in href:
                detail_url = href
                break

    return {
        "name": en_name or cn_name,
        "cn_name": cn_name,
        "en_name": en_name,
        "title": title,
        "email": email,
        "detail_url": detail_url
    }
```

### 7.4 关键处理要点

1. **容器识别启发式规则**:
   - 文本长度 20-3000 字符：太短是空标签，太长是整个 body
   - 必须是 `div` 或 `li` 标签：这是最常见的容器标签
   - 去重机制：同一容器只处理一次，避免重复提取

2. **中英文名分离**:
   ```python
   # 清华 MediaLab 格式: "Lu Fang 方路"
   cn_name = "".join(re.findall(r'[\u4e00-\u9fa5]+', raw_name_line))  # 方路
   en_name = re.sub(r'[\u4e00-\u9fa5]+', '', raw_name_line).strip()  # Lu Fang
   ```

3. **过滤页脚联系方式**:
   - 排除包含 "Address", "Mailbox", "Contact", "Office" 的条目
   - 这些通常是页面底部的联系信息，不是个人资料

4. **详情页深入抓取**:
   - 如果卡片中有详情页链接，可以进一步访问获取更多信息
   - 注意排除 `mailto:` 和外部链接

### 7.5 与其他方法的对比

| 方法 | 适用场景 | 优点 | 缺点 |
|------|---------|------|------|
| **CSS 选择器** | Hugo Academic 等模板网站 | 精确、快速 | 依赖固定结构 |
| **两阶段爬取** | 有明确人员链接列表 | 信息完整 | 需要 N+1 次请求 |
| **邮箱反向定位** | 自定义 HTML、无固定类名 | 通用性强、防御性好 | 可能误匹配页脚 |

**选择策略**:
```python
def choose_scraping_method(soup):
    """根据页面特征选择爬取方法"""
    # 1. 检测 Hugo Academic 模板
    if soup.select('.people-person') or soup.select('.portrait-title'):
        return 'card_mode'  # 使用 scrape_card_page()

    # 2. 检测是否有人员链接列表
    links = soup.select('a[href*="/author/"], a[href*="/people/"]')
    if len(links) > 5:
        return 'two_phase'  # 使用 scrape_lab()

    # 3. 降级到邮箱反向定位
    email_nodes = soup.find_all(string=re.compile(r'@'))
    if len(email_nodes) > 3:
        return 'email_anchor'  # 使用 scrape_by_email_anchor()

    return 'unknown'
```

**完整参考脚本**: `scripts/lab_member_scraper.py` (使用 `scrape_by_email_anchor()` 方法)

---

## 8. PDF 文本解析与邮箱提取 (PyMuPDF)

### 8.1 概述

从学术论文 PDF 中提取作者联系方式是 CVF 会议 (CVPR, ICCV, WACV) 爬虫的核心能力。与 OpenReview 的结构化 API 不同，CVF 论文的邮箱信息只存在于 PDF 首页。

**实测案例**: CVPR 2025 — 2,871 篇论文，约 85 分钟完成全量 PDF 解析。

**核心优势**:
- 从论文首页直接提取邮箱，比 OpenReview `preferredEmail` 更可能是真实使用的地址
- 内存流处理 (`io.BytesIO`)，无需落盘，避免数千次磁盘 I/O
- 双策略邮箱提取，覆盖标准格式和 LaTeX 花括号缩写格式

### 8.2 环境配置与包名陷阱

```bash
pip install PyMuPDF
```

**⚠️ 经典天坑**: PyPI 上有一个废弃的山寨包叫 `fitz` (版本 `0.0.1dev2`)。
**绝对不要** `pip install fitz`！
如果误装了:
```bash
pip uninstall -y fitz PyMuPDF && pip install PyMuPDF
```

> 在 Colab 中还需要**重启运行时** (Runtime → Restart session)，因为 Python 已将错误的包加载进内存。

### 8.3 内存流 PDF 解析

```python
import io
import fitz  # 导入名是 fitz，但安装包是 PyMuPDF

response = requests.get(pdf_url, timeout=20)

# 关键: 使用 io.BytesIO 内存流，不落盘
pdf_stream = io.BytesIO(response.content)
doc = fitz.open(stream=pdf_stream, filetype="pdf")

# 提取第一页文本
# replace('\n', ' ') 极其重要! PDF 是视觉排版，邮箱可能被断行
first_page_text = doc[0].get_text("text").replace('\n', ' ')
doc.close()
```

**MuPDF 非致命警告**:
```
MuPDF error: cannot create appearance stream for Screen annotations
```
这是 PDF 中嵌入多媒体标注的无害警告，不影响文本提取。

### 8.4 花括号缩写邮箱解析

CS 论文中常见的 LaTeX `authblk` 排版宏包会将多个作者邮箱缩写为花括号格式:

| 格式 | 示例 | 难度 |
|------|------|------|
| 标准 | `user@domain.edu` | 简单正则 |
| 基础缩写 | `{user1, user2}@domain.edu` | 花括号 + 拆分 |
| 变态缩写 | `{bguler@ece., amitrc@ece.}ucr.edu` | `@` 在括号内，域名被切断 |

```python
import re

# 花括号正则
EMAIL_REGEX_BRACKET = re.compile(
    r'\{([^}]+)\}\s*@?\s*([a-zA-Z0-9.-]*\.[a-zA-Z]{2,})'
)

bracket_matches = EMAIL_REGEX_BRACKET.findall(text)

for inside_text, domain_suffix in bracket_matches:
    users = inside_text.split(',')
    for user in users:
        # 清洗 LaTeX 角标符号 (*, †, ‡, 空格)
        user = re.sub(r'[^a-zA-Z0-9_.@+-]', '', user)
        clean_suffix = re.sub(r'[^a-zA-Z0-9_.@+-]', '', domain_suffix)

        # 智能拼接: 检测 @ 在哪一侧
        if '@' in user:
            email = user + clean_suffix       # bguler@ece. + ucr.edu
        else:
            email = user + '@' + clean_suffix  # user + @ + domain.edu

        # 修复: user@.edu → user@edu
        email = email.replace('@.', '@')
```

**完整参考脚本**: `scripts/cvf_paper_scraper.py`

---

## 9. 常见问题解决

### 8.1 编码问题

```python
# 问题: CSV 文件在 Excel 中打开乱码
# 解决: 使用 utf-8-sig 编码（带 BOM）

import csv

with open('output.csv', 'w', newline='', encoding='utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)
```

```python
# 问题: 网页编码不正确
# 解决: 手动设置编码

response = requests.get(url)
response.encoding = 'utf-8'  # 或 response.apparent_encoding
```

### 7.2 连接问题

```python
# 问题: SSL 连接错误
# 解决: 添加重试机制和超时设置

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

session = requests.Session()
retry = Retry(total=3, backoff_factor=1, status_forcelist=[500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)

response = session.get(url, timeout=15)
```

### 7.3 请求频率限制

```python
# 问题: 请求过于频繁被封
# 解决: 添加随机延迟

import time
import random

for url in urls:
    scrape(url)

    # 随机延迟 0.5-2 秒
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)
```

### 7.4 无效链接过滤

```python
# 问题: 页面模板链接干扰 (如 wowchemy)
# 解决: 过滤特定关键词

def extract_github(soup: BeautifulSoup) -> str:
    for link in soup.find_all('a', href=True):
        href = link.get('href', '')
        if 'github.com' in href.lower():
            # 排除模板链接
            if 'wowchemy' not in href.lower():
                return href
    return ''
```

---

## 8. 最佳实践总结

### 8.1 爬虫礼仪

1. **添加请求延迟**: 避免对服务器造成压力
2. **设置 User-Agent**: 模拟正常浏览器访问
3. **使用 Session**: 复用连接，提高效率
4. **遵守 robots.txt**: 检查网站是否允许爬取

### 8.2 错误处理

1. **异常捕获**: 单个页面失败不影响整体
2. **超时设置**: 避免长时间等待
3. **重试机制**: 对临时错误自动重试

### 8.3 数据处理

1. **正则表达式**: 提取结构化文本
2. **CSS 选择器**: 精确定位元素
3. **数据清洗**: 去除空白、过滤无效值

---

## 参考脚本

完整的代码模板请参见 `scripts/` 目录：

- `scripts/serper_search.py` - Serper API 搜索模板
- `scripts/httpx_scraper.py` - 异步 HTTP 爬虫
- `scripts/cloudflare_email_decoder.py` - Cloudflare 邮箱解密
- `scripts/lab_member_scraper.py` - 实验室成员批量爬取
- `scripts/openreview_scraper.py` - OpenReview 会议论文爬虫
- `scripts/cvf_paper_scraper.py` - CVF 论文爬虫 (PDF 邮箱提取)
- `scripts/github_network_scraper.py` - GitHub 社交网络爬虫

---

## 相关文档

- [URL 过滤与优先级规则](./url-priority-rules.md)
- [反爬虫解决方案](./anti-scraping-solutions.md)
- [Web Scraping Practice - TongClass](../../Note/Web-Scraping-Practice-TongClass.md)
