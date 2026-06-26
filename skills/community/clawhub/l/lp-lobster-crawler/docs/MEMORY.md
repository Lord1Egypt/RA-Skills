# 项目记忆（Agent 经验沉淀）

> 本文件是 Agent 从交互中提炼的项目级经验库，随 git 版本控制。
> 规则定义见 `CLAUDE.md` → 编码规范 → "执行后总结与经验沉淀"。

---

## 经验沉淀日志

> 按时间倒序记录，定期整理合并到下方分类中。

### 2026-03-21 — 重写 SKILL.md 适配 clawhub 规范

- **背景**：install block 用了 `kind: download` 和 `kind: command`，clawhub 不认识；浏览器缺系统依赖
- **修复**：
  - install block 改用 `kind: uv`（clawhub 支持的四种 kind 之一：brew/node/go/uv）
  - 浏览器安装改用 `uv run playwright install --with-deps chromium`（连系统库一起装）
  - 增加故障排除章节
- **发布**：`lp-lobster-crawler@0.6.0`

### 2026-03-21 — 修复容器环境 Chromium 启动失败

- **背景**：沙盒/容器环境线程资源不足 + 缺少 dbus，Chromium 起不来
- **修复**：`BrowserConfig.extra_args` 增加 `--no-sandbox`、`--disable-dev-shm-usage`、`--single-process`、`--no-zygote` 等容器必需参数
- **发布**：`lp-lobster-crawler@0.5.1`

### 2026-03-21 — 废弃旧 API，改用 catalog 页面抓取章节列表

- **背景**：旧章节 API (`/go/pcm/chapter/get-chapters`) 返回 404，已下线
- **方案**：改为请求 `/book/{bookId}/catalog` HTML 页面，从 `div.volume-item a[href*='/book/']` 提取章节链接
- **变更文件**：
  - `src/spiders/webnovel.py` — 移除 `parse_chapter_list` / `parse_chapter_content`，新增 `parse_catalog`
  - `config/sites/webnovel.yaml` — 新增 `catalog` URL，移除已失效的 API URL
  - `src/spiders/middlewares.py` — `spider_closed` 改为 async 修复协程警告
- **验证**：20 本书 + 63,986 章节全部入库，标题正确
- **发布**：`lp-lobster-crawler@0.5.0`

### 2026-03-20 — 修复 Webnovel 选择器 + Crawl4ai 超时

- **背景**：Crawl4ai 集成后 200 成功但解析 0 条数据
- **根因**：
  1. 排行榜 URL `/ranking/novel/all_time` 已失效（返回 404 页面），新入口是 `/stories/novel`
  2. 书籍 URL 格式变了：`/book/{id}` → `/book/{slug}_{id}` 或 `/zh/book/{slug}_{id}`
  3. 列表页结构变了：`div.j_bookList a.g_thumb` → `ul.clearfix li a.g_thumb`
  4. 详情页选择器全部失效，需逐个更新
  5. Crawl4ai 的 `wait_until="networkidle"` 在 Webnovel 上永远超时（页面有持续后台请求）
- **修复**：
  - `config/sites/webnovel.yaml` — 更新 ranking URL 为 `/stories/novel`，全部选择器重写
  - `src/spiders/webnovel.py` — `_extract_book_id` 支持新 URL 格式，`parse_ranking` 增加去重
  - `src/spiders/middlewares.py` — `wait_until` 改为 `domcontentloaded` + `delay_before_return_html=5.0`
- **验证**：列表页提取 20 本书，详情页标题/作者/分类/摘要/封面全部正确解析

### 2026-03-20 — 集成 Crawl4ai 绕过 Webnovel 403

- **背景**：Webnovel 排行榜页面对 Scrapy 普通 HTTP 请求返回 403，随机 UA + 重试不足以绕过 Cloudflare
- **方案**：新增 `Crawl4aiMiddleware` 下载中间件，对 `meta["use_crawl4ai"]=True` 的请求用无头浏览器替代 Scrapy 下载器
- **发布**：`clawhub publish` → `lp-lobster-crawler@0.4.0`
- **关键设计决策**：API 端点（chapter_list_api / chapter_content_api）保持走 Scrapy 原生下载，只有 HTML 页面走浏览器

---

## 编码经验

### Scrapy + asyncio 中间件

- Scrapy 的 `process_request` 可以是 `async` 方法，但需要配置 `TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"`
- Crawl4ai 的 `AsyncWebCrawler` 是 async context manager，需要在首次请求时 `__aenter__`，spider 关闭时 `__aexit__`
- `spider_closed` signal handler 不是 async 的，清理浏览器用 `asyncio.get_event_loop().run_until_complete()`

### Crawl4ai 配置要点

- **不要用 `networkidle`**：很多现代网站有持续后台请求（analytics、websocket），永远不会达到 networkidle
- 推荐：`wait_until="domcontentloaded"` + `delay_before_return_html=5.0`（等 JS 渲染）
- `page_timeout` 建议 60000ms（60 秒），留够 Cloudflare challenge 的时间

### 中间件优先级

当前 `DOWNLOADER_MIDDLEWARES` 顺序：
- 400: `RandomUserAgentMiddleware` — 先设置 UA
- 500: `Crawl4aiMiddleware` — 浏览器渲染（拦截标记请求）
- 550: `RetryOnErrorMiddleware` — 错误重试

### 依赖管理

- 每次新增 import 必须同步 `requirements.txt`（CLAUDE.md 强制要求）
- `SKILL.md` 的 install 块需要包含运行时前置步骤（如 `crawl4ai-setup` 安装浏览器）

---

## 架构决策

| 决策 | 选择 | 理由 |
|------|------|------|
| 反爬绕过 | Crawl4ai 无头浏览器 | 比 Selenium/Playwright 更轻量，内置 undetected 模式 |
| 中间件模式 | meta 标记 `use_crawl4ai` | 最小侵入，爬虫代码几乎不改，按需启用 |
| ROBOTSTXT_OBEY | False（全局） | Webnovel robots.txt 阻止合法抓取 |
| API vs HTML | 全部走 Crawl4ai 浏览器 | 旧 API 已失效（404），章节从 catalog HTML 解析 |

---

## 常见问题与解法

### Webnovel 403

- **症状**：Scrapy 抓取排行榜/详情页返回 403
- **原因**：Cloudflare 反爬检测
- **解法**：`Crawl4aiMiddleware` + `use_crawl4ai=True` meta 标记
- **注意**：首次运行需执行 `crawl4ai-setup`（或 `playwright install chromium`）安装浏览器

### Webnovel 解析 0 条数据

- **症状**：Crawl4ai 返回 200 但解析 0 条
- **可能原因**：
  1. Webnovel 改版，URL 或页面结构变化（已发生过：ranking → stories）
  2. `wait_until="networkidle"` 超时导致空 HTML（Webnovel 有持续后台请求）
  3. 页面返回的是 404 推荐页而非真正的列表页
- **排查方法**：用 Crawl4ai 独立脚本抓取页面，保存 HTML 后用 `response.css()` 测试选择器
- **经验**：Webnovel 页面结构不稳定，选择器需要定期校验

### Webnovel URL 格式（2026-03 已确认）

- 列表页：`/stories/novel`（旧 `/ranking/novel/all_time` 已 404）
- 书籍详情：`/book/{slug}_{id}` 或 `/zh/book/{url_encoded_name}_{id}`
- Book ID 提取正则：`r"/book/[^/]*?_(\d+)"` （匹配 slug_数字 格式）
- 列表页出来的是 `/zh/book/` 路径，详情页内部是英文路径

---

## 工作流经验

### 版本发布流程

1. 修改代码 + 更新 `requirements.txt`
2. 更新 `SKILL.md` 版本号 + install 块
3. `clawhub publish . --slug lp-lobster-crawler --version x.y.z --tags latest`

### 项目当前状态（v0.4.0）

- Phase A–E 全部 19 个 TODO 已完成
- 额外集成了 Crawl4ai 反爬（非原始 TODO，属于实战补丁）
- 两个爬虫：`webnovel`（小说，已适配反爬）、`reelshorts`（短剧，stub 状态）
- CLI 入口：`src/cli.py`，6 个子命令
- 存储：SQLite MVP，数据库文件 `data/lobster.db`
