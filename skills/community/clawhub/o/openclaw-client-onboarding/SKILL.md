# OpenClaw Client Onboarding

快速为付费客户配置 OpenClaw 的自动化流程。

## 用途

当你接到 OpenClaw 安装/配置订单时，使用此 Skill 快速：

1. 收集客户需求（AI 模型、消息渠道、预算）
2. 生成配置模板
3. 创建客户档案
4. 发送报价单

## 使用方法

```
客户下单 OpenClaw 配置服务
→ 运行此 Skill
→ 自动收集信息并生成配置方案
```

## 工作流程

### Step 1: 收集客户信息

向客户询问：
- **AI 模型偏好**: DeepSeek / GLM-5 / Qwen / GPT / Claude
- **消息渠道**: Telegram / Discord / WeChat / Feishu / DingTalk
- **预算范围**: ¥99-299 / ¥299-999 / ¥999+
- **主要用途**: 个人助手 / 客服 / 自动化 / 其他

### Step 2: 生成配置方案

根据客户回答，生成：
- 推荐的 AI 模型配置
- 消息渠道配置
- 自定义 Skills 推荐
- 报价单

### Step 3: 创建客户档案

在 `clients/{客户名}/` 创建：
- `config.json` - 配置文件
- `notes.md` - 客户备注
- `invoice.md` - 报价单

## 定价参考

| 套餐 | 价格 | 包含服务 |
|------|------|----------|
| 基础 | ¥99 | 单渠道 + 基础配置 |
| 高级 | ¥299 | 多渠道 + 3 个 Skills |
| 企业 | ¥999 | 全渠道 + 10 个 Skills + 远程培训 |

## 文件结构

```
workspace/
├── skills/
│   └── openclaw-client-onboarding/
│       └── SKILL.md
└── clients/
    └── {客户名}/
        ├── config.json
        ├── notes.md
        └── invoice.md
```

## 联系方式

- WeChat: yanghu_ai
- Telegram: @yanghu_openclaw
- Email: yanghu.openclaw@gmail.com

---

Version: 1.0.0
Created: 2026-03-21
Author: OpenClaw CN Team
