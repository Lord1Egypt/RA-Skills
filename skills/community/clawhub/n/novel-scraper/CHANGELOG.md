# Changelog

All notable changes to novel-scraper will be documented in this file.

## [1.6.0] - 2026-04-04

### 🔧 Technical
- **代码质量修复**：通过 ruff check 所有检查
- 删除未使用导入（os, sys, psutil, urljoin, argparse, re, Path, datetime 重复导入）
- 修复 f-string 无占位符问题（9 处）
- 删除未使用变量（prev_count, same_count, final_content, context）

### ✅ Code Quality
- `ruff check scripts/` 所有检查通过

---

## [1.5.0] - 2026-04-03

### 🐛 Bug Fixes
- **修复索引切片 bug**：之前使用 `data[300:400]` 按索引切片，错误对应章节号 300-419（应为 301-400）
- 新增 `--chapters` 参数，支持按章节号精确筛选（格式：`--chapters 301-400`）
- 自动检测并提示缺失章节（网站目录中没有的章节）

### ✨ Features
- 新增 `scripts/extract_urls.py` 辅助脚本，用于按章节号提取 URL
- 抓取前显示统计信息：实际章节范围、章节数量、缺失章节列表

### 📝 Documentation
- 更新 SKILL.md，添加 v1.5.0 使用说明和 `--chapters` 参数文档
- 添加版本对比说明，推荐优先使用 `--chapters` 参数

### 🔧 Technical
- 添加 `json` 模块导入支持
- 新增 `load_catalog()` 函数加载目录数据
- 新增 `extract_urls_by_chapter_range()` 函数按章节号筛选

---

## [1.4.0] - 2026-04-02

### ✨ Features
- 内存监控融合方案（趋势预测 + 分级释放）
- 修复趋势预测除数错误（`history_window - 1`）
- 日志级别优化（debug → info）

### 🐛 Bug Fixes
- 分页检测与自动补全（最多 5 页）
- 连续性验证（缺章检测与报告）

---

## [1.3.0] - 2026-04-02

### ✨ Features
- V4 完整版：章节号自动解析、内容质量评分、分页补全

---

## [1.2.0] - 2026-04-02

### ✨ Features
- 合并功能：默认每 10 章合并为一个文档

---

## [1.1.0] - 2026-03-29

### ✨ Features
- SPA 网站自动检测
- 批量抓取功能（`--urls` 参数）

---

## [1.0.0] - 2026-03-29

### ✨ Features
- 初始版本：笔趣阁抓取、自动翻页、内存监控
