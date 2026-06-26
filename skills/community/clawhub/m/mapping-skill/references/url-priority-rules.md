# URL 过滤与优先级规则

> 本文档定义了在 AI 人才搜索中 URL 的过滤和优先级排序规则，帮助快速定位高质量候选人信息。

---

## 概述

在进行人才搜索时，搜索结果往往包含大量 URL。合理的 URL 过滤和优先级排序可以：

1. **提高效率** - 优先爬取最可能包含目标信息的页面
2. **节省资源** - 跳过不相关的页面，减少 API 调用
3. **提升质量** - 过滤掉低质量或过时的信息源

---

## 优先级分类

### 一级优先 (P1) - 个人主页

最可靠的候选人信息来源，通常包含完整的个人简介、联系方式和研究信息。

| 域名模式 | 示例 | 可靠性 |
|---------|------|--------|
| `*.github.io` | `johnsmith.github.io` | ⭐⭐⭐⭐⭐ |
| `sites.google.com/*` | `sites.google.com/view/johnsmith` | ⭐⭐⭐⭐⭐ |
| `~username` 模式 | `cs.stanford.edu/~johnsmith` | ⭐⭐⭐⭐⭐ |
| 个人子域名 | `johnsmith.com`, `johnsmith.me` | ⭐⭐⭐⭐ |

**识别特征**：
- URL 包含波浪号 `~`
- 使用 GitHub Pages 或 Google Sites
- 域名是人名拼音

### 二级优先 (P2) - 学术机构

大学和实验室的官方人员页面，信息准确但可能不够详细。

| 域名模式 | 机构 | 国家 |
|---------|------|------|
| `*.stanford.edu` | Stanford University | 美国 |
| `*.berkeley.edu` | UC Berkeley | 美国 |
| `*.cmu.edu` | Carnegie Mellon University | 美国 |
| `*.mit.edu` | MIT | 美国 |
| `*.princeton.edu` | Princeton University | 美国 |
| `*.washington.edu` | University of Washington | 美国 |
| `*.tsinghua.edu.cn` | Tsinghua University | 中国 |
| `*.pku.edu.cn` | Peking University | 中国 |
| `*.sjtu.edu.cn` | Shanghai Jiao Tong University | 中国 |
| `*.ustc.edu.cn` | USTC | 中国 |

**URL 路径关键词**：
- `/people/`, `/members/`, `/students/`
- `/~username/`
- `/faculty/`, `/phd/`

### 三级优先 (P3) - 专业网络

专业社交网络的个人资料页，需要特殊处理。

| 域名 | 处理方式 | 信息完整度 |
|------|---------|-----------|
| `linkedin.com/in/*` | 需要 BrightData MCP | ⭐⭐⭐⭐ |
| `scholar.google.com/citations*` | 公开可访问 | ⭐⭐⭐⭐ |
| `dblp.org/pid/*` | 公开可访问 | ⭐⭐⭐ |
| `semanticscholar.org/author/*` | 公开可访问 | ⭐⭐⭐ |

### 四级优先 (P4) - 代码仓库

GitHub 等代码仓库可以提供技术能力和联系方式线索。

| 域名 | 信息类型 | 可靠性 |
|------|---------|--------|
| `github.com/username` | 技术能力、邮箱 (commit) | ⭐⭐⭐ |
| `gitlab.com/username` | 同上 | ⭐⭐⭐ |

---

## 排除规则

### 完全排除

以下类型的 URL 应完全排除：

| 排除类型 | 域名/模式 | 原因 |
|---------|---------|------|
| 视频平台 | `youtube.com`, `vimeo.com` | 不包含文本信息 |
| 新闻媒体 | `news.*`, `medium.com`, `reddit.com` | 非原始信息源 |
| 社交平台 | `facebook.com`, `instagram.com` | 信息质量低 |
| 电商平台 | `amazon.com`, `ebay.com` | 不相关 |
| 百科类 | `wikipedia.org` | 非个人资料 |
| 求职平台 | `indeed.com`, `glassdoor.com` | 职位信息，非个人资料 |

### 条件排除

| 排除类型 | 模式 | 条件 |
|---------|------|------|
| 课程页面 | `/course/`, `/class/`, `/syllabus/` | 非人员页面 |
| 职位公告 | `/jobs/`, `/positions/`, `/hiring/` | 非个人信息 |
| 新闻稿 | `/news/`, `/press/`, `/announcement/` | 非原始资料 |
| 活动页面 | `/events/`, `/workshop/`, `/conference/` | 非人员页面 |

---

## 过滤算法

### Python 实现

```python
import re
from typing import List, Tuple
from dataclasses import dataclass

@dataclass
class URLScore:
    url: str
    score: float
    category: str


# 优先级域名配置
PRIORITY_DOMAINS = {
    # P1: 个人主页
    'personal': {
        'domains': ['github.io', 'sites.google.com', '.me', '.dev'],
        'patterns': [r'/~\w+', r'/people/\w+', r'/members/\w+'],
        'score': 0.95
    },
    # P2: 顶级高校
    'top_university': {
        'domains': [
            'stanford.edu', 'berkeley.edu', 'cmu.edu', 'mit.edu',
            'princeton.edu', 'washington.edu', 'caltech.edu',
            'tsinghua.edu.cn', 'pku.edu.cn', 'sjtu.edu.cn'
        ],
        'score': 0.85
    },
    # P3: 专业网络
    'professional': {
        'domains': ['scholar.google.com', 'dblp.org', 'semanticscholar.org'],
        'score': 0.75
    },
    # P3: LinkedIn (需要 BrightData)
    'linkedin': {
        'domains': ['linkedin.com/in'],
        'score': 0.70
    },
    # P4: 代码仓库
    'code': {
        'domains': ['github.com', 'gitlab.com'],
        'score': 0.60
    }
}

# 排除域名配置
EXCLUDE_DOMAINS = [
    'youtube.com', 'vimeo.com',
    'medium.com', 'reddit.com',
    'facebook.com', 'instagram.com', 'twitter.com', 'x.com',
    'amazon.com', 'ebay.com',
    'wikipedia.org',
    'indeed.com', 'glassdoor.com'
]

# 排除路径模式
EXCLUDE_PATTERNS = [
    r'/course/', r'/class/', r'/syllabus/',
    r'/jobs/', r'/positions/', r'/hiring/',
    r'/news/', r'/press/', r'/announcement/',
    r'/events/', r'/workshop/', r'/conference/'
]


def score_url(url: str) -> URLScore:
    """
    对单个 URL 进行评分

    Args:
        url: 待评分的 URL

    Returns:
        URLScore 对象，包含分数和分类
    """
    url_lower = url.lower()

    # 检查排除域名
    for domain in EXCLUDE_DOMAINS:
        if domain in url_lower:
            return URLScore(url=url, score=-1.0, category='excluded_domain')

    # 检查排除路径
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, url_lower):
            return URLScore(url=url, score=-1.0, category='excluded_path')

    # 检查优先级域名
    for category, config in PRIORITY_DOMAINS.items():
        # 检查域名
        for domain in config.get('domains', []):
            if domain in url_lower:
                return URLScore(url=url, score=config['score'], category=category)

        # 检查路径模式
        for pattern in config.get('patterns', []):
            if re.search(pattern, url_lower):
                return URLScore(url=url, score=config['score'], category=category)

    # 默认分数
    return URLScore(url=url, score=0.5, category='general')


def filter_and_sort_urls(urls: List[str], min_score: float = 0.0) -> List[Tuple[str, float]]:
    """
    过滤和排序 URL 列表

    Args:
        urls: URL 列表
        min_score: 最低分数阈值

    Returns:
        排序后的 (URL, 分数) 列表
    """
    scored = []

    for url in urls:
        result = score_url(url)
        if result.score >= min_score:
            scored.append((url, result.score, result.category))

    # 按分数降序排序
    scored.sort(key=lambda x: x[1], reverse=True)

    return [(url, score) for url, score, _ in scored]


def get_top_urls(urls: List[str], n: int = 50) -> List[str]:
    """
    获取前 N 个高质量 URL

    Args:
        urls: URL 列表
        n: 返回数量

    Returns:
        排序后的前 N 个 URL
    """
    filtered = filter_and_sort_urls(urls, min_score=0.0)
    return [url for url, _ in filtered[:n]]


# 使用示例
if __name__ == "__main__":
    test_urls = [
        "https://johndoe.github.io/",
        "https://cs.stanford.edu/~johndoe/",
        "https://linkedin.com/in/johndoe",
        "https://scholar.google.com/citations?user=abc123",
        "https://youtube.com/watch?v=xyz",  # 应被排除
        "https://medium.com/@johndoe/some-article",  # 应被排除
    ]

    results = filter_and_sort_urls(test_urls)

    for url, score in results:
        print(f"[{score:.2f}] {url}")
```

### 输出示例

```
[0.95] https://johndoe.github.io/
[0.95] https://cs.stanford.edu/~johndoe/
[0.75] https://scholar.google.com/citations?user=abc123
[0.70] https://linkedin.com/in/johndoe
```

---

## 批量处理建议

### 1. 分阶段处理

```python
# 阶段 1: 快速过滤 (去除明显不相关的)
filtered_urls = [url for url in all_urls if score_url(url).score >= 0]

# 阶段 2: 优先处理高分数 URL
high_priority = [url for url in filtered_urls if score_url(url).score >= 0.8]

# 阶段 3: 依次降低阈值处理
medium_priority = [url for url in filtered_urls if 0.6 <= score_url(url).score < 0.8]
low_priority = [url for url in filtered_urls if score_url(url).score < 0.6]
```

### 2. 并发限制

```python
# 不同优先级使用不同的并发数
CONCURRENCY_LIMITS = {
    'personal': 10,      # 个人主页通常对爬虫友好
    'top_university': 5, # 大学网站可能有更严格的限制
    'linkedin': 1,       # LinkedIn 需要使用 BrightData，串行处理
}
```

### 3. 错误处理

```python
# 记录失败的 URL 和原因
failed_urls = []

for url in prioritized_urls:
    try:
        result = scrape(url)
    except Exception as e:
        failed_urls.append({
            'url': url,
            'error': str(e),
            'category': score_url(url).category
        })
```

---

## 特殊情况处理

### 学术会议作者页面

```python
# 从会议网站提取作者链接
CONFERENCE_PATTERNS = {
    'neurips': r'neurips\.cc/virtual/\d+/poster/(\d+)',
    'icml': r'icml\.cc/virtual/\d+/poster/(\d+)',
    'cvpr': r'cvpr\.thecvf\.com/content/.*'
}
```

### 实验室成员页面

```python
# 实验室成员页面通常包含多个候选人
LAB_MEMBER_PATTERNS = [
    r'/people/',
    r'/members/',
    r'/team/',
    r'/students/',
    r'/phd/'
]
```

---

## 相关文档

- [Python 爬虫技术指南](./python-scraping-guide.md)
- [反爬虫解决方案](./anti-scraping-solutions.md)
- [顶级 AI 实验室](./top-ai-labs.md)
