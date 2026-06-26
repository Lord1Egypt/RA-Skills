---
name: ipaas-vitepress-automation
title: iPaaS 内容生成与自动化发布工具
description: 自动生成 B 端集成解决方案文档并安全部署至 VitePress 站点。
version: 1.2.0
author: CJCloud
license: MIT
homepage: https://your-company.com
user-invocable: true

metadata:
  runtime: bash
  categories: [productivity, developer-tools]
  openclaw:
    requires:
      tools: [file_read, file_write, shell]
      binaries: [pnpm, rsync, ssh]
    env_vars:
      - SERVER_IP: "目标服务器 IP"
      - REMOTE_DIR: "目标服务器部署绝对路径"
      - REMOTE_USER: "部署用户 (建议非 root)"
      - SERVER_PORT: "SSH 端口 (默认 22)"
---

# 触发场景
- 当用户要求撰写或发布系统集成解决方案（如：金蝶集成天猫）时。

# 自动化流程 (Workflow)
1. **数据提取**：识别两个对接系统名称、接口范围及业务场景。
2. **读取模板**：`file_read: ./template/solution-template.md`
3. **内容创作**：基于模板逻辑生成 Markdown 文本。
4. **本地写入**：`file_write: ./docs/cases/{filename}.md`
5. **配置更新**：`file_write: ./docs/.vitepress/config.mts` (更新导航栏)
6. **安全部署**：调用项目内的 shell 脚本执行发布：
   `shell: bash ./scripts/deploy.sh`

# 安全约束
- **认证**：本工具仅支持 SSH Key 密钥认证，不接受密码输入。
- **环境**：运行环境需预装 pnpm 和 rsync。