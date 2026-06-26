---
name: openclaw-deploy
description: 一键打包和部署 OpenClaw 环境到任意服务器。自动移除敏感信息、支持本地/远程/批量部署、冲突处理、SHA256 完整性校验、详细日志与故障排查指南。适用于 OpenClaw 环境迁移、批量部署、团队标准化。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["bash", "tar", "ssh"] },
        "install":
          [
            {
              "id": "clone",
              "kind": "clone",
              "url": "https://github.com/lyx058019/openclaw-deploy",
              "label": "Clone openclaw-deploy repo",
            },
          ],
      },
  }
---

# OpenClaw Deploy - 一键打包部署

## 功能

1. **打包配置**：基础 / 完整 / 自定义打包，自动移除敏感信息
2. **镜像管理**：查看信息、SHA256 校验、版本管理
3. **本地部署**：一键还原部署、环境预检、4种冲突处理策略
4. **远程部署**：SSH 远程单台部署
5. **批量部署**：多主机并行部署，支持主机清单（V1.2 新增）
6. **运维辅助**：详细日志、故障排查指南（V1.2 新增）

---

## 快速开始

```bash
git clone https://github.com/lyx058019/openclaw-deploy.git
cd openclaw-deploy

# 打包
./build/full/full_builder.sh --output ./openclaw.tar.gz

# 本地部署
./build/full/full_builder.sh --package ./openclaw.tar.gz --install-dir ~/.openclaw

# 批量部署（多主机）
./deploy/batch/batch_deploy.sh \
  --inventory ./config/inventory.example.ini \
  --package ./openclaw.tar.gz \
  --parallel 4
```

---

## 批量部署示例

复制主机清单模板：

```bash
cp config/inventory.example.ini config/inventory.ini
# 编辑 inventory.ini 填入真实主机信息
```

清单格式（Ansible 兼容）：

```ini
[production]
web01 ansible_host=192.168.1.101 ansible_user=ubuntu
web02 ansible_host=192.168.1.102 ansible_user=ubuntu

[staging]
stage01 ansible_host=192.168.1.201 ansible_user=root
```

执行批量部署：

```bash
./deploy/batch/batch_deploy.sh \
  --inventory config/inventory.ini \
  --package ./openclaw.tar.gz \
  --parallel 8 \
  --mode backup
```

---

## 服务器要求

| 项目 | 最低要求 |
|------|----------|
| 系统 | Ubuntu 20.04+ / CentOS 7+ / macOS |
| Docker | 20.10+ |
| 内存 | ≥ 4GB |
| CPU | ≥ 2 核 |

---

## 安全说明

- ✅ 导出时自动移除敏感信息（apiKey、token 等）
- ✅ SHA256 完整性校验
- ✅ SSH 加密传输
- ⚠️ 部署后手动填入 API Keys
