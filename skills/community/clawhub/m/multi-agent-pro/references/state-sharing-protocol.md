# 状态共享协议

## 概述

本文档定义多Agent协作编排引擎中，Agent 节点之间如何通过 `pipeline_state.json` 进行状态共享和数据传递。

---

## 状态文件结构

```
pipeline_state.json
├── pipeline_id        # 流水线唯一标识
├── pipeline_name      # 流水线名称
├── status             # 总体状态: initialized/running/completed/aborted
├── created_at         # 创建时间
├── updated_at         # 最后更新时间
└── nodes              # 节点状态映射表
    ├── [node_id]
    │   ├── name           # 节点名称
    │   ├── role           # 角色描述
    │   ├── status         # pending/running/completed/failed/skipped
    │   ├── depends_on     # 依赖节点列表
    │   ├── retry_count    # 已重试次数
    │   ├── max_retry      # 最大重试次数
    │   ├── timeout        # 超时秒数
    │   ├── fallback       # 降级策略
    │   ├── inputs         # 输入参数名列表
    │   ├── outputs        # 输出参数名列表
    │   ├── output_data    # 实际输出数据（JSON 对象）
    │   ├── error          # 错误信息（失败时）
    │   ├── started_at     # 开始执行时间
    │   └── completed_at   # 完成时间
    └── ...
```

---

## 数据传递机制

### 上游 → 下游

当节点 A 完成执行后，其输出保存在 `nodes.A.output_data`。当下游节点 B 开始执行时，引擎自动将 A 的 `output_data` 注入 B 的上下文。

```
[A: collector] output_data: {"raw_data": "..."}
                    ↓ 自动注入
[B: analyzer]  收到: {"collector": {"raw_data": "..."}}
```

### 多上游汇聚

如果 B 依赖 A 和 C，则 B 收到的注入数据为：

```json
{
  "collector": {"raw_data": "..."},
  "cleaner": {"cleaned_data": "..."}
}
```

### 输出数据格式

`output_data` 是一个 JSON 对象，key 对应 DAG 定义中的 `outputs` 字段：

```json
// DAG 定义
{
  "id": "analyzer",
  "outputs": ["analysis_result", "key_metrics"]
}

// 执行后的 output_data
{
  "analysis_result": "市场增长率为12.5%...",
  "key_metrics": {"growth_rate": 12.5, "market_size": "500亿"}
}
```

---

## 完成节点

当 AI 执行完一个节点的任务后，需要将输出保存到状态文件：

```bash
python state_store.py complete pipeline_state.json collector '{"raw_data": "采集到的原始数据..."}'
```

输出数据必须是合法的 JSON 字符串。如果不提供输出，默认保存 `{"result": "completed"}`。

---

## 失败节点

当节点执行失败时：

```bash
python state_store.py fail pipeline_state.json collector "API 连接超时"
```

引擎会记录错误信息并增加重试计数。如果未达到最大重试次数，可以通过 `error_recovery.py retry` 重试。

---

## 跳过节点

当降级策略为 `skip` 时，节点被标记为 `skipped`，其 `output_data` 设为：

```json
{"skipped": true, "reason": "错误信息"}
```

下游节点会收到这个跳过标记，可以根据此判断是否继续处理。

---

## 状态转换

```
pending → running → completed
                 ↘ failed → pending (重试)
                         ↘ skipped (降级: skip)
                         ↘ completed (降级: default)
                         ↘ aborted (降级: abort)
```

---

## 最佳实践

1. **输出数据保持精简**：单节点输出超过 10MB 时建议写入独立文件，`output_data` 中只存文件路径
2. **输出字段与定义一致**：`output_data` 的 key 应与 DAG 中的 `outputs` 字段对应
3. **敏感数据脱敏**：不要将 API Key、密码等敏感信息存入 `output_data`
4. **及时标记状态**：AI 执行完任务后立即调用 `complete` 或 `fail`，确保状态文件是最新的
