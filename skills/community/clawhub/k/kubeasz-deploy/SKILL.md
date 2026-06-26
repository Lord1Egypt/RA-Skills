---
name: kubeasz-deploy
description: 为 K8s 初学者提供 Kubernetes 集群部署指导，支持 AllinOne 快速体验和生产环境高可用部署。
version: 1.0.0
metadata:
  openclaw:
    requires:
      bins:
        - ansible
        - ezctl
    emoji: "🚀"
    homepage: https://github.com/easzlab/kubeasz
---

# kubeasz 集群部署助手

## 技能概述

本技能帮助初学者使用 kubeasz 工具部署 Kubernetes 集群，支持两种场景：
- **AllinOne 快速部署**: 单机测试环境，适合学习和体验
- **生产环境部署**: 多节点高可用集群，满足生产需求

## 使用流程

AI 助手将引导你完成以下步骤：
1. 环境准备与检查
2. 选择部署方式
3. 配置集群参数
4. 执行部署命令
5. 验证集群状态

## 关键章节导航

- [前置条件检查](./guides/01-prerequisites.md)
- [AllinOne 快速部署](./guides/02-allinone-quickstart.md)
- [生产环境部署](./guides/03-production-deploy.md)
- [部署后验证](./guides/04-post-deploy.md)
- [常见问题排查](./troubleshooting.md)

## 配置示例参考

- [AllinOne 配置示例](./configs/hosts.allinone.example)
- [多节点配置示例](./configs/hosts.multi-node.example)
- [参数配置示例](./configs/config.yml.example)

## AI 助手能力

当你向 AI 描述部署需求时，AI 会：
- 评估你的环境是否符合要求
- 根据你的场景推荐合适的部署方式
- 生成或调整配置文件
- 执行部署命令并监控进度
- 验证部署结果并提供后续使用建议