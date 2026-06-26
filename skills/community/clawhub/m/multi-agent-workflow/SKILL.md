---
name: multi-agent-workflow
version: 1.0.3
description: 多Agent协作工作流 v1.0.3。让多个AI Agent组成团队，协同完成复杂任务。支持任务拆分、角色分配、结果汇总、任务管理。
---

# Multi Agent Workflow - 多Agent协作工作流

## 快速开始

```bash
cd scripts
python workflow.py --help
```

## 目录结构

```
multi-agent-workflow/
├── SKILL.md
├── README.md
├── scripts/
│   └── workflow.py
```

## 工作流程

1. 接收任务
2. 拆分任务
3. 分配角色
4. 并行执行
5. 汇总结果

## 更新日志

### v1.0.3 (2026-03-22)
- 修复：Windows控制台UTF-8编码输出问题

### v1.0.2 (2026-03-21)
- 新增：TaskManager任务管理器
- 新增：split_task任务拆分
- 新增：自动角色分配
