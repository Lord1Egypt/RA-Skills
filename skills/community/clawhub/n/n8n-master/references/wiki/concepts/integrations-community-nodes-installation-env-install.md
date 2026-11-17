# Manage community packages from environment variables

## 何时读取

当用户的问题涉及 n8n 文档 `integrations/community-nodes/installation/env-install.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- On self-hosted n8n, you can manage the set of installed community packages from environment variables. n8n reconciles the installed packages against the list on every startup, installing missing packages, correcting versions, and uninstalling packages not in the list. Use this method to bootstrap an instance with a fixed set of packages, for example through a deployment pipeline. Set the following environment variables on your n8n instance, then restart:

## 快速定位

- Configure
- Per-package fields
- Manage packages

