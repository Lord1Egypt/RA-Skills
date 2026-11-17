# Text Classifier node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Text Classifier node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.text-classifier`
- node group: `cluster-root-nodes`

## 核心要点

- Learn how to use the Text Classifier node in n8n. Follow technical documentation to integrate Text Classifier node into your workflows.

## 关键操作 / 参数线索

- **Input Prompt** defines the input to classify. This is usually an expression that references a field from the input items. For example, this could be `}` if the input is a chat trigger. By default it references the `text` field.
- **Categories**: Add the categories that you want to classify your input as. Categories have a name and a description. Use the description to tell the model what the category means. This is important if the meaning isn't obvious. You can add as many categories as you like.

## 常用选项线索

- **Allow Multiple Classes To Be True**: You can configure the classifier to always output a single class per item (turned off), or allow the model to select multiple classes (turned on).
- **When No Clear Match**: Define what happens if the model can't find a good match for an item. There are two options:
- **Discard Item** (the default): If the node doesn't detect any of the categories, it drops the item.
- **Output on Extra, 'Other' Branch**: Creates a separate output branch called **Other**. When the node doesn't detect any of the categories, it outputs items in this branch.
- **System Prompt Template**: Use this option to change the system prompt that's used for the classification. It uses the `` placeholder for the categories.
- **Enable Auto-Fixing**: When enabled, the node automatically fixes model outputs to ensure they match the expected format. Do this by sending the schema parsing error to the LLM and asking it to fix it.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

