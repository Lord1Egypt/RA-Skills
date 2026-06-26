---
name: model-usage-stats
description: 模型消耗统计技能，用于统计和展示不同会话、不同模型的 token 使用量、成本统计和消耗报告，通过飞书消息卡片进行可视化展示。当用户请求查看模型消耗、token 统计、成本分析或消耗报告时使用。
---

# 模型消耗统计技能

统计和展示模型（LLM）的使用情况，包括 token 消耗、成本分析和消耗报告。

## 快速开始

使用此技能时，请按照以下流程操作：

1. **确认查询类型**
   - 当前会话统计
   - 历史会话统计
   - 按模型分组统计
   - 导出消耗报告

2. **获取会话数据**
   - 使用 `session_status` 工具获取当前会话信息
   - 使用 `sessions_list` 和 `sessions_history` 获取历史会话

3. **计算统计指标**
   - 输入 Token（input tokens）
   - 输出 Token（output tokens）
   - 总 Token 数量
   - 成本（如果使用付费模型）

4. **通过飞书展示结果**
   - 使用 `message` 工具发送富文本消息卡片
   - 使用表格展示数据
   - 使用摘要和图表说明

## 核心指标

### Token 消耗
- **输入 Token（input tokens）**: 接收到的文本（系统提示、对话历史、用户消息）
- **输出 Token（output tokens）**: 生成的回复内容
- **总 Token 数量**: input + output

### 成本计算
根据模型定价计算成本：
- `zai/glm-4.7-flash`: 约 $0.0001/1K input, $0.0003/1K output
- `stepfun/step-3.5-flash`: 约 $0.0000/1K input, $0.0000/1K output（免费）
- `ollama/gemma4:26b-a4b-it-q4_K_M`: 约 $0.0000/1K（本地运行，免费）

### 成本公式
```
总成本 = (输入 Token 数量 / 1000) × 输入单价 + (输出 Token 数量 / 1000) × 输出单价
```

## 使用流程

### 1. 查看当前会话消耗

```bash
# 获取当前会话状态
session_status(sessionKey="当前会话的 session key")

# 分析数据
- 总输入 Token
- 总输出 Token
- 总 Token 数量
- 总成本
```

### 2. 查看历史会话消耗

```bash
# 列出所有会话
sessions_list(limit=50)

# 获取会话详情
sessions_history(sessionKey="会话 ID", limit=100)

# 按时间范围筛选
sessions_list(activeMinutes=1440)  # 最近 24 小时
sessions_list(activeMinutes=10080) # 最近 7 天
```

### 3. 按模型分组统计

从历史会话数据中提取模型信息：
- `zai/glm-4.7-flash`
- `stepfun/step-3.5-flash`
- `ollama/gemma4:26b-a4b-it-q4_K_M`

分别统计：
- 各模型的总 Token 数量
- 各模型的成本
- 各模型的使用次数
- 各模型占总消耗的百分比

### 4. 导出消耗报告

生成结构化报告，包含：
- 总体摘要（总 Token、总成本）
- 按时间范围统计（最近 1 天/7 天/30 天）
- 按模型分组统计
- 按会话分组统计（Top 10）
- 成本趋势分析

## 飞书消息卡片格式

### 摘要卡片

```markdown
## 📊 模型消耗统计

**总 Token 数量**: {total_tokens}
**总成本**: ${total_cost}
**会话数量**: {session_count}

### 📈 按模型分组

| 模型 | Token 数量 | 成本 | 占比 |
|------|-----------|------|------|
| {model1} | {tokens1} | ${cost1} | {percent1}% |
| {model2} | {tokens2} | ${cost2} | {percent2}% |
```

### 历史会话卡片

```markdown
## 📜 历史会话消耗（最近 {days} 天）

### 总体摘要
- **总 Token**: {total_tokens}
- **总成本**: ${total_cost}
- **活跃会话**: {session_count}

### Top 5 会话
| 排名 | 会话 ID | Token 数量 | 模型 | 成本 |
|------|---------|-----------|------|------|
| 1 | {session1} | {tokens1} | {model1} | ${cost1} |
| 2 | {session2} | {tokens2} | {model2} | ${cost2} |
```

### 详细报告卡片

```markdown
## 📋 消耗报告（{start_date} - {end_date}）

### 1. 总体统计
{overall_summary}

### 2. 按模型统计
{by_model}

### 3. 按会话统计
{by_session}

### 4. 成本分析
{cost_analysis}

---
**生成时间**: {generation_time}
**数据来源**: OpenClaw 会话记录
```

## 常见查询场景

### 场景 1: "查看当前会话消耗"

```markdown
## 📊 当前会话消耗统计

**会话 ID**: {session_id}
**运行模型**: {model_name}
**开始时间**: {start_time}

### Token 使用情况
- **输入 Token**: {input_tokens}
- **输出 Token**: {output_tokens}
- **总 Token**: {total_tokens}

### 成本统计
- **总成本**: ${total_cost}

### 会话统计
- **消息数量**: {message_count}
- **平均每条消息 Token**: {avg_tokens_per_message}
```

### 场景 2: "查看最近 7 天的消耗统计"

```markdown
## 📊 最近 7 天模型消耗统计

**统计范围**: 2026-04-06 - 2026-04-13

### 总体摘要
- **总 Token 数量**: {total_tokens}
- **总成本**: ${total_cost}
- **活跃会话**: {session_count}

### 按模型分组
{model_table}

### Top 10 会话
{top_sessions_table}
```

### 场景 3: "按模型对比成本"

```markdown
## 🆚 模型成本对比

### 成本汇总
| 模型 | 使用次数 | 总 Token | 总成本 |
|------|---------|---------|--------|
| zai/glm-4.7-flash | {count1} | {tokens1} | ${cost1} |
| stepfun/step-3.5-flash | {count2} | {tokens2} | ${cost2} |
| ollama/gemma4:26b | {count3} | {tokens3} | ${cost3} |

### 成本占比
{cost_pie_chart}

### 推荐使用
根据成本和性能，推荐：
- **成本敏感**: ollama/gemma4:26b（本地运行，免费）
- **高性能**: zai/glm-4.7-flash（速度快，成本合理）
- **快速原型**: stepfun/step-3.5-flash（免费，快速）
```

### 场景 4: "导出消耗报告"

生成文本文件，包含完整数据：

```
模型消耗统计报告
================
生成时间: 2026-04-13 10:52:00
统计范围: 2026-04-06 - 2026-04-13

1. 总体统计
   总 Token: {total_tokens}
   总成本: ${total_cost}
   会话数量: {session_count}

2. 按模型统计
   zai/glm-4.7-flash:
     - 使用次数: {count1}
     - 总 Token: {tokens1}
     - 总成本: ${cost1}

3. 按会话统计（Top 10）
   {session_list}

4. 成本趋势
   {cost_trend}
```

## 成本定价参考

### 云端模型
| 模型 | 输入单价 | 输出单价 | 备注 |
|------|---------|---------|------|
| zai/glm-4.7-flash | $0.0001/1K | $0.0003/1K | 快速响应 |
| stepfun/step-3.5-flash | $0.0000/1K | $0.0000/1K | 免费 |

### 本地模型
| 模型 | 成本 | 备注 |
|------|------|------|
| ollama/gemma4:26b-a4b-it-q4_K_M | $0.0000 | 本地运行，免费 |
| ollama/qwen3.5:27b-q4_K_M | $0.0000 | 本地运行，免费 |
| ollama/qwen3.5:9b-q4_K_M | $0.0000 | 本地运行，免费 |

## 注意事项

1. **Token 计算准确性**: 使用 `session_status` 工具获取准确的 token 数据
2. **成本估算**: 根据实际使用的模型定价计算成本
3. **数据范围**: 明确查询的时间范围（最近 1 天/7 天/30 天/全部）
4. **飞书格式**: 使用富文本表格和格式化，确保展示清晰
5. **隐私保护**: 不泄露敏感信息，只展示统计数据

## 示例输出

```markdown
## 📊 模型消耗统计（最近 7 天）

**统计范围**: 2026-04-06 - 2026-04-13
**总 Token**: 1,523,450
**总成本**: $0.457
**活跃会话**: 23

### 按模型分组

| 模型 | Token 数量 | 成本 | 占比 |
|------|-----------|------|------|
| zai/glm-4.7-flash | 1,200,000 | $0.360 | 78.8% |
| stepfun/step-3.5-flash | 200,000 | $0.000 | 13.1% |
| ollama/gemma4:26b | 123,450 | $0.000 | 8.1% |

### Top 5 会话

| 排名 | 会话 ID | Token 数量 | 模型 | 成本 |
|------|---------|-----------|------|------|
| 1 | 91e404e8-2ebf-4abb-b0e9-2bbb8d14d61f | 450,000 | zai/glm-4.7-flash | $0.135 |
| 2 | 6af34b70-9b36-43f8-b7a6-d632d3f0a3f9 | 300,000 | zai/glm-4.7-flash | $0.090 |
| 3 | 116d1d76-ead4-41a9-857e-57899eb58386 | 250,000 | zai/glm-4.7-flash | $0.075 |
| 4 | b738c0e4-e3e0-46ab-987a-182a1b93be5e | 150,000 | zai/glm-4.7-flash | $0.045 |
| 5 | 27be1e65-5959-4843-8077-4bd55f12b525 | 173,450 | zai/glm-4.7-flash | $0.052 |

---
**生成时间**: 2026-04-13 10:52:00
```

## 辅助函数

### 计算成本
```python
def calculate_cost(input_tokens, output_tokens, model):
    # 根据模型定价计算成本
    if model == "zai/glm-4.7-flash":
        input_cost = input_tokens / 1000 * 0.0001
        output_cost = output_tokens / 1000 * 0.0003
    elif model == "stepfun/step-3.5-flash":
        return 0  # 免费
    elif model.startswith("ollama"):
        return 0  # 本地运行，免费
    else:
        return 0

    return input_cost + output_cost
```

### 格式化数字
```python
def format_number(num):
    # 格式化为千分位
    return "{:,}".format(int(num))
```

### 生成成本占比饼图
使用飞书消息卡片，可以手动绘制简单的饼图或使用文本表示：
```
zai/glm-4.7-flash: ████░░░░░░░░░░░░░░░░░░ 78.8%
stepfun/step-3.5-flash: ██░░░░░░░░░░░░░░░░░░ 13.1%
ollama/gemma4:26b: █░░░░░░░░░░░░░░░░░░░░░ 8.1%
```
