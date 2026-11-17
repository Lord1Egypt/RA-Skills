# Facebook Graph API node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Facebook Graph API node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.facebookgraphapi`
- node group: `app-nodes`

## 核心要点

- Learn how to use the Facebook Graph API node in n8n. Follow technical documentation to integrate Facebook Graph API node into your workflows.

## 关键操作 / 参数线索

- **Default**
- GET
- POST
- DELETE
- **Video Uploads**
- **Host URL**: The host URL for the request. The following options are available:
- **Default**: Requests are passed to the `graph.facebook.com` host URL. Used for the majority of requests.
- **Video**: Requests are passed to the `graph-video.facebook.com` host URL. Used for video upload requests only.
- **HTTP Request Method**: The method to be used for this request, from the following options:
- **GET**
- **POST**
- **DELETE**
- **Graph API Version**: The version of the Facebook Graph API to be used for this request.
- **Node**: The node on which to operate, for example `//feed`. Read more about it in the official Facebook Developer documentation.
- **Edge**: Edge of the node on which to operate. Edges represent collections of objects which are attached to the node.
- **Ignore SSL Issues**: Toggle to still download the response even if SSL certificate validation isn't possible.
- **Send Binary File**: Available for `POST` operations. If enabled binary data is sent as the body. Requires setting the following:
- **Input Binary Field**: Name of the binary property which contains the data for the file to be uploaded.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

