# Hosting n8n on OpenShift Local (CRC)

## 何时读取

当用户的问题涉及 n8n 文档 `hosting/installation/server-setups/openshift-crc.md` 的主题、配置、概念或操作步骤时读取。

## 核心要点

- This guide walks you through deploying n8n on OpenShift Local (CRC), Red Hat's tool for running a local OpenShift cluster. It mirrors AWS/EKS deployment, but runs entirely on your local machine. It's designed for testing n8n in an OpenShift environment locally, without cloud costs. You will need a machine with significant resources available, given how many resources OpenShift itself consumes.

## 快速定位

- OpenShift concepts vs standard Kubernetes
- Prerequisites
- Prepare Ubuntu
- Open a terminal
- Update your system
- Check CPU virtualization support
- Install KVM and libvirt
- Add user to required groups
- Install NetworkManager
- Install tools
- Get a Red Hat account and pull secret
- Install CRC
- Install Helm
- Set environment variables
- Start OpenShift Local
- Run CRC setup
- Configure CRC memory and start the cluster
- Verify DNS resolution

