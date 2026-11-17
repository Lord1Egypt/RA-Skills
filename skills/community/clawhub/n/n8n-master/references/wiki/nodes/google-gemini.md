# Google Gemini node

## 何时读取

当用户要在 n8n 中使用、配置、排查或替代 `Google Gemini node` 时读取。该卡片由官方节点文档编译，完整细节以 source 为准。

## 节点标识

- n8n node id: `n8n-nodes-langchain.googlegemini`
- node group: `app-nodes`

## 核心要点

- Learn how to use the Google Gemini node in n8n. Follow technical documentation to integrate Google Gemini node into your workflows.

## 关键操作 / 参数线索

- Audio:
- Analyze Audio: Take in audio and answer questions about it.
- Transcribe a Recording: Transcribes audio into text.
- Document:
- Analyze Document: Take in documents and answer questions about them.
- File Search:
- Create File Search Store: Create a new File Search store for RAG (Retrieval Augmented Generation)
- Delete File Search Store: Delete File Search Store
- List File Search Stores: List all File Search stores owned by the user
- Upload to File Search Store: Upload a file to a File Search store for RAG (Retrieval Augmented Generation)
- Image:
- Analyze Image: Take in images and answer questions about them.
- Generate an Image: Creates an image from a text prompt.
- Edit Image: Upload one or more images and apply edits based on a prompt
- Media File:
- Upload Media File: Upload a file to the Google Gemini API for later user.
- Text:
- Message a Model: Create a completion with a Google Gemini model.

## n8n 使用建议

- 该节点涉及 credentials 或鉴权配置；生成工作流时使用占位 credential name，不写入真实密钥。
- 需要精确字段、选项枚举、认证方式或错误解释时，回读 source 文件，不凭记忆补全。

