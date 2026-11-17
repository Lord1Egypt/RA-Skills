# SSH

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `SSH` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.ssh`
- node group: `core-nodes`

## 核心要点

- Documentation for the SSH node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Execute** a command
- **Download** a file
- **Upload** a file
- **Credential to connect with**: Select an existing or create a new SSH credential to connect with.
- **Command**: Enter the command to execute on the remote device.
- **Working Directory**: Enter the directory where n8n should execute the command.
- **Path**: Enter the path for the file you want to download. This path must include the file name. The downloaded file will use this file name. To use a different name, use the **File Name** option. Refer to Download File options for more information.
- **File Property**: Enter the name of the object property that holds the binary data you want to download.
- **Input Binary Field**: Enter the name of the input binary field that contains the file you want to upload.
- **Target Directory**: The directory to upload the file to. The name of the file is taken from the binary data file name. To enter a different name, use the **File Name** option. Refer to Upload File options for more information.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

