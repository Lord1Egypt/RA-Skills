# Default Data Loader node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Default Data Loader node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.documentdefaultdataloader`
- node group: `cluster-sub-nodes`

## 核心要点

- Learn how to use the Default Data Loader node in n8n. Follow technical documentation to integrate Default Data Loader node into your workflows.

## 关键操作 / 参数线索

- **Text Splitting**: Choose from:
- **Simple**: Uses the Recursive Character Text Splitter with a chunk size of 1000 and an overlap of 200.
- **Custom**: Allows you to connect a text splitter of your choice.
- **Type of Data**: Select **Binary** or **JSON**.
- **Mode**: Choose from:
- **Load All Input Data**: Use all the node's input data.
- **Load Specific Data**: Use expressions to define the data you want to load. You can add text as well as expressions. This means you can create a custom document from a mix of text and expressions.
- **Data Format**: Displays when you set **Type of Data** to **Binary**. Select the file MIME type for your binary data. Set to **Automatically Detect by MIME Type** if you want n8n to set the data format for you. If you set a specific data format and the incoming file MIME type doesn't match it, the node errors. If you use **Automatically Detect by MIME Type**, the node falls back to text format if it can't match the file MIME type to a supported data format.

## 常用选项线索

- **Metadata**: Set the metadata that should accompany the document in the vector store. This is what you match to using the **Metadata Filter** option when retrieving data using the vector store nodes.

## n8n 使用建议

- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

