# Compression

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Compression` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.compression`
- node group: `core-nodes`

## 核心要点

- Documentation for the Compression node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Compress**: Create a compressed file from your input data.
- **Decompress**: Decompress an existing compressed file.
- **Input Binary Field(s)**: Enter the name of the fields in the input data that contain the binary files you want to compress. To compress more than one file, use a comma-separated list.
- **Output Format**: Choose whether to format the compressed output as **Zip** or **Gzip**.
- **File Name**: Enter the name of the zip file the node creates.
- **Put Output File in Field**: Enter the name of the field in the output data to contain the file.
- **Put Output File in Field**: Enter the name of the fields in the input data that contain the binary files you want to decompress. To decompress more than one file, use a comma-separated list.
- **Output Prefix**: Enter a prefix to add to the output file name.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

