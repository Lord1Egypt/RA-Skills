# OBS Skill - Open Build Service 专家技能

## 技能描述 | Skill Description

**名称 | Name:** obs  
**版本 | Version:** 1.0.0  
**作者 | Author:** OBS Agent  
**领域 | Domain:** Open Build Service (OBS) 包管理和分发  

这是一个全面的 OBS (Open Build Service) 管理技能，提供完整的 API 封装，支持项目、包、仓库、构建、提交请求等所有核心功能。

This is a comprehensive OBS (Open Build Service) management skill with full API coverage, supporting projects, packages, repositories, builds, submit requests, and all core functionalities.

---

## 功能列表 | Features

### 1. 项目管理 | Project Management
- 创建/删除项目 | Create/Delete projects
- 获取项目元数据 | Get project metadata
- 更新项目配置 | Update project configuration
- 列出项目下的包 | List packages in project
- 设置项目访问控制 | Set project access control

### 2. 包管理 | Package Management
- 创建/删除包 | Create/Delete packages
- 获取包信息 | Get package information
- 上传包文件 (spec, tarball 等) | Upload package files (spec, tarball, etc.)
- 下载包源码 | Download package sources
- 查看包历史 | View package history
- 锁定/解锁包 | Lock/Unlock packages

### 3. 仓库管理 | Repository Management
- 添加/删除仓库 | Add/Remove repositories
- 配置仓库路径 | Configure repository paths
- 设置仓库架构 | Set repository architectures
- 管理仓库依赖 | Manage repository dependencies

### 4. 构建管理 | Build Management
- 触发重建 | Trigger rebuild
- 查看构建状态 | View build status
- 获取构建日志 | Get build logs
- 停止构建 | Stop builds
- 查看构建结果 | View build results

### 5. 提交请求 | Submit Requests
- 创建提交请求 | Create submit requests
- 查看提交请求状态 | View submit request status
- 接受/拒绝提交请求 | Accept/Reject submit requests
- 撤销提交请求 | Revoke submit requests
- 列出待处理请求 | List pending requests

### 6. 文件操作 | File Operations
- 读取文件内容 | Read file content
- 上传/更新文件 | Upload/Update files
- 删除文件 | Delete files
- 列出目录内容 | List directory contents
- 文件版本历史 | File version history

### 7. 用户和组 | Users and Groups
- 获取用户信息 | Get user information
- 获取组信息 | Get group information
- 管理项目权限 | Manage project permissions
- 添加/移除维护者 | Add/Remove maintainers

### 8. 搜索和发现 | Search and Discovery
- 搜索项目 | Search projects
- 搜索包 | Search packages
- 查看依赖关系 | View dependencies
- 查看反向依赖 | View reverse dependencies

---

## 配置 | Configuration

### 环境变量 | Environment Variables

```bash
# OBS API 地址 | OBS API URL
OBS_APIURL=https://api.opensuse.org

# 用户名 | Username
OBS_USERNAME=your_username

# API Token (在 OBS Web UI: Profile -> Settings -> API Tokens 创建)
# API Token (create via OBS Web UI: Profile -> Settings -> API Tokens)
OBS_TOKEN=your_api_token
```

### osc 配置文件 | osc Config File

或者使用 osc 配置文件 `~/.config/osc/oscrc`:

Or use osc config file `~/.config/osc/oscrc`:

```ini
[general]
apiurl = https://api.opensuse.org

[https://api.opensuse.org]
user = your_username
pass = your_token
```

---

## 使用示例 | Usage Examples

### 项目操作 | Project Operations

#### 创建项目 | Create Project

```bash
# 创建新项目
# Create a new project

obs project create \
  --name "home:username:myproject" \
  --title "My Project" \
  --description "Project description here"
```

#### 获取项目信息 | Get Project Info

```bash
# 获取项目元数据
# Get project metadata

obs project get --name "home:username:myproject"
```

#### 列出项目下的包 | List Packages in Project

```bash
# 列出所有包
# List all packages

obs package list --project "home:username:myproject"
```

### 包操作 | Package Operations

#### 创建包 | Create Package

```bash
# 创建新包
# Create a new package

obs package create \
  --project "home:username:myproject" \
  --name "mypackage"
```

#### 上传包文件 | Upload Package Files

```bash
# 上传 spec 文件和源码
# Upload spec file and sources

obs file upload \
  --project "home:username:myproject" \
  --package "mypackage" \
  --file "./mypackage.spec" \
  --file "./mypackage-1.0.tar.gz"
```

#### 下载包源码 | Download Package Sources

```bash
# 下载包源码到本地
# Download package sources to local

obs package checkout \
  --project "home:username:myproject" \
  --package "mypackage" \
  --output "./mypackage"
```

### 构建操作 | Build Operations

#### 触发重建 | Trigger Rebuild

```bash
# 重建包
# Rebuild package

obs build rebuild \
  --project "home:username:myproject" \
  --package "mypackage" \
  --repository "openSUSE_Tumbleweed" \
  --arch "x86_64"
```

#### 查看构建状态 | View Build Status

```bash
# 查看构建结果
# View build results

obs build status \
  --project "home:username:myproject" \
  --package "mypackage"
```

#### 获取构建日志 | Get Build Logs

```bash
# 获取构建日志
# Get build logs

obs build log \
  --project "home:username:myproject" \
  --package "mypackage" \
  --repository "openSUSE_Tumbleweed" \
  --arch "x86_64"
```

### 提交请求 | Submit Requests

#### 创建提交请求 | Create Submit Request

```bash
# 创建提交请求到 Factory
# Create submit request to Factory

obs request create \
  --source-project "home:username:myproject" \
  --source-package "mypackage" \
  --target-project "openSUSE:Factory" \
  --target-package "mypackage" \
  --description "Update to version 1.0"
```

#### 查看提交请求 | View Submit Request

```bash
# 查看请求状态
# View request status

obs request get --id 123456
```

#### 接受/拒绝请求 | Accept/Reject Request

```bash
# 接受请求
# Accept request

obs request accept --id 123456

# 拒绝请求
# Reject request

obs request reject --id 123456
```

### 文件操作 | File Operations

#### 读取文件 | Read File

```bash
# 读取 spec 文件内容
# Read spec file content

obs file get \
  --project "home:username:myproject" \
  --package "mypackage" \
  --file "mypackage.spec"
```

#### 更新文件 | Update File

```bash
# 更新文件内容
# Update file content

obs file update \
  --project "home:username:myproject" \
  --package "mypackage" \
  --file "mypackage.spec" \
  --content "./updated.spec" \
  --message "Update spec file"
```

#### 列出文件 | List Files

```bash
# 列出包中的所有文件
# List all files in package

obs file list \
  --project "home:username:myproject" \
  --package "mypackage"
```

### 搜索 | Search

#### 搜索项目 | Search Projects

```bash
# 搜索项目
# Search projects

obs search projects --query "myproject"
```

#### 搜索包 | Search Packages

```bash
# 搜索包
# Search packages

obs search packages --query "mypackage"
```

---

## API 参考 | API Reference

### 基础命令 | Base Commands

```bash
# 查看所有可用命令
# View all available commands

obs --help

# 查看特定命令的帮助
# View help for specific command

obs <command> --help
```

### 命令结构 | Command Structure

```bash
obs <resource> <action> [options]

# 资源类型 | Resource types:
# - project (项目)
# - package (包)
# - build (构建)
# - request (请求)
# - file (文件)
# - repository (仓库)
# - search (搜索)
# - user (用户)
# - group (组)

# 操作类型 | Action types:
# - get (获取)
# - list (列表)
# - create (创建)
# - update (更新)
# - delete (删除)
# - rebuild (重建)
# - checkout (检出)
# - commit (提交)
```

---

## 最佳实践 | Best Practices

### 1. 认证安全 | Authentication Security

- 使用 API Token 而非密码 | Use API Token instead of password
- 不要将凭证提交到版本控制 | Do not commit credentials to version control
- 定期轮换 Token | Rotate tokens regularly

### 2. 项目命名 | Project Naming

- 个人项目使用 `home:username:projectname` 格式
- Personal projects use `home:username:projectname` format
- 官方项目遵循 OBS 命名规范
- Official projects follow OBS naming conventions

### 3. 提交请求 | Submit Requests

- 在提交前确保包在本地构建成功
- Ensure package builds locally before submitting
- 提供清晰的更新说明
- Provide clear update descriptions
- 先提交到 Factory，再同步到 Leap
- Submit to Factory first, then sync to Leap

### 4. 错误处理 | Error Handling

- 检查 API 响应状态码 | Check API response status codes
- 记录详细的错误日志 | Log detailed error messages
- 实现重试机制 | Implement retry mechanisms

---

## 故障排除 | Troubleshooting

### 常见问题 | Common Issues

#### 认证失败 | Authentication Failed

```bash
# 检查凭证配置
# Check credential configuration

obs auth test

# 重新配置凭证
# Reconfigure credentials

obs auth configure
```

#### 构建失败 | Build Failed

```bash
# 查看构建日志
# View build logs

obs build log \
  --project "home:username:myproject" \
  --package "mypackage" \
  --repository "openSUSE_Tumbleweed" \
  --arch "x86_64" \
  --last-failed
```

#### 权限错误 | Permission Error

```bash
# 检查项目权限
# Check project permissions

obs project meta \
  --name "home:username:myproject" \
  --show-access
```

---

## 扩展开发 | Extension Development

### 添加新命令 | Add New Commands

在 `scripts/` 目录中创建新的脚本文件：

Create new script files in the `scripts/` directory:

```bash
#!/bin/bash
# scripts/custom-command.sh

source "$(dirname "$0")/obs-lib.sh"

obs_custom_command() {
    local project="$1"
    local package="$2"
    
    # 实现自定义逻辑
    # Implement custom logic
    
    obs_api_call "GET" "/source/$project/$package"
}

obs_custom_command "$@"
```

### 使用 OBS API 库 | Using OBS API Library

```bash
source references/obs-lib.sh

# API 调用示例
# API call examples

obs_api_call "GET" "/source/$project"
obs_api_call "PUT" "/source/$project/$package/$file" --data "@file.txt"
obs_api_call "DELETE" "/source/$project/$package/$file"
```

---

## 参考资料 | References

- [OBS API 文档 | OBS API Docs](https://api.opensuse.org/apidocs/index)
- [OBS 官方文档 | OBS Official Docs](https://openbuildservice.org/help/)
- [osc 命令参考 | osc Command Reference](https://openbuildservice.org/help/manuals/obs-user-guide/cha.obs.osc.html)
- [openSUSE 打包指南 | openSUSE Packaging Guide](https://en.opensuse.org/openSUSE:Packaging_guidelines)

---

## 许可证 | License

MIT License - 与 OpenClaw AgentSkills 规范兼容
MIT License - Compatible with OpenClaw AgentSkills specification

---

## 更新日志 | Changelog

### v1.0.0 (2026-03-22)
- 初始版本，完整的 OBS API 支持
- Initial release with full OBS API coverage
- 支持项目、包、构建、请求、文件操作
- Support for projects, packages, builds, requests, file operations
- 中英文双语文档
- Bilingual documentation (Chinese/English)
