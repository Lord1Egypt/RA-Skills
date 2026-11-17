---
name: kes-security
description: KingbaseES 安全合规 — 测试用例
---

# KingbaseES 安全合规测试用例

## 测试用例 1: 三权分立配置

**场景**：等保合规要求实现三权分立

**输入问题**："金仓数据库怎么配置三权分立？"

**期望答案要点**：
- System Manager (系统管理员) — 负责系统管理
- Security Officer (安全官) — 负责安全策略
- Audit Officer (审计官) — 负责审计审查
- 受限 DBA 权限分配
- 参考 `ref/security-three-authority.md`

**验证方法**：答案包含三角色定义和权限分离

---

## 测试用例 2: 国密算法配置

**场景**：需要使用国密算法进行安全传输

**输入问题**："金仓数据库怎么用 SM2/SM3/SM4 国密算法？"

**期望答案要点**：
- SM2 证书认证配置 (`kcert` 系列工具)
- SM3 哈希算法使用
- SM4 对称加密配置
- 国密 SSL/TLS 传输配置
- 参考 `ref/security-national-crypto.md` 和 `ref/security-transport.md`

**验证方法**：答案包含 SM2/SM3/SM4 的配置方法

---

## 测试用例 3: TDE 透明数据加密

**场景**：敏感数据需要磁盘级加密

**输入问题**："金仓数据库怎么开启透明数据加密？"

**期望答案要点**：
- TDE 密钥管理配置
- 表空间加密启用
- 加密后的备份恢复注意事项
- 参考 `ref/security-encryption.md`

**验证方法**：答案包含 TDE 配置流程和密钥管理
