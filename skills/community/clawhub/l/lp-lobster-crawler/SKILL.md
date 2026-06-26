---
name: lp-lobster-crawler
description: 定向抓取 Webnovel/ReelShorts 等站点的书籍/短剧内容，支持内容分级与钉钉播报。
version: 0.7.0
metadata:
  openclaw:
    emoji: "🦞"
    os: ["darwin", "linux"]
    requires:
      anyBins:
        - uv
      env:
        - DINGTALK_WEBHOOK
    primaryEnv: DINGTALK_WEBHOOK
    install:
      - kind: uv
        package: "curl_cffi"
        bins: ["uv"]
---

## 龙虾爬虫技能

定向抓取 Webnovel 小说和 ReelShorts 短剧的结构化内容，支持增量更新、内容分级（高/中/低）和钉钉机器人播报。

## 环境初始化

首次使用前，在技能目录下初始化 Python 环境：

```bash
cd {{skillPath}}
uv venv .venv
uv pip install -r requirements.txt
```

不需要安装浏览器。反爬通过 curl_cffi TLS 指纹伪装实现，纯 Python 库，无系统依赖。

后续所有命令都通过 `uv run` 执行，它会自动激活 .venv 虚拟环境。

## 触发条件

当用户消息包含以下意图时激活此技能：

- 抓取/爬取小说、短剧、webnovel、reelshorts 内容
- 查看爬虫状态、已抓取作品列表
- 播报抓取结果到钉钉
- 生成 RSS 订阅源
- 管理定时抓取任务

## 命令

所有命令必须在技能目录下执行。先 `cd {{skillPath}}`，再运行命令。

### 抓取内容

```bash
uv run python -m src.cli crawl <spider_name>
```

- `spider_name` 可选值：`webnovel`（小说）、`reelshorts`（短剧）
- 支持传递爬虫参数：`uv run python -m src.cli crawl webnovel -a max_pages=5`

### 列出已抓取作品

```bash
uv run python -m src.cli list [--site <site>] [--grade <grade>] [--limit <n>]
```

- `--site`：按站点过滤（webnovel / reelshorts）
- `--grade`：按分级过滤（high / medium / low）
- `--limit`：显示数量，默认 20

### 查看系统状态

```bash
uv run python -m src.cli status
```

返回数据库统计（作品数、章节数、剧集数）和各分级数量。

### 播报到钉钉

```bash
uv run python -m src.cli broadcast [--site <site>] [--grade <grade>] [--title <title>]
```

生成 Markdown 消息并发送到钉钉群。需要设置环境变量 `DINGTALK_WEBHOOK`。

### 管理定时任务

```bash
uv run python -m src.cli schedule --action=list    # 查看任务
uv run python -m src.cli schedule --action=load    # 从配置加载
uv run python -m src.cli schedule --action=start   # 启动调度器
```

### 生成 RSS 订阅源

```bash
uv run python -m src.cli rss [--format rss|atom] [--output <path>] [--site <site>] [--grade <grade>]
```

默认输出到 `data/rss.xml`。

## 规则

1. 首次使用前，必须先运行"环境初始化"步骤安装依赖。如果 `uv run` 报错找不到模块，重新执行初始化。
2. 运行爬虫前，先执行 `status` 确认系统正常。
3. 用户未指定站点时，询问要抓取 webnovel 还是 reelshorts。
4. 播报前先用 `list` 确认有数据可播报。
5. 钉钉播报需要确认 `DINGTALK_WEBHOOK` 环境变量已配置。
6. 抓取可能耗时较长，提前告知用户并在完成后汇报结果。
7. 不要同时运行多个爬虫实例，避免并发冲突。

