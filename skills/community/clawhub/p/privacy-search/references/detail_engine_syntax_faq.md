# 引擎细节、语法表与完整 FAQ

本文档收录 SKILL.md 瘦身后移出的详细内容。

---

## 一、引擎详情

引擎清单唯一来源：`scripts/engines_registry.py`，运行 `--list-engines` 查看实时属性。

| 引擎 | 标识 | 类型 | 区域 | 隐私等级 | strict 可用 | 说明 |
|------|------|------|------|---------|------------|------|
| 本地 SearXNG | `searxng` | JSON API | 本机 | 高 | ✅ | 元搜索，query 不出本机，支持 bangs |
| Yandex | `yandex` | HTML 解析 | 俄罗斯 | 中 | ✅ | 国内直连速度较好 |
| Startpage | `startpage` | HTML 解析 | 荷兰 | 高 | ✅ | Google 结果代理 |
| Qwant | `qwant` | HTML 解析 | 法国 | 高 | ✅ | 受欧盟隐私法约束 |
| Brave Search | `brave` | HTML 解析 | 美国 | 高 | ✅ | 独立索引 |
| DuckDuckGo | `duckduckgo` | HTML 解析 | 美国 | 高 | ✅ | 国内直连不稳定，作兜底 |
| 百度 | `baidu` | HTML 解析 | 中国 | 低 | ❌ | 反爬较强，返回跳转链接 |
| 必应 | `bing` | HTML 解析 | 中国 | 低 | ❌ | 国内可直接访问 |
| 搜狗 | `sogou` | HTML 解析 | 中国 | 低 | ❌ | 返回跳转链接 |
| 360 搜索 | `360` | HTML 解析 | 中国 | 低 | ❌ | 返回跳转链接 |

### 架构分层

```
CLI / SearchOrchestrator
        │
        ├── engines_registry.py   引擎清单与元数据（单一真相源）
        │
        ├── engine_*.py          各引擎适配器（仅负责构建 URL + 解析 HTML）
        │
        ├── http_client.py       统一 HTTP 出口（UA池/代理/重试/隐私头）
        │
        ├── ranking.py           SimHash 去重 + 多因子排序
        │
        └── cache.py             结果缓存 + 搜索历史
```

### 选择器与诊断

每引擎配多套备选选择器，引擎改版时自动尝试下一套。诊断结论：

| 诊断 | 含义 | 处理 |
|------|------|------|
| 正常 | 解析成功 | 无需处理 |
| 确认无结果 | 该关键词确实无匹配 | 换关键词或换引擎 |
| 被拦截 | 触发验证码或风控 | 降低频率，稍后重试 |
| 选择器失效 | 引擎改版导致解析不到 | 更新到最新版本 |
| 未知 | 页面结构异常 | 用 `--verbose` 查看详情 |

---

## 二、统一查询语法表

### bangs 语法（走 SearXNG 快捷跳转）

| 语法 | 目标 |
|------|------|
| `!w 关键词` | 维基百科 |
| `!gh 关键词` | GitHub |
| `!yt 关键词` | YouTube |
| `!gm 关键词` | Google Maps |
| `!scholar 关键词` | Google Scholar |

### 高级检索语法（V1.8 新增）

| 语法 | 说明 | 支持引擎 |
|------|------|---------|
| `site:example.com` | 站点限定 | baidu, bing, duckduckgo, yandex, searxng |
| `filetype:pdf` | 文件类型 | bing, searxng |
| `after:2025` | 时间下限 | searxng, baidu |
| `before:2026` | 时间上限 | searxng, baidu |

不支持语法的引擎自动本地过滤并注明。

### 垂直搜索模式（V1.8 新增）

| 模式 | 标识 | 优先引擎 | 排序权重 |
|------|------|---------|---------|
| 新闻 | `news` | 百度资讯、必应新闻 | 时效性↑ |
| 实时 | `realtime` | 百度、必应、SearXNG | 新鲜度↑ |
| 学术 | `academic` | Semanticscholar、百度学术 | 引用数↑ |
| 图片 | `image` | 百度图片、必应图片 | 相关度↑ |

---

## 三、完整 FAQ

### strict 模式

**Q: strict 模式在国内能用吗？**
A: 可以。strict 默认使用 Yandex（国内快）+ Startpage + Qwant + Brave，DDG 作最后备选。

**Q: strict 模式下指定 `--engines baidu` 为什么没生效？**
A: 这是有意设计。strict 模式会拒绝隐私保护不足的引擎，避免"以为开了 strict 实际仍在向百度发送查询词"。需要用百度请改用 `--privacy normal`。

**Q: strict 模式搜不到结果，直接返回空？**
A: 隐私引擎全部不可用时默认停止搜索，而非静默降级到国内引擎——因为 strict 用户的预期是宁可无结果也不泄露查询词。确需降级请加 `--allow-fallback`。

### 缓存与历史

**Q: 结果是旧的怎么办？**
A: 默认缓存 1 小时。加 `--no-cache` 强制刷新，或调小 `cache.ttl_seconds`。

**Q: 缓存文件会无限增长吗？**
A: 不会。超过 `cache.max_size_mb`（默认 50MB）时自动淘汰最久未使用的条目，历史记录上限 500 条。

**Q: 缓存和历史存在哪？如何彻底清除？**
A: 默认在 `~/.workbuddy/output/privacy-search-cache.db`。`--clear-cache` 清结果，`--clear-history` 清历史，两者独立。

### 隐私

**Q: 怎么确认隐私设置真的生效了？**
A: 加 `--privacy-report` 查看本次搜索实际使用的请求头、代理与被屏蔽引擎。

**Q: 如何隐藏 IP？**
A: 在 config.yaml 设置 `privacy.strict.proxy`，支持 `http://` 与 `socks5://`。留空为直连。

### 引擎

**Q: 某个引擎突然搜不到结果？**
A: 先跑 `--selftest`。若显示「选择器失效」说明该引擎改版了，请更新到最新版本；显示「被拦截」则是触发了风控，稍后再试或换引擎。

**Q: 为什么指定了 searxng 却没用上？**
A: 检查 `searxng.enabled` 是否为 true，以及本地实例是否已启动（`python -m scripts.searxng_manager status`）。

**Q: 排序结果不满意能调吗？**
A: 可以。config.yaml 的 `ranking` 段可调五个权重，例如更看重多引擎共识就调高 `consensus`。

**Q: 中文分词报缺少 jieba？**
A: jieba 为可选依赖，缺失时自动降级为字符级切分，搜索仍可用。安装后相关度排序更准。

**Q: 会记录我搜了什么吗？**
A: 日志默认 INFO 级别，只记录查询词长度不记录原文；搜索历史存于本地且可随时清空。需完全静默可设 `logging.level: OFF`。

**Q: SearXNG 启动失败？**
A: 尝试切换：`--method pip`。确保 Docker 或 Python 3.10+ 可用。

### 更新与安装

**Q: 如何关闭更新检查？**
A: `python -m scripts.update_checker disable`

**Q: 安装依赖失败？**
A: `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

**Q: 支持哪些引擎？**
A: 10 个：百度、必应、搜狗、360、DuckDuckGo、Yandex、Startpage、Qwant、Brave、本地 SearXNG。运行 `--list-engines` 查看完整属性。

### MCP Server

**Q: 如何在其他程序里调用？**
A: ① 命令行 `--json` 获取结构化输出；② MCP Server（V1.7 新增），通过 stdio JSON-RPC 2.0 暴露 search/synthesize/fetch 三工具。详见 `references/mcp_schema.md`。

**Q: Pro 模式和普通摘要的区别？**
A: Pro 模式会抓取搜索结果正文并生成带 citation 的答案，每个论断都能追溯到来源。普通摘要（`--summarize`）只基于 snippet 生成简短总结。Pro 模式需要配置 `synthesis.api_key`，无 Key 时自动降级为抽取式摘要。

**Q: Pro 模式抓取正文失败怎么办？**
A: 系统会自动降级为该结果的 snippet，不会中断整体流程。可在 config.yaml 调整 `synthesis.fetch_timeout` 和 `synthesis.chunk_size`。

**Q: 定时 selftest 怎么配置每天跑一次？**
A: config.yaml 中设置 `selftest_schedule.interval: daily`，然后用系统 cron 或任务计划程序定时触发 `python scripts/search.py --selftest-schedule run`。当前不支持后台常驻进程。

**Q: selftest 告警发到哪？**
A: 默认写入 `~/.workbuddy/output/privacy-search-selftest.log`，设置 `selftest_schedule.alert_channel: both` 可同时推送到企业微信 webhook。

**Q: 如何配置 webhook 告警？**
A: 在 config.yaml 的 `selftest_schedule.webhook_url` 填入企业微信/钉钉机器人的 webhook 地址。

**Q: 配置项太多，哪些必须改？**
A: 首次只需改 3 项（config.yaml 中标注 [推荐修改]）：`default_engines`、`timeout`、`default_mode`。其他保持默认。

### V1.8 新功能

**Q: 事实核查是什么？怎么用？**
A: 事实核查是 V1.8 新增的可信合成层。用 `--synthesize-pro --fact-check` 启用，逐条论断回链原文做 TF-IDF 余弦相似度比对，标注支撑度三级（充分/部分/无源），无源论断默认剔除。核查报告自动追加在答案末尾，含引用清单与核查方法说明。

**Q: 无源论断怎么处理？**
A: 默认自动剔除（`fact_check.remove_unsupported: true`）。如想保留但标注警告，设置 `fact_check.remove_unsupported: false`。阈值也可调：`sufficient_threshold`（默认 0.55）、`partial_threshold`（默认 0.25）。

**Q: 垂直搜索怎么用？**
A: `--vertical news/realtime/academic/image` 四类。新闻走百度资讯/必应新闻，学术走 Semanticscholar 开放接口（不可用时降级为通用引擎+学术关键词），图片走引擎图片端。每类有独立的引擎优先级和排序权重。

**Q: 高级检索语法和 bangs 冲突吗？**
A: 不冲突，统一为查询语法表。bangs（`!w` `!gh` `!yt`）走 SearXNG 原生快捷跳转，高级语法（`after:/before:/site:/filetype:`）映射为各引擎等价参数。不支持语法的引擎本地过滤并注明。

**Q: MCP Server 是什么？怎么用？**
A: MCP Server 是 V1.7 新增的 stdio JSON-RPC 2.0 服务，把搜索/合成/抓取能力暴露为标准工具协议。V1.8 为 synthesize 工具新增事实核查层。运行 `python scripts/mcp_server.py` 即可启动，可被 Claude Code、Cursor、n8n 等支持 MCP 的客户端挂载。详见 `references/mcp_schema.md`。

**Q: MCP Server 暴露了哪些工具？**
A: 3 个工具：`search`（多引擎隐私搜索）、`synthesize`（Perplexity 式答案合成 + V1.8 事实核查）、`fetch`（URL 正文抓取）。可通过 config.yaml 的 `mcp_server.tools` 缩减子集。

**Q: MCP Server 超时怎么办？**
A: 默认单次调用 30 秒，超时返回 JSON-RPC 错误响应，不中断服务。可在 config.yaml 调整 `mcp_server.timeout`。LLM 不可用时自动降级为抽取式，不影响 search/fetch 工具。
