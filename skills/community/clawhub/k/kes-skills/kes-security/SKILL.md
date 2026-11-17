---
name: kes-security
name_for_command: kes-security
description: KingbaseES 安全合规指南。当用户提到安全、国密 SM2/SM3/SM4、三权分立、TDE 透明加密、审计、防篡改、MAC 标记访问控制、多因子认证、客体重用、等保合规时，必须使用此技能。
---

# KingbaseES 安全合规指南

本技能指导用户完成 KingbaseES 的安全配置和合规检查，涵盖国密认证、三权分立、TDE、审计、MAC 和防篡改。

## 安全模块

| 场景 | 模块 | 参考 |
|------|------|------|
| 三权分立 | system/sso/sao + 受限 DBA | `ref/security-three-authority.md` |
| 国密认证 | SM2 证书 + kcert 系列 | `ref/security-national-crypto.md` |
| 安全传输 | SSL/TLS + 国密 SSL | `ref/security-transport.md` |
| 操作审计 | 数据库审计 | `ref/security-audit.md` |
| TDE 透明加密 + 应用层加密 + 防篡改 | sysencrypt + kdb_ledger + encrypt/digest/sm2/sm3/sm4 | `ref/security-tde.md` |
| 强制访问控制 | 标签 / MAC (sysmac) | `ref/security-label-mac.md` |
| 强认证+脱敏 | 多因素认证/密码策略/数据脱敏 | `ref/security-auth.md` |
| 客体重用安全 | sysreuse_residual_data | `ref/security-reuse.md` |

## 等保合规检查流程

```
1. 三权分立审查 → security-three-authority.md
2. 认证强度评估 → security-auth.md / security-national-crypto.md
3. 传输加密检查 → security-transport.md
4. TDE 加密检查 → security-tde.md
5. 访问控制验证 → security-label-mac.md
6. 客体重用验证 → security-reuse.md
7. 审计策略审查 → security-audit.md
8. 生成合规报告
```

## 日常安全巡检

```
1. 检查审计日志 → security-audit.md
2. 检查认证强度 → security-auth.md
3. 检查传输加密 → security-transport.md
4. 检查 TDE 加密 → security-tde.md
5. 检查权限配置 → security-three-authority.md
6. 检查安全告警
```

## 安全提醒

1. 权限最小化：运维账户仅授予必要权限
2. 操作审计：所有运维操作记录审计日志
3. 变更窗口：高风险操作在维护窗口执行
4. 加密密钥管理：妥善管理 TDE 密钥

## 参考文档

```
kes-security/
├── SKILL.md                           # 本文件
├── ref/
│   ├── security-audit.md              # 审计配置
│   ├── security-auth.md               # 强认证+数据脱敏
│   ├── security-tde.md                # TDE 透明加密 + 应用层加密函数 + 防篡改
│   ├── security-label-mac.md          # MAC 标记访问控制
│   ├── security-national-crypto.md    # 国密证书认证(kcert)
│   ├── security-reuse.md              # 客体重用安全
│   ├── security-three-authority.md    # 三权分立
│   └── security-transport.md          # 安全传输(SSL/TLS)
└── test-cases.md
```
