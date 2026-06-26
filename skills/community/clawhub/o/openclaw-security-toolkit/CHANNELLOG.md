# OpenClaw Security Guard 安全管家

## 基本信息

- **名称**: openclaw-security-guard
- **版本**: v1.0.0
- **描述**: OpenClaw 用户的安全管家，审计配置、扫描敏感信息、管理权限
- **发布时间**: 2026-03-11
- **作者**: OpenClaw Community

## 核心功能

- 🔍 **安全审计** - 全面的安全配置检查，一键发现风险
- 🔐 **敏感信息扫描** - 检测暴露的 API 密钥和令牌
- 👥 **访问控制** - 管理设备、用户和权限
- 🔑 **令牌管理** - 轮换和验证令牌
- 📊 **安全报告** - 生成详细的安全报告
- 🛡️ **安全加固** - 应用安全最佳实践

## 安全检查项

| 类别 | 检查内容 |
|------|----------|
| 配置安全 | Gateway 绑定地址、认证模式、Token 强度 |
| 敏感信息 | API Key、Token、密码、私钥 |
| 访问控制 | 设备、用户、频道、会话 |
| 网络安全 | 公网暴露、开放端口 |

## 使用示例

```bash
# 运行安全审计
python3 {baseDir}/scripts/main.py audit

# 扫描敏感信息
python3 {baseDir}/scripts/main.py scan

# 生成安全报告
python3 {baseDir}/scripts/main.py report --format md

# 查看令牌状态
python3 {baseDir}/scripts/main.py token status

# 列出已配对设备
python3 {baseDir}/scripts/main.py access devices

# 安全加固（自动修复）
python3 {baseDir}/scripts/main.py harden --fix
```

## 输出格式

- **table** - 表格格式（默认）
- **json** - JSON 格式
- **md** - Markdown 格式

## 语言支持

- 中文 (zh)
- English (en)

根据系统语言自动选择。

## 更新记录

### v1.0.0 (2026-03-11)
- 初始版本发布
- 支持中英文界面
- 完整的安全审计功能

## 许可证

MIT License