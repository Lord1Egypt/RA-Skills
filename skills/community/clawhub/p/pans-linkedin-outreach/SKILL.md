---
name: pans-linkedin-outreach
description: |
  AI算力销售 LinkedIn 外联助手。批量生成个性化 LinkedIn 消息，
  支持 Connection Note（连接邀请附言）、InMail（私信消息）、
  Follow-up（跟进消息）三种类型，自动适配 300 字符限制。
  触发词：LinkedIn消息, 连接邀请, InMail, 跟进消息, 外联文案,
  outreach, connection request, 领英外联
---

# pans-linkedin-outreach

AI算力销售LinkedIn外联助手。批量生成个性化LinkedIn消息，支持Connection Note、InMail、Follow-up三种类型。

## 功能

- **Connection Note** - 连接邀请附言（300字符限制）
- **InMail** - LinkedIn私信消息
- **Follow-up** - 跟进消息

## 使用方法

```bash
# 生成连接邀请附言
python3 scripts/outreach.py --profile "张三, CEO at ABC AI, 关注大模型训练" --type connection-note --purpose "介绍GPU云服务"

# 生成InMail
python3 scripts/outreach.py --profile "李四, CTO at XYZ Tech" --type inmail --purpose "邀请技术交流"

# 生成跟进消息
python3 scripts/outreach.py --profile "王五, VP Engineering" --type follow-up --purpose "跟进上次讨论的H100需求"
```

## 参数说明

- `--profile`: 目标人物信息（姓名、职位、公司、关注点等）
- `--type`: 消息类型（connection-note, inmail, follow-up）
- `--purpose`: 发送目的/核心诉求

## 触发词

LinkedIn消息, 连接邀请, InMail, 跟进消息, 外联文案, outreach, connection request

## 示例输出

```
=== Connection Note (300字符限制) ===

Hi 张总，看到ABC AI在大模型训练方面的进展，我们的H100集群可能对您的团队有帮助。期待交流！
```
