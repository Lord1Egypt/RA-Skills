# Troubleshooting and errors

## 何时读取

当用户的问题涉及 n8n 文档 `integrations/community-nodes/troubleshooting.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- n8n installs community nodes directly onto the hard disk. The files must be available at startup for n8n to load them. If the packages aren't available at startup, you get an error warning of missing packages. If running n8n using Docker: depending on your Docker setup, you may lose the packages when you recreate your container or upgrade your n8n version. You must either:

## 快速定位

- Error: Missing packages
- Prevent loading community nodes on n8n cloud

