# 🔥 Juejin Skills - 掘金技术社区操作技能

> 一套基于自然语言驱动的掘金（juejin.cn）操作技能，支持热门文章排行榜查询、文章自动发布和文章下载保存为 Markdown。

## 📋 使用方法

### 安装依赖

```bash
pip install -r requirements.txt
# Install Playwright browsers (for login)
playwright install chromium
```

### 自然语言使用示例

直接对 AI 说出以下指令即可：

| 功能 | 示例指令 |
|------|----------|
| 查看分类 | "掘金有哪些文章分类？" |
| 热门排行 | "获取掘金前端热门文章排行榜" |
| 全站热榜 | "看看掘金最近最火的文章" |
| 登录掘金 | "登录掘金账号" |
| 发布文章 | "把 ./article.md 发布到掘金，分类前端，标签 Vue.js" |
| 下载文章 | "下载这篇掘金文章 https://juejin.cn/post/xxx" |
| 批量下载 | "下载掘金用户 xxx 的所有文章" |

### 代码调用示例

```python
from juejin_skill.api import JuejinAPI
from juejin_skill.hot_articles import HotArticles
from juejin_skill.publisher import ArticlePublisher
from juejin_skill.downloader import ArticleDownloader
from juejin_skill.auth import JuejinAuth

# 1. Get hot articles
hot = HotArticles()
categories = hot.get_categories()
articles = hot.get_hot_articles(category_id="6809637767543259144", sort_type=200)

# 2. Login and publish
auth = JuejinAuth()
cookie = auth.login_with_browser()

publisher = ArticlePublisher(cookie=cookie)
publisher.publish_markdown(
    filepath="./my-article.md",
    category_id="6809637767543259144",
    tag_ids=["6809640407484334093"],
    brief_content="Article summary",
    cover_image=""
)

# 3. Download articles
downloader = ArticleDownloader()
downloader.download_article("https://juejin.cn/post/7300000000000000000", output_dir="./output")
downloader.download_user_articles(user_id="123456", output_dir="./output")
```

## 🏗️ 项目结构

```
juejin/
├── SKILL.md              # 技能定义文档（详细描述激活条件和功能清单）
├── README.md             # 项目说明文档（当前文件）
├── requirements.txt      # Python 依赖
├── juejin_skill/         # 主模块
│   ├── __init__.py       # 模块入口
│   ├── config.py         # 配置管理（API 地址、默认参数）
│   ├── api.py            # 掘金 API 基础封装
│   ├── auth.py           # Playwright 浏览器登录鉴权
│   ├── hot_articles.py   # 热门文章排行榜
│   ├── publisher.py      # 文章自动发布
│   ├── downloader.py     # 文章下载（转 Markdown）
│   └── utils.py          # 工具函数
└── output/               # 下载文章输出目录（自动创建）
```

## ✨ 功能特性

### 📊 热门文章排行榜
- 获取掘金全部文章分类列表
- 查看指定分类或全站的热门文章排行
- 支持多种排序方式（最热、最新、三天/七天/月/历史热榜）
- 返回文章标题、作者、阅读量、点赞数等关键信息

### 📝 文章自动发布
- 通过 Playwright 浏览器让用户安全登录掘金，自动获取 Cookie
- Cookie 持久化存储，无需重复登录
- 读取本地 Markdown 文件自动发布
- 支持设置文章分类、标签、摘要和封面图
- 支持保存为草稿或直接发布

### 📥 文章下载
- 通过文章 URL 下载单篇文章
- 批量下载指定作者的所有文章
- 自动将掘金文章内容转换为标准 Markdown 格式
- 保留文章标题、作者、发布时间、标签等元信息
- 可选下载文章内嵌图片到本地

## 🔧 技术细节

| 项目 | 说明 |
|------|------|
| 语言 | Python 3.9+ |
| HTTP 客户端 | httpx（异步支持） |
| 浏览器自动化 | Playwright |
| HTML 转 Markdown | markdownify |
| 鉴权方式 | Cookie（Playwright 浏览器登录获取） |
| 目标网站 | https://juejin.cn/ |

## ⚠️ 注意事项

1. 文章发布功能需要先登录掘金账号，首次使用会通过浏览器引导登录
2. Cookie 保存在本地 `~/.juejin_cookie.json`，请注意安全
3. 请遵守掘金社区规范，不要发布违规内容
4. API 调用请注意频率限制，避免过于频繁的请求
5. 下载的文章仅供个人学习使用，请尊重原作者版权

## 📄 License

MIT License
