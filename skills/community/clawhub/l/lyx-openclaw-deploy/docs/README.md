# OpenClaw Deploy

> 一键打包 OpenClaw 环境，随时部署到任意服务器。

## 功能特性

| 模块 | 功能 |
|------|------|
| **镜像打包** | 基础打包 / 完整打包 / 自定义打包 |
| **镜像管理** | 查看信息 / SHA256 完整性校验 / 版本管理 |
| **本地部署** | 一键还原部署 / 环境预检 / 冲突处理 |
| **远程部署** | SSH 远程部署 / 传输加密 / 自动校验 |
| **批量部署** | 多主机并行部署 / 主机清单 / 逐个状态报告（V1.2） |
| **运维辅助** | 多级别日志 / 故障排查指南 / 部署模板（V1.2） |

## 支持场景

- **环境迁移**：从开发机迁移到服务器，一键打包带走
- **批量部署**：多台服务器统一部署同一套环境
- **环境备份**：完整快照，回滚无忧
- **团队标准化**：确保团队成员环境一致

## 快速开始

### 打包

```bash
# 基础打包（仅配置）
./build/base/base_builder.sh --output ./openclaw-config.tar.gz

# 完整打包（配置 + 工作区 + 技能）
./build/full/full_builder.sh --output ./openclaw-full.tar.gz

# 自定义打包（选择性包含内容）
./build/custom/custom_builder.sh --output ./openclaw-custom.tar.gz
```

### 本地部署

```bash
# 一键部署
./build/full/full_builder.sh --package ./openclaw-full.tar.gz --install-dir ~/.openclaw

# 指定冲突处理策略
./build/full/full_builder.sh --package ./openclaw-full.tar.gz --conflict backup
```

### 远程部署

```bash
# SSH 密钥部署
./build/remote/remote_deploy.sh \
  --host 192.168.1.100 \
  --user root \
  --key ~/.ssh/id_rsa \
  --package ./openclaw-full.tar.gz
```

### 批量部署（V1.2 新增）

```bash
# 复制主机清单模板并编辑
cp config/inventory.example.ini config/inventory.ini
# 编辑 inventory.ini 填入真实主机信息

# 并行部署到多台主机
./deploy/batch/batch_deploy.sh \
  --inventory config/inventory.ini \
  --package ./openclaw-full.tar.gz \
  --parallel 8 \
  --mode backup

# 模拟运行（不实际部署）
./deploy/batch/batch_deploy.sh \
  --inventory config/inventory.ini \
  --package ./openclaw-full.tar.gz \
  --dry-run
```

### 镜像管理

```bash
# 查看镜像信息
./build/image_manager.sh info ./openclaw-full.tar.gz

# 完整性校验
./build/image_manager.sh verify ./openclaw-full.tar.gz

# 列出本地镜像
./build/image_manager.sh list ~/.openclaw/images/
```

## 冲突处理策略

| 策略 | 说明 |
|------|------|
| `backup`（默认） | 先备份旧环境，再覆盖 |
| `cover` | 直接覆盖，不保留旧文件 |
| `update` | 仅更新插件/配置，不覆盖核心 |
| `parallel` | 安装到独立目录，多版本共存 |

## 系统要求

- **操作系统**：macOS、Linux（Ubuntu / CentOS / Debian）
- **依赖**：`bash 4.0+`、`tar`、`ssh`（远程部署）
- **网络**：GitHub 访问（用于拉取 OpenClaw 依赖）

## 目录结构

```
openclaw-deploy/
├── build/              # 打包模块
│   ├── base/           # 基础打包
│   ├── full/           # 完整打包
│   ├── custom/         # 自定义打包
│   ├── common.sh       # 通用函数
│   └── image_manager.sh # 镜像管理
├── deploy/             # 部署模块
│   ├── local/          # 本地部署
│   │   ├── check_env.sh
│   │   └── handle_conflict.sh
│   ├── remote/         # 远程部署
│   │   └── remote_deploy.sh
│   └── batch/          # 批量部署（V1.2）
│       └── batch_deploy.sh
├── config/             # 配置文件（V1.2）
│   └── inventory.example.ini
├── utils/              # 辅助工具
│   └── logging.sh       # 多级别日志（V1.2）
├── docker/             # Docker 部署配置
├── tests/              # 测试套件
└── docs/               # 文档
    └── TROUBLESHOOTING.md  # 故障排查指南（V1.2）
```

## 安全说明

- 打包时**自动清除**敏感信息（API Key、Token、密码）
- 传输使用 **SSH 加密**（远程部署）
- 完整性校验使用 **SHA256**

## 商业支持

OpenClaw Deploy 提供商业技术支持与定制服务：

- **标准支持**：¥999/月，适合个人/小团队
- **高级支持**：¥2999/月，含批量部署、优先响应
- **定制开发**：按需报价，含私有化部署、LDAP 集成等

联系：博客底部留言 / 微信公众号「MicRabbit」

---

*OpenClaw Deploy 是 MicRabbit AI 团队出品的开源工具，遵循 MIT 协议。*
