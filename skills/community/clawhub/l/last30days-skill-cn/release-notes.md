# 发行说明

> Author: Jesse (https://github.com/Jesseovo)

## v2.1.0

**last30days-cn** Bug 修复与增量优化：修复百度/小红书反爬失效及 WechatItem 渲染崩溃。

### Bug 修复

- **修复 WechatItem 渲染崩溃**：`render.py` 中 `render_compact` 访问 `WechatItem.engagement` 属性导致 `AttributeError`，改用 `getattr` 兜底。
- **移除 ScrapeCreators 集成**：`xiaohongshu.py` 中 `_search_via_scrapecreators` 函数调用的 `/v2/xiaohongshu/search` 端点在 ScrapeCreators 官方从未存在（始终返回 404），属于错误实现。v2.1 完整移除该函数，保留 `token` 参数但打印弃用警告。
- **修复百度公开搜索被安全验证拦截**：更新请求头（Accept-Language/Referer/Sec-Fetch-*）、UA 轮换池，增加安全验证页检测。被拦截时主动降级到 Bing 国内版兜底搜索。
- **修复小红书爬虫 Virtual DOM 问题**：改用 `page.on("response")` XHR 拦截（`/api/sns/web/v1/search/notes`），直接解析 API JSON 数据而非 DOM，参考 MediaCrawler 的思路。

### 增强

- **爬虫统一优化**：抽取 `_launch_browser_context` 公共函数，统一 locale/viewport/UA/cookie 管理。抖音同步改用 XHR 拦截（`/aweme/v1/web/search/item/`），DOM 解析仅作兜底。
- **HTTP 健壮性**：`http.py` 新增 `backoff` 参数支持指数退避。
- **新增回归测试**：`test_render_wechat.py`、`test_baidu_antibot.py`（含 ScrapeCreators 移除验证）。

### 变更

- 更新 `scripts/lib/xiaohongshu.py` — 移除 ScrapeCreators，调整降级顺序为 MCP → 爬虫 → 公开接口
- 更新 `scripts/lib/crawler_bridge.py` — 小红书/抖音 XHR 拦截，公共 browser context
- 更新 `scripts/lib/baidu.py` — UA 池 + 反爬检测 + Bing 兜底
- 更新 `scripts/lib/render.py` — getattr 兜底 engagement
- 更新 `scripts/lib/http.py` — backoff 参数、版本号
- 更新 `SKILL.md` — 平台可用性表格、v2.1 变更说明
- 新增 `tests/test_render_wechat.py`、`tests/test_baidu_antibot.py`

---

## v2.0.0

**last30days-cn** 重大升级：集成 MediaCrawler 爬虫引擎，大幅减少 API Key 依赖。

### 亮点

- **集成 MediaCrawler 爬虫引擎**：基于 Playwright 浏览器自动化，灵感来源于 [NanmiCoder/MediaCrawler](https://github.com/NanmiCoder/MediaCrawler)，无需逆向加密算法，降低使用门槛。
- **7/8 平台零 API Key 可用**：安装 Playwright 后，微博、小红书、抖音、B站、知乎、百度、今日头条均可无需 API Key 使用（仅微信公众号仍需 API）。
- **三级自动降级策略**：API 优先 → 爬虫模式 → 公开接口，确保最大数据可用性。
- **登录态 Cookie 缓存**：爬虫模式支持持久化 Cookie，减少重复登录操作。

### Bug 修复

- **修复 Issue #1**：修复 `marketplace.json` 缺少 `owner` 字段导致 Claude Code Marketplace 安装报错的问题（"Invalid input: expected object, received undefined"）。

### 变更

- 新增 `scripts/lib/crawler_bridge.py` — MediaCrawler 爬虫桥接模块
- 更新 `weibo.py`、`xiaohongshu.py`、`douyin.py`、`bilibili.py`、`zhihu.py` — 增加爬虫模式自动降级
- 更新 `env.py` — 诊断函数考虑 Playwright 可用性
- 更新 `last30days.py` — 诊断输出增加爬虫引擎状态
- 更新 `requirements.txt` — 新增 `playwright` 可选依赖
- 更新 `README.md` — 增加免责声明、法律合规说明、v2.0 升级文档
- 更新 `SKILL.md` — 版本号升级，配置说明更新
- 更新 `.claude-plugin/marketplace.json` — 添加 `owner` 字段，修复安装问题
- 更新 `.claude-plugin/plugin.json` — 版本号升级至 2.0.0

### 说明

配置与 CLI 详见 `README.md` 与 `SPEC.md`。许可证：**MIT**。

---

## v1.0.0

**last30days-cn** 首个正式发布：面向中文互联网的近 30 天多源研究技能。

### 亮点

- **8 大中文平台**：微博、小红书、B 站、知乎、抖音、微信公众号、百度搜索、今日头条并行检索与统一简报。  
- **中文 NLP**：集成 **jieba** 分词，用于查询扩展与相关性计算，更贴合中文检索与排序。  
- **多 Agent 支持**：可作为 Cursor Skill、Claude Code 技能、OpenClaw（ClawHub / `~/.agents`）、Gemini CLI Extension 或任意具备 Bash / 读写的 Agent 工具链使用。

### 说明

配置与 CLI 详见 `README.md` 与 `SPEC.md`。许可证：**MIT**。
