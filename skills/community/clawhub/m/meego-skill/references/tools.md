# Meego MCP 工具完整清单

## 调用基础
```
npx @lark-project/meego-mcporter call meego <工具名> --args '{...}' --config /workspace/meego-config.json
```

---

## 一、查询类工具（Read）

### list_todo
**查询当前用户的待办/在途工作项**（最高频）
```bash
npx @lark-project/meego-mcporter call meego list_todo --args '{}' --config /workspace/meego-config.json
```
- 无参数，自动查当前用户
- 含：工作项ID、名称、类型key、当前节点名、计划开始/结束时间
- 分页：每页50条，`page_num` 从1开始递增

---

### get_workitem_brief
**查单个工作项概况**
```bash
npx @lark-project/meego-mcporter call meego get_workitem_brief --args '{"project_key":"你的project_key","work_item_id":6458194568}' --config /workspace/meego-config.json
```
- 也支持 `url` 参数，自动解析 project_key 和 work_item_id

---

### get_node_detail
**查工作项的节点（子任务）及节点字段信息**
```bash
npx @lark-project/meego-mcporter call meego get_node_detail --args '{"project_key":"你的project_key","work_item_id":6458194568,"need_sub_task":true}' --config /workspace/meego-config.json
```
- `need_sub_task`：是否返回子任务
- `node_id_list`：只查特定节点
- `field_key_list`：只查特定字段

---

### get_workitem_brief / get_workitem_field_meta
**查创建某工作项类型的字段配置（创建工作项前必查）**
```bash
npx @lark-project/meego-mcporter call meego get_workitem_field_meta --args '{"project_key":"你的project_key","work_item_type":"issue"}' --config /workspace/meego-config.json
```

---

### list_workitem_field_config
**查某工作项类型的完整字段列表（含选项值）**
```bash
npx @lark-project/meego-mcporter call meego list_workitem_field_config --args '{"project_key":"你的project_key","work_item_type":"issue","page_num":1}' --config /workspace/meego-config.json
```
返回字段key、字段名、字段类型、选项值（option）等。

---

### list_node_field_config
**查工作项类型的节点字段配置（含模糊搜索）**
```bash
npx @lark-project/meego-mcporter call meego list_node_field_config --args '{"project_key":"你的project_key","work_item_type":"issue","query":"负责人"}' --config /workspace/meego-config.json
```
- `query`：模糊搜索字段名或字段key
- `field_keys`：按字段key精确筛选
- `field_types`：按字段类型筛选（text、number、select等）

---

### list_workitem_types
**查项目下所有工作项类型**
```bash
npx @lark-project/meego-mcporter call meego list_workitem_types --args '{"project_key":"你的project_key"}' --config /workspace/meego-config.json
```
返回 type_key、名称、是否禁用等。

---

### get_workitem_op_record
**查工作项操作记录（流转历史）**
```bash
npx @lark-project/meego-mcporter call meego get_workitem_op_record --args '{"project_key":"你的project_key","work_item_id":6458194568}' --config /workspace/meego-config.json
```
- `start` / `end`：时间范围过滤（毫秒级时间戳，最长7天）
- `operation_type`：筛选操作类型（create/modify/delete等）
- `operator`：按操作者筛选

---

### get_workitem_man_hour_records
**查工作项的工时登记记录**
```bash
npx @lark-project/meego-mcporter call meego get_workitem_man_hour_records --args '{"project_key":"你的project_key","work_item_id":6458194568,"work_item_type":"issue"}' --config /workspace/meego-config.json
```

---

### get_transitable_states
**查工作项可流转的所有状态**
```bash
npx @lark-project/meego-mcporter call meego get_transitable_states --args '{"project_key":"你的project_key","work_item_id":6458194568,"work_item_type":"issue","user_key":"你的user_key"}' --config /workspace/meego-config.json
```
- 前提：知道 work_item_type（issue/story/sub_task等）

---

### get_transition_required
**查流转到某状态需要填哪些必填字段**
```bash
npx @lark-project/meego-mcporter call meego get_transition_required --args '{"project_key":"你的project_key","work_item_id":6458194568,"state_key":"RESOLVED"}' --config /workspace/meego-config.json
```

---

### list_team_members
**查团队成员列表**
```bash
npx @lark-project/meego-mcporter call meego list_team_members --args '{"project_key":"你的project_key","team_id":"team_xxx"}' --config /workspace/meego-config.json
```

---

### list_project_team
**查项目下所有团队**
```bash
npx @lark-project/meego-mcporter call meego list_project_team --args '{"project_key":"你的project_key"}' --config /workspace/meego-config.json
```

---

### list_schedule
**查成员排期与工作量明细**
```bash
npx @lark-project/meego-mcporter call meego list_schedule --args '{"project_key":"你的project_key","user_keys":["你的user_key"],"start_time":"2026-03-01","end_time":"2026-03-31"}' --config /workspace/meego-config.json
```
- `start_time` / `end_time`：格式 `YYYY-MM-DD`，最大范围3个月
- `work_item_type_keys`：限定工作项类型，如 `["story", "issue"]`

---

### search_user_info
**查用户信息**
```bash
npx @lark-project/meego-mcporter call meego search_user_info --args '{"project_key":"你的project_key","user_keys":["你的user_key"]}' --config /workspace/meego-config.json
```

---

### search_project_info
**查项目空间信息**
```bash
npx @lark-project/meego-mcporter call meego search_project_info --args '{"project_key":"你的项目名称"}' --config /workspace/meego-config.json
# 或用 simple_name
npx @lark-project/meego-mcporter call meego search_project_info --args '{"project_key":"your_simple_name"}' --config /workspace/meego-config.json
```
返回：project_key（数字）、simple_name、空间名称

---

### list_charts
**查视图下所有图表**
```bash
npx @lark-project/meego-mcporter call meego list_charts --args '{"project_key":"你的project_key","view_id":"view_xxx"}' --config /workspace/meego-config.json
```

---

### get_chart_detail
**查图表详情**
```bash
npx @lark-project/meego-mcporter call meego get_chart_detail --args '{"project_key":"你的project_key","chart_id":"chart_xxx"}' --config /workspace/meego-config.json
```

---

### search_view_by_title
**按标题搜索视图**
```bash
npx @lark-project/meego-mcporter call meego search_view_by_title --args '{"project_key":"你的project_key","key_word":"迭代","view_scope":"all"}' --config /workspace/meego-config.json
```

---

### list_workitem_comments
**查工作项评论列表**
```bash
npx @lark-project/meego-mcporter call meego list_workitem_comments --args '{"project_key":"你的project_key","work_item_id":6458194568}' --config /workspace/meego-config.json
```

---

### list_related_workitems
**查某工作项关联的其他工作项**
```bash
npx @lark-project/meego-mcporter call meego list_related_workitems --args '{"project_key":"你的project_key","work_item_id":6458194568,"work_item_type":"issue","relation_key":"xxx"}' --config /workspace/meego-config.json
```

---

### create_fixed_view
**创建固定视图**
```bash
npx @lark-project/meego-mcporter call meego create_fixed_view --args '{"project_key":"你的project_key","name":"我的工作项","work_item_type":"issue","work_item_id_list":["6458194568"]}' --config /workspace/meego-config.json
```

---

### get_view_detail
**查视图详情**
```bash
npx @lark-project/meego-mcporter call meego get_view_detail --args '{"project_key":"你的project_key","view_id":"view_xxx"}' --config /workspace/meego-config.json
```

---

## 二、操作类工具（Write）

### add_comment
**添加评论**
```bash
npx @lark-project/meego-mcporter call meego add_comment --args '{"project_key":"你的project_key","work_item_id":6458194568,"comment_content":"这是一条评论，支持markdown格式"}' --config /workspace/meego-config.json
```
- `comment_content`：支持 markdown
- 也可只传 `url` 参数，自动解析项目和工作项

---

### update_field
**修改工作项字段**
```bash
npx @lark-project/meego-mcporter call meego update_field --args '{"project_key":"你的project_key","work_item_id":6458194568,"fields":["priority:1","name:新名称"]}' --config /workspace/meego-config.json
```
- `fields`：数组，每项格式 `字段key:值`
- 字段key 从 `list_workitem_field_config` 获取

---

### create_workitem
**创建工作项**
```bash
npx @lark-project/meego-mcporter call meego create_workitem --args '{"project_key":"你的project_key","work_item_type":"issue","fields":["name:新缺陷标题","priority:1"]}' --config /workspace/meego-config.json
```
- 先用 `get_workitem_field_meta` 查必要字段和格式

---

## 三、项目基础信息工具

| 工具名 | 用途 | 关键参数 |
|--------|------|---------|
| search_project_info | 查项目空间信息 | project_key（支持中文名/simplename） |
| list_project_team | 查所有团队 | project_key |
| list_workitem_types | 查所有工作项类型 | project_key |
| search_user_info | 查用户信息 | user_keys + project_key |

---

## 四、MQL 查询工具

### search_by_mql
**MQL 自由查询**（语法最复杂，见 mql.md）

```bash
npx @lark-project/meego-mcporter call meego search_by_mql --args '{"project_key":"你的project_key","mql":"<MQL语句>"}' --config /workspace/meego-config.json
```
- `session_id`：分页用，传上次返回的 session_id
- ⚠️ 字段名需精确匹配 API 字段名
