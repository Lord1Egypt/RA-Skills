---
name: core-executing-plans
description: 当有实施计划需要批量执行时使用，需要人工检查点
---

# Executing Plans - 执行实施计划

## 概述

批量执行实施计划中的任务，在关键点设置人工检查点。

**与 subagent-driven-development 的区别:**
- executing-plans: 批量执行，人工检查点
- subagent-driven-development: 每个任务派发子代理，自动审查

## 流程

### 1. 加载计划

读取计划文件，理解:
- 总体目标
- 任务列表
- 依赖关系
- 验证步骤

### 2. 批量执行

按顺序执行任务，每个任务:
1. 宣布当前任务
2. 遵循 TDD 循环（如果适用）
3. 验证任务完成
4. 提交代码

### 3. 检查点

在以下时机暂停并请求人工确认:
- 每 3-5 个任务后
- 遇到不确定的设计决策
- 测试失败需要决策
- 完成重大里程碑

### 4. 完成

所有任务完成后:
- 汇总完成情况
- 运行完整测试套件
- **REQUIRED SUB-SKILL:** 使用 `core-finishing-branch`

## 检查点模板

```
✅ 已完成任务 1-3:
1. [任务1描述] - 完成
2. [任务2描述] - 完成  
3. [任务3描述] - 完成

📋 下一批任务 4-6:
4. [任务4描述]
5. [任务5描述]
6. [任务6描述]

继续吗？或者有什么需要调整的？
```

## 领域扩展钩子

**如果是嵌入式项目，执行时应:**
- **RECOMMENDED:** 硬件相关任务使用 `embedded-hardware-debug` 验证
- **RECOMMENDED:** 驱动开发任务使用 `embedded-driver-development`
- **RECOMMENDED:** 集成任务使用 `embedded-rtos-integration`

## 注意事项

- 严格遵循计划顺序
- 不要跳过验证步骤
- 遇到问题立即停止并报告
- 保持频繁提交
