# Information Extractor node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Information Extractor node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.information-extractor`
- node group: `cluster-root-nodes`

## 核心要点

- Learn how to use the Information Extractor node in n8n. Follow technical documentation to integrate Information Extractor node into your workflows.

## 关键操作 / 参数线索

- **Text** defines the input text to extract information from. This is usually an expression that references a field from the input items. For example, this could be `}` if the input is a chat trigger, or `}` if a previous node is Extract from PDF.
- Use **Schema Type** to choose how you want to describe the desired output data format. You can choose between:
- **From Attribute Descriptions**: This option allows you to define the schema by specifying the list of attributes and their descriptions.
- **Generate From JSON Example**: Input an example JSON object to automatically generate the schema. The node uses the object property types and names. It ignores the actual values. n8n treats every field as mandatory when generating schemas from JSON examples.
- **Define using JSON Schema**: Manually input the JSON schema. Read the JSON Schema guides and examples for help creating a valid JSON schema.

## 常用选项线索

- **System Prompt Template**: Use this option to change the system prompt that's used for the information extraction. n8n automatically appends format specification instructions to the prompt.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

