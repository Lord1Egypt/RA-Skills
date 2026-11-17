# References 索引

NodeCoda Workflow skill 的参考文档。按职能分 5 类；每份文件的格式与维护规则见
[`docs/references-convention.md`](../../../docs/references-convention.md)。

## A. 语言规范
- **grammar-reference.md** — EBNF 文法（源真理 `lang/docs/dify-dsl.y` + `parser.py`）。查语法合法性先看这里。
- **language-reference.md** — 编程参考（场景化教学：LLM/工具/HTTP/检索/控制流/FFI/内置函数）。
- **target-capabilities.md** — 目标 profile（`dify-1.16-graphon-0.6`）能力分类与限制。

## B. 协议契约
- **mcp-contract.md** — MCP 工具（build_dify_workflow / get_workflow_build / cancel_workflow_build）签名与输入输出。
- **public-service.md** — 公共部署：REST 端点、认证、健康检查、MCP Streamable HTTP。

## C. 流程
- **project-workflow.md** — 项目模式状态机（INIT→…→SUCCEEDED）与恢复。
- **iteration-loop.md** — 诊断→修复迭代循环（≤5 次）。
- **source-generation.md** — 从需求生成 `.ncoda` 源码的原则。

## D. 诊断
- **diagnostics.md** — 诊断 code 理论分类。
- **diagnostics-map.md** — **实证** code→原文→修复动作映射表（真实 Build 回写）。
- **failure-modes.md** — 系统性失败模式与处置。
- **gotchas.md** — **实证**反模式清单 G1–G8（现象→原因→正确写法）。

## E. 机器可读语言包（`../language-pack/`）

人类文档的同源结构化数据，供 agent 按 feature 检索与校验：

- `grammar.ebnf` — 带 `[feature]` 标签的 EBNF（源自 grammar-reference.md）；
- `builtins.json` — 内置函数/操作策略（源自 language-reference.md §8、target-capabilities.md）；
- `diagnostics.json` — 诊断分类 + 实证 code→修复（源自 diagnostics.md / diagnostics-map.md）；
- `targets/dify-1.16-graphon-0.6.json` — 能力矩阵（源自 target-capabilities.md）；
- `antipatterns.json` — G1–G8 反模式（源自 gotchas.md）；
- `version.json` — 各文件 + 源文档的 sha256，防版本漂移。

任一源文档变更后必须重生成语言包；`node scripts/validate-language-pack.mjs` 校验一致性。

## 维护规则
1. 文法类跟随主仓库 `dify_dsl.y` / `parser.py` 重提炼；
2. 实证类遇到新诊断码/反模式**必须回写**（diagnostics-map.md / gotchas.md）；
3. 增删文件时同步本索引与 manifest.json `references`。
