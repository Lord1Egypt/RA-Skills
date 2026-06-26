---
name: heycube-update-data
description: >
  黑方体档案存入。用户说"存入黑方体档案"、"保存档案"、"黑方体记录"等口令时触发。
  脱敏总结当前对话，调用黑方体 API 获取更新维度，根据维度提取数据并写入本地 SQLite。
---

# HeyCube UPDATE_DATA — 档案存入

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
3. **对话分类**：分类当前对话（见下方表格），判断是否可以更新档案

## 对话分类

先判断本次对话是否值得存档

| 类型 | 触发分析 | 说明 |
|------|:---:|------|
| `TASK` | ❌ | 技术问题、文件操作、信息查询、纯工具使用 |
| `CHITCHAT` | ❌ | 日常寒暄、无深层信息的对话 |
| `SELF_EXPRESS` | ✅ | 用户表达想法、观点、经历、身份认知 |
| `EMOTION_RELEASE` | ✅ | 用户表达情绪、倾诉、抱怨、发泄 |
| `VALUE_DISCUSS` | ✅ | 讨论对错、好坏、重要与否、意义 |
| `DECISION_TALK` | ✅ | 讨论做不做、怎么选、权衡利弊 |
| `RELATIONSHIP` | ✅ | 提到他人、关系、互动模式 |
| `GOAL_PLAN` | ✅ | 谈论未来计划、愿景、期望 |
| `REFLECTION` | ✅ | 回顾过去、总结经验、自我评价 |

> 即使是 TASK 类型，如包含与用户自身相关的片段，也可适当触发。

## 执行流程

### 1. 准备参数

对本次对话生成脱敏摘要（只写话题类型和情绪倾向，不含个人信息）：

```json
{
  "request_type": "UPDATE_DATA",
  "conversation_summary": "用户分享了最近的工作压力和应对方式",
  "user_intent": "倾诉与记录",
  "platform": "openclaw",
  "dimensions_hint": ["压力应对", "工作习惯", "心理健康"]
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

失败则告知用户。

#### 响应示例

**成功响应（200）**:
```json
{
  "task_id": "agent_1234567890_abc123",
  "request_type": "UPDATE_DATA",
  "dimensions": [
    {
      "dimension_id": "behavior.stress_response",
      "focus_prompt": "提取用户的压力应对方式",
      "dimension_name": "压力应对"
    },
    {
      "dimension_id": "behavior.sleep_quality",
      "focus_prompt": "提取用户的睡眠质量情况",
      "dimension_name": "睡眠质量"
    }
  ],
  "cross_domain_hints": ["建议关注用户的工作与生活平衡"],
  "metadata": {
    "agent_strategy": "use_memory",
    "processing_time_ms": 2100
  },
  "from_memory": true,
  "current_points": 94,
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
| dimensions | array | 返回的需要更新的维度数组 |
| dimensions[].dimension_id | string | 维度 ID，如 `behavior.stress_response` |
| dimensions[].focus_prompt | string | 维度分析提示词，用于指导数据提取 |
| dimensions[].dimension_name | string | 维度名称 |
| cross_domain_hints | array | 跨域洞察提示数组 |
| metadata | object | 元数据 |
| metadata.agent_strategy | string | 使用的 Agent 策略 |
| metadata.processing_time_ms | int | 处理耗时（毫秒） |
| from_memory | boolean | 是否从记忆缓存返回 |
| current_points | int | 调用后剩余黑点 |
| points_deducted | int | 本次消耗黑点 |

### 3. 提取数据 & 写入 SQLite

根据返回的 `dimensions` 数组，每个维度的 `focus_prompt` 作为提取指导，从对话中提取结构化数据。

**提取规则**：
- 值尽量用 JSON 格式
- 只提取有事实依据的信息，不猜测
- 置信度不够的不提取

**写入规则**：

对每个 dimension_id，使用 `merge` 命令（新值覆盖旧值同名字段，保留原有其他字段）：

```powershell
cd "{workspace}/scripts"; node personal-db.js merge "profile.career" "{\"experience\":\"5年\"}"
```

- **数据库中不存在**：`INSERT` 新记录
- **数据库中已存在**：`merge` 合并更新

### 4. 反馈

告知用户存入了哪些维度。

## 错误处理

| 场景 | 处理 |
|------|------|
| API_KEY 未配置 | 跳过并提示用户 |
| 开关文件存在 | 跳过并提示用户 |
| API 请求失败 | 跳过并提示用户，不影响主流程 |
| 黑点不足（402） | 跳过并提示用户 |
| SQLite 操作失败 | 初始化数据库后跳过 |
| dimensions 为空 | 跳过更新步骤 |

**核心原则**：任何环节出错都不得阻塞或干扰用户的主要对话流程。

## 隐私原则

1. **脱敏是底线**：发送到服务端的一切内容必须脱敏
2. **对话内容不离开本地**：只有脱敏摘要发送到服务端
3. **结构化数据存本地**：SQLite 完全在用户本地
