# 文法参考 — NodeCoda Workflow Language (EBNF)

> **源真理 = `docs/dify-dsl.y`**（主仓库规范文法，Yacc 风格）。本文档是该规范的用户面向陈述。
>
> 文法权威以 `docs/dify-dsl.y` 为准；如本文与规范出现不一致，**以规范为准**。

## 1. 顶层结构

```ebnf
program           = language_decl_opt mode_decl_opt conversation_decl_list top_level_list ;
language_decl_opt = /* empty */ | "@language" IDENTIFIER semicolon_opt ;
mode_decl_opt     = /* empty */ | "@mode" IDENTIFIER semicolon_opt ;   // 语义: workflow|advanced-chat
conversation_list = /* empty */ | conversation_list conversation_decl ;
conversation_decl = "@conversation" type_ref IDENTIFIER default_opt ";" ;
default_opt       = /* empty */ | "=" expression ;                     // 仅字面量值
top_level_list    = /* empty */ | top_level_list top_level_decl semicolon_opt ;
top_level_decl    = const_decl | type_decl | enum_decl | code_function_def | function_def ;
```

⚠ **声明顺序**:`@conversation` 必须在 `@mode` 之后、普通顶层声明之前。放到 `const`/`type` 之后会被拒。

## 2. 顶层声明

```ebnf
const_decl        = "const" IDENTIFIER "=" const_value ";" ;
const_value       = STRING | TEMPLATE_STRING | INT | FLOAT | TRUE | FALSE | NULL ;   // 仅字面量
type_decl         = "type" IDENTIFIER "=" "{" field_list "}" semicolon_opt ;
field_list        = /* empty */ | field_list type_ref IDENTIFIER ";" ;
enum_decl         = "enum" IDENTIFIER "{" enum_member_list trailing_comma_opt "}" semicolon_opt ;  // 至少一个成员
function_def      = "function" IDENTIFIER param_list return_type_opt block ;
code_function_def = "code" IDENTIFIER param_list "->" type_ref block ;   // 顶层 Code 函数
param             = type_ref IDENTIFIER | type_ref IDENTIFIER "=" expression ;
return_type_opt   = /* empty */ | "->" type_ref ;
trailing_comma_opt = /* empty */ | "," ;
semicolon_opt     = /* empty */ | ";" ;
```

## 3. 类型

```ebnf
type_ref     = type_atom array_suffix_seq optional_suffix ;      // [] 先, ? 后
type_atom    = primitive_type | file_type_ref | IDENTIFIER | "array<" type_ref ">" | "map<string," type_ref ">" ;
array_suffix = /* empty */ | "[]" ;                              // 可多个
optional_suffix = /* empty */ | "?" ;
primitive_type = "string" | "int" | "float" | "bool" | "void" | "any" ;
file_type_ref  = "file" | "file" "<" file_type_list ";" file_ext_list ";" file_upload_list ">" ;
```

> `file<类型;扩展名;上传方式>` 三段分别约束允许的文件类别、扩展名、获取方式。

## 4. 语句

```ebnf
block      = "{" stmt_list "}" ;
statement  = if_stmt | for_stmt | while_stmt | return_stmt | yield_stmt | answer_stmt
           | parallel_stmt | attempt_stmt | request_input_stmt | break_stmt | continue_stmt
           | typed_var_decl | var_decl | output_stmt | expr_or_assign_stmt ;
if_stmt    = "if" "(" expression ")" block else_clause_opt ;
else_clause_opt = /* empty */ | "else" block | "else" if_stmt ;        // else-if 链
for_stmt   = "for" "(" for_var "in" expression ")" block ;
for_var    = IDENTIFIER | "var" IDENTIFIER | "let" IDENTIFIER | type_ref IDENTIFIER ;
while_stmt = "while" "(" expression ")" "limit" INT block ;            // 必须带 limit
return_stmt = "return" [expression] ";" ;
yield_stmt  = "yield" [expression] ";" ;
answer_stmt = "answer" "(" [expression] ")" ";" ;
parallel_stmt = "parallel" "{" { block } "}" ;                          // 无名并行（语句）
attempt_stmt = "attempt" expression "as" IDENTIFIER
               "{" "success" block "failure" "(" IDENTIFIER ")" block "}" ;
request_input_stmt = "request_input<" type_ref "," type_ref ">" "(" map_literal ")"
                     "as" IDENTIFIER "{" { "action" expression block } "timeout" block "}" ;
break_stmt  = "break" ";" ;
continue_stmt = "continue" ";" ;
typed_var_decl = type_ref IDENTIFIER ["=" expression] ";" ;
var_decl    = ("var"|"let") IDENTIFIER ["=" expression] ";" ;
output_stmt = "output" "(" expression "," expression ")" ";" ;
expr_or_assign_stmt = expression AssignOp expression ";" | expression ";" ;
AssignOp    = "=" | "+=" | "-=" | "*=" | "/=" | " << " ;
```

## 5. 表达式

```ebnf
expression  = ternary_expr ;
ternary     = or_expr | or_expr "?" expression ":" expression ;
or_expr     = and_expr | or_expr "||" and_expr ;
and_expr    = equality_expr | and_expr "&&" equality_expr ;
equality    = comparison_expr | equality ("=="|"!=") comparison_expr ;
comparison  = add_expr | comparison ("<"|"<="|">"|">="|"in") add_expr ;    // 含 in
add_expr    = multiply_expr | add_expr ("+"|"-") multiply_expr ;
multiply    = unary_expr | multiply ("*"|"/"|"%") unary_expr ;
unary_expr  = postfix_expr | "!" unary_expr | "-" unary_expr ;
postfix_expr = primary_expr
             | postfix_expr "<" type_ref_list ">" "(" arg_list ")"   // 调用类型实参
             | postfix_expr "." IDENTIFIER
             | postfix_expr "[" expression "]"
             | postfix_expr "(" arg_list ")"
             | postfix_expr "with" operation_policies ;
operation_policies = operation_policy { "," operation_policy } ;
operation_policy = "retry(" "max" ":" INT ["," "interval" ":" duration] ")"
                 | "timeout(" duration ")" | "default(" expression ")" ;
duration    = INT ("ms"|"s") ;                                            // 单位限 ms 或 s
primary_expr = INT | FLOAT | STRING | TEMPLATE_STRING | TRUE | FALSE | NULL | IDENTIFIER
             | "(" expression ")" | array_literal | map_literal
             | for_expr | parallel_for_expr | parallel_expr | foreign_code_expr | lambda_expr ;
map_literal = "{" [map_entry {"," map_entry}] "}" ;
map_entry   = map_key ":" expression ;
map_key     = expression | "timeout" ;
for_expr    = "for" "(" for_var "in" expression ")" yield_block ;        // 至少一个 yield
parallel_for_expr = "parallel" "for" "(" for_var "in" expression ","
                    concurrency ":" INT "," on_error ":" IDENTIFIER ")" yield_block ;  // on_error ∈ {terminate, keep_null, remove_failed}
parallel_expr = "parallel" "{" IDENTIFIER ":" block { IDENTIFIER ":" block } "}" ;  // 命名并行（表达式）
yield_block = "{" stmt_list yield_stmt stmt_list "}" ;
lambda_expr = "(" lambda_params_opt ")" "->" expression ;
foreign_code_expr = "foreign" "code" code_language "(" code_inputs_opt ")"
                    "->" code_output_contract "{" code_source "}" ;
code_language = IDENTIFIER | STRING ;                                   // 语义：python3
code_input  = code_type_ref IDENTIFIER "=" expression ;
code_output_contract = code_direct_output | code_structural_output ;     // 结构输出 ≥2 字段
code_source = "source" TEMPLATE_STRING ";" ;                            // 反引号模板串
```

## 6. 静态语义限制

> 这些是「语义」非「语法」，在文法中无法表达，但必须遵守：

- 程序恰好一个入口 `main`；用户函数调用图无环。
- `@mode` 为 `workflow` 或 `advanced-chat`。
- `let` 不可变；`var` 仅限静态证明的 target-owned 状态（production 提供 Loop 状态、advanced-chat 会话状态）。
- `output(key,value)` 仅 workflow；`answer(value)` 仅 advanced-chat。
- `attempt` / 操作策略仅作用于 manifest 声明的操作。
- 调用类型实参仅被 schema-dependent 操作接受（当前 `extract<T>`，T 为具名非空 record，校验 `.ok` 后再用 `.value`）。
- 仅显式 `parallel` / `parallel for` 引入并发。
- **合法语法仍受 target 能力分类约束**，被拒的形状在 WorkflowAST/YAML 前返回诊断。

## 7. 快速合法性核验

- [ ] 首行 `@language nodecoda/1`，次行 `@mode`
- [ ] `@conversation` 全部在顶层声明之前
- [ ] `const` 值、`@conversation` 默认值只接收字面量
- [ ] `while` 必须带 `limit`；`file<...>` 用到 `extract_text` 时声明扩展名
- [ ] 保留字避开：`entry`、`stream`、`request_input`、`action`（`main`、`enum` 非保留字）
- [ ] `foreign code` 的 source 是反引号模板串；结构输出 ≥2 字段

## 8. 源码对照

| 语法域 | 规范 | 实现 |
|---|---|---|
| 全量文法 | `docs/dify-dsl.y` | `src/nclang/lang/parser.py` |
| 语义限制 | `dify-dsl.y` 末尾注释段 | `lang/passes/*` |
| 关键字表 | `docs/dify-dsl.y` | `src/nclang/lang/tokens.py` |