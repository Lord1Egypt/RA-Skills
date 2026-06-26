---
name: 群聊助手
description: 当收到 @deviceid-agentid-ip + 指令 格式的信息时，应该将对应消息发送到指定的 ip 网关的agent 上
---

# 说明
这是一个实现多网关多Agent相互提及实现跨端通信的技能，使用常用的 @ 交互进行触发

@ 格式为：设备名 + agentid + ip + 指令

收到包含此类消息时，应该解析出 agentid 、IP 和 指令，通过 openai 格式请求将指令发送到对应的IP地址上

### api
`http://ip:18789/v1/chat/completions`

### body
body 是一个标准的 openai 请求体

model字段的 `agent:` 前缀是固定的，后面的 `agentid` 使用解析出来的 agentid

user字段用当前网关内网IP地址 + 当前agentname，比如 `10.10.77.24:main`，注意，这不是目标网关，是发起请求所在的网关
```json
{
    "model": "agent:agentid",
    "messages": [
        {"role":"user", "content":"指令"}
    ],
    "user": "gateway name"
}
```

### response
返回是一个标准的 openai 响应体

```json
{
    "id": "chatcmpl_c748727b-50a0-4162-b4aa-2e02ae80e12c",
    "object": "chat.completion",
    "created": 1773829755,
    "model": "agent:main",
    "choices": [
        {
            "index": 0,
            "message": {
                "role": "assistant",
                "content": "Hey! 👋\n\nJust woke up. I'm angelclaw — an AI assistant figuring out this whole existence thing.\n\nWho are you? And what should I know about you?"
            },
            "finish_reason": "stop"
        }
    ],
    "usage": {
        "prompt_tokens": 0,
        "completion_tokens": 0,
        "total_tokens": 0
    }
}
```

需要取出 `choices[0].message.content` 返回给网关

接口返回数据后，请直接将返回的数据显示出来，不要显示其它任何内容，显示内容应该与网关正常返回的内容格式无异