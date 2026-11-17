# PromptIR 中间层规范(R05,v0 草案)

## 目录
- 目的与边界
- 样本依据
- IR 字段表
- 五后端映射表(样本实证)
- 一致性不变量
- v1 迁移路径

## 目的与边界

PromptIR 是"一次解析、多目标后端"的中间表示:组装流程第 6 步产出通用提示词后,不再对每个模型各写一套模板,而是先落为 IR,再由后端渲染器(IR → 模型特定形态)生成最终产出。

**v0 边界(防过早抽象)**:
- 本规范只定义**字段结构**与**后端映射规则**,不含解析器/生成器实现(脚本属 v1,见迁移路径);
- IR 只承载"表达形态"差异,不承载档位语义——正交性原则与 R02 一致:**任何后端不得改变 9 位档位与头部指纹**;
- 字段全集以本表为准,新增字段必须先有 ≥5 组样本支撑,禁止凭空预定义。

## 样本依据

v0 抽象自 5 组同语义载荷的多模型产出样本(同一需求 case-07,B3 基调 [3,3,3,3,3,3,3,3,3],按 5 个适配器渲染):

| 样本 | 后端 | 文件 |
|------|------|------|
| 1 | claude | [benchmark/model-samples/sample-claude.md](benchmark/model-samples/sample-claude.md) |
| 2 | openai | [benchmark/model-samples/sample-openai.md](benchmark/model-samples/sample-openai.md) |
| 3 | gemini | [benchmark/model-samples/sample-gemini.md](benchmark/model-samples/sample-gemini.md) |
| 4 | deepseek | [benchmark/model-samples/sample-deepseek.md](benchmark/model-samples/sample-deepseek.md) |
| 5 | qwen | [benchmark/model-samples/sample-qwen.md](benchmark/model-samples/sample-qwen.md) |

## IR 字段表

| IR 字段 | 类型 | 来源原子 | 档位条件 |
|---------|------|----------|----------|
| `meta.fingerprint` | int[9] | DEPTH 指纹 | 必填,后端只读 |
| `meta.suffixes` | {model?, lang?, tokens?} | 指纹后缀 | 可选 |
| `role` | {identity, years, capabilities[≤3], perspective?, style?} | role-anchor | D1 单句;D2 双能力;D3 三维+视角+风格;D4 责任锚定 |
| `task` | {action, scope{time,geo,object,exclusions[]}, deliverable{form,words,format}, goal?, success_criteria[]?, ksf[3]?, phased_acceptance?} | task-define | D3+ 含成功标准;D4 含 KSF 与分阶段验收 |
| `context` | {background?, facts[]?, rules[]?, references[]?, timeliness_anchor?, assumptions[]?} | context-inject | D1 空;D2 背景+事实;D3 事实带来源;D4 含时效锚点与假设标注 |
| `examples` | {mode: minimal\|single\|contrast\|multi, items[]} | example-shot | D1 最小例/D2 单例/D3 正反对照/D4 两正一反+风格基准 |
| `format` | {form, structure[], granularity?, chart_contract?, hard_constraints?, closing?} | format-spec | D3+ 颗粒度量化;D4 含可机械检验硬约束 |
| `thinking` | {mode: none\|steps\|three_stage\|three_stage_plus, stages[]} | think-chain | D1 无;D2 五步;D3 三阶段;D4 三阶段+3方案+优化日志 |
| `constraints` | {must[], must_not[], boundaries[]?} | constraints | 条目数下限 D1:3/D2:5+/D3:8+/D4:12+ |
| `self_check` | {items[], scoring?, adversarial[]?, review_nodes[]?} | self-check | D2 三项/D3 五项+评分/D4 对抗质疑+复核节点 |
| `iterate` | {dims[], feedback_path, triggers[]?, depth_tuning?, log?} | iterate | D3+ 含触发词;D4 含深度调档与优化日志 |
| `injections.domains[]` | stem[] | 域判定信号表 | 命中注入,≤2 个 |
| `injections.outputs[]` | stem[] | 输出判定表 | 组合输出全部注入 |
| `tail_module` | string | model-adapters 注入模块 | 仅 @model 后缀存在时渲染 |

## 五后端映射表(样本实证)

| IR 字段 | claude(XML) | openai(# 层级+Schema) | gemini(全大写+编号) | deepseek(中文自然语言) | qwen(中文三段式) |
|---------|-------------|----------------------|--------------------|----------------------|-----------------|
| role | `<role>` | `# Role` | `INSTRUCTION:` | 开篇"你是..."自然语言 | `# 角色`(三维写满) |
| task | `<task>` | `# Task`(编号列表) | `TASK:`+编号 | `任务:`自然语言段 | `# 任务`(有序列表) |
| context | `<context>` | `# Context` | `CONTEXT:`+编号 | `背景与已知信息:` | `# 背景` |
| examples | `<examples>` | `# Examples` | `EXAMPLES:`+编号 | `示例:` | 并入 `# 背景` |
| format | `<output_format>` | `# Output Format`+JSON Schema | `OUTPUT FORMAT:`+编号 | `输出要求:` | `# 输出格式` |
| thinking | `<thinking_instructions>`(+`<thinking>` 开辟思考区) | `# Reasoning Steps`(o-series 撤销) | `STEPS:`显式编号 | 显式 CoT 触发语+三阶段 | `# 执行步骤`(有序列表) |
| constraints | `<constraints>` | `# Constraints`(MUST/MUST NOT 分列) | `CONSTRAINTS:`首尾各一次 | `约束条件:`正反分列 | `# 约束` |
| self_check | `<self_check>` | `# Self-Check` | `SELF-CHECK:` | `完成后请自查:` | `# 自检`(编号) |
| iterate | `<iteration>` | `# Iteration` | `ITERATION:` | `如需调整:` | `# 调整方式` |
| tail_module | `<output_contract>` | `## Output Contract`(Schema) | `REMINDER — CONSTRAINTS (repeat)` | 逐步思考触发语 | 分步执行与自检要求 |
| 域/输出注入 | 对应标签内合并 | 对应 `#` 区内合并 | 对应区块内合并编号 | 对应自然语言段合并 | 对应 `#` 段合并 |

**映射规律(实证结论)**:
1. 五后端的 IR 字段集完全同构,差异仅在**包裹形态**(标签/标题/关键字/自然语言)与**重复策略**(gemini 首尾复述、claude 首尾关键约束)。
2. openai 独有 `output_contract.schema` 子字段(JSON Schema);claude 独有 `thinking` 思考区声明;deepseek 独有显式触发语且禁止刚性 Schema;qwen 要求角色段三维写满且全文中文标点。
3. 内容载荷跨后端逐字等价(除形态词),这是 v1 解析器可往返(round-trip)的前提。

## 一致性不变量

任何后端渲染器必须满足,校验清单:

- [ ] 9 位 DEPTH 指纹与头部后缀逐字保留,渲染器只追加不改动;
- [ ] IR 全部非空字段在产出中均有落点,禁止静默丢弃字段(含 constraints 的每一条);
- [ ] 正反清单(must/must_not)的条目数渲染前后一致;
- [ ] 自检项条数渲染前后一致;
- [ ] examples 的 mode 与数量渲染前后一致;
- [ ] tail_module 只追加在产出尾部,不与任何 IR 字段交叉;
- [ ] 禁用写法遵守各 model-adapters 文件的"禁用写法"节(如 claude 禁 JSON Schema、deepseek 禁刚性模板)。

## v1 迁移路径

1. **触发条件**:每后端样本 ≥5 组(当前各 1 组),覆盖 B1-B4 至少各一档;
2. **交付物**:`scripts/prompt_ir.py`(IR ⇄ 通用提示词双向转换)+ 一致性校验器(逐条跑"不变量"清单);
3. **门禁**:IR005+(字段级 round-trip 校验,新增字段自动纳入);
4. **前置依赖**:无(R02 已稳定,后端差异已由本表锁定)。
