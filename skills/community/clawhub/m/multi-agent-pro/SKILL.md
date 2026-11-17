---
name: multi-agent-pro
description: 支持多Agent流水线编排（采集→分析→报告），基于DAG调度实现跨技能状态共享、错误重断点续传、执行报告生成、HTML甘特图可视化、人工审批节点（含超时策略）、历史执行对比、硬件自适应参数、版本更新提醒、官方流水线模板库（10类预置模板）、任务级重试策略、节点类型归组、统一错误恢复命令、条件表达式增强、Web控制台、MCP Server暴露、成本实测化桥接、新手向导（orchestrator init）。AI即编排器，脚本提供基础设施。
version: 5.5.0
---


# 多Agent协作编排引擎

> 让 AI 成为编排器，将"单Agent单任务"升级为"多Agent流水线协作"。

> **联系邮箱：** 有更好建议： njskills@agent.qq.com

---

## 快速入门（30秒）

### 速查表

| 你想做什么 | 直接对 AI 说 |
|-----------|-------------|
| 编排一个采集→分析→报告流水线 | "帮我编排一个数据采集到报告生成的流水线" |
| 多个Agent协作完成任务 | "用多Agent协作编排这个任务" |
| 定义并执行DAG流水线 | "帮我定义一个DAG流水线并执行" |
| 查看流水线执行状态 | "查看流水线执行状态" |
| 从断点恢复执行 | "断点续传流水线" |
| 生成执行报告 | "生成流水线执行报告" |
| 可视化甘特图 | "生成流水线甘特图" |
| 查看历史对比 | "对比最近5次执行记录" |

### 三步上手

```
第1步：定义流水线 → AI 生成 pipeline JSON（参考 templates/pipeline_dag_template.json）
第2步：验证并初始化 → python orchestrator.py run pipeline.json
第3步：逐步执行 → python orchestrator.py step state.json（循环直到完成）
```

### 可直接复制的开场白

```
"帮我编排一个竞品分析流水线：采集竞品信息 → 分析优劣势 → 生成报告"
"用多Agent协作编排引擎，把我这个任务拆成三个Agent串行执行"
"定义一个DAG流水线，包含数据采集、数据清洗、数据分析、报告生成四个节点"
"我需要人工审批节点，在关键步骤暂停等用户确认"
```

---

## 依赖

仅需 **Python 3.8+**，零第三方依赖。所有脚本仅使用 Python 标准库。

### 依赖检测

```python
import sys
print(f"Python: {sys.version.split()[0]}")
if sys.version_info < (3, 8):
    print("需要 Python 3.8+，请升级后重试")
else:
    print("环境满足要求，可以正常使用")
```

### 安全声明

| 项目 | 说明 |
|------|------|
| 网络请求 | 仅检查更新时有 GitHub 请求，其他均为本地操作 |
| API Key | 无。不需要任何密钥或认证 |
| 敏感数据 | 状态文件仅存储在本地，不上传任何服务器 |
| 子进程 | 由 AI 编排器管理 spawn 和回收，脚本不创建子进程 |
| 文件写入 | 仅写入 pipeline_state.json 和报告文件到指定路径 |

---

## 能力边界

### 三分类

| 分类 | 说明 | 示例 |
|------|------|------|
| ✅ 擅长 | 多Agent流水线编排、DAG验证、状态管理、错误恢复、执行报告 | "采集→分析→报告"三阶段流水线 |
| ✅ 擅长 | 断点续传、下游影响分析、拓扑排序执行计划 | 失败后从断点恢复执行 |
| ✅ 擅长 | HTML甘特图可视化、人工审批节点、历史执行对比 | DAG执行过程颜色编码时间轴 |
| ✅ 擅长 | 硬件自适应参数推荐、版本更新提醒 | 自动检测CPU/内存推荐并发数 |
| ✅ 擅长 | 动态工作流：条件分支/多路分支/动态节点/循环重试 | 按节点输出运行时决定执行路径 |
| ⚠️ 需素材 | 需要用户提供 DAG 定义（或由AI根据需求生成） | pipeline JSON 文件 |
| ⚠️ 需素材 | 各Agent的具体任务由AI执行，脚本仅管理编排流程 | AI需要自行完成采集/分析/报告等实际任务 |
| ❌ 超范围 | 实时流处理（如Kafka流式消费） | 请使用 Flink/Spark Streaming |
| ❌ 超范围 | 分布式多机调度 | 请使用 Airflow/Prefect |
| ❌ 超范围 | GPU资源调度 | 请使用 Kubernetes/Ray |

---

## 功能模块

---

### 模块 1：DAG 定义与验证

**功能**：用 JSON 定义多Agent流水线，自动验证结构合法性。

**触发词**：`验证DAG`、`检查流水线`、`DAG验证`

**可运行命令**：

```bash
python scripts/dag_validator.py pipeline.json
```

**DAG 定义格式**：

```json
{
  "pipeline_name": "流水线名称",
  "version": "3.0",
  "agents": [
    {
      "id": "agent_1",
      "name": "Agent名称",
      "role": "Agent职责描述",
      "type": "task",
      "inputs": ["input_param"],
      "outputs": ["output_param"],
      "depends_on": [],
      "retry": 3,
      "timeout": 60,
      "fallback": "skip",
      "default_value": null
    }
  ],
  "state_store": {
    "type": "json",
    "path": "./pipeline_state.json"
  }
}
```

**节点类型说明**：

| type 值 | 说明 |
|---------|------|
| `task` | 普通任务节点（默认），AI 自动执行 |
| `approval` | 人工审批节点，执行到此暂停等待用户确认 |
| `condition` | if-else 条件分支节点，按条件走 `on_true` / `on_false` 分支 |
| `switch` | 多路分支节点，按值命中 `cases` / `default` 分支 |
| `for-each` | 动态节点生成，按列表长度展开子节点并汇合 |
| `while-loop` | 循环重试节点，条件为真则回环重跑循环体 |
| `pipeline` | 子流水线引用节点，调用已注册的子流水线隔离执行 |
| `evaluate` | Self-Improving 质量评估节点，质量不达标自动重试目标节点 |

> 动态控制流完整示例见 `templates/control_flow_template.json`；子流水线示例见 `templates/sub_pipeline_template.json` 和 `templates/parent_pipeline_template.json`；控制流节点由引擎自动求值执行，不交给 AI。

**验证内容**：
1. Schema 结构完整性（必填字段检查）
2. 循环依赖检测（Kahn 算法）
3. 孤立节点检测
4. 输出拓扑排序执行顺序

---

### 模块 2：拓扑排序与执行计划

**功能**：按依赖关系自动排序节点，展示执行计划。

**触发词**：`执行计划`、`查看拓扑排序`、`流水线执行顺序`

**可运行命令**：

```bash
python scripts/orchestrator.py plan pipeline.json
```

---

### 模块 3：状态持久化与共享

**功能**：每个Agent的输出自动存入JSON状态文件，下游Agent自动读取上游输出。

**触发词**：`初始化状态`、`保存节点输出`、`查看状态`

**可运行命令**：

```bash
python scripts/orchestrator.py run pipeline.json
python scripts/state_store.py complete state.json node_id '{"result":"输出数据"}'
python scripts/state_store.py fail state.json node_id "错误描述"
python scripts/orchestrator.py status state.json
```

---

### 模块 4：错误恢复（三级降级）

**功能**：节点失败时，按"重试→降级→中止"三级策略自动恢复。

**触发词**：`重试节点`、`节点失败了`、`降级处理`、`错误恢复`

**可运行命令**：

```bash
python scripts/error_recovery.py retry state.json node_id "错误信息"
python scripts/error_recovery.py fallback state.json node_id "错误信息"
python scripts/error_recovery.py impact state.json node_id
```

---

### 模块 5：断点续传

**功能**：流水线中断后，从失败节点恢复执行，跳过已完成节点。

**触发词**：`断点续传`、`恢复执行`、`从断点继续`

**可运行命令**：

```bash
python scripts/orchestrator.py status state.json
python scripts/orchestrator.py resume state.json
python scripts/orchestrator.py step state.json
```

---

### 模块 6：执行报告生成

**功能**：自动生成 Markdown 执行报告，包含概览、节点详情、失败分析、建议。

**触发词**：`生成报告`、`执行报告`、`流水线报告`

**可运行命令**：

```bash
python scripts/orchestrator.py report state.json [output.md]
```

---

### 模块 7：HTML 甘特图可视化 🆕

**功能**：生成纯 HTML 甘特图，颜色编码每个节点的执行状态和时间轴。

**触发词**：`甘特图`、`可视化`、`执行过程图`

**可运行命令**：

```bash
python scripts/orchestrator.py gantt state.json [output.html]
```

**颜色编码**：

| 颜色 | 状态 | 说明 |
|------|------|------|
| 🟢 绿色 | 成功 | completed |
| 🔴 红色 | 失败 | failed |
| 🔵 蓝色 | 执行中 | running |
| 🟡 黄色 | 跳过 | skipped |
| ⚪ 灰色 | 待执行 | pending |

**输出路径**默认 `gantt_<pipeline_id>.html`，可用浏览器直接打开。

---

### 模块 8：人工审批节点 🆕

**功能**：在 DAG 中设置 `type: approval` 节点，流水线执行到此暂停，等待用户确认后继续或终止。

**触发词**：`审批节点`、`人工确认`、`暂停`

**使用方法**：在 pipeline.json 中定义：

```json
{
  "id": "reviewer",
  "name": "人工审核",
  "role": "请确认数据是否符合预期",
  "type": "approval",
  "depends_on": ["previous_node"]
}
```

**执行流程**：
1. 引擎遇到审批节点 → 显示节点信息和上游输出
2. 提示用户输入 `Y`（继续）或 `N`（拒绝）
3. Y → 标记 completed，继续下游
4. N → 标记 aborted，中止流水线

---

### 模块 9：历史执行对比 🆕

**功能**：每次执行完成后自动保存摘要，新执行时与最近5次对比，输出"本次比上次慢X%"。

**触发词**：`历史记录`、`执行对比`、`上次对比`

**可运行命令**：

```bash
# 查看历史记录
python scripts/orchestrator.py history state.json

# 对比最近5次执行
python scripts/orchestrator.py compare state.json
```

**对比维度**：
- 耗时对比（"本次比上次慢23%"）
- 成功/失败节点数对比
- 重试次数对比

**存储位置**：`.execution_history.json`（与 state.json 同目录，保留最近10次）

---

### 模块 10：硬件自适应与参数推荐 🆕

**功能**：自动检测用户电脑硬件配置，推荐最优流水线参数，确保不拖累用户电脑。

**触发词**：`硬件检测`、`性能检测`、`参数推荐`

**可运行命令**：

```bash
python scripts/orchestrator.py hardware
```

**检测内容**：
- CPU 核心数（使用 `os.cpu_count()`）
- 内存大小（Windows 使用 `ctypes` + `GlobalMemoryStatusEx`，Linux/macOS 读取 `/proc/meminfo`）
- 性能等级评估（高/中/低）

**推荐参数**：
- 并发节点数（根据 CPU 核数）
- 文件大小限制（根据内存大小）
- 默认超时时间（根据综合性能）

**安全说明**：仅读取系统信息，不上传任何数据，不修改系统配置。

---

### 模块 11：版本更新提醒 🆕

**功能**：启动时自动检查 GitHub 是否有新版本，有更新时提醒用户。

**触发词**：`检查更新`、`有新版本吗`

**可运行命令**：

```bash
python scripts/orchestrator.py check-update
```

**工作原理**：从 GitHub 仓库读取远程 SKILL.md 的 `version` 字段，与本地版本比对。

**安全说明**：仅读取远程文件，不下载、不安装、不收集数据。

---

### 模块 12：动态工作流（条件分支/多路分支/动态节点/循环）🆕

**功能**：突破静态 DAG 限制，支持运行时根据节点输出动态决定执行路径。四类控制流节点由引擎自动求值处理（不交给 AI）：

**触发词**：`条件分支`、`if-else`、`多路分支`、`switch`、`循环`、`动态节点`、`for-each`、`while循环`

**1) condition（if-else 条件分支）**

```json
{
  "id": "decide_publish",
  "type": "condition",
  "condition": "nodes.review.output_data.score >= 60",
  "on_true": ["publish"],
  "on_false": ["rework"],
  "depends_on": ["review"]
}
```
条件为真执行 `on_true` 分支，为假执行 `on_false` 分支，未选中分支（含下游）整体标记 skipped。

**2) switch（多路分支）**

```json
{
  "id": "route_by_type",
  "type": "switch",
  "switch": "nodes.classify.output_data.category",
  "cases": {"urgent": ["fast_track"], "normal": ["standard"]},
  "default": ["standard"],
  "depends_on": ["classify"]
}
```
按值命中对应 case 分支执行，无命中走 default，其余分支整体 skipped。

**3) for-each（动态节点生成）**

```json
{
  "id": "process_files",
  "type": "for-each",
  "items": "nodes.scan.output_data.file_list",
  "template": {"role": "处理单个文件", "timeout": 60, "retry": 2},
  "join": ["merge_results"],
  "depends_on": ["scan"]
}
```
按 `items` 列表长度展开 `process_files__0/1/2...` 子节点，汇合节点 `join` 自动改依赖所有子节点。单次展开上限 100 个。

**4) while-loop（循环 / 重试增强）**

```json
{
  "id": "loop_guard",
  "type": "while-loop",
  "condition": "nodes.check.output_data.passed == False",
  "loop_body": ["generate", "check"],
  "max_iterations": 5,
  "depends_on": ["check"]
}
```
每轮求值条件，为真且未达上限则重置 `loop_body` 节点重跑一轮，为假或达上限则结束。迭代硬上限 1000 轮，防死循环。

**条件表达式语法**（`scripts/condition_evaluator.py`）：

| 类别 | 支持 |
|------|------|
| 取值 | `nodes.<id>.output_data.<field>`（点路径，支持列表数字索引） |
| 比较 | `==` `!=` `>` `<` `>=` `<=` |
| 逻辑 | `and` `or` `not` |
| 成员 | `in` `not in` |
| 算术 | `+` `-` `*` `/` `//` `%` |

**安全说明**：表达式采用 AST 白名单求值，**禁止 eval/函数调用/lambda/推导式**，杜绝 `__import__`、`os.system` 等注入；表达式长度上限 1000 字符、嵌套上限 50 层，防 DoS。

**验证与自测**：

```bash
# 校验含控制流节点的 DAG
python scripts/dag_validator.py templates/control_flow_template.json

# 单独测试条件表达式
python scripts/condition_evaluator.py "nodes.a.output_data.score >= 60" '{"nodes":{"a":{"output_data":{"score":85}}}}'
```

---

### 模块 13：子流水线嵌套 / 模块化复用 🆕

**功能**：突破单一流水线限制，支持将已有流水线作为"积木"组装到更大的流水线中，实现逻辑复用。

**触发词**：`子流水线`、`模块化`、`流水线引用`、`pipeline 节点`

**核心概念**：
- **子流水线注册**：将可复用的流水线（如"发票处理""合同审查"）注册到注册表
- **pipeline 节点**：在父流水线中放置 `type: pipeline` 节点，引用子流水线
- **参数传递**：父→子传参，子→父映射输出
- **上下文隔离**：子流水线独立执行，内部节点不污染父上下文

**1) 注册子流水线**

```bash
python scripts/pipeline_registry.py register templates/sub_pipeline_template.json --name invoice-pipeline-v1 --version 1.0
```

**2) 查看已注册的子流水线**

```bash
python scripts/pipeline_registry.py list
```

**3) 在父流水线中引用子流水线**

```json
{
  "id": "invoice_step",
  "name": "发票处理（子流水线）",
  "type": "pipeline",
  "pipeline_ref": "invoice-pipeline-v1",
  "params": {
    "file_path": "nodes.submit.output_data.invoice_file"
  },
  "outputs": {
    "invoice_no": "nodes._terminal_.output_data.invoice_no",
    "amount": "nodes._terminal_.output_data.amount"
  },
  "depends_on": ["submit"]
}
```

字段说明：
- `pipeline_ref`：子流水线注册名（必填）
- `params`：传递给子流水线的参数（值支持表达式，在父上下文求值）
- `outputs`：子流水线输出到父上下文的映射（键=父变量名，值=子上下文表达式）

**执行流程**：
1. 引擎检测到 `pipeline` 节点 → 从注册表加载子流水线
2. 创建隔离 state 文件（子流水线独立运行）
3. 用 `params` 表达式求值 → 注入子流水线首节点
4. 逐步执行子流水线所有节点
5. 子流水线完成后，用 `outputs` 表达式映射回父节点 `output_data`
6. 父节点标记 completed，继续下游

**预期效果**：从"每次都从零开始"变成"搭积木式组装"，效率大幅提升。

---

### 模块 14：统一可视化命令 🆕

**功能**：用单一 `visualize` 命令替代原来的 `report` + `gantt` 命令，支持 MD/HTML/三种输出模式。

**触发词**：`可视化`、`生成报告`、`甘特图`、`执行结果'

**可运行命令**：

```bash
# 同时生成 MD 报告和 HTML 甘特图（默认 both）
python scripts/orchestrator.py visualize state.json

# 只生成 MD 报告
python scripts/orchestrator.py visualize state.json --format md

# 只生成 HTML 甘特图
python scripts/orchestrator.py visualize state.json --format html

# 指定输出路径
python scripts/orchestrator.py visualize state.json --format both ./my_report
```

**输出模式**：
| 模式 | 输出 | 说明 |
|------|------|------|
| `md` | `.md` 文件 | Markdown 执行报告（含成本概览） |
| `html` | `.html` 文件 | HTML 甘特图（颜色编码时间轴） |
| `both` | `.md` + `.html` | 两者同时生成 |

**成本概览**（当节点包含 cost_data 时自动展示）：
- 总 Token 消耗
- 总费用（¥）
- 节点成本分布表

**向后兼容**：原 `report` 和 `gantt` 命令仍可用（自动映射到 visualize 的 md/html 模式）。

---

### 模块 15：Self-Improving 循环（质量评估 + 自动重试）🆕

**功能**：在流水线中嵌入质量评估节点，当输出质量不达标时自动重跑上游节点，实现"自我改进"。

**触发词**：`质量评估`、`自动重试`、`Self-Improving`、`evaluate 节点`

**节点配置示例**：

```json
{
  "id": "quality_check",
  "type": "evaluate",
  "quality_expr": "nodes.review.output_data.score >= 80",
  "retry_targets": ["draft", "review"],
  "max_eval_rounds": 3,
  "depends_on": ["review"]
}
```

**字段说明**：
| 字段 | 必填 | 说明 |
|------|------|------|
| `quality_expr` | ✅ | 质量表达式（条件求值，AST 白名单） |
| `retry_targets` | ✅ | 质量不达标时重跑的目标节点 id 列表 |
| `max_eval_rounds` | ✅ | 最大评估轮次（防死循环） |

**执行流程**：
1. evaluate 节点完成 → 对 `quality_expr` 求值
2. 质量达标 → 节点 completed，继续下游
3. 质量不达标且未达上限 → 重置 `retry_targets` 为 pending，评估节点自身回到 pending，等重跑完再次评估
4. 质量不达标且已达上限 → 接受当前结果，节点 completed（带警告）

**安全说明**：
- `max_eval_rounds` 硬上限 1000 轮（防死循环）
- 评估轮次计数存储在 `eval_round` 字段

---

### 模块 16：执行回放 / Time Travel 🆕

**功能**：在复杂流水线调试时，回到任意历史节点重新执行而不影响下游，大幅提升调试效率。

**触发词**：`快照`、`执行回放`、`Time Travel`、`历史恢复`、`执行对比`

**核心能力**：
- **快照机制**：每个节点执行完自动保存上下文快照（输入、输出、执行时间、日志）
- **增量存储**：只保存变化的字段，避免存储膨胀
- **从快照恢复**：选任意历史快照点，从该点重新执行（上游保持不变，下游用新结果覆盖）
- **执行对比**：对比两次执行的结果差异，快速定位问题节点

**快照管理命令**：

```bash
# 列出当前执行的所有快照
python scripts/orchestrator.py snapshot list state.json

# 查看节点快照详情
python scripts/orchestrator.py snapshot show state.json node_id

# 从快照恢复（下游节点重置为 pending）
python scripts/orchestrator.py snapshot restore state.json node_id

# 对比两个节点的快照输出差异
python scripts/orchestrator.py snapshot diff state.json node_id_1 node_id_2
```

**存储结构**：
```
.snapshots/<execution_id>/
├── index.json            # 快照索引
├── snap_<node_id>.json   # 每个节点的快照
```

**版本标识**：`execution_id`（一次流水线运行）+ `snapshot_id`（每个节点快照）

**安全说明**：快照存储在本地 `.snapshots/` 目录，不上传任何服务器。

---

### 模块 17：成本追踪 🆕

**功能**：自动追踪每个节点的 token 消耗和费用，在可视化报告中展示成本概览。

**触发词**：`成本`、`token`、`费用`、`消耗`

**工作原理**：
- 节点完成时，如果 `output_data` 包含 `_cost` 字段，自动提取到 `cost_data`
- `_cost` 字段格式：`{"tokens": 1500, "cost_rmb": 0.003, "model": "gpt-4"}`
- 报告生成时自动汇总总 token/费用/节点分布

**成本数据格式**：

```json
{
  "tokens": 1500,
  "cost_rmb": 0.003,
  "model": "gpt-4"
}
```

**报告展示**：
- 总 Token 消耗
- 总费用（¥）
- 节点成本分布表（节点 id / Token / 费用 / 模型）

**安全说明**：成本数据仅存储在本地 state.json，不上传任何服务器。

---

## 统一入口命令速查

```bash
# 验证 DAG 结构
python scripts/orchestrator.py validate pipeline.json

# 查看执行计划
python scripts/orchestrator.py plan pipeline.json

# 初始化并开始执行
python scripts/orchestrator.py run pipeline.json

# 执行下一个节点
python scripts/orchestrator.py step state.json

# 查看当前状态
python scripts/orchestrator.py status state.json

# 断点续传
python scripts/orchestrator.py resume state.json

# 生成可视化（MD/HTML/both）
python scripts/orchestrator.py visualize state.json --format both

# 生成 Markdown 执行报告
python scripts/orchestrator.py report state.json

# 生成 HTML 甘特图
python scripts/orchestrator.py gantt state.json

# 查看执行历史
python scripts/orchestrator.py history state.json

# 对比最近执行
python scripts/orchestrator.py compare state.json

# 硬件检测与参数推荐
python scripts/orchestrator.py hardware

# 检查更新
python scripts/orchestrator.py check-update

# 快照管理（执行回放 / Time Travel）
python scripts/orchestrator.py snapshot list state.json
python scripts/orchestrator.py snapshot show state.json node_id
python scripts/orchestrator.py snapshot restore state.json node_id
python scripts/orchestrator.py snapshot diff state.json node_id_1 node_id_2

# 子流水线注册表
python scripts/pipeline_registry.py register <pipeline.json> [--name 名称] [--version 1.0]
python scripts/pipeline_registry.py list
python scripts/pipeline_registry.py show <name>
python scripts/pipeline_registry.py validate

# 下游影响分析
python scripts/orchestrator.py impact state.json node_id
```

---

## 反模式（请避免）

| 反模式 | 问题 | 正确做法 |
|--------|------|---------|
| 循环依赖 | A→B→C→A 死锁 | 打破循环，改为 DAG |
| 巨型节点 | 所有逻辑放一个节点 | 按职责拆分为多个节点 |
| 零容错 | retry=0 + fallback=abort | 前端节点高重试+skip，末端节点低重试+abort |

详见 `references/anti-patterns.md`。

---

## 安全风险项

| 风险项 | 等级 | 说明 | 缓解措施 |
|--------|------|------|---------|
| 子进程泄漏 | P1 | AI 编排器 spawn 的子 Agent 未正确回收 | AI 需确保每个子任务完成后回收资源；脚本不创建子进程 |
| 状态文件并发写入 | P2 | 多个编排实例同时写同一个 state.json | 每个流水线使用独立的 state 文件路径 |
| DAG 循环依赖 | P2 | 用户定义了循环依赖的 DAG | `dag_validator.py` 启动前强制检测，发现环即中止 |
| 状态文件过大 | P2 | 节点输出过多导致 state.json 膨胀 | 单节点输出超过 10MB 时写入独立文件，state 中只存路径 |
| 敏感数据泄露 | P1 | Agent 输出中可能包含敏感信息 | FAQ 说明脱敏方法；建议不要处理真实密钥 |

---

## FAQ

### Q: 脚本支持哪些操作系统？
A: Windows、macOS、Linux 全部支持。仅使用 Python 标准库，无平台依赖。

### Q: 需要安装第三方库吗？
A: 不需要。所有脚本仅使用 Python 标准库（json/os/sys/time/datetime/platform/ctypes/urllib），开箱即用。

### Q: AI 在编排中扮演什么角色？
A: AI 是编排器。脚本提供基础设施（验证/状态/报告），AI 负责理解用户需求→生成DAG→逐步执行各节点任务→管理错误恢复。详见 `references/examples.md`。

### Q: 如何处理节点间数据传递？
A: 节点完成时将输出保存到 `pipeline_state.json`，下游节点执行时引擎自动注入上游输出。详见 `references/state-sharing-protocol.md`。

### Q: 节点失败后怎么恢复？
A: 三级策略：重试（自动）→ 降级（skip/default/abort）→ 断点续传。详见 `references/error-recovery-patterns.md`。

### Q: 如何查看完整的端到端示例？
A: 参见 `references/examples.md`，包含竞品分析、数据处理（含错误恢复）、断点续传三个完整案例。

### Q: 甘特图怎么打开？
A: 运行 `python orchestrator.py gantt state.json`，生成的 `.html` 文件可直接用浏览器打开。

### Q: 如何设置人工审批节点？
A: 在 pipeline.json 中定义节点时添加 `"type": "approval"`，执行到此节点时会暂停等待用户确认。

### Q: 历史记录占用多少存储？
A: 默认保留最近10次执行摘要，每次摘要约200字节，总计不超过2KB。

### Q: 硬件检测会不会修改我的系统配置？
A: 不会。硬件检测仅读取系统信息（CPU核数、内存大小），不做任何修改。

---

## 深度参考

| 文档 | 内容 |
|------|------|
| `references/dag-scheduling-guide.md` | DAG 调度原理：拓扑排序、执行策略、环检测、孤立节点 |
| `references/state-sharing-protocol.md` | 状态共享协议：数据传递机制、状态转换、最佳实践 |
| `references/error-recovery-patterns.md` | 错误恢复模式库：5种常见场景及恢复决策树 |
| `references/anti-patterns.md` | 反模式说明：3类常见错误 + 改进对比 |
| `references/faq-deep.md` | 深度 FAQ：10题覆盖边缘场景 |
| `references/examples.md` | 完整使用示例：3个端到端案例 |
| `templates/pipeline_dag_template.json` | DAG 定义模板（含人工审批节点示例） |
| `templates/control_flow_template.json` | 动态控制流模板（condition/switch/for-each/while-loop 完整示例） |
| `templates/state_schema.json` | 状态文件 JSON Schema 规范 v5.0 |
| `tests/test_pipeline.json` | 测试用 DAG（含审批节点，用于自检） |
| `tests/test_control_flow.json` | 控制流测试 DAG（四类控制节点端到端验证） |

---

## 禁止文件类型

本 Skill **不支持**以下文件类型的处理或生成：

| 类别 | 禁止的文件类型 |
|------|---------------|
| Windows 可执行/批处理脚本 | `.bat`、`.cmd`、`.ps1`、`.vbs`、`.exe`、`.dll`、`.lnk`、`.msi` |
| Office 二进制文档 | `.docx`、`.xlsx`、`.pptx`、`.doc`、`.xls`、`.ppt`、`.xlsm`、`.docm`、`.pptm` |
| 二进制镜像/安装包 | `.iso`、`.dmg`、`.zip`、`.rar`、`.7z`、`.tar`、`.gz`、`.apk`、`.jar` |
| 系统缓存/隐藏文件 | `.DS_Store`、`.git`目录、`.env`、`.log`、`.tmp` |
| 其他风险脚本 | `.sh`、`.com`、`.scr`、`.hta`、`.reg` |

---

---

### 模块 18：官方流水线模板库 🆕

**功能**：预置 4 类高频流水线模板，让引擎价值被直接看见。每个模板元数据声明建议安装的外部 skill，运行时探测依赖是否就绪，缺失则标灰提示安装链接。

**触发词**：`预置模板`、`政采日报`、`视频分析`、`周报生成`、`巡检汇总`

**预置模板列表**：

| 模板 | 文件 | 分类 | 描述 |
|------|------|------|------|
| 政采日报 | `templates/gov_procurement_daily.json` | 数据加工 | 政采信息抓取→筛选→分析→风控审核→日报生成 |
| 视频批量分析 | `templates/video_batch_analysis.json` | 内容生成 | 视频加载→关键帧提取→画面分析→摘要生成 |
| 周报生成 | `templates/weekly_report_gen.json` | 分析汇总 | 执行记录汇总→成本分析→TL审核→周报排版 |
| 巡检汇总 | `templates/inspection_summary.json` | 监控预警 | 巡检项发现→状态检查→异常分析→运维审核→巡检报告 |

**模板元数据示例**：

```json
{
  "name": "政采日报",
  "description": "...",
  "category": "data-processing",
  "dependencies": [
    {
      "skill_id": "tencent-docs",
      "install_link": "https://skillhub.cn/skill/tencent-docs",
      "description": "腾讯文档（用于日报内容协作）",
      "required": false
    }
  ],
  "pipeline": { ... }
}
```

**可运行命令**：

```bash
# 列出所有预置模板
python orchestrator.py template list

# 显示模板详情 + 依赖状态
python orchestrator.py template show gov_procurement_daily.json

# 检查依赖是否满足
python orchestrator.py template check gov_procurement_daily.json

# 渲染为可执行 pipeline.json
python orchestrator.py template render gov_procurement_daily.json my_pipeline.json
```

**探测渲染规则**：
- 依赖已安装 → ✅ 正常显示
- 依赖缺失 + `required: true` → ⚠️ 对应节点标灰 + 显示安装链接
- 依赖缺失 + `required: false` → ⚠️ 提示安装链接但不阻塞执行

**安全说明**：仅提示安装，不自动下载/安装/隐式依赖，保持单包合规。

---

### 模块 19：任务级重试策略 🆕

**功能**：节点 schema 新增 `retry` 块，支持任务级重试策略配置。未配置的节点保持旧全局策略，完全向后兼容。

**触发词**：`节点重试`、`退避策略`、`降级链`、`retry 块`

**retry 块配置**：

```json
{
  "id": "node_a",
  "retry": {
    "count": 5,
    "backoff_base": 2,
    "fallback_chain": ["retry", "reparam", "skip"]
  }
}
```

| 字段 | 说明 | 默认值 |
|------|------|--------|
| `count` | 最大重试次数 | 3 |
| `backoff_base` | 指数退避基数（第 N 次等待 = base^N 秒） | 2 |
| `fallback_chain` | 降级动作链（按顺序执行） | `["retry", "skip"]` |

**降级动作**：
- `retry`：重置为 pending，等待重新执行
- `reparam`：换参数重试（保留 intermediate 输出供参考）
- `skip`：跳过此节点，下游收到 `output_data={"skipped": true}`
- `abort`：中止流水线

**向后兼容**：未配置 `retry` 块的节点走旧全局策略（`retry` 字段 / `fallback` 字段）。

---

### 模块 20：节点类型归组（认知层） 🆕

**功能**：7 种节点类型在文档、帮助、校验错误中归为 4 类，降低认知负担。DAG Schema 完全不变，旧流水线零迁移。

| 归组 | 包含的 type | 说明 |
|------|-----------|------|
| **任务** | `task` | 普通 AI 执行节点 |
| **控制** | `condition` / `switch` | 条件分支 / 多路分支 |
| **控制** | `for-each` / `while-loop` | 动态循环 / 条件循环 |
| **控制** | `evaluate` | 质量评估 + 自动重试 |
| **人工** | `approval` | 人工确认节点 |
| **复用** | `pipeline` | 子流水线引用 |

**实现原则**：归组只动认知层（文档/提示/校验错误信息），不动 DAG Schema。

---

### 模块 21：统一错误恢复命令 🆕

**功能**：将 `retry/fallback/impact` 三个独立子命令合并为 `recover` 带子命令。旧命令向后兼容（自动映射到 recover）。

**触发词**：`错误恢复`、`重试`、`降级`、`影响分析`

**可运行命令**：

```bash
# 统一入口（推荐）
python orchestrator.py recover retry state.json node_a '网络超时'
python orchestrator.py recover fallback state.json node_a '网络超时'
python orchestrator.py recover impact state.json node_a

# 旧命令（保持可用，自动映射到 recover）
python orchestrator.py retry state.json node_a '网络超时'
python orchestrator.py fallback state.json node_a '网络超时'
python orchestrator.py impact state.json node_a
```

**安全说明**：旧命令可用但推荐迁移到新入口，减少命令面。

---

### 模块 22：条件表达式增强 🆕

**功能**：AST 白名单求值器新增正则匹配（re_safe 子集）与字符串操作函数，白名单机制不变，长度与嵌套上限沿用。

**触发词**：`正则匹配`、`contains`、`startswith`、`split`

**新增字符串函数**：

| 函数 | 说明 | 示例 |
|------|------|------|
| `contains(s, sub)` | 包含检查 | `contains(nodes.a.output_data.text, "ERROR")` |
| `startswith(s, prefix)` | 前缀检查 | `startswith(nodes.a.output_data.status, "run")` |
| `endswith(s, suffix)` | 后缀检查 | `endswith(nodes.a.output_data.file, ".json")` |
| `split(s, sep)` | 分割 | `len(split(nodes.a.output_data.tags, ",")) > 3` |
| `join(sep, iterable)` | 连接 | `join(", ", nodes.a.output_data.items)` |
| `strip(s)` | 去空白 | `strip(nodes.a.output_data.name) == "test"` |
| `lower(s)` | 转小写 | `lower(nodes.a.output_data.env) == "prod"` |
| `upper(s)` | 转大写 | `upper(nodes.a.output_data.level) == "HIGH"` |
| `replace(s, old, new)` | 替换 | `replace(nodes.a.output_data.text, "a", "b")` |

**新增正则函数（re_safe 子集）**：

| 函数 | 说明 | 示例 |
|------|------|------|
| `match(pattern, string)` | 匹配开头 | `match("ERR-\\d+", nodes.a.output_data.code)` |
| `search(pattern, string)` | 搜索 | `search("[A-Z]{3}", nodes.a.output_data.text)` |
| `findall(pattern, string)` | 全部匹配 | `findall("\\d+", nodes.a.output_data.version)` |

**安全限制**：
- 禁止关键字参数（`re.sub` 等）
- 正则仅允许 match/search/findall，禁止 `re.compile`、`re.sub` 等
- 函数参数最多 5 个
- 表达式长度上限 1000 字符，嵌套上限 50 层

---

### 模块 23：Web 控制台 🆕

**功能**：内置 http.server 只读 Web 服务，使用 ECharts 渲染交互式甘特图，支持流水线列表、执行日志、节点输入输出查看、人工审批按钮。

**触发词**：`控制台`、`仪表盘`、`dashboard`、`web 控制台`、`可视化面板`

**启动方式**：
```bash
python orchestrator.py dashboard [state_dir] [port]
```

**默认配置**：
- 监听地址：`127.0.0.1:7788`（仅本机，不暴露外网）
- 端口可通过第二个参数覆盖

**功能说明**：

| 页面 | 功能 |
|------|------|
| 首页 `/` | 列出所有已执行的流水线（名称/状态/耗时/节点数） |
| 详情页 `/detail?file=<state.json>` | ECharts 甘特图：X 轴时间、Y 轴节点列表，颜色编码状态，点击节点显示输入/输出 |
| 审批按钮 | 审批节点出现"通过/拒绝"按钮，点击后 POST 到 `/api/approve`，需带 `X-Local-Token` 请求头（令牌从状态目录下的 `.dashboard_token` 文件读取） |

**安全设计**：
- 仅监听 `127.0.0.1`，拒绝外部连接
- 审批 API 需携带本地令牌（`secrets.token_hex(16)`），防止误操作
- 全部为只读操作（除审批外），不修改任何流水线文件

---

### 模块 24：MCP Server 暴露 🆕

**功能**：将 multi-agent-orchestrator 包装为 MCP（Model Context Protocol）工具，通过 stdio JSON-RPC 暴露三个工具，其他 Agent 框架可把整条流水线当作单个工具调用。

**触发词**：`MCP`、`tool`、`暴露为工具`、`跨框架调用`

**启动方式**：
```bash
python orchestrator.py mcp
```

**暴露的三个工具**：

| 工具名 | 说明 | 必需参数 |
|--------|------|---------|
| `pipeline_run` | 运行流水线 | `pipeline_file`（YAML/JSON 路径），可选 `inputs`（输入参数 dict） |
| `pipeline_status` | 查询运行状态 | `run_id`（由 pipeline_run 返回） |
| `pipeline_approve` | 人工审批/拒绝 | `run_id`、`node_id`、`approved`（True/False），可选 `comment` |

**集成方式**：其他 Agent 框架通过 MCP 协议连接 orchestrator 后，调用 `pipeline_run` 启动流水线，`pipeline_status` 轮询进度，`pipeline_approve` 处理人工审批。

---

### 模块 25：成本实测化桥接 🆕

**功能**：白名单探测 `cn-llm-router`，命中则子进程调用其成本报告命令（`--json {start,end}` 区间），回填真实 token/cost 到节点 `cost_data` 列；未安装则保留估算值，加 `est` 前缀。报告分"实测/估算"两列展示。

**触发词**：`成本`、`费用`、`实测成本`、`token消耗`、`cost`

**使用方式**：

```bash
# 1. 检测 cn-llm-router 是否可用
python orchestrator.py cost <state_dir> --check

# 2. 回填实测成本（扫描目录下所有状态文件）
python orchestrator.py cost <state_dir>

# 3. 指定流水线回填
python orchestrator.py cost <state_dir> --pipeline <pipeline_name>

# 4. 输出单个状态文件的成本汇总
python orchestrator.py cost <state_file> --summary
```

**数据流**：
1. `cost_bridge.detect_cn_llm_router()` 探测 `~/.workbuddy/skills/cn-llm-router/scripts/cn_llm_router.py` 是否存在
2. 若可用，调用 `cn_llm_router cost-report --json [--run-id X] [--start T] [--end T]` 获取实测数据
3. 匹配节点（按节点 ID/名称），覆盖估算值，标记 `"est": False`、`"source": "cn-llm-router"`
4. `pipeline_reporter._build_visualization_data()` 按 `est` 字段分组求和，报告展示：
   - 实测 Token / 实测费用（蓝色 🔵）
   - 估算 Token / 估算费用（白色 ⚪）
   - 合计 Token / 合计费用

**估算价格表**（未安装 cn-llm-router 时使用）：

| 模型 | 每 token 价格（¥） |
|------|------------------|
| default | 0.0004 |
| gpt-4 | 0.03 |
| gpt-3.5-turbo | 0.002 |
| deepseek-chat | 0.001 |
| qwen-turbo | 0.0008 |
| glm-4 | 0.001 |
| glm-4-flash | 0.0001 |

---

### 模块 26：模板库扩容（10 类官方模板） 🆕

**功能**：预置流水线模板库从 4 类扩容至 10 类，覆盖更多高频场景。每类模板含 pipeline 定义、依赖声明、示例数据、三要素声明（耗时/依赖/产物）。

**触发词**：`模板`、`template`、`预置`、`示例`

**10 类官方模板**：

| # | 模板名 | 分类 | 耗时预估 | API Key | 核心能力 |
|---|--------|------|---------|---------|---------|
| 1 | 政采日报 | data-processing | 5-10 分钟 | 不需要 | 政采信息抓取→筛选→分析→日报 |
| 2 | 视频批量分析 | content-generation | 10-20 分钟 | 可选 | 视频加载→关键帧提取→画面分析→摘要 |
| 3 | 周报生成 | analysis | 3-5 分钟 | 不需要 | 执行记录汇总→成本分析→周报排版 |
| 4 | 巡检汇总 | monitoring | 5-15 分钟 | 不需要 | 巡检项发现→状态检查→异常分析→报告 |
| 5 | 竞对监控日报 | monitoring | 8-15 分钟 | 可选 | 官网/价格/社媒监控→变动分析→日报 |
| 6 | 发票批量处理 | office | 10-30 分钟 | 可选 | OCR→真伪查验→分类→报销单填充→申报 |
| 7 | 文件整理归档 | office | 5-15 分钟 | 不需要 | 文件扫描→分类→重复检测→重命名→归档 |
| 8 | 考试刷题统计 | analysis | 3-5 分钟 | 不需要 | 刷题数据→正确率→薄弱点→趋势→报告 |
| 9 | 直播复盘 | media | 5-10 分钟 | 可选 | 直播数据采集→指标计算→高光/低谷→复盘 |
| 10 | 知识库周更 | content-generation | 10-20 分钟 | 可选 | 信息源扫描→变更检测→质量检查→更新→日志 |

**使用方式**：
```bash
python orchestrator.py template list                    # 列出所有模板（含三要素摘要）
python orchestrator.py template show <template_file>    # 查看模板详情（含三要素头部）
python orchestrator.py template render <template_file>  # 渲染为可执行 pipeline.json
python orchestrator.py template validate [template]     # CI 校验（三要素齐全 + 结构完整）
```

---

### 模块 27：newbie 向导 🆕

**功能**：交互式新手向导（`orchestrator init`），帮助新用户在 5 分钟内创建第一条流水线。全程"先清单后确认"（对齐 winskill 交互基因）。

**触发词**：`init`、`新手``向导`、`创建流水线`、`开始`

**流程**：
1. 列出所有可用模板（含三要素摘要）
2. 用户选择模板编号
3. 展示模板详情（含依赖状态）
4. 收集参数（流水线名称、输出目录）
5. Dry-run 预览（节点序列 + 依赖状态）
6. 确认生成 pipeline.json

**使用方式**：
```bash
python orchestrator.py init
```

---

### 模块 28：模板三要素化与 CI 校验 🆕

**功能**：每个模板头部强制标注三要素（耗时预估/依赖需求/产物清单），元数据 schema 扩展，CI 校验检查三要素齐全。

**触发词**：`三要素`、`校验`、`validate`、`CI`

**三要素元数据**（`template_schema.json` 扩展）：

| 字段 | 类型 | 说明 |
|------|------|------|
| `three_elements.time_estimate` | string | 跑一次大概多久（如 5-10 分钟） |
| `three_elements.api_key_required` | enum | 不需要 / 可选 / 必需 |
| `three_elements.output_files` | array | 产生什么文件列表 |

**CI 校验规则**：
- 三要素字段齐全（time_estimate、api_key_required、output_files）
- pipeline 结构完整（含 agents 列表）
- 必需字段存在（name、description、category、version）

**使用方式**：
```bash
python orchestrator.py template validate                    # 校验所有模板
python orchestrator.py template validate <template_file>    # 校验单个模板
```

---

## 更新日志

| 版本 | 日期 | 更新内容 |
|------|------|---------|
| v5.5.0 | 2026-10-10 | 增加：模板库扩容 4→10（新增竞对监控日报/发票批量处理/文件整理归档/考试刷题统计/直播复盘/知识库周更 6 类官方模板），每类模板含 pipeline 定义+依赖声明+示例数据+三要素声明（耗时/依赖/产物）；增加：newbie 向导（orchestrator init），交互式选模板→填参数→dry-run预览→确认生成，全程先清单后确认；增加：模板详情页三要素化（template_schema.json 扩展 three_elements 元数据，CI 校验检查三要素齐全）；增加：template validate 子命令（CI 校验入口）；增加：init 命令（新手向导入口）；优化：template list 展示三要素摘要；优化：template show 展示三要素头部信息 |
| v5.4.0 | 2026-08-07 | 增加：Web 控制台（web_dashboard.py），内置 http.server 只读服务（仅本机 127.0.0.1:7788）+ ECharts 甘特图，支持点击节点查看输入输出、人工审批按钮（POST 带 X-Local-Token 防误触）；增加：MCP Server（mcp_server.py），stdio JSON-RPC 暴露 pipeline_run/pipeline_status/pipeline_approve 三个工具，其他 Agent 框架可调用整条流水线为单工具；增加：成本实测化桥接（cost_bridge.py），白名单探测 cn-llm-router，命中则子进程调用成本报告回填真实 token/cost，未安装保留估算值加 est 前缀，报告分实测/估算两列展示；增加：cost 命令（cost_bridge 入口），支持 --check/--summary/--pipeline 参数；增加：dashboard 命令（Web 控制台入口），支持 [state_dir] [port] 参数；增加：mcp 命令（MCP Server 入口）；优化：pipeline_reporter 成本概览分实测/估算两列，节点成本分布表增加来源标签（🔵实测/⚪估算） |
| v5.3.0 | 2026-08-24 | 增加：官方流水线模板库（4类预置模板：政采日报/视频分析/周报/巡检），模板元数据声明依赖 skill，运行时探测缺失则标灰+安装链接，单包合规不自动安装；增加：任务级重试策略（节点级 retry 块：count/backoff_base/fallback_chain），未配置走旧全局策略向后兼容；增加：节点类型归组（7类→4类：任务/控制/人工/复用），仅认知层文档归组 Schema 零变更；增加：统一错误恢复命令 recover（retry/fallback/impact 三合一），旧命令向后兼容；增加：条件表达式增强（re_safe 正则子集 + contains/startswith/split/join 等字符串函数），AST 白名单机制不变 |
| v5.2.0 | 2026-08-07 | 增加：统一可视化命令 visualize（--format md|html|both），整合执行报告与甘特图为单一入口，消除 report/gantt 命令重复代码；增加：evaluate 控制流节点（Self-Improving 循环），支持质量表达式评估 + 自动重试目标节点 + 最大轮次限制；增加：节点级成本追踪（cost_data 字段），在 complete_node 自动提取 _cost 字段，报告展示总 token/费用/节点分布；增加：HTML 甘特图费用概览区块，展示总消耗与节点成本分布；优化：dag_validator 校验 evaluate 节点字段与 retry_targets 引用完整性；优化：flow_controller 扩展 evaluate 类型调度，复用 while-loop 迭代模式；优化：state_store 持久化 quality_expr/retry_targets/max_eval_rounds 控制流字段 |
| v5.1.0 | 2026-08-07 | 增加：统一状态恢复子系统 state_recovery，合并断点续传与快照恢复为单一入口，消除两套独立恢复代码；增加：快照保留策略（SNAPSHOT_MAX_AGE_DAYS=7天 / SNAPSHOT_MAX_COUNT=100次 / SNAPSHOT_MAX_SIZE_MB=100MB），按时间+数量+大小三维度自动淘汰旧快照；增加：审批节点超时策略（timeout_seconds + timeout_action），支持超时自动通过/拒绝，避免无人值守场景阻塞；增加：恢复前自动创建检查点（.recovery_checkpoints/），防止误操作不可逆；优化：dag_validator 校验 approval 节点 timeout_seconds 与 timeout_action 字段合法性 |
| v5.0.0 | 2026-07-13 | 增加：pipeline 子流水线节点，支持将已注册流水线作为模块嵌套到父流水线并实现上下文隔离；增加：pipeline_registry 子流水线注册表，支持注册/列出/查看/校验子流水线；增加：snapshot_store 快照存储机制，首个快照存完整数据后续只存增量 diff；增加：snapshot 子命令（list/show/restore/diff），支持从任意历史节点恢复下游重跑的 Time Travel 执行回放；增加：sub_pipeline_template 与 parent_pipeline_template 示例模板展示子流水线注册与引用；优化：flow_controller 扩展 pipeline 类型调度，自动加载子流水线并注入参数映射输出；优化：state_store 节点完成自动保存快照，持久化 pipeline_ref/params/outputs 控制流字段；优化：dag_validator 校验 pipeline 节点字段与 pipeline_ref 引用完整性 |
| v4.0.0 | 2026-07-13 | 增加：condition 条件分支节点，按表达式走 on_true/on_false 分支；增加：switch 多路分支节点，按值命中 cases/default；增加：for-each 动态节点生成，按列表长度展开子节点并自动重挂汇合依赖；增加：while-loop 循环重试节点，条件为真回环重跑循环体并设迭代上限防死循环；增加：condition_evaluator 表达式求值器，采用 AST 白名单禁止函数调用防注入；增加：flow_controller 控制流引擎自动求值路由；增加：control_flow_template 与 test_control_flow 示例及测试；优化：dag_validator 校验控制流节点字段与分支引用；优化：控制流求值失败标记终态失败避免调度器反复重取 |
| v3.0.0 | 2026-07-13 | 增加：HTML甘特图可视化模块，支持颜色编码的DAG执行时间轴；增加：人工审批节点（type: approval），可在关键步骤暂停等用户确认；增加：历史执行对比功能，自动保存最近10次执行摘要并对比耗时/成功率/重试次数；增加：硬件自适应模块，自动检测CPU/内存并推荐最优流水线参数；增加：版本更新提醒功能，对比GitHub远程版本；增加：禁止文件类型清单；优化：all_done判定逻辑，支持skipped节点视为完成；优化：calc_duration提取为独立函数供历史模块复用 |
| v2.0.1 | 2026-07-08 | 修复：状态文件并发写入potential问题；优化：atomic write安全性 |
| v2.0.0 | 2026-07-01 | 增加：三级错误恢复策略；增加：断点续传功能；增加：执行报告生成；优化：拓扑排序算法 |