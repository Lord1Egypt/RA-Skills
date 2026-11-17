# 列出字段

## 何时读取

当用户需要在 n8n 里通过 HTTP Request 节点调用这个飞书 / Lark API 时读取。

## Endpoint

- Method: `GET`
- URL: `https://open.feishu.cn/open-apis/bitable/v1/apps/:app_token/tables/:table_id/fields`

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

- 权限要求; **调用该 API 所需的权限。开启其中任意一项权限即可调用**; 开启任一权限即可 | 获取字段信息(base:field:read); 查看、评论、编辑和管理多维表格(bitable:app); 查看、评论和导出多维表格(bitable:app:readonly)
- 200 | 1254301 | OperationTypeError | 多维表格未开启高级权限或不支持开启高级权限
- 403 | 1254302 | Permission denied. | 调用身份缺少多维表格的高级权限。你需给予调用身份数据表的 **可管理** 权限或多维表格的 **可管理** 等权限，再重新调用。具体步骤如下所示：; - 对用户授予高级权限，你可在 **多维表格高级权限设置** 中添加用户，为用户开通足够权限；或在多维表格页面右上方 **分享** 入口为当前用户添加可管理权限。详情参考飞书帮助中心文档使用多维表格高级权限。; ![](//sf3-cn.feishucdn.com/obj/open-platform-opendoc/df3911b4f747d75914f35a46962d667d_dAsfLjv3QC.png?height=546&lazyload=true&maxWidth=550); - 对应用授予高级权限，你需通过多维表格页面右上方 **「...」** -> **「...更多」** ->**「添加文档应用」** 入口为应用添加可管理权限。; ![](//sf3-cn.feishucdn.com/obj/open-platform-opendoc/22c027f63c540592d3ca8f41d48bb107_CSas7OYJBR.png?height=1994&lazyload=true&maxWidth=550&width=3278); !image.png; **注意**：; 在 **添加文档应用** 前，你需确保目标应用至少开通了一个多维表格的 API 权限。否则你将无法在文档应用窗口搜索到目标应用。 ; - 你也可以在 **多维表格高级权限设置** 中添加用户或一个包含应用的群组，给予这个群自定义的读写等权限。

## 注意事项

- 权限要求; **调用该 API 所需的权限。开启其中任意一项权限即可调用**; 开启任一权限即可 | 获取字段信息(base:field:read); 查看、评论、编辑和管理多维表格(bitable:app); 查看、评论和导出多维表格(bitable:app:readonly)
- 200 | 1254301 | OperationTypeError | 多维表格未开启高级权限或不支持开启高级权限
- 403 | 1254302 | Permission denied. | 调用身份缺少多维表格的高级权限。你需给予调用身份数据表的 **可管理** 权限或多维表格的 **可管理** 等权限，再重新调用。具体步骤如下所示：; - 对用户授予高级权限，你可在 **多维表格高级权限设置** 中添加用户，为用户开通足够权限；或在多维表格页面右上方 **分享** 入口为当前用户添加可管理权限。详情参考飞书帮助中心文档使用多维表格高级权限。; ![](//sf3-cn.feishucdn.com/obj/open-platform-opendoc/df3911b4f747d75914f35a46962d667d_dAsfLjv3QC.png?height=546&lazyload=true&maxWidth=550); - 对应用授予高级权限，你需通过多维表格页面右上方 **「...」** -> **「...更多」** ->**「添加文档应用」** 入口为应用添加可管理权限。; ![](//sf3-cn.feishucdn.com/obj/open-platform-opendoc/22c027f63c540592d3ca8f41d48bb107_CSas7OYJBR.png?height=1994&lazyload=true&maxWidth=550&width=3278); !image.png; **注意**：; 在 **添加文档应用** 前，你需确保目标应用至少开通了一个多维表格的 API 权限。否则你将无法在文档应用窗口搜索到目标应用。 ; - 你也可以在 **多维表格高级权限设置** 中添加用户或一个包含应用的群组，给予这个群自定义的读写等权限。
- 飞书接口经常同时受应用权限、文档权限、字段权限影响；403/400 时先核对权限和 token 类型。

