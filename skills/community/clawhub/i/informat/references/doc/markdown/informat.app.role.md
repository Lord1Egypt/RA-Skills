<!-- DOCKEY: rol-5b3d8 -->
# Application Role Permission Documentation

This document explains how application roles (`RoleDefine`) store permissions, especially the `permissionList` field.

Before changing role permissions, always read the real application configuration first. Do not fabricate role IDs, module IDs, or permission IDs.

Recommended flow:

1. Call `_query_app_define_designer` to get the role list and module list.
2. Call `_app_permission_list` to get custom permission definitions.
3. Call `_app_query_role_by_id` to read the full target `RoleDefine`.
4. Modify `permissionList` incrementally from the original object.
5. Call `_app_update_role` with `updateFieldList` set to `["permissionList"]` and pass the new permission list.
6. If the change must take effect in the published app, remind the user to publish the app in the designer.

---

## 1. RoleDefine Structure

Example application role definition:

```json
{
  "id": "b29cshzy9mlf1",
  "key": "tester",
  "name": "Tester",
  "build": 2,
  "scope": "App",
  "isAdmin": false,
  "isDeleted": false,
  "createTime": "Sat Jun 06 21:47:22 CST 2026",
  "createUser": "skydu",
  "updateTime": "Sat Jun 06 21:49:19 CST 2026",
  "updateUser": "skydu",
  "draftVersion": 2,
  "permissionList": [
    "AppAccess",
    "AppMember",
    "cccc",
    "ct8kwtdpafpsl_aaa"
  ]
}
```

Key fields:

| Field | Description |
|------|-------------|
| `id` | Define object ID. Keep it when saving the role object. |
| `key` | Role identifier, unique in the app, for example `tester`. |
| `name` | Role display name. |
| `scope` | Application roles use `App`. |
| `isAdmin` | Whether this is the administrator role. Administrator roles have all permissions and should not be modified. |
| `permissionList` | Permission ID list owned by this role. |

---

## 2. permissionList ID Rules

Each item in `permissionList` is a permission ID. Permission IDs have three categories:

1. Built-in app-level permissions: use the permission name directly.
2. Built-in module-level permissions: use `{moduleId}_{permissionName}`.
3. Custom app permissions: format depends on `AppPermissionDefine.moduleId`.

---

## 3. Built-in App-Level Permissions

Built-in app-level permissions do not have a module prefix:

| Permission ID | Description |
|---------------|-------------|
| `AppAccess` | Allows access to the application. Members without it usually cannot enter the app. |
| `AppMember` | Allows managing application members. |

Example:

```json
{
  "permissionList": ["AppAccess", "AppMember"]
}
```

---

## 4. Module Access Permissions

Each module generates a module access permission:

```text
{moduleId}_{moduleType}Access
```

Examples:

| Module ID | Module Type | Permission ID |
|-----------|-------------|---------------|
| `customer` | `Table` | `customer_TableAccess` |
| `orderProcess` | `BpmnData` | `orderProcess_BpmnDataAccess` |
| `kbSearch` | `Textindex` | `kbSearch_TextindexAccess` |

Module IDs must come from the real module list returned by `_query_app_define_designer`.

---

## 5. Table Module Permissions

When the module type is `Table`, these operation permissions are supported:

| Permission ID Format | Description |
|----------------------|-------------|
| `{tableId}_TableAccess` | Access the table module. |
| `{tableId}_TableQuery` | Query records. |
| `{tableId}_TableInsert` | Insert records. |
| `{tableId}_TableUpdate` | Update records. |
| `{tableId}_TableDelete` | Delete records. |

Example:

```json
{
  "permissionList": [
    "customer_TableAccess",
    "customer_TableQuery",
    "customer_TableInsert",
    "customer_TableUpdate",
    "customer_TableDelete"
  ]
}
```

---

## 6. Survey Module Permissions

When the module type is `Survey`, these operation permissions are supported:

| Permission ID Format | Description |
|----------------------|-------------|
| `{moduleId}_SurveyAccess` | Access the survey module. |
| `{moduleId}_SurveyEdit` | Edit the survey. |

---

## 7. Workflow Data Module Permissions

When the module type is `BpmnData`, these operation permissions are supported:

| Permission ID Format | Description |
|----------------------|-------------|
| `{moduleId}_BpmnDataAccess` | Access the workflow data module. |
| `{moduleId}_BpmnDataViewData` | View process data. |
| `{moduleId}_BpmnDataViewTask` | View process tasks. |
| `{moduleId}_BpmnDataDeleteProcess` | Delete process instances. |
| `{moduleId}_BpmnDataRevokeProcess` | Revoke process instances. |
| `{moduleId}_BpmnDataEditData` | Edit process data. |
| `{moduleId}_BpmnDataProcessEditStatus` | Edit process status. |
| `{moduleId}_BpmnDataProcessEditVersion` | Edit process version. |
| `{moduleId}_BpmnDataProcessEditStartup` | Edit process startup settings. |

---

## 8. Text Index Module Permissions

When the module type is `Textindex`, these operation permissions are supported:

| Permission ID Format | Description |
|----------------------|-------------|
| `{moduleId}_TextindexAccess` | Access the text index module. |
| `{moduleId}_TextindexQuery` | Query the text index. |

---

## 9. Custom App Permissions

Custom permissions come from `AppPermissionDefine` and must be queried through `_app_permission_list`. Do not infer custom permissions from `_query_app_define_designer`.

Permission ID generation rules:

| `moduleId` | Permission ID Format |
|------------|----------------------|
| `App` | `{key}` |
| Not `App` | `{moduleId}_{key}` |

Example:

```json
{
  "moduleId": "App",
  "key": "cccc"
}
```

Role permission:

```json
"cccc"
```

Example:

```json
{
  "moduleId": "ct8kwtdpafpsl",
  "key": "aaa"
}
```

Role permission:

```json
"ct8kwtdpafpsl_aaa"
```

---

## 10. Custom Permission Management Methods

### 10.1 `_app_permission_list`

Queries all custom permission definitions in the current app.

Use it to:

- Get real `AppPermissionDefine.id` values.
- Get custom permission `moduleId`, `key`, `name`, and `remark`.
- Check whether a permission already exists before create, update, or delete operations.

Important rules:

- If a custom permission is bound to a table module, returned `moduleId` is the table key, not the internal module ID.
- If `moduleId` is `App`, the permission is app-level.

Example response:

```json
[
  {
    "id": "perm001",
    "moduleId": "App",
    "key": "cccc",
    "name": "App-level custom permission"
  },
  {
    "id": "perm002",
    "moduleId": "customer",
    "key": "aaa",
    "name": "Customer advanced permission"
  }
]
```

Here `customer` is the table key. In role `permissionList`, the permission IDs are:

```json
[
  "cccc",
  "customer_aaa"
]
```

### 10.2 `_app_query_role_by_id`

Queries application role details by role key.

Before calling:

1. Call `_query_app_define_designer` to get the real role list.
2. Read `references/system_app_query_role_by_id.json`.
3. Use the role `key` as the `id` parameter.

The returned `permissionList` converts internal table module IDs to table keys. For example, internally stored `ct8kwtdpafpsl_TableQuery` returns as `customer_TableQuery`. Later `_app_update_role` calls can keep using the table key format.

Example:

```json
{
  "id": "tester"
}
```

### 10.3 `_app_update_role`

Updates application role name, remark, and permission list.

When changing role permissions:

1. Call `_query_app_define_designer` to get real roles and modules.
2. Call `_app_permission_list` to get custom permission definitions.
3. Call `_app_query_role_by_id` to read the target `RoleDefine`, then modify the original `permissionList` incrementally.
4. Call `_app_update_role` to update `permissionList`.

Example:

```json
{
  "id": "tester",
  "updateFieldList": ["permissionList"],
  "permissionList": [
    "AppAccess",
    "customer_TableAccess",
    "customer_TableQuery",
    "customer_export"
  ]
}
```

Notes:

- `id` is the role key, not the RoleDefine object ID.
- `permissionList` replaces the original role permission list, so read the original list first and modify it incrementally.
- Do not modify the `admin` administrator role.

### 10.4 `_app_permission_create`

Creates a custom app permission.

Before calling:

1. Call `_query_app_define_designer` to get the real module list.
2. Call `_app_permission_list` to confirm the same `moduleId + key` does not exist.
3. Read `references/system_app_permission_create.json`.

Parameter rules:

| Field | Description |
|------|-------------|
| `moduleId` | Use `App` for app-level permissions; use table key for table permissions; real module ID can be used for non-table modules. |
| `key` | Custom permission identifier, unique under the same `moduleId`; must not use built-in permission names. |
| `name` | Permission display name. |
| `remark` | Optional permission description. |

Example:

```json
{
  "moduleId": "customer",
  "key": "export",
  "name": "Customer export permission",
  "remark": "Allows exporting customer data"
}
```

### 10.5 `_app_permission_update`

Updates a custom app permission.

Before calling:

1. Call `_app_permission_list` to get the real `id`.
2. Read `references/system_app_permission_update.json`.
3. Use `updateFieldList` to declare fields changed in this call.

Supported fields:

```json
["moduleId", "key", "name", "remark"]
```

Example:

```json
{
  "id": "perm002",
  "updateFieldList": ["name", "remark"],
  "name": "Customer data export permission",
  "remark": "Allows exporting customer data to files"
}
```

If changing `moduleId` to a table module, still pass the table key. The system converts it to the internal module ID when saving.

### 10.6 `_app_permission_delete`

Deletes a custom app permission.

Before calling:

1. Call `_app_permission_list` to get the real `id`.
2. Confirm the permission should be deleted.
3. Read `references/system_app_permission_delete.json`.

After deletion, the system also removes this permission from role `permissionList` values.

Example:

```json
{
  "id": "perm002"
}
```

---

## 11. AI Modification Rules

- Always read real application configuration first. Do not guess `role.id`, `role.key`, `moduleId`, or permission IDs.
- Custom permissions must be queried through `_app_permission_list`; do not infer custom permission definitions from `_query_app_define_designer`.
- Modify `permissionList` incrementally from the original `RoleDefine`; do not rebuild unknown fields.
- Do not modify administrator roles where `isAdmin=true` or `key=admin`.
- Do not add non-existent module permissions or custom permissions into `permissionList`.
- To change role name, remark, or permission list, use `_app_update_role`.
- To change `permissionList`, first read the full `RoleDefine` with `_app_query_role_by_id`, modify the original list incrementally, then call `_app_update_role`.
