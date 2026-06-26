# Changelog

All notable changes to novel-scraper-pro will be documented in this file.

## [2.0.3] - 2026-04-04

### 🐛 Bug Fixes

- **修复缓存命中导致分页不完整**：缓存内容<50 段时重新抓取
- **修复分页补全中断后无法恢复**：缓存命中时检查内容完整性

### ✨ Improvements

- 分页补全阈值：50 段（低于此值认为是不完整的分页）
- 缓存命中率与完整性平衡

## [2.0.2] - 2026-04-04

### ✨ 新功能

- **内存监控**（默认开启）：超过 2500MB 自动 GC 并等待
- **中断续抓**（默认开启）：进度自动保存，可随时中断续抓
- **SPA 支持**（可选）：`--force-spa` 启用浏览器抓取 SPA 网站

### 🔧 改进

- 更新 STATE_DIR 指向新 skill 目录
- 添加 SPA 域名缓存机制
- 优化 fetch_html 支持 SPA 检测与浏览器兜底

### 📚 V5 功能（100% 保留）

- 章节号自动解析
- 分页自动检测与补全
- 内容质量验证
- 非小说内容跳过
- 目录页 fallback
- 连续性检查
- 缓存系统
- 合并保存

### 📦 辅助工具（全部保留）

- fetch_catalog.py - 目录页抓取
- extract_urls.py - URL 提取
- merge_novels.py - 文件合并与完整性检查

### 📝 文档

- 完整 SKILL.md 使用文档
- 更新 CHANGELOG.md

---

## [1.6.0] - 2026-04-04 (novel-scraper)

### 🔧 Technical

- 代码质量修复：删除未使用导入和变量
- 修复 f-string 无占位符问题
- 通过 ruff check 所有检查

---

## [1.5.0] - 2026-04-03

### 🐛 Bug Fixes

- 修复索引切片 bug
- 新增 `--chapters` 参数

### ✨ Features

- 新增 extract_urls.py 辅助脚本

---

## [1.4.0] - 2026-04-02

### ✨ Features

- 内存监控融合方案（趋势预测 + 分级释放）
- 分页检测与自动补全
- 连续性验证

---

## [1.0.0] - 2026-03-29

### ✨ Features

- 初始版本：笔趣阁抓取、自动翻页、内存监控
