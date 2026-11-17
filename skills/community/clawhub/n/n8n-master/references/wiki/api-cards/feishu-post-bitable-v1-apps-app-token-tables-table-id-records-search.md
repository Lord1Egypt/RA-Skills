# 查询记录

## 何时读取

当用户需要在 n8n 里通过 HTTP Request 节点调用这个飞书 / Lark API 时读取。

## Endpoint

- Method: `POST`
- URL: `https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/records/search`

## Auth / Headers

- `Authorization: Bearer <tenant access token from previous auth step or environment>`
- `Content-Type: application/json; charset=utf-8`
- 不要在 workflow JSON 或示例里写入真实 app secret、tenant access token、user access token。

## n8n HTTP Request 配置

- Method: `POST`
- URL: 将 `:path_param` 替换为 n8n expression，例如 `{{$json.app_token}}`。
- Authentication: 通常选 `None`，用 headers 手动传 Bearer token；也可以封装为 n8n credential。
- Send Headers: on
- Send Body: 视接口请求体决定；写入 JSON 时使用官方字段结构。

## 关键字段线索

- 权限要求; **调用该 API 所需的权限。开启其中任意一项权限即可调用**; 开启任一权限即可 | 根据条件搜索记录(base:record:retrieve); 查看、评论、编辑和管理多维表格(bitable:app); 查看、评论和导出多维表格(bitable:app:readonly)
- 字段权限要求 | **注意事项**：该接口返回体中存在下列敏感字段，仅当开启对应的权限后才会返回；如果无需获取这些字段，则不建议申请; 获取用户基本信息(contact:user.base:readonly); 获取用户 user ID(contact:user.employee_id:readonly); 以应用身份访问通讯录(contact:contact:access_as_app); 读取通讯录(contact:contact:readonly); 以应用身份读取通讯录(contact:contact:readonly_as_app)
- user_id_type | string | 否 | 用户 ID 类型; **示例值**：open_id; **可选值有**：; - open_id：标识一个用户在某个应用中的身份。同一个用户在不同应用中的 Open ID 不同。了解更多：如何获取 Open ID; - union_id：标识一个用户在某个应用开发商下的身份。同一用户在同一开发商下的应用中的 Union ID 是相同的，在不同开发商下的应用中的 Union ID 是不同的。通过 Union ID，应用开发商可以把同个用户在多个应用中的身份关联起来。了解更多：如何获取 Union ID？; - user_id：标识一个用户在某个租户内的身份。同一个用户在租户 A 和租户 B 内的 User ID 是不同的。在同一个租户内，一个用户的 User ID 在所有应用（包括商店应用）中都保持一致。User ID 主要用于在不同的应用间打通用户数据。了解更多：如何获取 User ID？; **默认值**：`open_id`; **当值为 `user_id`，字段权限要求**：; 获取用户 user ID(contact:user.employee_id:readonly)

## 注意事项

- 权限要求; **调用该 API 所需的权限。开启其中任意一项权限即可调用**; 开启任一权限即可 | 根据条件搜索记录(base:record:retrieve); 查看、评论、编辑和管理多维表格(bitable:app); 查看、评论和导出多维表格(bitable:app:readonly)
- 字段权限要求 | **注意事项**：该接口返回体中存在下列敏感字段，仅当开启对应的权限后才会返回；如果无需获取这些字段，则不建议申请; 获取用户基本信息(contact:user.base:readonly); 获取用户 user ID(contact:user.employee_id:readonly); 以应用身份访问通讯录(contact:contact:access_as_app); 读取通讯录(contact:contact:readonly); 以应用身份读取通讯录(contact:contact:readonly_as_app)
- user_id_type | string | 否 | 用户 ID 类型; **示例值**：open_id; **可选值有**：; - open_id：标识一个用户在某个应用中的身份。同一个用户在不同应用中的 Open ID 不同。了解更多：如何获取 Open ID; - union_id：标识一个用户在某个应用开发商下的身份。同一用户在同一开发商下的应用中的 Union ID 是相同的，在不同开发商下的应用中的 Union ID 是不同的。通过 Union ID，应用开发商可以把同个用户在多个应用中的身份关联起来。了解更多：如何获取 Union ID？; - user_id：标识一个用户在某个租户内的身份。同一个用户在租户 A 和租户 B 内的 User ID 是不同的。在同一个租户内，一个用户的 User ID 在所有应用（包括商店应用）中都保持一致。User ID 主要用于在不同的应用间打通用户数据。了解更多：如何获取 User ID？; **默认值**：`open_id`; **当值为 `user_id`，字段权限要求**：; 获取用户 user ID(contact:user.employee_id:readonly)
- 飞书接口经常同时受应用权限、文档权限、字段权限影响；403/400 时先核对权限和 token 类型。

