# Skills API 文档

本文档定义了 MaskClaw 框架中三大核心 Skills 的输入输出契约。

## 目录

- [1. Smart Masker](#1-smart-masker)
- [2. Behavior Monitor](#2-behavior-monitor)
- [3. Skill Evolution](#3-skill-evolution)

---

## 1. Smart Masker

**智能视觉打码模块**，基于 RapidOCR 识别敏感文本区域并进行视觉脱敏处理。

### 1.1 类：`VisualMasker`

```python
from skills.smart_masker import VisualMasker

masker = VisualMasker()
result = masker.process_image(image_path, sensitive_keywords)
```

### 1.2 方法

#### `process_image(image_path, sensitive_keywords, method='blur')`

对图片中的敏感区域进行打码处理。

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:---:|:---|
| `image_path` | `str` | ✅ | 图片路径或 Base64 编码的图片 |
| `sensitive_keywords` | `List[str]` | ✅ | 敏感关键词列表 |
| `method` | `str` | ❌ | 打码方式：`blur`（高斯模糊，默认）/ `mosaic`（马赛克）/ `block`（色块） |

### 1.3 返回值

```json
{
  "success": true,
  "masked_image_path": "temp/masked_xxx.jpg",
  "detected_regions": [
    {
      "text": "13812345678",
      "bbox": [x1, y1, x2, y2],
      "keyword_matched": "手机号"
    }
  ],
  "regions_count": 1,
  "processing_time_ms": 45
}
```

### 1.4 核心能力

| 能力 | 说明 |
|:-----|:-----|
| **RapidOCR 识别** | 高性能 OCR 引擎，毫秒级文本检测与识别 |
| **语义相似匹配** | 支持模糊匹配，关键词部分匹配也能识别 |
| **多种打码方式** | 高斯模糊、马赛克、色块覆盖 |
| **坐标精确定位** | 返回打码区域坐标，便于后续处理 |

### 1.5 示例

```python
from skills.smart_masker import VisualMasker

masker = VisualMasker()

# 敏感关键词列表
keywords = ["手机号", "身份证", "银行卡", "密码"]

# 处理图片
result = masker.process_image(
    image_path="test.jpg",
    sensitive_keywords=keywords,
    method="blur"
)

print(f"检测到 {result['regions_count']} 个敏感区域")
print(f"脱敏图片已保存至: {result['masked_image_path']}")
```

---

## 2. Behavior Monitor

**行为监控模块**，标准化所有事件到共享 Schema，捕获用户参与的操作行为。

### 2.1 类：`BehaviorMonitor`

```python
from skills.behavior_monitor import BehaviorMonitor

monitor = BehaviorMonitor()
```

### 2.2 日志类型

| 类型 | 说明 |
|:-----|:-----|
| `behavior_log.jsonl` | 用户未参与的操作日志（level=1） |
| `correction_log.jsonl` | 用户参与的操作日志（level=2） |
| `session_trace.jsonl` | 结构化行为链（v2.0 新格式） |

### 2.3 核心方法

#### `log_action_to_chain(...)`

记录一次行为事件到结构化行为链。

```python
from skills.behavior_monitor import log_action_to_chain

# 记录 Agent 操作
log_action_to_chain(
    user_id="user_001",
    action="share_or_send",
    resolution="block",
    scenario_tag="钉钉发送病历截图",
    app_context="钉钉",
    field="medical_record",
    pii_type="MedicalRecord",
    relationship_tag="同事",
    correction_type="user_denied",
    auto_flush=True,
)
```

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:---:|:---|
| `user_id` | `str` | ✅ | 用户标识 |
| `action` | `str` | ✅ | 操作类型 |
| `resolution` | `str` | ✅ | 决策结果 |
| `scenario_tag` | `str` | ✅ | 场景标签（行为链唯一识别） |
| `app_context` | `str` | ❌ | 应用上下文 |
| `field` | `str` | ❌ | 字段名 |
| `pii_type` | `str` | ❌ | PII 类型 |
| `relationship_tag` | `str` | ❌ | 关系标签 |
| `correction_type` | `str` | ❌ | 纠错类型 |
| `auto_flush` | `bool` | ❌ | 是否自动持久化（纠错时自动 True） |

### 2.4 纠错类型

| 类型 | 说明 |
|:-----|:-----|
| `user_denied` | 用户明确不想要这个操作 |
| `user_modified` | 用户有具体偏好，信号最强 |
| `user_interrupted` | 用户主动介入，行为意图最明确 |

### 2.5 决策类型

| 决策 | 说明 | 系统行为 |
|:----:|:-----|:---------|
| `allow` | 安全操作 | 直接放行 |
| `block` | 风险操作 | 直接拦截 |
| `mask` | 需脱敏 | 执行打码后放行 |
| `ask` | 不确定 | 主动向用户确认 |
| `defer` | 延迟 | 等待进一步确认 |
| `interrupt` | 中断 | 停止当前操作 |
| `correction` | 纠错 | 用户参与的纠错 |

### 2.6 风险等级

| 等级 | 说明 |
|:----:|:-----|
| `H` | High Risk，高风险 |
| `S` | Standard Risk，中风险 |
| `N` | Normal Risk，低风险 |

### 2.7 返回值

```json
{
  "chain_id": "user_001_钉钉发送病历_1700000001",
  "action_count": 2,
  "has_correction": true,
  "correction_count": 1,
  "final_resolution": "correction"
}
```

---

## 3. Skill Evolution

**SOP 自进化模块**，基于爬山法持续优化 SOP（标准操作流程）。

### 3.1 核心流程（爬山法）

```
┌─────────────────────────────────────────────────────────────┐
│  第 1 步：agent 对 skill 做一个小改动                       │
│         （比如：加一条"必须核对输入数据"的规则）               │
├─────────────────────────────────────────────────────────────┤
│  第 2 步：用改动后的 skill 跑 10 个测试用例                  │
├─────────────────────────────────────────────────────────────┤
│  第 3 步：用 checklist 给每个输出打分                         │
│         （4 个检查项全过 = 100 分，3 个过 = 75 分...）        │
├─────────────────────────────────────────────────────────────┤
│  第 4 步：算平均分                                          │
│         - 比上一轮高 → 保留改动                              │
│         - 比上一轮低 → 撤销改动                              │
├─────────────────────────────────────────────────────────────┤
│  第 5 步：重复，直到连续 3 轮分数超过 90% 或你喊停           │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 子模块

| 模块 | 说明 |
|:-----|:-----|
| **SemanticEvaluator** | LLM-as-a-Judge，快速验证逻辑 |
| **ChecklistEvaluator** | 4项检查评分 |
| **FinalSandbox** | 严格验证后发布 |

### 3.3 数据库表

| 表名 | 说明 |
|:-----|:-----|
| `session_trace` | 会话轨迹 |
| `sop_draft` | SOP 草稿（多轮迭代） |
| `sop_version` | 已发布版本 |

### 3.4 核心方法

#### `run_pipeline(user_id, draft_name, step='all')`

完整 SOP 进化流水线。

```python
from skills.evolution_mechanic import SOPEvolution

engine = SOPEvolution()

result = engine.run_pipeline(
    user_id="user_001",
    draft_name="钉钉隐私规则",
    app_context="钉钉",
    task_goal="安全发送工作消息",
    step="all",  # rebuild/init/evolve/sandbox/publish/all
)
```

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|:-----|:-----|:---:|:---|
| `user_id` | `str` | ✅ | 用户标识 |
| `draft_name` | `str` | ✅ | 草稿名称 |
| `app_context` | `str` | ❌ | 应用上下文 |
| `task_goal` | `str` | ❌ | 任务目标 |
| `step` | `str` | ❌ | 流水线步骤 |

**步骤说明：**

| 步骤 | 说明 |
|:-----|:-----|
| `rebuild` | 重建会话轨迹 |
| `init` | 初始化草稿 |
| `evolve` | 爬山法进化 |
| `sandbox` | 沙盒验证 |
| `publish` | 发布 |
| `all` | 完整流程 |

### 3.5 返回值

```json
{
  "success": true,
  "evolve": {
    "total_iterations": 5,
    "final_score": 92.5,
    "reached_threshold": true,
    "terminated_reason": "consecutive_high"
  },
  "sandbox": {
    "passed": true,
    "report": {"test_count": 10}
  },
  "publish": {
    "skill_name": "dingtalk-privacy-rule",
    "version": "v1.0.0"
  }
}
```

### 3.6 进化阶段

| 阶段 | 说明 |
|:-----|:-----|
| `init` | 初始化 |
| `diagnose` | 诊断 |
| `mutate` | 变异 |
| `test` | 测试 |
| `evaluate` | 评估 |
| `evolving` | 进化中 |
| `sandbox` | 沙盒验证 |
| `ready` | 就绪待发布 |
| `published` | 已发布 |
| `failed` | 失败 |

---

## 五级置信度判决

| 判决 | 条件 | 系统行为 |
|:---:|:-----|:---------|
| **Allow** | 规则库完整匹配，安全 | 直接放行 |
| **Block** | 规则库完整匹配，风险明确 | 直接拦截 |
| **Mask** | 规则库完整匹配，需脱敏 | 执行打码后放行 |
| **Ask** | 规则库信息不完整 | 主动向用户确认 |
| **Unsure** | 新场景无记录 | 标记并等待用户教授 |

---

## 错误码

| 错误码 | 说明 | 处理建议 |
|:------:|:-----|:---------|
| `MASK_001` | 图片解码失败 | 检查图片格式 |
| `MASK_002` | 图片过大 | 压缩后重试 |
| `MASK_003` | OCR 识别失败 | 检查图片质量 |
| `MONITOR_001` | 日志写入失败 | 检查存储权限 |
| `EVOLUTION_001` | 规则生成失败 | 减少测试用例批次 |
| `EVOLUTION_002` | 沙盒测试超时 | 检查测试环境 |
