# 目标能力矩阵 — `dify-1.16-graphon-0.6`

> 当前唯一受支持的 Build Target。Source 必须以 `@language nodecoda/1` 开头并在 `build_dify_workflow` 中显式指定 `target_profile="dify-1.16-graphon-0.6"`。

## 完全支持(可直接使用)

| NodeCoda 构造 | 降级到 Dify 节点 | 备注 |
|---------------|------------------|------|
| `llm(model, opts)` | LLM node | temperature/max_tokens 直传 |
| `http(method, url, opts)` | HTTP Request node | body/headers 全部支持 |
| `tool("name", "action", params)` | Tool node | 工具需先在 Dify 配置 |
| `knowledge("ds-id", query, opts)` | Knowledge Retrieval node | 多 ds 用逗号分隔 |
| `extract<T>(model, text, opts)` | Parameter Extractor node | 仅支持 prompt strategy |
| `foreign code python3(...)` | Code node (Python) | 声明类型是唯一权威 |
| `std.v1.rag_answer(...)` | RAG 复合节点 | dataset-id 和 model 必须是字面量 |
| `std.v1.fetch_and_summarize(...)` | HTTP + LLM 复合节点 | 同上 |
| `if/else` | IF/ELSE node | 每个分支独立节点 |
| `parallel { ... }` | Parallel 分支 | 命名 / 无名都支持 |
| `for (item in items) { yield x }` | Iteration node | 收集 yield 出的数组 |
| `answer(...)` | Answer node | 仅 `@mode advanced-chat` |
| `@conversation T` | Variable Assigner 链 | 多个 assigner 串联 |
| `output("key", value)` | 多端点输出 | 配合 `return final` |
| `attempt { success/failure }` | 错误处理分支 | 包装任意单操作 |
| `with retry(max:, interval:)` | 节点级重试配置 | 仅 `llm` / `http` |

## 部分支持(写法受限)

| 构造 | 限制 |
|------|------|
| `main` 参数类型 | 只能是 `string` / `int` / `float` / `bool` / `file<>`;**不接受 `string[]` 或 `map<string,T>` 作为入口参数** |
| `extract<T>` 字段类型 | 只能是 `string` / `float` / `bool` / `string[]` / `float[]` / `bool[]` |
| `foreign code` 输入输出 | 不支持 `file` 类型 |
| `@conversation` 默认值 | 只能是字面量 |
| `std.v1.*` 参数 | 全部必须是字符串字面量,不能传变量 |
| `retry` | `extract<T>` 不支持,用就报 E1045 |
| `filter` / `take` / `split` | 可用,但目标 lowering 后是显式循环节点,Source 大数组慎用 |

## 不支持(改设计,不要试图绕过)

| 构造 | 替代方案 |
|------|----------|
| 自定义 Dify 节点类型 | 用 `tool(...)` 包装,或在 Dify 端配置 |
| 跨 Dify 应用的调用 | 改用 HTTP + Service API |
| 任意 LLM provider 切换 | 必须在 Dify 端先配置 Model Provider,Source 只用模型 id |
| 在 Source 里塞 Dify 私有变量 | 通过 `extract<T>` 输出后再在 Dify 端处理 |
| 文件输入输出到非 Dify 存储 | 用 `http` 走对象存储 API |

## 能力门诊断

构造不在上表"完全支持"里时,L2 `capability_gate` 会报 `CAPABILITY_BLOCKED` 或 `TARGET_FEATURE_UNSUPPORTED`,**Build 失败**。

**正确反应**:收到这种诊断**改设计,不改 Source**。具体步骤:
1. 读 `diagnostics.md` 确认 code
2. 在本表"部分支持"找替代写法
3. 找不到就在"不支持"列找替代设计(改架构、调用外部服务)
4. 仍不行 → 报告需求,问是否要拓展 target capability(需走主仓库 RFC)

**禁止**:收到 `CAPABILITY_BLOCKED` 后用更低级构造硬堆出来(例如用 `tool` 包 `http` 包 `llm` 套娃)。这违反"能力门不降级"原则,产物后续维护性极差。
