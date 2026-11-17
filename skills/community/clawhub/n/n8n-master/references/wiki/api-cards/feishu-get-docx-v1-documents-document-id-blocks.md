# 获取文档所有块

## 何时读取

当用户需要在 n8n 里通过 HTTP Request 节点调用这个飞书 / Lark API 时读取。

## Endpoint

- Method: `GET`
- URL: `https://open.feishu.cn/open-apis/docx/v1/documents/:document_id/blocks`

## Auth / Headers

- `Authorization: Bearer <tenant access token from previous auth step or environment>`
- `Content-Type: application/json; charset=utf-8`
- 不要在 workflow JSON 或示例里写入真实 app secret、tenant access token、user access token。

## n8n HTTP Request 配置

- Method: `GET`
- URL: 将 `:path_param` 替换为 n8n expression，例如 `{{$json.app_token}}`。
- Authentication: 通常选 `None`，用 headers 手动传 Bearer token；也可以封装为 n8n credential。
- Send Headers: on
- Send Body: 视接口请求体决定；写入 JSON 时使用官方字段结构。

## 关键字段线索

- 权限要求; **调用该 API 所需的权限。开启其中任意一项权限即可调用**; 开启任一权限即可 | 创建及编辑新版文档(docx:document); 查看新版文档(docx:document:readonly)
- 字段权限要求 | **注意事项**：该接口返回体中存在下列敏感字段，仅当开启对应的权限后才会返回；如果无需获取这些字段，则不建议申请; 获取用户 user ID(contact:user.employee_id:readonly)
- document_revision_id | int | 否 | 查询的文档版本，-1 表示文档最新版本。文档创建后，版本为 1。; - 若查询的版本为文档最新版本，则需要持有文档的阅读权限；; - 若查询的版本为文档的历史版本，则需要持有文档的编辑权限。; 你可通过调用获取文档基本信息获取文档的 revision_id; **示例值**：-1; **默认值**：`-1`; **数据校验规则**：; - 最小值：`-1`

## 注意事项

- 权限要求; **调用该 API 所需的权限。开启其中任意一项权限即可调用**; 开启任一权限即可 | 创建及编辑新版文档(docx:document); 查看新版文档(docx:document:readonly)
- 字段权限要求 | **注意事项**：该接口返回体中存在下列敏感字段，仅当开启对应的权限后才会返回；如果无需获取这些字段，则不建议申请; 获取用户 user ID(contact:user.employee_id:readonly)
- document_revision_id | int | 否 | 查询的文档版本，-1 表示文档最新版本。文档创建后，版本为 1。; - 若查询的版本为文档最新版本，则需要持有文档的阅读权限；; - 若查询的版本为文档的历史版本，则需要持有文档的编辑权限。; 你可通过调用获取文档基本信息获取文档的 revision_id; **示例值**：-1; **默认值**：`-1`; **数据校验规则**：; - 最小值：`-1`
- 飞书接口经常同时受应用权限、文档权限、字段权限影响；403/400 时先核对权限和 token 类型。

