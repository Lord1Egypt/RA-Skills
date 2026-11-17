# Infoseek 外部 API Key 清单（API Keys Reference）

> 版本：v1.2.0 ｜ 说明：所有 Key 均为**可选**——不配置时自动降级（LLM 走 mock、搜索层自动跳过限量引擎），核心免费搜索链（DDG/Bing/Wikipedia/Jina）无需任何 Key 即可工作。Key 经 `KeyManager` 归一化管理（加密落盘 + 系统 keyring 后端 + 状态机/熔断/配额），可通过 `keys` CLI 增删查改。

## 一、LLM Provider（核心 `llm_router.py`，用于 LLM 评分/摘要）

| Provider | 环境变量 | 优先级 | 用途 | 效益 | 获取 |
| --- | --- | --- | --- | --- | --- |
| Ollama（本地） | `OLLAMA_HOST` | 1 | 本地模型（零成本、数据不出域） | 无 API 费用、隐私最佳 | 本地安装 Ollama 后默认 `http://localhost:11434` |
| DeepSeek | `DEEPSEEK_API_KEY` | 2 | 中文推理/评分 | 中文质量高、价格低（约 OpenAI 1/10） | https://platform.deepseek.com |
| 智谱 GLM | `ZHIPU_API_KEY` | 2 | 中文推理/评分（复用搜索 Key） | 国内直连、中文友好 | https://open.bigmodel.cn |
| Kimi | `KIMI_API_KEY`（别名 `MOONSHOT_API_KEY`） | 3 | 长上下文推理 | 128K 长上下文、中文好 | https://platform.moonshot.cn |
| OpenAI | `OPENAI_API_KEY` | 3 | 通用推理 | 生态最全、多模型可选 | https://platform.openai.com |
| Anthropic | `ANTHROPIC_API_KEY` | 4 | Claude 推理 | 长文/复杂推理强 | https://console.anthropic.com |

**效益合计**：自动 fallback（主 provider 熔断后无缝切换）+ 成本控制（按优先级选最廉价可用）+ 配额感知；仅配 1 个即可启用 LLM 能力，全配最多 6 路冗余。

## 二、搜索 / AI 检索引擎（`infoseek_pipeline.py` / `search_engine_health.py`）

| Provider | 环境变量 | 用途 | 效益 | 获取 |
| --- | --- | --- | --- | --- |
| Exa | `EXA_API_KEY` | AI 语义搜索（默认层/AI 层主力） | 语义召回精准，适合技术/竞品调研 | https://exa.ai |
| Tavily | `TAVILY_API_KEY` | AI 搜索（AI 层 + 舆情兜底） | 为 LLM 优化的搜索 API，结果结构化 | https://tavily.com |
| 智谱搜索 | `ZHIPU_API_KEY` | 搜索（与 LLM 共用 Key） | 国内源覆盖 | https://open.bigmodel.cn |
| 秘塔 | `METASO_API_KEY` | AI 搜索（金融/国内长尾） | 中文金融内容覆盖 | https://metaso.cn |
| TinyFish | `TINYFISH_API_KEY` | AI 搜索兜底 | 补充长尾源 | https://tinyfish.io |
| QVeris | `QVERIS_API_KEY` | 能力路由网络（结构化金融/数据能力：量化/宏观固收/风控/加密/另类信号） | discover/inspect 免费，按调用计 credits（每结果 1 credits 起）；CN key（`sk-cn-`）自动走 `qveris.cn` 合规区 | https://qveris.com（Dashboard/API Keys） |

**效益合计**：免费层（DDG/Bing/Wikipedia/Jina）零 Key 可用；配置任一 AI 引擎 Key 后启用「AI 模式」层（`INFOSEEK_SEARCH_ENGINE=ai`），语义召回质量显著提升；多 Key 自动轮换 + 配额保护（限量引擎仅作兜底保留池，避免烧额度）。QVeris 作为**结构化数据兜底**（金融/宏观/风控等查询在网页召回不足时提供结构化执行），计费受 `INFOSEEK_QVERIS_CALL_BUDGET` 保护。

## 三、摘要 / 其它

| 用途 | 环境变量 | 说明 |
| --- | --- | --- |
| 摘要 LLM | `INFOSEEK_LLM_API_KEY` / `INFOSEEK_LLM_API_BASE` / `INFOSEEK_LLM_MODEL` | `summarize_content` 首选 LLM 摘要时的专用配置（缺省回落到 `llm_router` 全局路由） |
| MCP 远程鉴权 | `INFOSEEK_AUTH_TOKEN` | SSE 远程托管模式的 Bearer 鉴权（非第三方，见 PRIVACY.md） |

## 四、安全与合规

- **零明文落盘**：Key 经 `KeyManager` 加密存储（`.infoseek/keys.json`）或系统 keyring；`keys list` 输出全部脱敏
- **泄漏扫描**：`scripts/leak_scan.py` 可扫描代码库/目录中的密钥赋值模式（sk-/AWS/GitHub/JWT 等），发布前建议运行
- **L3 凭证抓取**：按 URL host 匹配注入，仅内存使用，不打日志（详见 `external-deps.md`）
- **不适用**：本清单不含任何免费额度承诺；各服务条款/配额以官方为准
