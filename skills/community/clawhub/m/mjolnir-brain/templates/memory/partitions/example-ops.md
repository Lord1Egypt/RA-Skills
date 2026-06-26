# 🔧 Ops — 运维类分区示例
<!-- Partition: example-ops -->
<!-- Keywords: 运维, 服务器, 部署, SSH, docker, ops, server, deploy, infrastructure -->
<!-- Max Size: 20KB -->
<!-- Description: 存储运维相关的记忆，包括服务器配置、部署流程、故障排查经验等 -->

> **这是一个示例分区文件。** 实际使用时，替换为你自己的内容。
> This is an example partition file. Replace with your own content when using.

## 🖥️ 服务器清单 / Server Inventory

- （示例）生产服务器：192.168.1.100，Ubuntu 24.04，8GB RAM
- （示例）测试服务器：192.168.1.101，Docker host

## 🚀 部署流程 / Deployment Procedures

- （示例）标准部署：git pull → build → restart service
- （示例）回滚步骤：切换 symlink → restart → verify

## 🔥 故障排查 / Troubleshooting Log

- （示例）2026-01-15：OOM killed — 解法：增加 swap + 限制进程内存
- （示例）2026-02-03：SSH 连接超时 — 原因：防火墙规则变更

## 📋 常用命令 / Frequently Used Commands

```bash
# （示例）查看服务状态
# systemctl status myservice

# （示例）查看日志
# journalctl -u myservice -f --since "1 hour ago"
```

---
*Last updated: (auto)*
