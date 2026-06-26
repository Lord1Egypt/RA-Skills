#!/usr/bin/env python3
"""
Token 消耗对比演示 — 展示 OpenViking L0/L1/L2 分层加载相比传统全量加载的 token 节省效果。

用法:
    python3 demo-token-compare.py <docs_directory>
    python3 demo-token-compare.py ./my-project-docs/

模拟场景: Agent 收到 "帮我写一个用户认证模块" 的自然语言开发需求。
对比传统全量塞入 prompt vs OpenViking 分层按需加载的 token 消耗差异。
"""

import glob
import json
import os
import sys
import time


def estimate_tokens(text: str) -> int:
    """粗略估算 token 数 — 中文按 1 token/字，英文按 4 字符/token"""
    if not text:
        return 0
    cn = sum(1 for c in text if "\u4e00" <= c <= "\u9fff")
    en = len(text) - cn
    return int(cn * 1.0 + en / 4.0)


def read_all_docs(directory: str) -> list[dict]:
    """读取目录下所有文档文件"""
    extensions = ("*.md", "*.txt", "*.py", "*.js", "*.ts", "*.json", "*.yaml", "*.yml", "*.html", "*.css")
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(directory, "**", ext), recursive=True))

    docs = []
    for f in sorted(set(files)):
        if os.path.isfile(f):
            try:
                with open(f, encoding="utf-8", errors="ignore") as fh:
                    content = fh.read()
                docs.append({"path": f, "content": content, "tokens": estimate_tokens(content)})
            except Exception:
                pass
    return docs


def simulate_l0_abstract(content: str) -> str:
    """模拟 L0 摘要 — 取首行或前 100 字符"""
    lines = content.strip().splitlines()
    first_meaningful = ""
    for line in lines:
        stripped = line.strip().lstrip("#").strip()
        if stripped and not stripped.startswith("---"):
            first_meaningful = stripped
            break
    return first_meaningful[:150] if first_meaningful else content[:150]


def simulate_l1_overview(content: str) -> str:
    """模拟 L1 概览 — 提取标题和首段，限制约 2000 字符"""
    lines = content.strip().splitlines()
    overview_parts = []
    total_chars = 0
    in_code_block = False

    for line in lines:
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        if line.startswith("#"):
            overview_parts.append(line)
            total_chars += len(line)
        elif line.strip() and total_chars < 2000:
            overview_parts.append(line)
            total_chars += len(line)

        if total_chars >= 2000:
            break

    return "\n".join(overview_parts)


def main():
    if len(sys.argv) < 2:
        print("用法: python3 demo-token-compare.py <docs_directory>")
        print()
        print("示例: python3 demo-token-compare.py ./my-project-docs/")
        print()
        print("如果没有文档目录，将使用内置演示数据。")
        use_demo = True
    else:
        use_demo = False

    print()
    print("═" * 60)
    print("  OpenViking 分层加载 Token 消耗对比演示")
    print("═" * 60)
    print()
    print("场景: Agent 收到自然语言需求 '帮我写一个用户认证模块'")
    print("对比: 传统全量加载 vs OpenViking L0/L1/L2 分层按需加载")
    print()

    if use_demo:
        docs = _generate_demo_docs()
        print(f"使用内置演示数据 ({len(docs)} 个模拟文档)")
    else:
        target_dir = sys.argv[1]
        if not os.path.isdir(target_dir):
            print(f"ERROR: 目录不存在: {target_dir}", file=sys.stderr)
            sys.exit(1)
        docs = read_all_docs(target_dir)
        print(f"扫描目录: {target_dir} ({len(docs)} 个文档)")

    if not docs:
        print("未找到文档文件")
        sys.exit(1)

    print()
    print("─" * 60)

    # === 方案 1: 传统全量加载 ===
    total_full_tokens = sum(d["tokens"] for d in docs)
    print(f"\n▸ 方案 1: 传统全量加载 (把所有文档塞进 prompt)")
    print(f"  文件数:    {len(docs)}")
    print(f"  总 Token:  {total_full_tokens:,}")
    print(f"  特点:      无差别加载，token 浪费严重")

    # === 方案 2: L0 扫描 ===
    l0_results = []
    for d in docs:
        abstract = simulate_l0_abstract(d["content"])
        l0_results.append({
            "path": d["path"],
            "abstract": abstract,
            "tokens": estimate_tokens(abstract),
            "full_tokens": d["tokens"],
        })

    total_l0_tokens = sum(r["tokens"] for r in l0_results)
    print(f"\n▸ 方案 2: OpenViking L0 扫描 (仅加载摘要)")
    print(f"  文件数:    {len(docs)}")
    print(f"  L0 Token:  {total_l0_tokens:,}")
    print(f"  节省:      {(1 - total_l0_tokens / max(total_full_tokens, 1)) * 100:.1f}%")
    print(f"  特点:      Agent 用 L0 摘要判断哪些资源相关")

    # === 方案 3: L0 + L1 按需 ===
    relevant_count = max(len(docs) // 3, 2)
    relevant_docs = sorted(l0_results, key=lambda x: x["full_tokens"], reverse=True)[:relevant_count]

    l1_tokens = 0
    for d in relevant_docs:
        full_doc = next((doc for doc in docs if doc["path"] == d["path"]), None)
        if full_doc:
            overview = simulate_l1_overview(full_doc["content"])
            l1_tokens += estimate_tokens(overview)

    total_l0_l1_tokens = total_l0_tokens + l1_tokens
    print(f"\n▸ 方案 3: OpenViking L0 + L1 (摘要 + 概览)")
    print(f"  L0 全部:   {total_l0_tokens:,} tokens ({len(docs)} 个文件)")
    print(f"  L1 选读:   {l1_tokens:,} tokens ({relevant_count} 个相关文件)")
    print(f"  合计:      {total_l0_l1_tokens:,}")
    print(f"  节省:      {(1 - total_l0_l1_tokens / max(total_full_tokens, 1)) * 100:.1f}%")
    print(f"  特点:      Agent 用 L1 概览理解架构，制定计划")

    # === 方案 4: L0 + L1 + L2 按需深读 ===
    deep_read_count = max(relevant_count // 2, 1)
    deep_docs = relevant_docs[:deep_read_count]
    l2_tokens = sum(d["full_tokens"] for d in deep_docs)

    total_layered = total_l0_tokens + l1_tokens + l2_tokens
    print(f"\n▸ 方案 4: OpenViking L0 + L1 + L2 (完整分层)")
    print(f"  L0 全部:   {total_l0_tokens:,} tokens ({len(docs)} 个文件)")
    print(f"  L1 选读:   {l1_tokens:,} tokens ({relevant_count} 个相关文件)")
    print(f"  L2 深读:   {l2_tokens:,} tokens ({deep_read_count} 个必要文件)")
    print(f"  合计:      {total_layered:,}")
    print(f"  节省:      {(1 - total_layered / max(total_full_tokens, 1)) * 100:.1f}%")
    print(f"  特点:      仅深读写代码必需的具体文件")

    # === 汇总 ===
    print()
    print("═" * 60)
    print("  对比汇总")
    print("═" * 60)
    print()
    print(f"  {'方案':<35} {'Token':>10}  {'节省':>8}")
    print(f"  {'─' * 35} {'─' * 10}  {'─' * 8}")
    print(f"  {'传统全量加载':<33} {total_full_tokens:>10,}  {'基准':>8}")
    print(f"  {'OpenViking L0 扫描':<33} {total_l0_tokens:>10,}  {(1 - total_l0_tokens / max(total_full_tokens, 1)) * 100:>7.1f}%")
    print(f"  {'OpenViking L0 + L1':<33} {total_l0_l1_tokens:>10,}  {(1 - total_l0_l1_tokens / max(total_full_tokens, 1)) * 100:>7.1f}%")
    print(f"  {'OpenViking L0 + L1 + L2 按需':<33} {total_layered:>10,}  {(1 - total_layered / max(total_full_tokens, 1)) * 100:>7.1f}%")
    print()

    if total_full_tokens > 0:
        ratio = total_layered / total_full_tokens
        print(f"  结论: OpenViking 分层加载消耗仅为全量加载的 {ratio * 100:.1f}%，")
        print(f"        节省 {(1 - ratio) * 100:.1f}% 的 token 开销。")
    print()

    # === 输出 JSON 报告 ===
    report = {
        "scenario": "自然语言开发 — 用户认证模块",
        "total_files": len(docs),
        "comparison": {
            "full_load": {"tokens": total_full_tokens, "description": "传统全量加载"},
            "l0_scan": {"tokens": total_l0_tokens, "saving_pct": round((1 - total_l0_tokens / max(total_full_tokens, 1)) * 100, 1)},
            "l0_l1": {"tokens": total_l0_l1_tokens, "relevant_files": relevant_count, "saving_pct": round((1 - total_l0_l1_tokens / max(total_full_tokens, 1)) * 100, 1)},
            "l0_l1_l2": {"tokens": total_layered, "deep_read_files": deep_read_count, "saving_pct": round((1 - total_layered / max(total_full_tokens, 1)) * 100, 1)},
        },
    }
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "token-report.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)
    print(f"  报告已保存: {report_path}")


def _generate_demo_docs() -> list[dict]:
    """生成内置演示数据 — 模拟一个中型项目的文档结构"""
    demo_files = {
        "docs/architecture.md": """# 项目架构

## 概述
本项目采用微服务架构，包含以下核心模块：
- 用户服务 (User Service)
- 认证服务 (Auth Service)
- 订单服务 (Order Service)
- 支付服务 (Payment Service)

## 技术栈
- 后端: Python FastAPI
- 数据库: PostgreSQL
- 缓存: Redis
- 消息队列: RabbitMQ

## 服务通信
服务间通过 gRPC 通信，外部 API 使用 RESTful 接口。
每个服务独立部署，通过 Kubernetes 编排管理。

## 数据流
1. 客户端请求 → API Gateway → 对应微服务
2. 微服务处理 → 数据库读写 → 响应返回
3. 异步任务 → 消息队列 → Worker 处理
""",
        "docs/auth/jwt-config.md": """# JWT 配置说明

## Token 结构
```json
{
  "sub": "user_id",
  "exp": 1234567890,
  "iat": 1234567890,
  "roles": ["admin", "user"],
  "permissions": ["read", "write"]
}
```

## 密钥管理
- 使用 RS256 算法
- 私钥存储在 Vault 中
- 公钥通过 JWKS 端点分发
- 密钥轮换周期: 90 天

## Token 生命周期
- Access Token: 15 分钟
- Refresh Token: 7 天
- 支持 Token 黑名单机制

## 配置项
```yaml
auth:
  jwt:
    algorithm: RS256
    access_token_expire: 900
    refresh_token_expire: 604800
    issuer: "auth-service"
    audience: "api-gateway"
```
""",
        "docs/auth/oauth2-flow.md": """# OAuth2 认证流程

## 支持的 Grant Types
1. Authorization Code (推荐)
2. Client Credentials (服务间调用)
3. Refresh Token

## Authorization Code 流程
1. 客户端重定向到授权端点
2. 用户登录并授权
3. 回调携带 authorization code
4. 客户端用 code 换取 token
5. 返回 access_token + refresh_token

## 第三方登录集成
- Google OAuth2
- GitHub OAuth
- WeChat OAuth (微信登录)

## 安全措施
- PKCE 扩展 (S256)
- State 参数防 CSRF
- Redirect URI 白名单
- Token 加密存储
""",
        "docs/auth/rbac.md": """# RBAC 权限模型

## 角色定义
| 角色 | 权限 | 说明 |
|------|------|------|
| super_admin | * | 超级管理员 |
| admin | user.*, order.read | 普通管理员 |
| user | self.*, order.create | 普通用户 |
| guest | public.read | 访客 |

## 权限检查中间件
```python
@require_permission("user.write")
async def update_user(user_id: str, data: UserUpdate):
    ...
```

## 数据库模型
- users: 用户表
- roles: 角色表
- permissions: 权限表
- user_roles: 用户-角色关联
- role_permissions: 角色-权限关联
""",
        "docs/api/endpoints.md": """# API 端点文档

## 用户管理
- POST /api/v1/users - 创建用户
- GET /api/v1/users/:id - 获取用户详情
- PUT /api/v1/users/:id - 更新用户
- DELETE /api/v1/users/:id - 删除用户
- GET /api/v1/users - 用户列表 (分页)

## 认证相关
- POST /api/v1/auth/login - 登录
- POST /api/v1/auth/logout - 登出
- POST /api/v1/auth/refresh - 刷新 Token
- POST /api/v1/auth/register - 注册
- POST /api/v1/auth/forgot-password - 忘记密码
- POST /api/v1/auth/reset-password - 重置密码

## 订单管理
- POST /api/v1/orders - 创建订单
- GET /api/v1/orders/:id - 订单详情
- GET /api/v1/orders - 订单列表
- PUT /api/v1/orders/:id/cancel - 取消订单

## 支付
- POST /api/v1/payments - 发起支付
- GET /api/v1/payments/:id - 支付状态
- POST /api/v1/payments/:id/callback - 支付回调

## 通用参数
- page: 页码 (默认 1)
- page_size: 每页数量 (默认 20, 最大 100)
- sort: 排序字段
- order: asc / desc
""",
        "docs/database/schema.md": """# 数据库 Schema

## users 表
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    nickname VARCHAR(100),
    avatar_url TEXT,
    status VARCHAR(20) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

## orders 表
```sql
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id),
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT NOW()
);
```

## payments 表
```sql
CREATE TABLE payments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    order_id UUID REFERENCES orders(id),
    amount DECIMAL(10,2) NOT NULL,
    method VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending',
    paid_at TIMESTAMP
);
```
""",
        "docs/deployment/docker.md": """# Docker 部署指南

## 构建镜像
```bash
docker build -t myapp:latest .
```

## Docker Compose
```yaml
version: '3.8'
services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://...
      - REDIS_URL=redis://redis:6379
    depends_on:
      - postgres
      - redis

  postgres:
    image: postgres:15
    volumes:
      - pgdata:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
```

## 环境变量
| 变量 | 必填 | 说明 |
|------|------|------|
| DATABASE_URL | Y | PostgreSQL 连接串 |
| REDIS_URL | Y | Redis 连接串 |
| JWT_SECRET | Y | JWT 签名密钥 |
| LOG_LEVEL | N | 日志级别，默认 INFO |
""",
        "docs/testing/guide.md": """# 测试指南

## 单元测试
```bash
pytest tests/unit/ -v
```

## 集成测试
```bash
pytest tests/integration/ -v --cov=app
```

## E2E 测试
```bash
pytest tests/e2e/ -v
```

## 覆盖率要求
- 核心模块: >= 80%
- 工具模块: >= 60%

## Mock 规范
- 外部 API 调用必须 mock
- 数据库使用 test fixtures
- 时间相关使用 freezegun
""",
        "src/auth/service.py": """# Auth Service 实现

from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.hash import bcrypt

from app.config import settings
from app.models import User
from app.database import get_db

class AuthService:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET
        self.algorithm = "RS256"
        self.access_expire = timedelta(minutes=15)
        self.refresh_expire = timedelta(days=7)

    async def authenticate(self, email: str, password: str) -> Optional[User]:
        db = get_db()
        user = await db.users.find_one({"email": email})
        if not user or not bcrypt.verify(password, user.password_hash):
            return None
        return user

    def create_access_token(self, user_id: str, roles: list) -> str:
        payload = {
            "sub": user_id,
            "roles": roles,
            "exp": datetime.utcnow() + self.access_expire,
            "iat": datetime.utcnow(),
            "type": "access"
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def create_refresh_token(self, user_id: str) -> str:
        payload = {
            "sub": user_id,
            "exp": datetime.utcnow() + self.refresh_expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def verify_token(self, token: str) -> dict:
        return jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
""",
        "src/auth/middleware.py": """# Auth Middleware

from functools import wraps
from fastapi import Request, HTTPException
from app.auth.service import AuthService

auth_service = AuthService()

def require_auth(func):
    @wraps(func)
    async def wrapper(request: Request, *args, **kwargs):
        token = request.headers.get("Authorization", "").replace("Bearer ", "")
        if not token:
            raise HTTPException(status_code=401, detail="Missing token")
        try:
            payload = auth_service.verify_token(token)
            request.state.user = payload
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")
        return await func(request, *args, **kwargs)
    return wrapper

def require_permission(permission: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            user = getattr(request.state, "user", None)
            if not user:
                raise HTTPException(status_code=401)
            roles = user.get("roles", [])
            if "super_admin" not in roles:
                # check specific permission
                pass
            return await func(request, *args, **kwargs)
        return wrapper
    return decorator
""",
    }

    docs = []
    for path, content in demo_files.items():
        docs.append({"path": path, "content": content, "tokens": estimate_tokens(content)})
    return docs


if __name__ == "__main__":
    main()
