# 项目管理 (project_*)

## 项目查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `project_queryMyTodoTasks` | — | — | 我的待办任务数量 |
| `project_queryMyProjects` | — | — | 我负责/参与的项目 |
| `project_queryProjectList` | — | `projectName`(模糊) `status`(计划中/进行中/已完成) `leaderId` `page` `limit` | 项目列表；按姓名查先获取leaderId |
| `project_queryProjectDetail` | `projectId` | — | 项目详情（成员/阶段/预算/成本/关联订单） |

## 项目创建

`project_createProject(projectData: JSON)`

**必填**：`name`

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `code` | 项目编码 | — |
| `description` | 项目描述 | — |
| `orderId` | 关联订单ID | — |
| `contractId` | 关联合同ID | — |
| `categoryId` | 项目分类ID | — |
| `projectBudget` | 项目预算 | — |
| `projectStartTime` | 项目开始时间 | yyyy-MM-dd HH:mm:ss |
| `projectEndTime` | 项目结束时间 | yyyy-MM-dd HH:mm:ss |
| `leaderId` | 负责人ID | 先调 `hr_queryEmployeeList` 获取 |
| `status` | 状态 | — |

> 负责人姓名→ID：先调 `hr_queryEmployeeList` 获取 `leaderId`

## 任务查询

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `project_queryTaskList` | — | `projectId` `status` `executorId` `priority`(1低/2中/3高) `page` `limit` | 任务列表 |
| `project_queryTaskDetail` | `taskId` | — | 任务详情（工时/子任务/评论） |

## 任务创建

`project_createTask(taskData: JSON)`

**必填**：`name` `projectId`

**可选字段**：

| 字段 | 说明 | 枚举值 |
|------|------|--------|
| `phaseId` | 阶段ID | — |
| `parentId` | 父任务ID | 用于创建子任务 |
| `executorId` | 执行人员ID | 先调 `hr_queryEmployeeList` 获取 |
| `priority` | 优先级 | 1低 / 2中 / 3高 |
| `taskType` | 任务类型 | 1研发 / 2测试 / 3设计 / 4产品 / 5项目管理 / 6预研 |
| `estimateHours` | 预计工时 | — |
| `estimateStartTime` | 预计开始时间 | yyyy-MM-dd HH:mm:ss |
| `estimateEndTime` | 预计完成时间 | yyyy-MM-dd HH:mm:ss |
| `description` | 任务描述 | — |
| `remark` | 备注 | — |

> 执行人姓名→ID：先调 `hr_queryEmployeeList` 获取 `executorId`

## 项目分析

| 工具 | 必填 | 可选 | 说明 |
|------|------|------|------|
| `project_queryWorkHoursStats` | `projectId` | — | 项目工时统计 |
| `project_queryProjectCost` | `projectId` | — | 项目成本核算（人工/费用/预算使用率） |
