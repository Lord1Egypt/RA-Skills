---
name: gi-security-audit
description: Audit code for security issues - sensitive data exposure, dependency vulnerabilities, SQL injection, hardcoded secrets. Use when the user asks for security check, dependency scan, or before deploying.
tags: ["security", "audit", "vulnerability", "secrets", "dependency"]
---

# Security Audit 安全审计

对代码进行安全审计：敏感信息泄露、依赖漏洞、SQL 注入、硬编码密钥等。适用于上线前检查、第三方技能审计、定期安全扫描。

## 何时使用

- 用户请求「安全审计」「安全检查」「依赖扫描」
- 上线/发布前
- 引入第三方包或技能前
- 用户提到「敏感信息」「密钥」「漏洞」

## 审计清单

### 1. 敏感信息检测

**检查项**：
- 硬编码的 API Key、Secret、Token、密码
- 数据库连接串（含密码）
- 私钥、证书内容
- 邮箱、手机号等 PII 明文

**正确做法**：
```python
from tkms import get_env
env = get_env()
api_key = env.get('api_key')  # 从配置读取
```

**危险模式**（需替换）：
```python
API_KEY = "sk-xxx"           # 硬编码
password = "123456"          # 明文密码
db_url = "mysql://user:pwd@host"  # 连接串含密码
```

### 2. 依赖漏洞扫描

**执行**：
```bash
# Python 依赖
pip install safety
safety check

# 或使用 pip-audit
pip install pip-audit
pip-audit

# Node/npm 依赖
npm audit
```

**处理**：升级有漏洞的包到安全版本，或评估风险后决定是否接受。

### 3. SQL 注入

**危险**：字符串拼接 SQL
```python
# 错误
sql = f"SELECT * FROM user WHERE id = {user_id}"
```

**正确**：使用参数化查询
```python
# tkms AsyncSqlSessionTemplate
await session.query_list("SELECT * FROM user WHERE id = :id", {"id": user_id})
```

### 4. XSS 与注入

- 前端：避免 `v-html` 渲染用户输入，或先转义
- 后端：校验、过滤用户输入，避免拼接进命令/模板

### 5. 权限与认证

- 敏感接口是否有鉴权
- 是否有越权风险（如通过改 ID 访问他人数据）
- Token 存储与传输是否安全（HTTPS、HttpOnly）

### 6. 日志与错误信息

- 日志中不输出密码、Token
- 对外错误信息不暴露内部路径、堆栈

## 输出格式

```markdown
## 安全审计报告

### 高危
- [ ] 问题描述 + 位置 + 修复建议

### 中危
- [ ] ...

### 低危/建议
- [ ] ...

### 通过项
- [x] 敏感信息：已使用配置
- [x] SQL：已参数化
```

## 快速扫描命令

```bash
# 搜索可能的硬编码密钥
rg -i "password\s*=\s*['\"]|api_key\s*=\s*['\"]|secret\s*=\s*['\"]" --type py

# 搜索可能的 SQL 拼接
rg "f['\"].*SELECT|f['\"].*INSERT|f['\"].*UPDATE|f['\"].*DELETE" --type py
```
