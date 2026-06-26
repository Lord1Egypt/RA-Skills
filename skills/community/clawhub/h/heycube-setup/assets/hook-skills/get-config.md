---
name: heycube-get-config
description: >
  【不要通过 description 匹配触发此 skill】
  黑方体前置 Hook：对话处理前执行，获取维度配置，从本地 SQLite 档案库填充用户画像到上下文。
  由 AGENTS.md 硬规则驱动，每次有实质内容的对话前自动执行。
---

# HeyCube GET_CONFIG — 对话前置画像加载

本 Skill 在对话处理**之前**执行，从黑方体 API 获取维度配置，从本地 SQLite 查询已有档案，注入上下文。

## 配置

在 `TOOLS.md` 中配置（必须）：

```markdown
### HeyCube Server
- BASE_URL: https://heifangti.com/api/api/v1/heifangti
- API_KEY: hey_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
- DB_PATH: {workspace}/personal-db.sqlite
```

## 前置检查（按顺序，任一失败则静默跳过）

1. **API_KEY 检查**：TOOLS.md 中未配置 API_KEY → 跳过
2. **开关文件**：workspace 根目录下 `.heycube-off` 文件存在 → 跳过

## 执行流程

### 1. 准备参数

根据对话内容，生成脱敏摘要和维度提示：

```json
{
  "request_type": "GET_CONFIG",
  "conversation_summary": "用户在讨论工作效率相关话题，希望获得提升建议",
  "user_intent": "获取建议",
  "platform": "openclaw",
  "dimensions_hint": ["工作习惯", "时间管理", "职业发展"]
}
```

**脱敏规则（必须严格执行）**：
- ❌ 不写具体姓名（用"朋友"、"同事"、"家人"替代）
- ❌ 不写具体年龄、电话、地址、公司名
- ❌ 不写对话原文或关键信息
- ✅ 只写话题类型、情绪倾向、讨论方向
- ✅ 如："用户提到工作压力大，想改善睡眠" ✅ "用户说在XX公司做产品经理，月薪3万" ❌

### 2. 发送请求

```bash
curl -s -X POST "{BASE_URL}/agent/analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: {API_KEY}" \
  -d '{请求JSON}'
```

#### 响应示例

**成功响应（200）**:
```json
{
  "task_id": "agent_1234567890_abc123",
  "request_type": "GET_CONFIG",
  "dimensions": [
    { "dimension_id": "profile.career", "focus_prompt": "获取用户的职业信息", "dimension_name": "职业信息" },
    { "dimension_id": "profile.career.career_stage", "focus_prompt": "获取用户的职业阶段", "dimension_name": "职业阶段" }
  ],
  "cross_domain_hints": [],
  "metadata": { "agent_strategy": "full_llm", "processing_time_ms": 3500 },
  "from_memory": false,
  "current_points": 97,
  "points_deducted": 3
}
```

**错误响应 - 黑点不足（402）**: `{ "detail": "黑点不足，需要 3 黑点，当前仅剩 1 黑点" }`
**错误响应 - 认证失败（401）**: `{ "detail": "无效的 API Key" }`

### 3. 从 SQLite 查询档案

拿到 `dimensions` 数组后，逐个从 SQLite 查询 dimension_id：

```powershell
cd "{workspace}/scripts" && node personal-db.js get-batch "profile.career,behavior.work_habits,..."
```

如果没有数据库或表，先初始化：`cd "{workspace}/scripts" && node personal-db.js init`

### 4. 注入上下文

将档案数据整理后附加在上下文末尾：

```
---
📋 个人档案（自动加载）：
- 工作习惯: {"planning":"daily_list","focus_duration":"2h"}
---
```

## 错误处理

| 场景 | 处理 |
|------|------|
| API_KEY 未配置 | 静默跳过 |
| 开关文件存在 | 静默跳过 |
| API 请求失败 | 静默跳过 |
| 黑点不足（402） | 跳过并提示用户 |
| SQLite 操作失败 | 初始化数据库后跳过 |
| dimensions 为空 | 跳过查询 |

**核心原则**：任何环节出错都不得阻塞用户主对话流程。

## 隐私原则

1. **脱敏是底线**：发送到服务端的一切内容必须脱敏
2. **对话内容不离开本地**：只有脱敏摘要发送到服务端
3. **结构化数据存本地**：SQLite 完全在用户本地
