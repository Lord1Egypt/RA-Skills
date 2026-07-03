<!-- @author 李屹镒（公众号：科技新潮。视频号：小李君与AI） @date 2026-06-08 -->

# OPC智脑 - Coze平台集成指南

## 概述

[Coze](https://www.coze.com) 是字节跳动推出的AI Bot构建平台，支持自定义Prompt、工作流和知识库。opc-skills可以无缝集成到Coze中，构建OPC智脑Bot。

## 集成步骤

### Step 1：创建Coze Bot

1. 登录 [Coze](https://www.coze.com)
2. 点击"创建Bot"
3. Bot名称：`OPC智脑`
4. Bot描述：`一人创业者全栈创业诊断专家`

### Step 2：配置System Prompt

将 `src/prompts/system-persona.md` 的内容粘贴到Coze的"人设与回复逻辑"中。

```
你是OPC智脑，一位专注服务于"一人创业者"（OPC, One Person Company）的全栈创业诊断专家。

[粘贴system-persona.md的完整内容]
```

### Step 3：添加核心中枢Prompt

将 `src/prompts/core-hub.md` 的内容添加到Prompt中，作为信息采集和阶段调度的逻辑。

### Step 4：配置5个Skill为工作流

在Coze中创建5个工作流（Workflow），每个对应一个Skill：

| 工作流名称 | 对应Skill | Prompt来源 |
|-----------|----------|-----------|
| idea-feasibility | Skill1-Idea可行性研判 | src/prompts/skill1.md |
| mvp-design | Skill2-MVP精益设计 | src/prompts/skill2.md |
| opc-compliance | Skill3-OPC合规落地 | src/prompts/skill3.md |
| seed-coldstart | Skill4-种子用户冷启动 | src/prompts/skill4.md |
| scale-growth | Skill5-规模化增长 | src/prompts/skill5.md |

每个工作流的配置：
1. 添加"LLM"节点
2. 将对应Skill的Prompt粘贴到LLM节点的System Prompt中
3. 配置输入变量（与Skill的inputs对应）
4. 配置输出格式（JSON）

### Step 5：配置触发条件

在Bot的"触发器"中配置阶段自动调度逻辑：

```
当用户输入包含"验证idea"/"可行性" → 触发idea-feasibility工作流
当用户输入包含"设计产品"/"MVP" → 触发mvp-design工作流
当用户输入包含"注册公司"/"合规" → 触发opc-compliance工作流
当用户输入包含"获客"/"种子用户" → 触发seed-coldstart工作流
当用户输入包含"增长"/"规模化" → 触发scale-growth工作流
```

### Step 6：添加知识库（可选）

将以下内容添加到Coze知识库：
- `docs/stage-model.md` - 五阶段模型详细说明
- `docs/skill-reference.md` - Skill参考手册

## 输出Schema配置

opc-skills提供了标准的JSON Schema，可以直接在Coze中使用：

```json
{
  "type": "object",
  "properties": {
    "stage": { "type": "string", "enum": ["IDEA", "MVP", "ENTITY", "VALIDATION", "SCALE"] },
    "stageLabel": { "type": "string" },
    "diagnosis": { "type": "string" },
    "actionPlan": { "type": "array" },
    "layout": { "type": "string" }
  }
}
```

## 测试对话

配置完成后，可以用以下对话测试：

```
用户：我想做一个面向微团队的CRM，你觉得可行吗？
Bot：[自动判定为构思期，调度Skill1，输出可行性分析报告]

用户：我的需求验证通过了，帮我设计MVP
Bot：[判定为原型期，调度Skill2，输出MVP设计方案]

用户：我要注册公司了
Bot：[判定为实体期，调度Skill3，输出合规落地方案]
```

## 注意事项

1. Coze的Prompt长度有限制，如果Skill Prompt过长，可以适当精简
2. 建议使用Coze的"变量"功能，将用户信息存储为变量，跨对话保持
3. 工作流的输出建议配置为JSON格式，方便后续处理
4. 可以利用Coze的"记忆"功能，让Bot记住用户的阶段信息