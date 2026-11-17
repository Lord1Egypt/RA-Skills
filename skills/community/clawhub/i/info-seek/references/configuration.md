# Infoseek 配置项参考（Configuration Reference）

> 版本：v1.2.0 ｜ 状态：✅ 已提供 ｜ 全量 env 配置清单

---

## 1. 路径与运行时

| 变量 | 默认 | 用途 |
|------|------|------|
| `INFOSEEK_ROOT` | skill 根目录 | 覆盖运行时根路径（脚本定位） |
| `INFOSEEK_DATA_DIR` | `~/.infoseek` | 运行时数据目录（claims/aliases/key_usage 等） |
| `INFOSEEK_DB` | `$DATA_DIR/infoseek_db.json` | 归档去重数据库路径 |
| `INFOSEEK_ARCHIVE` | `~/infoseek-archives` | 归档内容根目录 |
| `OPENCLAW_WORKSPACE` | 家目录 | 工作区路径（部分脚本的 WORKSPACE 基址） |

## 2. 搜索链

| 变量 | 默认 | 用途 |
|------|------|------|
| `INFOSEEK_SEARCH_ENGINE` | `auto` | `auto`（免费引擎）或 `ai`（启用 AI 键控引擎层） |
| `INFOSEEK_SEARCH_PARALLEL` | `1` | `0`=顺序降级；`1`=并行合并 |
| `INFOSEEK_SEARCH_MIN_RESULTS` | min(max_results,3) | 质量门控阈值（不足触发保留池兜底） |
| `INFOSEEK_SEARCH_RESERVED` | 动态 | 固定保留引擎（逗号分隔，如 `Wikipedia`） |
| `INFOSEEK_RESERVE_QUOTA` | `1` | `0`=关闭配额保护（全池轮换） |
| `INFOSEEK_CN_AI_SEARCH` | 未设置 | `1`=启用国内 AI 网页搜索兜底（360AI/Kimi/天工） |
| `INFOSEEK_RECALL_EXPAND` | `1` | 召回增强：query 别名扩展（识别 query 中已知实体并追加别名 ≤3 个，提升跨名召回；v1.2.x） |
| `INFOSEEK_RECALL_DIVERSITY` | `1` | 召回增强：跨引擎多样性合并（轮询逐引擎取结果，防单源垄断 top-N；v1.2.x） |
| `INFOSEEK_RECALL_ADAPTIVE` | `1` | 召回增强：相关性门槛自适应（候选 <6→门槛10 保召回；>20→门槛14 滤噪；v1.2.x） |
| `INFOSEEK_RECALL_DYN_WEIGHT` | `0` | 召回增强：动态层权重（按 query 类型 finance/tech/sentiment 调整引擎权重；opt-in，v1.2.x） |
| `INFOSEEK_ENGINE_WHITELIST` | 空 | 引擎白名单路由（策略②，2026-09-10）：逗号分隔引擎名，运行时优先于 engine-routes.json；空则用配置文件 whitelist 兜底；六键控引擎无 key 自动剔除 |
| `INFOSEEK_ENGINE_PROBE` | `0` | `1`=开启可用性探测：白名单引擎经 probe_http 实测，不可达引擎被剔除后再进入搜索池 |
| `INFOSEEK_PROBE_TIMEOUT` | `5` | 探测超时秒数（engine_router.probe_http） |
| `INFOSEEK_PROBE_TTL` | `600` | 探测结果缓存 TTL 秒数（`~/.infoseek/engine_routes.json`） |

### 抓取层级 extraction_level（v1.2.x L3/L4）

`tool_fetch_content` 支持 `extraction_level` 参数（1/2/3/4，钳制到合法范围；缺省 1）：
- **L1（静态 fetch）**：urllib 拉取 + 正文提取（默认）
- **L2（浏览器渲染）**：L1 不足 100 字时 playwright 无头渲染（可选依赖，缺失/失败静默降级 L1）
- **L3（凭证辅助）**：`extraction_level>=3` 且 L1 不足时，按 URL host 从 KeyManager 取凭证注入 playwright（`Authorization: Bearer <key>` 或 `Cookie:` 前缀）；**凭证仅内存使用，不落盘/不打日志**；无凭证/失败自动降级 L1/L2
- **L4（多媒体）**：`extraction_level>=4` 时识别 image/video/audio URL（Content-Type 优先、扩展名回退），返回统一 `media` chunk（`media_type`/`metadata`/`transcript`）；whisper 转录为可选能力，缺失时 `transcript_available=False` 降级不崩

## 3. LLM 路由

| 变量 | 用途 |
|------|------|
| `OLLAMA_HOST` | Ollama 本地服务地址（默认 `http://localhost:11434`） |
| `ZHIPU_API_KEY` | 智谱 GLM key |
| `OPENAI_API_KEY` | OpenAI key |
| `ANTHROPIC_API_KEY` | Anthropic key |
| `DEEPSEEK_API_KEY` | DeepSeek key（OpenAI 兼容端点） |
| `KIMI_API_KEY` / `MOONSHOT_API_KEY` | Kimi key（MOONSHOT 为别名） |

## 4. Key 管理（KeyManager，v1.0.1）

| 变量 | 默认 | 用途 |
|------|------|------|
| `INFOSEEK_DOTENV` | `.env` | .env 文件路径（KeyManager 启动加载，不覆盖已有 env） |
| `INFOSEEK_KEY_FAIL_THRESHOLD` | `3` | 连续失败 N 次 → DEGRADED |
| `INFOSEEK_KEY_CIRCUIT_THRESHOLD` | `5` | 连续失败 M 次 → CIRCUIT_OPEN（熔断） |
| `INFOSEEK_KEY_CIRCUIT_COOLDOWN` | `60` | 熔断冷却秒数（秒，浮点） |
| `INFOSEEK_KEY_AUTO_PERSIST` | `0` | 每 N 次 key get 自动落盘用量（0=关闭，v1.0.1） |
| keyring service | `infoseek` | 系统 keyring 服务名（`keys keyring-persist/load` 使用，B1） |

### 搜索引擎生命周期（v1.0.1 评估升级 P0/P1/P2 + P3 新鲜度）

| 变量 | 默认 | 用途 |
| --- | --- | --- |
| `INFOSEEK_ENGINE_FAIL_THRESHOLD` | `3` | 引擎连续失败 N 次 → 临时禁用（降权） |
| `INFOSEEK_ENGINE_DISABLE_SECONDS` | `600` | 临时禁用时长（秒）；超时后自动恢复尝试 |
| `INFOSEEK_ENGINE_AUTH_STICKY` | `1` | `401/403` 认证损坏是否持续禁用直到手动 `engine-reset`（1=是） |
| `INFOSEEK_ENGINE_QUOTA_RESET` | `monthly` | 配额重置模式：`monthly`(下月1日UTC) / `daily`(次日0点本地) / `hourly`(整点) / `fixed:<ISO>`（P3.1） |
| `INFOSEEK_ENGINE_AUTH_RECOVER_SECONDS` | `0` | 认证自动恢复冷却（秒）；`0`=禁用（保持 sticky，需手动 reset），`>0`=冷却期满后自动恢复（P3.2） |
| `INFOSEEK_ENGINE_API_DRIFT` | `0` | API 漂移检测开关（1=启用）；启用后响应签名连续 N 次不一致置 `api_changed` 告警（不影响禁用判定，P3.3） |
| `INFOSEEK_ENGINE_API_DRIFT_N` | `3` | 触发 `api_changed` 所需的连续不一致次数（P3.3） |
| `INFOSEEK_ENGINE_FRESHNESS_TTL` | `86400` | 状态新鲜度 TTL（秒）；超过则视为过期，下次 `reconcile` 强制重新评估（P3.4） |

- 状态持久化：`engine_state.json`（同 `INFOSEEK_DATA_DIR`），记录 per-engine 健康/配额/认证 + 新鲜度字段
- 配额耗尽（`429`/`quota_exceeded`）→ 标记 `quota_exhausted` + 推算重置时刻（Retry-After 或按 `QUOTA_RESET` 模式），自动退出保留池与并行层；到重置时刻由 `reconcile()` 自动清零（P3.1，修复「日/时额度引擎被误禁 30 天」）
- 自愈链路：`_call_engine` 调用前经 `reconcile()` 对账；配额/认证标记到期即恢复，无需手动 `engine-reset`（P3.1/P3.2）
- API 漂移：成功响应抽取 `response_signature`，连续 N 次结构不一致置 `api_changed=True` 告警（默认关闭，避免误报 churn，P3.3）
- 管理命令：`keys engine-status`（查看健康/配额/认证/漂移）、`keys engine-reset [--engine X]`（重置）、`keys engine-reconcile [--engine X]`（一键对账恢复）、`keys engine-probe`（存活探测并报告恢复项）

## 5. 摘要 / MCP

| 变量 | 用途 |
|------|------|
| `INFOSEEK_LLM_API_KEY` | 摘要 LLM API key（`prefer=llm` 时启用） |
| `INFOSEEK_LLM_API_BASE` | 摘要 LLM 端点 base |
| `INFOSEEK_LLM_MODEL` | 摘要 LLM 模型名 |
| `INFOSEEK_AUTH_TOKEN` | MCP 远程鉴权 Bearer token |
| `INFOSEEK_HOST` / `INFOSEEK_PORT` | 远程托管 host/port（infoseek_host.py） |

## 6. 搜索引擎 API key（AI 层）

| 变量 | 引擎 |
|------|------|
| `EXA_API_KEY` | Exa 语义搜索（免费 1000 次/月） |
| `TAVILY_API_KEY` | Tavily 搜索 |
| `TINYFISH_API_KEY` | TinyFish 搜索 |
| `ZHIPU_API_KEY` | 智谱搜索（与 LLM 共用 key） |
| `METASO_API_KEY` | 秘塔搜索 |
| `QVERIS_API_KEY` | QVeris 能力路由（结构化金融/数据能力；CN key 前缀 `sk-cn-`） |

### QVeris 能力路由（v1.3，scripts/qveris_client.py）

| 变量 | 默认 | 用途 |
|------|------|------|
| `INFOSEEK_QVERIS_BASE_URL` | 自动选区 | QVeris REST Base；未设置时按 key 前缀自动选区（`sk-cn-`→`https://qveris.cn/api/v1`，其余→`https://qveris.ai/api/v1`） |
| `INFOSEEK_QVERIS_TIMEOUT` | `5` | HTTP 超时秒数 |
| `INFOSEEK_QVERIS_CALL_BUDGET` | `3` | 每次 search 最多执行的 call 次数（credits 保护；discover/inspect 免费不计数） |

协议四步（两区一致，Bearer 认证）：`POST /search`（discover，免费）→ `POST /tools/by-ids`（inspect，免费）→ `POST /tools/probe`（预验证，免费）→ `POST /tools/execute`（call，消耗 credits）。CN 区 discover 返回精简结果，客户端自动走 **Discover→Inspect→Call** 补全流程。错误分类 429→quota / 401/403→forbidden，自动进入引擎生命周期。

### 内容抓取分级（v1.0.1 C2）

- **L1 静态 fetch**（默认）：urllib 抓取 + 正文提取（`tool_fetch_content`）
- **L2 浏览器渲染**（可选增强）：playwright 无头渲染（JS/SPA/反爬页面）；
  `content < 100 字` 时自动尝试，失败静默降级 L1（返回 `extraction_level` 1/2）；
  playwright 库缺失 / 浏览器未装均自动降级（零依赖哲学）
- **L3 凭证辅助 / L4 多媒体**：v1.2.x 规划

### 搜索召回调优（v1.0.1 C1）

**引擎分层**：默认层 = 免费引擎（Bing RSS / DDG / Jina 免 key）并行 + 键控引擎保留池；
`INFOSEEK_SEARCH_ENGINE=ai` 时启用 AI 层（键控引擎高权重并行）。

**提升召回的操作顺序**：
1. **探测现状**：`python scripts/search_engine_health.py` → 看哪些引擎可达/缺 key
2. **优先配 Exa**（免费 1000 次/月，语义搜索中文召回显著优于 RSS）：
   ```bash
   export EXA_API_KEY=<your-key>
   export INFOSEEK_SEARCH_ENGINE=ai   # 启用 AI 键控层
   ```
3. **冗余配 Tavily**（RAG 调优，Exa 不可用时兜底）：`export TAVILY_API_KEY=<your-key>`
4. 复测：`python scripts/search_engine_health.py` 确认键控引擎 ✅

**已知限制**（上游引擎，非本库缺陷）：Bing RSS 对中文长查询分词质量差（如
"新能源汽车 2026 市场" 返回单字噪音）—— `search_web` 已内置 jieba 多字词
相关性过滤缓解，但召回上限受引擎本身限制；配 Exa/Tavily 可根本改善。

---

## 7. 安全建议

- **密钥注入**：优先经 MCP 客户端 env 注入（`${env:XXX_API_KEY}`），或 `keys add` + 加密落盘（Fernet）
- **明文禁令**：API key 明文永不写入日志 / 归档 / 报告（`mask_token` / `key_fingerprint` 均脱敏）
- **Windows 权限**：`chmod 0o600` 仅 POSIX 生效，Windows 依赖 NTFS ACL（保存时会有 RuntimeWarning）
- **.env 位置**：默认 CWD 下 `.env`，可用 `INFOSEEK_DOTENV` 覆盖；KeyManager 不覆盖已存在的 env 变量
