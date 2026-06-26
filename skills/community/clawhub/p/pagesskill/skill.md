---
name: nocobase-page-building
description: Guide AI to build NocoBase pages — menus, tables, forms, popups, KPIs, JS blocks, outlines, event flows
triggers:
  - 搭建页面
  - 创建菜单
  - 页面
  - 区块
  - page
  - build page
  - create menu
  - table block
  - form
  - outline
  - 大纲
tools:
  - nb_crud_page
  - nb_create_group
  - nb_create_page
  - nb_create_menu
  - nb_list_routes
  - nb_delete_route
  - nb_page_layout
  - nb_table_block
  - nb_addnew_form
  - nb_edit_action
  - nb_detail_popup
  - nb_filter_form
  - nb_kpi_block
  - nb_js_block
  - nb_js_column
  - nb_set_layout
  - nb_clean_tab
  - nb_outline
  - nb_event_flow
  - nb_inspect_page
  - nb_inspect_all
  - nb_show_page
  - nb_read_node
  - nb_locate_node
  - nb_patch_field
  - nb_patch_column
  - nb_add_field
  - nb_remove_field
  - nb_add_column
  - nb_remove_column
  - nb_list_pages
---

# NocoBase Page Building

## Core Philosophy: Agent-First Development

This toolkit is **designed for AI agents to build and maintain pages**. Every tool
prioritizes agent convenience with sensible defaults:

- **`nb_crud_page`**: One call builds a complete page — agents don't need to
  orchestrate 8+ individual tools.
- **Detail popup auto-generation**: When `detail_json` is omitted, the detail popup
  is automatically generated from the edit form's field layout (same fields, same
  dividers, minus required markers). Agents ONLY need to specify `detail_json` when
  they want sub-table tabs or custom blocks beyond the main detail fields.
- **`nb_inspect_page`**: Compact visual output designed for agent comprehension —
  structure at a glance, not raw JSON.
- **`nb_read_node`**: Deep-dive into any node's event flows, JS code, or linkage
  rules when debugging.

**Defaults eliminate unnecessary work.** If something has a sensible default, the
agent should NOT specify it. The less the agent writes, the fewer mistakes.

---

You are guiding the user to build pages in NocoBase using FlowModel API. Follow this exact workflow.

## Key Concepts

### Group vs Page
- **Group** (📁): Folder in sidebar. NO content, only holds children.
- **Page** (📄): Has actual content (tables, forms, etc.). Must be under a group.

### FlowModel Tree Structure
```
Tab (RouteModel)
  └── BlockGridModel (layout container)
        ├── TableBlockModel (table)
        │     ├── TableColumnModel (column) → DisplayFieldModel
        │     ├── AddNewActionModel → ChildPageModel → CreateFormModel
        │     ├── TableActionsColumnModel → EditActionModel
        │     └── FilterActionModel, RefreshActionModel
        ├── FilterFormBlockModel (search bar)
        ├── JSBlockModel (custom JS content)
        └── ...more blocks
```

### CRITICAL: FlowModel API is Full Replace
The `flowModels:update` API does a **full replace**, not incremental merge. The client always does GET → deep_merge → PUT internally. Never send partial data.

## Recommended: Fast Path (nb_crud_page)

For standard CRUD pages, use `nb_crud_page` — it creates layout + KPIs + filter + table + forms + popup in ONE call:

```
nb_crud_page("tab_uid", "nb_crm_customers",
    '["name","code","status","industry","phone","createdAt"]',
    '--- 基本信息\nname* | code\ncustomer_type | industry\nstatus | level\n--- 联系方式\nphone | email\naddress',
    filter_fields='["name","status","industry"]',
    kpis_json='[{"title":"客户总数"},{"title":"已签约","filter":{"status":"已签约"},"color":"#52c41a"},{"title":"跟进中","filter":{"status":"跟进中"},"color":"#1890ff"}]',
    detail_json='[{"title":"客户详情","fields":"name | code\nstatus | level\nindustry | scale\nphone | email\naddress\nremark"},{"title":"联系人","assoc":"contacts","coll":"nb_crm_contacts","fields":["name","position","mobile","email"]}]')
```

This replaces 8+ individual tool calls with ONE call. Use this for every standard page.

**When to use individual tools instead:**
- Non-standard layouts (multiple tables on one page)
- JS blocks, event flows, outlines
- Page modifications after initial build

## Manual Path (Individual Tools)

### Phase 1: Menu Structure

Use `nb_create_menu` for the simplest approach:

```
nb_create_menu("Asset Management", top_group_id,
    '[["Asset Ledger","databaseoutlined"],["Purchases","shoppingcartoutlined"]]',
    group_icon="bankoutlined")
```

This creates a group + pages in one call, returning `{"Asset Ledger": "tab_uid_1", "Purchases": "tab_uid_2"}`.

Or build manually:
1. `nb_create_group("Module Name", parent_id)` — creates the folder
2. `nb_create_page("Page Name", group_id)` — creates each page

### Phase 2: Page Content (Per Page)

For each page, follow this order:

#### Step 1: Create Page Layout
```
nb_page_layout("tab_uid")  →  returns grid_uid
```
This cleans existing content (idempotent) and creates a BlockGridModel.

#### Step 2: Create KPI Cards (Optional)
```
nb_kpi_block(grid, "Total", "nb_pm_projects")
nb_kpi_block(grid, "Active", "nb_pm_projects", filter_='{"status":"active"}', color="#52c41a")
```

#### Step 3: Create Filter/Search Bar
```
nb_filter_form(grid, "nb_pm_projects", '["name","code","description"]', target_uid=table_uid)
```

**Parameters:**
- `label` (str, default `"Search"`): Placeholder label for the search input.

Note: Create filter AFTER table (needs table_uid for target), but place it ABOVE in layout.

#### Step 4: Create Table Block
```
nb_table_block(grid, "nb_pm_projects",
    '["name","code","status","priority","createdAt"]',
    first_click=true, title="Projects")
```

**Parameters:**
- `first_click` (bool, default `true`): If true, the first column becomes click-to-open
  (users click to view detail popup). Set to `false` if no detail popup needed.
- `title` (str, optional): Card header title displayed above the table.

Returns: `{table_uid, addnew_uid, actcol_uid}`

#### Step 5: Create AddNew Form
```
nb_addnew_form(addnew_uid, "nb_pm_projects",
    "--- Basic Info\nname* | code\nstatus | priority\n--- Details\ndescription")
```

**Fields DSL syntax:**
- `name` — single field, full width
- `name*` — required field
- `name | code` — two fields side by side (auto 12+12)
- `name:16 | code:8` — explicit widths (total=24)
- `--- Section Title` — divider with label
- `---` — plain divider

#### Step 6: Create Edit Action
```
nb_edit_action(actcol_uid, "nb_pm_projects",
    "--- Basic Info\nname* | code\nstatus | priority\n--- Details\ndescription")
```

#### Step 7: Set Layout
```
nb_set_layout(grid_uid, '[
    [["kpi1",6],["kpi2",6],["kpi3",6],["kpi4",6]],
    [["filter1"]],
    [["table1"]]
]')
```

Layout rules:
- Each row is an array of `[uid, span]` pairs
- Spans use Ant Design grid (total = 24 per row)
- `[["uid"]]` or `[["uid",24]]` = full width
- `[["a",12],["b",12]]` = two equal columns

#### Step 8: Detail Popup (Auto-Generated by Default)

**You usually DON'T need to specify `detail_json`.** When omitted in `nb_crud_page`,
a "详情" tab is auto-generated using the same field layout as the Edit form
(form_fields DSL minus `*` required markers). This gives every page a meaningful
detail popup with zero extra work.

Only specify `detail_json` when you need:
- Sub-table tabs (e.g., customer → contacts, orders)
- JS blocks or custom layout inside the popup
- A different field layout from the edit form

```
# Custom detail popup (only when needed)
nb_detail_popup(click_field_uid, "nb_pm_projects", '[
    {"title":"Info", "fields":"--- Basic\\nname | code\\nstatus"},
    {"title":"Tasks", "assoc":"tasks", "coll":"nb_pm_tasks", "fields":["name","status"]}
]', mode="drawer", size="large")
```

**Detail popup modes:**
- `mode="drawer"` + `size="large"` — side panel, good for business detail pages
- `mode="drawer"` + `size="medium"` — smaller side panel, for reference data
- `mode="dialog"` + `size="small"` — modal dialog, for quick views

**Finding the click field UID:**
The first column in a table created with `first_click=true` is clickable. Use the click_field_uid from the column's DisplayFieldModel. The field_name passed to the find function must match the first column's field name.

**Multi-tab detail popup with sub-tables:**
```json
[
    {"title": "Details", "blocks": [
        {"type": "details", "fields": "--- Section 1\\nfield1 | field2\\nfield3"}
    ]},
    {"title": "Sub Items", "assoc": "items", "coll": "nb_order_items",
     "fields": ["name", "quantity", "price", "createdAt"]}
]
```
Note: The `assoc` sub-table requires an o2m relation to be defined between the parent and child collections.

#### Step 9: Outlines — Plan JS Capabilities (Recommended)
Use `nb_outline` to plan JS blocks/columns without writing actual code.
A dedicated JS agent implements them later.

**`kind` parameter** (default `"block"`):
- `"block"` — creates JSBlockModel on page grid (for KPI cards, charts)
- `"column"` — creates JSColumnModel in a table (for status tags, computed columns)
- `"item"` — creates JSItemModel in a form (for computed form fields)

```
# KPI outline (page-level block)
nb_outline(grid, "Active Count", '{"type":"kpi","collection":"assets","filter":{"status":"active"}}')

# Table JS column outline
nb_outline(table_uid, "Status Tag", '{"type":"status-tag","field":"status","colors":{"active":"green"}}', kind="column")

# Event flow outline (in form)
nb_outline(form_grid, "Auto Total", '{"type":"event-flow","event":"formValuesChange","formula":"qty*price"}', kind="item")
```

#### Step 10: Event Flows (Optional)
```
nb_event_flow(form_uid, "formValuesChange",
    "const v=ctx.form?.values||{}; if(v.qty&&v.price) ctx.form.setFieldsValue({total:v.qty*v.price});")
```

#### Step 11: JS Columns — Direct Implementation (Alternative to Outlines)
```
nb_js_column(table_uid, "Status",
    "const s=(ctx.record||{}).status;ctx.render(ctx.React.createElement(ctx.antd.Tag,{color:s==='active'?'green':'red'},s||'-'))",
    width=100)
```

**Parameters:**
- `width` (int, optional): Column width in pixels. Omit for auto-width.

### Phase 3: Verify & Debug — Three-Level Drill-Down

```
nb_inspect_all("CRM")            — system overview (~1 line per page, default)
nb_inspect_all("CRM", depth=1)   — full structure of every page

nb_inspect_page("客户列表")       — single page: forms, columns, popups, hidden-point annotations
                                    [JS 1200c] [2 events] [3 linkage] sort: field desc (drawer,large)

nb_read_node(uid, "events")      — deep-dive: JS code, event flows, linkage rules
nb_read_node(uid, "js")
nb_read_node(uid, "linkage")
```

**Full tree** (for raw UIDs): `nb_show_page("Page Title")`

**Workflow: Debug → Locate → Fix**
1. `nb_inspect_page` — find the problem area (empty popup, wrong layout, hidden-point hints)
2. `nb_read_node(uid, "events")` — see the actual event flow code or configuration
3. `nb_event_flow` / `nb_patch_field` / `nb_js_block` — fix it

## Common Patterns

### Standard CRUD Page
1. `page_layout` → grid
2. `kpi_block` × N → kpi cards
3. `table_block` → table + addnew + actcol
4. `filter_form` → search bar (target=table)
5. `addnew_form` → new record form
6. `edit_action` → edit record form
7. `set_layout` → arrange: KPIs row → filter → table
8. Optionally: `detail_popup`, `js_column`

### KPI Row Pattern
```
kpi1 = nb_kpi_block(grid, "Total", collection)
kpi2 = nb_kpi_block(grid, "Active", collection, filter_='{"status":"active"}', color="#52c41a")
kpi3 = nb_kpi_block(grid, "Pending", collection, filter_='{"status":"pending"}', color="#faad14")
# Then in layout: [["kpi1",8],["kpi2",8],["kpi3",8]]
```

### Multi-Block Detail Popup
```json
[
    {"title": "Overview", "blocks": [
        {"type": "details", "title": "Info", "fields": "name | code\nstatus"},
        {"type": "js", "title": "Stats", "code": "ctx.render(...)"}
    ], "sizes": [14, 10]},
    {"title": "Tasks", "assoc": "tasks", "coll": "nb_pm_tasks",
     "fields": ["name", "status", "createdAt"]}
]
```

### Page Modification & Debugging
For tweaking existing pages or diagnosing issues:
```
# 1. Overview — understand the page structure
nb_inspect_page("Page Title")

# 2. Find — locate a specific node
nb_locate_node("Page Title", field="status")  # returns UID
nb_locate_node("Page Title", block="addnew")  # find AddNew form

# 3. Debug — read node configuration
nb_read_node(uid, "events")     # event flow JS code
nb_read_node(uid, "js")         # JS block/column code
nb_read_node(uid, "linkage")    # button linkage rules

# 4. Fix — modify the node
nb_patch_field(uid, '{"required":true}')
nb_patch_column(column_uid, '{"width":120}')
nb_add_column(table_uid, collection, "new_field")
nb_remove_column(column_uid)
nb_event_flow(form_uid, "formValuesChange", "...")
```

**`nb_patch_field` common patches:**
```
nb_patch_field(uid, '{"required":true}')           # make field required
nb_patch_field(uid, '{"hidden":true}')             # hide field
nb_patch_field(uid, '{"defaultValue":"active"}')   # set default value
nb_patch_field(uid, '{"readOnly":true}')           # read-only field
```

**`nb_patch_column` common patches:**
```
nb_patch_column(uid, '{"width":120}')              # set column width
nb_patch_column(uid, '{"fixed":"left"}')           # pin column to left
nb_patch_column(uid, '{"title":"New Title"}')      # rename column header
```

**`nb_delete_route` — remove a menu item:**
```
nb_list_routes()                                    # find route_id
nb_delete_route(350416708763648)                     # delete group + children
```

**Batch inspect** — check all pages in a system:
```
nb_inspect_all("CRM")            # compact overview (1 line per page, default)
nb_inspect_all("CRM", depth=1)   # full structure of every page
nb_inspect_all()                  # ALL pages (compact)
```

## Ant Design Icons
Common icons for menus: `homeoutlined`, `settingoutlined`, `databaseoutlined`,
`shoppingcartoutlined`, `bankoutlined`, `tooloutlined`, `formoutlined`,
`barchartoutlined`, `piechartoutlined`, `idcardoutlined`, `caroutlined`,
`containeroutlined`, `clusteroutlined`, `apartmentoutlined`, `environmentoutlined`,
`shopoutlined`, `controloutlined`, `appstoreoutlined`, `inboxoutlined`,
`deleteoutlined`, `swapoutlined`, `sendoutlined`

## Status Tag Colors
For `ctx.antd.Tag` in JS columns/blocks:
- Green: active, completed, approved → `color: 'green'` or `'#52c41a'`
- Blue: in progress, processing → `color: 'blue'` or `'#1890ff'`
- Orange: pending, warning → `color: 'orange'` or `'#faad14'`
- Red: error, rejected, overdue → `color: 'red'` or `'#ff4d4f'`
- Default: draft, inactive → `color: 'default'`
