# Credentials file

## 何时读取

当用户的问题涉及 n8n 文档 `integrations/creating-nodes/build/reference/credentials-files.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- The credentials file defines the authorization methods for the node. The settings in this file affect what n8n displays in the **Credentials** modal, and must reflect the authentication requirements of the service you're connecting to. In the credentials file, you can use all the n8n UI elements. n8n encrypts the data that's stored using credentials using an encryption key.

## 快速定位

- Structure of the credentials file
- Outline structure
- Parameters
- `name`
- `displayName`
- `documentationUrl`
- `properties`
- `authenticate`
- `test`

