---
name: feishu-lark
description: >
  Comprehensive Feishu/Lark integration skill for OpenClaw. Covers messaging,
  group management, Bitable (multi-dimensional tables), documents, calendar,
  video conferencing (vc.v1), meeting minutes (minutes.v1), task management,
  approval workflows, contacts, cloud drive, wiki/knowledge base.
  Requires the official Lark MCP server to be configured and running.
version: "3.1.0"
author: community
tags: [feishu, lark, messaging, bitable, calendar, vc, minutes, docs, tasks, approvals]
homepage: "https://github.com/lucascheung/lark-mcp"
source: "https://github.com/larksuite/lark-openapi-mcp"
requires:
  env:
    - name: LARK_APP_ID
      description: "Your Feishu/Lark App ID from the Open Platform developer console (open.feishu.cn/app or open.larksuite.com/app)"
      sensitive: false
    - name: LARK_APP_SECRET
      description: "Your Feishu/Lark App Secret from the Open Platform developer console"
      sensitive: true
  mcp_servers:
    - name: lark-mcp
      package: "@larksuiteoapi/lark-mcp"
      source: "https://github.com/larksuite/lark-openapi-mcp"
      description: "Official Feishu/Lark OpenAPI MCP server — install with: npx -y @larksuiteoapi/lark-mcp mcp -a $LARK_APP_ID -s $LARK_APP_SECRET"
---

# Feishu / Lark Comprehensive Skill

> **Prerequisite**: You must have the official Lark MCP server running before using this skill.
> Setup: `npx -y @larksuiteoapi/lark-mcp mcp -a <APP_ID> -s <APP_SECRET>`
> For user-identity APIs (useUAT): first run `npx -y @larksuiteoapi/lark-mcp login -a <APP_ID> -s <APP_SECRET>`
> To enable Video Conferencing + Minutes APIs, add: `-t preset.calendar.default,vc.v1.reserve.apply,vc.v1.meeting.get,vc.v1.meetingRecording.get,minutes.v1.minute.get,minutes.v1.minuteTranscript.get,minutes.v1.minuteStatistic.get`
> Full docs: https://open.larkoffice.com/document/home/index

---

## Core Concepts

### Tool Naming
All MCP tools use the prefix `mcp__lark-mcp__`. Example:
```
mcp__lark-mcp__im.v1.message.create
```

### Identity Types
| Parameter | Value | Meaning |
|-----------|-------|---------|
| `useUAT` | `true` | Act as the logged-in **user** — resources are owned by the user, directly accessible |
| `useUAT` | `false` (default) | Act as the **app/bot** — resources owned by the application |

Use `useUAT: true` for most interactive operations. Use `false` for background automation.

### Standard Parameter Structure
```yaml
path:      # URL path parameters (IDs, tokens)
params:    # Query string parameters (pagination, filters, id_type)
data:      # Request body payload
useUAT:    # true = user identity, false = app identity
```

### Common ID Types
| ID | Format | Represents |
|----|--------|-----------|
| `app_token` | `appXXX` | Bitable application |
| `table_id` | `tblXXX` | Bitable table |
| `record_id` | `recXXX` | Bitable record |
| `open_id` | `ou_XXX` | User (OpenID) |
| `union_id` | `on_XXX` | User (UnionID, cross-app) |
| `chat_id` | `oc_XXX` | Group/DM chat |
| `message_id` | `om_XXX` | Individual message |
| `document_id` | `doxcXXX` | Docs document |
| `file_token` | varies | Drive file |
| `node_token` | varies | Wiki node |
| `event_uid` | varies | Calendar event |
| `task_guid` | varies | Task |
| `approval_code` | varies | Approval definition |

---

## 1. Messaging (IM)

### Send a Message
**Tool**: `mcp__lark-mcp__im.v1.message.create`
```yaml
params:
  receive_id_type: "chat_id"   # or: open_id, union_id, email, user_id
data:
  receive_id: "oc_xxx"
  msg_type: "text"             # text | post | image | interactive | file | audio | media | sticker | share_chat | share_user
  content: '{"text":"Hello!"}'
useUAT: true
```

**Message types and content formats:**
- `text`: `{"text": "Hello @user"}`
- `post` (rich text): `{"zh_cn": {"title": "Title", "content": [[{"tag":"text","text":"body"}]]}}`
- `interactive` (card): JSON card definition — use Card Builder at https://open.larkoffice.com/cardkit
- `image`: `{"image_key": "img_xxx"}` (upload image first via Drive)
- `share_chat`: `{"chat_id": "oc_xxx"}`

### Reply to a Message
**Tool**: `mcp__lark-mcp__im.v1.message.reply`
```yaml
path:
  message_id: "om_xxx"
data:
  content: '{"text":"Got it!"}'
  msg_type: "text"
  reply_in_thread: false   # true = create/continue a thread
useUAT: true
```

### List Messages in a Chat
**Tool**: `mcp__lark-mcp__im.v1.message.list`
```yaml
params:
  container_id_type: "chat"
  container_id: "oc_xxx"
  page_size: 20
  sort_type: "ByCreateTimeDesc"
  start_time: "1700000000"   # optional Unix timestamp
  end_time: "1700100000"     # optional Unix timestamp
```

### Get a Single Message
**Tool**: `mcp__lark-mcp__im.v1.message.get`
```yaml
path:
  message_id: "om_xxx"
```

### Delete a Message
**Tool**: `mcp__lark-mcp__im.v1.message.delete`
```yaml
path:
  message_id: "om_xxx"
useUAT: true
```

### Update / Edit a Message (cards or text)
**Tool**: `mcp__lark-mcp__im.v1.message.update`
```yaml
path:
  message_id: "om_xxx"
data:
  msg_type: "interactive"
  content: '{"config":{},"elements":[...]}'
useUAT: true
```

### Add a Message Reaction (Emoji)
**Tool**: `mcp__lark-mcp__im.v1.messageReaction.create`
```yaml
path:
  message_id: "om_xxx"
data:
  reaction_type:
    emoji_type: "THUMBSUP"   # THUMBSUP, OK, HEART, etc.
useUAT: true
```

### List Message Reactions
**Tool**: `mcp__lark-mcp__im.v1.messageReaction.list`
```yaml
path:
  message_id: "om_xxx"
params:
  reaction_type: "THUMBSUP"   # optional filter
```

### Pin / Unpin a Message
**Tool**: `mcp__lark-mcp__im.v1.pin.create` / `mcp__lark-mcp__im.v1.pin.delete`
```yaml
data:
  message_id: "om_xxx"
  chat_id: "oc_xxx"
useUAT: true
```

### Read Receipts (who has read)
**Tool**: `mcp__lark-mcp__im.v1.message.readUsers`
```yaml
path:
  message_id: "om_xxx"
params:
  user_id_type: "open_id"
  page_size: 50
```

---

## 2. Group / Chat Management

### List All Chats the Bot Is In
**Tool**: `mcp__lark-mcp__im.v1.chat.list`
```yaml
params:
  user_id_type: "open_id"
  page_size: 20
```

### List Chats the User Is In
**Tool**: `mcp__lark-mcp__im.v1.chat.list`
```yaml
params:
  user_id_type: "open_id"
  page_size: 20
useUAT: true
```

### Get Chat Info
**Tool**: `mcp__lark-mcp__im.v1.chat.get`
```yaml
path:
  chat_id: "oc_xxx"
params:
  user_id_type: "open_id"
```

### Create a Group Chat
**Tool**: `mcp__lark-mcp__im.v1.chat.create`
```yaml
data:
  name: "Project Alpha"
  description: "Discuss Project Alpha here"
  owner_id: "ou_xxx"           # optional, defaults to app/user
  user_id_list: ["ou_xxx", "ou_yyy"]
  bot_id_list: []
  chat_mode: "group"
  chat_type: "private"         # private | public
  external: false
useUAT: true
```

### Update Group Info
**Tool**: `mcp__lark-mcp__im.v1.chat.update`
```yaml
path:
  chat_id: "oc_xxx"
data:
  name: "New Name"
  description: "Updated description"
  owner_id: "ou_xxx"           # transfer ownership
  add_member_permission: "all_members"
  at_all_permission: "all_members"
  edit_permission: "all_members"
useUAT: true
```

### Disband a Group
**Tool**: `mcp__lark-mcp__im.v1.chat.delete`
```yaml
path:
  chat_id: "oc_xxx"
useUAT: true
```

### List Chat Members
**Tool**: `mcp__lark-mcp__im.v1.chatMembers.get`
```yaml
path:
  chat_id: "oc_xxx"
params:
  member_id_type: "open_id"
  page_size: 50
```

### Add Members to Chat
**Tool**: `mcp__lark-mcp__im.v1.chatMembers.create`
```yaml
path:
  chat_id: "oc_xxx"
params:
  member_id_type: "open_id"
data:
  id_list: ["ou_xxx", "ou_yyy"]
useUAT: true
```

### Remove Members from Chat
**Tool**: `mcp__lark-mcp__im.v1.chatMembers.delete`
```yaml
path:
  chat_id: "oc_xxx"
params:
  member_id_type: "open_id"
data:
  id_list: ["ou_xxx"]
useUAT: true
```

### Search Public Chats
**Tool**: `mcp__lark-mcp__im.v1.chat.search`
```yaml
params:
  query: "design team"
  page_size: 20
useUAT: true
```

### List Chat Tabs
**Tool**: `mcp__lark-mcp__im.v1.chatTab.listTabs`
```yaml
path:
  chat_id: "oc_xxx"
```

### Get Chat Announcement
**Tool**: `mcp__lark-mcp__im.v1.chatAnnouncement.get`
```yaml
path:
  chat_id: "oc_xxx"
params:
  user_id_type: "open_id"
```

### Update Chat Announcement
**Tool**: `mcp__lark-mcp__im.v1.chatAnnouncement.patch`
```yaml
path:
  chat_id: "oc_xxx"
data:
  revision_id: 1
  requests: ['{"requestType":"InsertBlocksAtDocumentTail","insertBlocksAtDocumentTailRequest":{"payload":{"blocks":[{"blockType":2,"text":{"elements":[{"textRun":{"content":"New announcement"}}],"style":{}}}]}}}']
useUAT: true
```

---

## 3. Bitable (Multi-Dimensional Tables / Base)

### Create a Bitable App
**Tool**: `mcp__lark-mcp__bitable.v1.app.create`
```yaml
data:
  name: "Project Tracker"
  folder_token: ""   # optional: Drive folder to place it in
useUAT: true
```

### Get Bitable App Info
**Tool**: `mcp__lark-mcp__bitable.v1.app.get`
```yaml
path:
  app_token: "appXXX"
```

### Update Bitable App
**Tool**: `mcp__lark-mcp__bitable.v1.app.update`
```yaml
path:
  app_token: "appXXX"
data:
  name: "New Name"
  is_advanced: true   # enable advanced features
useUAT: true
```

### List Tables in a Bitable App
**Tool**: `mcp__lark-mcp__bitable.v1.appTable.list`
```yaml
path:
  app_token: "appXXX"
params:
  page_size: 20
```

### Create a Table
**Tool**: `mcp__lark-mcp__bitable.v1.appTable.create`
```yaml
path:
  app_token: "appXXX"
data:
  table:
    name: "Tasks"
    default_view_name: "Grid View"
    fields:
      - field_name: "Task Name"
        type: 1   # 1=text, 2=number, 3=single-select, 4=multi-select, 5=date, 7=checkbox, 11=person, 15=url, 99001=phone
      - field_name: "Status"
        type: 3
        property:
          options:
            - name: "To Do"
              color: 0
            - name: "In Progress"
              color: 1
            - name: "Done"
              color: 2
      - field_name: "Assignee"
        type: 11
      - field_name: "Due Date"
        type: 5
useUAT: true
```

### Delete a Table
**Tool**: `mcp__lark-mcp__bitable.v1.appTable.delete`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
useUAT: true
```

### List Fields in a Table
**Tool**: `mcp__lark-mcp__bitable.v1.appTableField.list`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
params:
  page_size: 50
  view_id: ""   # optional: filter by view
```

### Create a Field
**Tool**: `mcp__lark-mcp__bitable.v1.appTableField.create`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
data:
  field_name: "Priority"
  type: 3   # single-select
  property:
    options:
      - name: "High"
        color: 0
      - name: "Medium"
        color: 1
      - name: "Low"
        color: 2
useUAT: true
```

### Update a Field
**Tool**: `mcp__lark-mcp__bitable.v1.appTableField.update`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
  field_id: "fldXXX"
data:
  field_name: "Renamed Field"
  property:
    options:
      - name: "Critical"
        color: 0
useUAT: true
```

### Delete a Field
**Tool**: `mcp__lark-mcp__bitable.v1.appTableField.delete`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
  field_id: "fldXXX"
useUAT: true
```

### Search / List Records
**Tool**: `mcp__lark-mcp__bitable.v1.appTableRecord.search`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
params:
  user_id_type: "open_id"
  page_size: 100
  page_token: ""   # for pagination
data:
  view_id: ""   # optional
  field_names: ["Task Name", "Status", "Assignee"]   # optional: only return these fields
  sort:
    - field_name: "Due Date"
      desc: false
  filter:
    conjunction: "and"   # and | or
    conditions:
      - field_name: "Status"
        operator: "is"   # is | isNot | contains | doesNotContain | isEmpty | isNotEmpty | isGreater | isLess
        value: ["In Progress"]
  automatic_fields: false
useUAT: true
```

### Get a Single Record
**Tool**: `mcp__lark-mcp__bitable.v1.appTableRecord.get`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
  record_id: "recXXX"
params:
  user_id_type: "open_id"
```

### Create a Record
**Tool**: `mcp__lark-mcp__bitable.v1.appTableRecord.create`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
params:
  user_id_type: "open_id"
data:
  fields:
    "Task Name": "Fix login bug"
    "Status": "To Do"
    "Assignee": [{"id": "ou_xxx"}]
    "Due Date": 1700000000000   # milliseconds timestamp
useUAT: true
```

### Batch Create Records
**Tool**: `mcp__lark-mcp__bitable.v1.appTableRecord.batchCreate`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
params:
  user_id_type: "open_id"
data:
  records:
    - fields:
        "Task Name": "Task 1"
        "Status": "To Do"
    - fields:
        "Task Name": "Task 2"
        "Status": "In Progress"
useUAT: true
```

### Update a Record
**Tool**: `mcp__lark-mcp__bitable.v1.appTableRecord.update`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
  record_id: "recXXX"
params:
  user_id_type: "open_id"
data:
  fields:
    "Status": "Done"
useUAT: true
```

### Batch Update Records
**Tool**: `mcp__lark-mcp__bitable.v1.appTableRecord.batchUpdate`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
params:
  user_id_type: "open_id"
data:
  records:
    - record_id: "recXXX"
      fields:
        "Status": "Done"
    - record_id: "recYYY"
      fields:
        "Status": "In Progress"
useUAT: true
```

### Delete a Record
**Tool**: `mcp__lark-mcp__bitable.v1.appTableRecord.delete`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
  record_id: "recXXX"
useUAT: true
```

### Batch Delete Records
**Tool**: `mcp__lark-mcp__bitable.v1.appTableRecord.batchDelete`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
data:
  records: ["recXXX", "recYYY"]
useUAT: true
```

### List Views
**Tool**: `mcp__lark-mcp__bitable.v1.appTableView.list`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
params:
  page_size: 20
```

### Create a View
**Tool**: `mcp__lark-mcp__bitable.v1.appTableView.create`
```yaml
path:
  app_token: "appXXX"
  table_id: "tblXXX"
data:
  view_name: "Kanban"
  view_type: "kanban"   # grid | kanban | gallery | gantt | form
useUAT: true
```

### Manage Bitable Collaborators
**Tool**: `mcp__lark-mcp__bitable.v1.appRoleMember.create`
```yaml
path:
  app_token: "appXXX"
  role_id: "roleXXX"
data:
  member_id: "ou_xxx"
  member_id_type: "open_id"
useUAT: true
```

---

## 4. Documents (Docs)

### Search Documents
**Tool**: `mcp__lark-mcp__drive.v1.file.search` (or `docx.builtin.search`)
```yaml
params:
  query: "Q4 report"
  page_size: 20
useUAT: true
```

### Get Document Content (plain text)
**Tool**: `mcp__lark-mcp__docx.v1.document.rawContent`
```yaml
path:
  document_id: "doxcXXX"
params:
  lang: 0   # 0=default
useUAT: true
```

### Get Document Metadata
**Tool**: `mcp__lark-mcp__docx.v1.document.get`
```yaml
path:
  document_id: "doxcXXX"
useUAT: true
```

### Create a New Document
**Tool**: `mcp__lark-mcp__docx.v1.document.create`
```yaml
data:
  folder_token: ""   # optional: Drive folder
  title: "Meeting Notes - 2026-03-06"
useUAT: true
```

### List Document Blocks
**Tool**: `mcp__lark-mcp__docx.v1.documentBlock.list`
```yaml
path:
  document_id: "doxcXXX"
params:
  page_size: 50
  document_revision_id: -1   # -1 = latest
useUAT: true
```

### Update Document Blocks (insert content)
**Tool**: `mcp__lark-mcp__docx.v1.documentBlockChildren.batchUpdate`
```yaml
path:
  document_id: "doxcXXX"
  block_id: "doxcXXX"   # parent block (document root = document_id)
data:
  requests:
    - insertBlocksAfterBlockRequest:
        targetBlockId: "blockXXX"
        payload:
          blocks:
            - blockType: 2   # 2=text, 3=heading1, 4=heading2, 12=bullet, 22=code
              text:
                elements:
                  - textRun:
                      content: "New paragraph content"
  revision_id: -1   # -1 = latest
useUAT: true
```

---

## 5. Cloud Drive (Drive)

### List Files in Root or Folder
**Tool**: `mcp__lark-mcp__drive.v1.file.list`
```yaml
params:
  folder_token: ""   # empty = root ("My Drive")
  page_size: 20
  order_by: "EditedTime"   # EditedTime | CreatedTime | Name
  direction: "DESC"
useUAT: true
```

### Create a Folder
**Tool**: `mcp__lark-mcp__drive.v1.file.createFolder`
```yaml
data:
  name: "Q1 Reports"
  folder_token: ""   # parent folder, empty = root
useUAT: true
```

### Move a File
**Tool**: `mcp__lark-mcp__drive.v1.file.move`
```yaml
path:
  file_token: "xxx"
data:
  type: "doc"   # doc | sheet | bitable | mindnote | file | wiki | docx
  folder_token: "targetFolderToken"
useUAT: true
```

### Copy a File
**Tool**: `mcp__lark-mcp__drive.v1.file.copy`
```yaml
path:
  file_token: "xxx"
data:
  name: "Copy of Report"
  type: "docx"
  folder_token: "targetFolderToken"
useUAT: true
```

### Delete a File
**Tool**: `mcp__lark-mcp__drive.v1.file.delete`
```yaml
path:
  file_token: "xxx"
params:
  type: "docx"
useUAT: true
```

### Get File Statistics
**Tool**: `mcp__lark-mcp__drive.v1.fileStatistics.get`
```yaml
path:
  file_token: "xxx"
  file_type: "docx"   # docx | sheet | bitable | file
```

### Manage File Permissions (add collaborator)
**Tool**: `mcp__lark-mcp__drive.v1.permissionMember.create`
```yaml
path:
  token: "xxx"
  type: "docx"
data:
  member_type: "openid"   # openid | unionid | email | opendepartmentid | groupid
  member_id: "ou_xxx"
  perm: "view"   # view | edit | full_access
useUAT: true
```

### List File Collaborators
**Tool**: `mcp__lark-mcp__drive.v1.permissionMember.list`
```yaml
path:
  token: "xxx"
  type: "docx"
useUAT: true
```

### Get File Comments
**Tool**: `mcp__lark-mcp__drive.v1.fileComment.list`
```yaml
path:
  file_token: "xxx"
  file_type: "docx"
params:
  is_solved: false
  page_size: 20
useUAT: true
```

### Add a File Comment
**Tool**: `mcp__lark-mcp__drive.v1.fileComment.create`
```yaml
path:
  file_token: "xxx"
  file_type: "docx"
data:
  reply_list:
    replies:
      - content:
          elements:
            - type: "text_run"
              text_run:
                text: "Great work on this section!"
useUAT: true
```

---

## 6. Calendar

### List All Calendars
**Tool**: `mcp__lark-mcp__calendar.v4.calendar.list`
```yaml
params:
  page_size: 20
useUAT: true
```

### Get Primary Calendar
**Tool**: `mcp__lark-mcp__calendar.v4.calendar.primary`
```yaml
params:
  user_id_type: "open_id"
useUAT: true
```

### Create a Calendar
**Tool**: `mcp__lark-mcp__calendar.v4.calendar.create`
```yaml
data:
  summary: "Team Calendar"
  description: "Shared team schedule"
  permissions: "public"   # private | show_only_free_busy | public
  color: -1
  summary_alias: ""
useUAT: true
```

### List Events
**Tool**: `mcp__lark-mcp__calendar.v4.calendarEvent.list`
```yaml
path:
  calendar_id: "primary"   # or specific calendar ID
params:
  start_time: "1700000000"
  end_time: "1702600000"
  page_size: 50
useUAT: true
```

### Get a Calendar Event
**Tool**: `mcp__lark-mcp__calendar.v4.calendarEvent.get`
```yaml
path:
  calendar_id: "primary"
  event_id: "xxx"
params:
  user_id_type: "open_id"
useUAT: true
```

### Create a Calendar Event
**Tool**: `mcp__lark-mcp__calendar.v4.calendarEvent.create`
```yaml
path:
  calendar_id: "primary"
data:
  summary: "Team Standup"
  description: "Daily sync"
  start_time:
    timestamp: "1700000000"
    timezone: "Asia/Shanghai"
  end_time:
    timestamp: "1700003600"
    timezone: "Asia/Shanghai"
  attendees:
    - type: "user"
      user_id: "ou_xxx"
  need_notification: true
  visibility: "default"   # default | public | private
  free_busy_status: "busy"   # busy | free
  color: -1
  reminders:
    - minutes: 10
  recurrence_rule: ""   # e.g. "FREQ=DAILY;COUNT=5" for recurring events
useUAT: true
```

### Update a Calendar Event
**Tool**: `mcp__lark-mcp__calendar.v4.calendarEvent.patch`
```yaml
path:
  calendar_id: "primary"
  event_id: "xxx"
data:
  summary: "Updated Meeting Title"
  description: "Updated description"
useUAT: true
```

### Delete a Calendar Event
**Tool**: `mcp__lark-mcp__calendar.v4.calendarEvent.delete`
```yaml
path:
  calendar_id: "primary"
  event_id: "xxx"
params:
  need_notification: true
useUAT: true
```

### List Event Attendees
**Tool**: `mcp__lark-mcp__calendar.v4.calendarEventAttendee.list`
```yaml
path:
  calendar_id: "primary"
  event_id: "xxx"
params:
  user_id_type: "open_id"
  page_size: 50
useUAT: true
```

### Add Attendees to an Event
**Tool**: `mcp__lark-mcp__calendar.v4.calendarEventAttendee.create`
```yaml
path:
  calendar_id: "primary"
  event_id: "xxx"
data:
  attendees:
    - type: "user"
      user_id: "ou_xxx"
  need_notification: true
useUAT: true
```

### Get User Free/Busy
**Tool**: `mcp__lark-mcp__calendar.v4.freebusy.list`
```yaml
data:
  time_min: "2026-03-06T09:00:00+08:00"
  time_max: "2026-03-06T18:00:00+08:00"
  user_id_list: ["ou_xxx", "ou_yyy"]
useUAT: true
```

---

## 7. Tasks

### List Tasks
**Tool**: `mcp__lark-mcp__task.v2.task.list`
```yaml
params:
  completed: false
  type: "my"   # my | created | assigned
  page_size: 50
useUAT: true
```

### Get a Task
**Tool**: `mcp__lark-mcp__task.v2.task.get`
```yaml
path:
  task_guid: "xxx"
params:
  user_id_type: "open_id"
useUAT: true
```

### Create a Task
**Tool**: `mcp__lark-mcp__task.v2.task.create`
```yaml
params:
  user_id_type: "open_id"
data:
  summary: "Write Q4 report"
  description: "Compile all metrics and write the Q4 summary report"
  due:
    timestamp: "1700000000000"   # milliseconds
    is_all_day: false
  origin:
    platform_i18n_name: '{"zh_cn":"来自OpenClaw","en_us":"From OpenClaw"}'
  members:
    - id: "ou_xxx"
      type: "user"
      role: "assignee"   # assignee | follower
  task_list_configs:
    - tasklist_guid: "tsklistXXX"   # optional: add to a task list
  repeat_rule: ""   # e.g. "FREQ=WEEKLY;BYDAY=MO" for recurring
useUAT: true
```

### Update a Task
**Tool**: `mcp__lark-mcp__task.v2.task.patch`
```yaml
path:
  task_guid: "xxx"
params:
  user_id_type: "open_id"
data:
  task:
    summary: "Updated task name"
    due:
      timestamp: "1700100000000"
  update_fields: ["summary", "due"]   # specify which fields to update
useUAT: true
```

### Complete a Task
**Tool**: `mcp__lark-mcp__task.v2.task.complete`
```yaml
path:
  task_guid: "xxx"
useUAT: true
```

### Uncomplete a Task
**Tool**: `mcp__lark-mcp__task.v2.task.uncomplete`
```yaml
path:
  task_guid: "xxx"
useUAT: true
```

### Delete a Task
**Tool**: `mcp__lark-mcp__task.v2.task.delete`
```yaml
path:
  task_guid: "xxx"
useUAT: true
```

### Add a Task Comment
**Tool**: `mcp__lark-mcp__task.v2.taskComment.create`
```yaml
path:
  task_guid: "xxx"
data:
  content: "Progress update: 80% complete"
  reply_to_comment_id: ""   # optional
useUAT: true
```

### List Task Comments
**Tool**: `mcp__lark-mcp__task.v2.taskComment.list`
```yaml
path:
  task_guid: "xxx"
params:
  page_size: 20
useUAT: true
```

### List Task Lists
**Tool**: `mcp__lark-mcp__task.v2.tasklist.list`
```yaml
params:
  user_id_type: "open_id"
  page_size: 20
useUAT: true
```

### Create a Task List
**Tool**: `mcp__lark-mcp__task.v2.tasklist.create`
```yaml
data:
  name: "Sprint 12"
  members:
    - id: "ou_xxx"
      type: "user"
      role: "editor"
useUAT: true
```

### Add Task to a Task List
**Tool**: `mcp__lark-mcp__task.v2.task.addTasklist`
```yaml
path:
  task_guid: "xxx"
data:
  tasklist_guid: "tsklistXXX"
  section_guid: ""   # optional: specific section
useUAT: true
```

---

## 8. Contacts (Users & Departments)

### Get User by Open ID
**Tool**: `mcp__lark-mcp__contact.v3.user.get`
```yaml
path:
  user_id: "ou_xxx"
params:
  user_id_type: "open_id"
useUAT: true
```

### Batch Get Users by Email or Phone
**Tool**: `mcp__lark-mcp__contact.v3.user.batchGetId`
```yaml
params:
  user_id_type: "open_id"
data:
  emails: ["user@company.com"]
  mobiles: ["+8613800000000"]
useUAT: true
```

### Search Users
**Tool**: `mcp__lark-mcp__contact.v3.user.findByDepartment`
```yaml
params:
  user_id_type: "open_id"
  department_id_type: "open_department_id"
  department_id: "od_xxx"
  page_size: 50
useUAT: true
```

### Get Current User Info
**Tool**: `mcp__lark-mcp__authen.v1.userInfo.get`
```yaml
useUAT: true
```

### List Departments
**Tool**: `mcp__lark-mcp__contact.v3.department.children`
```yaml
params:
  department_id_type: "open_department_id"
  parent_department_id: "0"   # "0" = root
  page_size: 50
  fetch_child: false
useUAT: true
```

### Get Department Info
**Tool**: `mcp__lark-mcp__contact.v3.department.get`
```yaml
path:
  department_id: "od_xxx"
params:
  department_id_type: "open_department_id"
  user_id_type: "open_id"
useUAT: true
```

---

## 9. Wiki / Knowledge Base

### List Wiki Spaces
**Tool**: `mcp__lark-mcp__wiki.v2.space.list`
```yaml
params:
  page_size: 20
useUAT: true
```

### Get Wiki Space Info
**Tool**: `mcp__lark-mcp__wiki.v2.space.get`
```yaml
path:
  space_id: "xxx"
useUAT: true
```

### List Wiki Nodes
**Tool**: `mcp__lark-mcp__wiki.v2.spaceNode.list`
```yaml
path:
  space_id: "xxx"
params:
  parent_node_token: ""   # empty = root level
  page_size: 50
useUAT: true
```

### Search Wiki
**Tool**: `mcp__lark-mcp__wiki.v2.spaceNode.search`
```yaml
path:
  space_id: "xxx"
params:
  keyword: "onboarding guide"
  page_size: 20
useUAT: true
```

### Get Wiki Node Info
**Tool**: `mcp__lark-mcp__wiki.v2.spaceNode.get`
```yaml
params:
  token: "wikcXXX"
useUAT: true
```

### Create a Wiki Node (new page)
**Tool**: `mcp__lark-mcp__wiki.v2.spaceNode.create`
```yaml
path:
  space_id: "xxx"
data:
  node_type: "origin"   # origin = new doc; copy = copy existing
  parent_node_token: "wikcXXX"   # parent page token
  title: "New Page Title"
useUAT: true
```

### Move a Wiki Node
**Tool**: `mcp__lark-mcp__wiki.v2.spaceNode.move`
```yaml
path:
  space_id: "xxx"
  node_token: "wikcXXX"
data:
  target_parent_token: "wikcYYY"
  target_space_id: ""   # empty = same space
useUAT: true
```

---

## 10. Approval Workflows

### Get Approval Definition
**Tool**: `mcp__lark-mcp__approval.v4.approval.get`
```yaml
path:
  approval_code: "xxx"
params:
  locale: "zh-CN"   # zh-CN | en-US | ja-JP
```

### Create an Approval Instance (submit for approval)
**Tool**: `mcp__lark-mcp__approval.v4.instance.create`
```yaml
data:
  approval_code: "xxx"
  open_id: "ou_xxx"   # submitter
  form: '[{"id":"widget1","type":"input","value":"Expense claim for $500"}]'
  node_approver_open_id_list: []   # optional: specify approvers per node
useUAT: true
```

### Get an Approval Instance
**Tool**: `mcp__lark-mcp__approval.v4.instance.get`
```yaml
path:
  instance_id: "xxx"
params:
  locale: "zh-CN"
  user_id: "ou_xxx"
  user_id_type: "open_id"
useUAT: true
```

### List Approval Instances
**Tool**: `mcp__lark-mcp__approval.v4.instance.list`
```yaml
params:
  approval_code: "xxx"
  start_time: "1700000000000"
  end_time: "1702600000000"
  page_size: 100
```

### Approve an Instance
**Tool**: `mcp__lark-mcp__approval.v4.instance.approve`
```yaml
data:
  approval_code: "xxx"
  instance_code: "xxx"
  user_id: "ou_xxx"
  task_id: "xxx"
  comment: "Looks good, approved!"
useUAT: true
```

### Reject an Instance
**Tool**: `mcp__lark-mcp__approval.v4.instance.reject`
```yaml
data:
  approval_code: "xxx"
  instance_code: "xxx"
  user_id: "ou_xxx"
  task_id: "xxx"
  comment: "Please revise the budget figures"
useUAT: true
```

### Cancel an Approval Instance
**Tool**: `mcp__lark-mcp__approval.v4.instance.cancel`
```yaml
data:
  approval_code: "xxx"
  instance_code: "xxx"
  user_id: "ou_xxx"
useUAT: true
```

### Add a Comment to an Approval Instance
**Tool**: `mcp__lark-mcp__approval.v4.instanceComment.create`
```yaml
path:
  instance_id: "xxx"
data:
  content: "Please check the attached receipts"
  at_info_list:
    - user_id: "ou_xxx"
      name: "John"
      offset: "14"
useUAT: true
```

---

## 11. Common Workflows

### Workflow: Find User and Send DM
```
1. mcp__lark-mcp__contact.v3.user.batchGetId
   → emails: ["user@company.com"] → get open_id

2. mcp__lark-mcp__im.v1.message.create
   → receive_id_type: "open_id"
   → receive_id: <open_id from step 1>
   → send the message
```

### Workflow: Create Bitable Table and Populate from Data
```
1. mcp__lark-mcp__bitable.v1.app.create → get app_token
2. mcp__lark-mcp__bitable.v1.appTable.create → define schema → get table_id
3. mcp__lark-mcp__bitable.v1.appTableRecord.batchCreate → insert records (up to 500 per call)
```

### Workflow: Weekly Report to Group
```
1. mcp__lark-mcp__bitable.v1.appTableRecord.search
   → filter: Status = "Done", Due Date in last 7 days
   → collect completed items

2. Format into rich-text post or interactive card

3. mcp__lark-mcp__im.v1.message.create
   → msg_type: "post" or "interactive"
   → send to project group chat_id
```

### Workflow: Schedule a Meeting with Free/Busy Check
```
1. mcp__lark-mcp__calendar.v4.freebusy.list
   → check availability of all attendees in target window

2. Pick a free slot

3. mcp__lark-mcp__calendar.v4.calendarEvent.create
   → add all attendees, set reminders

4. mcp__lark-mcp__im.v1.message.create
   → notify attendees with meeting details
```

### Workflow: Submit and Track Approval
```
1. mcp__lark-mcp__approval.v4.approval.get → inspect form fields

2. mcp__lark-mcp__approval.v4.instance.create
   → fill form data, submit

3. mcp__lark-mcp__approval.v4.instance.get
   → poll for status: PENDING | APPROVED | REJECTED | CANCELED
```

### Workflow: Create Task and Assign
```
1. mcp__lark-mcp__contact.v3.user.batchGetId → resolve assignee email → open_id

2. mcp__lark-mcp__task.v2.task.create
   → summary, description, due date, members with role "assignee"

3. Optionally: mcp__lark-mcp__im.v1.message.create
   → notify assignee via DM
```

---

## 12. Error Reference

| Error Code | Meaning | Fix |
|------------|---------|-----|
| `99991663` | Token expired | Re-login or refresh token |
| `99991664` | Invalid token | Check app credentials |
| `99991400` | Permission denied | Grant required scopes in developer console |
| `230001` | Bot not in chat | Add bot to the group first |
| `1254502` | Record not found | Verify record_id is correct |
| `1254520` | Field not found | Check field_name spelling exactly |
| `1300006` | Event not found | Verify event_id and calendar_id |
| `1100003` | Meeting not found | Meeting may have ended or reserve_id is wrong |
| `1100007` | Meeting not active | Use `reserve.get` to check status first |
| `1100032` | Not meeting host | Only host can perform this action |
| `1700001` | Minutes not found | Check minute_token format (`obcn...`) |
| `1700002` | Minutes not ready | Transcription still processing, retry later |

### Common Issues
- **"Tool not found"**: MCP server not running. Start with `npx -y @larksuiteoapi/lark-mcp mcp -a <APP_ID> -s <APP_SECRET>`
- **Resources inaccessible**: Use `useUAT: true` — resources created by bot identity may not be visible to users
- **Permission error**: In Feishu Open Platform console, enable the required permissions scopes (e.g. `bitable:app`, `im:message`, `calendar:calendar`, `task:task:write`)
- **message_id not found**: Messages expire or may require `im:message:send_as_bot` scope
- **user_access_token expired**: Run `npx -y @larksuiteoapi/lark-mcp login` to refresh (valid 2h, refreshable with offline_access scope)

---

## 13. Video Conferencing (vc.v1)

> **Note**: Video Conferencing APIs require the `vc:meeting` scope family and generally need `useUAT: true` (user identity). Enable via `-t vc.v1.*` in lark-mcp or add individually.

### Schedule / Reserve a Meeting
**Tool**: `mcp__lark-mcp__vc.v1.reserve.apply`
```yaml
data:
  end_time: "1700003600"          # Unix timestamp seconds
  meeting_settings:
    topic: "Q4 Planning Meeting"
    action_permissions:
      - permission: 1             # 1=invite members 2=share screen 3=record
        permission_checker_type: 1  # 1=host only 2=everyone
    meeting_initial_type: 1       # 1=video 2=audio
    auto_record: false
    enable_waiting_room: false
    allow_screen_sharing: true
    only_employee_join: false
    join_meeting_permission: 1    # 1=any Feishu user 2=only invited 3=only org members
    push_question_to_vc: false
    meeting_reminder: true
useUAT: true
```
Returns: `reserve_id`, `reserve_token` — save these to manage the reservation.

### Update a Meeting Reservation
**Tool**: `mcp__lark-mcp__vc.v1.reserve.update`
```yaml
path:
  reserve_id: "xxx"
data:
  end_time: "1700007200"
  meeting_settings:
    topic: "Updated Meeting Title"
useUAT: true
```

### Delete / Cancel a Reservation
**Tool**: `mcp__lark-mcp__vc.v1.reserve.delete`
```yaml
path:
  reserve_id: "xxx"
useUAT: true
```

### Get Reservation Details
**Tool**: `mcp__lark-mcp__vc.v1.reserve.get`
```yaml
path:
  reserve_id: "xxx"
params:
  with_meeting_info: true     # also return active meeting info
useUAT: true
```

### Get Active Meeting from a Reservation
**Tool**: `mcp__lark-mcp__vc.v1.reserve.getActiveMeeting`
```yaml
path:
  reserve_id: "xxx"
params:
  with_participants: true
useUAT: true
```

### Get Meeting Details (by meeting_id)
**Tool**: `mcp__lark-mcp__vc.v1.meeting.get`
```yaml
path:
  meeting_id: "xxx"
params:
  with_participants: true
  with_meeting_ability: true
useUAT: true
```

### List Meetings by No (meeting number)
**Tool**: `mcp__lark-mcp__vc.v1.meeting.listByNo`
```yaml
params:
  meeting_no: "123456789"   # 9-digit meeting number shown in UI
  start_time: "1700000000"
  end_time: "1700100000"
  page_size: 20
useUAT: true
```

### Invite Participants to a Meeting
**Tool**: `mcp__lark-mcp__vc.v1.meeting.invite`
```yaml
path:
  meeting_id: "xxx"
data:
  invitees:
    - id: "ou_xxx"
      type: 1             # 1=Feishu user, 2=room, 3=phone, 5=SIP/H323
useUAT: true
```

### Kick a Participant from a Meeting
**Tool**: `mcp__lark-mcp__vc.v1.meeting.kickout`
```yaml
path:
  meeting_id: "xxx"
data:
  kickout_users:
    - id: "ou_xxx"
      type: 1
useUAT: true
```

### Set Host of a Meeting
**Tool**: `mcp__lark-mcp__vc.v1.meeting.setHost`
```yaml
path:
  meeting_id: "xxx"
data:
  host_user:
    id: "ou_xxx"
    type: 1
  old_host_user:
    id: "ou_yyy"
    type: 1
useUAT: true
```

### End a Meeting
**Tool**: `mcp__lark-mcp__vc.v1.meeting.end`
```yaml
path:
  meeting_id: "xxx"
useUAT: true
```

### List Meeting Participants
**Tool**: `mcp__lark-mcp__vc.v1.participant.list`
```yaml
params:
  meeting_id: "xxx"
  meeting_start_time: "1700000000"
  meeting_end_time: "1700003600"
  page_size: 100
useUAT: true
```

### Get Meeting Recording
**Tool**: `mcp__lark-mcp__vc.v1.meetingRecording.get`
```yaml
path:
  meeting_id: "xxx"
useUAT: true
```
Returns: recording file URL, duration, size.

### Set Recording Permissions
**Tool**: `mcp__lark-mcp__vc.v1.meetingRecording.setPermission`
```yaml
path:
  meeting_id: "xxx"
data:
  permission_objects:
    - id: "ou_xxx"
      type: 1             # 1=user, 2=department
      permission: 1       # 1=view
  action_type: 1          # 1=set 2=add 3=remove
useUAT: true
```

### Export Meeting Attendance Report
**Tool**: `mcp__lark-mcp__vc.v1.export.meetingList`
```yaml
data:
  start_time: "1700000000"
  end_time: "1700100000"
  meeting_status: 3       # 1=not started, 2=in progress, 3=ended
  page_size: 100
useUAT: true
```

### Export Participant Quality Report
**Tool**: `mcp__lark-mcp__vc.v1.export.participantList`
```yaml
data:
  meeting_start_time: "1700000000"
  meeting_end_time: "1700003600"
  meeting_no: "123456789"
  page_size: 100
useUAT: true
```

### Get Room (Conference Room) Info
**Tool**: `mcp__lark-mcp__vc.v1.room.get`
```yaml
path:
  room_id: "xxx"
params:
  user_id_type: "open_id"
```

### List Rooms
**Tool**: `mcp__lark-mcp__vc.v1.room.list`
```yaml
params:
  page_size: 20
  room_level_id: ""       # optional: filter by building/floor
```

---

## 14. Meeting Minutes (minutes.v1)

> Feishu Minutes (妙记) is the AI-powered meeting transcription and notes product.
> **Note**: Minutes APIs require `minutes:minute:readonly` scope. Currently read-only via API (no write endpoints).
> Minutes are auto-generated from video conference recordings or uploaded audio/video files.

### Get Minutes Metadata
**Tool**: `mcp__lark-mcp__minutes.v1.minute.get`
```yaml
path:
  minute_token: "obcnXXXXXX"   # token from the Minutes URL: feishu.cn/minutes/obcnXXX
params:
  user_id_type: "open_id"
useUAT: true
```
Returns: title, duration, owner, creation time, video status, transcription status.

### Get Minutes Transcript (full text)
**Tool**: `mcp__lark-mcp__minutes.v1.minuteTranscript.get`
```yaml
path:
  minute_token: "obcnXXXXXX"
params:
  user_id_type: "open_id"
useUAT: true
```
Returns: array of transcript segments, each with:
- `start_time` / `end_time` (milliseconds)
- `paragraph` — spoken text content
- `speaker_id`, `speaker_name` — who said it

### List Statistics / Participants in Minutes
**Tool**: `mcp__lark-mcp__minutes.v1.minuteStatistic.get`
```yaml
path:
  minute_token: "obcnXXXXXX"
params:
  user_id_type: "open_id"
useUAT: true
```
Returns: list of participants with speaking time and word counts.

### Get Minutes Audio/Video File (metadata only)
**Tool**: `mcp__lark-mcp__minutes.v1.minuteMedia.get`
```yaml
path:
  minute_token: "obcnXXXXXX"
params:
  type: 1     # 1=video file 2=audio file
useUAT: true
```
Returns: download URL for the original recording.
> ⚠️ File download/upload is not supported by lark-mcp directly. Use the URL to stream/access externally.

### How to Get a minute_token
Minutes tokens can be found:
1. From the meeting recording — the Minutes URL shown after a meeting ends
2. From the calendar event after the meeting (included in event details)
3. Format: `obcn` followed by alphanumeric characters (e.g. `obcn6qGKMiZy0eNFSKl6e8XXXXX`)

### Workflow: Post Meeting Summary to Group
```
1. mcp__lark-mcp__minutes.v1.minuteTranscript.get
   → get all transcript segments

2. Summarize transcript with LLM (handled by OpenClaw automatically)

3. mcp__lark-mcp__minutes.v1.minuteStatistic.get
   → get participant list and speaking stats

4. mcp__lark-mcp__im.v1.message.create
   → send summary + participant stats as rich card to the meeting group chat
```

---

## 15. Enhanced Group Chat Workflows

This section covers advanced group chat scenarios beyond basic CRUD.

### Find a Group by Name
```
1. mcp__lark-mcp__im.v1.chat.list → fetch all chats (paginate as needed)
2. Filter by name field client-side
   OR
   mcp__lark-mcp__im.v1.chat.search → params: query: "group name"
```

### Send an @mention Message
```yaml
# Tool: mcp__lark-mcp__im.v1.message.create
data:
  receive_id: "oc_xxx"
  msg_type: "text"
  content: '{"text":"<at user_id=\"ou_xxx\">John</at> please review this"}'
  # For @all:
  # content: '{"text":"<at user_id=\"all\">All</at> meeting in 5 minutes"}'
useUAT: true
```

### Send an Interactive Card to a Group
```yaml
# Tool: mcp__lark-mcp__im.v1.message.create
data:
  receive_id: "oc_xxx"
  msg_type: "interactive"
  content: |
    {
      "config": {"wide_screen_mode": true},
      "header": {
        "title": {"tag": "plain_text", "content": "Action Required"},
        "template": "red"
      },
      "elements": [
        {
          "tag": "div",
          "text": {"tag": "lark_md", "content": "**Task**: Please approve the Q4 budget\n**Deadline**: Tomorrow 5pm"}
        },
        {
          "tag": "action",
          "actions": [
            {"tag": "button", "text": {"tag": "plain_text", "content": "Approve"}, "type": "primary", "value": {"action": "approve"}},
            {"tag": "button", "text": {"tag": "plain_text", "content": "Reject"}, "type": "danger", "value": {"action": "reject"}}
          ]
        }
      ]
    }
useUAT: true
```

### Create a Dedicated Project Group with Bot and Members
```
1. mcp__lark-mcp__contact.v3.user.batchGetId
   → resolve member emails → open_ids

2. mcp__lark-mcp__im.v1.chat.create
   → name: "Project X - Team"
   → user_id_list: [all open_ids]
   → chat_type: "private"

3. mcp__lark-mcp__im.v1.message.create
   → send a welcome card message introducing the project
```

### Set a Group-Wide Announcement
```
1. mcp__lark-mcp__im.v1.chatAnnouncement.patch
   → insert new announcement text block at document tail
   → all members see the pinned announcement at top of chat
```

### Monitor Group Messages (Event-driven)
> Register the `im.message.receive_v1` event in Feishu Open Platform to receive
> all messages sent in groups where the bot is present. OpenClaw's Feishu channel
> handles this automatically when configured — no polling needed.

Event payload includes: `message_id`, `chat_id`, `sender.open_id`, `message.content`, `message.msg_type`

### Batch Notify Multiple Groups
```
1. Prepare list of chat_ids (from mcp__lark-mcp__im.v1.chat.list)
2. Loop: for each chat_id call mcp__lark-mcp__im.v1.message.create
   → throttle to avoid rate limits: ~5 req/sec recommended
```

### Thread / Reply to Specific Message in Group
```yaml
# Tool: mcp__lark-mcp__im.v1.message.reply
path:
  message_id: "om_xxx"      # the specific message to reply to
data:
  content: '{"text":"Thanks for the update!"}'
  msg_type: "text"
  reply_in_thread: true     # creates or continues a message thread
useUAT: true
```

### Forward a Message to Another Chat
```yaml
# Tool: mcp__lark-mcp__im.v1.message.forward
path:
  message_id: "om_xxx"
params:
  receive_id_type: "chat_id"
data:
  receive_id: "oc_yyy"
useUAT: true
```

### Merge Forward Multiple Messages
```yaml
# Tool: mcp__lark-mcp__im.v1.message.mergeForward
params:
  receive_id_type: "chat_id"
data:
  receive_id: "oc_yyy"
  message_id_list: ["om_xxx", "om_yyy", "om_zzz"]
useUAT: true
```

### Get Unread Messages for a User
```yaml
# Tool: mcp__lark-mcp__im.v1.message.list
params:
  container_id_type: "chat"
  container_id: "oc_xxx"
  sort_type: "ByCreateTimeDesc"
  page_size: 50
useUAT: true
# Then filter client-side for messages after last-read timestamp
```

### Transfer Group Ownership
```yaml
# Tool: mcp__lark-mcp__im.v1.chat.update
path:
  chat_id: "oc_xxx"
data:
  owner_id: "ou_new_owner"
useUAT: true
```

### Workflow: Post Meeting Notes to Group After VC
```
1. [Meeting ends] → get minute_token from calendar event or meeting recording

2. mcp__lark-mcp__minutes.v1.minuteTranscript.get
   → retrieve full transcript

3. Summarize with AI → key decisions, action items, owners

4. mcp__lark-mcp__im.v1.message.create
   → msg_type: "interactive"
   → send structured card to the meeting group with:
      - Meeting summary
      - Action items (bullet list)
      - Recording link
      - Participants

5. mcp__lark-mcp__task.v2.task.create (repeat for each action item)
   → assign to relevant team members
   → link due dates from discussion
```

---

## 16. Required App Permissions Reference

| Feature | Required Scopes |
|---------|----------------|
| Send messages | `im:message` |
| Read messages | `im:message:readonly` |
| Group management | `im:chat`, `im:chat:write` |
| Forward messages | `im:message` |
| Bitable (read) | `bitable:app:readonly` |
| Bitable (write) | `bitable:app` |
| Documents (read) | `docs:doc:readonly` |
| Documents (write) | `docs:doc` |
| Cloud Drive | `drive:drive` |
| Calendar (read) | `calendar:calendar:readonly` |
| Calendar (write) | `calendar:calendar` |
| Tasks | `task:task:write` |
| Contacts | `contact:user.base:readonly` |
| Wiki | `wiki:wiki:readonly` |
| Approvals | `approval:approval:readonly`, `approval:instance` |
| **Video Conf (reserve/manage)** | `vc:meeting` |
| **Video Conf (participants)** | `vc:meeting:readonly` |
| **Video Conf (recording)** | `vc:record` |
| **Video Conf (rooms)** | `vc:room:readonly` |
| **Video Conf (export reports)** | `vc:export` |
| **Minutes (read transcript)** | `minutes:minute:readonly` |
