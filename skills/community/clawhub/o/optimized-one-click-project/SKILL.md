---
name: optimized-one-click-project
description: 全自动项目生成和启动器 - 生成完整的Spring Boot + Vue3项目，包含前后端完整代码（RBAC+业务实体）、数据库初始化、编译启动、自动浏览器打开。支持完整CRUD（列表、查询、新增、修改、删除、查看）、多条件查询、状态下拉枚举、Redis配置、Swagger文档，使用JSON配置文件自定义参数。
---

# 优化版一键项目生成器 v2.1

🚀 **前后端完整代码生成（RBAC+业务实体）· 完整CRUD功能 · 多条件查询 · 状态下拉枚举 · 数据库初始化 · 智能编译启动 · 自动浏览器打开**

---

## 🎯 **核心功能**

### 1️⃣ **完整代码生成**
根据JSON配置文件自动生成完整的项目代码：

#### **后端 (Spring Boot)**
- 📦 **RBAC权限系统** - SysUser、SysRole、SysPermission完整CRUD
- 📦 **业务实体系统** - 根据配置自动生成Entity、Mapper、Service、Controller
- 📦 **完整CRUD接口** - 列表查询、根据ID查询、新增、修改、删除
- 📦 **Redis支持** - 可选Redis缓存配置（RedisConfig、RedisUtil）
- 📦 **Swagger文档** - 可选API文档支持
- 📦 **application.yml** - 使用配置文件中的数据库/Redis参数

#### **前端 (Vue3)**
- 🎨 **RBAC管理页面** - 登录页、用户/角色/权限管理
- 🎨 **业务实体页面** - 根据配置自动生成管理页面
- 🎨 **完整CRUD功能** - 列表、查询、新增、编辑、删除、查看
- 🎨 **多条件查询** - 支持多个字段的条件组合查询
- 🎨 **状态下拉枚举** - 状态字段统一使用下拉选择框显示（启用/禁用）
- 🎨 **分页功能** - 支持分页展示和切换
- 🎨 **路由配置** - 含路由守卫、权限控制
- 🎨 **API封装** - Axios请求封装、接口文件
- 🎨 **Element Plus UI** - 完整的管理系统界面，含图标支持

### 2️⃣ **数据库初始化**
- 🗄️ **RBAC系统表** - 用户、角色、权限、关联表
- 🗄️ **业务实体表** - 根据实体配置自动生成
- 🗄️ **默认数据** - admin/123456、user/123456等
- 🗄️ **物理删除** - 不使用逻辑删除字段

### 3️⃣ **9步全自动流程**
从配置到上线，一键完成所有步骤。

---

## 📁 **项目结构**

```
project-name/
├── backend/                           # Spring Boot后端
│   ├── src/main/java/com/example/
│   │   ├── entity/                   # 实体类
│   │   │   ├── SysUser.java          # 用户实体 (RBAC)
│   │   │   ├── SysRole.java          # 角色实体 (RBAC)
│   │   │   ├── SysPermission.java    # 权限实体 (RBAC)
│   │   │   └── [业务实体].java        # 配置的业务实体
│   │   ├── mapper/                   # Mapper接口
│   │   ├── service/                  # Service层
│   │   ├── controller/               # Controller层
│   │   │   ├── SysUserController.java       # 用户管理API
│   │   │   ├── SysRoleController.java       # 角色管理API
│   │   │   ├── SysPermissionController.java # 权限管理API
│   │   │   ├── AuthController.java          # 登录认证API
│   │   │   └── [业务实体]Controller.java    # 业务实体API
│   │   ├── config/                   # 配置类
│   │   │   ├── RedisConfig.java      # Redis配置（可选）
│   │   │   └── SwaggerConfig.java    # Swagger配置（可选）
│   │   ├── util/                     # 工具类
│   │   │   └── RedisUtil.java        # Redis工具类（可选）
│   │   └── [Application].java        # 启动类
│   ├── src/main/resources/
│   │   ├── application.yml           # 配置文件（使用配置的参数）
│   │   └── db/init.sql               # 数据库初始化脚本
│   └── pom.xml                       # Maven配置（含Redis依赖）
├── frontend/                          # Vue3前端
│   ├── src/
│   │   ├── views/                    # 页面组件
│   │   │   ├── Login.vue             # 登录页面
│   │   │   ├── Layout.vue            # 布局组件
│   │   │   ├── UserManagement.vue    # 用户管理（含搜索、查看、CRUD）
│   │   │   ├── RoleManagement.vue    # 角色管理（含搜索、查看、CRUD）
│   │   │   ├── PermissionManagement.vue  # 权限管理（含搜索、查看、CRUD）
│   │   │   └── [业务实体]Management.vue  # 业务实体管理页面（含搜索、查看、CRUD）
│   │   ├── router/                   # 路由配置
│   │   ├── api/                      # API接口
│   │   │   ├── user.js               # 用户API（列表、查询、新增、修改、删除）
│   │   │   ├── role.js               # 角色API（列表、查询、新增、修改、删除）
│   │   │   ├── permission.js         # 权限API（列表、查询、新增、修改、删除）
│   │   │   └── [业务实体].js          # 业务实体API
│   │   ├── utils/                    # 工具函数
│   │   │   └── request.js            # Axios封装
│   │   ├── main.js
│   │   └── App.vue
│   ├── index.html
│   ├── vite.config.js                # 使用配置的服务器端口
│   └── package.json
└── config.json                       # 项目配置文件
```

---

## 🚀 **执行流程（9步）**

| 步骤 | 功能 | 说明 |
|-----|------|------|
| 1/9 | 验证环境 | Java/Maven/Node.js/NPM必需检测 |
| 2/9 | 生成项目代码 | 前后端完整代码生成（使用配置参数）|
| 3/9 | 检查端口占用 | 检测配置的端口（默认8080/5173）|
| 4/9 | 测试数据库连接 | 验证配置的MySQL连接 |
| 5/9 | 执行数据库初始化 | 创建表和初始数据 |
| 6/9 | 构建后端项目 | Maven编译打包 |
| 7/9 | 安装前端依赖 | NPM install |
| 8/9 | 启动后端服务 | 在新CMD窗口启动，使用配置端口 |
| 9/9 | 启动前端并打开浏览器 | 在新CMD窗口启动+自动打开 |

---

## 🎊 **使用方式**

### 📋 **OpenClaw命令**
```bash
使用 optimized-one-click-project 创建一个用户信息管理系统
```

### 🎯 **直接执行脚本**
```bash
python optimized-one-click-project\scripts\optimized-start-win.py config.json
```

---

## 📋 **配置文件说明**

### **完整配置示例**

```json
{
  "project_name": "user-info-system-v2",
  "description": "用户信息管理系统",
  "entities": [
    {
      "name": "UserInfo",
      "fields": [
        {"name": "userCode", "type": "String", "comment": "用户编码"},
        {"name": "username", "type": "String", "comment": "用户名"},
        {"name": "realName", "type": "String", "comment": "真实姓名"},
        {"name": "email", "type": "String", "comment": "邮箱"},
        {"name": "phone", "type": "String", "comment": "电话"}
      ]
    },
    {
      "name": "Department",
      "fields": [
        {"name": "deptCode", "type": "String", "comment": "部门编码"},
        {"name": "deptName", "type": "String", "comment": "部门名称"},
        {"name": "description", "type": "String", "comment": "描述"}
      ]
    }
  ],
  "database": {
    "host": "your_ip",
    "port": 3306,
    "name": "your_database_name",
    "user": "your_user",
    "password": "your_password"
  },
  "redis": {
    "enable": true,
    "host": "your_ip",
    "port": 6379,
    "password": "your_password"
  },
  "server": {
    "backend_port": 8080,
    "frontend_port": 5173
  },
  "enable_swagger": true
}
```

### **配置参数说明**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `project_name` | String | ✓ | 项目名称（英文，将作为包名）|
| `description` | String | | 项目描述 |
| `entities` | Array | | 业务实体列表 |
| `entities[].name` | String | ✓ | 实体类名 |
| `entities[].fields` | Array | ✓ | 字段列表 |
| `entities[].fields[].name` | String | ✓ | 字段名 |
| `entities[].fields[].type` | String | ✓ | 字段类型（String/Long/Integer）|
| `entities[].fields[].comment` | String | | 字段注释 |
| `database` | Object | ✓ | 数据库配置 |
| `database.host` | String | ✓ | 数据库主机地址 |
| `database.port` | Number | ✓ | 数据库端口（默认3306）|
| `database.name` | String | ✓ | 数据库名称 |
| `database.user` | String | ✓ | 数据库用户名 |
| `database.password` | String | ✓ | 数据库密码 |
| `redis` | Object | | Redis配置 |
| `redis.enable` | Boolean | | 是否启用Redis（默认false）|
| `redis.host` | String | | Redis主机地址 |
| `redis.port` | Number | | Redis端口（默认6379）|
| `redis.password` | String | | Redis密码 |
| `server` | Object | | 服务器配置 |
| `server.backend_port` | Number | | 后端端口（默认8080）|
| `server.frontend_port` | Number | | 前端端口（默认5173）|
| `enable_swagger` | Boolean | | 是否启用Swagger（默认true）|

---

## 🌐 **系统访问**

- **前端页面**: http://localhost:{frontend_port}
- **登录页面**: http://localhost:{frontend_port}/login
- **后端API**: http://localhost:{backend_port}/api
- **Swagger文档**: http://localhost:{backend_port}/api/swagger-ui.html
- **默认账号**: admin / 123456

---

## ⚙️ **后端API接口**

### RBAC接口
```
GET    /api/users          # 列表查询（分页）
GET    /api/users/{id}     # 根据ID查询（查看详情）
POST   /api/users          # 新增
PUT    /api/users/{id}     # 修改
DELETE /api/users/{id}     # 删除（物理删除）

GET    /api/roles          # 列表查询
GET    /api/roles/{id}     # 根据ID查询
POST   /api/roles          # 新增
PUT    /api/roles/{id}     # 修改
DELETE /api/roles/{id}     # 删除

GET    /api/permissions          # 列表查询
GET    /api/permissions/{id}     # 根据ID查询
POST   /api/permissions          # 新增
PUT    /api/permissions/{id}     # 修改
DELETE /api/permissions/{id}     # 删除

POST   /api/auth/login    # 登录
GET    /api/auth/info     # 获取当前用户信息
```

### 业务实体接口
```
GET    /api/{entities}          # 列表查询（分页）
GET    /api/{entities}/{id}     # 根据ID查询
POST   /api/{entities}          # 新增
PUT    /api/{entities}/{id}     # 修改
DELETE /api/{entities}/{id}     # 删除
```

---

## 🎨 **前端页面功能**

### 列表页功能
- ✅ **多条件查询** - 支持多个字段的条件组合查询（文本输入框、状态下拉框）
- ✅ **查询/重置按钮** - 执行查询或清空条件
- ✅ **数据表格** - 显示所有字段，支持状态标签显示
- ✅ **分页** - 支持分页展示、页码切换、每页数量调整
- ✅ **操作列** - 查看、编辑、删除按钮，带图标

### 对话框功能
- ✅ **查看对话框** - 使用Descriptions组件展示详情（只读）
- ✅ **新增/编辑对话框** - 表单输入，支持验证
- ✅ **状态下拉枚举** - 状态字段使用el-select下拉选择（启用/禁用）
- ✅ **表单验证** - 必填项验证

### 按钮功能
- ✅ **查询** - 根据关键词搜索
- ✅ **重置** - 清空搜索条件
- ✅ **新增** - 打开新增对话框
- ✅ **查看** - 查看详情
- ✅ **编辑** - 打开编辑对话框
- ✅ **删除** - 确认后删除

---

## 🗄️ **数据库设计**

### RBAC表结构
```sql
-- 用户表
CREATE TABLE sys_user (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    real_name VARCHAR(50),
    email VARCHAR(100),
    phone VARCHAR(20),
    avatar VARCHAR(255),
    status TINYINT DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 角色表
CREATE TABLE sys_role (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    role_code VARCHAR(50) NOT NULL UNIQUE,
    role_name VARCHAR(50) NOT NULL,
    description VARCHAR(255),
    status TINYINT DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 权限表
CREATE TABLE sys_permission (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    permission_code VARCHAR(100) NOT NULL UNIQUE,
    permission_name VARCHAR(50) NOT NULL,
    parent_id BIGINT DEFAULT 0,
    type VARCHAR(20) DEFAULT 'menu',
    path VARCHAR(255),
    method VARCHAR(20),
    icon VARCHAR(50),
    sort_order INT DEFAULT 0,
    status TINYINT DEFAULT 1,
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

### 业务实体表结构
- ✅ 自动根据 `entities` 配置生成
- ✅ 驼峰命名自动转下划线
- ✅ 含 `id`, `create_time`, `update_time` 字段
- ✅ 不含逻辑删除字段（物理删除）

---

## 🎉 **最新优化功能**

### v2.1 新增功能
| 优化项 | 说明 |
|--------|------|
| **多条件查询** | 前端业务页面增加条件查询区域，支持多个字段组合查询 |
| **状态下拉枚举** | 状态字段统一使用el-select下拉选择框显示（启用/禁用） |
| **分页优化** | 完整分页功能，支持页码切换和每页数量调整 |
| **查看详情** | 使用Descriptions组件优化详情展示 |
| **图标支持** | 按钮和菜单添加Element Plus图标 |
| **模板优化** | 提取公共Vue模板，代码结构更清晰 |

### v2.0 基础功能
| 功能 | 说明 |
|------|------|
| **查询功能** | 前端关键词搜索 |
| **查看功能** | 根据ID查询详情，对话框展示 |
| **完整CRUD** | 列表、查询、新增、修改、删除 |
| **前后端匹配** | API接口完全对应 |
| **物理删除** | 去掉逻辑删除字段 |
| **字段显示** | 表格显示所有字段 |
| **搜索表单** | 查询/重置按钮 |

---

## 📦 **技能信息**

- **名称**: optimized-one-click-project
- **版本**: v2.1
- **作者**: OpenClaw
- **更新时间**: 2026-03-20

**技能已安装完成，随时可以使用！** 🚀
