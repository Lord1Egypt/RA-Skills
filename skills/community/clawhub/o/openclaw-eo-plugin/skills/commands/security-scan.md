# /security-scan - 安全扫描指令

## 功能
调度 Security 专家，对目标代码或系统进行安全漏洞扫描。

## 参数
```
/security-scan <目标> [options]

参数:
  <目标>        必填，扫描目标（路径、URL或系统描述）
  --scope <范围> 可选，扫描范围
                  值: quick | full | api | web | infra
                  默认: quick
  --standard <标准> 可选，合规标准
                      值: owasp | pci | hipaa | gdpr | custom
                      默认: owasp
```

## 执行流程

1. **解析目标** - 确定扫描范围和类型
2. **加载安全专家** - Security + 可选 AppSec/Penetration Tester
3. **执行扫描** - OWASP Top 10 + 业务逻辑审计
4. **生成报告** - 漏洞列表 + 风险评级 + 修复建议

## 输出格式

```markdown
# 🛡️ 安全扫描报告

## 📍 扫描目标
`https://api.example.com/v1`

## 🔍 发现漏洞

### 🔴 高危 (2项)
| # | 漏洞 | 位置 | CVSS |
|---|------|------|------|
| 1 | SQL Injection | /api/user?id=1 | 9.8 |
| 2 | 敏感数据泄露 | /api/config | 7.5 |

### 🟡 中危 (3项)
| # | 漏洞 | 位置 | CVSS |
|---|------|------|------|
| 3 | XSS 存储型 | /api/comment | 6.1 |
| 4 | CSRF Token 缺失 | 所有 POST | 5.3 |
| 5 | 弱密码策略 | /api/auth | 4.2 |

## 💡 修复建议

### SQL Injection (高危)
**问题**：用户输入直接拼接到 SQL 查询
```sql
-- 危险
SELECT * FROM users WHERE id = ' + userId + '

-- 安全：使用参数化查询
SELECT * FROM users WHERE id = @userId
```
