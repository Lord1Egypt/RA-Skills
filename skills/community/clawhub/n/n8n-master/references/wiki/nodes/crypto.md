# Crypto

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Crypto` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.crypto`
- node group: `core-nodes`

## 核心要点

- Documentation for the Crypto node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Property Name**: Enter the name of the property to write the random string to.
- **Type**: Select the encoding type to use to generate the string. Choose from:
- **ASCII**
- **BASE64**
- **HEX**
- **UUID**
- **Type**: Select the hash type to use. Choose from:
- **MD5**
- **SHA256**
- **SHA3-256**
- **SHA3-384**
- **SHA3-512**
- **SHA385**
- **SHA512**
- **Binary File**: Turn this parameter on if the data you want to hash is from a binary file.
- **Value**: If you turn off **Binary File**, enter the value you want to hash.
- **Binary Property Name**: If you turn on **Binary File**, enter the name of the binary property that contains the data you want to hash.
- **Property Name**: Enter the name of the property you want to write the hash to.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

