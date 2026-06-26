# OpenClaw 系统需求文档

## 目录
- [硬件需求](#硬件需求)
- [操作系统支持](#操作系统支持)
- [软件依赖](#软件依赖)
- [网络要求](#网络要求)
- [权限要求](#权限要求)
- [部署模式](#部署模式)

## 概览
本文档详细说明 OpenClaw 智能体平台在各类环境下的系统需求,包括硬件配置、操作系统、软件依赖、网络连接和权限管理等方面。

## 硬件需求

### 轻量级配置 (网关模式)
适用于使用云端 API 的场景,硬件压力极小。

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| CPU | 2 核心 | 4 核及以上 |
| 内存 | 2 GB | 4 GB+ |
| 存储 | 10 GB SSD | 20 GB+ SSD |
| GPU | 不需要 | 不需要 |

### 标准配置 (本地小模型)
适用于运行 7B 参数本地模型。

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| CPU | 4 核 | 8 核+ (i5/Ryzen 5) |
| 内存 | 8 GB | 16 GB |
| 存储 | 20 GB SSD | 50 GB+ SSD |
| GPU | 6 GB 显存 (GTX 1660) | 8 GB+ 显存 (RTX 3060+) |

### 高级配置 (全本地大模型)
适用于运行 13B+ 参数大模型。

| 组件 | 最低要求 | 推荐配置 |
|------|----------|----------|
| CPU | 8 核 | 16 核+ (i7/Ryzen 7/M3 Pro) |
| 内存 | 16 GB | 32-64 GB |
| 存储 | 50 GB SSD | 500 GB+ NVMe SSD |
| GPU | 12 GB 显存 (RTX 3060) | 24 GB+ (2x RTX 4090) |

### 特殊说明

**内存需求**
- 网关模式(调用云端 API): 2 GB 足够
- 本地模型: 模型参数大小 × 2 (FP16) 或 × 1.3 (INT8) + 系统开销
- 7B 模型: 至少 14 GB 内存 (推荐 16 GB)
- 13B 模型: 至少 26 GB 内存 (推荐 32 GB)

**存储需求**
- 基础安装: 1-2 GB
- 日志和记忆: 根据使用量增长,建议预留 20 GB+
- 本地模型缓存: 模型文件大小 + 临时文件

**GPU 需求**
- 仅在运行本地模型时需要
- 推荐使用 NVIDIA GPU (支持 CUDA)
- 显存大小决定了能运行的最大模型
- 多 GPU 支持需要额外配置

## 操作系统支持

### macOS
- **最低版本**: macOS 12.0 (Monterey)
- **推荐版本**: macOS 14.0 (Sonoma) 及以上
- **架构**: Intel x86_64 或 Apple Silicon (M1/M2/M3)
- **优势**: 原生支持,体验最佳,无需额外配置
- **注意事项**: 需要安装 Xcode Command Line Tools

### Linux
- **发行版**:
  - Ubuntu 20.04 LTS 及以上 (推荐 Ubuntu 22.04 LTS)
  - Debian 11 及以上
  - CentOS 8 及以上
  - Fedora 35 及以上
  - Arch Linux (滚动更新)
- **内核**: 需要启用 `transparent_hugepage` 特性
- **优势**: 稳定可靠,适合生产环境
- **注意事项**: 需要手动安装构建工具

### Windows
- **最低版本**: Windows 10 21H2+
- **推荐版本**: Windows 11
- **部署方式**:
  - **WSL2**: 强烈推荐 (Ubuntu 22.04 镜像)
  - **原生 Windows**: 未经充分测试,兼容性问题较多
- **优势**: 桌面应用友好
- **注意事项**: 需要先安装 WSL2,原生 Windows 支持有限

### Windows WSL2 安装步骤

```powershell
# 1. 启用 WSL 功能 (管理员 PowerShell)
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 2. 重启计算机

# 3. 设置 WSL 默认版本为 2
wsl --set-default-version 2

# 4. 安装 Ubuntu
wsl --install -d Ubuntu

# 5. 完成 WSL 配置后,在 Ubuntu 终端中运行 OpenClaw 安装脚本
```

## 软件依赖

### 核心依赖

#### Node.js
- **最低版本**: v22.0.0
- **推荐版本**: v22 LTS 或更高
- **安装方式**:
  - macOS: `brew install node@22`
  - Linux: 使用 nvm 或包管理器
  - Windows: 官方安装包
- **验证命令**: `node --version` (应显示 v22.x.x)

#### npm
- **版本要求**: 随 Node.js 同步安装 (npm v10+)
- **验证命令**: `npm --version`

#### Git
- **用途**: 拉取 OpenClaw 源码和插件
- **安装方式**:
  - macOS: `brew install git`
  - Ubuntu/Debian: `sudo apt install git`
  - CentOS/RHEL: `sudo yum install git`
- **验证命令**: `git --version`

### 可选依赖

#### Python
- **版本**: Python 3.10 或 3.11
- **用途**: 某些插件和技能需要
- **注意**: Python 3.12+ 可能存在兼容性问题

#### 构建工具 (Linux/macOS)
- **包含**: gcc, g++, make, cmake
- **安装方式**:
  - Ubuntu/Debian: `sudo apt install build-essential`
  - CentOS/RHEL: `sudo yum groupinstall "Development Tools"`
  - macOS: Xcode Command Line Tools

#### Docker
- **版本**: 20.10.24+
- **用途**: 容器化部署和沙箱隔离
- **可选**: 仅在需要容器化部署时必需

#### Ollama
- **版本**: v0.15.4+
- **用途**: 本地模型运行
- **可选**: 仅在需要运行本地模型时必需

## 网络要求

### 出站连接

OpenClaw 需要访问以下服务:

1. **npm 仓库** (安装和更新)
   - 官方源: https://registry.npmjs.org/
   - 国内镜像: https://registry.npmmirror.com/ (推荐中国用户)

2. **GitHub** (源码和插件)
   - https://github.com/
   - https://api.github.com/

3. **AI 模型 API** (如使用云端模型)
   - OpenAI: https://api.openai.com/
   - Anthropic: https://api.anthropic.com/
   - DeepSeek: https://api.deepseek.com/
   - 阿里云百炼: https://dashscope.aliyuncs.com/

4. **通讯平台 API** (如接入第三方聊天工具)
   - Telegram: https://api.telegram.org/
   - Discord: https://discord.com/api/
   - 其他平台 API

### 网络配置

**企业网络环境**
- 配置 HTTP/HTTPS 代理
- 配置 npm 代理: `npm config set proxy http://proxy-server:port`
- 配置 git 代理: `git config --global http.proxy http://proxy-server:port`

**国内网络环境**
- 配置 npm 国内镜像源: `npm config set registry https://registry.npmmirror.com`
- 配置 GitHub 加速镜像或代理

### 端口要求

OpenClaw 默认使用以下端口:

| 端口 | 用途 | 协议 | 是否必需 |
|------|------|------|----------|
| 18789 | Web UI 和 API | HTTP/WS | 必需 |
| 18790 | 网关备用端口 | HTTP/WS | 可选 |
| 11434 | Ollama 本地模型 | HTTP | 本地模型时必需 |

**注意事项**:
- 防火墙需要放行上述端口
- 云服务器需要在安全组中开放端口
- 端口冲突时可修改配置文件

## 权限要求

### 用户权限

**macOS/Linux**
- 必须以具备 sudo 权限的普通用户身份运行
- 禁止使用 root 账户直接运行 OpenClaw
- 推荐创建专用用户: `sudo adduser openclaw`

**Windows**
- PowerShell 需要以"管理员身份运行"
- WSL2 中使用普通用户(避免使用 root)

### 目录权限

OpenClaw 需要以下目录的读写权限:

```
~/.openclaw/           # 配置和数据目录
  ├── config/          # 配置文件
  ├── logs/            # 日志文件
  ├── workspace/       # 工作空间
  └── plugins/         # 插件目录
~/.npm-global/         # npm 全局目录 (如配置)
```

**修复权限**:
```bash
chown -R $USER:$USER ~/.openclaw
chmod -R 755 ~/.openclaw
```

### 系统权限

**macOS 辅助功能**
- 文件操作需要辅助功能权限
- 系统偏好设置 > 安全性与隐私 > 辅助功能
- 添加终端或 OpenClaw 应用

**屏幕录制权限** (macOS)
- 屏幕截图需要屏幕录制权限
- 系统偏好设置 > 安全性与隐私 > 屏幕录制
- 添加终端或 OpenClaw 应用

## 部署模式

### 模式一: 网关模式 (Gateway Only)
- **描述**: OpenClaw 仅作为调度器,推理任务通过云端 API 完成
- **硬件需求**: 最低
- **网络需求**: 稳定的互联网连接
- **适用场景**: 个人使用、轻量级任务、快速体验

### 模式二: 混合模式 (Hybrid)
- **描述**: 核心功能使用本地小模型,复杂任务调用云端大模型
- **硬件需求**: 中等 (需要 GPU)
- **网络需求**: 偶尔联网
- **适用场景**: 追求性能和成本的平衡

### 模式三: 全本地模式 (Fully Local)
- **描述**: 所有推理都在本地完成,完全离线运行
- **硬件需求**: 高 (需要多 GPU)
- **网络需求**: 仅初始化时需要
- **适用场景**: 隐私优先、企业内部、完全自主

### 模式四: 分布式模式 (Distributed)
- **描述**: 网关、模型、节点分布在多台设备上
- **硬件需求**: 可扩展
- **网络需求**: 内网或 VPN
- **适用场景**: 企业级部署、多设备协同

## 推荐配置示例

### 个人开发者
```
系统: macOS 14 (M3 Pro 8GB)
模型: 调用 DeepSeek API
部署: 网关模式
```

### 小型团队
```
系统: Ubuntu 22.04 (8核 16GB)
模型: 本地 Qwen-7B
部署: Docker 容器化
```

### 企业内部
```
系统: 集群部署 (多节点)
模型: 本地 Qwen-14B
部署: 分布式模式 + VPN
```

## 环境检查清单

在安装前,请确认以下检查项:

- [ ] 操作系统版本符合要求
- [ ] Node.js 版本 >= 22
- [ ] npm 可用
- [ ] Git 已安装
- [ ] 内存满足最低要求
- [ ] 磁盘空间 >= 10GB
- [ ] 网络连接正常 (能访问 npm 和 GitHub)
- [ ] 端口 18789 未被占用
- [ ] 具备 sudo 权限 (macOS/Linux)
- [ ] 防火墙已配置 (如需要)

## 常见问题

### Q: 最低配置能否运行?
A: 最低配置 (2GB 内存, 2 核 CPU) 可以运行网关模式,但仅适合轻量任务。

### Q: 必须使用 GPU 吗?
A: 只有运行本地模型时才需要 GPU。如果使用云端 API,无需 GPU。

### Q: Windows 原生安装可以吗?
A: 官方未充分测试,强烈推荐使用 WSL2,兼容性问题更少。

### Q: 可以在服务器上无头运行吗?
A: 可以,OpenClaw 支持完全无头模式,通过 Web UI 或 CLI 控制。

### Q: 多用户如何部署?
A: 可以使用 Docker 容器化部署,或配置多租户支持。
