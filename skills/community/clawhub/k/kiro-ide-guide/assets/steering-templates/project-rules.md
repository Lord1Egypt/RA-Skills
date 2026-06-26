# 项目规则模板

将此文件保存为 `.kiro/steering/project-rules.md`

---

## 代码风格

### TypeScript
- 使用严格模式 (`strict: true`)
- 优先使用 `const` 而非 `let`
- 函数不超过 50 行
- 所有公共 API 必须有 JSDoc
- 使用 ES Module 语法 (`import`/`export`)

### 命名规范
- 文件：kebab-case (`user-auth.ts`)
- 类/组件：PascalCase (`UserProfile`)
- 函数/变量：camelCase (`getUserData`)
- 常量：UPPER_SNAKE_CASE (`MAX_RETRY_COUNT`)
- 类型：PascalCase (`UserProfile`)

### 文件组织
- 按功能模块组织，而非按类型
- 每个文件不超过 300 行
- 相关组件放在同一目录

```
✅ 推荐
src/
  auth/
    login.ts
    register.ts
    auth-context.tsx
    
❌ 避免
src/
  components/
  hooks/
  utils/
```

## 错误处理

### 原则
- 所有 async 函数必须用 try-catch 包裹
- 禁止吞掉错误而不记录日志
- API 错误必须返回标准格式

### 标准错误格式

```typescript
interface ApiError {
  error: {
    code: string;      // 机器可读错误码
    message: string;   // 用户可读消息
    details?: any;     // 可选的详细信息
  };
}

// 示例
throw {
  error: {
    code: 'AUTH_INVALID_CREDENTIALS',
    message: '邮箱或密码错误',
    details: { field: 'password' }
  }
};
```

### 日志记录

```typescript
import { logger } from '@/lib/logger';

try {
  await riskyOperation();
} catch (error) {
  logger.error('Operation failed', {
    error: error.message,
    context: { userId, operation: 'riskyOperation' }
  });
  throw error; // 重新抛出或转换为标准错误
}
```

## 测试规范

### 单元测试

```typescript
import { describe, it, expect } from 'vitest';
import { loginUser } from './auth';

describe('loginUser', () => {
  it('should return token for valid credentials', async () => {
    const result = await loginUser('test@example.com', 'password123');
    expect(result).toHaveProperty('token');
  });

  it('should throw error for invalid credentials', async () => {
    await expect(loginUser('wrong@email.com', 'wrong'))
      .rejects.toThrow('AUTH_INVALID_CREDENTIALS');
  });
});
```

### 测试覆盖要求
- 所有业务逻辑函数必须有单元测试
- 核心功能覆盖率 > 80%
- 边界条件必须测试

## 安全规范

### 认证授权
- 所有 API 端点必须验证用户身份
- 敏感操作需要额外权限检查
- JWT token 有效期不超过 24 小时

### 数据验证
- 所有用户输入必须验证
- 使用 Zod 或 Yup 进行 schema 验证
- SQL 查询必须使用参数化

```typescript
import { z } from 'zod';

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

// 使用
const validated = loginSchema.parse(request.body);
```

### 敏感信息
- 禁止在代码中硬编码密钥
- 使用环境变量管理敏感信息
- 密码必须加盐哈希 (bcrypt/argon2)

## 性能规范

### 数据库
- 所有查询必须有索引
- 避免 N+1 查询
- 大数据集使用分页

### API
- 响应时间 < 200ms (P95)
- 支持请求限流
- 大数据响应使用流式传输

### 前端
- 首屏加载 < 2 秒
- 图片使用懒加载
- 组件使用 React.memo 优化

## Git 规范

### 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式
- `refactor`: 重构
- `test`: 测试相关
- `chore`: 构建/工具

**示例:**
```
feat(auth): add Google OAuth login

- Implement OAuth2 flow
- Add Google provider configuration
- Update user model to support OAuth

Closes #123
```

### 分支策略
- `main`: 生产环境代码
- `staging`: 预发布环境
- `feature/*`: 功能开发
- `fix/*`: bug 修复
- `hotfix/*`: 紧急修复

## 项目特定规则

[在此添加项目特定的规则和约定]

### 技术栈
- 框架：Next.js 15
- 语言：TypeScript 5.x
- 样式：Tailwind CSS
- 数据库：Supabase (PostgreSQL)
- 部署：Vercel

### 目录结构
```
/
├── src/
│   ├── app/          # Next.js App Router
│   ├── components/   # React 组件
│   ├── lib/          # 工具函数
│   └── types/        # TypeScript 类型
├── .kiro/
│   ├── specs/        # Kiro 规格文档
│   └── steering/     # Kiro 规则文件
└── tests/            # 测试文件
```

---

*最后更新：2026-03-15*
