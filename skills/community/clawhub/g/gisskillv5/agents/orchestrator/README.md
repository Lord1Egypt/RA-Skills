<!-- wm:坤图_GIS:V5.0 -->
# 多Agent流程编排引擎 V5.0

> 版本：V5.0 | 层级：上层-调度引擎 | 优先级：高于数据处理逻辑
> 约束：V5_CONSTITUTION.md 全部条款强制生效

---

## 引擎架构

```
                    ┌──────────────────────┐
                    │   Orchestrator       │
                    │   (流程调度器)        │
                    │   优先级 > 数据处理   │
                    └──────┬───────────────┘
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                   │
   ┌────▼────┐      ┌─────▼─────┐      ┌─────▼─────┐
   │ 数据探查 │      │ 处理执行   │      │ 质检校验   │
   │ Agent    │      │ Agent     │      │ Agent      │
   └────┬────┘      └─────┬─────┘      └─────┬─────┘
        │                  │                   │
   ┌────▼────┐      ┌─────▼─────┐
   │ 标准合规 │      │ 文档生成   │
   │ Agent    │      │ Agent      │
   └─────────┘      └───────────┘
```

---

## Agent 定义

### 1. 数据探查 Agent (Data Explorer)

```yaml
agent_id: AGT-001
agent_name: data_explorer
trigger_skills: [ATS-002 dlg_inspection]
responsibility: 数据格式识别/坐标系探查/属性分析/风险报告
input_artifacts: [原始数据文件]
output_artifacts: [数据透视与风险报告]
block_next_if: 报告未生成 或 风险等级 > 2
```

### 2. 处理执行 Agent (Process Executor)

```yaml
agent_id: AGT-002
agent_name: process_executor
trigger_skills: [ATS-001 坐标转换, ATS-003 拓扑修复, ATS-004 编码校验, ATS-009 DWG互转]
responsibility: 执行数据处理全链路
input_artifacts: [数据探查报告, 原始数据]
output_artifacts: [处理后数据, 执行日志, 修复记录]
retry_policy: {max_retries: 3, backoff: "exponential"}
```

### 3. 质检校验 Agent (Quality Inspector)

```yaml
agent_id: AGT-003
agent_name: quality_inspector
trigger_skills: [ATS-005 二级质检]
responsibility: 成果质量检查/缺陷判定/整改建议
input_artifacts: [处理后数据, 质检标准引用]
output_artifacts: [质检报告, 缺陷清单, 整改建议]
pass_threshold: 60分(GB/T 18316标准)
```

### 4. 标准合规 Agent (Standard Compliance)

```yaml
agent_id: AGT-004
agent_name: standard_compliance
trigger_skills: [ATS-004 编码校验]
responsibility: 国标/行标/地方标准合规校验
input_artifacts: [数据, 标准引用]
output_artifacts: [合规报告, 不合规清单]
```

### 5. 文档生成 Agent (Doc Generator)

```yaml
agent_id: AGT-005
agent_name: doc_generator
trigger_skills: [ATS-010 项目归档]
responsibility: 元数据/质检报告/成果文档/归档清单自动生成
input_artifacts: [各阶段产出物]
output_artifacts: [元数据文件, 项目报告, 归档目录]
```

---

## 工序准入/阻断规则

| 当前阶段 | 前置准入凭证 | 缺失时行为 |
|---------|------------|-----------|
| 坐标转换 | 数据探查报告 | 🔴 阻断，等待探查完成 |
| 拓扑修复 | 统一坐标系数据 | 🔴 阻断 |
| 编码校验 | 无拓扑错误数据 | 🔴 阻断 |
| 质检 | 国标分层数据 | 🔴 阻断 |
| 元数据 | 质检通过数据 | 🔴 阻断 |
| 归档 | 全部成果文件 | 🔴 阻断 |

---

## 调度策略

| 场景 | 策略 | 说明 |
|------|------|------|
| 单图层处理 | 串行 | 7阶段顺序执行 |
| 多图层同质 | 并行 | 每图层独立Agent处理 |
| 多源融合 | 混合 | 同类数据并行→融合串行 |
| 百万级数据 | 分批 | 分块→并行→合并 |
