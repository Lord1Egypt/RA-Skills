# Error handling in n8n nodes

## 何时读取

当用户的问题涉及 n8n 文档 `integrations/creating-nodes/build/reference/error-handling.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- Proper error handling is crucial for creating robust n8n nodes that provide clear feedback to users when things go wrong. n8n provides two specialized error classes to handle different types of failures in node implementations: Use `NodeApiError` when dealing with external API calls and HTTP requests. This error class is specifically designed to handle API response errors and provides enhanced features for parsing and presenting API-related failures such as:

## 快速定位

- NodeApiError
- Common usage patterns
- NodeOperationError

