# 更新字段

## 何时读取

当用户需要在 n8n 里通过 HTTP Request 节点调用这个飞书 / Lark API 时读取。

## Endpoint

- Method: `PUT`
- URL: `https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/fields/:field_id`

## Auth / Headers

- `Authorization: Bearer <tenant access token from previous auth step or environment>`
- `Content-Type: application/json; charset=utf-8`
- 不要在 workflow JSON 或示例里写入真实 app secret、tenant access token、user access token。

## n8n HTTP Request 配置

- Method: `PUT`
- URL: 将 `:path_param` 替换为 n8n expression，例如 `{{$json.app_token}}`。
- Authentication: 通常选 `None`，用 headers 手动传 Bearer token；也可以封装为 n8n credential。
- Send Headers: on
- Send Body: 视接口请求体决定；写入 JSON 时使用官方字段结构。

## 关键字段线索

- 权限要求; **调用该 API 所需的权限。开启其中任意一项权限即可调用**; 开启任一权限即可 | 更新字段(base:field:update); 查看、评论、编辑和管理多维表格(bitable:app)
- 200 | 1254301 | OperationTypeError | 多维表格未开启高级权限或不支持开启高级权限
- 403 | 1254302 | Permission denied. | 调用身份缺少多维表格的高级权限。你需要为调用身份授予高级权限。

## 注意事项

- 权限要求; **调用该 API 所需的权限。开启其中任意一项权限即可调用**; 开启任一权限即可 | 更新字段(base:field:update); 查看、评论、编辑和管理多维表格(bitable:app)
- 200 | 1254301 | OperationTypeError | 多维表格未开启高级权限或不支持开启高级权限
- 403 | 1254302 | Permission denied. | 调用身份缺少多维表格的高级权限。你需要为调用身份授予高级权限。
- 飞书接口经常同时受应用权限、文档权限、字段权限影响；403/400 时先核对权限和 token 类型。

