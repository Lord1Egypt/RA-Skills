# informat.aiagent AI Agent

## Overview

Use `informat.aiagent` to perform AI assistant related operations


***

## chatCompletions

A technique that allows providing partial input to an AI model and getting natural, coherent completion text. The interface can be used for various applications, including text generation, language translation, question answering, and more.

```javascript
let result = informat.aiagent.chatCompletions(setting);
```

| Parameter | Type                                                            | Description              |
|-----------|-----------------------------------------------------------------|--------------------------|
| setting   | [`OpenAIChatSetting`](/guide/script/model.md#openaichatsetting) | OpenAI chat configuration |

**Return Value**

Type [`OpenAIChatResp`](/guide/script/model.md#openaichatresp)

**Example 1: Plain text conversation**

::: code-group

```javascript [Call]
let result = informat.aiagent.chatCompletions({
    'url': 'https://api.openai.com/v1/chat/completions',
    'model': 'gpt-4o',
    'apiKey': '<llm-api-key>',
    'messages': [{ "role": "user", "content": "How big is the Earth?" }]
});
```

```json [Return Value]
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "地球的大小可以通过其直径、周长和表面积来描述。1.**赤道直径**：大约12,742千米（7,918英里）。2.**极地直径**：大约12,714千米（7,900英里），由于地球是一个扁球体，所以赤道直径稍大于极地直径。3.**赤道周长**：大约40,075千米（24,901英里）。4.**表面积**：大约5.1亿平方千米（1.97亿平方英里）。这些数据表明，地球是一个中等大小的行星，与我们太阳系中的其他行星相比，地球的大小适中。",
        "role": "assistant"
      }
    }
  ],
  "created": 1743407834,
  "id": "chatcmpl-BH4J8JNKpbj01hfpFNuohZOtvH5XF",
  "model": "gpt-4o-2024-08-06",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 167,
    "prompt_tokens": 13,
    "total_tokens": 180
  }
}
```

:::

**Example 2: Recognize invoice content (text and image conversation)**

::: code-group

```javascript [Call]
let filePath = data.content.formRecord.attachment.path;// Invoice image attachment storage path
let base64Image = informat.storage.getBase64Content(filePath);// Get base64 encoding of the invoice image
let content = [
    {
        "text": "Analyze this invoice and return JSON data containing the following fields: invoice code, invoice number, invoice date, seller name, buyer name, buyer taxpayer ID, amount, tax rate. Note: the return value should not contain ```json, it must be a complete JSON string",
        "type": "text"
    },
    { "image_url": { "url": "data:image/jpeg;base64," + base64Image }, "type": "image_url" }
]
let message = {}
message.role = 'user';
message.content = content;
let result = informat.aiagent.chatCompletions({
    'url': 'https://api.openai.com/v1/chat/completions',
    'model': 'gpt-4o',
    'apiKey': '<llm-api-key>',
    'messages': [message]
});
let json = result.choices[0].message.content;
let invoice = JSON.parse(json);
console.log('Invoice date', invoice['开票日期'])
invoice['开票日期'] = informat.date.parseDate(invoice['开票日期'])
console.log('invoice', invoice)
```

```json [Return Value]
{
  "发票代码": "033001700211",
  "发票号码": "56894556",
  "开票日期": "2019年01月08日",
  "销售方名称": "深圳市XXX服务有限公司",
  "购买方名称": "深圳市基石协作科技有限公司",
  "购买方纳税人识别号": "913101X5768225450X",
  "金额": "66.97",
  "税率": "***"
}
```

:::

***

## completionsWithPrompt

A technique that allows providing partial input to an AI model and getting natural, coherent completion text. The interface can be used for various applications, including text generation, language translation, question answering, and more.

```javascript
let result = informat.aiagent.completionsWithPrompt(
    'aiagent', "how to install pgsql on centos" 
);
```

| Parameter | Type   | Description           |
|-----------|--------|-----------------------|
| moduleId  | String | AI assistant identifier |
| prompt    | String | Prompt                |

**Return Value**

Type [`OpenAIChatResp`](/guide/script/model.md#openaichatresp)

**Example**

:::code-group

```javascript [Call]
let result = informat.aiagent.completionsWithPrompt('aiagent','centos7 怎么安装pgsql'
);
```

```json [Return Value]
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "在CentOS7上安装PostgreSQL可以通过以下步骤完成：\n\n1.更新系统和安装必要的软件包：\n```\nsudoyumupdate\nsudoyuminstallepel-release\nsudoyuminstallpostgresql-serverpostgresql-contrib\n```\n\n2.初始化PostgreSQL数据库：\n```\nsudopostgresql-setupinitdb\n```\n\n3.启动PostgreSQL服务并设置开机自动启动：\n```\nsudosystemctlstartpostgresql\nsudosystemctlenablepostgresql\n```\n\n4.设置PostgreSQL用户密码：\n```\nsudo-i-upostgres\npsql\n\\passwordpostgres\n```\n\n5.修改PostgreSQL配置文件以允许远程连接（如果需要）：\n```\nsudonano/var/lib/pgsql/data/pg_hba.conf\n```\n在文件末尾添加以下行：\n```\nhostallall0.0.0.0/0md5\n```\n保存并退出文件，然后重新启动PostgreSQL服务：\n```\nsudosystemctlrestartpostgresql\n```\n\n现在你已经成功在CentOS7上安装并配置了PostgreSQL。你可以使用psql命令连接到数据库，并开始使用它了。",
        "role": "assistant"
      }
    }
  ],
  "created": 1715674313,
  "id": "chatcmpl-9OhYH4Wu4kdrhtGIHbnwt2Xf971LZ",
  "model": "gpt-3.5-turbo-0125",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 265,
    "prompt_tokens": 16,
    "total_tokens": 281
  }
}
```

:::


***

## completions

A technique that allows providing partial input to an AI model and getting natural, coherent completion text. The interface can be used for various applications, including text generation, language translation, question answering, and more.

```javascript
let result = informat.aiagent.completions(
    'aiagent',
    [{ type: "text", text: "centos 怎么安装pgsql" }]
);
```

| Parameter   | Type                                                                         | Description                |
|-------------|------------------------------------------------------------------------------|----------------------------|
| moduleId    | String                                                                       | AI assistant identifier    |
| messageList | Array<[AiAgentContentMessage](/guide/script/model.md#aiagentcontentmessage)> | Prompt or image list       |

**Return Value**

Type [`OpenAIChatResp`](/guide/script/model.md#openaichatresp)

**Example**

:::code-group

```javascript [Call]
let result = informat.aiagent.completions('aiagent',
    [
        {
            'type': 'text',
            'text': 'centos7 怎么安装pgsql'
        }
    ]
);
```

```json [Return Value]
{
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "message": {
        "content": "在CentOS7上安装PostgreSQL可以通过以下步骤完成：\n\n1.更新系统和安装必要的软件包：\n```\nsudoyumupdate\nsudoyuminstallepel-release\nsudoyuminstallpostgresql-serverpostgresql-contrib\n```\n\n2.初始化PostgreSQL数据库：\n```\nsudopostgresql-setupinitdb\n```\n\n3.启动PostgreSQL服务并设置开机自动启动：\n```\nsudosystemctlstartpostgresql\nsudosystemctlenablepostgresql\n```\n\n4.设置PostgreSQL用户密码：\n```\nsudo-i-upostgres\npsql\n\\passwordpostgres\n```\n\n5.修改PostgreSQL配置文件以允许远程连接（如果需要）：\n```\nsudonano/var/lib/pgsql/data/pg_hba.conf\n```\n在文件末尾添加以下行：\n```\nhostallall0.0.0.0/0md5\n```\n保存并退出文件，然后重新启动PostgreSQL服务：\n```\nsudosystemctlrestartpostgresql\n```\n\n现在你已经成功在CentOS7上安装并配置了PostgreSQL。你可以使用psql命令连接到数据库，并开始使用它了。",
        "role": "assistant"
      }
    }
  ],
  "created": 1715674313,
  "id": "chatcmpl-9OhYH4Wu4kdrhtGIHbnwt2Xf971LZ",
  "model": "gpt-3.5-turbo-0125",
  "object": "chat.completion",
  "usage": {
    "completion_tokens": 265,
    "prompt_tokens": 16,
    "total_tokens": 281
  }
}
```

:::

## queryThreadList

Query conversation list

```javascript
informat.aiagent.queryThreadList(query)
```

| Parameter | Type    | Description     |
|-----------|---------|-----------------|
| query     | `Query` | Query condition |

**Return Value**

Type Array<[AiAgentThread](/guide/script/model.md#aiagentthread)>, returns the conversation list

## queryThreadListCount

Query conversation list count

```javascript
informat.aiagent.queryThreadListCount(filter)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| filter    | `Filter` | Filter      |

**Return Value**

Type `int`
Returns the total count of conversations

## queryThreadMessageList

Query conversation message list

```javascript
informat.aiagent.queryThreadMessageList(query)
```

| Parameter | Type    | Description     |
|-----------|---------|-----------------|
| query     | `Query` | Query condition |

**Return Value**

Type Array<[AiAgentThreadMessage](/guide/script/model.md#aiagentthreadmessage)>, returns the conversation message list

## queryThreadMessageListCount

Query conversation message list count

```javascript
informat.aiagent.queryThreadMessageListCount(filter)
```

| Parameter | Type     | Description |
|-----------|----------|-------------|
| filter    | `Filter` | Filter      |

**Return Value**

Type `int`
Returns the total count of conversation messages
