# 诊断解读

`nclang-compile` 跑完 L1→L2→L3→L4 整条流水线,**每到达的 stage 都贡献诊断**,所以一次 Build 可能同时报"语法错 + 类型错 + 能力门被拦"。诊断是结构化的,可机器读。

## Diagnostic 形状

```json
{
  "code": "TYPE_MISMATCH",
  "severity": "error",
  "message": "expected string, got int",
  "location": {
    "file": "demo.ncoda",
    "line": 12,
    "column": 9,
    "node_id": "expr:12:9",
    "path": "main.body[0].let.rhs"
  }
}
```

| 字段 | 含义 |
|------|------|
| `code` | 稳定枚举,跨版本不破坏(见下文分类) |
| `severity` | `error` / `warning` / `info` / `hint` |
| `message` | 人类可读,英文为主,可能含中文片段 |
| `location.line` / `column` | Source 中的行列(1-indexed) |
| `location.node_id` | AST 节点稳定 id,跨编辑保持引用 |
| `location.path` | 嵌套路径,可直接定位到 Symbol |
| `file` | 永远是 `source_filename` 的值 |

**最多 100 条诊断**,按 severity 排序,error 在前。

## Code 分类(按 pasS 来源)

| 类别 | 典型 code | 触发阶段 | 修复方向 |
|------|-----------|----------|----------|
| **语法** | `SYNTAX_UNEXPECTED_TOKEN`、`SYNTAX_UNTERMINATED_STRING` | L1 lexer/parser | 改 Source 语法,看 `language-reference.md` |
| **作用域** | `UNDEFINED_SYMBOL`、`SHADOWED_BINDING`、`DUPLICATE_DECL` | L2 scope pass | 检查名字拼写,确认 import/声明顺序 |
| **类型** | `TYPE_MISMATCH`、`INCOMPATIBLE_TYPES`、`MISSING_RETURN` | L2 type pass | 对齐声明类型,补全分支返回值 |
| **效应/初始化** | `UNINITIALIZED_READ`、`NONEXHAUSTIVE_PATTERNS` | L2 effect pass / definite_init | 显式初始化,补全 match 分支 |
| **能力门** | `CAPABILITY_BLOCKED`、`TARGET_FEATURE_UNSUPPORTED` | L2 capability gate | **不改 Source**,改设计或换目标 |
| **响应契约** | `RESPONSE_CONTRACT_VIOLATION`、`YIELD_OUTSIDE_LOOP` | L2 response_contract / yield_contract | 调整 return/output/answer 写法 |
| **目标验证** | `TARGET_INCOMPATIBLE` | L4 target validation | **不改 Source**,降级设计或换目标 |
| **代码生成** | `CODEGEN_ERROR`、`ARTIFACT_INVALID` | L4 lowering/serializer | 视为服务 bug,留 Build ID 报告 |

> 完整 code 枚举见 `lang/src/nclang/lang/passes/base.py` 的 `DSLDiagnosticCode`(每次 release 自动同步)。

## Severity 行为

- `error`:**Build 必失败**,无论在哪一阶段
- `warning`:Build 仍可 SUCCEEDED,但应修复
- `info` / `hint`:风格建议,可忽略

**warning 不阻断**,但同一 warning 重复 3 次以上应视为设计气味。

## 修复优先级

1. **首个 error** —— error 会阻断后续阶段,先修这一条
2. **同一 location 的 error 簇** —— 通常是同一个根因
3. **跨文件同 code 的 error** —— 看是否共用类型/能力
4. **warning 簇** —— error 修完再看

**不要按行号顺序盲改**。诊断是按 pass 输出顺序排的,但根因可能在更早的 location。

## 错误解读纪律

- **不读 Dify YAML 反推** —— YAML 是产物,不是 source
- **不修不在诊断里的问题** —— 修诊断没指出的代码属于"猜测性修改",违反"连续两次没严格减少错误就停"的规则
- **同一诊断重出现 = 停** —— Build ID 重复 + 同一 diagnostic code + 同一 location = 没进展,放弃这次 build
- **诊断最大量是 100 条** —— 超过 100 通常意味着根本性设计错误,先重新看需求
