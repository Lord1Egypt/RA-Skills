# OBS Skill

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://clawhub.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![OBS](https://img.shields.io/badge/OBS-API-lightgrey.svg)](https://api.opensuse.org)

## 📦 简介 | Introduction

OBS 是一个全面的 Open Build Service (OBS) 管理技能，提供完整的 API 封装，支持项目、包、仓库、构建、提交请求等所有核心功能。

OBS is a comprehensive Open Build Service (OBS) management skill with full API coverage, supporting projects, packages, repositories, builds, submit requests, and all core functionalities.

### ✨ 特性 | Features

- 🌐 **完整 API 支持** - 覆盖 OBS 所有核心接口
- 🌐 **Full API Coverage** - All core OBS endpoints supported
- 📝 **中英文文档** - 双语使用指南
- 📝 **Bilingual Docs** - Chinese and English documentation
- 🔧 **命令行工具** - 易用的 CLI 接口
- 🔧 **CLI Tools** - Easy-to-use command line interface
- 🛡️ **安全可靠** - 支持 API Token 认证
- 🛡️ **Secure** - API Token authentication support

---

## 🚀 快速开始 | Quick Start

### 1. 安装技能 | Install Skill

```bash
# 从 ClawHub 安装
# Install from ClawHub

clawhub skill install obs
```

### 2. 配置凭证 | Configure Credentials

```bash
# 方法一：环境变量 | Method 1: Environment Variables
export OBS_APIURL=https://api.opensuse.org
export OBS_USERNAME=your_username
export OBS_TOKEN=your_api_token

# 方法二：osc 配置文件 | Method 2: osc Config File
# 编辑 ~/.config/osc/oscrc
```

### 3. 测试连接 | Test Connection

```bash
# 测试认证
# Test authentication

obs auth test
```

---

## 📖 使用指南 | Usage Guide

### 项目管理 | Project Management

```bash
# 创建项目 | Create Project
obs project create \
  --name "home:username:myproject" \
  --title "My Project" \
  --description "Project description"

# 获取项目信息 | Get Project Info
obs project get --name "home:username:myproject"

# 列出项目下的包 | List Packages
obs project list --name "home:username:myproject"
```

### 包管理 | Package Management

```bash
# 创建包 | Create Package
obs package create \
  --project "home:username:myproject" \
  --package "mypackage"

# 下载包源码 | Checkout Package Sources
obs package checkout \
  --project "home:username:myproject" \
  --package "mypackage" \
  --output "./mypackage"

# 列出包文件 | List Package Files
obs package list \
  --project "home:username:myproject" \
  --package "mypackage"
```

### 文件操作 | File Operations

```bash
# 上传文件 | Upload File
obs file upload \
  --project "home:username:myproject" \
  --package "mypackage" \
  --file "./mypackage.spec" \
  --message "Initial commit"

# 读取文件 | Read File
obs file get \
  --project "home:username:myproject" \
  --package "mypackage" \
  --file "mypackage.spec"

# 列出文件 | List Files
obs file list \
  --project "home:username:myproject" \
  --package "mypackage"
```

### 构建管理 | Build Management

```bash
# 查看构建状态 | View Build Status
obs build status \
  --project "home:username:myproject" \
  --package "mypackage"

# 触发重建 | Trigger Rebuild
obs build rebuild \
  --project "home:username:myproject" \
  --package "mypackage" \
  --repository "openSUSE_Tumbleweed" \
  --arch "x86_64"

# 获取构建日志 | Get Build Logs
obs build log \
  --project "home:username:myproject" \
  --package "mypackage" \
  --repository "openSUSE_Tumbleweed" \
  --arch "x86_64"
```

### 提交请求 | Submit Requests

```bash
# 创建提交请求 | Create Submit Request
obs request create \
  --source-project "home:username:myproject" \
  --source-package "mypackage" \
  --target-project "openSUSE:Factory" \
  --target-package "mypackage" \
  --description "Update to version 1.0"

# 查看请求详情 | View Request Details
obs request get --id 123456

# 列出待处理请求 | List Pending Requests
obs request list --states "new,review"

# 接受/拒绝请求 | Accept/Reject Request
obs request accept --id 123456 --message "Looks good"
obs request reject --id 123456 --message "Needs work"
```

### 搜索 | Search

```bash
# 搜索项目 | Search Projects
obs search projects --query "myproject"

# 搜索包 | Search Packages
obs search packages \
  --query "mypackage" \
  --project "openSUSE:Factory"
```

---

## 🔧 命令参考 | Command Reference

### 项目命令 | Project Commands

| 命令 | Command | 描述 | Description |
|------|---------|------|-------------|
| `project get` | 获取项目信息 | Get project info |
| `project meta` | 获取项目元数据 | Get project metadata |
| `project create` | 创建项目 | Create project |
| `project delete` | 删除项目 | Delete project |
| `project list` | 列出项目下的包 | List packages in project |

### 包命令 | Package Commands

| 命令 | Command | 描述 | Description |
|------|---------|------|-------------|
| `package get` | 获取包信息 | Get package info |
| `package meta` | 获取包元数据 | Get package metadata |
| `package create` | 创建包 | Create package |
| `package delete` | 删除包 | Delete package |
| `package list` | 列出包文件 | List package files |
| `package checkout` | 下载包源码 | Download package sources |

### 构建命令 | Build Commands

| 命令 | Command | 描述 | Description |
|------|---------|------|-------------|
| `build status` | 查看构建状态 | View build status |
| `build rebuild` | 触发重建 | Trigger rebuild |
| `build log` | 获取构建日志 | Get build logs |
| `build stop` | 停止构建 | Stop build |
| `build results` | 查看构建结果 | View build results |

### 请求命令 | Request Commands

| 命令 | Command | 描述 | Description |
|------|---------|------|-------------|
| `request create` | 创建提交请求 | Create submit request |
| `request get` | 获取请求详情 | Get request details |
| `request list` | 列出请求 | List requests |
| `request accept` | 接受请求 | Accept request |
| `request reject` | 拒绝请求 | Reject request |
| `request revoke` | 撤销请求 | Revoke request |

---

## 🔐 认证 | Authentication

### API Token 获取 | Get API Token

1. 登录 OBS Web UI | Login to OBS Web UI
2. 点击 Profile -> Settings | Click Profile -> Settings
3. 选择 API Tokens 标签 | Select API Tokens tab
4. 创建新 Token | Create new token
5. 保存 Token（只显示一次）| Save token (shown only once)

### 安全最佳实践 | Security Best Practices

- ✅ 使用 API Token 而非密码 | Use API Token instead of password
- ✅ 定期轮换 Token | Rotate tokens regularly
- ✅ 不要将凭证提交到版本控制 | Do not commit credentials to VCS
- ✅ 使用最小权限原则 | Use principle of least privilege

---

## 📚 示例工作流 | Example Workflows

### 工作流 1: 发布新包 | Workflow 1: Publish New Package

```bash
# 1. 创建项目 | Create Project
obs project create \
  --name "home:username:myproject" \
  --title "My Project" \
  --description "My OBS project"

# 2. 创建包 | Create Package
obs package create \
  --project "home:username:myproject" \
  --package "mypackage"

# 3. 上传文件 | Upload Files
obs file upload \
  --project "home:username:myproject" \
  --package "mypackage" \
  --file "./mypackage.spec"

obs file upload \
  --project "home:username:myproject" \
  --package "mypackage" \
  --file "./mypackage-1.0.tar.gz"

# 4. 等待构建完成 | Wait for build
obs build status \
  --project "home:username:myproject" \
  --package "mypackage"

# 5. 创建提交请求到 Factory | Create Submit Request to Factory
obs request create \
  --source-project "home:username:myproject" \
  --source-package "mypackage" \
  --target-project "openSUSE:Factory" \
  --target-package "mypackage" \
  --description "Initial package submission"
```

### 工作流 2: 更新现有包 | Workflow 2: Update Existing Package

```bash
# 1. 下载当前包源码 | Download Current Package Sources
obs package checkout \
  --project "home:username:myproject" \
  --package "mypackage" \
  --output "./mypackage-update"

# 2. 更新 spec 文件和源码 | Update Spec and Sources
# (在本地编辑文件 | Edit files locally)

# 3. 上传更新的文件 | Upload Updated Files
obs file upload \
  --project "home:username:myproject" \
  --package "mypackage" \
  --file "./mypackage.spec" \
  --message "Update to version 1.1"

obs file upload \
  --project "home:username:myproject" \
  --package "mypackage" \
  --file "./mypackage-1.1.tar.gz" \
  --message "Update to version 1.1"

# 4. 触发重建 | Trigger Rebuild
obs build rebuild \
  --project "home:username:myproject" \
  --package "mypackage" \
  --repository "openSUSE_Tumbleweed" \
  --arch "x86_64"

# 5. 查看构建日志 | View Build Logs
obs build log \
  --project "home:username:myproject" \
  --package "mypackage" \
  --repository "openSUSE_Tumbleweed" \
  --arch "x86_64"
```

---

## 🐛 故障排除 | Troubleshooting

### 认证失败 | Authentication Failed

```bash
# 检查凭证配置 | Check Credentials
obs auth status

# 测试连接 | Test Connection
obs auth test
```

### 构建失败 | Build Failed

```bash
# 查看详细构建日志 | View Detailed Build Logs
obs build log \
  --project "home:username:myproject" \
  --package "mypackage" \
  --repository "openSUSE_Tumbleweed" \
  --arch "x86_64" \
  --last-failed
```

### 权限错误 | Permission Error

```bash
# 检查项目元数据 | Check Project Metadata
obs project meta --name "home:username:myproject"
```

---

## 📄 许可证 | License

MIT License - 详见 LICENSE 文件
MIT License - See LICENSE file for details

---

## 🔗 相关链接 | Related Links

- [OBS API 文档 | OBS API Docs](https://api.opensuse.org/apidocs/index)
- [OBS 官方文档 | OBS Official Docs](https://openbuildservice.org/help/)
- [osc 命令参考 | osc Command Reference](https://openbuildservice.org/help/manuals/obs-user-guide/cha.obs.osc.html)
- [openSUSE 打包指南 | openSUSE Packaging Guide](https://en.opensuse.org/openSUSE:Packaging_guidelines)
- [ClawHub | 技能市场 | Skill Marketplace](https://clawhub.com)

---

## 🤝 贡献 | Contributing

欢迎提交 Issue 和 Pull Request！
Issues and Pull Requests are welcome!

1. Fork 本仓库 | Fork this repository
2. 创建功能分支 | Create feature branch
3. 提交更改 | Commit changes
4. 推送到分支 | Push to branch
5. 创建 Pull Request | Create Pull Request

---

**版本 | Version:** 1.0.0  
**作者 | Author:** OBS Agent  
**最后更新 | Last Updated:** 2026-03-22
