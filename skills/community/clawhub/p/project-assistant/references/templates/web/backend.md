# Web后端项目分析

分析Node.js、Python、Java等后端项目。

## 适用类型

- `nodejs` - Node.js后端 (Express/Koa/Fastify/NestJS)
- `django` - Django项目
- `fastapi` - FastAPI项目
- `flask` - Flask项目
- `spring` - Spring Boot项目
- `maven` - Maven项目
- `gradle-java` - Gradle Java项目

## 执行步骤

### 1. Node.js后端

解析 `package.json`:
```bash
python3 ~/.claude/tools/init/parsers/package_json_parser.py "$TARGET_DIR"
```

识别框架：
- `express` → Express
- `koa` → Koa
- `fastify` → Fastify
- `nest` → NestJS

目录结构：
```
src/
├── routes/        # 路由
├── controllers/   # 控制器
├── services/      # 业务逻辑
├── models/        # 数据模型
├── middleware/    # 中间件
└── config/        # 配置
```

### 2. Python后端

#### Django
解析 `settings.py`:
```bash
python3 ~/.claude/tools/init/parsers/django_parser.py "$TARGET_DIR"
```

提取：
- INSTALLED_APPS
- MIDDLEWARE
- DATABASES配置

#### FastAPI/Flask
解析主文件和requirements.txt:
```bash
python3 ~/.claude/tools/init/parsers/python_parser.py "$TARGET_DIR"
```

### 3. Java/Spring后端

解析 `pom.xml` 或 `build.gradle`:
```bash
python3 ~/.claude/tools/init/parsers/maven_parser.py "$TARGET_DIR"
```

提取：
- Spring Boot版本
- 依赖列表
- 构建配置

目录结构：
```
src/main/java/
├── controller/
├── service/
├── repository/
├── entity/
├── dto/
└── config/
```

### 4. 识别通用组件

数据库:
- MySQL, PostgreSQL, MongoDB, Redis, SQLite

ORM:
- Sequelize, TypeORM, Prisma (Node.js)
- SQLAlchemy, Django ORM (Python)
- MyBatis, JPA/Hibernate (Java)

认证:
- JWT, OAuth2, Session

API风格:
- REST, GraphQL, gRPC

### 5. 分析API端点

扫描路由文件，提取：
- 路由路径
- HTTP方法
- 处理函数

## 输出格式

```
项目初始化完成！

项目名称: {name}
项目类型: Web后端服务
主要语言: {JS/TS/Python/Java}
框架: {framework}
构建系统: {npm/pip/maven/gradle}

技术栈:
  - 数据库: {db}
  - ORM: {orm}
  - 认证: {auth}
  - API风格: {style}

API端点: {count} 个
核心功能: {count} 项

已生成项目文档: .claude/project.md
```