# Prompt Templates 文档

本文档收集了 MaskClaw 框架中使用的 Prompt 模板。

## 1. SOP 生成模板

### 1.1 初始 SOP 生成

```
你是一个手机操作 SOP 编写专家。请为安卓手机上的应用生成标准作业程序（SOP）。

【重要】所有操作都是针对 Android 手机 UI，不是电脑操作。

应用场景：{app_context}
任务目标：{task_goal}

请生成一个符合以下要求的 SOP：
1. **手机操作术语**：使用"点击"、"滑动"、"长按"、"返回"、"切换"等手机操作词汇
2. **清晰的步骤序列**：每个步骤对应一个手机界面动作
3. **每步骤具体动作**：如"点击屏幕底部的发送按钮"、"滑动到下一页"
4. **异常处理提示**：手机特有的异常情况处理

【示例格式】
步骤 1: 打开应用
具体动作：点击手机桌面上的应用图标，进入应用首页
异常处理：若应用未响应，点击"强制停止"后重新打开

请输出完整的手机操作 SOP：
```

### 1.2 SOP 变异模板

```
你是一个手机操作 SOP 优化专家。当前有一个 SOP，你需要对它做小幅改进。

【重要】所有操作都是针对 Android 手机 UI，不是电脑操作。

当前 SOP：
{current_sop}

应用场景：{app_context}
任务目标：{task_goal}

变异要求：
{mutation_hint}

要求：
1. 只做小幅改动，不要全量重写
2. 保持原有逻辑结构
3. 可以添加、删除或修改个别步骤
4. 确保新 SOP 逻辑连贯
5. 所有步骤必须是手机操作

请输出改进后的完整手机操作 SOP：
```

### 1.3 规则提炼模板

```
## 任务：分析当前 SOP/规则的问题并给出改进方向

### 当前上下文
- 应用场景：{app_context}
- 任务目标：{task_goal}
- 迭代轮次：{iteration}

### 当前 SOP 内容
```sop
{current_sop}
```

### 测试结果
- 测试场景数：{total_scenarios}
- 通过数：{passed_scenarios}
- 通过率：{pass_rate}%

### 评估结果
- Checklist 得分：{checklist_score}
- 测试通过率：{test_pass_rate}%
- 综合得分：{final_score}

### 失败的测试场景
{failed_scenarios}

### 原始用户 correction 数据（了解用户真正关心的问题）
{corrections_summary}

---

## 输出要求

请分析上述信息，输出以下 JSON 格式：

```json
{
    "problems": [
        "问题1：SOP 中缺少对 XX 场景的处理",
        "问题2：步骤顺序不够清晰",
        "问题3：异常处理不够完善"
    ],
    "direction": "改进方向：需要加强 XX 方面的描述",
    "next_hint": "mutation_hint: 请在下一轮变异中重点关注..."
}
```

请只输出 JSON，不要有其他内容。
```

## 2. 语义核验模板

### 2.1 LLM-as-a-Judge

```
## 任务：评估 SOP 对给定场景的适用性

### 待评估 SOP
{sop_content}

### 测试场景
```json
{scenario}
```

### 应用上下文
{app_context}

---

## 评估标准

请评估 SOP 是否能正确处理该场景，输出以下 JSON：

```json
{
    "passed": true/false,
    "score": 0-100,
    "reasoning": "评估理由",
    "issues": ["问题1", "问题2"]
}
```

请只输出 JSON。
```

## 3. 规则生成模板

### 3.1 从纠错日志生成规则

```
## 任务：从用户纠错日志提炼隐私保护规则

### 用户信息
- 用户ID: {user_id}
- 应用场景: {app_context}

### 纠错日志
```json
{correction_logs}
```

### 上下文信息
- Agent 尝试的操作: {agent_action}
- 用户修正后的值: {user_correction}
- 敏感数据类型: {pii_types}

---

## 输出要求

基于上述纠错日志，提炼出一条隐私保护规则：

```json
{
    "rule_id": "{user_id}_{timestamp}_{seq}",
    "user_id": "{user_id}",
    "scene": "场景描述",
    "sensitive_field": "敏感字段",
    "strategy": "block/mask/replace",
    "replacement": "替代值（如果有）",
    "rule_text": "规则文本描述",
    "confidence": 0.0-1.0,
    "trigger_count": 触发次数,
    "created_ts": 时间戳
}
```

请只输出 JSON。
```

## 4. 场景分析模板

### 4.1 UI 上下文分析

```
## 任务：分析当前 UI 截图中的敏感信息

### UI 描述
```xml
{ui_xml}
```

### OCR 识别结果
```json
{ocr_results}
```

---

## 分析要求

1. 识别图中可能包含的敏感信息
2. 评估风险等级 (H/S/N)
3. 推荐处理策略 (allow/block/mask/ask)

请输出 JSON：
```json
{
    "sensitive_regions": [
        {"text": "识别的文本", "bbox": [x1,y1,x2,y2], "pii_type": "类型", "risk_level": "H"}
    ],
    "overall_risk": "H/S/N",
    "recommended_strategy": "allow/block/mask/ask"
}
```

请只输出 JSON。
```

## 5. 行为推断模板

### 5.1 用户意图推断

```
## 任务：从用户行为推断隐私偏好

### 行为历史
```json
{behavior_history}
```

### 当前操作
- 操作类型: {action_type}
- 涉及字段: {field}
- Agent 建议值: {proposed_value}

---

## 推断要求

基于历史行为，推断用户对该场景的隐私偏好：

```json
{
    "inferred_preference": "prefer_block/prefer_mask/prefer_allow",
    "confidence": 0.0-1.0,
    "reasoning": "推断理由",
    "recommended_strategy": "block/mask/ask"
}
```

请只输出 JSON。
```

## 6. 使用示例

### 6.1 调用 MiniCPM

```python
import json
from urllib import parse, request, error

def call_minicpm(prompt: str, timeout: int = 180) -> str:
    """调用 MiniCPM API"""
    url = "http://127.0.0.1:8000/chat"
    data = parse.urlencode({"prompt": prompt}).encode("utf-8")
    req = request.Request(url, data=data, method="POST")
    
    try:
        with request.urlopen(req, timeout=timeout) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
            return payload.get("response", "")
    except error.URLError as e:
        raise RuntimeError(f"MiniCPM 请求失败: {e}")

def extract_json(text: str) -> dict:
    """从模型输出中提取 JSON"""
    start = text.find("{")
    end = text.rfind("}")
    if start < 0 or end < 0:
        raise ValueError("模型输出中未找到 JSON")
    return json.loads(text[start:end+1])

# 示例：生成初始 SOP
prompt = INITIAL_SOP_TEMPLATE.format(
    app_context="钉钉",
    task_goal="安全发送工作消息"
)
response = call_minicpm(prompt)
sop_content = response.strip()

# 示例：提炼规则
prompt = RULE_EXTRACTION_TEMPLATE.format(
    user_id="user_001",
    app_context="钉钉",
    correction_logs=json.dumps(corrections),
    agent_action="share_or_send",
    user_correction="user_denied",
    pii_types=["MedicalRecord"]
)
response = call_minicpm(prompt)
rule = extract_json(response)
```
