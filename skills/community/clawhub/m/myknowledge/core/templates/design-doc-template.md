# {{project_name}} 设计文档

**版本**: {{version}}  
**创建日期**: {{created_at}}  
**最后更新**: {{updated_at}}

---

## 1. 架构设计

### 1.1 整体架构

{{architecture_overview}}

### 1.2 模块划分

| 模块 | 职责 | 关键类/函数 |
|------|------|-------------|
| {{module_name}} | {{module_responsibility}} | {{key_components}} |

---

## 2. 接口设计

### 2.1 对外接口

```python
class {{ClassName}}:
    def {{method_name}}(self, {{params}}) -> {{return_type}}:
        """{{method_description}}"""
        pass
```

### 2.2 内部接口

{{internal_interfaces}}

---

## 3. 数据模型

### 3.1 核心数据结构

{{data_structures}}

### 3.2 状态流转

{{state_transitions}}

---

## 4. 错误处理

| 错误类型 | 处理方式 | 返回信息 |
|----------|----------|----------|
| {{error_type}} | {{handling_strategy}} | {{error_message}} |

---

## 5. 依赖关系

### 5.1 依赖项

| 依赖 | 用途 | 版本要求 |
|------|------|----------|
| {{dependency}} | {{usage}} | {{version}} |

### 5.2 被依赖项

{{dependents}}

---

## 6. 设计决策记录

| 日期 | 决策 | 原因 | 替代方案 |
|------|------|------|----------|
| {{date}} | {{decision}} | {{reason}} | {{alternatives}} |

---

## 7. 待解决问题

- [ ] {{pending_issue}}

---

## 附录

### A. 参考文档

{{references}}

### B. 术语表

| 术语 | 定义 |
|------|------|
| {{term}} | {{definition}} |

---

## 填写范例

> 以下范例来自一个实际的"用户认证模块"设计文档。

```markdown
# 用户认证模块 设计文档

**版本**: 1.0
**创建日期**: 2026-06-10
**最后更新**: 2026-06-12

---

## 1. 架构设计

### 1.1 整体架构

采用 JWT + Refresh Token 双令牌方案：
- 客户端 → Nginx → Auth Service → Redis（Token 存储）
- 客户端 → Nginx → Auth Service → PostgreSQL（用户数据）
- 会话管理：Access Token（15min）+ Refresh Token（7d）

### 1.2 模块划分

| 模块 | 职责 | 关键类/函数 |
|------|------|-------------|
| AuthController | 登录/注册/登出 API | `login()`, `register()`, `logout()` |
| TokenService | JWT 生成与验证 | `generateToken()`, `verifyToken()`, `refreshToken()` |
| UserRepository | 用户数据访问层 | `findByEmail()`, `createUser()` |
| PasswordHasher | 密码哈希与验证 | `hash()`, `verify()` |

---

## 2. 接口设计

### 2.1 对外接口

```python
class AuthController:
    def login(self, email: str, password: str) -> TokenPair:
        """用户登录，返回 Access Token + Refresh Token"""
        pass

    def register(self, email: str, password: str, name: str) -> User:
        """新用户注册，返回用户信息"""
        pass

    def refresh(self, refresh_token: str) -> TokenPair:
        """用 Refresh Token 刷新 Access Token"""
        pass
```

### 2.2 内部接口

- `TokenService.verify(access_token)` → 供中间件调用
- `UserRepository.findByEmail(email)` → 供 AuthController 调用

---

## 3. 数据模型

### 3.1 核心数据结构

```python
class User:
    id: UUID
    email: str          # 唯一索引
    password_hash: str  # bcrypt，cost=12
    name: str
    created_at: datetime
    updated_at: datetime

class TokenPair:
    access_token: str   # JWT, 15min
    refresh_token: str  # UUID, 7d, 存 Redis
```

### 3.2 状态流转

```
用户状态：
  Active → Suspended（管理员操作）
  Active → Deleted（用户主动注销，30 天后硬删除）
```

---

## 4. 错误处理

| 错误类型 | 处理方式 | 返回信息 |
|----------|----------|----------|
| 邮箱已注册 | 409 Conflict | "该邮箱已被注册" |
| 密码错误 | 401 Unauthorized | "邮箱或密码错误" |
| Token 过期 | 401 Unauthorized | "登录已过期，请重新登录" |
| Token 无效 | 401 Unauthorized | "无效的认证信息" |
| 用户不存在 | 404 Not Found | "用户不存在" |

---

## 5. 依赖关系

### 5.1 依赖项

| 依赖 | 用途 | 版本要求 |
|------|------|----------|
| PyJWT | JWT 生成与解析 | >=2.8 |
| bcrypt | 密码哈希 | >=4.0 |
| redis-py | Redis 客户端 | >=5.0 |
| SQLAlchemy | ORM | >=2.0 |

### 5.2 被依赖项

- 所有需要认证的 API 模块（通过中间件）

---

## 6. 设计决策记录

| 日期 | 决策 | 原因 | 替代方案 |
|------|------|------|----------|
| 06-10 | JWT 而非 Session | 无状态，易扩展 | Session + Redis（需额外查库） |
| 06-10 | bcrypt cost=12 | 安全与性能平衡 | cost=10（不够安全）、cost=14（太慢） |
| 06-11 | Access Token 15min | 减少泄露风险 | 30min（泄露窗口大）、5min（频繁刷新） |

---

## 7. 待解决问题

- [ ] 是否需要支持 OAuth2（Google/GitHub 登录）？
- [ ] 密码重置流程的邮件服务选型
- [ ] 是否需要设备指纹（多设备登录检测）

---

## 附录

### A. 参考文档

- [JWT RFC 7519](https://datatracker.ietf.org/doc/html/rfc7519)
- [OWASP 认证最佳实践](https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html)

### B. 术语表

| 术语 | 定义 |
|------|------|
| JWT | JSON Web Token，无状态认证令牌 |
| Access Token | 短期令牌（15min），用于 API 请求认证 |
| Refresh Token | 长期令牌（7d），用于刷新 Access Token |
| bcrypt | 基于 Blowfish 的密码哈希算法 |
```
