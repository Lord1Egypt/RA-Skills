# Mock Skill - 安全包构建

## 技能描述 | Skill Description

**名称 | Name:** mock  
**版本 | Version:** 1.0.0  
**作者 | Author:** OS Build Agent  
**领域 | Domain:** RPM Package Build Environment  

专业的 RPM 包安全构建环境管理技能，使用 Mock 在干净的 chroot 环境中构建 RPM 包，确保构建的可重复性和安全性。

Professional RPM package build environment management skill using Mock to build RPM packages in clean chroot environments, ensuring build reproducibility and security.

---

## 功能列表 | Features

### 1. 构建环境管理 | Build Environment Management
- 创建 chroot 环境 | Create chroot environments
- 初始化构建根 | Initialize build roots
- 清理构建环境 | Clean build environments
- 缓存管理 | Cache management

### 2. 包构建 | Package Building
- SRPM 构建 | SRPM building
- 本地 spec 构建 | Local spec building
- Git 仓库构建 | Git repo building
- 批量构建 | Batch building

### 3. 配置管理 | Configuration Management
- 预设配置 | Preset configurations
- 自定义配置 | Custom configurations
- 多架构配置 | Multi-arch configurations
- 仓库配置 | Repository configuration

### 4. 依赖管理 | Dependency Management
- 依赖解析 | Dependency resolution
- 依赖缓存 | Dependency caching
- 外部仓库 | External repositories
- 本地仓库 | Local repositories

### 5. 结果管理 | Result Management
- 构建结果查询 | Build result query
- 日志管理 | Log management
- RPM 提取 | RPM extraction
- SRPM 提取 | SRPM extraction

---

## 配置 | Configuration

### 工具安装 | Tool Installation

```bash
# RHEL/Fedora
dnf install mock

# 添加用户到 mock 组
# Add user to mock group
usermod -a -G mock $USER

# 配置 sudo (可选)
# Configure sudo (optional)
visudo
# 添加：youruser ALL=(ALL) NOPASSWD: /usr/bin/mock
```

### 配置文件 | Config Files

```bash
# 主配置文件
# Main config file
/etc/mock/default.cfg

# 预设配置目录
# Preset configs directory
/etc/mock/configs/

# 用户配置
# User config
~/.config/mock.cfg
```

### 常用预设 | Common Presets

```bash
# Fedora
fedora-39-x86_64
fedora-40-x86_64
fedora-rawhide-x86_64

# RHEL/CentOS
epel-9-x86_64
epel-8-x86_64
centos-stream-9-x86_64

# 其他架构
# Other architectures
fedora-39-aarch64
fedora-39-ppc64le
fedora-39-s390x
```

---

## 使用示例 | Usage Examples

### 基本构建 | Basic Building

```bash
# 从 SRPM 构建
# Build from SRPM
mock -r fedora-39-x86_64 ./package-1.0-1.fc39.src.rpm

# 从 spec 文件构建
# Build from spec file
mock -r fedora-39-x86_64 ./package.spec

# 指定结果目录
# Specify result directory
mock -r fedora-39-x86_64 \
  --resultdir ./results \
  ./package-1.0-1.fc39.src.rpm
```

### 环境管理 | Environment Management

```bash
# 初始化 chroot
# Initialize chroot
mock -r fedora-39-x86_64 --init

# 清理 chroot
# Clean chroot
mock -r fedora-39-x86_64 --clean

# 完全清理（包括缓存）
# Scrub all (including cache)
mock -r fedora-39-x86_64 --scrub=all

# 只清理缓存
# Scrub cache only
mock -r fedora-39-x86_64 --scrub=cache

# 列出可用的 chroot
# List available chroots
mock --list-chroots
```

### 自定义配置 | Custom Configuration

```bash
# 使用自定义配置
# Use custom config
mock -r ./custom.cfg ./package.src.rpm

# 添加额外仓库
# Add extra repository
mock -r fedora-39-x86_64 \
  --enable-plugin=chroot_scan \
  --enable-plugin=package_state \
  --config-opts=repo_add="https://example.com/repo" \
  ./package.src.rpm

# 添加本地仓库
# Add local repository
mock -r fedora-39-x86_64 \
  --repodir /path/to/local/repo \
  ./package.src.rpm
```

### 构建选项 | Build Options

```bash
# 重新构建
# Rebuild
mock -r fedora-39-x86_64 --rebuild ./package.src.rpm

# 仅构建 SRPM
# Build SRPM only
mock -r fedora-39-x86_64 --buildsrpm \
  --spec ./package.spec \
  --sources ./SOURCES/

# 安装构建结果
# Install build results
mock -r fedora-39-x86_64 \
  --install ./results/package-1.0-1.rpm

# 在 chroot 中执行命令
# Execute command in chroot
mock -r fedora-39-x86_64 --chroot -- rpm -qa

# 获取 shell
# Get shell
mock -r fedora-39-x86_64 --shell
```

### 结果管理 | Result Management

```bash
# 列出构建结果
# List build results
mock -r fedora-39-x86_64 --print-result-path

# 复制结果到目录
# Copy results to directory
mock -r fedora-39-x86_64 \
  --copyout /var/lib/mock/fedora-39-x86_64/result/ \
  ./results/

# 查看构建日志
# View build log
mock -r fedora-39-x86_64 --print-result-path
cat ./results/build.log

# 获取 SRPM
# Get SRPM
mock -r fedora-39-x86_64 --get-result='*.src.rpm'
```

### 插件使用 | Plugin Usage

```bash
# 启用 chroot_scan 插件（保存 chroot 状态）
# Enable chroot_scan plugin (save chroot state)
mock -r fedora-39-x86_64 \
  --enable-plugin=chroot_scan \
  --plugin-opt=chroot_scan:only_failed=True \
  ./package.src.rpm

# 启用 package_state 插件（记录包状态）
# Enable package_state plugin (log package state)
mock -r fedora-39-x86_64 \
  --enable-plugin=package_state \
  ./package.src.rpm

# 启用 sign 插件（签名包）
# Enable sign plugin (sign packages)
mock -r fedora-39-x86_64 \
  --enable-plugin=sign \
  --plugin-opt=sign:cmds="rpm --addsign" \
  ./package.src.rpm

# 启用 ccache 插件（编译缓存）
# Enable ccache plugin (compile cache)
mock -r fedora-39-x86_64 \
  --enable-plugin=ccache \
  ./package.src.rpm
```

### 批量构建 | Batch Building

```bash
# 构建多个 SRPM
# Build multiple SRPMs
for srpm in *.src.rpm; do
  mock -r fedora-39-x86_64 "$srpm"
done

# 并行构建（使用 systemd-run）
# Parallel build (using systemd-run)
for srpm in *.src.rpm; do
  systemd-run --scope mock -r fedora-39-x86_64 "$srpm" &
done
wait

# 使用 mockchain（链式构建）
# Use mockchain (chain build)
mockchain \
  -r fedora-39-x86_64 \
  --basedir /var/mockchain \
  --localrepo /var/mockchain/local \
  package1.src.rpm \
  package2.src.rpm \
  package3.src.rpm
```

---

## 自定义配置示例 | Custom Config Example

```python
# custom.cfg 示例
# custom.cfg example

config_opts['root'] = 'custom-1.0-x86_64'
config_opts['target_arch'] = 'x86_64'
config_opts['legal_host_arches'] = ('x86_64',)

# 基础发行版
# Base distribution
config_opts['dist'] = 'fc39'
config_opts['releasever'] = '39'

# 仓库配置
# Repository configuration
config_opts['yum.conf'] = """
[main]
cachedir=/var/cache/yum
debuglevel=1
reposdir=/dev/null
logfile=/var/log/yum.log
retries=20
obsoletes=1
gpgcheck=0
assumeyes=1
syslog_ident=mock
syslog_device=

[fedora]
name=Fedora $releasever - $basearch
baseurl=https://download.fedoraproject.org/pub/fedora/linux/releases/$releasever/Everything/$basearch/os/
enabled=1

[updates]
name=Fedora $releasever - $basearch - Updates
baseurl=https://download.fedoraproject.org/pub/fedora/linux/updates/$releasever/Everything/$basearch/
enabled=1

[epel]
name=EPEL $releasever - $basearch
baseurl=https://download.fedoraproject.org/pub/epel/$releasever/$basearch/
enabled=1
"""

# 包管理
# Package management
config_opts['chroot_additional_packages'] = 'gcc gcc-c++ make rpm-build'
config_opts['chroot_setup_cmd'] = 'install bash bzip2 coreutils cpio diffutils findutils gawk grep gzip info make patch redhat-rpm-config rpm-build sed shadow-utils tar unzip util-linux which xz'

# 资源限制
# Resource limits
config_opts['rpmbuild_networking'] = True
config_opts['use_host_resolv'] = True
config_opts['print_main_output'] = True
```

---

## 命令参考 | Command Reference

| 命令 | Command | 描述 | Description |
|------|---------|------|-------------|
| `mock -r <config>` | build | 构建 SRPM | Build SRPM |
| `--init` | initialize | 初始化 chroot | Initialize chroot |
| `--clean` | clean | 清理 chroot | Clean chroot |
| `--scrub=all` | scrub all | 完全清理 | Scrub all |
| `--shell` | shell | 进入 chroot shell | Enter chroot shell |
| `--chroot` | chroot | 在 chroot 中执行命令 | Execute in chroot |
| `--rebuild` | rebuild | 重新构建 | Rebuild |
| `--buildsrpm` | build SRPM | 仅构建 SRPM | Build SRPM only |
| `--resultdir` | result dir | 指定结果目录 | Specify result dir |
| `--copyout` | copy out | 复制结果 | Copy results |
| `--install` | install | 安装结果包 | Install result packages |
| `--list-chroots` | list chroots | 列出可用 chroot | List available chroots |
| `--enable-plugin` | enable plugin | 启用插件 | Enable plugin |

---

## 最佳实践 | Best Practices

### 1. 构建环境 | Build Environment
- 使用官方预设配置 | Use official preset configs
- 定期清理缓存 | Clean cache regularly
- 保持 chroot 更新 | Keep chroot updated

### 2. 性能优化 | Performance Optimization
- 启用 ccache 插件 | Enable ccache plugin
- 使用 SSD 存储 | Use SSD storage
- 调整并发构建数 | Adjust concurrent builds

### 3. 安全性 | Security
- 在隔离环境中构建 | Build in isolated environment
- 验证 SRPM 签名 | Verify SRPM signatures
- 不信任上游代码 | Don't trust upstream code blindly

---

## 故障排除 | Troubleshooting

### 构建失败 | Build Failed
```bash
# 查看详细日志
# View detailed logs
cat /var/lib/mock/<config>/result/build.log

# 检查 chroot 状态
# Check chroot state
mock -r <config> --chroot -- rpm -qa

# 重新初始化
# Reinitialize
mock -r <config> --scrub=all
mock -r <config> --init
```

### 依赖问题 | Dependency Issues
```bash
# 检查仓库配置
# Check repo configuration
mock -r <config> --chroot -- cat /etc/yum.repos.d/*

# 手动安装依赖
# Manually install dependencies
mock -r <config> --chroot -- dnf install <package>
```

---

## 参考资料 | References

- [Mock 官方文档 | Mock Official Docs](https://rpm-software-management.github.io/mock/)
- [Fedora 构建指南 | Fedora Build Guide](https://docs.fedoraproject.org/en-US/quick-docs/mock/)
- [Mock 插件文档 | Mock Plugin Docs](https://rpm-software-management.github.io/mock/plugins.html)

---

## 许可证 | License

MIT License

---

## 更新日志 | Changelog

### v1.0.0 (2026-03-23)
- 初始版本，完整的 Mock 支持
- Initial release with full Mock support
- 中英文双语文档
- Bilingual documentation (Chinese/English)
