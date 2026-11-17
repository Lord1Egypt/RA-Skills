# Infoseek 外部依赖清单（External Dependencies）

> 版本：v1.3.0 ｜ 说明：全部第三方依赖均为**可选降级**设计——缺失时自动走标准库兜底路径，不阻断核心流程（零依赖哲学）。
> 机器可读真源：`deps/registry.yaml`（19 项声明）+ `core/dep_registry.py`（`dep_status` / `import_optional` / `require`，S1 建表零回归）；本清单为人类可读视图。`requirements.txt` 为核心 + 文本分析 + 可选 LLM；`requirements-extra.txt` 为浏览器抓取。

## 一、必需依赖（直接 import，缺失即相关功能不可用）

| 依赖 | 版本下限 | 用途 | 加载方式 | 缺失影响 |
| --- | --- | --- | --- | --- |
| `PyYAML` | 6.0 | 解析 `domains/*.yaml` 领域配置与 `templates.yaml` 报告模板 | 模块级（domain_orchestrator / domain_router / exporter） | 领域编排与报告导出不可用 |
| `Jinja2` | 3.1 | 报告模板渲染（领域模板填充） | 懒导入（domain_orchestrator） | 模板渲染降级为纯文本拼接 |
| `httpx` | 0.27 | 异步 HTTP 客户端（Wikidata 同步等） | 懒导入（wikidata_sync） | 降级 urllib 同步请求 |

> 注：`openai` / `anthropic` 虽列于 requirements.txt，但**无 key 时自动降级 mock 模式**，不阻断（见下）。

## 二、文本分析（懒加载，缺失自动降级）

| 依赖 | 用途 | 加载位置 | 缺失降级 |
| --- | --- | --- | --- |
| `jieba` ≥0.42 | 中文分词 / TextRank 关键词 / 词性标注（POS） | anchor_adapter / entity_aliases / entity_profile / infoseek_pipeline（召回多字词硬门槛）/ zerodep_nlp / summarize_adapter | 中文关键词改走 summa 或零依赖共识 |
| `summa` ≥1.2 | TextRank 抽取式摘要 / 关键词（英文友好） | anchor_adapter / summarize_adapter / zerodep_nlp | 摘要降级首句截取 |

## 三、可选能力（requirements-extra.txt / 未硬性要求）

| 依赖 | 用途 | 加载位置 | 缺失降级 |
| --- | --- | --- | --- |
| `playwright` ≥1.44 | 抓取 L2 浏览器渲染（JS/SPA/反爬）+ L3 凭证辅助渲染 | mcp_tools_search（懒导入） | L2/L3 自动降级为 L1 静态抓取 |
| `keyring` | Key 管理系统密钥环后端（Windows Vault / macOS Keychain 等） | key_manager（懒导入） | 回退加密文件落盘（`.infoseek/keys.json`） |
| `schedule` | `freshness_cron daemon` 后台调度器 | freshness_cron.start_scheduler | 仅 daemon 命令受影响；full-scan/decay 正常 |
| `openai-whisper` | L4 多媒体音频/视频转录 | mcp_tools_search._probe_media | `transcript_available=False`，仅返回元信息 |
| `openai` ≥1.30 | OpenAI / DeepSeek 兼容端点的 LLM 调用 | llm_router（懒加载） | 该 provider 降级跳过，其余 provider 继续 |
| `anthropic` ≥0.34 | Claude LLM 调用 | llm_router（懒加载） | 同上 |

## 四、标准库能力（无第三方依赖）

- **搜索链**：urllib 实现 DDG HTML / Bing RSS / Wikipedia opensearch / Jina / CN 网页兜底
- **QVeris 能力路由**（v1.3）：urllib 直连 `https://qveris.ai/api/v1`（国际）/ `https://qveris.cn/api/v1`（CN，sk-cn- key 自动选区），零第三方依赖；Redis 式体质无需安装
- **相关性过滤**：`anchor_adapter.compute_semantic_similarity`（Jaccard 语义相似）
- **零依赖 NLP**：`infoseek_zerodep_nlp.py`（语言检测 / 句子切分 / ngram 关键词共识 / 摘要）——jieba/summa 全缺时的最终防线
- **冲突检测 / 实体识别 / 热度预测**：纯标准库（conflict_v3 / ner / entity_heat）

## 五、安装

```bash
pip install -r requirements.txt            # 核心 + 文本分析 + 可选 LLM
pip install -r requirements-extra.txt      # playwright（L2/L3 浏览器抓取）
pip install openai-whisper                 # L4 多媒体转录（可选）
```
