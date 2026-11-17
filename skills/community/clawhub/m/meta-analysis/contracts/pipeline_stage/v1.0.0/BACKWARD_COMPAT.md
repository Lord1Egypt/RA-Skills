# Meta-Analysis 契约向后兼容性分析
## 原 coze 出入参 vs 升级后出入参（老技能 → 新 coze 端）

> 配套：`SPEC.md` / `request.schema.json` / `response.schema.json` / `example_roundtrip.json` / `test_contract.py`
> 本文回答一个问题：**未升级的老版本本地技能（`coze_client.run_meta`）调用「升级后的 coze 端」，是否仍能正常工作？**

---

## 0. 结论先行

**向后兼容可以成立，但有 1 条 Critical 前提（R1）必须被 coze 端实现，否则老技能直接解析失败。**

- 入参侧：老字段全部保留为 optional，老请求天然通过（已用 schema + 测试证明）。
- 出参侧：计算层字段语义不变，老解析路径有效——**前提是 coze 端对「无管线字段的旧请求」仍按旧逻辑填充 `outer.result`**。
- 已修复一个真实缺陷：新 `request.schema.json` 的 `query_origin` 正则原本写成带方括号的 `[debug:]`，与老客户端实际生成的 `debug:sha256:...`（无方括号）不符，会在未来新 adapter 做 schema 校验时误拒老请求；已改为 `^(?:debug:)?sha256:[0-9a-f]{64}$`。

---

## 1. 老版本技能的行为基线（事实，来源 `adapters/coze_client.py::run_meta`）

### 1.1 它【发送】什么（Request）
| 字段 | 是否发送 | 说明 |
|---|---|---|
| `task` / `data` / `params` / `figure` | ✅ 必带 | `figure` 被强制 `format="svg"` |
| `query_origin` | ✅ 必带 | 自动生成 `sha256:<64hex>`（`_default_query_origin`）；裸 POST 由 `_assert_query_origin` 硬校验 |
| `request_id` | ✅ 必带 | 每次调用 UUID |
| `_debug` | 条件 | 仅 `debug=True` 时 |
| `probe` | 否 | 仅 `health()` 用，不经 `run_meta` |
| `contract_version` / `schema` / `pipeline_id` / `pipeline` / `stage` / `stage_context` / `next_human_action` / `tool_cards` | ❌ 不发送 | 老技能无这些字段 |

端点：`POST /run`，`body = json.dumps(payload)`。

### 1.2 它【消费】什么（Response）
```
outer        = json.loads(raw)            # /run 返回 GlobalState
result_str   = outer.get("result")        # ← 关键依赖：R 引擎 JSON 字符串
if not result_str: parsed = outer         # fallback：要求 outer 自身含 status/stats/figures
else:             parsed = json.loads(result_str)   # ← 真正的分析结果
# 之后 _fetch_full_json / _fill_external_svgs / _assess_contract 处理 S3 外置与字段别名自适应
# 从 outer 透传 feishu_write_success / feishu_write_time
```
**关键事实**：老 adapter 完全依赖 `outer.get("result")` 这个**外层字符串字段**拿分析结果。一旦 coze 端对旧请求不再填充 `result`，老技能即走 fallback 分支，而 fallback 要求 `outer` 自身含 `status/stats/figures`——若新响应只有 `stage_result` 而无这些字段，渲染层会拿到空/缺字段。

---

## 2. 原 coze 出入参（`coze_contract.md` §2/§4 + `state.py`）

**Request（`GraphInput` / `GlobalState`）**：`task` / `data` / `params` / `figure` / `query_origin` / `probe`，全部 pydantic `extra='ignore'`。

**Response（`GraphOutput`）**：`result`（R 引擎 JSON 字符串）。`/run` 返回的 `GlobalState` 顶层还含 `feishu_write_success` / `feishu_write_time`。
内层（`json.loads(result)`）字段：`status` / `task` / `stats` / `figures` / `warnings` / `notes` / `repro` / `_coze_full` / `_coze_truncated` 等。

---

## 3. 升级后 coze 出入参（`SPEC.md` v1.0.0 + `coze_contract.md` §9）

**Request 增量（全 optional）**：`contract_version` / `schema` / `pipeline_id` / `pipeline` / `stage` / `stage_context`。

**Response 增量（全 optional，与 `result` 并列）**：`stage_result` / `next_human_action` / `tool_cards` / `contract_version` / `schema` / `pipeline_id` / `stage`。

---

## 4. 字段级差异对照表

### 4.1 Request
| 字段 | 原契约 | 升级后 | 老技能影响 |
|---|---|---|---|
| `task` / `data` / `params` / `figure` | ✅ | ✅ 保留 | 无 |
| `query_origin` | ✅ 必带 | ✅ 必带，pattern 已对齐老客户端 `^(?:debug:)?sha256:[0-9a-f]{64}$` | 无 |
| `request_id` | ✅ | ✅ 保留 | 无 |
| `_debug` | ⚠️ 条件 | ⚠️ 保留 | 无 |
| `probe` | ✅（health） | ✅ 保留 | 无 |
| `contract_version` / `schema` / `pipeline_id` / `pipeline` / `stage` / `stage_context` | — | 新增（optional） | 老技能不发送；coze `extra='ignore'` 忽略 |

### 4.2 Response
| 字段 | 原契约 | 升级后 | 老技能影响 |
|---|---|---|---|
| `result`（外层 R 引擎 JSON 串） | ✅ | ✅ **必须仍填充**（见 R1/R2） | **关键依赖** |
| `status` / `stats` / `figures` / `warnings` / `notes` / `repro`（内层） | ✅ | ✅ 语义不变 | 无（R3 禁止改名） |
| `feishu_write_success` / `feishu_write_time`（外层） | ✅（可空） | ✅ 保留 | 无 |
| `stage_result` / `next_human_action` / `tool_cards` / `contract_version` 等 | — | 新增（optional） | 老 adapter 忽略（不在消费路径） |

---

## 5. 兼容性结论

- **入参**：老请求是「新信封的超集去掉新增字段」，`additionalProperties` 默认 true，新字段全 optional → 老请求通过校验（已验证）。
- **出参**：只要 coze 对旧请求仍产 `result` + 内层计算字段，老解析路径 100% 有效。
- **唯一阻断点**：coze 端若把旧请求误路由进「stage 编排器」而只填 `stage_result`、不填 `result` → 老技能 fallback 拿不到 `status/stats/figures` → 渲染失败。这是 R1。

---

## 6. coze 端必须实现的保证（风险分级）

| ID | 等级 | 保证内容 | 失败后果 |
|---|---|---|---|
| **R1** | 🔴 Critical | **双模路由**：coze 检测请求是否含 `{contract_version, schema, pipeline_id, pipeline, stage}` 任一；**不含 → 判定为 legacy，100% 复用旧 R 引擎路由并填充 `outer.result`**。判定函数 `is_legacy_request()`。 | 老技能解析失败 |
| **R2** | 🟠 High | 新模式下 **Block B 计算阶段仍须填充 `result`**（与 `stage_result` 并存），使部分升级/新 adapter 都能读。 | 混版本期调用方读不到结果 |
| **R3** | 🟡 Medium | 不得重命名/移除内层 `status`/`stats`/`figures`/`warnings`/`notes`/`repro`；`_assess_contract` 别名表继续有效。 | 老 adapter 渲染缺字段 |
| **R4** | 🟢 Low | `query_origin` 严格 pattern 须与老客户端一致（已修 `^(?:debug:)?sha256:[0-9a-f]{64}$`）。 | 未来新 adapter 校验误拒老请求 |
| **R5** | ✅ OK | `extra='ignore'` 保证新字段不破坏旧节点逻辑（已满足）。 | — |

> `is_legacy_request(payload)` = `not any(k in payload for k in ("contract_version","schema","pipeline_id","pipeline","stage"))`
> 与 `test_contract.py` §6 中的实现逐字一致，作为 coze 端实现的单一参考。

---

## 7. 已落地的验证（机器可跑）

`test_contract.py` §6「legacy dual-mode guarantee (R1)」：
1. `is_legacy_request(legacy_req)` → `True`；含 `stage` 的新请求 → `False`（双模判定正确）。
2. `debug:sha256:<64hex>` 前缀的 legacy 请求通过 request schema（R4 修复验证）。
3. 模拟 coze legacy handler 返回 `outer={result: <inner JSON>}` → 老提取路径 `outer.get("result")`→`json.loads` 成功取出 `status`/`stats`/`figures`（R1 不变量）。
4. legacy 解析结果（inner）通过 response schema（R3 字段语义不变）。

运行：`C:/Tools/anaconda3/python.exe test_contract.py` → 当前 **PASS**。

---

## 8. coze 端落地清单（state.py 重部署前核对）

- [ ] **R1**：新增双模路由，legacy 请求填充 `GraphOutput.result`（旧 R 引擎路径不变）。
- [ ] **R2**：管线模式下 Block B 计算阶段 `result` 与 `stage_result` 并存。
- [ ] **R3**：内层计算字段名保持。
- [ ] **R4**：`query_origin` pattern 与老客户端一致（schema 已修）。
- [ ] 重部署后，用一份「老 `run_meta` 风格请求（无管线字段）」实测返回仍含 `result`+内层字段，再进发布轨道。
