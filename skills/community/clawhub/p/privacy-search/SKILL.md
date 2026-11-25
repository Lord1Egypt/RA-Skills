---
name: privacy-search
description: "隐私优先的多引擎并行搜索 Skill，十大搜索引擎并行检索。V2.1 新增可信答案 RAG-lite（本地 TF-IDF，结论/依据/反证三段，零 Key）和隐私量化报告（隐私分数+档案周报+DNS 泄露提示+SearXNG 一键自检）；无源论断标注保留；答案缓存「上次搜过」提示。V1.9 可信度标记与口语化错误建议。V1.8 可信合成与垂直搜索。V1.7 MCP Server。"
version: 2.1.0
---


# 隐私搜索（Privacy Search）

隐私优先的多引擎并行搜索 Skill。V2.1 新增 **可信答案 RAG-lite**（结论/依据/反证三段，全本地 TF-IDF，零 Key）和 **隐私量化报告**（隐私分数 + DNS 泄露提示 + SearXNG 一键自检）。V1.9 新增结果可信度标记与口语化错误建议。V1.8 新增可信合成与垂直搜索。

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
python -m scripts.search "关键词"                          # 基础搜索
python -m scripts.search "关键词" --engines baidu,bing     # 指定引擎
python -m scripts.search "关键词" --privacy strict         # 隐私模式
python -m scripts.search "关键词" --privacy strict --allow-fallback  # 允许降级
python -m scripts.search "关键词" --json / --verbose       # JSON/详细诊断
python -m scripts.search --list-engines / --selftest       # 引擎列表/体检
python -m scripts.search "关键词" --privacy-report         # 隐私摘要
```

### F4/F8：答案合成 + RAG-lite（V1.6/V2.1）

```bash
python -m scripts.search "关键词" --synthesize-pro              # 无 Key 自动走 RAG-lite 三段
python -m scripts.search "关键词" --synthesize-pro --privacy strict
python -m scripts.search "量子计算" --synthesize-pro --fact-check  # 事实核查
```

### F5：定时引擎告警（V1.6）

```bash
python -m scripts.search --selftest-schedule run    # status 查上次结果
```

### F7：垂直搜索与高级语法（V1.8）

```bash
python -m scripts.search "AI 大模型" --vertical news
python -m scripts.search "突发新闻" --vertical realtime
python -m scripts.search "quantum computing" --vertical academic
python -m scripts.search "猫咪" --vertical image
python -m scripts.search "python教程 site:github.com filetype:pdf"
```

### F8：可信答案 RAG-lite（V2.1）

```bash
# synthesize v2：无 Key 自动走 RAG-lite 三段答案（结论/依据/反证）
python -m scripts.search "量子计算的优势" --synthesize-pro

# 显示本次搜索隐私分数
python -m scripts.search "关键词" --privacy-score
```

无源论断默认标注 `[无源]` 保留进正文（可配置剔除），依据引用全部可回链原文。

### F9：隐私量化报告（V2.1）

```bash
python -m scripts.search --privacy-profile report   # 隐私档案周报
python -m scripts.search --privacy-profile dns      # DNS 泄露检测
python -m scripts.search --privacy-profile cookie   # cookie 零残留自检
python -m scripts.search --searxng-audit            # SearXNG 一键自检
```

### F6：MCP Server（V1.7）

```bash
python -m scripts.mcp_server
python -m scripts.mcp_server --schema
python -m scripts.mcp_server --test
```

### 缓存/历史/bangs/SearXNG/隐私模式

```bash
python -m scripts.search "关键词" --no-cache     # 跳过缓存
python -m scripts.search --history               # 搜索历史
python -m scripts.search --clear-cache           # 清缓存
python -m scripts.search "!w 量子计算"           # bangs：维基/GitHub/YouTube
python -m scripts.searxng_manager start --method docker  # 启动本地 SearXNG
python -m scripts.privacy mode --set strict      # 切换隐私模式
python -m scripts.privacy report                 # 隐私报告
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
| 可信答案 RAG-lite | 结论/依据/反证三段，全本地 TF-IDF，零 Key；无源标注保留 |
| 答案缓存提示 | 相同/近似问题提示「上次搜过」 |
| 隐私量化报告 | 五指标隐私分+档案周报；DNS 泄露提示；SearXNG 一键自检 |

## 不能做哪些

- ❌ **不隐藏 IP 地址**：未配置代理时引擎可见真实 IP
- ❌ **不保证 100% 正文抓取**：部分网站反爬严格
- ❌ **不保证 LLM 摘要 100% 准确**：LLM 可能产生幻觉
- ❌ **不提供浏览器插件**（V2.0+ 规划）
- ❌ **不保证引擎长期可解析**：改版后需等待选择器更新

## 风险声明

### 隐私边界

| 风险 | 缓解 |
|------|------|
| IP 可见性（未配代理时引擎可见真实 IP） | 设置 `privacy.strict.proxy` 或配合 VPN |
| 搜索词明文传输 | strict 走隐私引擎或本地 SearXNG |
| 本地缓存/日志留痕 | `--clear-cache`/`--clear-history`；日志只记长度，静默设 `logging.level: OFF` |
| SearXNG 端口暴露 | 默认 127.0.0.1，禁止改为 0.0.0.0 |

### 合规使用

自动化访问须尊重 robots.txt；缓存与历史存于本地，共享设备建议关闭缓存。

## 常见错误

失败时输出口语化建议（非堆栈）：🌐 网络问题→检查网络/代理/`--verbose`；⚙️ 配置错误→确认 YAML 格式（冒号后有空格）/复制 config.yaml.example；🔧 引擎解析失败→`--selftest` 体检/更新版本/`--engines` 排除问题引擎。

## 常见问题

> 完整 FAQ（41 条，含全部参数细节）→ `references/detail_engine_syntax_faq.md`

**Q: strict 模式在国内能用吗？怎么隐藏 IP？**
A: 可以，默认 Yandex + Startpage + Qwant + Brave，DDG 兜底；指定 `--engines baidu` 不生效是有意设计。隐藏 IP 设 `privacy.strict.proxy`（http/socks5），`--privacy-report` 查看实际生效配置。

**Q: RAG-lite 三段答案 / 无源论断 / 隐私分数怎么用？**
A: `--synthesize-pro` 无 Key 自动走 RAG-lite（结论/依据/反证，全本地零 Key）；无源论断默认标注 `[无源]` 保留；`--privacy-score` 显示隐私分，`--privacy-profile report/dns/cookie` 看周报/查泄露/查零残留，`--searxng-audit` 自检 SearXNG。详情见 references FAQ。

**Q: 支持哪些引擎 / 如何在其他程序调用？**
A: 10 个：百度、必应、搜狗、360、DuckDuckGo、Yandex、Startpage、Qwant、Brave、本地 SearXNG。调用：`--json` 或 MCP Server（stdio JSON-RPC 2.0）。详见 `references/mcp_schema.md`。

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
│   ├── fact_checker.py        # F7: 事实核查（V2.1 无源标注保留）
│   ├── vertical_search.py     # F7: 垂直搜索
│   ├── query_parser.py        # F7: 高级语法
│   ├── rag_lite.py            # F8: RAG-lite 三段答案（V2.1）
│   ├── privacy_score.py       # F9: 隐私分数与档案（V2.1）
│   └── searxng_audit.py       # F9: SearXNG 自检（V2.1）
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

| v2.1.0 | 2026-11-18 | 增加：可信答案 RAG-lite（多源正文→本地分块→TF-IDF 选块→结论/依据/反证三段答案，无 Key 抽取式为主）；优化：核查与合成合链（无源论断标注 [无源] 保留进正文，非黑盒剔除）；增加：答案缓存「上次搜过」提示；增加：隐私分数体系（五指标加权，累计隐私档案周报）；增加：strict DNS 泄露提示与 cookie 零残留自证；增加：SearXNG 一键自检清单；修复：--synthesize-pro 参数未注册问题 |
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