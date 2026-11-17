# 完整使用示例

## 示例 1：竞品分析报告流水线

### 场景

采集竞品信息 → 分析优劣势 → 生成报告

### DAG 定义

```json
{
  "pipeline_name": "竞品分析报告",
  "version": "1.0",
  "agents": [
    {
      "id": "scraper",
      "name": "竞品信息采集",
      "role": "采集3个竞品的定价、功能、用户评价信息",
      "inputs": ["competitor_list"],
      "outputs": ["competitor_raw_data"],
      "depends_on": [],
      "retry": 3,
      "timeout": 90,
      "fallback": "skip"
    },
    {
      "id": "analyzer",
      "name": "竞品分析",
      "role": "对比分析各竞品的优劣势，输出SWOT分析",
      "inputs": ["competitor_raw_data"],
      "outputs": ["swot_analysis", "competitive_landscape"],
      "depends_on": ["scraper"],
      "retry": 2,
      "timeout": 120,
      "fallback": "default",
      "default_value": {"swot_analysis": "数据不足", "competitive_landscape": {}}
    },
    {
      "id": "reporter",
      "name": "报告生成",
      "role": "生成竞品分析报告，包含对比表格和战略建议",
      "inputs": ["swot_analysis", "competitive_landscape"],
      "outputs": ["report"],
      "depends_on": ["analyzer"],
      "retry": 1,
      "timeout": 180,
      "fallback": "abort"
    }
  ]
}
```

### 执行流程

```bash
# 1. 查看执行计划
python orchestrator.py plan competitor_analysis.json

# 2. 初始化
python orchestrator.py run competitor_analysis.json

# 3. 逐步执行
python orchestrator.py step state.json
# AI 执行 scraper 任务...
python state_store.py complete state.json scraper '{"competitor_raw_data": "..."}'

python orchestrator.py step state.json
# AI 执行 analyzer 任务...
python state_store.py complete state.json analyzer '{"swot_analysis": "...", "competitive_landscape": "..."}'

python orchestrator.py step state.json
# AI 执行 reporter 任务...
python state_store.py complete state.json reporter '{"report": "..."}'

# 4. 生成报告
python orchestrator.py report state.json
```

---

## 示例 2：数据处理流水线（含错误恢复）

### 场景

数据采集 → 清洗 → 分析 → 可视化，其中清洗节点可能失败

### 执行过程

```bash
# 初始化并开始
python orchestrator.py run data_pipeline.json

# Step 1: 采集成功
python orchestrator.py step state.json
python state_store.py complete state.json collector '{"raw_data": "采集到的1000条记录"}'

# Step 2: 清洗失败
python orchestrator.py step state.json
python state_store.py fail state.json cleaner "数据格式异常，无法解析第523行"

# Step 2.1: 重试（第1次）
python error_recovery.py retry state.json cleaner "数据格式异常"
# 等待2秒...

# Step 2.2: 重试（第2次，达到最大重试次数2）
python error_recovery.py retry state.json cleaner "仍然失败"
# 引擎自动进入降级策略

# Step 2.3: 使用默认值降级
# cleaner 的 fallback 为 "default"，自动使用 default_value
# 下游 analyzer 收到默认值继续执行

# Step 3: 分析成功
python orchestrator.py step state.json
python state_store.py complete state.json analyzer '{"analysis_result": "..."}'

# Step 4: 生成报告
python orchestrator.py report state.json
# 报告中会标注 cleaner 节点使用了默认值降级
```

---

## 示例 3：断点续传

### 场景

流水线在第3个节点失败中止，修复后从断点继续

```bash
# 查看当前状态
python orchestrator.py status state.json
# 输出：
#   ✅ [collector] 数据采集 - completed
#   ✅ [cleaner] 数据清洗 - completed
#   ❌ [analyzer] 数据分析 - failed (重试 2/2)
#   ⏳ [reporter] 报告生成 - pending

# 分析下游影响
python orchestrator.py impact state.json analyzer
# 输出：受影响节点：reporter

# 修复问题后，断点续传
python orchestrator.py resume state.json
# 输出：重置失败节点 1 个

# 继续执行
python orchestrator.py step state.json
# analyzer 重新执行
python state_store.py complete state.json analyzer '{"analysis_result": "..."}'

python orchestrator.py step state.json
# reporter 执行
python state_store.py complete state.json reporter '{"report": "..."}'

# 生成最终报告
python orchestrator.py report state.json
```
