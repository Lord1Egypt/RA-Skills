# 反爬虫解决方案汇总

> 本文档汇总了在进行 AI 人才搜索时遇到的常见反爬虫机制及其解决方案。

---

## 概述

在爬取 researcher 个人主页和实验室页面时，经常会遇到各种反爬虫机制。本文档按照问题类型分类，提供对应的解决方案。

---

## 问题分类与解决方案

### 1. Cloudflare 邮箱保护

#### 问题描述

网站使用 Cloudflare CDN 的邮箱保护功能，邮箱地址被替换为加密字符串：

```html
<!-- 原始邮箱: example@domain.com -->
<a href="/cdn-cgi/l/email-protection#0762637474346762637474342964686a">
    [email protected]
</a>
```

#### 解决方案

**XOR 解密算法**（免费）：

```python
def decode_cloudflare_email(encoded: str) -> str:
    """
    解码 Cloudflare 邮箱保护

    原理: Cloudflare 使用简单的 XOR 加密
    - 第一个字节是密钥
    - 后续字节与密钥 XOR 得到原始字符
    """
    try:
        key = int(encoded[:2], 16)
        decoded = ''
        for i in range(2, len(encoded), 2):
            char_code = int(encoded[i:i+2], 16) ^ key
            decoded += chr(char_code)
        return decoded
    except:
        return ''


# 使用示例
href = "/cdn-cgi/l/email-protection#0762637474346762637474342964686a"
encoded = href.split('#')[-1]
email = decode_cloudflare_email(encoded)
print(email)  # 输出: example@domain.com
```

**完整参考实现**: `scripts/cloudflare_email_decoder.py`

**实战案例**:
- **PKU.AI**: 65 名成员中，30+ 个 Cloudflare 加密邮箱成功解密（成功率 ~95%）
- **清华 THUNLP**: 邮箱格式 `xxx@mails.tsinghua.edu.cn`

**在 Hugo Academic 卡片页中的集成**: 当遍历 `.network-icon a` 链接时，检测 `email-protection` 关键词后直接解密，无需额外请求：

```python
for link in card.select('.network-icon a'):
    href = link.get('href', '')
    if 'email-protection' in href:
        encoded = href.split('#')[-1]
        email = decode_cloudflare_email(encoded)
        continue  # 跳过后续链接分类
```

#### 成功率

| 方案 | 成功率 | 成本 |
|------|--------|------|
| XOR 解密 | 95%+ | 免费 |
| BrightData MCP | 99%+ | 付费 |

**Cloudflare 邮箱保护的调试决策路径** (基于 TongClass 实战):

当遇到 Cloudflare 邮箱保护时，不要直接上 Selenium/Playwright，按以下顺序排查:

```
1. requests + BS4 → 邮箱为空
   ↓ 检查 HTML: 发现 /cdn-cgi/l/email-protection#...
   ↓
2. 尝试 Selenium → 可能在 Windows 上 WebDriver 报错
   ↓ 不要继续调试 Selenium，换思路
   ↓
3. 关键认知: Cloudflare 邮箱保护只是客户端 XOR 加密
   ↓ 密文已经在 HTML 中，不需要执行 JavaScript!
   ↓
4. 直接用 XOR 解密 → 成功!
   ↓ 密钥 = 十六进制字符串的前 2 位
```

> **核心洞察**: Cloudflare Email Protection 不是服务端加密，密文和密钥都在 HTML 里。
> `requests` 拿到的 HTML 就足以解密，完全不需要浏览器自动化。

---

### 2. 邮箱文本混淆（中国高校常见）

#### 问题描述

许多中国高校网站（如南大 LAMDA、清华 THUNLP 等）不使用 Cloudflare，而是直接在 HTML 文本中将 `@` 替换为 `[at]` 或 `(at)` 来防止垃圾邮件抓取：

```html
<!-- 原始邮箱: zhangsx@lamda.nju.edu.cn -->
<p>Email: zhangsx [at] lamda.nju.edu.cn</p>
```

#### 解决方案

**正则表达式匹配**（免费，简单有效）：

```python
import re

def extract_obfuscated_email(text):
    """
    提取 [at]/(at) 混淆的邮箱地址

    支持格式:
    - user [at] domain.edu.cn
    - user(at)domain.edu.cn
    - user [at] domain.edu.cn  (含多余空格)
    """
    pattern = r'([a-zA-Z0-9._-]+)\s*(?:\[at\]|@|\(at\))\s*([a-zA-Z0-9._-]+\.[a-zA-Z]{2,})'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return f"{match.group(1)}@{match.group(2)}"
    return ''

# 使用示例
text = "Email: zhangsx [at] lamda.nju.edu.cn"
email = extract_obfuscated_email(text)  # zhangsx@lamda.nju.edu.cn
```

**完整的邮箱提取策略**（优先级从高到低）：

```python
def extract_email_all_methods(soup, text_content):
    """综合邮箱提取，覆盖所有常见混淆方式"""
    # 1. mailto 链接 (最可靠)
    mailto = soup.select_one('a[href^="mailto:"]')
    if mailto:
        return mailto['href'].replace('mailto:', '').strip()

    # 2. Cloudflare 保护 (XOR 解密)
    cf_link = soup.select_one('a[href*="/cdn-cgi/l/email-protection"]')
    if cf_link:
        encoded = cf_link['href'].split('#')[-1]
        return decode_cloudflare_email(encoded)

    # 3. [at] / (at) 混淆 (中国高校常见)
    at_pattern = r'([a-zA-Z0-9._-]+)\s*(?:\[at\]|\(at\))\s*([a-zA-Z0-9._-]+\.[a-zA-Z]{2,})'
    match = re.search(at_pattern, text_content, re.IGNORECASE)
    if match:
        return f"{match.group(1)}@{match.group(2)}"

    # 4. 纯文本正则 (最后手段，可能误匹配)
    email_pattern = r'[\w.-]+@[\w.-]+\.\w+'
    match = re.search(email_pattern, text_content)
    if match:
        return match.group()

    return ''
```

#### 常见域名

| 高校 | 邮箱域名 | 混淆方式 |
|------|---------|---------|
| 南大 LAMDA | `lamda.nju.edu.cn` | `[at]` |
| 清华 | `mails.tsinghua.edu.cn` | Cloudflare XOR |
| 北大 PKU.AI | `stu.pku.edu.cn` | Cloudflare XOR |
| 北大 PKU.AI (外部) | `gmail.com`, `outlook.com` 等 | Cloudflare XOR |
| 通用 | `*.edu.cn` | 各种 |

---

### 2.5 URL 编码占位符过滤（Hugo Academic 常见）

#### 问题描述

部分 Hugo Academic 网站的成员在社交链接字段中填写了中文 "无" 作为占位符。这些文字在 URL 中被编码为 `%e6%97%a0`，导致提取出无效的社交链接：

```html
<!-- 成员填写了 "无" 作为 Twitter 链接 -->
<a href="https://twitter.com/%e6%97%a0">Twitter</a>
```

#### 解决方案

```python
# 过滤 URL 编码的中文 "无" 占位符
if '%e6%97%a0' not in href:
    profile['twitter'] = href
```

**实战案例**: TongClass — 154 名成员中多人填写 "无" 作为 Twitter/LinkedIn 占位符。

> **经验**: 任何从表单收集数据的学术网站都可能有此问题。除了 "无"，还可能出现 "N/A"、"none" 等占位符，建议统一过滤:
> ```python
> PLACEHOLDER_PATTERNS = ['%e6%97%a0', '/none', '/n/a', '/null']
> if not any(p in href.lower() for p in PLACEHOLDER_PATTERNS):
>     profile['twitter'] = href
> ```

---

### 3. PDF 花括号缩写邮箱（CS 论文 LaTeX 排版）

#### 问题描述

CS 领域论文（特别是 CVPR, ICCV 等 CVF 会议）使用 LaTeX `authblk` 宏包排版时，会将多个作者邮箱缩写为花括号格式。这不是反爬虫，而是 PDF 文本提取时遇到的数据格式挑战：

```
# 基础缩写
{zhangsan, lisi}@wayne.edu

# 变态缩写 (@ 符号在括号内，域名被切断)
{bguler@ece., amitrc@ece.}ucr.edu
```

#### 解决方案

**花括号正则 + 智能拼接引擎**（免费）：

```python
import re

# 匹配花括号结构: {内容}@?域名
EMAIL_REGEX_BRACKET = re.compile(
    r'\{([^}]+)\}\s*@?\s*([a-zA-Z0-9.-]*\.[a-zA-Z]{2,})'
)

def parse_bracket_emails(text):
    """解析花括号缩写邮箱"""
    results = []
    for inside_text, domain_suffix in EMAIL_REGEX_BRACKET.findall(text):
        users = inside_text.split(',')
        for user in users:
            # 清洗 LaTeX 角标符号 (*, †, ‡)
            user = re.sub(r'[^a-zA-Z0-9_.@+-]', '', user)
            suffix = re.sub(r'[^a-zA-Z0-9_.@+-]', '', domain_suffix)

            if not user:
                continue

            # 智能拼接: 检测 @ 在哪一侧
            if '@' in user:
                email = user + suffix       # bguler@ece. + ucr.edu
            else:
                email = user + '@' + suffix  # user + @ + domain.edu

            email = email.replace('@.', '@')  # 修复双点

            if re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
                results.append(email.lower())
    return results
```

**完整参考实现**: `scripts/cvf_paper_scraper.py` (`extract_emails_from_text()`)

**实战案例**:
- **CVPR 2025**: 2,871 篇论文全量爬取，成功解析包含花括号的邮箱格式

#### 成功率

| 方案 | 成功率 | 成本 |
|------|--------|------|
| 标准正则 (仅 Lv1) | 70% | 免费 |
| 标准正则 + 花括号解析 (Lv1-3) | 95%+ | 免费 |

---

### 4. PyMuPDF 包名冲突（Python 环境陷阱）

#### 问题描述

在 Python 中处理 PDF 时需要导入 `fitz`（PyMuPDF 的导入名），但 PyPI 上有一个废弃的同名山寨包 `fitz` (版本 `0.0.1dev2`)。如果误装了山寨包：

```
import fitz
# → ModuleNotFoundError: No module named 'tools'
```

#### 解决方案

```bash
# 1. 卸载山寨包和残留
pip uninstall -y fitz PyMuPDF

# 2. 安装正版 PyMuPDF
pip install PyMuPDF
```

> **Colab 特别注意**: 卸载后必须**重启运行时** (Runtime → Restart session)，
> 因为 Python 已将错误的包加载进内存，仅 pip uninstall 无法清除。

#### 预防措施

```python
# 在代码中添加明确的导入检查
try:
    import fitz
    # 检查是否为真正的 PyMuPDF (版本号应 >= 1.x)
    assert hasattr(fitz, 'open'), "安装了错误的 fitz 包，请运行: pip install PyMuPDF"
except ImportError:
    raise ImportError("请安装 PyMuPDF: pip install PyMuPDF (不是 pip install fitz!)")
```

---

### 5. SSL 握手失败（中国 .edu.cn 常见）

#### 问题描述

部分中国高校网站的 SSL 配置不标准，请求时会触发握手失败：

```
SSLError: [SSL: SSLV3_ALERT_HANDSHAKE_FAILURE] sslv3 alert handshake failure
```

**典型触发场景**: 爬取成员列表时，URL 中混入了 `http://www.nju.edu.cn` 等校主页链接。

#### 解决方案

```python
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.ssl_ import create_urllib3_context

# 方案 1: 跳过 SSL 验证 (简单粗暴)
response = requests.get(url, verify=False, timeout=10)

# 方案 2: 捕获异常并跳过 (推荐)
try:
    response = requests.get(url, timeout=10)
except requests.exceptions.SSLError:
    print(f"SSL 错误，跳过: {url}")
    # 可选：尝试 http 而非 https
    if url.startswith('https://'):
        response = requests.get(url.replace('https://', 'http://'), timeout=10)
```

**预防措施**: 在爬取前过滤掉已知有 SSL 问题的域名：

```python
SSL_PROBLEM_DOMAINS = ['www.nju.edu.cn', 'www.tsinghua.edu.cn']  # 根据实际经验积累

def should_skip_url(url):
    return any(d in url for d in SSL_PROBLEM_DOMAINS)
```

---

### 4. User-Agent 检测

#### 问题描述

服务器检测请求的 User-Agent，拒绝非浏览器请求：

```
HTTP 403 Forbidden
```

#### 解决方案

**设置真实浏览器 User-Agent**：

```python
import requests

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
})

response = session.get(url)
```

**随机 User-Agent 轮换**：

```python
import random

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
]

def get_random_ua():
    return random.choice(USER_AGENTS)
```

#### 成功率

| 方案 | 成功率 | 成本 |
|------|--------|------|
| 固定 User-Agent | 70% | 免费 |
| 随机 User-Agent | 85% | 免费 |
| BrightData MCP | 99%+ | 付费 |

---

### 3. 请求频率限制

#### 问题描述

服务器限制请求频率，过于频繁的请求会被暂时封禁：

```
HTTP 429 Too Many Requests
```

#### 解决方案

**随机延迟**：

```python
import time
import random

for url in urls:
    scrape(url)
    # 随机延迟 0.5-2 秒
    delay = random.uniform(0.5, 2.0)
    time.sleep(delay)
```

**指数退避重试**：

```python
import time

def scrape_with_retry(url, max_retries=3):
    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=15)
            if response.status_code == 429:
                # 指数退避
                wait_time = (2 ** attempt) + random.random()
                print(f"Rate limited, waiting {wait_time:.1f}s...")
                time.sleep(wait_time)
                continue
            return response
        except Exception as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)
    return None
```

**使用 Session 复用连接**：

```python
session = requests.Session()
# 复用 session 减少连接开销
for url in urls:
    response = session.get(url)
```

#### 建议配置

| 目标类型 | 建议延迟 | 并发数 |
|---------|---------|--------|
| 个人主页 | 0.5-1s | 5-10 |
| 大学网站 | 1-2s | 3-5 |
| LinkedIn | N/A (用 BrightData) | 1 |

---

### 4. IP 封锁

#### 问题描述

服务器检测到异常请求模式后封锁 IP：

```
HTTP 403 Forbidden
Connection timed out
```

#### 解决方案

**方案 1: 降低请求频率**

```python
# 使用更长的延迟
time.sleep(random.uniform(2, 5))
```

**方案 2: 使用代理池**（付费）

```python
import requests

proxies = {
    'http': 'http://proxy-server:port',
    'https': 'https://proxy-server:port',
}

response = requests.get(url, proxies=proxies)
```

**方案 3: BrightData MCP**（推荐）

对于高反爬网站，直接使用 BrightData 服务：

```python
# BrightData 会自动处理 IP 轮换
# 使用 mcp__brightdata__scrape_as_markdown 工具
```

#### 成本对比

| 方案 | 成本 | 可靠性 |
|------|------|--------|
| 降低频率 | 免费 | 中等 |
| 代理池 | $10-50/月 | 较高 |
| BrightData | $50+/月 | 最高 |

---

### 5. JavaScript 渲染

#### 问题描述

页面内容通过 JavaScript 动态加载，直接请求 HTML 无法获取完整内容：

```python
response = requests.get(url)
# response.text 不包含动态加载的内容
```

#### 解决方案

**方案 1: Playwright**（免费）

```python
from playwright.sync_api import sync_playwright

def scrape_dynamic(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url, wait_until='networkidle')

        # 等待特定元素加载
        page.wait_for_selector('.profile-content')

        content = page.content()
        browser.close()
        return content
```

**方案 2: Selenium**（免费）

```python
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def scrape_with_selenium(url):
    options = Options()
    options.add_argument('--headless')

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    # 等待页面加载
    time.sleep(3)

    content = driver.page_source
    driver.quit()
    return content
```

**方案 3: BrightData Scraping Browser**（付费）

```python
# 使用 mcp__brightdata__scraping_browser_* 工具
# 自动处理 JavaScript 渲染
```

#### 对比

| 方案 | 速度 | 资源占用 | 成本 |
|------|------|---------|------|
| Playwright | 快 | 中等 | 免费 |
| Selenium | 较慢 | 高 | 免费 |
| BrightData | 快 | 无 | 付费 |

---

### 6. 登录要求

#### 问题描述

部分网站（如 LinkedIn）需要登录才能查看完整信息。

#### 解决方案

**唯一推荐方案: BrightData MCP**

```python
# LinkedIn 必须使用 BrightData
# 工具: mcp__brightdata__web_data_linkedin_person_profile

# 对于 LinkedIn，不要尝试使用 Python 直接爬取
# 成功率极低且可能违反服务条款
```

**哪些网站必须用 BrightData**：

| 网站 | 必须用 BrightData | 原因 |
|------|------------------|------|
| LinkedIn | ✅ | 登录要求 + 高反爬 |
| Twitter/X | ✅ | 登录要求 |
| Facebook | ✅ | 登录要求 |
| 学术网站 | ❌ | 通常公开 |

---

### 7. 无固定 CSS 类名（自定义 HTML）

#### 问题描述

部分学术网站使用自定义 HTML，没有固定的 CSS 类名（如 `.people-person`），或者类名无意义（如 `.div1`, `.box2`），导致传统的 CSS 选择器方法失效。

**典型场景**: 清华 MediaLab 等自定义 HTML 网站，页面结构混乱，无法通过 CSS 选择器定位人员卡片。

#### 解决方案

**邮箱反向定位法**（免费，防御性策略）：

```python
import re
from bs4 import BeautifulSoup

def scrape_by_email_anchor(page_url, base_url):
    """
    通过邮箱文本节点反向查找人员卡片容器

    核心策略:
    1. 搜索所有包含 @ 的文本节点
    2. 向上回溯 DOM 树 (最多 4 层)
    3. 容器识别启发式规则:
       - 必须是 div 或 li 标签
       - 文本长度在 20-3000 字符之间
       - 去重：同一容器只处理一次
    """
    soup = BeautifulSoup(html, 'html.parser')

    # 1. 查找所有包含 @ 的文本节点
    email_nodes = soup.find_all(string=re.compile(r'@'))

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

                        # 解析该卡片
                        person = extract_from_container(container)
                        members.append(person)
                        break

            if container.parent:
                container = container.parent
            else:
                break

    return members


def extract_from_container(card_tag):
    """从容器中提取信息"""
    lines = [line.strip() for line in card_tag.get_text(separator="\n").split('\n') if line.strip()]

    # 提取邮箱
    email_pattern = re.compile(r'[\w\.-]+@[\w\.-]+\.[a-zA-Z]{2,}')
    email = None
    for line in lines:
        if "@" in line:
            match = email_pattern.search(line)
            if match:
                email = match.group(0)
                break

    # 提取姓名 (第一行，过滤掉头衔词)
    raw_name = lines[0] if lines else ""
    if raw_name in ["All Faculty", "Team", "Members"]:
        raw_name = lines[1] if len(lines) > 1 else ""

    # 分离中英文名
    cn_name = "".join(re.findall(r'[\u4e00-\u9fa5]+', raw_name))
    en_name = re.sub(r'[\u4e00-\u9fa5]+', '', raw_name).strip()

    return {
        "name": en_name or cn_name,
        "cn_name": cn_name,
        "en_name": en_name,
        "email": email
    }
```

**完整参考实现**: `scripts/lab_member_scraper.py` (`scrape_by_email_anchor()` 方法)

#### 实战案例

**清华 MediaLab**: 39 名成员，通过 `@tsinghua.edu.cn` 反向定位人员卡片，100% 提取成功。

**关键处理要点**:
1. **容器识别启发式**: 文本长度 20-3000 字符，太短是空标签，太长是整个 body
2. **中英文名分离**: `re.findall(r'[\u4e00-\u9fa5]+')` 提取中文，`re.sub` 去除中文得到英文
3. **过滤页脚联系方式**: 排除包含 "Address", "Mailbox", "Contact" 的条目
4. **去重机制**: 同一容器只处理一次，避免重复提取

#### 成功率

| 方案 | 成功率 | 成本 | 适用场景 |
|------|--------|------|---------|
| CSS 选择器 | 95%+ | 免费 | 模板网站 (Hugo Academic 等) |
| 邮箱反向定位 | 90%+ | 免费 | 自定义 HTML、无固定类名 |
| BrightData MCP | 99%+ | 付费 | 高反爬网站 |

---

## 决策流程图

```
┌─────────────────────────────────────────────────────────────┐
│                    遇到反爬虫问题                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 识别问题类型                                             │
│      │                                                       │
│      ├─> 邮箱显示 [email protected]                          │
│      │       └─> 使用 Cloudflare XOR 解密 (免费)             │
│      │                                                       │
│      ├─> 邮箱显示 user [at] domain.edu.cn                    │
│      │       └─> 正则匹配 \[at\]|\(at\) 并替换为 @ (免费)    │
│      │                                                       │
│      ├─> PDF 中花括号邮箱 {user@sub.}domain.edu              │
│      │       └─> 花括号正则 + 智能拼接引擎 (免费)             │
│      │                                                       │
│      ├─> import fitz 报错 "No module named 'tools'"          │
│      │       └─> pip uninstall fitz && pip install PyMuPDF    │
│      │                                                       │
│      ├─> SSL: SSLV3_ALERT_HANDSHAKE_FAILURE                  │
│      │       └─> 跳过该 URL / 尝试 HTTP / verify=False       │
│      │                                                       │
│      ├─> 无固定 CSS 类名 (自定义 HTML)                       │
│      │       └─> 邮箱反向定位法: 搜索 @ 节点 → DOM 回溯      │
│      │                                                       │
│      ├─> 社交链接含 "无"/%e6%97%a0 占位符                     │
│      │       └─> URL 编码占位符过滤 (免费)                     │
│      │                                                       │
│      ├─> HTTP 403 Forbidden                                  │
│      │       ├─> 检查 User-Agent → 设置浏览器 UA             │
│      │       └─> 检查 IP → 降低频率 / 使用 BrightData        │
│      │                                                       │
│      ├─> HTTP 429 Too Many Requests                          │
│      │       └─> 添加随机延迟 / 指数退避                      │
│      │                                                       │
│      ├─> 页面内容不完整                                      │
│      │       └─> 使用 Playwright 或 BrightData               │
│      │                                                       │
│      └─> 需要登录 (LinkedIn 等)                              │
│              └─> 必须使用 BrightData MCP                     │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## 最佳实践总结

### 1. 预防措施

```python
# 标准请求配置
session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 ...',
    'Accept': 'text/html,application/xhtml+xml,...',
    'Accept-Language': 'en-US,en;q=0.5',
})

# 添加重试机制
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

retry = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
adapter = HTTPAdapter(max_retries=retry)
session.mount('https://', adapter)
```

### 2. 错误处理

```python
def safe_scrape(url):
    try:
        response = session.get(url, timeout=15)
        response.raise_for_status()

        # 检查是否被 Cloudflare 拦截
        if 'cloudflare' in response.text.lower() and 'checking your browser' in response.text.lower():
            return {'status': 'cloudflare_challenge', 'url': url}

        return {'status': 'success', 'content': response.text}

    except requests.Timeout:
        return {'status': 'timeout', 'url': url}
    except requests.TooManyRedirects:
        return {'status': 'too_many_redirects', 'url': url}
    except requests.HTTPError as e:
        return {'status': 'http_error', 'code': e.response.status_code, 'url': url}
    except Exception as e:
        return {'status': 'error', 'message': str(e), 'url': url}
```

### 3. 智能选择策略

```python
def smart_scrape(url):
    """根据 URL 特征智能选择爬取方式"""

    # LinkedIn 等必须用 BrightData
    if any(domain in url for domain in ['linkedin.com', 'twitter.com', 'x.com']):
        return scrape_with_brightdata(url)

    # 学术网站用普通请求
    if any(domain in url for domain in ['.edu', 'github.io', 'scholar.google']):
        return scrape_with_requests(url)

    # 其他网站先尝试普通请求，失败后考虑 BrightData
    result = scrape_with_requests(url)
    if result.get('status') != 'success':
        return scrape_with_brightdata(url)
    return result
```

---

## 相关文档

- [Python 爬虫技术指南](./python-scraping-guide.md)
- [URL 过滤与优先级规则](./url-priority-rules.md)
- [Web Scraping Practice - TongClass](../../Note/Web-Scraping-Practice-TongClass.md)
