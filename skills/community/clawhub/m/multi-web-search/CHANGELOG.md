# Changelog

All notable changes to multi-web-search will be documented in this file.

## [3.4.0] - 2026-05-02

### Added
- **Fallback 内容抓取**：当 ddgs 失败时，自动使用 requests + BeautifulSoup 抓取搜索结果
- **Bing URL 解码**：自动解码 Bing 的 Base64 重定向链接（移除 'a1' 前缀 + 填充修复）
- **结果真实性**：Fallback 模式现在返回真实的搜索结果，而非空列表

### Fixed
- **问题 2**：Fallback 模式返回空结果 — 现在能够实际抓取并解析搜索引擎页面
- **问题 3**：`mullvad_google` 未在 constants.py 声明 — 已添加到 DDGS_ENGINES 列表
- Bing 重定向链接解析错误（Base64 解码 + 填充问题）

### Changed
- 优化 HTML 解析选择器，支持 Google/Brave/DuckDuckGo/Bing/通用引擎
- 改进 URL 去重逻辑，确保只保留真实链接
- 增强错误处理，单引擎失败不影响其他引擎

## [3.3.0] - 2026-05-01

### Added
- 图片搜索支持（size, color, type, layout, license 参数）
- 新闻搜索支持（时间过滤）
- 视频搜索支持（resolution, duration 参数）
- 书籍搜索支持

### Changed
- 统一搜索类型接口（text/images/news/videos/books）
- 优化结果格式化，不同搜索类型返回不同字段

## [3.2.0] - 2026-04-30

### Added
- DHT 网络加速支持（重复查询提速 90%）
- 代理支持（--proxy / -pr 参数）
- 可配置超时（--timeout 参数，默认 30s）
- 结果评分排序（基于相关性）

### Changed
- 改进缓存机制（TTL 1 小时）
- 优化 ddgs CLI 调用逻辑

## [3.1.0] - 2026-04-30

### Added
- 新增 Mojeek 引擎（独立索引、隐私友好）
- 新增 Google HK 引擎（香港版 Google）
- 专业知识引擎：Wikipedia, WolframAlpha

### Changed
- 从单文件重构为 7 个模块（constants, cache, scorer, url_builder, etc.）
- 改进错误处理，三级降级（ddgs → Lite → web_fetch）

## [3.0.0] - 2026-04-29

### Added
- **合并 multi-search-engine v2.1** 所有功能
- 新增 4 个引擎（总计 20 个）
- ddgs 多引擎并行搜索
- 结果缓存（TTL 1 小时）
- 结果评分排序

### Changed
- 完全重写代码架构（从 500 行单文件 → 2724 行 7 模块）
- 统一引擎定义到 constants.py
- 改进文档，详细的使用指南和参数说明

### Deprecated
- 停用 multi-search-engine v2.1（功能已合并）

## [2.1.0] - 2026-04-11 (multi-search-engine)

### Added
- 支持 16 个搜索引擎（7 国内 + 9 国际）
- 高级搜索运算符（site:, filetype:, intitle:, etc.）
- 时间过滤器（hour/day/week/month/year）
- DuckDuckGo Bangs 支持

### Features
- 隐私友好引擎（Brave, DuckDuckGo, Startpage, Ecosia, Qwant）
- 国内引擎（百度、搜狗、360、微信、神马、必应国内版、必应国际版）
- 国际引擎（Google, Google HK, DuckDuckGo, Yahoo, Brave, etc.）

---

## Migration from multi-search-engine

如果您之前使用 `multi-search-engine` v2.1，迁移到 `multi-web-search` v3.0+ 是无缝的：

- ✅ 所有引擎保留
- ✅ 参数名称一致
- ✅ 新增功能自动可用（图片/新闻/视频/DHT/代理）
- ✅ 性能提升（缓存 + 评分 + 并行）

只需将调用从 `multi-search-engine` 改为 `multi-web-search` 即可。
