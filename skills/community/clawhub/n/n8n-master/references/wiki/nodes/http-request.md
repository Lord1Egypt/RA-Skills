# HTTP Request node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `HTTP Request node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.httprequest`
- node group: `core-nodes`

## 核心要点

- Learn how to use the HTTP Request node in n8n. Follow technical documentation to integrate HTTP Request node into your workflows.

## 关键操作 / 参数线索

- DELETE
- GET
- HEAD
- OPTIONS
- PATCH
- POST
- PUT
- Basic auth
- Custom auth
- Digest auth
- Header auth
- OAuth1 API
- OAuth2 API
- Query auth
- **Using Fields Below**: Enter **Name**/**Value** pairs of **Query Parameters**. To enter more query parameter name/value pairs, select **Add Parameter**. The name is the name of the field you're filtering on, and the value is the filter value.
- **Using JSON**: Enter **JSON** to define your query parameters.
- **Using Fields Below**: Enter **Name**/**Value** pairs of **Header Parameters**. To enter more header parameter name/value pairs, select **Add Parameter**. The name is the header you wish to set, and the value is the value you want to pass for that header.
- **Using JSON**: Enter **JSON** to define your header parameters.

## 常用选项线索

- **No Brackets**: Arrays will format as the name=value for each item in the array, for example: `foo=bar&foo=qux`.
- **Brackets Only**: The node adds square brackets after each array name, for example: `foo[]=bar&foo[]=qux`.
- **Brackets with Indices**: The node adds square brackets with an index value after each array name, for example: `foo[0]=bar&foo[1]=qux`.
- **Items per Batch**: Enter the number of input items to include in each batch.
- **Batch Interval**: Enter the time to wait between each batch of requests in milliseconds. Enter 0 for no batch interval.
- **Include Response Headers and Status**: By default, the node returns only the body. Turn this option on to return the full response (headers and response status code) as well as the body.
- **Never Error**: By default, the node returns success only when the response returns with a 2xx code. Turn this option on to return success regardless of the code returned.
- **Response Format**: Select the format in which the data gets returned. Choose from:
- **Autodetect** (default): The node detects and formats the response based on the data returned.
- **File**: Select this option to put the response into a file. Enter the field name where you want the file returned in **Put Output in Field**.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。
- 存在 common issues 文档；排障时优先读取下方 source 中的 common-issues 文件。

