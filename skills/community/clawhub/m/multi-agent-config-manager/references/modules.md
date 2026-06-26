# 多代理编排引擎 — 模块参考

## 核心模块架构

```
index.js          命令入口 → 解析用户命令 → 调用对应处理器
lib/executor.js   执行引擎 → buildSpawnParams、buildExecutionPlan、看板系统
lib/communication.js  提示词生成 → generateAgentPrompt、generateFeedbackPrompt
lib/modelSelector.js  模型选择 → selectModel、selectBatchModels (异构分配)
lib/retryManager.js   重试管理 → diagnoseFailure、buildRetrySpawn
lib/validator.js      质量验证 → validate、formatValidationReport
lib/aggregator.js     结果聚合 → aggregate、formatAggregation
lib/archiver.js       归档清理 → archiveWorkflow、cleanShared、archiveAndClean
```

## executor.js 导出函数

### spawn 构建
- `buildSpawnParams(profile, task, workflow, options)` — 单个子代理的 sessions_spawn 参数
- `buildParallelSpawnParams(agentNames, workflow, profiles, phaseTasks)` — 批量并行 spawn 参数

### 目录管理
- `buildOutputDirs(workflow, version)` — 创建三层分层目录
- `buildOutputPath(directories, agentName, version)` — 构建输出文件路径

### 看板系统
- `createPlanBoard(workflow, phases, directories)` — 创建计划看板
- `createExecBoard(workflow, directories)` — 初始化执行看板
- `updateExecBoard(execBoard, phaseData, directories)` — 更新阶段状态
- `loadExecBoard(workflowId)` — 加载执行看板
- `formatExecBoard(execBoard)` — 格式化为可读表格

### 执行计划
- `buildExecutionPlan(workflow, profiles)` — 生成完整工作流执行计划
- `saveExecutionPlan(plan, filePath)` — 持久化到 JSON
- `loadExecutionPlan(filePath)` — 从 JSON 加载

### 结果收集
- `collectResults(agentNames, outputDir)` — 从文件系统读取子代理产出
- `validateAgentOutput(agentName, content, goal)` — 验证单个代理产出
- `aggregateResults(results, goal, template)` — 融合所有结果为最终报告
- `buildCriticTask(aggregatedContent, goal, workflowId)` — 构建Critic任务

### 模型选择 (re-export)
- `selectModel(agentRole, options)` — 为单个代理选择最优模型
- `selectBatchModels(agentRoles, options)` — 批量异构选择（不重复）

### 重试管理 (re-export)
- `diagnoseFailure(result)` — 诊断失败类型
- `buildRetrySpawn(originalSpawn, diagnosis)` — 构建重试 spawn 参数
- `assessDegradation(successRate)` — 评估降级级别
- `buildDegradationPlan(successRate, spawns)` — 构建降级计划

### 归档清理 (re-export)
- `archiveWorkflow(workflow, dashboard)` — 归档产出物
- `cleanShared({dryRun})` — 清理临时文件
- `generateFinalSummary(plan, results)` — 生成最终摘要
- `archiveAndClean(workflow, dashboard)` — 一键归档+清理
