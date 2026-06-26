# 详细文件结构与命名规范

## 目录

- [Next.js 项目标准结构](#nextjs-项目标准结构)
- [Node.js 后端项目结构](#nodejs-后端项目结构)
- [React 组件库项目结构](#react-组件库项目结构)
- [命名规范](#命名规范)
- [Git 提交规范](#git-提交规范)

---

## Next.js 项目标准结构

### 完整目录树

```
project-name/
├── app/                              # App Router 目录
│   ├── (auth)/                       # 路由组 - 认证相关
│   │   ├── login/
│   │   │   └── page.tsx
│   │   └── register/
│   │       └── page.tsx
│   ├── (dashboard)/                  # 路由组 - 仪表板
│   │   ├── layout.tsx
│   │   └── page.tsx
│   ├── api/                          # API 路由
│   │   └── hello/
│   │       └── route.ts
│   ├── layout.tsx                    # 根布局
│   ├── page.tsx                      # 首页
│   └── globals.css                   # 全局样式
├── components/                       # 可复用组件
│   ├── ui/                           # 基础 UI 组件 (Button, Input, etc.)
│   │   ├── button.tsx
│   │   └── input.tsx
│   ├── layout/                       # 布局组件
│   │   ├── header.tsx
│   │   └── sidebar.tsx
│   └── features/                     # 业务组件
│       └── user-profile.tsx
├── lib/                             # 工具库
│   ├── utils/                        # 通用工具函数
│   │   └── format.ts
│   ├── hooks/                        # 自定义 Hooks
│   │   └── use-local-storage.ts
│   ├── types/                        # TypeScript 类型定义
│   │   └── index.ts
│   └── clients/                      # 第三方客户端
│       ├── supabase.ts
│       └── openai.ts
├── public/                           # 静态资源
│   ├── images/
│   ├── icons/
│   └── favicon.ico
├── styles/                           # 样式文件
│   └── theme.css
├── .env.example                      # 环境变量示例
├── .env.local                        # 本地环境变量 (gitignore)
├── .gitignore
├── package.json
├── pnpm-lock.yaml / package-lock.json
├── tsconfig.json
├── next.config.js
├── tailwind.config.js (可选)
├── README.md
└── *-init.sql                        # 数据库初始化SQL
```

### 文件命名规则

| 类型 | 命名规范 | 示例 |
|------|---------|------|
| 页面组件 | kebab-case + page.tsx | `user-profile/page.tsx` |
| UI 组件 | PascalCase | `Button.tsx`, `UserCard.tsx` |
| Hook 函数 | camelCase, use- 前缀 | `use-local-storage.ts` |
| 工具函数 | camelCase | `format-date.ts` |
| 类型定义 | PascalCase | `User.ts`, `ApiResponse.ts` |
| 配置文件 | dot notation | `.eslintrc.js`, `tailwind.config.js` |

---

## Node.js 后端项目结构

```
backend-project/
├── src/
│   ├── controllers/                  # 控制器层
│   │   └── user.controller.ts
│   ├── services/                     # 业务逻辑层
│   │   └── user.service.ts
│   ├── repositories/                 # 数据访问层
│   │   └── user.repository.ts
│   ├── routes/                       # 路由定义
│   │   └── user.routes.ts
│   ├── middleware/                   # 中间件
│   │   └── auth.middleware.ts
│   ├── models/                       # 数据模型
│   │   └── user.model.ts
│   ├── types/                        # 类型定义
│   │   └── index.ts
│   ├── utils/                        # 工具函数
│   │   └── validator.ts
│   ├── config/                       # 配置文件
│   │   └── database.ts
│   └── app.ts                        # 应用入口
├── tests/                            # 测试文件
│   └── user.test.ts
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
└── README.md
```

---

## React 组件库项目结构

```
component-library/
├── src/
│   ├── components/
│   │   ├── Button/
│   │   │   ├── Button.tsx
│   │   │   ├── Button.test.tsx
│   │   │   ├── Button.stories.tsx
│   │   │   └── index.ts
│   │   └── Input/
│   │       ├── Input.tsx
│   │       ├── Input.test.tsx
│   │       ├── Input.stories.tsx
│   │       └── index.ts
│   ├── hooks/
│   ├── utils/
│   ├── styles/
│   └── index.ts                      # 库入口
├── .env.example
├── .gitignore
├── package.json
├── tsconfig.json
├── vite.config.ts (可选)
└── README.md
```

---

## 命名规范

### 通用原则

1. **语义化** - 名称要能准确表达用途
2. **一致性** - 同一类事物用相同命名模式
3. **简洁性** - 不使用冗余词汇，不缩写到难以理解

### 文件命名

| 类型 | 规范 | 正确示例 | 错误示例 |
|------|------|---------|---------|
| React 组件 | PascalCase | `UserProfile.tsx` | `userProfile.tsx`, `user_profile.tsx` |
| 普通模块 | kebab-case | `auth-utils.ts` | `authUtils.ts`, `AuthUtils.ts` |
| Hook 文件 | kebab-case, use- 前缀 | `use-click-outside.ts` | `UseClickOutside.ts` |
| 类型定义 | PascalCase | `UserProfile.ts` | `user-profile.ts` |
| 配置文件 | dot notation | `.eslintrc.js` | `eslintrc.js` |
| 图片资源 | kebab-case | `hero-banner.png` | `HeroBanner.png` |

### 代码命名

| 类型 | 规范 | 正确示例 | 错误示例 |
|------|------|---------|---------|
| 类/组件 | PascalCase | `class UserService {}` | `class userService {}` |
| 函数/方法 | camelCase | `function getUser() {}` | `function GetUser() {}` |
| 变量 | camelCase | `const userName = 'xxx'` | `const UserName = 'xxx'` |
| 常量 | UPPER_SNAKE_CASE | `const MAX_RETRY = 3` | `const maxRetry = 3` |
| 接口/类型 | PascalCase | `interface User {}` | `interface user {}` |
| 枚举 | PascalCase | `enum Status {}` | `enum STATUS {}` |

### React 特有命名

| 类型 | 规范 | 示例 |
|------|------|------|
| 组件名 | PascalCase | `UserProfile`, `Button` |
| Props 接口 | `ComponentNameProps` | `UserProfileProps`, `ButtonProps` |
| Hook 函数 | camelCase, use 前缀 | `useLocalStorage`, `useDebounce` |
| 事件处理 | `handle` + 名词 + 动词 | `handleSubmitClick`, `handleInputChange` |

---

## Git 提交规范

### 提交信息格式

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Type 类型

| 类型 | 说明 |
|------|------|
| feat | 新功能 |
| fix | 修复 bug |
| docs | 文档更新 |
| style | 代码格式调整（不影响代码运行） |
| refactor | 重构（既不是新增功能，也不是修复 bug） |
| perf | 性能优化 |
| test | 增加测试 |
| chore | 构建过程或辅助工具的变动 |
| ci | CI/CD 相关变更 |

### 示例

```
feat(auth): add user registration flow

- Add registration form validation
- Add email verification
- Add password strength checker

Closes #123
```

```
fix(api): correct user profile response type

The profile endpoint was returning incorrect field names.
This fix aligns the response with the API specification.
```

---

## README 必须包含的内容

每个项目的 README.md 必须包含以下部分：

1. **项目介绍** - 一句话说明项目是做什么的
2. **功能特性** - 主要功能列表
3. **技术栈** - 使用的主要技术
4. **快速开始**
   - 环境要求
   - 安装步骤
   - 启动命令
5. **环境变量** - 所有需要配置的环境变量及说明
6. **项目结构** - 简要目录结构说明
7. **开发指南** - 如何添加新功能/组件
8. **部署说明** - 如何部署到生产环境
9. **License** - 开源协议

### README 模板

```markdown
# 项目名称

一句话项目介绍。

## ✨ 功能特性

- 功能 1
- 功能 2
- 功能 3

## 🛠️ 技术栈

- **前端框架**: Next.js 14
- **样式**: Tailwind CSS
- **数据库**: Supabase
- **语言**: TypeScript

## 🚀 快速开始

### 环境要求

- Node.js >= 18
- pnpm >= 8

### 安装

```bash
# 克隆项目
git clone https://github.com/username/repo.git

# 进入项目目录
cd repo

# 安装依赖
pnpm install
```

### 配置环境变量

```bash
cp .env.example .env.local
```

编辑 `.env.local` 填入以下配置：

| 变量名 | 说明 | 示例 |
|--------|------|------|
| DATABASE_URL | 数据库连接地址 | `postgresql://...` |
| API_KEY | API 密钥 | `sk-xxx` |

### 启动开发环境

```bash
pnpm dev
```

访问 http://localhost:3000

## 📁 项目结构

```
简要目录结构说明
```

## 📝 开发指南

### 添加新组件

1. 在 `components/features/` 创建组件
2. 遵循组件命名规范
3. 添加类型定义

### 提交代码

参考 [Git 提交规范](#git-提交规范)

## 🚢 部署

```bash
pnpm build
pnpm start
```

## 📄 License

MIT
```

---

*本规范基于 Harness Engineering 理念 + 企业级全AI研发实践制定*
