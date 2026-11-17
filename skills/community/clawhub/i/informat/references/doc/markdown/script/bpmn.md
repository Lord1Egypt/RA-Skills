# informat.bpmn Workflow Operations

## Overview

Use `informat.bpmn` to query and create workflow instances and workflow tasks

## processEngine

ProcessEngine is the core component of the Flowable process engine, responsible for managing process definitions, process instances, tasks, variables, events, and other aspects, providing users with a complete set of process management interfaces.

```javascript
informat.bpmn.processEngine()
```

::: tip Note
This interface requires the license to include the `System Function Call` module

[Refer to ProcessEngine Documentation](https://javadoc.io/static/org.flowable/flowable-engine/6.7.2/org/flowable/engine/ProcessEngine.html)

:::

**Example**

```javascript
// Set workflow task assignee
let processEngine = informat.bpmn.processEngine();
let taskService = processEngine.getTaskService();
taskService.setAssignee('dcc50d2e-0601-11ef-92a9-0e6cd3d9f023', 'zhangsan');
```

## getBpmnProcessDefineList

Query workflow definition list

```javascript
informat.bpmn.getBpmnProcessDefineList(module, query);
```

| Parameter  | Type                                                          | Description |
|----------|-------------------------------------------------------------|----------|
| moduleId | `String`                                                    | Workflow module identifier |
| query    | [BpmnProcessQuery](/guide/script/model.md#bpmnprocessquery) | Query conditions |

**Return Value**

Returns a list of workflow definitions matching the conditions, type is Array<[BpmnProcess](/guide/script/model.md#bpmnprocess)>;

**Example**

::: code-group

```javascript [Call]
informat.bpmn.getBpmnProcessDefineList('flow', {
    accountId: 'zhangsan',
    name: '请假'
})
```
```json [Return Value]
[
  {
    "color": "c2",
    "createTime": 1692861587735,
    "icon": "store",
    "id": "s615lvvta7l7",
    "key": "leave",
    "name": "请假流程",
    "remark": "",
    "rowNumber": 1,
    "updateTime": 1692861587735
  }
]
```
:::

## isMultiInstanceActivity

Check if a node is a multi-instance node

```javascript
informat.bpmn.isMultiInstanceActivity(procDefId, activityId)
```

**Parameters**

| Parameter    | Type       | Description |
|------------|----------|--------|
| procDefId  | `String` | Process definition ID |
| activityId | `String` | Node ID |

**Return Value**

Returns Boolean

**Example**

::: code-group

```javascript [Call]
informat.bpmn.isMultiInstanceActivity('process_uotiqkw6kk5d:22:56aa67bf-8b65-11ee-adfa-a6c0b0be7615', 'Activity_121ubs9');
```
```json [Return Value]
true
```
:::

## queryInstanceList

Query workflow instance list

```javascript
informat.bpmn.queryInstanceList(module, query)
```

**Parameters**

| Parameter  | Type                                           | Description |
|----------|----------------------------------------------|----------|
| moduleId | `String`                                     | Workflow module identifier |
| query    | [BpmnInstanceQuery](/guide/script/model.md#bpmninstancequery) | Query conditions |

**Return Value**

Returns a list of workflow instances matching the conditions, type is Array<[BpmnInstance](/guide/script/model.md#bpmninstance)>;

**Example - Query workflow instances by status**


::: code-group

```javascript [Call]
informat.bpmn.queryInstanceList('flow', {
    pageIndex: 1,
    pageSize: 10,
    processDefineId: 'leave',
    status: 'doing'
});
```
```json [Return Value]
[
  {
    "active": true,
    "businessKey": "s615lvvta7l7",
    "id": "9cc1e6fa-ca24-11ed-8bc0-be634eacf49a",
    "isActive": true,
    "name": "请假",
    "procDefId": "process_idy5gsmor6ym:78:3663d930-ca24-11ed-b464-9604767b6c5e",
    "procDefName": "请假流程",
    "procInstId": "9cc1e6fa-ca24-11ed-8bc0-be634eacf49a",
    "startTime": 1679649411594,
    "startUserAvatar": "pic15.png",
    "startUserId": "zhangsan",
    "startUserName": "张三",
    "taskCount": 0,
    "tenantId": "g09aj7cus3d8s_croe0zft168y3_pwlfcrmbm46t"
  }
]
```

:::

**Example - Query workflow instances by data table record ID**

::: code-group

```javascript [Call]
informat.bpmn.queryInstanceList('flow', {
    pageIndex: 1,
    pageSize: 10,
    status: 'doing',
    processDefineId: 'leave',
    varList: [{ 'name': 'form_recordId', 'value': 'vem8fxf4ooztl' }]
});
```
```json [Return Value]
[
  {
    "active": true,
    "businessKey": "s615lvvta7l7",
    "id": "9cc1e6fa-ca24-11ed-8bc0-be634eacf49a",
    "isActive": true,
    "name": "请假",
    "procDefId": "process_idy5gsmor6ym:78:3663d930-ca24-11ed-b464-9604767b6c5e",
    "procDefName": "请假流程",
    "procInstId": "9cc1e6fa-ca24-11ed-8bc0-be634eacf49a",
    "startTime": 1679649411594,
    "startUserAvatar": "pic15.png",
    "startUserId": "zhangsan",
    "startUserName": "张三",
    "taskCount": 0,
    "tenantId": "g09aj7cus3d8s_croe0zft168y3_pwlfcrmbm46t"
  }
]
```
:::

## addComment

Add a comment

```javascript
informat.bpmn.addComment(moduleId, taskId, msg)
```

**Parameters**

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Task ID |
| msg      | `String` | Comment content |

**Return Value**

Returns the ID of the newly added comment

**Example**

::: code-group

```javascript [Call]
informat.bpmn.addComment('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'The weather is great today');
```
```text [Return Value]
c5cyqgj06avp0
```

:::

::: warning Note
The message format stored in the database is:

```json
{
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "The weather is great today"
        }
      ]
    }
  ]
}
```

:::

## addCommentWithUser

Add a comment with a specified user

```javascript
informat.bpmn.addCommentWithUser(moduleId, taskId, msg, userId);
```

**Parameters**

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Task ID |
| msg      | `String` | Comment content |
| userId   | `String` | Specified comment user ID |

**Return Value**

Returns the ID of the newly added comment

**Example**

::: code-group

```javascript [Call]
informat.bpmn.addCommentWithUser('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'Approved', 'zhangsan');
```
```text [Return Value]
c263580f-9402-11ee-b865-eed108c67451
```

:::

::: warning Note
The message format stored in the database is:

```json
{
  "type": "doc",
  "content": [
    {
      "type": "paragraph",
      "content": [
        {
          "type": "text",
          "text": "Approved"
        }
      ]
    }
  ]
}
```

:::

## deleteComment

Delete a comment

```javascript
informat.bpmn.deleteComment(moduleId, taskId, id)
```

**Parameters**

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Task ID |
| id       | `String` | Comment ID |

**Return Value**

Number of comments deleted

**Example**

::: code-group

```javascript [Call]
informat.bpmn.deleteComment('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'b8sy2k46dfckh');
```
```text [Return Value]
1
```

:::

## queryCommentListCount

Query the total count of workflow task comments

```javascript
informat.bpmn.queryCommentListCount(moduleId, query);
```

| Parameter  | Type                                          | Description |
|----------|---------------------------------------------|----------|
| moduleId | `String`                                    | Workflow module identifier |
| query    | [BpmnCommentQuery](/guide/script/model.md#bpmncommentquery) | Query conditions |

**Return Value**

Returns the total count of comments matching the conditions, type is `Integer`

**Example**

::: code-group

```javascript [Call]
informat.bpmn.queryCommentListCount('flow', {
    procInstId: '1554f565-3e48-11ed-8392-a210f8dfa819',
    taskId: 'bf5e798f-3f1b-11ed-b5f4-a210f8dfa819'
});
```
```text [Return Value]
1
```

:::

## queryCommentList

Query workflow comment list

```javascript
informat.bpmn.queryCommentList(module, query);
```

| Parameter  | Type                                          | Description |
|----------|---------------------------------------------|----------|
| moduleId | `String`                                    | Workflow module identifier |
| query    | [BpmnCommentQuery](/guide/script/model.md#bpmncommentquery) | Query conditions |

**Return Value**

Returns a list of workflow comments matching the conditions, type is Array<[BpmnComment](/guide/script/model.md#bpmncomment)>;

**Example**


::: code-group

```javascript [Call]
informat.bpmn.queryCommentList('flow', {
    pageIndex: 1,
    pageSize: 10,
    moduleId: 'flow',
    procInstId: '1554f565-3e48-11ed-8392-a210f8dfa819',
    taskId: 'bf5e798f-3f1b-11ed-b5f4-a210f8dfa819'
});
```
```json [Return Value]
[
  {
    "userId": "liutao",
    "procInstId": "9cc1e6fa-ca24-11ed-8bc0-be634eacf49a",
    "taskId": "15571850-3e48-11ed-8392-a210f8dfa819",
    "startTime": 1664271502000,
    "message": "{\"type\":\"doc\",\"content\":[{\"type\":\"paragraph\",\"content\":[{\"type\":\"text\",\"text\":\"同意\"}]}]}"
  }
]
```

:::

## queryInstanceListCount

Query the total count of workflow instances

```javascript
informat.bpmn.queryInstanceListCount(moduleId, query);
```

| Parameter  | Type                                           | Description |
|----------|----------------------------------------------|----------|
| moduleId | `String`                                     | Workflow module identifier |
| query    | [BpmnInstanceQuery](/guide/script/model.md#bpmninstancequery) | Query conditions |

**Return Value**

Returns the total count of workflow instances matching the conditions, type is `Integer`

**Example**

::: code-group

```javascript [Call]
informat.bpmn.queryInstanceListCount('flow', {
    moduleId: 'flow',
    processDefineId: 'insertUser',
    status: 'doing'
});
```
```text [Return Value]
1
```

:::

## queryInstanceById

Query a workflow instance

```javascript
informat.bpmn.queryInstanceById(moduleId, instanceId);
```

| Parameter    | Type       | Description |
|------------|----------|----------|
| moduleId   | `String` | Workflow module identifier |
| instanceId | `String` | Process instance ID |

**Return Value**

Returns the matching instance, type is [BpmnInstance](/guide/script/model.md#bpmninstance)

**Example**


::: code-group

```javascript [Call]
informat.bpmn.queryInstanceById('flow', '9cc1e6fa-ca24-11ed-8bc0-be634eacf49a');
```
```json [Return Value]
{
  "active": true,
  "businessKey": "s615lvvta7l7",
  "id": "9cc1e6fa-ca24-11ed-8bc0-be634eacf49a",
  "isActive": true,
  "name": "请假",
  "procDefId": "process_idy5gsmor6ym:78:3663d930-ca24-11ed-b464-9604767b6c5e",
  "procDefName": "请假流程",
  "procInstId": "9cc1e6fa-ca24-11ed-8bc0-be634eacf49a",
  "startTime": 1679649411594,
  "startUserAvatar": "pic15.png",
  "startUserId": "zhangsan",
  "startUserName": "zhangsan",
  "taskCount": 0,
  "tenantId": "g09aj7cus3d8s_croe0zft168y3_pwlfcrmbm46t"
}
```

:::

## queryTaskList

Query workflow task list

```javascript
informat.bpmn.queryTaskList(moduleId, query);
```

| Parameter  | Type                                       | Description |
|----------|------------------------------------------|----------|
| moduleId | `String`                                 | Workflow module identifier |
| query    | [BpmnTaskQuery](/guide/script/model.md#bpmntaskquery) | Query conditions |

**Return Value**

Returns a list of tasks matching the conditions, type is Array<[BpmnTask](/guide/script/model.md#bpmntask)>;

**Example**


::: code-group

```javascript [Call]
informat.bpmn.queryTaskList('flow', {
    pageIndex: 1,
    pageSize: 10,
    procInstId: '9cc1e6fa-ca24-11ed-8bc0-be634eacf49a',
    status: 'doing'
});
```
```json [Return Value]
[
  {
    "assignee": "zhangsan",
    "assigneeAvatar": "c4b936e826fe45b38e1b4072c79a7a79.jpg",
    "assigneeName": "张三",
    "duration": 0,
    "executionId": "9cdf8124-ca24-11ed-8bc0-be634eacf49a",
    "id": "9cf63d7a-ca24-11ed-8bc0-be634eacf49a",
    "name": "部门经理审批",
    "procDefId": "process_idy5gsmor6ym:78:3663d930-ca24-11ed-b464-9604767b6c5e",
    "procDefName": "请假流程",
    "procInstId": "9cc1e6fa-ca24-11ed-8bc0-be634eacf49a",
    "procInstName": "请假",
    "startTime": 1679649411860,
    "startUserAvatar": "pic15.png",
    "startUserId": "zhangsan",
    "startUserName": "zhangsan",
    "taskDefKey": "Activity_0ofrc9c",
    "tenantId": "g09aj7cus3d8s_croe0zft168y3_pwlfcrmbm46t"
  }
]
```

:::

## queryTaskListCount

Query the total count of workflow tasks

```javascript
informat.bpmn.queryTaskListCount(moduleId, query);
```

| Parameter  | Type              | Description |
|----------|-----------------|----------|
| moduleId | `String`        | Workflow module identifier |
| query    | [BpmnTaskQuery](/guide/script/model.md#bpmntaskquery) | Query conditions |

**Return Value**

Returns the total count of tasks matching the conditions, type is `Integer`

**Example**

::: code-group

```javascript [Call]
informat.bpmn.queryTaskListCount('flow', {
    procInstId: '9cc1e6fa-ca24-11ed-8bc0-be634eacf49a',
    status: 'doing'
});
```
```text [Return Value]
1
```
:::


## queryTaskById

Query a workflow task

```javascript
informat.bpmn.queryTaskById(moduleId, taskId);
```

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Task ID |

**Return Value**

Returns the matching task, type is [BpmnTask](/guide/script/model.md#bpmntask)

**Example**

::: code-group

```javascript [Call]
informat.bpmn.queryTaskById('flow', '9cf63d7a-ca24-11ed-8bc0-be634eacf49a');
```
```json [Return Value]
{
  "assignee": "zhangsan",
  "assigneeAvatar": "c4b936e826fe45b38e1b4072c79a7a79.jpg",
  "assigneeName": "zhangsan",
  "duration": 0,
  "executionId": "9cdf8124-ca24-11ed-8bc0-be634eacf49a",
  "id": "9cf63d7a-ca24-11ed-8bc0-be634eacf49a",
  "name": "部门经理审批",
  "procDefId": "process_idy5gsmor6ym:78:3663d930-ca24-11ed-b464-9604767b6c5e",
  "procDefName": "请假流程",
  "procInstId": "9cc1e6fa-ca24-11ed-8bc0-be634eacf49a",
  "procInstName": "请假",
  "startTime": 1679649411860,
  "startUserAvatar": "pic15.png",
  "startUserId": "zhangsan",
  "startUserName": "zhangsan",
  "taskDefKey": "Activity_0ofrc9c",
  "tenantId": "g09aj7cus3d8s_croe0zft168y3_pwlfcrmbm46t"
}
```

:::

## setInstanceVar

Set a process instance variable

```javascript
informat.bpmn.setInstanceVar(moduleId, instanceId, name, value);
```

| Parameter    | Type       | Description |
|------------|----------|----------|
| moduleId   | `String` | Workflow module identifier |
| instanceId | `String` | Process instance ID |
| name       | `String` | Variable name |
| value      | `Object` | Variable value |

**Example**

```javascript
informat.bpmn.setInstanceVar('flow', 'a8bbc752-24af-11ef-bcd1-a6c0b0be7615', 'userName', '张三');
```

## getInstanceVar

Get a process instance variable

```javascript
informat.bpmn.getInstanceVar(moduleId, instanceId, name);
```

| Parameter    | Type       | Description |
|------------|----------|----------|
| moduleId   | `String` | Workflow module identifier |
| instanceId | `String` | Process instance ID |
| name       | `String` | Variable name. For example, `form_recordId` retrieves the record ID of the workflow start table, and `form` retrieves the start table's record data object |

**Return Value**

Type `Object`, returns the variable value

**Example**

::: code-group

```javascript [Call]
informat.bpmn.getInstanceVar('flow', '9cc1e6fa-ca24-11ed-8bc0-be634eacf49a', 'userName');
```
```text [Return Value]
张三
```

:::

## getInstanceVars

Get all process instance variables

```javascript
informat.bpmn.getInstanceVars(moduleId, instanceId);
```

| Parameter    | Type       | Description |
|------------|----------|----------|
| moduleId   | `String` | Workflow module identifier |
| instanceId | `String` | Process instance ID |

**Return Value**

Type `Object`, returns all variable key-value pairs

**Example**

::: code-group

```javascript [Call]
informat.bpmn.getInstanceVars('flow', '9cc1e6fa-ca24-11ed-8bc0-be634eacf49a');
```
```json [Return Value]
{
  "reason": "家里有事",
  "instanceId": "9cc1e6fa-ca24-11ed-8bc0-be634eacf49a",
  "form": {
    "approver": {
      "avatar": "c4b936e826fe45b38e1b4072c79a7a79.jpg",
      "id": "zhangsan",
      "name": "张三"
    },
    "id": "isvuoz412f1ve",
    "title": "333",
    "day": 5,
    "status": "1"
  },
  "initiator": "zhangsan",
  "project": "项目管理",
  "taskName": "任务",
  "userName": "张三",
  "taskStatus": "进行中"
}
```

:::

## setInstanceLocalVar

Set a process instance local variable

```javascript
informat.bpmn.setInstanceLocalVar(moduleId, instanceId, name, value);
```

| Parameter    | Type       | Description |
|------------|----------|----------|
| moduleId   | `String` | Workflow module identifier |
| instanceId | `String` | Process instance ID |
| name       | `String` | Variable name |
| value      | `Object` | Variable value |

**Example**

```javascript
informat.bpmn.setInstanceLocalVar('flow', 'a8bbc752-24af-11ef-bcd1-a6c0b0be7615', 'project', '项目管理');
```

## getInstanceLocalVar

Get a process instance local variable

```javascript
informat.bpmn.getInstanceLocalVar(moduleId, instanceId, name);
```

| Parameter    | Type       | Description |
|------------|----------|----------|
| moduleId   | `String` | Workflow module identifier |
| instanceId | `String` | Process instance ID |
| name       | `String` | Variable name |

**Return Value**

Type `Object`, returns the variable value

**Example**

::: code-group

```javascript [Call]
informat.bpmn.getInstanceLocalVar('flow', 'a8bbc752-24af-11ef-bcd1-a6c0b0be7615', 'project');

```
```text [Return Value]
项目管理
```

:::

## setTaskVar

Set a process task variable

```javascript
informat.bpmn.setTaskVar(moduleId, taskId, name, value);
```

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |
| name     | `String` | Variable name |
| value    | `Object` | Variable value |

**Example**

```javascript
informat.bpmn.setTaskVar('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'taskName', '任务');
```

## getTaskVar

Get a process task variable

```javascript
informat.bpmn.getTaskVar(moduleId, taskId, name);
```

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |
| name     | `String` | Variable name |

**Return Value**

Type `Object`, returns the variable value

**Example**

::: code-group

```javascript [Call]
informat.bpmn.getTaskVar('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'taskName');
```
```text [Return Value]
任务
```
:::

## getTaskVars

Get process task variables

```javascript
informat.bpmn.getTaskVars(moduleId, taskId, localVariable);
```

| Parameter       | Type        | Description |
|---------------|-----------|----------|
| moduleId      | `String`  | Workflow module identifier |
| taskId        | `String`  | Process task ID |
| localVariable | `Boolean` | Whether to get local variables |

**Return Value**

Type `Object`, returns the variable values

**Example**

::: code-group

```javascript [Call]
informat.bpmn.getTaskVars('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', false);
```
```json [Return Value]
{
  "name": "张三"
}
```

:::

## setTaskLocalVar

Set a process task local variable

```javascript
informat.bpmn.setTaskLocalVar(moduleId, taskId, name, value);
```

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |
| name     | `String` | Variable name |
| value    | `Object` | Variable value |

**Example**

```javascript
informat.bpmn.setTaskLocalVar('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'taskStatus', '进行中');
```

:::warning Important Notes
When the workflow task node has [`Store form data as task variables (task variables are only visible to the current task)`](/guide/bpmn/vars.md#任务变量) enabled, to set form information for the process task variable, the **variable name** must use `${form}_task`, where ${form} is the form identifier
:::

## getTaskLocalVar

Get a process task local variable

```javascript
informat.bpmn.getTaskLocalVar(moduleId, taskId, name);
```

| Parameter    | Type       | Description |
|------------|----------|----------|
| moduleId   | `String` | Workflow module identifier |
| instanceId | `String` | Process instance ID |
| name       | `String` | Variable name |

**Return Value**

Type `Object`, returns the variable value

**Example**

::: code-group

```javascript [Call]
informat.bpmn.getTaskLocalVar('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'taskStatus');
```
```text [Return Value]
进行中
```
:::

:::warning Important Notes
When the workflow task node has [`Store form data as task variables (task variables are only visible to the current task)`](/guide/bpmn/vars.md#任务变量) enabled, to get form information from the process task variable, the **variable name** must use `${form}_task`, where ${form} is the form identifier
:::

## createInstance

Create a workflow instance

```javascript
informat.bpmn.createInstance(moduleId, processDefineId, startUserId, form, vars);
```

| Parameter         | Type       | Description |
|-----------------|----------|----------|
| moduleId        | `String` | Workflow module identifier |
| processDefineId | `String` | Workflow definition identifier |
| startUserId     | `String` | Initiator account ID |
| form            | `Object` | Data table record |
| vars            | `Object` | Startup variables |

**Return Value**

Type `String`, returns the process instance ID

**Example**

::: code-group

```javascript [Call]
let form = {
    level: 1,
    sex: 'man',
    idNo: '450323111111111111',
    post: '刚刚',
    biographicalNote: {
        'id': 'qqc5uxend8j5zg8annd6w.crx',
        'md5': '0b3df75922df4b125309577c93645d0b',
        'name': 'JSON-handle_0.6.1.crx',
        'path': 'do5u69j9ff3ap/jcn3qaf48z6dh/qqc5uxend8j5zg8annd6w.crx',
        'size': 197147,
    },
    name: '肖建宇',
    status: 'atInterview',
};

let vars = {
    startTime: new Date(),
};

informat.bpmn.createInstance('flow', 'insertUser', 'yvkc2kwpy3xzr', form, vars);
```
```text [Return Value]
3cc15cd9-8b9f-11ee-bbf4-a6c0b0be7615
```
:::

## createInstanceWithRecord

Create a workflow instance from an existing data table record

```javascript
informat.bpmn.createInstanceWithRecord(moduleId, processDefineId, startUserId, recordId, vars);
```

| Parameter         | Type       | Description |
|-----------------|----------|----------|
| moduleId        | `String` | Workflow module identifier |
| processDefineId | `String` | Workflow definition identifier |
| startUserId     | `String` | Initiator account ID |
| recordId        | `String` | Existing data table record ID |
| vars            | `Object` | Startup variables |

**Return Value**

Type `String`, returns the process instance ID

**Example**

::: code-group

```javascript [Call]
let vars = {
    startTime: new Date(),
};

informat.bpmn.createInstanceWithRecord('flow', 'insertUser', 'yvkc2kwpy3xzr', 'recordId', vars);
```
```text [Return Value]
3cc15cd9-8b9f-11ee-bbf4-a6c0b0be7615
```
:::

## saveTaskForm

Save a workflow task form

```javascript
informat.bpmn.saveTaskForm(moduleId, taskId, keyRecord);
```

| Parameter | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |
| keyRecord | `Object` | Form keyRecord data |

**Return Value**

Type `String`, returns the associated data table record ID; returns `null` for non-table forms

**Example**

::: code-group

```javascript [Call]
let recordId = informat.bpmn.saveTaskForm('flow', taskId, {
    id: 'recordId',
    name: 'Approval comment'
});
```
```text [Return Value]
recordId
```
:::

## setTaskAssignee

Set the assignee for a task

```javascript
informat.bpmn.setTaskAssignee(moduleId, taskId, userId);
```

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |
| userId   | `String` | Assignee account ID |

**Example**

```javascript
informat.bpmn.setTaskAssignee('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'yvkc2kwpy3xzr');
```

## setTaskOwner

Set the owner of a task

```javascript
informat.bpmn.setTaskOwner(moduleId, taskId, userId);
```

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |
| userId   | `String` | Owner account ID |

**Example**

```javascript
informat.bpmn.setTaskOwner('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'yvkc2kwpy3xzr');
```

## claimTask

Claim a task (assign the responsibility of a task to a specific participant)

::: info
If the task has already been claimed, it cannot be claimed again.
:::

```javascript
informat.bpmn.claimTask(moduleId, taskId, userId);
```

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |
| userId   | `String` | Assignee account ID |

**Example**

```javascript
informat.bpmn.claimTask('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'zhangsan');
```

## unclaimTask

Unclaim a task

```javascript
informat.bpmn.unclaimTask(moduleId, taskId);
```

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |

**Example**

```javascript
informat.bpmn.unclaimTask('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615');
```

## transferTask

Transfer a task (transfer ownership and processing rights from the current participant to another participant)

```javascript
informat.bpmn.transferTask(moduleId, taskId, userId);
```

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |
| userId   | `String` | Assignee account ID |

**Example**

```javascript
informat.bpmn.transferTask('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'zhangsan');
```

## delegateTask

Delegate a task (transfer the responsibility of a task from the current participant to another participant)

```javascript
informat.bpmn.delegateTask(moduleId, taskId, userId, autoDelegate);
```

| Parameter      | Type        | Description |
|--------------|-----------|----------|
| moduleId     | `String`  | Workflow module identifier |
| taskId       | `String`  | Process task ID |
| userId       | `String`  | Assignee account ID |
| autoDelegate | `Boolean` | Whether to auto-delegate |

::: warning Important Notes
Note that when `autoDelegate` is true, you need to ensure that auto-delegation rules have been defined to ensure the task can be correctly delegated to the appropriate participant. Also, ensure that auto-delegation does not cause infinite loops or other issues to maintain process stability and reliability.
:::

**Example**

```javascript
informat.bpmn.delegateTask('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'zhangsan', true);
```

## getIdentityLinksForTask

Get the identity link list associated with a task

```javascript
informat.bpmn.getIdentityLinksForTask(moduleId, taskId);
```

::: info
Used to query participants or candidates related to a task. By querying the identity link list, you can determine which users or roles are associated with the task and manage task authorization accordingly
:::

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |

**Return Value**

Type Array<[BpmnIdentityLink](/guide/script/model.md#bpmnidentitylink)>;

**Example**

::: code-group

```javascript [Call]
informat.bpmn.getIdentityLinksForTask('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615');
```
```json [Return Value]
[
  {
    "groupId": "admin",
    "id": "662e2b7b-e8e5-11ed-9724-9604767b6c5e",
    "taskId": "a8c27e21-24af-11ef-bcd1-a6c0b0be7615",
    "type": "candidate"
  },
  {
    "taskId": "a8c27e21-24af-11ef-bcd1-a6c0b0be7615",
    "type": "owner",
    "userId": "zhangsan"
  }
]
```
:::

## addTaskCandidateRole

Add a candidate role to a task

```javascript
informat.bpmn.addTaskCandidateRole(moduleId, taskId, roleId);
```

::: tip
Candidate roles are application roles that can participate in task processing, such as "Developer", "Tester", etc.
:::

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |
| roleId   | `String` | Application role ID |

**Example**

```javascript
informat.bpmn.addTaskCandidateRole('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'tester');
```

## deleteTaskCandidateRole

Delete a candidate role from a task

```javascript
informat.bpmn.deleteTaskCandidateRole(moduleId, taskId, roleId);
```

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |
| roleId   | `String` | Application role ID |

**Example**

```javascript
informat.bpmn.deleteTaskCandidateRole('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'tester');
```

## addTaskCandidateUser

Add a candidate user to a task

```javascript
informat.bpmn.addTaskCandidateUser(moduleId, taskId, userId);
```

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |
| userId   | `String` | Candidate user ID |

**Example**

```javascript
informat.bpmn.addTaskCandidateUser('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'zhangsan');
```

## deleteTaskCandidateUser

Delete a candidate user from a task

```javascript
informat.bpmn.deleteTaskCandidateUser(moduleId, taskId, userId);
```

| Parameter  | Type       | Description |
|----------|----------|----------|
| moduleId | `String` | Workflow module identifier |
| taskId   | `String` | Process task ID |
| userId   | `String` | Candidate user ID |

**Example**

```javascript
informat.bpmn.deleteTaskCandidateUser('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'zhangsan');
```

## completeTask

Complete a task

```javascript
informat.bpmn.completeTask(moduleId, taskId, variables);
```

| Parameter   | Type       | Description |
|-----------|----------|--------------------------|
| moduleId  | `String` | Workflow module identifier |
| taskId    | `String` | Process task ID |
| variables | `Object` | Output data and process variables to pass to subsequent steps when completing the task |

**Example**

```javascript
informat.bpmn.completeTask('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', null);
```

## moveToActivity

Move a process node from the current position to another node

```javascript
informat.bpmn.moveToActivity(moduleId, taskId, targetActivityId);
```

| Parameter          | Type       | Description |
|------------------|----------|-----------------------------------------|
| moduleId         | `String` | Workflow module identifier |
| taskId           | `String` | Process task ID |
| targetActivityId | `String` | Target node ID (can be found in Workflow "Set Process Diagram >> Select Node >> Basic Info") |

**Example**

```javascript
informat.bpmn.moveToActivity('flow', 'a8c27e21-24af-11ef-bcd1-a6c0b0be7615', 'Activity_0y15knc');
```

## revokeInstance

Revoke a process instance

```javascript
informat.bpmn.revokeInstance(moduleId, instanceId, reason);
```

| Parameter    | Type       | Description |
|------------|----------|----------|
| moduleId   | `String` | Workflow module identifier |
| instanceId | `String` | Process instance ID |
| reason     | `String` | Revocation reason |

**Example**

```javascript
informat.bpmn.revokeInstance('flow', 'a8bbc752-24af-11ef-bcd1-a6c0b0be7615', 'Cancel process');
```

## deleteInstance

Delete a process instance

```javascript
informat.bpmn.deleteInstance(moduleId, instanceId, reason);
```

::: warning Important Notes
When a process instance is deleted, the process will be terminated and all data and state information related to the process instance will be cleared.
:::

| Parameter    | Type       | Description |
|------------|----------|----------|
| moduleId   | `String` | Workflow module identifier |
| instanceId | `String` | Process instance ID |
| reason     | `String` | Deletion reason |

**Example**

```javascript
informat.bpmn.deleteInstance('flow', 'a8bbc752-24af-11ef-bcd1-a6c0b0be7615', 'Delete process');
```

## sendMessage

Send a message to a process instance or execution instance

```javascript
informat.bpmn.sendMessage(moduleId, instanceId, messageName);
```

| Parameter     | Type       | Description |
|-------------|----------|----------|
| moduleId    | `String` | Workflow module identifier |
| instanceId  | `String` | Process instance ID |
| messageName | `String` | Message name |

**Example**

```javascript
informat.bpmn.sendMessage('flow', '9cd49233-24b2-11ef-bcd1-a6c0b0be7615', 'Message A');
```

## sendSignal

Send a signal to a process instance or execution instance

```javascript
informat.bpmn.sendSignal(moduleId, instanceId, signalName);
```

| Parameter    | Type       | Description |
|------------|----------|----------|
| moduleId   | `String` | Workflow module identifier |
| instanceId | `String` | Process instance ID |
| signalName | `String` | Signal name |

**Example**

```javascript
informat.bpmn.sendSignal('flow', '9cd49233-24b2-11ef-bcd1-a6c0b0be7615', 'Signal A');
```

## trigger

Trigger a waiting process instance

```javascript
informat.bpmn.trigger(moduleId, instanceId, activityId);
```

| Parameter    | Type       | Description |
|------------|----------|----------------------------|
| moduleId   | `String` | Workflow module identifier |
| instanceId | `String` | Process instance ID |
| activityId | `String` | Intermediate event ID (can be viewed in the Basic Info of the process design node) |

**Example**

```javascript
informat.bpmn.trigger('flow', '9cd49233-24b2-11ef-bcd1-a6c0b0be7615', 'Activity_0jl4nsq');
```

## getProcessDefineXml

Get the XML content of a workflow definition

```javascript
informat.bpmn.getProcessDefineXml(moduleId, procDefId);
```

| Parameter   | Type       | Description |
|-----------|----------|----------|
| moduleId  | `String` | Workflow module identifier |
| procDefId | `String` | Process definition ID |

**Example**


::: code-group

```javascript [Call]
informat.bpmn.getProcessDefineXml('flow', 'process_idy5gsmor6ym:100:ae4923cb-6d64-11ee-a8da-eed108c67451');
```

```xml [Return Value]
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL" xmlns:flowable="http://flowable.org/bpmn"
             xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI" xmlns:di="http://www.omg.org/spec/DD/20100524/DI"
             xmlns:dc="http://www.omg.org/spec/DD/20100524/DC" xmlns:informat="http://informat.cn/schema/bpmn/ip"
             xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" targetNamespace="Examples">
    <process id="process_uotiqkw6kk5d" name="项目变更流程" isExecutable="true"
    ...
    >
    <message id="message" name="消息"/>
    <bpmndi:BPMNDiagram id="BPMNDiagram_1"
    ...
    >
</definitions>
```
:::


## getProcessDefineXmlObject

Parse the workflow definition XML and return the corresponding JSON object

```javascript
informat.bpmn.getProcessDefineXmlObject(moduleId, procDefId);
```

| Parameter   | Type       | Description |
|-----------|----------|----------|
| moduleId  | `String` | Workflow module identifier |
| procDefId | `String` | Process definition ID |


**Return Value**

Returns the matching task, type is [BpmnTask](/guide/script/model.md#bpmnprocessxml)

**Example**

::: code-group

```javascript [Call]
informat.bpmn.getProcessDefineXml('flow', 'process_rzuwivdv487t:1:8aed09cb-fd70-11f0-ae9f-feb6f6e499c9');
```

```json [Return Value]
{
  "flowList": [
    {
      "id": "Flow_ToSupervisor",
      "name": "提交审批",
      "remark":"同意",
      "sourceRef": "StartEvent_1",
      "targetRef": "UserTask_DirectSupervisor"
    },
    {
      "id": "Flow_Approve",
      "name": "同意",
      "sourceRef": "UserTask_DirectSupervisor",
      "targetRef": "EndEvent_Approve"
    },
    {
      "id": "Flow_Reject",
      "conditionExpression":"${form.totalDays==3}"
      "name": "驳回",
      "sourceRef": "UserTask_DirectSupervisor",
      "targetRef": "EndEvent_Reject"
    }
  ],
  "id": "process_rzuwivdv487t",
  "name": "请假审批流程",
  "nodeList": [
    {
      "id": "StartEvent_1",
      "name": "",
      "type": "startEvent"
    },
    {
      "id": "UserTask_DirectSupervisor",
      "name": "直接上级审批",
      "taskSetting": {
        "autocompleteNodeIds": [],
        "enableAutocomplete": false,
        "formSetting": {
          "completeSetVarList": [
            {
              "expression": "${Context.userId()}",
              "fieldId": "sruifsds4sqgd"
            },
            {
              "expression": "${Date.sysdate()}",
              "fieldId": "eu26q3x2tjwfc"
            }
          ],
          "enableShowProcessInfo": false,
          "formDesignerFieldSettingList": [],
          "formType": "Form",
          "id": "form",
          "localVariable": false,
          "tableFieldSettingList": [
            {
              "editable": false,
              "id": "lqvcgyi7g9z51",
              "visible": true
            },
            {
              "editable": false,
              "id": "utpt26idm3yg4",
              "visible": true
            },
            {
              "editable": false,
              "id": "wic79p7snatwg",
              "visible": true
            },
            {
              "editable": false,
              "id": "l88pwp787rghc",
              "visible": true
            },
            {
              "editable": false,
              "id": "rrllebhnpehsr",
              "visible": true
            },
            {
              "editable": false,
              "id": "yml19s62xf8ch",
              "visible": true
            },
            {
              "editable": false,
              "id": "qphuwqxdqf9l3",
              "visible": true
            },
            {
              "editable": false,
              "id": "qw5sx5kzv1y8t",
              "visible": true
            },
            {
              "editable": false,
              "id": "rsovlr2l2bdan",
              "visible": true
            },
            {
              "editable": false,
              "id": "sruifsds4sqgd",
              "visible": true
            },
            {
              "editable": false,
              "id": "eu26q3x2tjwfc",
              "visible": true
            },
            {
              "editable": true,
              "id": "ukjoz8ztq3m5m",
              "visible": true
            }
          ],
          "tableId": "h6u3t0in1tca2",
          "toolBarButtonList": [
            {
              "action": "TaskComplete",
              "actionSetting": {
                "enableComment": false,
                "bpmnModuleId": "nn2fbs4iv0uh1",
                "taskIdExpression": "${task.id}",
                "tableId": "h6u3t0in1tca2"
              },
              "buttonSetting": {
                "enableConfirm": false,
                "hideName": false,
                "icon": "check-double",
                "plain": false,
                "round": false,
                "type": "primary"
              },
              "controlType": "button",
              "hideExpression": "${task.endTime != null || task.assignee != user.id}",
              "id": "approve",
              "inputSetting": {
                "width": 200
              },
              "isDirectory": false,
              "labelSetting": {
                "bold": false,
                "fontSize": 13
              },
              "name": "同意",
              "selectSetting": {
                "multiple": false,
                "optionList": [],
                "width": 200
              },
              "switchSetting": {
                "type": "primary"
              }
            },
            {
              "action": "TaskMoveToActivity",
              "actionSetting": {
                "activityId": "EndEvent_Reject",
                "enableComment": true,
                "bpmnModuleId": "nn2fbs4iv0uh1",
                "taskIdExpression": "${task.id}",
                "tableId": "h6u3t0in1tca2"
              },
              "buttonSetting": {
                "enableConfirm": false,
                "hideName": false,
                "icon": "check-double",
                "plain": false,
                "round": false,
                "type": "primary"
              },
              "controlType": "button",
              "hideExpression": "${task.endTime != null || task.assignee != user.id}",
              "id": "reject",
              "inputSetting": {
                "width": 200
              },
              "isDirectory": false,
              "labelSetting": {
                "bold": false,
                "fontSize": 13
              },
              "name": "驳回",
              "selectSetting": {
                "multiple": false,
                "optionList": [],
                "width": 200
              },
              "switchSetting": {
                "type": "primary"
              }
            }
          ]
        },
        "noAssigneeHandleType": "UnClaimed",
        "userAction": "Form"
      },
      "type": "userTask"
    },
    {
      "id": "EndEvent_Approve",
      "name": "批准完成",
      "type": "endEvent"
    },
    {
      "id": "EndEvent_Reject",
      "name": "驳回完成",
      "type": "endEvent"
    }
  ],
  "startSetting": {
    "activityUserList": [],
    "draftNameVar": "${String.concat(User.user(initiator).name,'的请假申请草稿')}",
    "enableStartForm": true,
    "formSetting": {
      "completeSetVarList": [],
      "enableShowProcessInfo": false,
      "formDesignerFieldSettingList": [],
      "formType": "Form",
      "id": "form",
      "localVariable": false,
      "tableFieldSettingList": [
        {
          "editable": false,
          "id": "leaveNo",
          "visible": true
        },
        {
          "editable": false,
          "id": "applicant",
          "visible": true
        },
        {
          "editable": true,
          "id": "leaveType",
          "visible": true
        },
        {
          "editable": true,
          "id": "startDate",
          "visible": true
        },
        {
          "editable": true,
          "id": "endDate",
          "visible": true
        },
        {
          "editable": true,
          "id": "totalDays",
          "visible": true
        },
        {
          "editable": true,
          "id": "reason",
          "visible": true
        },
        {
          "editable": true,
          "id": "attachment",
          "visible": true
        },
        {
          "editable": false,
          "id": "status",
          "visible": true
        }
      ],
      "tableId": "leaveApplication",
      "toolBarButtonList": []
    },
    "instanceNameVar": "${String.concat(User.user(initiator).name,'的请假申请')}",
    "instanceToolbarButtonList": [],
    "startFormToolbarButtonList": [],
    "startVarList": []
  }
}
```
:::


## generateProcessDiagram

Generate a workflow process diagram image

```javascript
informat.bpmn.generateProcessDiagram(moduleId, procDefId, config);
```

| Parameter   | Type                                                  | Description |
|-----------|-----------------------------------------------------|----------|
| moduleId  | `String`                                            | Workflow module identifier |
| procDefId | `String`                                            | Process definition ID |
| config    | [BpmnProcessDiagramConfig](/guide/script/model.md#bpmnprocessdiagramconfig) | Configuration |

**Example**

::: code-group

```javascript [Call]
let config = {
    activityFontName: "宋体",
    labelFontName: "宋体",
    annotationFontName: "宋体",
    highLightedActivities: ['StartEvent_1', 'Activity_0ofrc9c', 'Activity_0i7rzdo'],
    highLightedFlows: ['Flow_061bx1o', 'Flow_0l1tmev', 'Flow_0n92u98'],
    scaleFactor: 1.0,
    drawSequenceFlowNameWithNoLabelDI: false
}
let procDefId = 'process_idy5gsmor6ym:100:ae4923cb-6d64-11ee-a8da-eed108c67451';
let base64Img = informat.bpmn.generateProcessDiagram('flow', procDefId, config);
console.log('base64Img', base64Img);
```
```text [Return Value]
iVBORw0KGgoAAAANSUhEUgAAByYAAAImCAYAAAAWme0EAACAAElEQVR4XuzdCZxkVX33/8MmIuCCgiAiAwKi4...
```

:::

## setProcessInstanceName

Set the process instance name

```javascript
informat.bpmn.setProcessInstanceName(moduleId, instanceId, name);
```

| Parameter    | Type       | Description |
|------------|----------|----------|
| moduleId   | `String` | Workflow module identifier |
| instanceId | `String` | Process instance ID |
| name       | `String` | Instance name |

**Example**

```javascript
informat.bpmn.setProcessInstanceName('flow', 'a8bbc752-24af-11ef-bcd1-a6c0b0be7615', 'New process instance name');
```

## addMultiInstanceExecution

Add a multi-instance execution

```javascript
informat.bpmn.addMultiInstanceExecution(moduleId, activityId, parentExecutionId, variables);
```

| Parameter           | Type       | Description |
|-------------------|----------|-------------------|
| moduleId          | `String` | Workflow module identifier |
| activityId        | `String` | Process node ID |
| parentExecutionId | `String` | Parent execution ID, can be the process instance ID |
| variables         | `Object` | Execution variables |

**Return Value**

Returns the newly added execution ID, type is `String`

**Example**


::: code-group

```javascript [Call]
// Add an approver (lisi) to node A
var variables = {
    'assignee': 'yvkc2kwpy3xzr'	// assignee is the variable name used in the process node assignee field, modify according to your specific case
}
informat.bpmn.addMultiInstanceExecution('flow', 'Activity_0a866jw', 'fa3d9fde-93ff-11ee-b865-eed108c67451', variables);
```
```text [Return Value]
c263580f-9402-11ee-b865-eed108c67451
```

:::

::: warning Important Notes
This interface is only effective for multi-instance nodes
:::

## deleteMultiInstanceExecution

Delete a multi-instance execution

```javascript
informat.bpmn.deleteMultiInstanceExecution(moduleId, executionId, executionIsCompleted);
```

| Parameter              | Type        | Description |
|----------------------|-----------|-------------|
| moduleId             | `String`  | Workflow module identifier |
| executionId          | `String`  | Process node ID |
| executionIsCompleted | `Boolean` | Whether to mark the execution as completed |

**Example**

```javascript
// Delete an approver from node A
informat.bpmn.deleteMultiInstanceExecution('flow', 'a8be867d-24af-11ef-bcd1-a6c0b0be7615', true);
```

::: warning Important Notes
This interface is only effective for multi-instance nodes
:::

## addBpmnTaskCcList

Add CC (carbon copy) recipients to a BPMN task

```javascript
informat.bpmn.addBpmnTaskCcList(taskId, copyUserList);
```

| Parameter        | Type              | Description |
|----------------|-----------------|----------------|
| `taskId`       | `String`        | BPMN task ID |
| `copyUserList` | `Array<String>` | List of CC recipient user IDs to add |

**Example**

```javascript
informat.bpmn.addBpmnTaskCcList('a8c27e21-24af-11ef-bcd1-a6c0b0be7615', ['yvkc2kwpy3xzr']);
```

## deleteBpmnTaskCc

Remove a CC recipient from a BPMN task

```javascript
informat.bpmn.deleteBpmnTaskCc(taskId, copyUserId);
```

| Parameter      | Type       | Description |
|--------------|----------|-----------------|
| `taskId`     | `String` | BPMN task ID |
| `copyUserId` | `String` | User ID to remove from the CC list |

**Example**

```javascript
informat.bpmn.deleteBpmnTaskCc('3cc8fe05-8b9f-11ee-bbf4-a6c0b0be7615', 'zhangsan');
```

## queryBpmnTaskCcList

Retrieve the BPMN task CC recipient list based on the given query

```javascript
informat.bpmn.queryBpmnTaskCcList(query);
```

| Parameter | Type      | Description |
|---------|---------|----------------------|
| `query` | `Query` | Query object to filter BPMN task CC recipients |

Filterable fields

| Parameter      | Type       | Description |
|--------------|----------|------|
| `taskId`     | `String` | Task ID |
| `copyUserId` | `String` | CC user |

**Example**

::: code-group

```javascript [Call]
informat.bpmn.queryBpmnTaskCcList({
    pageIndex: 1,
    pageSize: 10,
    filter: {
        conditionList: [
            { fieldId: 'taskId', opt: 'eq', value: 'taskId' }
        ]
    }
})
```
```json [Return Value]
[
  {
    "copyUserAvatar": "pic7.png",
    "copyUserId": "xwi9jogl4fcx4",
    "copyUserName": "张三",
    "id": "ifpno8kcp60w0",
    "taskId": "fb8ff623-f7ae-11ee-b253-a6c0b0be7615"
  },
  {
    "copyUserAvatar": "383e58e051c849e9bff4f26f432c0764.jpg",
    "copyUserId": "nx8hcjsq4xk8z",
    "copyUserName": "李四",
    "id": "fyyew216vjagc",
    "taskId": "396ebfdd-1770-11ef-b056-a6c0b0be7615"
  }
]
```
:::

## queryBpmnTaskCcListCount

Get the count of BPMN task CC recipients based on the given filter

```javascript
informat.bpmn.queryBpmnTaskCcListCount(filter);
```

| Parameter  | Type       | Description |
|----------|----------|-----------------------|
| `filter` | `Filter` | Filter object to count BPMN task CC recipients |

**Example**

::: code-group

```javascript [Call]
informat.bpmn.queryBpmnTaskCcList({
    conditionList: [
        { fieldId: 'taskId', opt: 'eq', value: 'taskId' }
    ]
})

```
```text [Return Value]
2
```

:::

## getHistoryTaskVariables

Get historical task variables

```javascript
informat.bpmn.getHistoryTaskVariables(taskId);
```

| Parameter | Type       | Description |
|--------|----------|---------|
| taskId | `String` | Process task ID |

**Return Value**

Type `Object`, returns all variable values

**Example**

```javascript
informat.bpmn.getHistoryTaskVariables('9cf63d7a-ca24-11ed-8bc0-be634eacf49a')
```

## getHistoryTaskVariable

Get a historical task variable

```javascript
informat.bpmn.getHistoryTaskVariable(taskId, variableName);
```

| Parameter      | Type       | Description |
|--------------|----------|---------|
| taskId       | `String` | Process task ID |
| variableName | `String` | Variable name |

**Return Value**

Type `Object`, returns the variable value

**Example**

```javascript
informat.bpmn.getHistoryTaskVariable('9cf63d7a-ca24-11ed-8bc0-be634eacf49a', 'form')

```

## deleteTasks

Delete workflow task list

```javascript
informat.bpmn.deleteTasks(moduleId, taskIds, deleteReason, cascade);
```

| Parameter      | Type              | Description |
|--------------|-----------------|--------|
| moduleId     | `String`        | Module identifier |
| taskIds      | `Array<String>` | Task ID list |
| deleteReason | `String`        | Deletion reason |
| cascade      | `Boolean`       | Whether to cascade delete |

**Example**

```javascript
informat.bpmn.deleteTasks('flow', ['9cf63d7a-ca24-11ed-8bc0-be634eacf49a'], 'Test deletion', true);
```

## getStartSetting

Get the process definition start settings

```javascript
informat.bpmn.getStartSetting(moduleKey, defineId);
```

| Parameter   | Type       | Description |
|-----------|----------|--------|
| moduleKey | `String` | Module identifier |
| defineId  | `String` | Process definition ID |

**Return Value**

Return type is [BpmnStartSetting](/guide/script/model.md#bpmnstartsetting), the process start settings information

**Example**

::: code-group

```javascript [Call]
informat.bpmn.getStartSetting('flow', 'h141dq1w5ijpf')
```
```json [Return Value]
{
  "activityUserList": [],
  "enableStartForm": true,
  "formSetting": {
    "completeSetVarList": [],
    "enableShowProcessInfo": false,
    "formDesignerFieldSettingList": [],
    "id": "form",
    "localVariable": false,
    "tableFieldSettingList": [
      {
        "editable": true,
        "id": "y68l84iidbr9l",
        "visible": true
      },
      {
        "editable": true,
        "id": "vn4v208530vfj",
        "visible": true
      },
      {
        "editable": true,
        "id": "gjkb3rq7q44wu",
        "visible": true
      },
      {
        "editable": true,
        "id": "ceumuggdjze5i",
        "visible": true
      },
      {
        "editable": true,
        "id": "t9416rt5uv818",
        "visible": true
      },
      {
        "editable": true,
        "id": "a3rumke2j97m6",
        "visible": true
      }
    ],
    "tableId": "skwl7tkdsh650",
    "toolBarButtonList": []
  },
  "instanceToolbarButtonList": [],
  "startFormToolbarButtonList": [],
  "startVarList": []
}
```

:::

## getTaskSetting

Get task settings

```javascript
informat.bpmn.getTaskSetting(procDefineId, taskDefKey);
```

| Parameter      | Type       | Description |
|--------------|----------|--------|
| procDefineId | `String` | Process definition ID |
| taskDefKey   | `String` | Task definition ID |

**Return Value**

Type `BpmnTaskSetting`

**Example**

::: code-group

```javascript [Call]
informat.bpmn.getTaskSetting('process_swf2089hng2j:1:c0cc319f-7a59-11ef-bb07-0242d99c1a6f', 'Activity_1nky9zn')
```
```json [Return Value]
{
  "autocompleteNodeIds": [],
  "enableAutocomplete": false,
  "formSetting": {
    "completeSetVarList": [],
    "enableShowProcessInfo": false,
    "formDesignerFieldSettingList": [],
    "formType": "Form",
    "id": "form",
    "localVariable": false,
    "tableFieldSettingList": [
      {
        "editable": false,
        "id": "y68l84iidbr9l",
        "visible": true
      },
      {
        "editable": false,
        "id": "vn4v208530vfj",
        "visible": true
      },
      {
        "editable": false,
        "id": "gjkb3rq7q44wu",
        "visible": true
      },
      {
        "editable": false,
        "id": "ceumuggdjze5i",
        "visible": true
      },
      {
        "editable": false,
        "id": "t9416rt5uv818",
        "visible": true
      },
      {
        "editable": false,
        "id": "a3rumke2j97m6",
        "visible": true
      }
    ],
    "tableId": "skwl7tkdsh650",
    "toolBarButtonList": [
      {
        "action": "TaskComplete",
        "actionSetting": {
          "enableComment": false,
          "bpmnModuleId": "b6qe23fkfwlux",
          "taskIdExpression": "${task.id}",
          "varList": [],
          "valueList": [],
          "tableId": "skwl7tkdsh650"
        },
        "buttonSetting": {
          "enableConfirm": false,
          "hideName": false,
          "icon": "check-double",
          "plain": false,
          "round": false,
          "type": "primary"
        },
        "children": [],
        "controlType": "button",
        "hideExpression": "${task.endTime != null || task.assignee != user.id}",
        "id": "w7b5ah41xs1e",
        "inputSetting": {
          "width": 200
        },
        "isDirectory": false,
        "labelSetting": {
          "bold": false,
          "fontSize": 13
        },
        "name": "同意",
        "selectSetting": {
          "multiple": false,
          "optionList": [
          ],
          "width": 200
        },
        "switchSetting": {
          "type": "primary"
        }
      },
      {
        "action": "TaskMoveToEnd",
        "actionSetting": {
          "enableComment": false,
          "bpmnModuleId": "b6qe23fkfwlux",
          "taskIdExpression": "${task.id}",
          "valueList": [],
          "tableId": "skwl7tkdsh650"
        },
        "buttonSetting": {
          "completeExpression": "流程终止成功",
          "confirmMessageExpression": "确认要终止该流程吗？",
          "enableConfirm": true,
          "hideName": false,
          "icon": "stop-circle",
          "plain": false,
          "round": false,
          "type": "danger"
        },
        "children": [],
        "controlType": "button",
        "hideExpression": "${task.endTime != null || task.assignee != user.id}",
        "id": "mum6gdf67m9q",
        "inputSetting": {
          "width": 200
        },
        "isDirectory": false,
        "labelSetting": {
          "bold": false,
          "fontSize": 13
        },
        "name": "终止",
        "selectSetting": {
          "multiple": false,
          "optionList": [
          ],
          "width": 200
        },
        "switchSetting": {
          "type": "primary"
        }
      }
    ]
  },
  "userAction": "Form"
}
```
:::


## getActiveProcessDefineObject

Get the latest deployed XML content by workflow process definition identifier

```javascript
informat.bpmn.getActiveProcessDefineObject(moduleId, processDefineKey);
```

| Parameter        | Type       | Description |
|-----------|----------|----------|
| moduleId  | `String` | Workflow module identifier |
| processDefineKey | `String` | Process definition identifier |


**Example**

```javascript [Call]
informat.bpmn.getActiveProcessDefineObject('workflow', 'leaveApproval');
```

## getBpmnProcessVersionList

Query process definition version list

```javascript
informat.bpmn.getBpmnProcessVersionList(moduleKey, processDefineKey);
```

| Parameter          | Type       | Description |
|------------------|----------|----------|
| moduleKey        | `String` | Workflow module identifier |
| processDefineKey | `String` | Process definition identifier |

**Return Value**

Returns a version list, type is `Array<BpmnProcessVersion>`

| Field                 | Type       | Description |
|---------------------|----------|--------|
| id                  | `String` | Version ID |
| name                | `String` | Name |
| status              | `String` | Status (`None` not configured / `Pending` pending activation / `Running` active / `Finished` completed) |
| startTime           | `Date`   | Effective start time |
| activeTime          | `Date`   | Activation time |
| createAccountId     | `String` | Creator ID |
| createAccountName   | `String` | Creator name |
| createAccountAvatar | `String` | Creator avatar |
| createTime          | `Date`   | Creation time |
| updateTime          | `Date`   | Last modified time |

**Example**

::: code-group

```javascript [Call]
informat.bpmn.getBpmnProcessVersionList('flow', 'leave');
```
```json [Return Value]
[
  {
    "id": "s615lvvta7l7",
    "name": "V1",
    "status": "Running",
    "startTime": 1692861587735,
    "activeTime": 1692861587735,
    "createAccountId": "zhangsan",
    "createAccountName": "张三",
    "createAccountAvatar": "pic15.png",
    "createTime": 1692861587735,
    "updateTime": 1692861587735
  }
]
```
:::

## setProcessCurrentVersion

Set the current version of a process definition

```javascript
informat.bpmn.setProcessCurrentVersion(moduleKey, processDefineKey, versionId);
```

| Parameter          | Type       | Description |
|------------------|----------|----------|
| moduleKey        | `String` | Workflow module identifier |
| processDefineKey | `String` | Process definition identifier |
| versionId        | `String` | Version ID |

**Example**

```javascript
informat.bpmn.setProcessCurrentVersion('flow', 'leave', 's615lvvta7l7');
```
