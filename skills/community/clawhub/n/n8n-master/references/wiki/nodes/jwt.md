# JWT

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `JWT` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.jwt`
- node group: `core-nodes`

## 核心要点

- Documentation for the JWT node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- Decode
- Sign
- Verify

## 常用选项线索

- **Return Additional Info**: This toggle controls how much information the node returns. When turned on, the node returns the complete decoded token with information about the header and signature. When turned off, the node only returns the payload.
- **Ignore Expiration**: This toggle controls whether the node should ignore the token's expiration time claim (`exp`). Refer to "exp" (Expiration Time) Claim for more information.
- **Ignore Not Before Claim**: This toggle controls whether to ignore the token's not before claim (`nbf`). Refer to "nbf" (Not Before) Claim for more information.
- **Clock Tolerance**: Enter the number of seconds to tolerate when checking the `nbf` and `exp` claims. This allows you to deal with small clock differences among different servers. Refer to "exp" (Expiration Time) Claim for more information.
- **Override Algorithm**: The algorithm to use for verifying the token. This algorithm will override the algorithm selected in the credentials.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

