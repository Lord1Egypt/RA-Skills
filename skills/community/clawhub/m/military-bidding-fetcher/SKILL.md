---
name: milb-fetcher
description: 军工采招商机自动抓取工具。从全军武器装备采购信息网、军队采购网、国防科大采购网抓取招标信息，过滤并生成 Excel 报表。当用户说"抓取商机"、"查新"、"采集招标"时触发。
metadata: {"openclaw":{"emoji":"🕷️","requires":{milb-fetcher},"install":"pip install -e {baseDir}"}}
---

# Milb Fetcher

从三大军工采购平台自动抓取招标信息。

## 快速使用

- `/milb-fetcher` → 自动检测各渠道最新可用日期并抓取（默认）
- `/milb-fetcher --help` → 显示帮助信息

日期选择（三选一，不指定则自动检测）
- `/milb-fetcher --today` → 抓取今日
- `/milb-fetcher --yesterday` → 抓取昨日
- `/milb-fetcher --date 2026-03-23` → 抓取指定日期

筛选参数
- `--keywords "关键词1,关键词2"` → 核心关键词
- `--exclude-keywords "排除词1,排除词2"` → 排除关键词
- `--high-value-keywords "高价值词1,高价值词2"` → 高价值关键词（用于推荐评级）
- `--regions "地区1,地区2"` → 地区筛选（仅对军队采购网生效）

输出控制
- `--output /path/to/file.xlsx` → 指定输出路径（默认存至 `~/.openclaw/workspace/military-bidding/军队采购商机汇总_{date}.xlsx`）
- `--no-auto-latest` → 禁用自动检测最新日期（未指定日期时改用今日）

## 数据源

- 全军武器装备采购信息网
- 军队采购网
- 国防科大采购信息网

## 推荐等级

基于 `FETCHER_HIGH_VALUE_KEYWORDS` 配置自动评定：

- **高**：标题命中高价值关键词
- **中**：标题命中核心关键词但未命中高价值词
- **低**：其他匹配项

## 过滤词

通过 `FETCHER_EXCLUDE_KEYWORDS` 配置，命中排除词的条目将被过滤掉。

## 触发词

抓取、采集、爬虫、查新、每日商机

## 配置文件

配置文件位于 `milb_fetcher/.env`（独立配置），可配置以下参数：

| 环境变量 | 用途 | 格式 |
|----------|------|------|
| `FETCHER_KEYWORDS` | 核心关键词，逗号分隔 | `词1,词2,...` |
| `FETCHER_EXCLUDE_KEYWORDS` | 排除关键词，逗号分隔 | `词1,词2,...` |
| `FETCHER_HIGH_VALUE_KEYWORDS` | 高价值关键词，逗号分隔 | `词1,词2,...` |
| `FETCHER_REGIONS` | 地区，逗号分隔 | `省份1,省份2,...` |

创建配置文件可复制 `milb_fetcher/.env.example` 为 `milb_fetcher/.env` 后修改。

