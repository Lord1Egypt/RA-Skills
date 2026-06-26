# GitHub Hosts CN - 中国用户专用 GitHub Hosts 更新工具

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Node.js](https://img.shields.io/badge/Node.js-%3E%3D16-green.svg)](https://nodejs.org/)

安全、智能地更新系统hosts文件，帮助中国用户正常访问GitHub。

## 🌟 核心特性

### 🛡️ 安全优先
- **自动备份**：每次修改前自动创建时间戳备份
- **保留原配置**：智能识别并保留所有非GitHub相关条目
- **仅替换GitHub**：只修改GitHub相关域名，不影响其他站点
- **一键恢复**：支持快速恢复到任意备份版本

### 🌍 多源获取
- 并行测试多个数据源
- 自动选择最快的可用源
- 支持备用源自动切换

### 📋 风险提示
- 执行前显示详细风险说明
- 需要用户明确确认后才执行
- 提供预览模式，不实际修改文件

## 📦 安装

```bash
cd /Users/claw/Documents/trae_projects/skills/github-hosts-cn
npm install
```

## 🚀 使用方法

### 基本使用

```bash
# 交互式更新（推荐）
node update.js

# 查看帮助
node update.js --help
```

### 高级选项

```bash
# 预览模式 - 查看将要修改的内容，不实际修改
node update.js --preview

# 查看当前状态
node update.js --status

# 恢复最近的备份
node update.js --restore

# 跳过确认（谨慎使用，适合脚本调用）
node update.js --yes
```

## 📊 数据源

| 源 | URL | 类型 | 优先级 | 说明 |
|----|-----|------|--------|------|
| HelloGitHub | raw.hellogithub.com | 独立站点 | 1 | 推荐，稳定快速 |
| GitLab Mirror | gitlab.com/ineo6 | GitLab | 2 | GitLab镜像 |
| Gitee Mirror | gitee.com | 国内镜像 | 3 | 国内加速 |
| JSDelivr CDN | cdn.jsdelivr.net | CDN | 4 | CDN加速 |

## 🔧 工作流程

```
┌─────────────────────────────────────────────────────────────────┐
│                     GitHub Hosts CN 工作流程                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. 显示风险提示 → 用户确认                                       │
│         ↓                                                       │
│  2. 读取当前 /etc/hosts 文件                                     │
│         ↓                                                       │
│  3. 创建时间戳备份                                               │
│         ↓                                                       │
│  4. 并行测试所有数据源，选择最快的                                │
│         ↓                                                       │
│  5. 解析GitHub hosts条目                                        │
│         ↓                                                       │
│  6. 合并：保留非GitHub条目 + 新GitHub条目                        │
│         ↓                                                       │
│  7. 写入新的hosts文件（需要sudo）                                │
│         ↓                                                       │
│  8. 刷新DNS缓存                                                 │
│         ↓                                                       │
│  9. 显示更新结果                                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🛡️ 安全机制详解

### 备份策略
- 每次修改前自动备份
- 备份文件命名：`hosts.backup.YYYY-MM-DDTHH-mm-ss`
- 备份位置：`~/.openclaw/backups/github-hosts/`
- 保留最近10个备份文件（自动清理旧备份）

### 合并策略
工具会智能识别以下GitHub相关域名：
- github.com
- github.global.ssl.fastly.net
- github.githubusercontent.com
- api.github.com
- 以及其他20+个GitHub相关域名

所有非GitHub的hosts条目都会被完整保留。

### 恢复机制
```bash
# 恢复最近的备份
node update.js --restore

# 查看所有备份（在状态命令中）
node update.js --status
```

## ⚠️ 风险说明

**修改hosts文件存在以下风险：**

| 风险类型 | 说明 | 缓解措施 |
|---------|------|---------|
| 权限风险 | 需要sudo权限 | 在可信环境执行 |
| 网络风险 | 可能暂时影响网络访问 | 自动备份，可快速恢复 |
| 配置错误 | 错误的hosts可能导致DNS问题 | 智能合并，仅替换GitHub条目 |
| IP失效 | GitHub IP可能随时变化 | 定期更新，多源获取 |

**建议：**
- ✅ 在执行前理解hosts文件的作用
- ✅ 定期检查备份文件
- ✅ 如遇问题立即使用 `--restore` 恢复
- ✅ 使用 `--preview` 先预览再执行

## 📋 系统要求

- **Node.js**: 16+
- **操作系统**: macOS / Linux
- **权限**: sudo权限（用于修改/etc/hosts）
- **网络**: 需要访问数据源

## 🧪 测试

更新完成后，可以使用以下命令测试：

```bash
# 测试GitHub连接
ping github.com

# 查看DNS解析
nslookup github.com

# 测试克隆
git clone https://github.com/your-repo/test.git
```

## 📝 示例输出

```
🚀 GitHub Hosts CN - 中国用户专用更新工具

╔════════════════════════════════════════════════════════════════════════╗
║                     安全更新 GitHub Hosts                               ║
╠════════════════════════════════════════════════════════════════════════╣
║  ✓ 保留所有非GitHub条目                                                ║
║  ✓ 仅替换GitHub相关地址                                                ║
║  ✓ 自动备份，支持恢复                                                  ║
║  ✓ 多源获取，自动选择最快                                              ║
╚════════════════════════════════════════════════════════════════════════╝

╔════════════════════════════════════════════════════════════════════════╗
║                        ⚠️  风险警告 / RISK WARNING                      ║
╠════════════════════════════════════════════════════════════════════════╣
║  此工具将修改系统hosts文件(/etc/hosts)，存在以下风险：                   ║
║  ...                                                                   ║
╚════════════════════════════════════════════════════════════════════════╝

确认更新GitHub hosts？ [y/N]: y

[2024-01-01T12:00:00.000Z] [INFO] 步骤 1/4: 从多源获取GitHub hosts...
[2024-01-01T12:00:00.100Z] [INFO] 测试源: HelloGitHub (https://raw.hellogithub.com/hosts)
[2024-01-01T12:00:00.500Z] [SUCCESS] ✓ HelloGitHub: 25 条记录, 400ms
[2024-01-01T12:00:00.600Z] [SUCCESS] 找到 3 个可用数据源
...
[2024-01-01T12:00:01.000Z] [SUCCESS] ✅ 更新成功！

🧪 测试命令: ping github.com
🔄 如需恢复: node update.js --restore
```

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📜 License

MIT License - 详见 [LICENSE](LICENSE) 文件

---

**⚠️ 免责声明**：此工具仅供学习和个人使用，使用前请确保理解hosts文件的作用和风险。作者不对因使用此工具造成的任何问题负责。