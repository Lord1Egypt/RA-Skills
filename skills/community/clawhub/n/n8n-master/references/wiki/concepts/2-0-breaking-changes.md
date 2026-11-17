# n8n v2.0 breaking changes

## 何时读取

当用户的问题涉及 n8n 文档 `2-0-breaking-changes.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- Breaking changes coming in version 2.0

## 快速定位

- Behavior changes
- Return expected sub-workflow data when the sub-workflow resumes from waiting (waiting for webhook, forms, HITL, etc.)
- Start node removed
- Saving and publishing workflows
- Removed nodes for retired services
- Security
- Block environment variable access from Code Node by default
- Enforce settings file permissions
- Enable task runners by default
- Remove task runner from `n8nio/n8n` docker image
- Remove Pyodide-based Python Code node and tool
- Disable ExecuteCommand and LocalFileTrigger nodes by default
- Require authentication on OAuth callback URLs by default
- Set default value for N8N_RESTRICT_FILE_ACCESS_TO
- Change the default value of N8N_GIT_NODE_DISABLE_BARE_REPOS to true
- Data
- Drop MySQL/MariaDB support
- Remove SQLite legacy driver

