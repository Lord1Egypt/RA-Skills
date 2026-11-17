# Infoseek

> 端到端内容智能采集与调研工作流。**v2.6.1 发布版**。

[![Status](https://img.shields.io/badge/status-GA%20stable-brightgreen)](#)
[![Version](https://img.shields.io/badge/version-2.6.1-blue)](#)
[![Tests](https://img.shields.io/badge/tests-88%20suites%20green-success)](#)
[![MCP](https://img.shields.io/badge/MCP-19%20tools-blueviolet)](#)

---

## 5 秒看懂

```python
# scripts/ 与 core/ 不在 site-packages，需先把 scripts 加入 PYTHONPATH（见下文「安装」）
import sys; sys.path.insert(0, "scripts")
from infoseek_core_v2 import streaming_research

# 流式研究：lite 模式多步 yield，秒级完成
async for partial in streaming_research("GPT-5", sources, lite=True):
    print(partial["step"], "...")
```

```bash
# MCP server（18 规范工具 + 12 兼容并存，见下文「MCP 工具面」）
python scripts/infoseek_mcp_server.py
```

---

## 🎉 2.x 能力概览

| 能力 | 说明 |
|------|------|
| 🧭 **搜索引擎全生命周期** | 健康状态机 / 配额追踪 / 认证粘滞 + 新鲜度自愈（配额重置、冷却恢复、API 漂移检测）+ CLI engine-status/reconcile/probe |
| 🎯 **搜索召回增强** | query 别名扩展 / 跨引擎多样性轮询 / 自适应相关性门槛 / 动态层权重；v1.9.0 起人名 NER 消歧 + 跨语言别名桥接 |
| 🕸️ **4 级抓取** | L1 静态 → L2 浏览器渲染 → L3 凭证辅助（KeyManager 注入，仅内存）→ L4 多媒体 chunk（whisper 可选降级） |
| 💯 **四维锚点评分（唯一口径）** | interaction / topic_match / credibility / llm_readability 四维 base + 信任源/KB 加权；0–1 量纲入口自动归一（P0-OPEN-04），三链路同一聚合真源 |
| ⚖️ **矛盾检测（键控事实槽）** | GA11 同槽键值冲突 + 否定/反义 + **P0-OPEN-06 时间事实槽**（年月/季度→ISO 区间）；结果区分 冲突 / 无冲突 / 未评估，附覆盖率 |
| 🗂️ **按域报告模板** | 5 领域 profile + templates.yaml（v3.2.0）：tech 已收窄为通用技术（制造 + AI/软件），高分源（≥70）跨源综合段，核心源为 0 时禁止空骨架 |
| 🕵️ **OSINT 身份归因** | v2.1.0 双源（sherlock + maigret）真实 CLI 契约 + 双源聚合去重；默认 OFF + consent 授权闸（`infoseek_consent_cli.py`） |
| 🔗 **QCM 协同** | `qcm_query` 反向调用归零质量管理框架；QVeris 能力路由 + 统一能力注册表 |
| ✅ **回归测试** | **62 套件**（`tests/run_all.py` 统一入口，绿基线 0 FAIL；可选依赖缺失自动 SKIP，不污染基线） |

---

## 快速上手

### 1. 安装 / 升级

```bash
pip install -r requirements.txt            # 核心 + 文本分析 + 可选 LLM
pip install -r requirements-extra.txt      # playwright（L2/L3 浏览器抓取，可选）
# 完整依赖说明见 references/external-deps.md
```

> **PYTHONPATH（重要）**：infoseek 的 `scripts/` 与 `core/` 是**脚本风格模块**，
> 未打包安装到 site-packages。在 skill 根目录之外以脚本/SDK 方式调用时，需让
> Python 能找到它们，二选一：
>
> ```bash
> # 方式 A：运行前导出（scripts + core 都需要时）
> export PYTHONPATH="$PWD/scripts:$PWD/core:$PYTHONPATH"
> python your_script.py
> ```
> ```python
> # 方式 B：代码内注入（推荐写在入口顶部）
> import sys
> sys.path.insert(0, "/path/to/infoseek/scripts")
> sys.path.insert(0, "/path/to/infoseek/core")
> from infoseek_core_v2 import research
> ```
>
> MCP server 与 `tests/run_all.py` 已内部处理路径，**无需**手动设置 PYTHONPATH。
> 可选依赖（jieba / pypinyin / jinja2 / playwright 等）缺失时自动降级或 SKIP，不致命。

### 2. Python SDK

```python
import sys; sys.path.insert(0, "scripts")
from infoseek_core_v2 import (
    research,            # 同步（兼容入口）
    async_research,      # 异步（推荐）
    streaming_research,  # 流式（推荐目标）
)
from infoseek_core_v2 import score_source, detect_conflicts

res = research("GPT-5", sources, lite=True)
async for partial in streaming_research("GPT-5", sources, lite=True):
    pass  # partial['step'] ∈ {score_complete, wikidata_complete, ...}

# 评分：入参 score 可为 0–1（自动 ×100 归一）或 0–100；返回含 classification / base_origin
r = score_source({"url": "...", "title": "...", "snippet": "..."}, "GPT-5")
```

### 3. MCP 集成

项目提供 `.mcp.json`（双服务器配置，可直接被 Claude/Codex 等客户端加载）：

```json
{
  "mcpServers": {
    "infoseek-search": {
      "command": "${INFOSEEK_ROOT}/scripts/infoseek_mcp_server.py",
      "args": ["--transport", "stdio"],
      "env": {
        "INFOSEEK_ROOT": "${INFOSEEK_ROOT}",
        "INFOSEEK_DB": "${HOME}/.infoseek/infoseek_db.json",
        "INFOSEEK_ARCHIVE": "${HOME}/infoseek-archives"
      }
    }
  }
}
```

> 💡 Windows 环境请将 `command` 改为 `python3` + `args: ["脚本路径", "--transport", "stdio"]`。

**MCP 工具面（v2.2.0 = 18 规范工具 + 12 兼容并存）**：

| # | 规范工具 | 用途 |
|---|------|------|
| 1 | `search_anchors_async` | 锚点发现（真实多引擎搜索） |
| 2 | `fetch_content_async` | 4 级降级抓取正文 |
| 3 | `save_archive_async` | 调研产物归档 |
| 4 | `check_dedup_async` | 去重校验 |
| 5 | `dedup_stats_async` | 去重统计 |
| 6 | `fuse_analysis_async` | 跨源融合分析 |
| 7 | `cross_subject_analysis_async` | 跨主题分析 |
| 8 | `summarize_content_async` | 内容摘要 |
| 9 | `conflict_detection_async` | 实体感知冲突检测（v3） |
| 10 | `score_source_async` | 单源四维评分（唯一聚合口径） |
| 11 | `score_contradiction_async` | 声明对矛盾评分（键控槽 + 时间槽 + 否定路） |
| 12 | `research_v3` | 研究主入口 |
| 13 | `research_stream` | 流式研究（多步 progress 推送） |
| 14 | `manage_keys` | Key 管理（list/stat/rotate/revoke，脱敏） |
| 15 | `key_usage` | Key 用量成本报表 |
| 16 | `qcm_query` | 反向调用 QCM 归零质量管理框架 |
| 17 | `identity_attribution` | OSINT 用户名→跨平台身份归因（默认 OFF + consent） |
| 18 | `account_forensics` | 账号可信度取证（FakeDetect，默认 OFF + consent） |

> 工具定义真源：`scripts/infoseek_mcp_server.py` 的 `_CANONICAL_TOOL_NAMES`（**18 项**）。
> 12 个 v1.x 同步名（`search_anchors` / `fetch_content` / … / `research`）为**兼容并存期**，
> 结果附 `deprecated: true` + `migrate_to`，计划 v4.0.0 冻结。

---

## 预留接口（可选扩展 · 默认关闭）

> 原则：**默认零风险、扩展按需开启**。以下能力**默认不启用**；接口与开关语义已定义，
> 供你按需选择。如需启用，按表中说明配置，或提出需求由我们按你的策略实现
> （启用不改变其他默认行为）。

### 1. 搜索层引擎请求缓存（预留 · 默认关闭）

**默认行为（现状）**：**不缓存**。每次搜索都实时请求搜索引擎端点
（DuckDuckGo / Bing-RSS / Jina / Wikipedia / 智谱 / CN-Web …），保证结果时效性。

> 注：**目标网页内容抓取**（`tool_fetch_content` 链路）**已接入** `http_cache.py`
> （LRU + TTL + 容量上限，默认存 `~/.infoseek/http_cache/`），与本节无关。

| 项 | 值 |
|---|---|
| 预留开关 | `INFOSEEK_SEARCH_HTTP_CACHE`（`0` = 关闭·默认 / `1` = 开启）|
| 预留 TTL | `INFOSEEK_SEARCH_HTTP_CACHE_TTL`（秒，建议 60–300）|
| 生效范围 | 搜索层 `infoseek_pipeline._http_get()` 的引擎端点请求 |

**取舍（请选择）**：缓存引擎请求可**省流量、抗限流、加速降级**，但会**直接返回陈旧搜索结果**。
各引擎时效特性不同（DuckDuckGo / Bing 变化快，Wikipedia 较稳定），建议启用时按引擎分级 TTL，
或仅在「失败重试 / 降级」场景缓存。

### 2. 知识库（KB）接线（预留 · 默认未接线）

**默认行为（现状）**：infoseek 为**闭环采集器** —— 调研产物落本地（archive / dedup），
**不从外部知识库取信源，也不回写知识库**。

> 注：`trusted_kb.py`（可信资源库）与 `core/entity_profile.py`（实体画像）为 skill
> **内部**可信库，与知识库平台无关。

| 预留方向（请选择其一） | 含义 | 规划接口 |
|---|---|---|
| A. KB → infoseek | 知识库作为信源召回，与 web 结果混排 | `INFOSEEK_KB_ID` + 检索 API |
| B. infoseek → KB | 调研报告自动归档进知识库 | `INFOSEEK_KB_ID` + 新建 / 写入文档 API |
| C. 双向 | A + B | 同上 |

**启用前需确定**：知识库 ID（`kb_id`）、写入格式（Markdown / 文件）、去重与更新策略。

**如何选择**：提供 kb_id 与方向（A / B / C），我们按契约接线；未选择时保持默认
（不接线、零行为变化）。

---

## 搜索层并发与聚合窗口（G5 · 默认开启）

> 搜索层默认**全引擎并发 + 聚合窗口**：并发上限 12、窗口 8s（仅对超慢引擎生效）。

| 参数 | 默认 | 说明 |
|---|---|---|
| `INFOSEEK_SEARCH_MAX_WORKERS` | `12` | 进程级常驻池并发上限（懒创建，不浪费线程）|
| `INFOSEEK_SEARCH_WINDOW_MS` | `8000` | 聚合窗口；到期即聚合返回，未达引擎结果丢弃；`0` = 关闭（回退原语义）|
| `INFOSEEK_SEARCH_EARLY_FACTOR` | `1.5` | 提前收敛倍数：已完成引擎去重结果 ≥ max_results×factor 即提前返回；`0` = 关闭 |
| `INFOSEEK_SEARCH_SHARED_BUDGET` | `1` | 层间共享总预算（AI 层与默认层共享一个窗口，总延迟有上界）；`0` = 各层各耗窗口 |
| `INFOSEEK_SEARCH_TOTAL_BUDGET_MS` | `= WINDOW_MS` | 层间共享总预算时长（覆盖默认窗口值）|
| `INFOSEEK_SEARCH_OVERRUN_LIMIT` | `2` | 连续超窗次数阈值；达阈值 → 引擎临时降权（暂停拉起）；`0` = 关闭降级 |
| `INFOSEEK_SEARCH_OVERRUN_MUTE_S` | `60` | 降权冷却秒；到期自动复活（计数清零重新积累）；`0` = 静默到进程结束 |

**行为**：
- **常驻池**：线程池进程级复用，单次搜索退出不再 `shutdown(wait=True)` 阻塞 → 层耗时不再等于最慢引擎。
- **聚合窗口**：`wait(timeout=window)` 到期即返回；**正常场景（引擎均 < 窗口）零影响** —— 全部完成即立即返回，
  仅截断病态慢引擎（实测：3s 慢引擎 + 快引擎，窗口 400ms → **0.8s** 返回完整快引擎结果）。
- **提前收敛（v1.6.1）**：轮询 `FIRST_COMPLETED`，已完成引擎结果 ≥ max_results×1.5 即提前返回（不等满窗）——
  高产出批次（如 5 引擎×10 条）最快 0.05s 返回，且不丢已完成结果。
- **超窗引擎（v1.6.1）**：结果丢弃，健康记录仍由线程内正常完成（**不误杀引擎**）；连续超窗达阈值
  → 临时降权（`_filter_muted` 不再拉起该引擎），冷却后自动复活 —— 慢引擎自我淘汰，不拖累整链。
- **保留兜底入预算（v1.6.1）**：主并行不足 `min_expected` 时兜底，保留引擎**并行提交并纳入剩余预算**
  （原 0.8s×N 串行兜底移除）；预算耗尽（剩余 ≤0.05s）则跳过兜底，延迟上界优先。
- **层间共享总预算（v1.6.1）**：AI 层与默认层共享一个 deadline（总预算 = WINDOW 或 TOTAL_BUDGET_MS）——
  AI 层未耗完则默认层继承剩余预算（结果不丢）；AI 层耗完则默认层快速失败，**总延迟不再两层叠加**；
  层间 0.8s 限速在剩余预算不足时自动跳过（预算即节流）。
- **一键回退**：`INFOSEEK_SEARCH_WINDOW_MS=0` 回到旧行为。`INFOSEEK_SEARCH_SHARED_BUDGET=0`
  `INFOSEEK_SEARCH_EARLY_FACTOR=0` `INFOSEEK_SEARCH_OVERRUN_LIMIT=0` 分别关闭 P1/P2 各子能力。

---

## 文档导航

| 文档 | 用途 |
|------|------|
| [SKILL.md](SKILL.md) | Skill 完整定义（概念/能力/触发词） |
| [RELEASE_NOTES.md](RELEASE_NOTES.md) | 版本发布说明 |
| [requirements.txt](requirements.txt) | 运行时依赖清单 |
| [references/external-deps.md](references/external-deps.md) | 外部依赖清单 + 作用 + 降级路径 |
| [references/api-keys.md](references/api-keys.md) | 外部 API Key 清单 + 效益 + 获取 |
| [references/ROADMAP.md](references/ROADMAP.md) | 当前基线 · 待办 · 前景方向（纯净版） |
| references/ROADMAP_archive_20260917.md | v1.0.0→v2.0.0 历史实施记录归档 |
| [tests/](tests/) | 测试套件（85 个 `test_*.py`；标准聚合入口 `run_tests.py`，并发全量 `run_all.py`） |

> ℹ️ **冷启动说明**：运行时状态（`claims.json`、`entity_aliases.json`、`pending_entities.json`、`anchor_db.json`、`engine_state.json` 等）首跑为空占位，运行后随调研逐步积累。这些文件**不写入技能源码目录**，落在运行时数据目录（默认 `~/.infoseek/`，可用 `INFOSEEK_DATA_DIR` 覆盖），技能更新不丢数据。详见 `core/state_dir.py`。

---

## 版本路线

| 版本 | 状态 | 备注 |
|------|------|------|
| v2.2.0 | 🟢 **当前发布版** | GA11 三元事件身份 + 跨文本时间槽键 + LLM 路径收口；HF 人因指纹增强；G7/G8 文档口径与入口类型契约 |
| v2.1.0 | ✅ 历史 | OSINT 双客户端真实 CLI 契约修复 + 双源聚合 + consent 授权 CLI |
| v2.0.0 | ✅ 历史 | GA11 键控事实槽矛盾检测 + GA12 网络边界门控；DSH 插件 manifest |
| v1.9.0 | ✅ 历史 | GA9 人名消歧五步 + GA10 跨语言别名桥接 |
| v1.8.x | ✅ 历史 | 版本单源化 / 回归 runner / 评分三链路口径统一 / 分词单源化 |
| v1.5.0 | ✅ 历史 | 身份归因能力链 P0：发现→验证闭环（v2.1.0 已重写其 CLI 契约） |
| v1.4.1 | ✅ 历史 | 引擎生命周期 / 召回增强 / 4 级抓取 / Key 管理 / perf 10k |
| 后续 | 🟡 待办 | 见 `references/ROADMAP.md` |

---

## 测试

> 测试为「脚本风格」（顶层直接执行），**不要用 pytest 直接收集**（会因 SystemExit 崩溃）。
> 标准入口：**`python tests/run_tests.py`**（88 标准套件）。当前共 **89 个 `test_*.py`**，绿基线判据
> = 0 FAIL + 0 TIMEOUT；SKIP 单列（可选依赖缺失，不污染基线）。

```bash
python tests/run_tests.py               # 标准回归（77 套件，唯一验收入口）
python tests/run_all.py --timeout 300   # 并发全量（放宽每套件超时）
python tests/test_three_chain_v183.py   # 单套件直跑
```

- **run_tests.py（标准聚合入口 · 推荐）**：逐子进程直跑，排除深度测试 `test_deep_v101.py` → **88 标准套件**；
  v2.1.0 已修正 SKIP 判定（旧逻辑 returncode==0 先短路吞掉自报 SKIP、且只看 stdout）。
- **run_all.py（并发全量）**：4 并发统一发现**全部** `test_*.py`、隔离搜索 env
  （`INFOSEEK_PLATFORM_WEBSEARCH=off`）、per-suite 超时、PASS/FAIL/SKIP 三态严格归类、结果 JSON 落盘。
- **SKIP / 可选依赖**：jieba / pypinyin 等可选依赖缺失时，相关套件自报
  `0 PASS / N SKIP` 并 `exit 0`，run_all 归类 SKIP；装齐依赖后自动恢复为全断言运行。
- **性能套件**：`test_perf_v101.py` 为独立观测（LRU 缓存基线），在 SLOW_SUITES 中给独立超时。

> 环境差异说明：`test_stability_v240.py` 在 POSIX 环境含内存维度（ru_maxrss）；Windows 下自动跳过内存判定，不误报 FAIL。

---

## 项目结构

```
infoseek/
├── SKILL.md            # Skill 定义（yfm + 文档）
├── manifest.yaml       # 平台 manifest
├── RELEASE_NOTES.md   # 版本发布说明
├── README.md           # 本文件
├── core/               # 核心库（矛盾评分/实体图谱/身份归因/状态管理）
│   ├── conflict_v3.py / contradiction_scorer.py  # 冲突 v3 + 键控/时间事实槽
│   ├── person_ner.py / xling_bridge.py           # v1.9.0 人名消歧 + 跨语言别名
│   ├── identity_aggregator.py / maigret_client.py / sherlock_client.py  # v2.1.0 OSINT
│   ├── entity_*.py     # graph/heat/profile/trajectory/tracker/aliases
│   ├── wikidata_sync.py / freshness_cron.py / claim_store.py
│   ├── key_manager.py / llm_router.py / ner.py / trust_sources.py
│   └── state_dir.py
├── scripts/            # 适配层 + MCP server
│   ├── infoseek_core_v2.py       # 核心 API（research/async/streaming/score/conflict）
│   ├── infoseek_mcp_server.py    # MCP server 门面（18 规范工具 + 12 兼容并存）
│   ├── mcp_tools_*.py            # 工具模块（search/archive/analysis/keys/async/common/qcm）
│   ├── domain_router.py          # 5 领域路由（词边界匹配 + 多域交集）
│   ├── domain_orchestrator.py    # 领域调度 + 按域模板渲染 + 过滤清单
│   ├── infoseek_pipeline.py      # 搜索降级链 + 召回增强
│   ├── engine_lifecycle.py       # 搜索引擎全生命周期
│   ├── infoseek_consent_cli.py   # v2.1.0 能力授权 CLI（list/grant/revoke/doctor）
│   └── ...
├── references/         # 契约 + 配置（keyword.yaml / contradiction-synonyms.json）+ 依赖/Key/路线图
├── deps/               # 外部依赖注册表（registry.yaml，S1 建表零回归）
├── domains/            # 领域配置（tech/market/finance/policy/competitor）
│   ├── *.yaml          # 领域 profile（Markdown 文本，raw 读取）
│   └── templates.yaml  # 报告模板（v3.2.0，含跨源综合段 + 空源守卫）
├── tests/              # 89 个测试文件（run_all.py 全发现；run_tests.py → 88 标准套件）
└── dist/               # perf 基准（perf_baseline_v101 / perf_profile_v101）+ 生态构建产物
```

---

## 贡献与反馈

- **Bug 报告**：附 `infoseek --version` + 最小复现
- **性能问题**：附 `dist/perf_baseline_v101.json` 对比
- **功能请求**：附用例 + 期望输出
- **路线图**：见 `references/ROADMAP.md`

---

> v2.2.0 | 三元事件身份 + 键控/时间事实槽矛盾检测 + 四维锚点评分 + 人因指纹增强（HF） | 多生态（ima/Claude/Codex/Dify/Coze）| MIT License
