---
name: openclaw-security-checklist
description: OpenClaw 部署前安全检查清单。聚焦合规导向的部署前检查（非事后加固），覆盖防火墙、SSH、API 密钥管理、数据出境合规、多部署场景验证。使用清单式检查，可逐项打勾并生成报告。适用于个人 Mac、VPS、Docker、企业部署场景。
---

# OpenClaw 安全部署检查清单

**定位**: 部署前合规检查（与 `healthcheck` 技能的事后加固互补）

**核心价值**:
- ✅ 部署前检查（不是事后加固）
- ✅ 合规导向（工信部要求、API 密钥管理、数据出境）
- ✅ 清单式（可逐项打勾，适合分享传播）
- ✅ 多场景覆盖（个人 Mac / VPS / Docker / 企业部署）

## 快速开始

### 方式一：执行自动检查脚本

```bash
cd ~/.openclaw/workspace/skills/openclaw-security-checklist
./scripts/security-check.sh
```

脚本会自动检查以下类别并生成报告：
- 🔥 防火墙配置
- 🔐 SSH 安全配置
- 🔑 API 密钥管理
- 🌍 数据出境合规
- 📦 部署场景检查
- 🔄 系统更新

### 方式二：手动逐项检查

参考 `references/` 目录下的详细检查清单：

```bash
# 查看某类检查项
cat references/compliance-cn.md        # 中国法规合规
cat references/api-key-management.md   # API 密钥管理
cat references/data-border.md          # 数据出境检查

# 查看特定部署场景
cat references/deployment-scenarios/personal-mac.md
cat references/deployment-scenarios/vps.md
cat references/deployment-scenarios/docker.md
cat references/deployment-scenarios/enterprise.md
```

## 检查流程

### 1. 部署前（Pre-Deployment）

**必须完成**:
- [ ] 阅读 `references/compliance-cn.md` 了解法规要求
- [ ] 根据部署场景选择对应检查清单
- [ ] 配置 API 密钥管理（使用环境变量，非硬编码）
- [ ] 如服务器在境外，评估数据出境合规风险

### 2. 部署中（During Deployment）

**执行检查**:
```bash
./scripts/security-check.sh
```

**修复问题**:
- 红色 ❌ 失败项：必须修复后才能上线
- 黄色 ⚠️ 警告项：建议优化，可后续处理

### 3. 部署后（Post-Deployment）

**持续监控**:
- 保存检查报告：`~/openclaw-security-report.txt`
- 定期（每月）重新运行检查
- 重大变更后（如迁移、升级）重新检查

## 检查项详解

### 🔥 防火墙配置

| 检查项 | 要求 | 修复建议 |
|--------|------|----------|
| 防火墙状态 | 必须启用 | UFW: `sudo ufw enable` |
| 开放端口 | 仅开放必要端口 | 默认：7001 (Gateway), 7002 (Node) |
| 访问来源 | 限制 IP 范围 | VPS 安全组配置白名单 |

### 🔐 SSH 安全配置

| 检查项 | 要求 | 修复建议 |
|--------|------|----------|
| Root 登录 | 禁止 | `PermitRootLogin no` |
| 密码认证 | 禁用（仅密钥） | `PasswordAuthentication no` |
| SSH 端口 | 非标准端口 | 修改 `/etc/ssh/sshd_config` |
| 密钥类型 | Ed25519 或 RSA 4096+ | `ssh-keygen -t ed25519` |

### 🔑 API 密钥管理

| 检查项 | 要求 | 修复建议 |
|--------|------|----------|
| 存储方式 | 环境变量或加密文件 | 使用 `.env` 文件，权限 600 |
| 硬编码检测 | 无硬编码密钥 | 扫描代码库：`grep -r "sk-\|api_key"` |
| 密钥轮换 | 定期轮换（90 天） | 设置日历提醒 |
| 访问日志 | 记录密钥使用 | 检查 OpenClaw 日志 |

### 🌍 数据出境合规（中国法规）

**适用场景**: 服务器位于中国境外 + 服务中国用户

| 检查项 | 要求 | 修复建议 |
|--------|------|----------|
| 服务器位置 | 境内优先 | 如境外需申报安全评估 |
| 隐私政策 | 必须存在 | 创建 `PRIVACY.md` |
| 数据加密 | 传输 + 存储加密 | 启用 HTTPS，使用 OpenSSL |
| 用户同意 | 明确告知数据用途 | 隐私政策中说明 |

**法规参考**:
- 《网络安全法》
- 《数据安全法》
- 《个人信息保护法》
- 《数据出境安全评估办法》

详见：`references/compliance-cn.md`

### 📦 部署场景检查

#### 个人 Mac
- [ ] 启用 FileVault 磁盘加密
- [ ] 配置 macOS 防火墙
- [ ] 禁用不必要的系统服务

#### VPS（阿里云/腾讯云/AWS）
- [ ] 配置安全组规则（最小开放原则）
- [ ] 启用云监控和告警
- [ ] 配置自动快照备份

#### Docker
- [ ] 使用非 root 用户运行容器
- [ ] 限制容器资源（CPU/内存）
- [ ] 挂载卷权限检查

#### 企业部署
- [ ] 配置 SSO/LDAP 集成
- [ ] 审计日志集中收集
- [ ] 灾备和恢复演练

## 报告解读

脚本生成的报告格式：

```
检查项目总数：24
通过：20
警告：3
失败：1

⚠️  发现 1 项严重问题，建议立即修复！
```

**评级标准**:
- 🟢 优秀：0 失败，0-2 警告
- 🟡 合格：0 失败，3-5 警告
- 🔴 风险：任何失败项

## 与 healthcheck 技能的区别

| 维度 | openclaw-security-checklist | healthcheck |
|------|----------------------------|-------------|
| **时机** | 部署前检查 | 部署后加固 |
| **导向** | 合规清单式 | 技术硬编码 |
| **输出** | 检查报告（可分享） | 修复建议（可执行） |
| **场景** | 多场景覆盖 | 主机加固为主 |
| **频率** | 部署时 + 重大变更 | 定期（每月） |

**建议工作流**:
1. 部署前：运行 `openclaw-security-checklist`
2. 修复问题后上线
3. 定期：运行 `healthcheck` 进行加固审计

## 相关文件

- `scripts/security-check.sh` - 自动检查脚本
- `references/compliance-cn.md` - 中国法规合规详解
- `references/api-key-management.md` - API 密钥管理规范
- `references/data-border.md` - 数据出境检查清单
- `references/deployment-scenarios/` - 各场景详细检查项

## 更新日志

- **v1.0 (2026-03-15)**: 初始版本，覆盖基础检查项
