---
name: govb-fetcher
description: 地方政府采购商机自动抓取工具（非军队采购）。从北京中建云智、湖南政府采购网等地方政府采购平台抓取招标公告，按关键词过滤，补全采购人、代理机构、预算、时间节点等详情，生成 Excel 报表。与 milb-fetcher（军队采购）互补，本工具专注地方政府渠道。
metadata: {"openclaw":{"emoji":"🏛️","requires":{govb-fetcher},"install":"uv pip install -e {baseDir}"}}
---

# govb-fetcher

从多个地方政府采购平台自动抓取招标公告，关键词过滤后生成 Excel 报表。

## 快速使用

- `/govb-fetcher` → 抓取今日数据（默认）
- `/govb-fetcher --help` → 显示帮助信息

日期选择（三选一，不指定则默认今日）
- `/govb-fetcher --today` → 抓取今日
- `/govb-fetcher --yesterday` → 抓取昨日
- `/govb-fetcher --date 2026-03-30` → 抓取指定日期

输出控制
- `--no-detail` → 仅输出列表字段（更快，跳过详情接口，Excel 只保留有值的列）
- `--output /path/to/file.xlsx` → 指定输出路径

筛选参数
- `--keywords "关键词1,关键词2"` → 覆盖核心关键词
- `--exclude-keywords "词1,词2"` → 覆盖排除关键词
- `--high-value-keywords "词1,词2"` → 覆盖高价值关键词（影响推荐等级）

凭证更新
- `/govb-fetcher --set-cookie --source bjzc --bearer "Bearer xxx" --session "YGCG_TBSESSION=xxx; JSESSIONID=xxx; jcloud_alb_route=xxx"`

## 数据源

| 标识 | 平台 | 认证 |
|------|------|------|
| `bjzc` | 北京中建云智政府采购网 | 需 Cookie + Bearer |
| `hnzc` | 湖南政府采购网 | 免认证 |

## 推荐等级

- **高**：命中高价值关键词（模型/仿真/数据/AI/软件等）或含「意向」
- **中**：命中「系统」关键词
- **空**：其他匹配项

## 触发词

政府采购商机、地方政府采购、地方招标、北京政府采购、湖南政府采购、政府商机

## 配置文件

配置文件搜索顺序（高优先级在前）：
1. 当前目录 `.env`
2. `~/.config/govb-fetcher/.env`

| 环境变量 | 用途 |
|---------|------|
| `FETCHER_BJZC_BEARER_TOKEN` | 北京政采 Bearer token |
| `FETCHER_BJZC_TBSESSION` | 北京政采 YGCG_TBSESSION（自动刷新） |
| `FETCHER_BJZC_JSESSIONID` | 北京政采 JSESSIONID |
| `FETCHER_BJZC_ALB_ROUTE` | 北京政采负载均衡路由 |
| `FETCHER_KEYWORDS` | 核心关键词，逗号分隔 |
| `FETCHER_EXCLUDE_KEYWORDS` | 排除关键词，逗号分隔 |
| `FETCHER_HIGH_VALUE_KEYWORDS` | 高价值关键词，逗号分隔 |
| `FETCHER_OUTPUT_DIR` | Excel 输出目录（默认 `~/.openclaw/workspace/govb-bidding`）|
| `FETCHER_USE_PROXY` | 是否启用代理，`true` / `false`（默认 `false`）|
| `FETCHER_PROXY` | 代理地址，格式 `http://user:pass@host:port` |
