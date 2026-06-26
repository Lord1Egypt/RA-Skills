# OpenClaw 安全部署检查清单

**版本**: v1.0.0  
**更新日期**: 2026-03-15  
**作者**: OpenClaw Community

---

## 📋 技能简介

**OpenClaw 安全部署检查清单** 是一个合规导向的部署前安全检查工具，帮助个人和企业用户在部署 OpenClaw 前完成必要的安全配置和合规检查。

### 核心特性

- ✅ **部署前检查** - 不是事后加固，而是预防性检查
- ✅ **合规导向** - 覆盖中国法规要求（网络安全法、个人信息保护法、数据出境）
- ✅ **清单式设计** - 可逐项打勾，适合团队分享和审计
- ✅ **多场景支持** - 个人 Mac、VPS、Docker、企业部署全覆盖
- ✅ **自动化报告** - 一键生成 Markdown 格式检查报告

### 与 healthcheck 技能的区别

| 维度 | openclaw-security-checklist | healthcheck |
|------|----------------------------|-------------|
| **时机** | 部署前检查 | 部署后加固 |
| **导向** | 合规清单式 | 技术硬编码 |
| **输出** | 检查报告（可分享） | 修复建议（可执行） |
| **场景** | 多场景覆盖 | 主机加固为主 |
| **频率** | 部署时 + 重大变更 | 定期（每月） |

**建议工作流**: 先用 `security-checklist` 做部署前检查，上线后用 `healthcheck` 定期加固。

---

## 🚀 快速开始

### 安装

```bash
# 通过 clawhub 安装
clawhub install openclaw-security-checklist

# 或手动克隆
git clone https://github.com/your-repo/openclaw-security-checklist.git \
  ~/.openclaw/workspace/skills/openclaw-security-checklist
```

### 使用

#### 方式一：自动检查脚本（推荐）

```bash
cd ~/.openclaw/workspace/skills/openclaw-security-checklist
./scripts/security-check.sh
```

脚本会自动检查以下类别：
- 🔥 防火墙配置
- 🔐 SSH 安全配置
- 🔑 API 密钥管理
- 🌍 数据出境合规
- 📦 部署场景检查
- 🔄 系统更新

#### 方式二：手动检查

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

#### 方式三：生成报告

```bash
# 生成 Markdown 报告
./scripts/security-check.sh > ~/openclaw-security-report.md

# 查看报告
cat ~/openclaw-security-report.md
```

---

## 📊 检查项详解

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
| 硬编码检测 | 无硬编码密钥 | 扫描代码库：`grep -r "sk-"` |
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

---

## 📈 报告解读

脚本生成的报告格式：

```
检查项目总数：24
通过：20
警告：3
失败：1

⚠️  发现 1 项严重问题，建议立即修复！
```

**评级标准**:
- 🟢 **优秀**: 0 失败，0-2 警告
- 🟡 **合格**: 0 失败，3-5 警告
- 🔴 **风险**: 任何失败项

**示例报告**: 参见 `example-report.md`

---

## 🛠️ 高级用法

### 自定义检查项

编辑 `scripts/security-check.sh`，添加自定义检查函数：

```bash
check_custom() {
    section "🔧 自定义检查"
    
    if [[ -f /path/to/check ]]; then
        print_result "PASS" "自定义检查项"
    else
        print_result "FAIL" "自定义检查项未通过"
    fi
}

# 在主函数中调用
main() {
    check_firewall
    check_ssh
    check_api_keys
    check_data_border
    check_deployment
    check_updates
    check_custom  # 添加自定义检查
    generate_report
}
```

### 集成到 CI/CD

```yaml
# .gitlab-ci.yml 示例
security_check:
  stage: test
  script:
    - cd ~/.openclaw/workspace/skills/openclaw-security-checklist
    - ./scripts/security-check.sh
  artifacts:
    reports:
      security: ~/openclaw-security-report.md
```

### 定期自动检查

```bash
# crontab -e
# 每月 1 号凌晨 2 点自动检查
0 2 1 * * ~/.openclaw/workspace/skills/openclaw-security-checklist/scripts/security-check.sh
```

---

## 📚 参考文档

### 核心文档
- `SKILL.md` - 技能定义和触发逻辑
- `scripts/security-check.sh` - 自动检查脚本
- `example-report.md` - 示例报告

### 合规参考
- `references/compliance-cn.md` - 中国法规合规详解
- `references/api-key-management.md` - API 密钥管理规范
- `references/data-border.md` - 数据出境检查清单

### 部署场景
- `references/deployment-scenarios/personal-mac.md` - 个人 Mac 部署
- `references/deployment-scenarios/vps.md` - VPS 部署
- `references/deployment-scenarios/docker.md` - Docker 部署
- `references/deployment-scenarios/enterprise.md` - 企业部署

---

## 🤝 贡献指南

### 报告问题

发现检查项遗漏或错误？请提交 Issue：

```markdown
**问题类型**: 遗漏检查项 / 检查项错误 / 文档问题
**场景**: 个人 Mac / VPS / Docker / 企业
**描述**: 详细描述问题
**建议**: 你的改进建议
```

### 提交改进

欢迎提交 PR 改进检查项或文档：

```bash
# Fork 仓库
git clone https://github.com/your-username/openclaw-security-checklist.git

# 创建分支
git checkout -b feature/add-new-check

# 修改并测试
# ...

# 提交
git commit -m "feat: 添加 XXX 检查项"
git push origin feature/add-new-check
```

### 分享场景

如果你在使用特定场景（如 Kubernetes、树莓派等），欢迎贡献对应的检查清单：

```bash
# 创建新场景文件
cat > references/deployment-scenarios/raspberry-pi.md << EOF
# 树莓派部署检查清单

## 特殊考虑
- SD 卡寿命（避免频繁写入）
- 散热配置
- 电源稳定性

## 检查项
...
EOF
```

---

## 📝 更新日志

### v1.0.0 (2026-03-15)
- ✨ 初始版本发布
- ✅ 支持 4 大部署场景
- ✅ 覆盖 6 类安全检查
- ✅ 生成 Markdown 报告
- ✅ 集成 Discord 告警

### v0.1.0 (2026-03-14)
- 🧪 内部测试版
- 基础检查框架
- 个人 Mac 场景支持

---

## 📄 许可证

MIT License - 详见 `LICENSE` 文件

---

## 🔗 相关资源

- **OpenClaw 官方文档**: https://docs.openclaw.ai
- **ClawHub 技能市场**: https://clawhub.com
- **Discord 社区**: https://discord.com/invite/clawd
- **GitHub 仓库**: https://github.com/openclaw/openclaw

### 相关技能推荐
- `healthcheck` - 主机安全加固
- `openclaw-skill-vetter` - 技能安全审查
- `discord` - Discord 消息通知

---

## 💬 常见问题

### Q: 检查脚本会修改我的系统配置吗？

**A**: 不会。脚本只读检查，不会修改任何配置。修复建议需要手动执行。

### Q: 所有检查项都必须通过吗？

**A**: 不一定。失败项（❌）建议修复，警告项（⚠️）可根据实际情况决定。但涉及安全基线的检查项（如防火墙、SSH）强烈建议修复。

### Q: 可以在 Windows 上运行吗？

**A**: 当前版本仅支持 macOS 和 Linux。Windows 用户建议使用 WSL2 或 Docker 部署。

### Q: 如何自定义告警阈值？

**A**: 编辑 `scripts/security-check.sh`，修改 `generate_report` 函数中的评级逻辑。

### Q: 检查报告可以分享给客户吗？

**A**: 可以。报告设计为可分享格式，适合交付给客户或审计团队。

---

**🦞 Happy Securing!**
