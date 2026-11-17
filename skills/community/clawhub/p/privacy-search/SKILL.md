---
name: privacy-search
description: "隐私优先的多引擎并行搜索 Skill，十大搜索引擎并行检索。V1.9 新增可信度标记和口语化错误建议，SKILL.md 瘦身至 ≤12KB。V1.8 新增可信合成与垂直搜索。V1.7 新增 MCP Server 形态。V1.6 新增 Perplexity 式答案合成。V1.5 新增网页正文抓取、结果导出、LLM 摘要。V1.2 统一 HTTP 出口、SimHash 去重、多因子排序、结果缓存、SearXNG 本地部署、隐私模式切换。"
version: 1.9.0
---


# 隐私搜索（Privacy Search）

隐私优先的多引擎并行搜索 Skill。V1.9 新增 **结果可信度标记**（每条结果标注「引擎数/10 引擎返回」）和 **口语化错误建议**。V1.8 新增可信合成与垂直搜索。V1.7 新增 MCP Server 形态。

## 环境要求

- Python 3.10+
- Docker（可选，推荐用于 SearXNG）
- 网络连接（本地 SearXNG 启动后可离线搜索）
- Windows / macOS / Linux

## 🚀 快速开始

```bash
python scripts/quick_setup.py              # 一键安装
python scripts/search.py "关键词"          # 一条命令搜索
python scripts/search.py "关键词" --privacy strict  # 隐私搜索
python scripts/update_checker check        # 检查更新
```

详细上手指南 → [QUICK_START.md](references/QUICK_START.md)

## 核心命令速查

### F1：多引擎并行搜索

```bash
python -m scripts.search "关键词"
python -m scripts.search "关键词" --engines baidu,bing
python -m scripts.search "关键词" --privacy strict
python -m scripts.search "关键词" --privacy strict --allow-fallback
python -m scripts.search "关键词" --json
python -m scripts.search "关键词" --verbose
python -m scripts.search --list-engines
python -m scripts.search --selftest
python -m scripts.search "关键词" --privacy-report
```

### F4：Perplexity 式答案合成（V1.6）

```bash
python -m scripts.search "关键词" --synthesize-pro
python -m scripts.search "关键词" --synthesize-pro --privacy strict
```

### F5：定时引擎告警（V1.6）

```bash
python -m scripts.search --selftest-schedule run
python -m scripts.search --selftest-schedule status
```

### F7：可信合成与垂直搜索（V1.8）

```bash
python -m scripts.search "量子计算" --synthesize-pro --fact-check
python -m scripts.search "AI 大模型" --vertical news
python -m scripts.search "突发新闻" --vertical realtime
python -m scripts.search "quantum computing" --vertical academic
python -m scripts.search "猫咪" --vertical image
python -m scripts.search "python教程 site:github.com filetype:pdf"
```

### F6：MCP Server（V1.7）

```bash
python -m scripts.mcp_server
python -m scripts.mcp_server --schema
python -m scripts.mcp_server --test
```

### 缓存与历史

```bash
python -m scripts.search "关键词" --no-cache
python -m scripts.search --cache-stats
python -m scripts.search --clear-cache
python -m scripts.search --history
python -m scripts.search --clear-history
```

### bangs 快捷语法

```bash
python -m scripts.search "!w 量子计算"
python -m scripts.search "!gh asyncio"
python -m scripts.search "!yt python 教程"
```

### F2：SearXNG 管理 / F3：隐私模式

```bash
python -m scripts.searxng_manager start --method docker
python -m scripts.searxng_manager status
python -m scripts.privacy mode --set strict
python -m scripts.privacy report
```

### 版本更新检查（死规则 11）

```bash
python -m scripts.update_checker check
python -m scripts.update_checker status
```

## 能做哪些

| 能力 | 说明 |
|------|------|
| 多引擎并发搜索 | 10 引擎并行，SimHash 去重 |
| 多因子加权排序 | 共识度 + 位次 + 相关度 + 权威度 + 域名质量 |
| 结果缓存 | 相同查询秒回，容量上限自动淘汰 |
| 搜索历史 | 本地留存最近 500 条 |
| 统一隐私出口 | 隐私头 / UA 池 / 代理 / 重试一致生效 |
| 隐私优先兜底 | strict 下拒绝非白名单引擎 |
| 本地 SearXNG | Docker/pip 双路径，query 不出本机 |
| bangs 语法 | `!w` `!gh` `!yt` 快捷跳转 |
| 解析健壮性 | 多套备选选择器，改版自动尝试 |
| 引擎体检 | `--selftest` 检查连通与解析状态 |
| 错误分类诊断 | 网络/配置/引擎三类，口语化建议 |
| 版本更新提醒 | 启动异步检查，24h 不重复 |
| Perplexity 式合成 | 抓取正文→分块→LLM 带 citation |
| 事实核查层 | 逐论断回链原文，三级标注支撑度 |
| 垂直搜索 | news/realtime/academic/image 四类 |
| 高级检索语法 | after:/before:/site:/filetype: |
| 定时引擎告警 | 每日/每小时自动 selftest |
| jieba 中文分词 | 默认安装，中文相关度提升 |
| MCP Server | stdio JSON-RPC 2.0，search/synthesize/fetch |
| 可信度标记 | 每条结果标注引擎数（3/10 返回） |

## 不能做哪些

- ❌ **不隐藏 IP 地址**：未配置代理时引擎可见真实 IP
- ❌ **不保证 100% 正文抓取**：部分网站反爬严格
- ❌ **不保证 LLM 摘要 100% 准确**：LLM 可能产生幻觉
- ❌ **不提供浏览器插件**（V2.0+ 规划）
- ❌ **不保证引擎长期可解析**：改版后需等待选择器更新

## 风险声明

### 隐私边界

| 风险 | 说明 | 缓解 |
|------|------|------|
| IP 可见性 | 不配置代理时引擎可见真实 IP | 设置 `privacy.strict.proxy` 或配合 VPN |
| 搜索词明文传输 | 查询词需发送至引擎 | strict 走隐私引擎或本地 SearXNG |
| 本地缓存留痕 | 缓存与历史含查询词 | `--clear-cache` / `--clear-history` |
| 日志留痕 | 默认 INFO 只记录查询词长度 | 需完全静默设 `logging.level: OFF` |
| SearXNG 端口暴露 | 默认 127.0.0.1 | 禁止改为 0.0.0.0 |

### 合规使用

| 风险 | 说明 | 缓解 |
|------|------|------|
| 搜索引擎条款 | 自动化访问可能受限 | 尊重 robots.txt |
| 数据合规 | 缓存与历史存于本地 | 共享设备建议关闭缓存 |

## 常见错误

### 网络故障 🌐

```
💡 网络连接失败，看起来是网络问题。
   • 检查网络：ping www.baidu.com
   • 确认代理：config.yaml 中 search.proxy
   • 加 --verbose 查看具体错误
```

### 配置错误 ⚙️

```
💡 配置有问题，config.yaml 没读对。
   • 确认 YAML 格式（冒号后面要有空格）
   • 复制 references/config.yaml.example 重新配置
```

### 引擎错误 🔧

```
💡 搜索引擎解析失败，引擎可能改版了。
   • 运行 --selftest 体检各引擎状态
   • 更新到最新版本
   • 用 --engines 排除问题引擎
```

## 常见问题

**Q: strict 模式在国内能用吗？**
A: 可以。默认 Yandex + Startpage + Qwant + Brave，DDG 作最后备选。

**Q: strict 模式下指定 `--engines baidu` 为什么没生效？**
A: 有意设计。strict 拒绝隐私保护不足的引擎。需用百度请改用 `--privacy normal`。

**Q: 结果是旧的怎么办？**
A: 默认缓存 1 小时。加 `--no-cache` 强制刷新。

**Q: 缓存文件会无限增长吗？**
A: 不会。超过 50MB 自动淘汰最久未使用条目。

**Q: 怎么确认隐私设置真的生效了？**
A: 加 `--privacy-report` 查看实际请求头、代理与被屏蔽引擎。

**Q: 如何隐藏 IP？**
A: config.yaml 设置 `privacy.strict.proxy`，支持 `http://` 与 `socks5://`。

**Q: 某个引擎突然搜不到结果？**
A: 先跑 `--selftest`。选择器失效说明改版，更新到最新版本。

**Q: 排序结果不满意能调吗？**
A: 可以。config.yaml 的 `ranking` 段可调五个权重。

**Q: 会记录我搜了什么吗？**
A: 日志默认只记录查询词长度；搜索历史存于本地且可随时清空。

**Q: 支持哪些引擎？**
A: 10 个：百度、必应、搜狗、360、DuckDuckGo、Yandex、Startpage、Qwant、Brave、本地 SearXNG。

**Q: 如何在其他程序里调用？**
A: ① `--json` 获取结构化输出；② MCP Server（stdio JSON-RPC 2.0）。详见 `references/mcp_schema.md`。

**Q: Pro 模式和普通摘要的区别？**
A: Pro 模式抓取正文生成带 citation 的答案。普通摘要（`--summarize`）只基于 snippet 生成简短总结。

**Q: 事实核查是什么？怎么用？**
A: V1.8 新增。用 `--synthesize-pro --fact-check` 启用，逐论断回链原文做相似度比对，标注支撑度三级。

**Q: 垂直搜索怎么用？**
A: `--vertical news/realtime/academic/image` 四类。每类有独立引擎优先级和排序权重。

**Q: 高级检索语法和 bangs 冲突吗？**
A: 不冲突。详见 `references/detail_engine_syntax_faq.md`。

**Q: MCP Server 是什么？怎么用？**
A: stdio JSON-RPC 2.0 服务。运行 `python scripts/mcp_server.py` 启动。详见 `references/mcp_schema.md`。

**Q: 配置项太多，哪些必须改？**
A: 首次只需改 3 项：`default_engines`、`timeout`、`default_mode`。

## 项目结构

```
privacy-search/
├── SKILL.md
├── requirements.txt
├── scripts/
│   ├── search.py              # F1: 搜索编排与 CLI
│   ├── searxng_manager.py     # F2: SearXNG 管理
│   ├── privacy.py             # F3: 隐私模式
│   ├── engines_registry.py    # 引擎清单
│   ├── engine_selectors.py    # 选择器与诊断
│   ├── http_client.py         # 统一 HTTP 出口
│   ├── ranking.py             # 去重与排序
│   ├── cache.py               # 缓存与历史
│   ├── logging_util.py        # 日志
│   ├── version_util.py        # 版本解析
│   ├── update_checker.py      # 更新检查（死规则 11）
│   ├── quick_setup.py         # 一键安装
│   ├── synthesiser.py         # F4: 答案合成
│   ├── selftest_scheduler.py  # F5: 定时告警
│   ├── mcp_server.py          # F6: MCP Server
│   ├── fact_checker.py        # F7: 事实核查
│   ├── vertical_search.py     # F7: 垂直搜索
│   └── query_parser.py        # F7: 高级语法
├── references/
│   ├── config.yaml.example
│   ├── engines.md
│   ├── engines_zh.md
│   ├── mcp_schema.md
│   ├── QUICK_START.md
│   └── detail_engine_syntax_faq.md
└── tests/
```

## 更新日志

| v1.9.0 | 2026-09-19 | 增加：结果可信度标记（每条结果标注「引擎数/10 引擎返回」）；优化：错误诊断升级为口语化建议；优化：SKILL.md 瘦身至 ≤12KB（引擎细节/语法表/FAQ 迁 references/）；优化：quick_setup 输出简化 |
| v1.8.0 | 2026-09-19 | 增加：事实核查层（逐论断回链原文，三级标注支撑度）；增加：垂直搜索（news/realtime/academic/image）；增加：高级检索语法（after:/before:/site:/filetype:）；增加：内容处理管线 |
| v1.7.0 | 2026-08-28 | 增加：MCP Server（stdio JSON-RPC 2.0，search/synthesize/fetch 三工具） |
| v1.6.0 | 2026-08-17 | 增加：Perplexity 式答案合成；增加：定时 selftest 调度+引擎失效告警 |
| v1.5.0 | 2026-08-07 | 增加：网页正文抓取；增加：结果导出（Markdown/HTML/PDF）；增加：LLM 摘要 |
| v1.1.0 | 2026-07-19 | 增加 4 个国内可用备选引擎；strict 模式自动降级与故障转移 |
| v1.0.0 | 2026-07-18 | 初始版本发布 |

## 支持与反馈

- **联系邮箱**：njskills@agent.qq.com
- **问题反馈**：欢迎通过邮件或 SkillHub 评论提出建议
- **版本更新**：运行 `python -m scripts.update_checker check` 检查新版本