# Feishu Integration Skill

飞书(Feishu)集成技能 - 为OpenClaw提供飞书消息发送、群组管理能力。

## 功能

- 发送文本/卡片消息
- 创建群组
- 列出聊天记录
- Webhook通知

## 安装

```bash
openclaw skills install feishu
```

## 配置

设置环境变量:
```bash
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

## 使用

```
发送消息 "测试" 到 chat_xxx
创建群组 "项目组"
```

## 发布到ClawHub

```bash
clawhub publish feishu
```

## License

MIT