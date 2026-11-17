# Gotchas / 反模式清单 — NodeCoda Workflow Language

> 全部来自**真实 Build 诊断**实证(2026-08-12)。每条:现象 → 原因 → 正确写法。这些是文档里不明显、但编译器强制执行的硬约束。遇到类似报错先查这里。

## G1. `@conversation` 声明顺序 — SYNTAX_ERROR
- **现象**:`Expected declaration, got AT_CONVERSATION ('@conversation')`
- **原因**:解析器把 `@conversation` 当顶层声明,要求它位于 `const`/`type`/`function` 之前。放在 `const MODEL` 之后即报错。
- **正确写法**:`@conversation` 全部紧跟在 `@mode` 之后,`const` 之前。
  ```nodecoda
  @mode advanced-chat
  @conversation string content = "";
  const MODEL = "...";
  ```

## G2. 文件变量没有 `.text` 字段 — FIELD_NOT_FOUND
- **现象**:`Field 'text' not found on file type. Available fields: name, filename, extension, mime_type, size, type, transfer_method, url, remote_url, related_id`
- **原因**:`file<>` 变量只暴露元数据字段,不直接提供文本内容。
- **正确写法**:用 `extract_text(doc)` 内置函数提取,再取 `.text`:
  ```nodecoda
  let extracted = extract_text(doc);
  return extracted.text;
  ```

## G3. `extract_text` 要求声明可提取扩展名 — TARGET_NOT_LOWERABLE
- **现象**:`extract_text requires a selector-backed scalar file with a declared extractable extension`
- **原因**:只有文件类型声明了可提取扩展名,才能下降为 document-extractor 节点。
- **正确写法**:`file<document; .pdf>`(可多扩展名 `file<document; .pdf, .md, .txt>`)。
  ```nodecoda
  function main(file<document; .pdf> doc) -> string { ... }
  ```

## G4. 会话变量赋值只支持标量字面量 — TARGET_NOT_LOWERABLE
- **现象**:`conversation variable set operation only supports scalar literal values`
- **原因**:`@conversation` 变量在运行期只能写标量字面量,不能存动态计算值。
- **正确写法**:只存字面量标记(`first_done = true`);动态数据(如提取的文本)靠 LLM 对话记忆或 Dify 端处理,别塞会话变量。
  ```nodecoda
  @conversation bool first_done = false;
  // first_done = true;            // OK
  // content = extracted.text;     // 非法
  ```

## G5. `@conversation` 默认值仅限字面量
- **现象**:默认值若不是字面量会报错。
- **原因**:target 要求会话变量默认值是常量。
- **正确写法**:默认值写死:`@conversation string content = "";`(不能 `= someExpr`)。

## G6. 文件直传 LLM 不被接受 — TYPE_MISMATCH
- **现象**:`Map value has incompatible type Type(file); expected Type(string)`
- **原因**:LLM 的 `content` 字段要 string;把整个 `file` 变量当 user 消息传进去不行。
- **正确写法**:先 `extract_text` 变成 string,再喂给 LLM。

## G7. 构建入口 / 工具 base 路径
- **现象**:`/api/v1/workflow-builds` 返回 `401 INVALID_TOKEN`;`save-build.mjs` 配 `.../v1` 会拼出 `/v1/v1/...` 404。
- **原因**:两套 base——admin `/api/v1`(登录/key)与 MCP gateway `/v1`(build/poll/cancel);`sk-` key 走 `/v1`。`save-build.mjs` 内部已含 `/v1`,base 传宿主根。
- **正确写法**:构建 `POST https://www.nodecoda.com/v1/workflow-builds`;`NODECODA_API_BASE=https://www.nodecoda.com`。

## G8. 变量名避开保留字
- **现象**:用 `code`/`source`/`answer`/`limit` 等当变量名会撞保留字。
- **原因**:§7 保留字表(见 `grammar-reference.md`)。
- **正确写法**:换名,如 `result`/`content`。(保留字全表见 grammar-reference §7)

## G9. 操作策略支持矩阵（白名单实证）
- **白名单来源**:主仓 `lang/src/nclang/lang/operation_registry.py`（`OperationPolicySupport`）+
  真实 Build 实证。违反白名单报 `OPERATION_POLICY`。

| 操作 | retry | timeout | default | failure_branch(attempt) |
|------|:---:|:---:|:---:|:---:|
| `llm` | ✓ | ✗ | ✓ | ✓ |
| `http` | ✓ | ✓ | ✓ | ✓ |
| `tool` | ✓ | ✗ | ✗ | ✓ |
| `knowledge` / `extract_text` / `classify` | ✗ | ✗ | ✗ | ✗ |
| `extract<T>` | ✗（E1045） | ✗ | ✗ | ✓ |

- **实证现象**:`Operation 'llm' does not support timeout`（OPERATION_POLICY，2026-08-13 e2e）。
- **正确写法**:
  - llm 要兜底:`with default(...)` 合法;要超时:别写 `timeout`,用 `attempt` 包装或 Dify 端配置。
  - http 超时:`with timeout(30s)` 合法(主仓单测 `test_http_timeout_and_default_policies_serialize`)。
  - `attempt` + `default` 冲突:`attempt ... with default(...) as x` 会被拒
    （`default policy cannot be combined with an explicit failure branch`）。
  - `retry(max: N)` 必须 N ≥ 1,且同调用不能重复 `retry`。

## G10. `if` 条件可降级形态受限 — LOWERING_INVARIANT
- **现象**:
  - `Condition expression BinaryExpr is not directly lowerable` — 比较左侧是 2 级字段
    （如 `extracted.value.days > 5`）；
  - `Validated expression has no physical producer selector` — 三元结果变量在 if
    分支的模板串里插值。
- **原因**:IF/ELSE 降级只接受:裸 bool 字段（任意深度）、`!expr`、`x.contains("字面量")`、
  以及**左侧为 1 级字段/标识符**的比较（`==`/`!=`/`<`/`>`/`<=`/`>=`，右侧为字面量）；
  `&&` 可拆分组合（每侧须各自可降级）。2 级字段比较、推迟三元（`let x = a ? b : c`）
  在分支模板插值走不通。
- **正确写法**:
  ```nodecoda
  let trip_days = extracted.value.days;   // 2 级字段先绑定为 1 级局部变量
  if (trip_days > 5) { ... }
  if (extracted.value.flexible) { ... }   // 裸 bool 字段任意深度可用
  ```
  三元结果变量只在非分支上下文使用（直接 `return` 或非分支模板串可以；放进 if
  分支体内的模板串不行）。

## G11. 会话变量不能放进模板串插值 — LOWERING_INVARIANT
- **现象**:`Validated calculation identifier 'greeting' has no value`（模板串 `${greeting}` 处）
- **原因**:`@conversation` 变量没有物理 producer 可供模板引用解析。
- **正确写法**:
  ```nodecoda
  answer(greeting);                    // 直接作参数 ✓
  if (visit_count > 3) { ... }         // 条件判断 ✓
  // answer(`欢迎,${greeting}`);       // ✗ LOWERING_INVARIANT
  ```
  非会话变量（main 参数、局部变量）可插值：`answer(\`你说:${user_input}\`)` ✓。

## G12. `parallel for` 的 `on_error` 只接受三种模式 — SYNTAX_ERROR
- **现象**:`Expected parallel-for error mode, got KW_CONTINUE ('continue')`
- **原因**:parser 对 on_error 白名单 `{terminate, keep_null, remove_failed}`。
- **正确写法**:
  ```nodecoda
  let r = parallel for (x in xs, concurrency: 3, on_error: remove_failed) { ... };
  ```
  - `terminate` — 遇错终止；`keep_null` — 失败项保留为 null；`remove_failed` — 失败项剔除。

## G13. `else if` 链合法（勿按 EBNF 误判）
- **现象**：想写 `if ... else if ... else`，查 `grammar.ebnf` 只见 `if_stmt = "if" "(" expression ")" block else_clause_opt`，怀疑不支持链式。
- **原因**：EBNF 是简化写法，`else_clause_opt` 实际可承接嵌套 `if`。
- **正确写法**：`else if (cond) { ... } else { ... }` 直接可用（实证：`ticket-triage` 用 `else if` 构建通过，0 诊断）。

## G14. REST 直连缺 `Idempotency-Key` header — 400 WORKFLOW_BUILD_REQUEST_INVALID
- **现象**：按 mcp-contract.md 的 body 示例直连 `POST /v1/workflow-builds`，返回 `400` / `WORKFLOW_BUILD_REQUEST_INVALID`；以为是 idempotency_key 含非法字符，换纯字母数字 key 仍 400。
- **原因**：公网网关要求幂等 key **双份**——body `idempotency_key` + `Idempotency-Key` 请求头；MCP server 自动转发，REST 直连不会。
- **正确写法**：curl 加 `-H "Idempotency-Key: <key>"`，与 body 同值。

## 排查顺序
1. 按 error code 定位到上面某条(不全时配 `diagnostics-map.md`)。
2. 若文档与现象不符 → **先跑最小复现探针**(一个最小文件单向验证),隔离【声明顺序】vs【构造不支持】,别猜。