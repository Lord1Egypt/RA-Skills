# 提示词包协议(R06,v0 草案)

## 目录
- 目的与边界
- 包结构
- 交接协议(Handoff Schema)
- 组包流程
- 最小示例
- 门禁与验收

## 目的与边界

单提示词无法承载"主任务拆解 → 子任务并行 → 结果回传汇总"的复杂编排。提示词包(Prompt Package)把一次复杂任务组织为:1 个主提示词 + N 个子任务提示词 + 1 份交接协议。

**v0 边界**:
- 本协议只定义**包结构与交接字段**,不含运行时编排引擎(R09 CLI 或外部 Agent 运行时属后续);
- 模型适配沿用 R02 后缀正交原则:主/子提示词各自独立携带 DEPTH 指纹与 @model 后缀,禁止在交接层改写档位;
- 依赖规则 R1-R5 在**每个提示词内部**独立成立,不跨提示词求值(v0 不做跨文档指纹校验)。

## 包结构

```
<package-name>/
  package.yaml          # 包清单(见下)
  main.md               # 主提示词(含 DEPTH 指纹头部)
  subtasks/
    st-01.md            # 子任务提示词(各自含 DEPTH 指纹头部)
    st-02.md
    ...
```

**package.yaml 字段**(极简解析,与 benchmark/cases.yaml 同风格,不引第三方依赖):

```yaml
version: 1
name: package-name
main: main.md
subtasks:
  - id: st-01
    file: subtasks/st-01.md
    depends_on: []          # 前置子任务 id 列表,形成 DAG
    input_from: main        # 输入来源: main 或某子任务 id
    output_to: main         # 输出去向: main 或某子任务 id
  - id: st-02
    file: subtasks/st-02.md
    depends_on: [st-01]
    input_from: st-01
    output_to: main
```

约束:`depends_on` 必须无环(DAG);`input_from`/`output_to` 引用的 id 必须存在(main 或已登记子任务);文件路径必须真实存在。

## 交接协议(Handoff Schema)

子任务之间的数据交接统一为 JSON 对象,字段固定:

```json
{
  "task_id": "st-01",
  "status": "done | blocked | needs_human",
  "output": { },
  "assumptions": ["假设: ..."],
  "handoff_notes": "给下游的显式说明"
}
```

| 字段 | 必填 | 约定 |
|------|------|------|
| task_id | 是 | 必须与 package.yaml 登记的 id 一致 |
| status | 是 | `done`(可交接)/ `blocked`(需上游补救)/ `needs_human`(挂起等人工) |
| output | status=done 时必填 | 任意 JSON 值,结构由上游子提示词的输出契约声明 |
| assumptions | 否 | 未经核实的前提,沿用"假设:"前缀规范 |
| handoff_notes | 否 | 下游必须阅读的显式说明,禁止隐式依赖 |

## 组包流程

1. **拆解判定**:主任务含 ≥2 个可独立交付的子目标,且子目标间存在明确输入输出关系,才组包;单一交付物禁止组包(防止过度工程)。
2. **主提示词生成**:按 manifest 组装流程生成,交付物定义为"汇总各子任务结果";指纹按主任务自身复杂度判定,不受子任务影响。
3. **子提示词生成**:每个子任务独立走完整组装流程(信息检查→基调判定→指纹→组装);子提示词头部 DEPTH 指纹独立判定。
4. **交接声明**:每个子提示词在 format 段声明输出契约(与 Handoff Schema 的 output 字段对齐);主提示词声明"按 Handoff Schema 回传"。
5. **包校验**:package.yaml 引用完整性(文件存在、DAG 无环、id 双向一致);每个 .md 头部 DEPTH 指纹可解析(fingerprint.py parse)。
6. **运行与回传**(v0 由人工或外部 Agent 执行):按 DAG 拓扑序执行子任务,回传 Handoff 对象,主提示词汇总。

## 最小示例

以"市场调研 + 数据测算 + 报告汇总"为例:

```yaml
version: 1
name: ev-market-package
main: main.md
subtasks:
  - id: st-data
    file: subtasks/st-data.md      # 子任务 1:数据收集与口径整理
    depends_on: []
    input_from: main
    output_to: st-analysis
  - id: st-analysis
    file: subtasks/st-analysis.md  # 子任务 2:接受度分析(依赖 st-data)
    depends_on: [st-data]
    input_from: st-data
    output_to: main
```

主提示词交付物声明:"汇总 st-analysis 的 output 与 assumptions,输出最终报告;status 非 done 的子任务在报告'待验证事项'节显式列出"。

## 门禁与验收

- PK 系列:`validate_prompt_package()`(IR/PK/RG 门禁统一在 validate_skill.py);
- 结构验收:包目录内每个 .md 可通过 fingerprint.py parse;package.yaml 引用完整性;
- 语义验收:主/子提示词各自通过七维速查表核对;交接字段与子提示词输出契约对齐。

## v1 迁移路径

1. 触发条件:R09 CLI 落地后,由 `ape build --package` 执行包校验与拓扑排序;
2. 交付物:`scripts/prompt_package.py`(包校验器:YAML 解析 + DAG 检查 + 指纹解析);
3. 扩展:跨子任务的依赖规则求值(如子任务指纹总和的预算约束)、失败重试策略。
