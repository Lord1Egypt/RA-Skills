---
name: novel-scraper-pro
description: >-
  智能小说抓取工具 V6，支持自动翻页、分页补全、章节号自动解析、内存监控、中断续抓。
  使用 curl+BeautifulSoup 抓取笔趣阁等小说网站，输出格式化 TXT 文件。
  默认每 10 章合并为一个文档，避免文件零散分布。
  自动检测分页并补全，智能跳过非小说内容（作者感言、抽奖预告等）。
  内存监控和中断续抓默认开启，支持 SPA 网站抓取（--force-spa）。
  Use when: 抓取网络小说章节、批量下载小说内容、保存小说为 TXT 格式。
---

# Novel Scraper Pro

## 概述

Novel Scraper Pro 是智能小说抓取工具，支持自动翻页、分页补全、章节号解析、内存监控、中断续抓等功能。
使用 curl+BeautifulSoup 抓取笔趣阁等小说网站，输出格式化 TXT 文件。

## 快速开始

```bash
# 安装
clawhub install novel-scraper-pro

# 单章抓取
python3 scripts/scraper.py --url "https://www.bqquge.com/4/1962"

# 批量抓取（1-100 章）
python3 scripts/scraper.py --chapters "1-100" --book "书名"

# 中断续抓（默认开启）
python3 scripts/scraper.py --chapters "1-100" --book "书名"
# 中途 Ctrl+C 后，再次运行相同命令会自动从断点继续
```

## 功能特性

### 核心功能（V5 保留，100%）

| 功能 | 说明 |
|------|------|
| ✅ 章节号自动解析 | 从标题提取章节号，自动修正 URL 推算错误 |
| ✅ 分页自动检测 | 检测"下一页"链接，自动补全分页（最多 5 页） |
| ✅ 内容质量验证 | 段落数检查、结束标记检测 |
| ✅ 非小说内容跳过 | 智能判断并跳过作者感言、抽奖预告等 |
| ✅ 目录页 fallback | 连续失败 2 次自动切换目录页模式 |
| ✅ 连续性检查 | 缺章检测与警告 |
| ✅ 缓存系统 | 章节级缓存，重复抓取秒级返回 |
| ✅ 合并保存 | 每 10 章合并为一个文件 |

### V6 新增功能

| 功能 | 默认状态 | 说明 |
|------|----------|------|
| 🧠 内存监控 | ✅ 开启 | 超过 2500MB 自动 GC 并等待 |
| 💾 中断续抓 | ✅ 开启 | 进度自动保存，可随时中断续抓 |
| 🌐 SPA 支持 | ❌ 关闭 | `--force-spa` 启用浏览器抓取 |

## CLI 参数

### 基础参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `--url` | 单章 URL | `--url "https://..."` |
| `--urls` | 多章 URL（逗号分隔） | `--urls "url1,url2,..."` |
| `--chapters` | 章节号范围 | `--chapters "1-100"` |
| `--book` / `-b` | 书名 | `--book "书名"` |
| `--merge-interval` | 每 N 章合并（默认 10） | `--merge-interval 10` |

### 质量选项

| 参数 | 说明 |
|------|------|
| `--strict` | 严格质量验证（字符数<1000 警告） |
| `-v` / `--verbose` | 详细日志输出 |

### V6 新增参数

| 参数 | 说明 | 默认 |
|------|------|------|
| `--no-memory-monitor` | 关闭内存监控 | 开启 |
| `--no-resume` | 关闭中断续抓 | 开启 |
| `--force-spa` | 强制使用浏览器抓取 SPA 网站 | 关闭 |

## 使用场景

### 场景 1：批量抓取小说

```bash
# 抓取第 1-100 章
python3 scripts/scraper.py --chapters "1-100" --book "没钱修什么仙"

# 输出：
# novels/没钱修什么仙_第 1-10 章.txt
# novels/没钱修什么仙_第 11-20 章.txt
# ...
```

### 场景 2：中断续抓

```bash
# 开始抓取 500 章
python3 scripts/scraper.py --chapters "1-500" --book "书名"

# 中途 Ctrl+C 中断

# 再次运行，自动从断点继续
python3 scripts/scraper.py --chapters "1-500" --book "书名"
# 输出：✅ 跳过已完成 237 章
```

### 场景 3：分页章节补全

```bash
# 自动检测并补全分页章节
python3 scripts/scraper.py --chapters "1-100" --book "书名"

# 输出：
# 📄 检测到 3 个分页章节，自动补全...
# ✅ 补全完成，共 156 段
```

### 场景 4：SPA 网站抓取

```bash
# 强制使用浏览器抓取 SPA 网站
python3 scripts/scraper.py --url "https://spa-novel.com/chapter/1" --force-spa
```

## 辅助工具

### fetch_catalog.py - 目录页抓取

```bash
# 抓取目录页，生成章节 URL 映射
python3 scripts/fetch_catalog.py
```

### extract_urls.py - URL 提取

```bash
# 从目录文件提取指定章节范围的 URL
python3 scripts/extract_urls.py 1 100
```

### merge_novels.py - 文件合并与完整性检查

```bash
# 合并已抓取的分散文件并检查缺失
python3 scripts/merge_novels.py --book "书名" --range 1 100
```

## 输出位置

抓取的小说保存在：`~/.openclaw/workspace/novels/`

文件名格式：`书名_第 X-Y 章.txt`

## 依赖

- Python 3.8+
- beautifulsoup4

```bash
pip install beautifulsoup4
```

## 版本

- **当前版本**: v2.0.0
- **基础**: scraper_v5.py（智能版）
- **新增**: 内存监控、中断续抓、SPA 支持

## 常见问题

### Q: 如何关闭内存监控？

```bash
python3 scripts/scraper.py --chapters "1-100" --book "书名" --no-memory-monitor
```

### Q: 如何关闭中断续抓？

```bash
python3 scripts/scraper.py --chapters "1-100" --book "书名" --no-resume
```

### Q: 如何清空进度重新抓取？

```bash
rm ~/.openclaw/workspace/skills/novel-scraper-pro/state/progress.json
python3 scripts/scraper.py --chapters "1-100" --book "书名"
```

### Q: 缓存在哪里？如何清理？

```bash
# 缓存位置
/tmp/novel_scraper_cache/

# 清理缓存
rm -rf /tmp/novel_scraper_cache/*
```
