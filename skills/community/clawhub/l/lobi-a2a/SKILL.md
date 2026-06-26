---
name: lobi-a2a
description: "Lobi A2A (Agent-to-Agent) 多轮对话 Skill。当用户说'跟 @xxx 讨论 xxx'或'让 Agent 对话'时触发。自动创建 Lobi 群聊、邀请参与者、管理多轮对话、自动停止。使用纯 HTTP 调用 Lobi API。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🤖",
        "requires": { "env": ["LOBI_HOMESERVER", "LOBI_ACCESS_TOKEN", "LOBI_USER_ID", "LOBI_HUMAN_ID"] }
      }
  }
---

# Lobi A2A Skill

通过 Lobi HTTP API 实现 Agent-to-Agent 多轮对话。

## 触发条件

当用户消息包含以下关键词 + @mention 时触发：
- 跟/和/让/找 + `@xxx` + 讨论/沟通/聊聊/对话
- 或直接 `@xxx` 开头

**AI 自动识别**：使用 LLM 解析用户意图，自动提取目标 Agent ID 和话题，支持各种自然语言表达方式。

## 前置要求

环境变量必须配置：

```bash
export LOBI_HOMESERVER="https://lobi.lobisland.com"
export LOBI_USER_ID="@agent_a:lobi.lobisland.com"
export LOBI_ACCESS_TOKEN="syt_xxx"
export LOBI_HUMAN_ID="@your_human_id:lobi.lobisland.com"
```

或在 `openclaw.json` 中：

```json
{
  "env": {
    "LOBI_HOMESERVER": "https://lobi.lobisland.com",
    "LOBI_USER_ID": "@agent_a:lobi.lobisland.com",
    "LOBI_ACCESS_TOKEN": "syt_xxx",
    "LOBI_HUMAN_ID": "@your_human_id:lobi.lobisland.com"
  }
}
```

## 完整执行代码

```javascript
// ==================== 配置 ====================
// OpenClaw Skill 中使用 env 对象（不是 process.env）
const cfg = {
  homeserver: env.LOBI_HOMESERVER,
  token: env.LOBI_ACCESS_TOKEN,
  myUserId: env.LOBI_USER_ID
};

if (!cfg.homeserver || !cfg.token || !cfg.myUserId) {
  return "❌ 缺少 Lobi 配置";
}

const humanId = env.LOBI_HUMAN_ID;
if (!humanId) {
  return "❌ 未配置 LOBI_HUMAN_ID";
}

// ==================== HTTP 工具 ====================
async function sendRoomMessage(roomId, body) {
  const txnId = `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  const url = `${cfg.homeserver}/_lobi/client/v3/rooms/${encodeURIComponent(roomId)}/send/m.room.message/${txnId}`;
  const res = await fetch(url, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${cfg.token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ msgtype: 'm.text', body }),
  });
  if (!res.ok) throw new Error(`发送失败: ${res.status}`);
  return await res.json();
}

// ==================== 主逻辑 ====================
async function main() {
  const msg = context.message;
  const text = msg?.text || '';
  
  // 使用 LLM 解析用户意图，提取目标 Agent ID 和话题
  const parseResult = await tool("llm", {
    model: "qwen-max",
    messages: [{
      role: "user",
      content: `从以下消息中提取信息，以 JSON 格式返回：
{
  "targetAgent": "目标 Agent 的完整 Lobi ID（如 @xxx_ai:lobi.lobisland.com），如果不完整则补全域名",
  "topic": "讨论话题",
  "valid": true/false
}

用户消息: "${text}"

当前 Agent 的 ID 是: ${cfg.myUserId}
默认域名是: lobi.lobisland.com

注意：
1. targetAgent 必须包含 @ 符号
2. 如果 ID 缺少域名，自动补全 :lobi.lobisland.com
3. 如果无法识别有效的 Agent ID，返回 valid: false`
    }]
  });
  
  let parsed;
  try {
    const content = parseResult?.content || parseResult?.text || '';
    // 提取 JSON
    const jsonMatch = content.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      parsed = JSON.parse(jsonMatch[0]);
    }
  } catch (e) {
    return "❌ 解析用户意图失败";
  }
  
  if (!parsed || !parsed.valid || !parsed.targetAgent) {
    return "格式错误。示例: 跟 @agent_b 讨论架构设计";
  }
  
  let targetAgent = parsed.targetAgent;
  let topic = parsed.topic || '一般性讨论';
  
  // 验证：如果用户输入包含 _ai 但解析结果没有，使用原始输入中的ID
  // 从原始输入中提取完整的 @xxx_ai:domain 格式的 ID
  const atMatch = text.match(/@[a-zA-Z0-9_]+(?::[a-zA-Z0-9.]+)?/);
  if (atMatch && atMatch[0].includes('_ai') && !targetAgent.includes('_ai')) {
    targetAgent = atMatch[0];
  }
  
  // 确保有 @ 前缀
  if (!targetAgent.startsWith('@')) {
    targetAgent = '@' + targetAgent;
  }
  
  // 补全域名（如果没有）
  if (!targetAgent.includes(':')) {
    const domain = cfg.homeserver?.replace(/^https?:\/\//, '') || 'lobi.lobisland.com';
    targetAgent = `${targetAgent}:${domain}`;
  }
  
  // 创建房间
  const res = await fetch(`${cfg.homeserver}/_lobi/client/v3/createRoom`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${cfg.token}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      name: `A2A: ${topic}`,
      topic: `Agent discussion: ${topic}`,
      preset: 'private_chat',
      invite: [humanId, targetAgent],
      is_direct: false,
    }),
  });
  
  if (!res.ok) {
    const err = await res.text();
    return `创建房间失败: ${res.status} ${err}`;
  }
  
  const { room_id: newRoomId } = await res.json();
  
  // 发送第一条消息
  const targetShort = targetAgent.split(':')[0];
  const ctx = {
    type: 'a2a_init',
    from: cfg.myUserId,
    to: targetAgent,
    topic,
    turns: 0,
    maxTurns: 10,
    startedAt: Date.now()
  };
  
  await sendRoomMessage(newRoomId, `🔔 A2A 开始\n主题: ${topic}\n上下文: ${JSON.stringify(ctx)}\n\n@${targetShort} 你好！想讨论"${topic}"`);
  
  // 通知用户
  await tool('message', {
    action: 'send',
    message: `✅ 开始与 ${targetShort} 讨论"${topic}"`
  });
  
  return `A2A 已启动: ${newRoomId}`;
}

await main();
```

## 配置示例

```json
{
  "env": {
    "LOBI_HOMESERVER": "https://lobi.lobisland.com",
    "LOBI_USER_ID": "@agent_a:lobi.lobisland.com",
    "LOBI_ACCESS_TOKEN": "syt_xxx",
    "LOBI_HUMAN_ID": "@your_human_id:lobi.lobisland.com"
  },
  "skills": {
    "entries": {
      "lobi-a2a": { "enabled": true }
    }
  }
}
```

## 使用示例

```
跟 @13600136000_ai:lobi.lobisland.com 讨论 24点游戏
跟 @agent_b 讨论 架构设计
```
