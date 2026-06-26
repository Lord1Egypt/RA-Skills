# 我的多 Agent 项目

这是一个使用 **多 Agent 项目构建器** 创建的项目。

## 📋 项目概述

- **项目名称**: [填写项目名称]
- **项目类型**: [填写项目类型]
- **项目描述**: [填写项目描述]

## 🚀 快速开始

### 1. 配置项目

编辑 `PROJECT_CONFIG.yaml` 文件，配置你的项目需求：

```yaml
project:
  name: "你的项目名称"
  type: "web-app"
  description: "详细描述你的项目"
```

### 2. 在 Hermes 中执行

打开 Hermes，进入项目目录，然后发送：

```
我要使用多 Agent 协作来完成这个项目，请参考 PROJECT_CONFIG.yaml。
```

### 3. 查看结果

所有输出会保存在 `outputs/` 目录中。

## 📁 项目结构

```
.
├── PROJECT_CONFIG.yaml      # 项目配置文件
├── EXECUTION_GUIDE.md       # 执行指南
├── README.md                # 本文件
└── outputs/                 # 输出目录
    ├── 01-requirements/     # 需求分析
    ├── 02-research/         # 技术调研
    ├── 03-architecture/     # 架构设计
    ├── 04-implementation/   # 代码实现
    └── 05-testing/          # 测试报告
```

## 🎯 Agent 角色

| 角色 | 职责 |
|------|------|
| Analyst | 需求分析 |
| Researcher | 技术调研 |
| Architect | 架构设计 |
| Implementer | 代码实现 |
| Tester | 测试验证 |

## 📚 更多帮助

- 查看 `EXECUTION_GUIDE.md` 了解详细执行步骤
- 在 Hermes 中使用 `/skills autonomous-ai-agents/multi-agent-project-builder` 查看完整文档

## 📄 许可证

MIT License
