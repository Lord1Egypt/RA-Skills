# 多 Agent 项目执行指南

本指南将帮助你使用 Hermes 的多 Agent 系统完成你的项目。

## 📋 前置准备

1. ✅ 确保你在 Hermes 环境中运行
2. ✅ 检查 `PROJECT_CONFIG.yaml` 配置是否正确
3. ✅ 准备好清晰的项目目标描述

## 🚀 执行步骤

### 第一步：初始化项目

在 Hermes 中发送以下消息：

```
我要使用多 Agent 协作来完成这个项目：

项目名称：[你的项目名称]
项目描述：[详细描述你的项目目标]

请参考 PROJECT_CONFIG.yaml 文件中的配置来执行。
```

### 第二步：等待任务分解

Hermes 会自动：
1. 📝 创建 Todo 任务列表
2. 👥 分配任务给各个专业 Agent
3. 🔄 开始并行执行

### 第三步：监控进度

你会看到类似这样的进度：

```
📋 任务状态：
- [x] 需求分析 - Analyst (已完成)
- [x] 技术调研 - Researcher (已完成)
- [x] 架构设计 - Architect (已完成)
- [ ] 代码实现 - Implementer (进行中)
- [ ] 测试验证 - Tester (待开始)
```

### 第四步：查看输出

所有输出会保存在 `outputs/` 目录：

```
outputs/
├── 01-requirements/
│   └── requirements.md          # 需求分析文档
├── 02-research/
│   └── research.md              # 技术调研报告
├── 03-architecture/
│   ├── architecture.md          # 架构设计文档
│   └── diagrams/                # 架构图（如果有）
├── 04-implementation/
│   ├── src/                     # 源代码
│   └── README.md                # 实现说明
└── 05-testing/
    └── test-report.md           # 测试报告
```

## 💡 交互提示

### 如果需要调整需求

在执行过程中，你可以随时：

```
我想调整一下需求：[描述你的调整]
```

### 如果对某个结果不满意

```
关于 [某部分]，我希望：[描述你的期望]
请让对应的 Agent 重新处理一下。
```

### 如果想跳过某个阶段

```
我们已经有了 [某部分] 的内容，可以跳过这个阶段。
直接进入下一阶段吧。
```

## 🎯 成功标志

项目完成时，你应该获得：

1. ✅ 完整的需求文档
2. ✅ 技术选型和调研报告
3. ✅ 系统架构设计
4. ✅ 可运行的代码实现
5. ✅ 测试报告和质量评估

## 🔧 故障排除

### Agent 没有响应

检查：
1. Hermes 是否正常运行
2. 网络连接是否正常
3. 任务描述是否清晰

### 输出质量不符合预期

尝试：
1. 在配置中添加更详细的 `custom_prompt`
2. 提供更具体的项目目标和约束
3. 在交互中给予更明确的反馈

### 想要重新开始

```
让我们重新开始这个项目。
这一次我希望：[描述你的改进想法]
```

## 📚 更多帮助

如需更多帮助，请参考：
- `/skills autonomous-ai-agents/multi-agent-project-builder` - 查看完整 Skill 文档
- `/skills autonomous-ai-agents/multi-agent-coordination` - 多 Agent 协作基础
