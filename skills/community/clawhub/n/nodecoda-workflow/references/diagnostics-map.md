# 诊断 → 修复映射表(实证)

> `diagnostics.md` 给理论 code 分类,`iteration-loop.md` 给修复模式。本文列出**真实 Build 返回过的 code + 原文 + 具体改法**。与某条不符时以最新 Build 为准,并回写本文。

## 已实证的 diagnostic code

| code | 原文(节选) | 原因 | 修复动作 |
|------|------------|------|----------|
| `SYNTAX_ERROR` | `Expected declaration, got AT_CONVERSATION ('@conversation')` | `@conversation` 在 `const`/`type`/`function` 之后 | 把 `@conversation` 移到 `@mode` 之后、`const` 之前(见 G1) |
| `TYPE_MISMATCH` | `Map value has incompatible type Type(file); expected Type(string)` | 把整个 `file` 变量当 LLM user 消息 `content` | 先 `extract_text`,喂提取后的 string(见 G6) |
| `FIELD_NOT_FOUND` | `Field 'text' not found on file type. Available fields: name, filename, ...` | 访问了文件不存在的字段 | 用 `extract_text(doc).text`,别用 `doc.text`(见 G2) |
| `TARGET_NOT_LOWERABLE` | `extract_text requires a selector-backed scalar file with a declared extractable extension` | `file<>` 没声明可提取扩展名 | 类型写 `file<document; .pdf>`(见 G3) |
| `TARGET_NOT_LOWERABLE` | `conversation variable set operation only supports scalar literal values` | 给会话变量赋了动态值 | 只赋标量字面量,动态数据靠 LLM 记忆(见 G4) |
| `OPERATION_POLICY` | `Operation 'llm' does not support timeout` | 策略白名单:llm 无 timeout(http 有) | llm 用 `with default(...)` 或 `attempt`;http 可 `with timeout(30s)`(见 G9) |
| `LOWERING_INVARIANT` | `Condition expression BinaryExpr is not directly lowerable` | 比较左侧为 2 级字段(如 a.b.c) | 左侧绑 1 级局部变量再比较(见 G10) |
| `LOWERING_INVARIANT` | `Validated expression has no physical producer selector` | 三元结果变量在 if 分支模板串插值 | 三元只在非分支上下文,分支内不插值(见 G10) |
| `LOWERING_INVARIANT` | `Validated calculation identifier 'greeting' has no value` | 会话变量模板串插值 | 直接作 answer 参数/条件判断(见 G11) |
| `SYNTAX_ERROR` | `Expected parallel-for error mode, got KW_CONTINUE ('continue')` | on_error 用了非白名单词 | 用 terminate/keep_null/remove_failed(见 G12) |

## 尚未在本 repo 实证、但理论存在的 code

> 见 `diagnostics.md` §Code 分类 与 `iteration-loop.md` §修复模式。常见:
> `SYNTAX_UNEXPECTED_TOKEN` / `UNDEFINED_SYMBOL` / `SHADOWED_BINDING` / `INCOMPATIBLE_TYPES` / `MISSING_RETURN` / `UNINITIALIZED_READ` / `CAPABILITY_BLOCKED` / `TARGET_FEATURE_UNSUPPORTED` / `RESPONSE_CONTRACT_VIOLATION` / `YIELD_OUTSIDE_LOOP` / `TARGET_INCOMPATIBLE` / `CODEGEN_ERROR` / `ARTIFACT_INVALID`。

## 修复护栏(与 iteration-loop 一致)

- 只修诊断指向的 location;不顺手改别的代码。
- 每次 Source 变化换新幂等 key。
- error 数必须严格下降;新 error = 回归,回退上一版。
- `CAPABILITY_BLOCKED` / `TARGET_INCOMPATIBLE` / `POLICY` / `TIMEOUT` / `SERVICE` → **不改 Source**。
- 文档与现象不符 → 先跑最小复现探针,别猜。