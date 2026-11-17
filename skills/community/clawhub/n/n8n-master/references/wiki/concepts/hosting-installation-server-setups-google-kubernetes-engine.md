# Hosting n8n on Google Kubernetes Engine

## 何时读取

当用户的问题涉及 n8n 文档 `hosting/installation/server-setups/google-kubernetes-engine.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- Google Cloud offers several options suitable for hosting n8n, including Cloud Run (optimized for running containers), Compute Engine (VMs), and Kubernetes Engine (containers running with Kubernetes). This guide uses the Google Kubernetes Engine (GKE) as the hosting option. If you want to use Cloud Run, refer to these instructions.

## 快速定位

- Prerequisites
- Create project
- Enable the Kubernetes Engine API
- Create a cluster
- Set Kubectl context
- Clone configuration repository
- Configure Postgres
- Create a volume for persistent storage
- Postgres environment variables
- Configure n8n
- Create a volume for file storage
- Pod resources
- Optional: Environment variables
- Deployments
- Services
- Send to Kubernetes cluster
- Set up DNS
- Delete resources

