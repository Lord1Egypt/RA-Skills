# Koji Expert 技能 - Koji 构建系统专家（完整版）

## 技能描述 | Skill Description

**名称 | Name:** koji  
**版本 | Version:** 2.0.0  
**作者 | Author:** OS Build Agent  
**领域 | Domain:** Koji Build System (Fedora/CentOS/RHEL)

专业级 Koji 构建系统管理技能，提供完整的构建任务、包管理、标签、仓库、用户、归档、构建根等所有核心功能管理能力。

Professional-level Koji Build System management skill with comprehensive API coverage for build tasks, package management, tags, repositories, users, archives, buildroots, and all core functionalities.

---

## ⭐ 核心特性 | Key Features

### 1. 构建管理 | Build Management
- ✅ 创建构建任务 | Create build tasks
- ✅ 查看构建状态 | View build status
- ✅ 取消构建 | Cancel builds
- ✅ 重试失败构建 | Retry failed builds
- ✅ 获取构建日志 | Get build logs
- ✅ 列出构建历史 | List build history
- ✅ 构建标签管理 | Build tag management

### 2. 包管理 | Package Management
- ✅ 列出包 | List packages
- ✅ 获取包信息 | Get package info
- ✅ 包所有权管理 | Package ownership
- ✅ 包列表管理 | Package list management
- ✅ 添加/删除包 | Add/Remove packages

### 3. 标签管理 | Tag Management
- ✅ 创建/删除标签 | Create/Delete tags
- ✅ 标签继承配置 | Tag inheritance
- ✅ 标签包列表 | Tag package list
- ✅ 标签外部仓库 | Tag external repos

### 4. 目标管理 | Target Management
- ✅ 创建构建目标 | Create build targets
- ✅ 目标配置管理 | Target configuration
- ✅ 构建根管理 | Buildroot management

### 5. 用户管理 | User Management
- ✅ 用户信息查询 | User info query
- ✅ 用户权限管理 | User permissions
- ✅ 用户组管理 | User groups
- ✅ KRB5 认证 | Kerberos authentication

### 6. 仓库管理 | Repository Management
- ✅ 仓库列表 | Repository list
- ✅ 外部仓库配置 | External repo config
- ✅ 仓库分发 | Repository distribution

### 7. 任务管理 | Task Management
- ✅ 任务状态查询 | Task status query
- ✅ 任务结果获取 | Task results
- ✅ 任务取消 | Task cancellation
- ✅ 任务重试 | Task retry

### 8. SRPM/RPM 管理 | SRPM/RPM Management
- ✅ SRPM 上传 | SRPM upload
- ✅ RPM 下载 | RPM download
- ✅ 构建根查询 | Buildroot query
- ✅ 归档管理 | Archive management

### 9. 构建系统集成 | Build System Integration
- ✅ DistGit 集成 | DistGit integration
- ✅ 自动化构建 | Automated building
- ✅ CI/CD 支持 | CI/CD support

---

## 📁 本文档结构 | Document Structure

### 1️⃣ 核心能力 | Core Capabilities
- 构建管理、包管理、标签管理、目标管理
- 用户管理、仓库管理、任务管理
- SRPM/RPM 管理、构建系统集成

### 2️⃣ 基础功能 | Basic Functions
- 构建操作、包管理操作、标签管理操作
- 任务管理操作、用户管理操作

### 3️⃣ 高级功能 | Advanced Functions
- 目标管理、仓库管理、归档管理
- 构建根管理、DistGit 集成

### 4️⃣ 配置与最佳实践 | Configuration & Best Practices
- Koji 配置、环境变量、认证方式
- 最佳实践、故障排除

---

## 🔧 基础功能 | Basic Functions

### 1️⃣ 构建管理 | Build Management

#### 构建操作 | Build Operations

```bash
# 从 SRPM 构建
# Build from SRPM
koji build --target "f39" "./package-1.0-1.fc39.src.rpm"

# 从 Git 构建 (DistGit)
# Build from Git (DistGit)
koji build --target "f39" --git "https://src.fedoraproject.org/rpms/package.git"

# 查看构建信息
# View build info
koji build-info 123456

# 查看构建状态
# View build status
koji build-state 123456

# 查看构建日志
# View build logs
koji build-logs 123456

# 查看构建产物
# View build artifacts
koji list-builds --package "mypackage"

# 取消构建
# Cancel build
koji cancel-build 123456

# 重试构建
# Retry build
koji retry-build 123456

# 取消所有待处理构建
# Cancel all pending builds
koji cancel-all --user "username"
```

#### 批量构建操作 | Batch Build Operations

```bash
# 列出用户构建
# List user builds
koji list-builds --user "username"

# 列出构建历史
# List build history
koji list-builds --package "mypackage" --quiet

# 查看构建任务
# View build tasks
koji list-task --owner "username" --state "open"
```

### 2️⃣ 包管理 | Package Management

#### 包操作 | Package Operations

```bash
# 搜索包
# Search packages
koji list-packages --query "mypackage"

# 获取包信息
# Get package info
koji package-info "mypackage"

# 列出包维护者
# List package owners
koji list-owners "mypackage"

# 添加包维护者
# Add package owner
koji add-owner "mypackage" "username"

# 删除包维护者
# Remove package owner
koji remove-owner "mypackage" "username"

# 列出所有包
# List all packages
koji list-packages

# 列出包组
# List package groups
koji list-groups --tag "f39"
```

### 3️⃣ 标签管理 | Tag Management

#### 标签操作 | Tag Operations

```bash
# 列出所有标签
# List all tags
koji list-tags

# 获取标签信息
# Get tag info
koji tag-info "f39-updates"

# 创建标签
# Create tag
koji create-tag --name "f39-custom" --parent "f39"

# 删除标签
# Delete tag
koji delete-tag "f39-custom"

# 复制标签
# Clone tag
koji clone-tag --name "f39-custom" --clone "f39-updates"

# 列出标签继承关系
# List tag inheritance
koji list-tag-inheritance "f39-custom"
```

#### 标签包管理 | Tag Package Management

```bash
# 列出标签下的包
# List packages in tag
koji list-tag-packages "f39-updates"

# 添加包到标签
# Add package to tag
koji add-to-tag "f39-updates" "mypackage-1.0-1"

# 从标签删除包
# Remove package from tag
koji remove-from-tag "f39-updates" "mypackage-1.0-1"

# 设置包的标签权限
# Set package tag permissions
koji set-pkg-perm "f39-updates" --perms "read/write" "mypackage"

# 列出标签的外部仓库
# List tag external repos
koji list-tag-ext-repos "f39-updates"

# 添加外部仓库到标签
# Add external repo to tag
koji add-ext-repo "f39-updates" --url "https://example.com/repo" --priority 1
```

### 4️⃣ 任务管理 | Task Management

#### 任务操作 | Task Operations

```bash
# 查看任务状态
# View task status
koji task-info 789012

# 查看任务结果
# View task results
koji task-results 789012

# 取消任务
# Cancel task
koji cancel-task 789012

# 查看任务日志
# View task logs
koji task-logs 789012

# 重试任务
# Retry task
koji retry-task 789012

# 列出任务
# List tasks
koji list-tasks --user "username" --state "open"
```

### 5️⃣ 用户管理 | User Management

#### 用户操作 | User Operations

```bash
# 查看用户信息
# View user info
koji user-info "username"

# 查看用户权限
# View user permissions
koji user-permissions "username"

# 列出用户构建
# List user builds
koji list-builds --user "username"

# 创建用户
# Create user
koji create-user --name "username" --email "user@example.com"

# 删除用户
# Delete user
koji delete-user "username"

# 设置用户权限
# Set user permissions
koji grant-perm "perm-name" --user "username"

# 撤销用户权限
# Revoke user permissions
koji revoke-perm "perm-name" --user "username"
```

### 6️⃣ SRPM/RPM 管理 | SRPM/RPM Management

#### SRPM 操作 | SRPM Operations

```bash
# 上传 SRPM
# Upload SRPM
koji upload-srpm "./package-1.0-1.fc39.src.rpm"

# 下载 SRPM
# Download SRPM
koji download-srpm "mypackage-1.0-1.fc39.src.rpm"

# 下载构建的 SRPM
# Download build SRPM
koji download-build 123456 --srpm
```

#### RPM 操作 | RPM Operations

```bash
# 下载 RPM
# Download RPM
koji download-rpm "mypackage-1.0-1.fc39.x86_64.rpm"

# 下载构建产物
# Download build artifacts
koji download-build 123456 --arch "x86_64"

# 列出构建的 RPM
# List build RPMs
koji list-rpms --build-id 123456
```

---

## 🚀 高级功能 | Advanced Functions

### 1️⃣ 目标管理 | Target Management

#### 目标操作 | Target Operations

```bash
# 列出所有目标
# List all targets
koji list-targets

# 获取目标信息
# Get target info
koji target-info "f39-build"

# 创建构建目标
# Create build target
koji create-target --name "f39-custom" --build "f39-build" --destination "f39"

# 删除目标
# Delete target
koji delete-target "f39-custom"

# 复制目标
# Clone target
koji clone-target --name "f39-custom" --clone "f39-build"

# 设置目标的构建根
# Set target buildroot
koji set-buildquota "f39-custom" --quota 100
```

#### 构建根管理 | Buildroot Management

```bash
# 列出构建根
# List buildroots
koji list-buildroots --target "f39-build"

# 获取构建根信息
# Get buildroot info
koji buildroot-info 123456

# 列出构建根内容
# List buildroot contents
koji buildroot-list 123456

# 清理构建根
# Clean buildroot
koji clean-buildroot --id 123456
```

### 2️⃣ 仓库管理 | Repository Management

#### 仓库操作 | Repository Operations

```bash
# 列出所有仓库
# List all repos
koji list-repos

# 获取仓库信息
# Get repo info
koji repo-info "f39"

# 创建仓库
# Create repo
koji create-repo --name "f39-custom" --tag "f39-custom"

# 删除仓库
# Delete repo
koji delete-repo "f39-custom"

# 刷新仓库
# Refresh repo
koji refresh-repo "f39"
```

#### 外部仓库配置 | External Repo Configuration

```bash
# 列出标签的外部仓库
# List tag external repos
koji list-tag-ext-repos "f39-updates"

# 添加外部仓库到标签
# Add external repo to tag
koji add-ext-repo "f39-updates" --url "https://example.com/repo" --priority 1

# 删除外部仓库
# Delete external repo
koji remove-ext-repo "f39-updates" --repo-id 1
```

### 3️⃣ 归档管理 | Archive Management

#### 归档操作 | Archive Operations

```bash
# 列出归档
# List archives
koji list-archives --build-id 123456

# 获取归档信息
# Get archive info
koji archive-info 123456

# 下载归档
# Download archive
koji download-archive 123456

# 删除归档
# Delete archive
koji delete-archive 123456
```

#### 归档类型 | Archive Types

```bash
# 列出归档类型
# List archive types
koji list-archive-types

# 搜索归档
# Search archives
koji search-archives --type "tar" --name "mypackage"
```

### 4️⃣ DistGit 集成 | DistGit Integration

#### DistGit 构建 | DistGit Build

```bash
# 从 DistGit 构建
# Build from DistGit
koji build --target "f39" --git "https://src.fedoraproject.org/rpms/package.git"

# 从 DistGit 特定分支构建
# Build from DistGit specific branch
koji build --target "f39" --git "https://src.fedoraproject.org/rpms/package.git" --branch "main"

# 从 DistGit 特定提交构建
# Build from DistGit specific commit
koji build --target "f39" --git "https://src.fedoraproject.org/rpms/package.git" --revision "abc123"

# 创建 DistGit 仓库
# Create DistGit repo
koji clone-repo --name "mypackage" --source "source-package"
```

---

## ⚙️ 配置 | Configuration

### Koji 配置文件 | Koji Config File

**位置 | Location:** `~/.koji/config`

```ini
[koji]
server = https://koji.fedoraproject.org/kojihub
weburl = https://koji.fedoraproject.org/koji
topdir = ~/koji

# 认证方式 | Authentication Methods

# 方法 1: Kerberos
auth_method = kerberos

# 方法 2: SSL 证书
# auth_method = ssl
# ssl_ca_cert = /etc/koji/koji_ca.crt
# ssl_cert = ~/.koji/client.crt
# ssl_key = ~/.koji/client.key

# 方法 3: GSSAPI
# auth_method = gssapi

# 其他配置 | Other config
ca_cert = /etc/koji/koji_ca.crt
client_cert = ~/.koji/client.crt
server_cert = ~/.koji/server.crt
cert_cn = Koji Client
krb_principal = username@FEDORAPROJECT.ORG
krb_keytab = /etc/krb5.keytab
```

### 环境变量 | Environment Variables

```bash
# Koji 配置文件路径
export KOJI_CONF=~/.koji/config

# Koji 目录
export KOJI_DIR=~/koji

# 调试模式
export KOJI_DEBUG=1

# 禁用 SSL 验证（不推荐）
export KOJI_SSL_VERIFY=0
```

---

## 🔐 认证 | Authentication

### Kerberos 认证 | Kerberos Authentication

```bash
# 检查 KRB5 票据
# Check KRB5 ticket
klist

# 刷新票据
# Refresh ticket
kinit username@FEDORAPROJECT.ORG

# 查看配置
# Check config
koji config show
```

### SSL 证书认证 | SSL Certificate Authentication

```bash
# 生成证书 | Generate certificate
koji create-cert --cn "username" --email "user@example.com"

# 导出证书 | Export certificate
koji export-cert --cn "username" --output "~/.koji/client.crt"

# 配置文件配置 | Config file setup
[koji]
auth_method = ssl
ssl_cert = ~/.koji/client.crt
ssl_key = ~/.koji/client.key
ssl_ca_cert = /etc/koji/koji_ca.crt
```

---

## 📊 命令参考 | Command Reference

### 构建命令 | Build Commands

| 命令 | 描述 | Description |
|------|------|-------------|
| `build` | 创建构建 | Create build |
| `build-info` | 构建信息 | Build info |
| `build-state` | 构建状态 | Build state |
| `build-logs` | 构建日志 | Build logs |
| `cancel-build` | 取消构建 | Cancel build |
| `retry-build` | 重试构建 | Retry build |
| `cancel-all` | 取消所有构建 | Cancel all builds |

### 包命令 | Package Commands

| 命令 | 描述 | Description |
|------|------|-------------|
| `list-packages` | 列出包 | List packages |
| `package-info` | 包信息 | Package info |
| `list-owners` | 列出维护者 | List owners |
| `add-owner` | 添加维护者 | Add owner |
| `remove-owner` | 删除维护者 | Remove owner |

### 标签命令 | Tag Commands

| 命令 | 描述 | Description |
|------|------|-------------|
| `list-tags` | 列出标签 | List tags |
| `tag-info` | 标签信息 | Tag info |
| `create-tag` | 创建标签 | Create tag |
| `delete-tag` | 删除标签 | Delete tag |
| `clone-tag` | 复制标签 | Clone tag |
| `list-tag-packages` | 标签包列表 | Tag packages |
| `add-to-tag` | 添加到标签 | Add to tag |
| `remove-from-tag` | 从标签删除 | Remove from tag |
| `list-tag-ext-repos` | 标签外部仓库 | Tag ext repos |

### 任务命令 | Task Commands

| 命令 | 描述 | Description |
|------|------|-------------|
| `task-info` | 任务信息 | Task info |
| `task-results` | 任务结果 | Task results |
| `cancel-task` | 取消任务 | Cancel task |
| `task-logs` | 任务日志 | Task logs |
| `retry-task` | 重试任务 | Retry task |
| `list-tasks` | 列出任务 | List tasks |

### 用户命令 | User Commands

| 命令 | 描述 | Description |
|------|------|-------------|
| `user-info` | 用户信息 | User info |
| `user-permissions` | 用户权限 | User permissions |
| `list-builds` | 用户构建 | User builds |
| `create-user` | 创建用户 | Create user |
| `delete-user` | 删除用户 | Delete user |
| `grant-perm` | 授予权限 | Grant permission |
| `revoke-perm` | 撤销权限 | Revoke permission |

### SRPM/RPM 命令 | SRPM/RPM Commands

| 命令 | 描述 | Description |
|------|------|-------------|
| `upload-srpm` | 上传 SRPM | Upload SRPM |
| `download-srpm` | 下载 SRPM | Download SRPM |
| `download-rpm` | 下载 RPM | Download RPM |
| `download-build` | 下载构建产物 | Download build |
| `list-rpms` | 列出 RPM | List RPMs |

---

## 📚 最佳实践 | Best Practices

### 1. 构建前检查 | Pre-build Checks

- ✅ 确保 spec 文件符合打包规范
- ✅ 在本地 mock 环境中测试构建
- ✅ 检查依赖关系
- ✅ 验证 DistGit 仓库状态
- ✅ 确认目标标签存在

### 2. 标签策略 | Tag Strategy

- ✅ 使用标准标签命名（如 f39, f39-updates）
- ✅ 正确配置标签继承
- ✅ 管理好外部仓库
- ✅ 定期清理 unused tags
- ✅ 使用 clone-tag 进行标签模板

### 3. 错误处理 | Error Handling

- ✅ 检查构建失败原因
- ✅ 查看完整构建日志
- ✅ 在本地重现问题
- ✅ 使用 retry-build 重试临时失败
- ✅ 了解不同构建状态的含义

### 4. 性能优化 | Performance Optimization

- ✅ 批量操作使用脚本
- ✅ 合理使用缓存
- ✅ 避免重复构建
- ✅ 使用 --quiet 选项减少输出
- ✅ 并行执行独立构建

### 5. 安全性 | Security

- ✅ 使用 SSL 证书认证
- ✅ 定期更新 Kerberos 票据
- ✅ 限制用户权限
- ✅ 使用 HTTPS 连接
- ✅ 定期清理敏感数据

---

## ⚠️ 常见问题 | Common Issues

### 认证失败 | Authentication Failed

```bash
# 检查 KRB5 票据
# Check KRB5 ticket
klist

# 刷新票据
# Refresh ticket
kinit username@FEDORAPROJECT.ORG

# 检查配置文件
# Check config file
koji config show

# 重启 D-Bus
# Restart D-Bus
systemctl --user restart dbus
```

### 构建失败 | Build Failed

```bash
# 查看构建日志
# View build logs
koji build-logs 123456

# 查看失败原因
# View failure reason
koji build-info 123456

# 重试构建
# Retry build
koji retry-build 123456

# 检查构建任务
# Check build task
koji list-task --build 123456
```

### 连接问题 | Connection Issues

```bash
# 测试服务器连接
# Test server connection
koji server ping

# 检查服务器状态
# Check server status
koji server status

# 检查网络连接
# Check network connection
curl https://koji.fedoraproject.org/kojihub

# 检查防火墙
# Check firewall
firewall-cmd --list-ports
```

### 权限问题 | Permission Issues

```bash
# 检查用户权限
# Check user permissions
koji user-permissions "username"

# 检查包权限
# Check package permissions
koji list-owners "mypackage"

# 检查标签权限
# Check tag permissions
koji list-tag-packages "f39-updates" --perms
```

---

## 🔧 故障排除 | Troubleshooting

### 构建挂起 | Build Hangs

```bash
# 检查构建状态
# Check build status
koji build-state 123456

# 检查任务状态
# Check task status
koji list-task --build 123456

# 检查构建根
# Check buildroot
koji buildroot-info <buildroot_id>

# 查看完整日志
# View complete logs
koji build-logs 123456 --all
```

### 权限拒绝 | Permission Denied

```bash
# 检查用户权限
# Check user permissions
koji user-permissions "username"

# 检查包所有权
# Check package ownership
koji list-owners "mypackage"

# 检查标签权限
# Check tag permissions
koji list-tag-packages "f39-updates" --perms

# 联系管理员
# Contact admin
koji contact-admin
```

### 构建失败 - 依赖问题 | Build Failed - Dependency Issues

```bash
# 检查依赖
# Check dependencies
koji build-logs 123456 | grep "Cannot find"

# 解析依赖
# Resolve dependencies
dnf whatprovides "required-package"

# 添加缺失的依赖
# Add missing dependency
koji add-owner "missing-package" "username"
```

---

## 📖 参考资料 | References

### 官方文档 | Official Documentation

- [Koji 官方文档](https://koji.fedoraproject.org/docs/)
- [Fedora 打包指南](https://docs.fedoraproject.org/en-US/packaging-guidelines/)
- [DistGit 文档](https://src.fedoraproject.org/)
- [Koji API 文档](https://koji.fedoraproject.org/docs/developer/)

### 工具 | Tools

- [koji-tools](https://github.com/koji/koji-tools)
- [koji-hub](https://github.com/koji/koji-hub)
- [koji-web](https://github.com/koji/koji-web)

### 社区 | Community

- [Koji Mailing List](https://lists.fedoraproject.org/admin/lists/koji-users.lists.fedoraproject.org/)
- [Koji IRC Channel](irc://irc.freenode.net:6667/koji)
- [Fedora Build System](https://fedoraproject.org/wiki/Build_System)

---

## 📅 版本历史 | Changelog

### v2.0.0 (2026-04-17) ⭐⭐⭐ 重大更新 | Major Update

- **功能合并：** 整合 koji-expert 的全部高级功能
- **全新结构：** 重新组织文档结构，清晰分类
- **目标管理：** 添加完整的构建目标和构建根管理
- **归档管理：** 添加归档管理功能
- **DistGit 集成：** 添加 DistGit 构建和仓库管理
- **命令参考：** 添加完整的命令参考表格
- **最佳实践：** 添加详细的 Best Practices 章节

### v1.0.0 (2026-03-23)
- 初始版本，完整的 Koji API 支持
- 支持构建、包、标签、任务、用户管理
- 基础的 SRPM/RPM 管理
- 中英文双语文档

---

## 📄 许可证 | License

MIT License - 与 OpenClaw AgentSkills 规范兼容  
MIT License - Compatible with OpenClaw AgentSkills specification
