# Execute Sub-workflow

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Execute Sub-workflow` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.executeworkflow`
- node group: `core-nodes`

## 核心要点

- Documentation for the Execute Sub-workflow node in n8n, a workflow automation platform. Includes guidance on usage, and links to examples.

## 关键操作 / 参数线索

- **Database**: Select this option to load the workflow from the database by ID. You must also enter either:
- **From list**: Select the workflow from a list of workflows available to your account.
- **Workflow ID**: Enter the ID for the workflow. The URL of the workflow contains the ID after `/workflow/`. For example, if the URL of a workflow is `https://my-n8n-acct.app.n8n.cloud/workflow/abCDE1f6gHiJKL7`, the **Workflow ID** is `abCDE1f6gHiJKL7`.
- **Local File**: Select this option to load the workflow from a locally saved JSON file. You must also enter:
- **Workflow Path**: Enter the path to the local JSON workflow file you want the node to execute.
- **Parameter**: Select this option to load the workflow from a parameter. You must also enter:
- **Workflow JSON**: Enter the JSON code you want the node to execute.
- **URL**: Select this option to load the workflow from a URL. You must also enter:
- **Workflow URL**: Enter the URL you want to load the workflow from.
- **Run once with all items**: Pass all input items into a single execution of the node.
- **Run once for each item**: Execute the node once for each input item in turn.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

