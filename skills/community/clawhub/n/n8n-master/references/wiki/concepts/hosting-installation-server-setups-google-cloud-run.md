# Hosting n8n on Google Cloud Run

## 何时读取

当用户的问题涉及 n8n 文档 `hosting/installation/server-setups/google-cloud-run.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- This hosting guide shows you how to self-host n8n on Google Cloud Run, a serverless container runtime. If you're just getting started with n8n and don't need a production-grade deployment, you can go with the "easy mode" option below for deployment. Otherwise, if you intend to use this n8n deployment at-scale, refer to the "durable mode" instructions further down. You can also enable access via OAuth to Google Workspace, such as Gmail and Drive, to use these services as n8n workflow tools. Instructions for granting n8n access to these services are at the end of this documentation.

## 快速定位

- Before you begin: get a Google Cloud project
- Easy mode
- Durable mode
- Enable APIs and set env vars
- You may need to login first
- Setup your Postgres database
- Store sensitive data in Secret Manager
- Create a service account for Cloud Run
- Deploy the Cloud Run service
- Troubleshooting
- (Optional) Enabling Google Workspace services as n8n tools
- Enable whichever APIs you need
- Note: If you want Sheets/Docs, it's not enough to just enable Drive; these services each have their own API
- e.g. https://n8n-12345678.us-west1.run.app

