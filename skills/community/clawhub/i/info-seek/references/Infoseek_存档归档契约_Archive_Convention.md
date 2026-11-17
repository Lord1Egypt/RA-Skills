# Infoseek 存档归档契约

> 版本：v1.0.1 ｜ 状态：✅ 已提供 ｜ 对齐全：`scripts/infoseek_helper.py` / `core/state_dir.py`

## 1. 目录结构

```
<archives_dir>/                     # 默认 ~/infoseek-archives/（env: INFOSEEK_ARCHIVE）
└── <subject>/                      # 按主题分目录（subject 原文，空格保留）
    ├── YYYYMMDD-title-website.md   # 内容文件（markdown 默认）
    ├── YYYYMMDD-title-website.json # 元数据（可选）
    └── README.md                   # 主题索引（可选）
```

运行时数据（claims / aliases / pending / anchor_db）落 `~/.infoseek/`（env: `INFOSEEK_DATA_DIR` / `INFOSEEK_DB`），**不写技能目录**。

## 2. 文件名规范

```
格式: YYYYMMDD-title-website.ext
规则:
  - date: 抓取日期（YYYYMMDD）
  - title: 清洗后标题（去 <>:"/\|?*，截断 80 字符）
  - website: 域名小写、去 www.、取首段
  - ext: md（默认）/ json / txt
  - 重名: 追加 SHA1 前 8 位 → "YYYYMMDD-title-website_8hash.ext"
```

## 3. 元数据表头（内容文件内嵌）

```yaml
url: 原始 URL
url_normalized: 标准化后 URL
website: 站点名
source: web_search | ...
date: YYYYMMDD
title: 标题
author: unknown
editor: unknown
```

## 4. 归档触发方式

| 方式 | 说明 |
|------|------|
| CLI | `python scripts/infoseek_helper.py save --subject X --url ...` |
| 调研指令 | `research("主题 [归档]")` → 自动落盘 |
| MCP | `save_archive_async(subject, url, title, content, metadata)` |

## 5. 去重

- `normalize_url()` 标准化后 SHA1 哈希为去重键
- `check_dedup_async` / `dedup_stats_async` 提供查询

## 6. 兼容性

- 归档文件名规则变更需同步 `generate_filename()` 与 README 文档
- 已归档文件不支持静默重命名（防外部引用失效）
