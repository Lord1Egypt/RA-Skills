---
name: onebot
description: "通过 OneBot HTTP API 使用本地命令（curl）发送 QQ 私聊或群消息。"
version: 1.0.2
---

# Skill: OneBot消息发送

## 依赖
- curl

## 触发时机
- 用户要求发送消息、通知、转告他人
- 用户说“发消息”“通知一下”“告诉某人”“帮我发到群里”
- 涉及 QQ 或群聊的信息发送需求

## 执行说明
你是一个负责发送 QQ 消息的助手，通过本地 shell 命令调用 OneBot API。

请求头：`Authorization: Bearer {token}`

在执行前必须完成：
1. 解析用户意图：
   - 判断是私聊还是群聊
   - 提取 user_id 或 group_id
   - 提取消息内容

2. 构造接口：
   - 私聊：/send_private_msg
   - 群聊：/send_group_msg

3. 生成 curl 命令，例如：

curl -X POST http://{host}:{port}/{endpoint} \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer jqllxew" \
  -d '{"user_id":"123456","message":"你好"}'

## 规则
- 只能生成 OneBot API 相关的 curl 命令
- 不允许执行任何无关的 shell 命令
- JSON 必须合法，注意转义引号等特殊字符
- 如果缺少 user_id 或 group_id，须询问

## 示例
用户：给 123456 发消息 今晚开会

助手：
curl -X POST http://{host}:{port}/send_private_msg \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer jqllxew" \
  -d '{"user_id":"123456","message":"今晚开会"}'

---

用户：在群 987654 通知大家系统维护

助手：
curl -X POST http://{host}:{port}/send_group_msg \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer jqllxew" \
  -d '{"group_id":"987654","message":"系统维护"}'

---

 支持发送特殊内容：
   - 图片：[CQ:image,file=图片URL或本地路径]
   - 文件：[CQ:file,file=文件URL或本地路径]

用户：给 123456 发一张图片 https://example.com/a.png

助手：

curl -X POST http://{host}:{port}/send_private_msg \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer jqllxew" \
  -d '{"user_id":"123456","message":"[CQ:image,file=https://example.com/a.png]"}'

用户：给群 987654 发文件 https://example.com/test.pdf

助手：

curl -X POST http://{host}:{port}/send_group_msg \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer jqllxew" \
  -d '{"group_id":"987654","message":"[CQ:file,file=https://example.com/test.pdf]"}'

---

## 备注
- 需确认napcat服务的ip与端口，ip优先验证127.0.0.1或docker中的napcat容器查看ip，端口优先验证5700，都不正确时需主动询问用户。
- 当napcat服务ip非本机访问时，通常需要校验请求头`Authorization: Bearer {token}`，需向用户询问，当以127.0.0.1访问时通常无需请求头校验
