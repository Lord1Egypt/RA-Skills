# Hosting n8n on Amazon Web Services

## 何时读取

当用户的问题涉及 n8n 文档 `hosting/installation/server-setups/aws.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- This hosting guide shows you how to self-host n8n with Amazon Web Services (AWS). It uses n8n with Postgres as a database backend using Kubernetes to manage the necessary resources and reverse proxy. AWS offers several ways suitable for hosting n8n, including EC2 (virtual machines), and EKS (containers running with Kubernetes).

## 快速定位

- Hosting options
- Prerequisites
- Create a cluster
- Clone configuration repository
- Configure Postgres
- Configure volume for persistent storage
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
- Next steps

