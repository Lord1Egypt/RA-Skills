# OSTree Skill - 原子化系统更新

## 技能描述 | Skill Description

**名称 | Name:** ostree  
**版本 | Version:** 1.0.0  
**作者 | Author:** OS Build Agent  
**领域 | Domain:** Atomic System Updates (Fedora/RHEL CoreOS)  

专业的 OSTree 原子化系统更新管理技能，支持不可变基础设施、原子更新、版本回滚等现代系统管理功能。

Professional OSTree atomic system update management skill supporting immutable infrastructure, atomic updates, version rollback, and modern system management features.

---

## 功能列表 | Features

### 1. 仓库管理 | Repository Management
- 创建 OSTree 仓库 | Create OSTree repos
- 初始化系统仓库 | Initialize system repos
- 仓库配置 | Repository configuration
- 远程仓库 | Remote repositories

### 2. 提交管理 | Commit Management
- 创建提交 | Create commits
- 查看提交历史 | View commit history
- 提交签名 | Commit signing
- 提交验证 | Commit verification

### 3. 部署管理 | Deployment Management
- 系统部署 | System deployment
- 版本切换 | Version switching
- 回滚操作 | Rollback operations
- 部署清理 | Deployment cleanup

### 4. 分支管理 | Branch Management
- 创建分支 | Create branches
- 列出分支 | List branches
- 删除分支 | Delete branches
- 分支合并 | Branch merging

### 5. 远程同步 | Remote Synchronization
- 添加远程 | Add remotes
- 拉取更新 | Pull updates
- 推送提交 | Push commits
- 镜像同步 | Mirror sync

### 6. 系统管理 | System Management
- 状态查询 | Status query
- 配置管理 | Configuration management
- 解锁系统 | Unlock system
- 叠加层管理 | Overlay management

---

## 配置 | Configuration

### 工具安装 | Tool Installation

```bash
# RHEL/Fedora
dnf install ostree rpm-ostree

# openSUSE
zypper install ostree

# Debian/Ubuntu
apt-get install ostree
```

### 仓库类型 | Repository Types

```bash
# 系统仓库 (bare-user)
# System repo (bare-user)
ostree --repo=/ostree/repo init --mode=bare-user

# 归档仓库 (archive-z2)
# Archive repo (archive-z2)
ostree --repo=/path/to/repo init --mode=archive-z2

#  bare 仓库
# Bare repo
ostree --repo=/path/to/repo init --mode=bare
```

---

## 使用示例 | Usage Examples

### 仓库初始化 | Repository Initialization

```bash
# 初始化系统仓库
# Initialize system repository
ostree --repo=/ostree/repo init --mode=bare-user

# 初始化归档仓库
# Initialize archive repository
ostree --repo=/var/www/html/repo init --mode=archive-z2

# 配置仓库
# Configure repository
cat > /ostree/repo/config << EOF
[core]
repo_version=1
mode=bare-user

[remote "fedora"]
url=https://ostree.fedoraproject.org
gpg-verify=true
EOF
```

### 提交管理 | Commit Management

```bash
# 创建提交
# Create commit
ostree commit \
  --repo=/path/to/repo \
  --branch=fedora/x86_64/server \
  --subject="Initial commit" \
  --tree=dir=/path/to/rootfs

# 从目录树创建提交
# Create commit from directory tree
ostree commit \
  --repo=/path/to/repo \
  --branch=main \
  --subject="Update packages" \
  --tree=dir=/var/www/html/rootfs

# 查看提交历史
# View commit history
ostree log --repo=/ostree/repo fedora/x86_64/server

# 显示提交详情
# Show commit details
ostree show --repo=/ostree/repo fedora/x86_64/server

# 删除提交
# Delete commit
ostree prune --repo=/path/to/repo --ref=main
```

### 签名和验证 | Signing and Verification

```bash
# 导入 GPG 密钥
# Import GPG key
ostree remote gpg-import \
  --repo=/ostree/repo \
  fedora \
  --stdin < /path/to/gpg-key

# 签名提交
# Sign commit
ostree sign \
  --repo=/path/to/repo \
  --gpg-key=KEYID \
  fedora/x86_64/server

# 验证提交
# Verify commit
ostree verify \
  --repo=/ostree/repo \
  fedora/x86_64/server

# 添加远程仓库（带签名验证）
# Add remote with signature verification
ostree remote add \
  --repo=/ostree/repo \
  fedora \
  https://ostree.fedoraproject.org/repo \
  --gpg-verify
```

### 部署管理 | Deployment Management

```bash
# 查看部署状态
# View deployment status
ostree admin status

# 部署新版本
# Deploy new version
ostree admin deploy --os=fedora fedora/x86_64/server

# 切换部署
# Switch deployment
ostree admin switch --os=fedora fedora/x86_64/server

# 回滚到上一版本
# Rollback to previous version
ostree admin rollback

# 清理旧部署
# Cleanup old deployments
ostree admin undeploy 1

# 设置下次启动版本
# Set next boot version
ostree admin set-origin --os=fedora fedora

# 查看部署历史
# View deployment history
journalctl -b -1
```

### 远程仓库管理 | Remote Repository Management

```bash
# 添加远程仓库
# Add remote repository
ostree remote add \
  --repo=/ostree/repo \
  fedora \
  https://ostree.fedoraproject.org/repo

# 列出远程仓库
# List remote repositories
ostree remote list --repo=/ostree/repo

# 删除远程仓库
# Remove remote repository
ostree remote delete \
  --repo=/ostree/repo \
  fedora

# 拉取更新
# Pull updates
ostree pull \
  --repo=/ostree/repo \
  --remote=fedora \
  fedora/x86_64/server

# 拉取最新提交
# Pull latest commit
ostree pull \
  --repo=/ostree/repo \
  --remote=fedora \
  --depth=1 \
  fedora/x86_64/server

# 推送提交
# Push commits
ostree push \
  --repo=/path/to/repo \
  --remote=origin \
  main
```

### 分支管理 | Branch Management

```bash
# 列出所有分支
# List all branches
ostree refs --repo=/path/to/repo

# 创建分支
# Create branch
ostree refs --repo=/path/to/repo \
  --create=feature/new-feature

# 删除分支
# Delete branch
ostree refs --repo=/path/to/repo \
  --delete=feature/old-feature

# 重命名分支
# Rename branch
ostree refs --repo=/path/to/repo \
  --rename=old/new

# 显示分支内容
# Show branch content
ostree ls --repo=/path/to/repo fedora/x86_64/server
```

---

## RPM-OSTree 集成 | RPM-OSTree Integration

### 包管理 | Package Management

```bash
# 叠加安装包
# Layer packages
rpm-ostree install vim wget curl

# 卸载叠加包
# Remove layered packages
rpm-ostree uninstall vim

# 查看叠加包
# View layered packages
rpm-ostree status

# 替换包
# Replace packages
rpm-ostree override replace https://example.com/package.rpm

# 安装本地 RPM
# Install local RPM
rpm-ostree install ./package.rpm
```

### 系统更新 | System Updates

```bash
# 检查更新
# Check for updates
rpm-ostree upgrade --check

# 执行更新
# Perform update
rpm-ostree upgrade

# 回滚更新
# Rollback update
rpm-ostree rollback

# 重新部署当前版本
# Redeploy current version
rpm-ostree rebase :current

# 切换到不同分支
# Switch to different branch
rpm-ostree rebase fedora/x86_64/silverblue
```

### 自定义镜像 | Custom Image

```bash
# 从 Kickstart 创建
# Create from Kickstart
rpm-ostree compose tree \
  --repo=/path/to/repo \
  --ref=fedora/x86_64/custom \
  --compose=/path/to/compose.json \
  /path/to/manifest.json

# 容器构建
# Container build
rpm-ostree compose container \
  --repo=/path/to/repo \
  --ref=fedora/x86_64/custom \
  fedora-custom:latest

# 导出为 ISO
# Export to ISO
rpm-ostree compose image \
  --repo=/path/to/repo \
  fedora/x86_64/custom \
  ./output.iso
```

---

## 高级用法 | Advanced Usage

### 自定义 OSTree 仓库 | Custom OSTree Repository

```bash
# 创建自定义仓库配置
# Create custom repo config
cat > /etc/ostree/remotes.d/custom.conf << EOF
[remote "custom"]
url=https://ostree.example.com/repo
gpg-verify=true
gpg-keypath=/etc/pki/ostree/gpg-keys
EOF

# 创建分支策略
# Create branch policy
cat > /etc/ostree/branches.conf << EOF
[branch "fedora/x86_64/*"]
collection-id=org.fedoraproject
EOF
```

### 自动化部署 | Automated Deployment

```bash
# 自动化部署脚本
# Automated deployment script
cat > /usr/local/bin/ostree-deploy.sh << 'EOF'
#!/bin/bash
set -e

# 拉取最新提交
# Pull latest commit
ostree pull --repo=/ostree/repo --remote=fedora fedora/x86_64/server

# 部署
# Deploy
ostree admin deploy --os=fedora fedora/x86_64/server

# 清理
# Cleanup
ostree admin undeploy 1
ostree prune --repo=/ostree/repo

echo "Deployment complete"
EOF

chmod +x /usr/local/bin/ostree-deploy.sh
```

### 监控和日志 | Monitoring and Logging

```bash
# 查看 OSTree 日志
# View OSTree logs
journalctl -u ostree-remount
journalctl -u rpm-ostreed

# 监控系统状态
# Monitor system status
watch -n 5 'ostree admin status'

# 检查仓库健康
# Check repo health
ostree fsck --repo=/ostree/repo
```

---

## 命令参考 | Command Reference

### OSTree 核心命令 | Core Commands

| 命令 | Command | 描述 | Description |
|------|---------|------|-------------|
| `ostree init` | initialize | 初始化仓库 | Initialize repo |
| `ostree commit` | commit | 创建提交 | Create commit |
| `ostree log` | log | 查看日志 | View log |
| `ostree show` | show | 显示提交 | Show commit |
| `ostree refs` | refs | 管理分支 | Manage branches |
| `ostree remote` | remote | 远程管理 | Remote management |
| `ostree pull` | pull | 拉取提交 | Pull commits |
| `ostree push` | push | 推送提交 | Push commits |
| `ostree verify` | verify | 验证提交 | Verify commit |

### OSTree Admin 命令 | Admin Commands

| 命令 | Command | 描述 | Description |
|------|---------|------|-------------|
| `ostree admin status` | status | 部署状态 | Deployment status |
| `ostree admin deploy` | deploy | 部署系统 | Deploy system |
| `ostree admin rollback` | rollback | 回滚 | Rollback |
| `ostree admin switch` | switch | 切换版本 | Switch version |
| `ostree admin undeploy` | undeploy | 删除部署 | Remove deployment |

### RPM-OSTree 命令 | RPM-OSTree Commands

| 命令 | Command | 描述 | Description |
|------|---------|------|-------------|
| `rpm-ostree status` | status | 系统状态 | System status |
| `rpm-ostree upgrade` | upgrade | 系统升级 | System upgrade |
| `rpm-ostree rollback` | rollback | 回滚 | Rollback |
| `rpm-ostree install` | install | 安装包 | Install package |
| `rpm-ostree uninstall` | uninstall | 卸载包 | Uninstall package |
| `rpm-ostree rebase` | rebase | 切换分支 | Switch branch |

---

## 最佳实践 | Best Practices

### 1. 仓库管理 | Repository Management
- 定期清理旧提交 | Prune old commits regularly
- 使用 GPG 签名 | Use GPG signing
- 配置多个远程 | Configure multiple remotes

### 2. 部署策略 | Deployment Strategy
- 测试后再部署 | Test before deploying
- 保留回滚版本 | Keep rollback versions
- 监控部署状态 | Monitor deployment status

### 3. 安全性 | Security
- 验证所有提交 | Verify all commits
- 使用 HTTPS 远程 | Use HTTPS remotes
- 定期更新密钥 | Rotate keys regularly

---

## 故障排除 | Troubleshooting

### 部署失败 | Deployment Failed
```bash
# 查看详细状态
# View detailed status
ostree admin status --verbose

# 检查仓库完整性
# Check repo integrity
ostree fsck --repo=/ostree/repo

# 清理并重新部署
# Clean and redeploy
rpm-ostree cleanup -b
rpm-ostree upgrade
```

### 签名验证失败 | Signature Verification Failed
```bash
# 重新导入密钥
# Re-import keys
ostree remote gpg-import --repo=/ostree/repo fedora

# 检查密钥
# Check keys
ostree remote gpg-list-keys --repo=/ostree/repo fedora
```

---

## 参考资料 | References

- [OSTree 官方文档 | OSTree Official Docs](https://ostreedev.github.io/ostree/)
- [Fedora Silverblue 文档 | Fedora Silverblue Docs](https://silverblue.fedoraproject.org/)
- [RHEL CoreOS 文档 | RHEL CoreOS Docs](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux_coreos/)

---

## 许可证 | License

MIT License

---

## 更新日志 | Changelog

### v1.0.0 (2026-03-23)
- 初始版本，完整的 OSTree 支持
- Initial release with full OSTree support
- 中英文双语文档
- Bilingual documentation (Chinese/English)
