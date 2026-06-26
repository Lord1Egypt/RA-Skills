---
name: github-hosts-cn
description: GitHub Hosts 更新工具（中国用户专用）。安全地更新系统hosts文件以访问GitHub，保留原有非GitHub条目，仅替换GitHub相关地址。支持备份恢复、风险提示。当用户需要解决GitHub访问问题时使用此技能。
risk_level: high
risk_description: |
  ⚠️ 此工具需要修改系统hosts文件(/etc/hosts)，存在以下风险：
  1. 需要sudo权限执行
  2. 可能影响网络访问
  3. 错误的hosts配置可能导致网络问题
  4. 需要用户确认后才能执行
safety_features:
  - 自动备份原有hosts文件
  - 保留所有非GitHub相关条目
  - 仅替换GitHub相关域名
  - 支持一键恢复备份
  - 详细的操作日志
---

# GitHub Hosts CN - 中国用户专用 GitHub Hosts 更新工具

安全、智能地更新系统hosts文件，帮助中国用户正常访问GitHub。

## 🌟 特性

- **🛡️ 安全优先**：自动备份、保留原有配置、仅替换GitHub条目
- **🌍 多源获取**：从多个镜像源获取最新GitHub hosts（HelloGitHub、GitLab、Gitee等）
- **⚡ 自动选择**：并行测试所有源，使用最快的可用源
- **💾 智能备份**：时间戳备份，支持一键恢复
- **🔍 精确替换**：只替换GitHub相关域名，保留其他所有hosts配置
- **📋 风险提示**：执行前显示详细风险说明，需用户确认

## 📦 安装

```bash
cd /Users/claw/Documents/trae_projects/skills/github-hosts-cn
npm install
```

## 🚀 使用方法

```bash
# 更新GitHub hosts
node update.js

# 查看帮助
node update.js --help

# 恢复最近的备份
node update.js --restore

# 查看当前状态
node update.js --status

# 仅获取不更新（预览模式）
node update.js --preview
```

## 📊 数据源

| 源 | URL | 类型 | 优先级 |
|----|-----|------|--------|
| HelloGitHub | raw.hellogithub.com | 独立站点 | 1 |
| GitLab Mirror | gitlab.com/ineo6 | GitLab | 2 |
| Gitee Mirror | gitee.com | 国内镜像 | 3 |
| JSDelivr CDN | cdn.jsdelivr.net | CDN | 4 |

## 🔧 工作流程

```
1. 显示风险提示 → 用户确认
2. 读取当前 /etc/hosts
3. 创建时间戳备份
4. 从多源获取最新GitHub hosts
5. 合并：保留非GitHub条目 + 新GitHub条目
6. 写入新的hosts文件
7. 刷新DNS缓存
8. 显示更新结果
```

## 🛡️ 安全机制

### 备份策略
- 每次修改前自动备份
- 备份文件命名：`hosts.backup.YYYY-MM-DDTHH-mm-ss`
- 备份位置：`~/.openclaw/backups/github-hosts/`
- 保留最近10个备份文件

### 合并策略
- 识别所有GitHub相关域名（github.com, github.global.ssl.fastly.net等）
- 保留hosts文件中的所有非GitHub条目
- 仅替换GitHub相关IP地址

### 恢复机制
- `--restore` 恢复最近备份
- `--restore <backup-file>` 恢复指定备份

## ⚠️ 风险说明

**修改hosts文件存在以下风险：**

1. **权限风险**：需要sudo权限，请确保在可信环境执行
2. **网络风险**：错误的hosts可能导致无法访问某些网站
3. **IP失效风险**：GitHub IP可能随时变化，需要定期更新
4. **备份风险**：请确保备份目录可写

**建议：**
- 在执行前理解hosts文件的作用
- 定期检查备份文件
- 如遇问题立即使用 `--restore` 恢复

## 📋 系统要求

- Node.js 16+
- macOS / Linux
- sudo权限（用于修改/etc/hosts）
- 网络连接

## 📜 License

MIT