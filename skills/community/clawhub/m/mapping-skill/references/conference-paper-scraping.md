# 会议论文爬取指南

> 本文档记录从学术会议平台爬取论文和作者信息的完整实践经验，涵盖两大平台：
> - **OpenReview** (ICML, NeurIPS, ICLR) — 基于 ICML 2025 实战
> - **CVF Open Access** (CVPR, ICCV, WACV) — 基于 CVPR 2025 实战

---

## 概述

学术会议是发现 AI/ML 领域优秀研究者的重要渠道。通过爬取会议论文数据，可以：
1. **发现新晋作者** - 找到刚进入领域的新 PhD
2. **获取最新研究** - 了解前沿研究方向
3. **建立作者档案** - 收集联系方式和学术链接（Homepage、Scholar、GitHub 等）

---

## 支持的会议平台

| 平台 | 会议 | API 支持 | 推荐方案 |
|------|------|---------|---------|
| **OpenReview** | ICML, NeurIPS, ICLR, AAAI | ✅ 官方 Python SDK | `openreview-py` |
| **CVF Open Access** | CVPR, ICCV, WACV | ❌ 纯 HTML 爬虫 | `requests + BS4 + PyMuPDF` |
| **ACL Anthology** | ACL, EMNLP, NAACL | ⚠️ 需要爬虫 | `requests + BS4` |
| **ACM DL** | KDD, SIGIR | ⚠️ 需要爬虫 | `requests + BS4` |

### 平台选择决策

```
收到会议爬取任务
    │
    ├── ICML / NeurIPS / ICLR / AAAI
    │       └── OpenReview API (结构化数据，Profile 链接丰富)
    │           → 使用 scripts/openreview_scraper.py
    │
    ├── CVPR / ICCV / WACV
    │       └── CVF Open Access (HTML 爬虫 + PDF 邮箱提取)
    │           → 使用 scripts/cvf_paper_scraper.py
    │
    └── ACL / EMNLP / KDD / ...
            └── 参考 CVF 方案思路，定制 HTML 解析逻辑
```

---

## OpenReview 平台（重点）

### 1. 环境配置

```bash
pip install openreview-py pandas tqdm
```

### 2. 登录认证

OpenReview API 要求注册账号登录。有两种常见方式：

```python
import openreview

# 方式 1: 本地环境 (直接传入 / 环境变量)
import os
client = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net',
    username=os.getenv('OPENREVIEW_USER'),
    password=os.getenv('OPENREVIEW_PASSWORD')
)

# 方式 2: Google Colab 环境 (使用 Secrets)
from google.colab import userdata
client = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net',
    username=userdata.get('OPENREVIEW_USER'),
    password=userdata.get('OPENREVIEW_PASSWORD')
)
```

> **注意**: API base URL 必须是 `https://api2.openreview.net`（v2 API），不要用旧版 `api.openreview.net`。

### 3. 常用会议 Venue ID

```python
VENUE_IDS = {
    # ICML
    'ICML 2025': 'ICML.cc/2025/Conference',
    'ICML 2024': 'ICML.cc/2024/Conference',
    # NeurIPS
    'NeurIPS 2024': 'NeurIPS.cc/2024/Conference',
    'NeurIPS 2023': 'NeurIPS.cc/2023/Conference',
    # ICLR
    'ICLR 2025': 'ICLR.cc/2025/Conference',
    'ICLR 2024': 'ICLR.cc/2024/Conference',
}
```

> **Venue ID 格式规律**: `{会议名}.cc/{年份}/Conference`，可推断其他年份。

### 4. 获取论文列表

```python
# 核心 API 调用 - 一次性获取全部论文
submissions = client.get_all_notes(content={'venueid': VENUE_ID})
print(f"共获取到 {len(submissions)} 篇论文")
```

**实测数据**:
- ICML 2025: 3,257 篇论文，获取耗时约 1-2 分钟

### 5. 论文 Note 对象的字段结构

OpenReview 的 Note 对象字段以嵌套字典存储，需要 `.get('value')` 取值：

```python
# ⚠️ 注意：不是 note.content['title']，而是 note.content['title']['value']
title      = note.content.get('title', {}).get('value', '')
authors    = note.content.get('authors', {}).get('value', [])
author_ids = note.content.get('authorids', {}).get('value', [])
paper_link = f"https://openreview.net/forum?id={note.id}"

# 对齐作者名和 ID（有时长度不一致）
if len(authors) != len(author_ids):
    author_ids = author_ids + [''] * (len(authors) - len(author_ids))
```

### 6. Author ID 的两种形式

Author ID 有两种格式，需要分别处理：

| 类型 | 格式示例 | 含义 | 处理方式 |
|------|---------|------|---------|
| **Profile ID** | `~San_Zhang1` | 已注册 OpenReview 的用户 | 调用 `client.get_profile()` 获取详情 |
| **Email ID** | `user@email.com` | 未注册用户，由共同作者添加 | 直接用作邮箱，跳过 Profile 查询 |

```python
for name, uid in zip(authors, author_ids):
    # Email ID → 直接当邮箱用，跳过 Profile
    if '@' in uid:
        record = {
            'Author Name': name,
            'Email': uid,
            'Profile Link': 'N/A (Email User)',
            # ... 其他字段留空
        }
        continue

    # Profile ID → 查询 Profile 获取详细信息
    profile_link = f"https://openreview.net/profile?id={uid}"
    try:
        profile = client.get_profile(uid)
        links = extract_profile_links(profile)
    except Exception as e:
        links = {}  # Profile 获取失败，可能已被删除
```

### 7. Profile 对象详细字段提取

这是最关键的部分 —— 从 Profile 的 `content` 中提取各种链接和联系方式：

```python
def extract_profile_links(profile):
    """从 Profile 对象提取各种链接和联系方式"""
    data = {
        'Homepage': '',
        'Google Scholar': '',
        'DBLP': '',
        'ORCID': '',
        'GitHub': '',
        'LinkedIn': '',
        'Email': ''
    }

    if not profile or not hasattr(profile, 'content'):
        return data

    content = profile.content

    # -------- 邮箱提取（三级回退） --------
    # 优先用 preferredEmail，其次用 emails 列表第一个
    preferred = content.get('preferredEmail', '')
    emails = content.get('emails', [])
    if preferred:
        data['Email'] = preferred
    elif emails:
        data['Email'] = emails[0]
    else:
        data['Email'] = 'Hidden'  # 用户隐藏了邮箱

    # -------- 个人主页 --------
    data['Homepage'] = content.get('homepage', '')

    # -------- Google Scholar --------
    # ⚠️ OpenReview 字段名不统一！有时叫 gscholar，有时叫 google_scholar
    data['Google Scholar'] = content.get('gscholar', '') or content.get('google_scholar', '')

    # -------- DBLP --------
    data['DBLP'] = content.get('dblp', '')

    # -------- ORCID --------
    # ⚠️ 有时只存了 ORCID ID（纯数字），需要拼接完整 URL
    orcid = content.get('orcid', '')
    if orcid and 'http' not in orcid:
        data['ORCID'] = f"https://orcid.org/{orcid}"
    else:
        data['ORCID'] = orcid

    # -------- GitHub & LinkedIn --------
    data['GitHub'] = content.get('github', '')
    data['LinkedIn'] = content.get('linkedin', '')

    return data
```

**关键踩坑点**:

| 字段 | 问题 | 解决方案 |
|------|------|---------|
| `email` | `preferredEmail` 可能为空 | 三级回退：`preferredEmail → emails[0] → 'Hidden'` |
| `google_scholar` | 字段名不统一 | 同时检查 `gscholar` 和 `google_scholar` |
| `orcid` | 有时只存 ID 不存 URL | 判断是否含 `http`，缺则拼接 `https://orcid.org/` |
| `emails` | 是列表类型 | 取 `emails[0]` 作为主邮箱 |

---

## 华人作者识别

### 简单姓氏匹配法（推荐，速度快）

实际生产中使用的方案 —— 仅靠姓氏判断，简单高效：

```python
# 常见华人姓氏拼音 Top 70
CHINESE_SURNAMES = set([
    'li', 'wang', 'zhang', 'liu', 'chen', 'yang', 'huang', 'zhao', 'wu', 'zhou',
    'xu', 'sun', 'ma', 'zhu', 'hu', 'guo', 'he', 'gao', 'lin', 'luo', 'cheng',
    'zheng', 'xie', 'tang', 'deng', 'feng', 'han', 'cao', 'zeng', 'peng',
    'xiao', 'cai', 'pan', 'tian', 'dong', 'yuan', 'jiang', 'ye', 'wei', 'su',
    'lu', 'ding', 'ren', 'tan', 'jia', 'liao', 'yao', 'xiong', 'jin', 'wan',
    'xia', 'fu', 'fang', 'bai', 'zou', 'meng', 'qin', 'qiu', 'hou', 'jiang',
    'shi', 'xue', 'mu', 'gu', 'du', 'qian', 'sun', 'song', 'dai', 'fan'
])

def is_likely_chinese(name):
    """判断姓名是否可能是华人（简单姓氏匹配）"""
    if not name:
        return False
    parts = name.strip().lower().split()
    if len(parts) < 2:
        return False
    # 假设姓在最后（英文格式：FirstName LastName）
    return parts[-1] in CHINESE_SURNAMES
```

> **实测效果**: ICML 2025 共 3,257 篇论文，用此方法识别出 8,221 条华人作者记录。

### 多维度评分法（高精度场景）

当需要更精确的识别时，可使用多维度评分，详见 `references/chinese-surnames.md`：

```python
def chinese_score(name, institution='', profile_id=''):
    """多维度华人识别评分 (0.0 - 1.0)"""
    score = 0.0
    # 1. 姓氏匹配 (40%)
    if is_likely_chinese(name): score += 0.4
    # 2. 机构匹配 (35%) - 中国大陆/港澳台高校
    if any(inst in institution.lower() for inst in chinese_institutions): score += 0.35
    # 3. 名字结构 (15%) - 华人名字拼音通常较短
    if len(first_name) <= 4 and first_name.isalpha(): score += 0.15
    # 4. Profile ID 模式 (10%) - ~开头的 OpenReview ID
    if profile_id and profile_id.startswith('~'): score += 0.1
    return min(score, 1.0)  # 阈值 >= 0.5 判定为华人
```

---

## 完整爬取流程

### 端到端示例（基于 ICML 2025 实战代码）

```python
import openreview
import pandas as pd
from tqdm import tqdm
import time

# ============ 配置 ============
VENUE_ID = 'ICML.cc/2025/Conference'
OUTPUT_FILE = 'ICML2025_Chinese_Authors.csv'

# ============ 登录 ============
client = openreview.api.OpenReviewClient(
    baseurl='https://api2.openreview.net',
    username='...',
    password='...'
)

# ============ 获取论文 ============
submissions = client.get_all_notes(content={'venueid': VENUE_ID})
print(f"共获取到 {len(submissions)} 篇论文")

# ============ 遍历提取 ============
results = []

for note in tqdm(submissions):
    try:
        title = note.content.get('title', {}).get('value', '')
        authors = note.content.get('authors', {}).get('value', [])
        author_ids = note.content.get('authorids', {}).get('value', [])
        paper_link = f"https://openreview.net/forum?id={note.id}"

        # 对齐
        if len(authors) != len(author_ids):
            author_ids += [''] * (len(authors) - len(author_ids))

        for name, uid in zip(authors, author_ids):
            # 筛选华人
            if not is_likely_chinese(name):
                continue

            # Email ID → 直接记录
            if '@' in uid:
                results.append({
                    'Paper Title': title,
                    'Author Name': name,
                    'OpenReview Link': paper_link,
                    'Profile Link': 'N/A (Email User)',
                    'Email': uid,
                    'Homepage': '', 'Google Scholar': '', 'DBLP': '',
                    'ORCID': '', 'GitHub': ''
                })
                continue

            # Profile ID → 查询详情
            profile_link = f"https://openreview.net/profile?id={uid}"
            try:
                profile = client.get_profile(uid)
                links = extract_profile_links(profile)
                results.append({
                    'Paper Title': title,
                    'Author Name': name,
                    'OpenReview Link': paper_link,
                    'Profile Link': profile_link,
                    **links
                })
            except Exception:
                results.append({
                    'Paper Title': title,
                    'Author Name': name,
                    'OpenReview Link': paper_link,
                    'Profile Link': profile_link,
                    'Email': 'Error Fetching Profile',
                    'Homepage': '', 'Google Scholar': '', 'DBLP': '',
                    'ORCID': '', 'GitHub': ''
                })

    except Exception:
        continue

# ============ 保存 ============
df = pd.DataFrame(results)
df.to_csv(OUTPUT_FILE, index=False, encoding='utf-8-sig')
print(f"总计: {len(df)} 条")
print(f"Homepage: {len(df[df['Homepage'] != ''])}")
print(f"Google Scholar: {len(df[df['Google Scholar'] != ''])}")
```

---

## 性能与优化

### 实测性能基准（ICML 2025）

```
平台: Google Colab (免费版)
论文总数: 3,257 篇
华人作者记录: 8,221 条
处理速度: 4.73 it/s (每篇论文约 0.21 秒)
总耗时: 11 分 29 秒
包含 Homepage: 6,013 (73%)
包含 Google Scholar: 5,891 (72%)
```

### 优化建议

1. **作者缓存**: 同一作者可能出现在多篇论文中，缓存 Profile 可减少 API 调用

```python
profile_cache = {}
if uid not in profile_cache:
    profile_cache[uid] = client.get_profile(uid)
profile = profile_cache[uid]
```

2. **调试模式**: 先用少量论文验证逻辑

```python
# 快速测试 50 篇
target_submissions = submissions[:50]
# 全量运行
target_submissions = submissions
```

3. **速率控制**: OpenReview 有速率限制，建议加 `time.sleep(0.05~0.1)`，但实测不加也能跑通

---

## Google Colab 部署要点

在 Colab 环境下使用有几个特殊注意事项：

```python
# 1. Secrets 管理 (不要硬编码密码！)
from google.colab import userdata
user = userdata.get('OPENREVIEW_USER')
password = userdata.get('OPENREVIEW_PASSWORD')

# 2. 文件下载 (爬取完自动弹出下载)
from google.colab import files
files.download(OUTPUT_FILE)

# 3. CSV 编码 (Excel 兼容)
df.to_csv(OUTPUT_FILE, encoding='utf-8-sig')  # 带 BOM 头
```

---

## 参考脚本

- OpenReview 会议爬虫: `scripts/openreview_scraper.py`
- CVF 论文爬虫: `scripts/cvf_paper_scraper.py`

---

## CVF Open Access 平台（CVPR / ICCV / WACV）

> 基于 CVPR 2025 全量爬取实战 (2,871 篇论文, 耗时约 85 分钟)

### 1. 平台特点

CVF Open Access (`openaccess.thecvf.com`) 与 OpenReview 的核心区别：

| 维度 | OpenReview | CVF Open Access |
|------|-----------|-----------------|
| 数据获取 | Python SDK (API) | HTML 爬虫 (BeautifulSoup) |
| 作者联系方式 | Profile API 返回 | 需从 PDF 首页提取 |
| 邮箱来源 | `preferredEmail` 字段 | PDF 文本中的邮箱字符串 |
| 机构信息 | Profile 中的 `history` | 从邮箱域名推断 |
| 认证要求 | 需要 OpenReview 账号 | 无需登录，完全公开 |
| 速度 | 快 (~0.2s/篇，API 调用) | 慢 (~1.8s/篇，需下载 PDF) |

### 2. 环境配置

```bash
pip install requests beautifulsoup4 PyMuPDF pandas tqdm
```

**⚠️ PyMuPDF 包名冲突陷阱**:

PyPI 上有一个废弃的山寨包 `fitz` (版本 `0.0.1dev2`)。如果误装会报错:
```
ModuleNotFoundError: No module named 'tools'
```

修复方法:
```bash
pip uninstall -y fitz PyMuPDF && pip install PyMuPDF
```

> 在 Google Colab 中需要额外步骤: 卸载后**必须重启运行时** (Runtime → Restart session)，
> 因为 Python 已将错误的包加载进内存。

### 3. 常用会议 URL 路径

```python
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
```

> **URL 格式规律**: `https://openaccess.thecvf.com/{会议名}{年份}?day=all`，可推断其他年份。

### 4. 第一阶段: HTML 元数据提取

CVF 网页是纯静态 HTML，结构固定:

```html
<dt class="ptitle"><a href="/content...">论文标题</a></dt>
<dd><a>作者1</a>, <a>作者2</a>, <a>作者3</a></dd>
<dd><a href="/content.../paper.pdf">pdf</a></dd>
```

**核心技巧: BeautifulSoup 兄弟节点漫游法**

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(response.text, 'html.parser')
paper_nodes = soup.find_all('dt', class_='ptitle')

for dt in paper_nodes:
    title = dt.text.strip()

    # 核心: find_next_sibling() 定位兄弟 <dd> 节点
    author_dd = dt.find_next_sibling('dd')
    authors = [a.text.strip() for a in author_dd.find_all('a') if a.text.strip()]

    pdf_dd = author_dd.find_next_sibling('dd')
    pdf_a = pdf_dd.find('a', string='pdf')
    pdf_link = BASE_URL + pdf_a['href']
```

> **工程经验**: 不要用正则匹配 HTML! 使用 DOM 树的父子/兄弟关系进行相对定位最稳妥。

### 5. 第二阶段: PDF 内存流解析

从 PDF 首页提取邮箱和机构信息。

**性能优化: 内存流处理 (io.BytesIO)**

传统做法是下载 PDF 到磁盘再读取，但爬取 2,871 篇论文会产生数千次磁盘 I/O。
使用内存流，PDF 数据从网络直接进入内存，由 PyMuPDF 解析，全程无磁盘写入。

```python
import io
import fitz  # PyMuPDF

response = requests.get(pdf_url, timeout=20)
pdf_stream = io.BytesIO(response.content)    # 内存流
doc = fitz.open(stream=pdf_stream, filetype="pdf")

# 提取第一页文本，去换行防止邮箱被截断
first_page_text = doc[0].get_text("text").replace('\n', ' ')
doc.close()
```

> **关键细节**: `replace('\n', ' ')` 必须做! PDF 是视觉排版格式，长邮箱会被强行断行。

**MuPDF 非致命警告**:
```
MuPDF error: unsupported error: cannot create appearance stream for Screen annotations
```
这是 PDF 中嵌入多媒体标注的警告，不影响文本提取，可以安全忽略。

### 6. 邮箱提取双策略 (核心技术突破)

CS 论文中的邮箱格式远比想象中复杂:

| 难度 | 格式示例 | 说明 |
|------|---------|------|
| Lv1 | `zhangsan@wayne.edu` | 标准格式，普通正则即可 |
| Lv2 | `{zhangsan, lisi}@wayne.edu` | 基础花括号缩写 |
| Lv3 | `{bguler@ece., amitrc@ece.}ucr.edu` | `@` 符号在括号内，域名被切断 |

**策略 1: 标准邮箱正则**
```python
import re
EMAIL_REGEX_STD = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
std_emails = re.findall(EMAIL_REGEX_STD, text)
```

**策略 2: 花括号缩写邮箱解析引擎**

```python
# 匹配 {内容}@?域名后缀
EMAIL_REGEX_BRACKET = r'\{([^}]+)\}\s*@?\s*([a-zA-Z0-9.-]*\.[a-zA-Z]{2,})'

bracket_matches = re.findall(EMAIL_REGEX_BRACKET, text)

for inside_text, domain_suffix in bracket_matches:
    users = inside_text.split(',')
    for user in users:
        # 清洗 LaTeX 角标符号 (*, †, ‡)
        user = re.sub(r'[^a-zA-Z0-9_.@+-]', '', user)
        clean_suffix = re.sub(r'[^a-zA-Z0-9_.@+-]', '', domain_suffix)

        # 智能拼接: 检测 @ 在哪一侧
        if '@' in user:
            email = user + clean_suffix       # bguler@ece. + ucr.edu
        else:
            email = user + '@' + clean_suffix  # zhangsan + @ + wayne.edu

        # 修复双点: user@.edu → user@edu
        email = email.replace('@.', '@')

        # 最终验证
        if re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
            final_emails.append(email.lower())
```

**花括号正则详解**:
- `\{([^}]+)\}` — 捕获 `{}` 里的全部内容 (Group 1: 前缀)
- `\s*@?\s*` — 容错: `{}` 和域名之间可能有 `@`、空格，也可能没有
- `([a-zA-Z0-9.-]*\.[a-zA-Z]{2,})` — 捕获域名后缀 (Group 2)

### 7. 机构推断

从邮箱域名中提取学术机构:

```python
def infer_institutions(emails):
    institutions = set()
    for email in emails:
        domain = email.split('@')[-1]
        if '.edu' in domain or '.ac' in domain:
            institutions.add(domain)
    return list(institutions)
```

### 8. 防御性编程

爬取近 3,000 篇论文耗时约 85 分钟，必须确保不会因单个错误而中断:

1. **请求超时**: `requests.get(..., timeout=20)`
2. **状态码检查**: `response.raise_for_status()` 拦截 404 等错误
3. **try-except 护航**: 每篇论文的解析都在 `try-except` 中，失败只记录状态，不中断循环
4. **礼貌爬虫**: `time.sleep(1)` — 每秒最多一个 PDF 请求，避免被封

### 9. 实测性能基准 (CVPR 2025)

```
平台: Google Colab (免费版)
论文总数: 2,871 篇
处理速度: ~1.78 s/篇 (主要耗时在 PDF 下载)
总耗时: 约 85 分钟
MuPDF 非致命警告: 多处 (Screen annotations, cmsOpenProfileFromMem) — 不影响结果
最终输出: CSV (标题, 作者, 论文链接, PDF链接, 邮箱, 机构)
```

### 10. 与 OpenReview 方案的互补

| 场景 | 推荐方案 | 原因 |
|------|---------|------|
| ICML / NeurIPS / ICLR | OpenReview API | 结构化数据，Profile 链接丰富 (Homepage 73%, Scholar 72%) |
| CVPR / ICCV / WACV | CVF HTML + PDF | 无 API，但 PDF 中邮箱和机构更直接 |
| 需要 Homepage/Scholar/GitHub | OpenReview API | Profile 字段直接返回 |
| 需要精确邮箱 | CVF PDF 提取 | 论文首页的邮箱比 OpenReview `preferredEmail` 更可能是真实使用的 |
| 两个平台都有的会议 | 两者结合 | OpenReview 提供 Profile 链接，CVF 提供 PDF 邮箱，互相补充 |

---

## 相关文档

- [华人姓氏数据库](./chinese-surnames.md) - 200+ 姓氏 + 港台粤语变体
- [URL 过滤与优先级规则](./url-priority-rules.md)
- [候选人去重规则](./deduplication-rules.md)
