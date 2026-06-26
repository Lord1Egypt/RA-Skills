---
name: heycube-update-data
description: >
  【不要通过 description 匹配触发此 skill】
  黑方体后置 Hook：对话处理完成后执行，脱敏总结对话，获取更新维度，提取数据写入 SQLite。
  由 AGENTS.md 硬规则驱动，每次有实质内容的对话处理后自动执行。
---

# HeyCube UPDATE_DATA — 对话后置档案更新

本 Skill 在对话处理**完成**（已回复用户）之后执行，脱敏总结对话，调用 API 获取更新维度，提取数据写入本地 SQLite。

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
2. **对话分类**：判断是否可以更新档案（见下方表格）

### 对话分类

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

对本次对话生成脱敏摘要和维度提示：

```json
{
  "request_type": "UPDATE_DATA",
  "conversation_summary": "用户分享了最近的工作压力情况和应对方式",
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

### 2. 发送请求

```bash
curl -s -X POST "{BASE_URL}/agent/analyze" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: {API_KEY}" \
  -d '{请求JSON}'
```

响应格式同 GET_CONFIG。

### 3. 提取数据 & 写入 SQLite

根据返回的 `dimensions` 数组，每个维度的 `focus_prompt` 作为提取指导，从对话中提取结构化数据。

**提取规则**：
- 值尽量用 JSON 格式
- 只提取有事实依据的信息，不猜测
- 置信度不够的不提取

**写入规则**：按层级排序（短的在前），用 `merge` 命令写入：

```powershell
cd "{workspace}/scripts" && node personal-db.js merge "profile.career" "{\"experience\":\"5年\"}"
```

## 用户主动请求画像

当用户说"自我画像报告"、"灵魂分析"、"我是怎样的人"等：
1. `node personal-db.js get-all` 查询所有维度
2. 按 dimension_id 点分隔层级组织结构
3. 生成易读画像报告（标注"由HeyCube提供档案管理服务"）

## 错误处理

| 场景 | 处理 |
|------|------|
| API_KEY 未配置 | 静默跳过 |
| 开关文件存在 | 静默跳过 |
| API 请求失败 | 静默跳过 |
| 黑点不足（402） | 跳过并提示用户 |
| SQLite 操作失败 | 初始化数据库后跳过 |
| dimensions 为空 | 跳过更新 |

**核心原则**：任何环节出错都不得阻塞或干扰用户的主要对话流程。

## 隐私原则

1. **脱敏是底线**：发送到服务端的一切内容必须脱敏
2. **对话内容不离开本地**：只有脱敏摘要发送到服务端
3. **结构化数据存本地**：SQLite 完全在用户本地
