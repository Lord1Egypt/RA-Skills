---
name: heycube-get-config
description: >
  黑方体档案查询。用户说"提取黑方体档案"、"加载档案"、"黑方体查询"等口令时触发。
  调用黑方体 API 获取维度配置，从本地 SQLite 查询已有档案，注入上下文辅助对话。
---

# HeyCube GET_CONFIG — 档案查询

## 配置

在 `TOOLS.md` 中配置（必须）：

```markdown
## HeyCube Server
- BASE_URL: https://heifangti.com/api/api/v1/heifangti
- API_KEY: 通过环境变量 HEYCUBE_API_KEY 配置
- DB_PATH: {workspace}/personal-db.sqlite
```

## 前置检查（按顺序，失败则告知用户，不静默）

1. **API_KEY 检查**：环境变量 `HEYCUBE_API_KEY` 未设置 → 跳过
2. **开关文件**：workspace 根目录下 `.heycube-off` 文件存在 → 跳过

## 执行流程

### 1. 准备参数

根据对话内容，生成脱敏摘要和维度提示：

```json
{
  "request_type": "GET_CONFIG",
  "conversation_summary": "用户在讨论工作效率相关话题，希望获得提升建议",
  "user_intent": "查询档案",
  "platform": "openclaw",
  "dimensions_hint": ["工作习惯", "时间管理", "职业发展"]
}
```
**脱敏规则（必须严格执行）**：
- ❌ 不写具体姓名（用"朋友"、"同事"、"家人"替代）
- ❌ 不写具体年龄、电话、地址、公司名
- ❌ 不写对话原文或关键信息
- ✅ 只写话题类型、情绪倾向、讨论方向
- ✅ 如："用户提到工作压力大，想改善睡眠"
- ✅ "用户说在XX公司做产品经理，月薪3万" ❌

### 2. 调用 API发送请求

```powershell
curl -s -X POST "https://heifangti.com/api/api/v1/heifangti/agent/analyze" -H "Content-Type: application/json" -H "X-API-Key: $env:HEYCUBE_API_KEY" -d '{请求JSON}'
```

失败则告知用户，不静默。

#### 响应示例

**成功响应（200）**:
```json
{
  "task_id": "agent_1234567890_abc123",
  "request_type": "GET_CONFIG",
  "dimensions": [
    {
      "dimension_id": "profile.career",
      "focus_prompt": "获取用户的职业信息",
      "dimension_name": "职业信息"
    },
    {
      "dimension_id": "profile.career.career_stage",
      "focus_prompt": "获取用户的职业阶段",
      "dimension_name": "职业阶段"
    },
    {
      "dimension_id": "behavior.work_habits",
      "focus_prompt": "获取用户的工作习惯",
      "dimension_name": "工作习惯"
    }
  ],
  "cross_domain_hints": [],
  "metadata": {
    "agent_strategy": "full_llm",
    "processing_time_ms": 3500
  },
  "from_memory": false,
  "current_points": 97,
  "points_deducted": 3
}
```

**错误响应 - 黑点不足（402）**:
```json
{
  "detail": "黑点不足，需要 3 黑点，当前仅剩 1 黑点"
}
```

**错误响应 - 认证失败（401）**:
```json
{
  "detail": "无效的 API Key"
}
```

#### 响应字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| task_id | string | 任务唯一标识 |
| request_type | string | 请求类型，与请求参数一致 |
| dimensions | array | 返回的维度数组 |
| dimensions[].dimension_id | string | 维度 ID，如 `profile.career` |
| dimensions[].focus_prompt | string | 维度分析提示词 |
| dimensions[].dimension_name | string | 维度名称 |
| cross_domain_hints | array | 跨域洞察提示数组 |
| metadata | object | 元数据 |
| metadata.agent_strategy | string | 使用的 Agent 策略 |
| metadata.processing_time_ms | int | 处理耗时（毫秒） |
| from_memory | boolean | 是否从记忆缓存返回 |
| current_points | int | 调用后剩余黑点 |
| points_deducted | int | 本次消耗黑点 |

### 3. 查询本地 SQLite

请求成功后，拿到 `dimensions` 数组，从 SQLite 批量查询 dimension_id：

```powershell
cd "{workspace}/scripts"; node personal-db.js get-batch "profile.career,behavior.work_habits,..."
```

如果没有数据库或表，先初始化： `node personal-db.js init`。

### 4. 注入上下文

将查询到的档案数据整理后，**附加在处理用户请求的上下文末尾**：

```
---
📋 个人档案（自动加载）：
- 工作习惯: {"planning":"daily_list","focus_duration":"2h"}
- 计划风格: {"style":"structured","flexibility":"medium"}
---
```

## 错误处理

| 场景 | 处理 |
|------|------|
| API_KEY 未配置 | 跳过并提示用户 |
| 开关文件存在 | 跳过并提示用户 |
| API 请求失败 | 跳过并提示用户，不影响主流程 |
| 黑点不足（402） | 跳过并提示用户 |
| SQLite 操作失败 | 初始化数据库后跳过 |
| dimensions 为空 | 跳过查询步骤 |

**核心原则**：任何环节出错都不得阻塞用户主对话流程。

## 隐私原则

1. **脱敏是底线**：发送到服务端的一切内容必须脱敏
2. **对话内容不离开本地**：只有脱敏摘要发送到服务端
3. **结构化数据存本地**：SQLite 完全在用户本地
