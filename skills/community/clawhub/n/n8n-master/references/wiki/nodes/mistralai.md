# MistralAI node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `MistralAI node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-base.mistralai`
- node group: `app-nodes`

## 核心要点

- Learn how to use the Mistral AI node in n8n. Follow technical documentation to integrate Mistral AI node into your workflows.

## 关键操作 / 参数线索

- **Resource**: The resource that Mistral AI should operate on. The current implementation supports the "Document" resource.
- **Operation**: The operation to perform:
- **Extract Text**: Extracts text from a document or image using optical character recognition (OCR).
- **Model**: The model to use for the given operation. The current version requires the `mistral-ocr-latest` model.
- **Document Type**: The document format to process. Can be "Document" or "Image".
- **Input Type**: How to input the document:
- **Binary Data**: Pass the document to this node as a binary field.
- **URL**: Fetch the document from a given URL.
- **Input Binary Field**: When using the "Binary Data" input type, defines the name of the input binary field containing the file.
- **URL**: When using the "URL" input type, the URL of the document or image to process.

## 常用选项线索

- **Enable Batch Processing**: Whether to process multiple documents in the same API call. This may reduce your costs by bundling requests.
- **Batch Size**: When using "Enable Batch Processing", sets the maximum number of documents to process per batch.
- **Delete Files After Processing**: When using "Enable Batch Processing", whether to delete the files from Mistral Cloud after processing.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

