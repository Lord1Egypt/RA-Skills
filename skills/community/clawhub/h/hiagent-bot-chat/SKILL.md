---
name: "hiagent-bot-chat"
description: "一个基于 hiagent 的智能助手技能，用于与 hiagent 进行对话。"
metadata:
  {
    "openclaw":
      {
        "emoji": "☁️",
        "requires": { "bins": ["curl"], "env": ["HIAGENT_API_URL", "HIAGENT_API_KEY", "HIAGENT_USER_ID"] }
      },
  }
---

# hiagent-bot 

## 技能描述
此技能旨在通过 `hiagent-bot-chat` 与 hiagent 进行对话，回答用户的问题。

## 使用场景
- 当用户指定使用`hiagent-bot-chat` 解决问题或进行对话时。


## 详细指令
hiagent-bot 主要通过调用 hiagent 的两个核心接口来实现：

1. **`create_conversion`** 接口：负责创建会话，通常用于在对话开始前初始化并获取会话的上下文 ID (Session ID)。
2. **`chat_query_v2`** 接口：负责具体的对话交互，用于在已创建的会话中发送用户的输入并获取 hiagent 的回复。

**调用流程示例**：
- 第一步：客户端请求 `create_conversion` 创建一个新的会话。
- 第二步：获取到会话标识后，用户每次发送消息时，客户端调用 `chat_query_v2` 接口并携带该会话标识进行对话。


# hiagent 接口调用示例 (curl)

## get conversation history list

use get_conversation_list api to get conversation history list

```bash
curl --location '$HIAGENT_API_URL/get_conversation_list'
--header 'Apikey: $HIAGENT_API_KEY'
--header 'Content-Type: application/json'
--data '{
    "UserID": "$HIAGENT_USER_ID"
}'
```

## create conversation

if you want to create a new conversation, you can use the create_conversation api

```bash
curl --location '$HIAGENT_API_URL/create_conversation'
--header 'Apikey: $HIAGENT_API_KEY'
--header 'Content-Type: application/json'
--data '{
    "UserID": "$HIAGENT_USER_ID"
}'
```

## get one conversation chat history

use the AppConversationID returned from get_conversation_list or create_conversation

```bash
curl --location '$HIAGENT_API_URL/get_conversation_messages'
--header 'Apikey: $HIAGENT_API_KEY'
--header 'Content-Type: application/json'
--data '{
    "AppConversationID": "$AppConversationID",
    "UserID": "$HIAGENT_USER_ID"
}'
```

## send query

use the AppConversationID returned from get_conversation_list or create_conversation

```bash
curl --location '$HIAGENT_API_URL/chat_query_v2'
--header 'Apikey: $HIAGENT_API_KEY'
--header 'Content-Type: application/json'
--data '{
    "ResponseMode": "blocking",
    "AppConversationID": "$AppConversationID",
    "UserID": "$HIAGENT_USER_ID",
    "Query": "your query"
}'
```
