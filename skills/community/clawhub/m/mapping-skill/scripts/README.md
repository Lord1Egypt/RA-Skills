# 参考脚本说明

本目录包含可复用的 Python 爬虫脚本模板，供开发者参考和集成到自己的项目中。

---

## 文件说明

| 文件 | 功能 | 依赖 |
|------|------|------|
| `serper_search.py` | Serper API 搜索模板 | httpx, python-dotenv |
| `httpx_scraper.py` | 异步 HTTP 爬虫 | httpx |
| `cloudflare_email_decoder.py` | Cloudflare 邮箱解密 | 无 |
| `lab_member_scraper.py` | 实验室成员爬取 (三种模式: 两阶段/Hugo Academic 卡片/邮箱反向定位，含 [at] 解析和 CF 解密) | requests, beautifulsoup4 |
| **`openreview_scraper.py`** | **OpenReview 会议论文爬取** (含 Profile 缓存、Email 三级回退、ORCID 拼接) | **openreview-py, pandas** |
| **`cvf_paper_scraper.py`** | **CVF 论文爬取** (CVPR/ICCV/WACV, HTML 元数据 + PDF 内存流邮箱提取, 花括号缩写解析) | **requests, beautifulsoup4, PyMuPDF, pandas** |
| **`github_network_scraper.py`** | **GitHub 社交网络爬取** (Following/Followers 遍历 + 三层数据拼装) | **requests, pandas, openpyxl** |

---

## 使用方式

这些脚本是**参考实现**，不是可执行的包。请根据实际需求：

1. **复制相关代码**到你的项目
2. **根据目标网站**调整解析逻辑
3. **配置环境变量**和 API Keys

---

## 快速开始

### 1. 安装依赖

```bash
pip install requests beautifulsoup4 httpx python-dotenv
```

### 2. 配置环境变量

创建 `.env` 文件：

```env
SERPER_API_KEY=your_serper_api_key
```

### 3. 使用示例

```python
# 使用 Serper 搜索
from serper_search import serper_search
results = await serper_search("reinforcement learning PhD", api_key)

# 使用 Cloudflare 邮箱解密
from cloudflare_email_decoder import decode_cloudflare_email
email = decode_cloudflare_email("f493919e85c6c5...")

# 使用异步爬虫
from httpx_scraper import batch_scrape
results = await batch_scrape(urls, max_concurrent=5)

# 使用 OpenReview 会议爬虫
from openreview_scraper import OpenReviewScraper
scraper = OpenReviewScraper(username, password)
results = scraper.scrape_conference('ICML.cc/2025/Conference')
scraper.save_to_csv('icml2025.csv')

# 使用 GitHub 社交网络爬虫
from github_network_scraper import GitHubNetworkScraper
scraper = GitHubNetworkScraper(token="ghp_xxx")
users = scraper.scrape_following("AmandaXu97")
scraper.save_to_excel(users, "following.xlsx")

# 使用 CVF 论文爬虫 (CVPR/ICCV/WACV)
from cvf_paper_scraper import CVFPaperScraper
scraper = CVFPaperScraper()
scraper.scrape_conference('CVPR2025', max_papers=10)  # 调试: 10 篇
scraper.save_to_csv('cvpr2025_test.csv')
# 全量: scraper.scrape_conference('CVPR2025')

# 使用卡片模式爬取 Hugo Academic 网站 (如 PKU.AI)
from lab_member_scraper import LabMemberScraper
scraper = LabMemberScraper(base_url="https://pku.ai")
members = scraper.scrape_card_page("https://pku.ai/people/")
# 自动解密 Cloudflare 保护的邮箱

# 使用邮箱反向定位模式爬取自定义 HTML 网站 (如清华 MediaLab)
scraper = LabMemberScraper(base_url="https://media.au.tsinghua.edu.cn")
members = scraper.scrape_by_email_anchor("https://media.au.tsinghua.edu.cn/Team.htm")
# 通过邮箱文本节点反向查找人员卡片容器

# 两阶段 Hugo Academic 模式 (如 TongClass)
# 第一阶段: 从列表页提取成员 URL 列表 (含年级分组)
# 第二阶段: 逐个访问个人页，用正则提取 Interests/Education 段落
# 邮箱通过 Cloudflare XOR 解密提取
# 参见 references/python-scraping-guide.md Section 6.6
```

---

## 注意事项

1. **遵守网站 robots.txt** - 检查网站是否允许爬取
2. **合理使用数据** - 仅用于人才搜索等正当目的
3. **保护隐私** - 不要公开传播个人联系信息
4. **控制频率** - 添加适当延迟避免对服务器造成压力
5. **遵守法律** - 确保爬取行为符合当地法律法规

---

## 相关文档

- [Python 爬虫技术指南](../references/python-scraping-guide.md)
- [URL 过滤与优先级规则](../references/url-priority-rules.md)
- [反爬虫解决方案](../references/anti-scraping-solutions.md)
- [会议论文爬取指南](../references/conference-paper-scraping.md)
