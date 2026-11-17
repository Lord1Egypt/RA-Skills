<!-- DOCKEY: lsn-1c6f7 -->
This document defines the complete configuration guide and event list for Informat Application Listeners.

# Informat Listener Documentation

## 1. Overview

Listeners are a powerful tool in the Informat AI low-code platform. They monitor specific system events to trigger and execute pre-configured automation programs. Listeners capture specific events in the system (such as data changes, user operations, etc.) and automatically execute corresponding automation programs based on predefined rules and conditions. Automation programs can include data processing, notification sending, external system integration, and more.

Within **Automation** programs or **Scripts**, you can publish a custom **Application Event** using the "Publish Application Event" step. The application event type needs to be pre-configured in the listener settings.

> **Important**: Listeners that are not client-side triggered must not contain interactive steps in their automation programs.

The automation or script accepts a parameter of type `AppEvent`, with the following structure:

```ts
interface AppEvent {
    id: string;      // Event ID
    content: object;  // Event content
}
```

## 2. Transactions

All event listeners (excluding notification sending and client-triggered ones) execute within the same transaction as the trigger point. For example, if an exception is thrown during the execution of an automation program listening to the "Before Record Create" event, all transactions including the record insertion will be rolled back.

For instance, when submitting data that requires rule validation, set up a rule-checking automation program in the "Before Record Create" event listener. If the rules are not satisfied, the automation program executes "Terminate Execution". Upon receiving the "Terminate Execution" command, the system automatically rolls back all transactions, and the data submission fails.

## 3. Event List

### 3.1 Before & After Record Create

Triggered when a user creates a record through a form.

> **TIP**: Creating records via automation or scripts will **not** trigger these events.

**Event trigger order when creating a record:**
1. Trigger the main table's "Before Record Create" event
2. For each sub-table record, trigger "Before Record Create" and "After Record Create" events
3. Trigger the main table's "After Record Create" event

**Before Create Event Content:**
```json
{
    "content":{
        "record":{
            "name":"name","age":0
        },
        "source":"form",
        "tableId":"listenerData"
    },
    "id":"record.create.before"
}
```

**After Create Event Content:**
```json
{
   "content": {
      "afterRecord": {
         "age": 0,
         "id": "d6dhvhodo62nl",
         "name": "name",
         "seq": 2
      },
      "record": {
         "age": 0,
         "name": "name"
      },
      "source": "form",
      "tableId": "listenerData"
   },
   "id": "record.create.after"
}
```

### 3.2 Before & After Record Update

Triggered when a user updates a record through a form.

> **TIP**: Updating records via automation or scripts will **not** trigger these events.

**When updating a record**, sub-tables may involve "Create", "Update", and "Delete" actions. The event trigger order is:
1. Trigger the main table's "Before Record Update" event
2. For newly added sub-table data, trigger "Before Record Create" and "After Record Create" events
3. For updated sub-table data, trigger "Before Record Update" and "After Record Update" events
4. For deleted sub-table data, trigger "Before Record Delete" and "After Record Delete" events
5. Trigger the main table's "After Record Update" event

**Before Update Event Content:**
```json
{
   "content": {
      "beforeRecord": {
         "age": 100,
         "id": "xg2d0hi83cwym",
         "name": "Zhang San",
         "seq": 1
      },
      "record": {
         "id": "xg2d0hi83cwym",
         "name": "Zhang San 1"
      },
      "source": "form",
      "tableId": "listenerData",
      "updateFieldList": [
         "name"
      ]
   },
   "id": "record.update.before"
}
```

**After Update Event Content:**
```json
{
   "content": {
      "afterRecord": {
         "age": 100,
         "id": "xg2d0hi83cwym",
         "name": "Zhang San 1",
         "seq": 1
      },
      "beforeRecord": {
         "age": 100,
         "id": "xg2d0hi83cwym",
         "name": "Zhang San",
         "seq": 1
      },
      "record": {
         "id": "xg2d0hi83cwym",
         "name": "Zhang San 1"
      },
      "source": "form",
      "tableId": "listenerData",
      "updateFieldList": [
         "name"
      ],
      "updateRowCount": 1
   },
   "id": "record.update.after"
}
```

### 3.3 Before & After Record Delete

Triggered when a user deletes a record through a form.

> **TIP**: Deleting records via automation or scripts will **not** trigger these events.

**When deleting a record**, the event trigger order is:
1. Trigger the main table's "Before Record Delete" event
2. Trigger the main table's "After Record Delete" event

> **TIP**: For "Related List" field types, deleting only removes the relationship, not the actual data, so sub-table events will not be triggered.

**Before Delete Event Content:**
```json
{
   "content": {
      "record": {
         "age": 0,
         "id": "d6dhvhodo62nl",
         "name": "example",
         "seq": 2
      },
      "source": "form",
      "tableId": "listenerData"
   },
   "id": "record.delete.before"
}
```

**After Delete Event Content:**
```json
{
   "content": {
      "record": {
         "age": 0,
         "id": "d6dhvhodo62nl",
         "name": "example",
         "seq": 2
      },
      "source": "form",
      "tableId": "listenerData"
   },
   "id": "record.delete.after"
}
```

### 3.4 Record Sort Update

Triggered when a user reorders records by dragging in the table view.

**Before Sort:**
```json
{
   "content": {
      "beforeRowNumber": 4,
      "recordId": "gf13shmq3njqf",
      "source": "form",
      "tableId": "listenerData"
   },
   "id": "record.rownumber.update.before"
}
```

**After Sort:**
```json
{
   "content": {
      "afterRowNumber": 3,
      "beforeRowNumber": 4,
      "recordId": "gf13shmq3njqf",
      "source": "form",
      "tableId": "listenerData"
   },
   "id": "record.rownumber.update.after"
}
```

### 3.5 After Record Comment Create

Triggered when a user posts a comment through a form.

```json
{
   "content": {
      "comment": {
         "content": "Comment content (rich text JSON)",
         "id": 0,
         "parentId": 0,
         "recordId": "xg2d0hi83cwym",
         "tableId": "listenerData"
      }
   },
   "id": "record.comment.create.after"
}
```

### 3.6 After Record Comment Delete

Triggered when a user deletes a comment through a form.

```json
{
   "content": {
      "comment": {
         "content": "Deleted comment content (rich text JSON)",
         "id": 0,
         "parentId": 0,
         "recordId": "xg2d0hi83cwym",
         "tableId": "listenerData"
      }
   },
   "id": "record.comment.delete.after"
}
```

### 3.7 Automation Execution

Listen for three key automation execution events: `Execute Start`, `Execute End`, and `Execute Failed`. Use this listener to log the automation execution process.

Use cases:
- Log execution process for statistical analysis
- Perform global permission checks before execution
- Send execution records to message queues for monitoring systems

**Before Execution:**
```json
{
   "content": {
      "args": ["lefttop"],
      "draft": false,
      "id": "trang7ixclbtg",
      "isDraft": false,
      "uuid": "trang7ixclbtg:sesgv3tgz0el"
   },
   "id": "app.automatic.before"
}
```

**Execution Success:**
```json
{
   "content": {
      "args": ["lefttop"],
      "draft": false,
      "id": "trang7ixclbtg",
      "isDraft": false,
      "uuid": "trang7ixclbtg:sesgv3tgz0el"
   },
   "id": "app.automatic.success"
}
```

### 3.8 Schedule Task Execution

Listen for three key schedule task execution events: `Execute Start`, `Execute Success`, and `Execute Failed`. Use this listener to log the schedule task process.

Use cases:
- Log execution process for statistical analysis
- Send execution records to message queues for monitoring systems

**Before Execution:**
```json
{
   "content": {
      "endTime": 1718092915132,
      "id": "tlijinwmbtnet",
      "name": "Schedule task name",
      "requestId": "arqwu3bsirbh8",
      "serverId": "informat-biz2-prd",
      "startTime": 1718157714369
   },
   "id": "app.schedule.before"
}
```

**Execution Success:**
```json
{
   "content": {
      "endTime": 1718092915132,
      "id": "tlijinwmbtnet",
      "name": "Schedule task name",
      "requestId": "arqwu3bsirbh8",
      "serverId": "informat-biz2-prd",
      "startTime": 1718157714369
   },
   "id": "app.schedule.success"
}
```

### 3.9 Enter Application

The "Enter Application" listener event triggers when a user enters an application from the client.

Use cases:
- Use the "Show Dialog" automation step to display a welcome dialog
- Use the "Set Badge" automation step to display badges on the application icon
- Log user login time to a log table for analysis or auditing

> **TIP**: This listener is client-side triggered, so the automation can include interactive logic.

```json
{
   "eventContent": {
      "app": { ... },
      "platform": "web",
      "query": {
         "appId": "i1mwqy35y88hl"
      },
      "url": "https://next.informat.cn/app/i1mwqy35y88hl",
      "user": { ... }
   },
   "eventId": "app.enter",
   "id": "app.enter"
}
```

### 3.10 Enter Module

The "Enter Module" listener event triggers when a user enters a specific module of an application from the client.

Use cases:
- Use the "Show Dialog" automation step to display a welcome dialog
- Log user access time to a log table for analysis or auditing

> **TIP**: This listener is client-side triggered, so the automation can include interactive logic.

```json
{
   "appId": "i1mwqy35y88hl",
   "eventContent": {
      "app": { ... },
      "moduleKey": "listenerData",
      "platform": "web",
      "query": {
         "appId": "i1mwqy35y88hl",
         "moduleId": "snahtjpjwbz3f"
      },
      "url": "https://next.informat.cn/app/i1mwqy35y88hl/table/snahtjpjwbz3f",
      "user": { ... }
   },
   "eventId": "app.module.enter",
   "id": "app.module.enter",
   "moduleId": "snahtjpjwbz3f"
}
```

### 3.11 Application Publish

Triggered after an application is published.

```json
{
   "content": {
      "appDefineId": "demoApp",
      "appId": "i1mwqy35y88hl",
      "build": 1906,
      "companyId": "icxt9rsd1f0ai",
      "publishUser": "publisher"
   },
   "id": "app.publish"
}
```

### 3.12 Member Events

Member events are triggered after adding, removing, or modifying member roles through the "Member Management" interface.

**After Member Join:**
```json
{
   "content": {
      "appDefineId": "demoApp",
      "appId": "i1mwqy35y88hl",
      "companyId": "icxt9rsd1f0ai",
      "roleList": ["admin"],
      "userId": "bt4tdzx8vtjoe"
   },
   "id": "app.member.add.after"
}
```

**After Member Remove:**
```json
{
   "content": {
      "appDefineId": "demoApp",
      "appId": "i1mwqy35y88hl",
      "companyId": "icxt9rsd1f0ai",
      "roleList": ["admin"],
      "userId": "pacrwba408wd0"
   },
   "id": "app.member.remove.after"
}
```

**After Member Role Update:**
```json
{
   "content": {
      "afterRoleList": ["admin", "ceo", "manager"],
      "appDefineId": "demoApp",
      "appId": "i1mwqy35y88hl",
      "beforeRoleList": ["admin", "ceo"],
      "companyId": "icxt9rsd1f0ai",
      "userId": "yvkc2kwpy3xzr"
   },
   "id": "app.member.role.update.after"
}
```

### 3.13 Task Status Change

Triggered when a workflow task under monitoring performs `Delegate`, `Transfer`, `Jump Node`, `Complete Task`, `Claim Task`, or `Start Task` actions.

> **TIP**: This listener is client-side triggered, so the automation can include interactive logic.

```json
{
    "eventId": "client.bpmn.task.change",
    "eventContent": {
        "app": { ... },
        "query": { ... },
        "moduleId": "ztkva3xsc2vbw",
        "user": { ... },
        "url": "https://next.informat.cn/app/i1mwqy35y88hl/bpmn/ztkva3xsc2vbw"
    },
    "id": "client.bpmn.task.change"
}
```

### 3.14 Process Status Change

Triggered when a monitored workflow is `Revoked` or `Deleted`.

> **TIP**: This listener is client-side triggered, so the automation can include interactive logic.

```json
{
  "eventId": "client.bpmn.process.change",
  "eventContent": {
    "app": { ... },
    "instanceId": "6f5771e7-351d-11ef-b137-a6c0b0be7615",
    "query": { ... },
    "moduleId": "ztkva3xsc2vbw",
    "type": "delete",
    "user": { ... },
    "url": "https://next.informat.cn/app/i1mwqy35y88hl/bpmn/ztkva3xsc2vbw?ri=6f5771e7-351d-11ef-b137-a6c0b0be7615"
  },
  "id": "client.bpmn.process.change"
}
```

### 3.15 After Record Create (Client-side)

Triggered after a record is created via `Form submission` or `Workflow submission`.

> **TIP**: This listener is client-side triggered, so the automation can include interactive logic.

```json
{
    "eventId": "client.record.create.after",
    "eventContent": {
        "app": { ... },
        "query": { ... },
        "tableId": "snahtjpjwbz3f",
        "source": "form",
        "user": { ... },
        "url": "https://next.informat.cn/app/i1mwqy35y88hl/table/snahtjpjwbz3f"
    },
    "id": "client.record.create.after"
}
```

### 3.16 After Record Update (Client-side)

Triggered after a record is updated via `Form submission` or `Workflow submission`.

> **TIP**: This listener is client-side triggered, so the automation can include interactive logic.

```json
{
    "eventId": "client.record.update.after",
    "eventContent": {
        "app": { ... },
        "recordList": ["c67wwyqeth1up"],
        "query": { ... },
        "tableId": "snahtjpjwbz3f",
        "source": "form",
        "user": { ... },
        "url": "https://next.informat.cn/app/i1mwqy35y88hl/table/snahtjpjwbz3f?ri=c67wwyqeth1up"
    },
    "id": "client.record.update.after"
}
```

### 3.17 After Record Delete (Client-side)

Triggered after a record is deleted via `Form submission` or `Workflow submission`.

> **TIP**: This listener is client-side triggered, so the automation can include interactive logic.

```json
{
    "eventId": "client.record.delete.after",
    "eventContent": {
        "app": { ... },
        "query": { ... },
        "tableId": "snahtjpjwbz3f",
        "source": "form",
        "user": { ... },
        "url": "https://next.informat.cn/app/i1mwqy35y88hl/table/snahtjpjwbz3f"
    },
    "id": "client.record.delete.after"
}
```

## 4. Event Summary Table

| Event ID | Description | Trigger Condition | Client-side | Transactional |
|----------|-------------|-------------------|:-----------:|:-------------:|
| `record.create.before` | Before record create | Before user creates record via form | No | Yes |
| `record.create.after` | After record create | After user creates record via form | No | Yes |
| `record.update.before` | Before record update | Before user updates record via form | No | Yes |
| `record.update.after` | After record update | After user updates record via form | No | Yes |
| `record.delete.before` | Before record delete | Before user deletes record via form | No | Yes |
| `record.delete.after` | After record delete | After user deletes record via form | No | Yes |
| `record.rownumber.update.before` | Before record sort | Before drag-to-reorder records | No | Yes |
| `record.rownumber.update.after` | After record sort | After drag-to-reorder records | No | Yes |
| `record.comment.create.after` | After comment create | After user posts a comment | No | Yes |
| `record.comment.delete.after` | After comment delete | After user deletes a comment | No | Yes |
| `app.automatic.before` | Before automation execute | Before automation starts | No | Yes |
| `app.automatic.success` | After automation success | After automation succeeds | No | Yes |
| `app.schedule.before` | Before schedule execute | Before schedule task starts | No | Yes |
| `app.schedule.success` | After schedule success | After schedule task succeeds | No | Yes |
| `app.enter` | Enter application | After user enters app from client | Yes | No |
| `app.module.enter` | Enter module | After user enters a module from client | Yes | No |
| `app.publish` | App publish | After application is published | No | Yes |
| `app.member.add.after` | Member join | After adding app member | No | Yes |
| `app.member.remove.after` | Member remove | After removing app member | No | Yes |
| `app.member.role.update.after` | Member role update | After modifying member role | No | Yes |
| `client.bpmn.task.change` | Task status change | Task delegate/transfer/jump/complete/claim/start | Yes | No |
| `client.bpmn.process.change` | Process status change | Process revoke/delete | Yes | No |
| `client.record.create.after` | Create after (client) | After user creates record via form/workflow | Yes | No |
| `client.record.update.after` | Update after (client) | After user updates record via form/workflow | Yes | No |
| `client.record.delete.after` | Delete after (client) | After user deletes record via form/workflow | Yes | No |

## 5. Creating a Listener (Call Convention)

The sections above describe the **event content the automation/script receives when a listener fires**; this section describes **how to compose the parameters when creating a listener (`_app_listener_create`)**. The two structures differ and must not be conflated.

### 5.1 Parameter Structure

- **`eventList`**: the events to listen for, typed as an **array of event-ID strings** whose values must come from the summary table in Section 4. For example, listening for record-update-after is `["record.update.after"]`.
- **Table filter** `tableEventSetting`: when listening for `record.*` events, `tableEventSetting.tableList` (an array of table IDs) specifies which tables to listen on (empty means all tables); `tableSourceList` further filters by source (`form` / `survey` / `bpmn`). **Table IDs do not go inside `eventList`.**
- **`invokeType`** and the execution body: with `automatic`, set `automaticList` (array of automation IDs); with `script`, set `scriptId` + `scriptFunc`.
- For other event categories, provide the corresponding setting object: `app.postevent` → `postEventSetting`, `app.automatic.*` → `automaticEventSetting`, `app.schedule.*` → `scheduleEventSetting`, workflow-related → `bpmnEventSetting`.

### 5.2 Correct Example: listen for updates on the project table and trigger an automation

```json
{
  "name": "Project status change listener",
  "eventList": ["record.update.after"],
  "isEnable": true,
  "invokeType": "automatic",
  "automaticList": ["<automationId>"],
  "tableEventSetting": {
    "tableList": ["project"],
    "tableSourceList": ["form"]
  }
}
```

### 5.3 Common Mistakes (must avoid)

- ❌ Writing an event as an object with the table ID embedded: `"eventList": [{"type": "record.update.after", "tableId": "project"}]`. Each `eventList` element is an **event-ID string**; there is no `type` / `tableId` field. That form is parsed as an invalid event, and the "listen event" in the UI shows a raw JSON string rather than a recognizable event type.
- ❌ Using `tableId` (singular, string) in place of `tableEventSetting.tableList` (array).
- ❌ Setting `invokeType=automatic` without `automaticList`, or `invokeType=script` while omitting `scriptFunc` — the listener is created successfully but has no execution body when triggered.
