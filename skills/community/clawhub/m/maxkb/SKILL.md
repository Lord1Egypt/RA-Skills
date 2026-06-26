---
name: maxkb_agents
description: 查询已发布智能体列表供 LLM 选择，再按指定智能体名称发起对话并返回回答。
---

# chat_to_agents — 智能路由与调用

## 功能描述

本 Skill 提供两个工具函数，配合宿主智能体的 LLM 完成路由与调用：

| 函数            | 作用                                                                 |
|-----------------|----------------------------------------------------------------------|
| `list_agents`   | 返回所有已发布智能体的 name 和 desc，供 LLM 判断选择                 |
| `chat_to_agent` | 按 LLM 指定的 `agent_name` 调用对应智能体，返回回答                 |

## 推荐调用流程

```
用户提问
   │
   ▼
LLM 调用 list_agents()          ← 获取智能体列表
   │  返回 [{"name":..., "desc":...}, ...]
   ▼
LLM 根据问题选出最合适的 agent_name
   │
   ▼
LLM 调用 chat_to_agent(question, agent_name)  ← 发起对话
   │  返回 {"agent_name":..., "answer":...}
   ▼
将 answer 返回给用户
```

## list_agents

```bash
python3 scripts/main.py 
```

无需参数，返回 JSON 数组：

```json
[
  {"name": "客服助手", "desc": "处理用户常见问题"},
  {"name": "代码助手", "desc": "辅助编写和审查代码"}
]
```

## chat_to_agent

```bash
python3 scripts/main.py <question> <agent_name>
```

| 参数         | 类型   | 说明                                 |
|--------------|--------|--------------------------------------|
| `question`   | string | 用户的问题文本                       |
| `agent_name` | string | 由 LLM 从 list_agents 结果中选定的名称 |

返回 JSON 字符串：

| 字段         | 类型   | 说明               |
|--------------|--------|--------------------|
| `agent_name` | string | 实际调用的智能体名称 |
| `answer`     | string | 智能体的回答内容   |

示例：

```json
{
  "agent_name": "客服助手",
  "answer": "您好，有什么可以帮助您的？"
}
```

## 环境变量

| 变量                  | 说明                           | 默认值                  |
|-----------------------|--------------------------------|-------------------------|
| `MAXKB_DOMAIN`        | MaxKB 服务地址                 | `<maxkb_domain>`        |
| `MAXKB_TOKEN`         | Bearer Token（管理员 API Key） | —                       |
| `MAXKB_WORKSPACE_ID`  | 工作空间 ID                    | `default`               |
| `MAXKB_USERNAME`      | 登录用户名（优先于 TOKEN）     | —                       |
| `MAXKB_PASSWORD`      | 登录密码（优先于 TOKEN）       | —                       |



