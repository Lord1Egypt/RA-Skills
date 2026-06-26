# 男装电商系统生成技能

## 技能概述

本技能用于生成完整的男装电商系统项目，采用现代化的技术栈：
- **后端**: SpringBoot3 + MyBatis Plus + Spring Security + JWT
- **前端**: Vue3 + Element Plus + Pinia + Vue Router
- **数据库**: MySQL 8.x
- **构建工具**: Maven + Vite

## 技能特点

1. **完整的电商功能**: 包含用户管理、商品管理、购物车、订单管理、支付集成等核心功能
2. **现代化架构**: 采用前后端分离架构，RESTful API设计
3. **企业级规范**: 代码符合企业级开发规范，包含完整的异常处理、日志记录、安全防护
4. **可扩展性**: 模块化设计，易于扩展和维护
5. **详细文档**: 提供完整的技术文档和API文档

## 使用流程

### 第一阶段：技术方案设计
1. 需求分析与确认
2. 技术架构设计
3. 数据库设计
4. API接口设计
5. 输出详细技术方案文档

### 第二阶段：代码生成
1. 后端项目初始化
2. 数据库实现
3. 核心模块开发
4. 前端项目开发
5. 系统集成与测试

## 项目结构

```
mens-fashion-ecommerce/
├── mens-fashion-ecommerce-backend/     # 后端项目
│   ├── src/main/java/com/mensfashion/ecommerce/
│   │   ├── config/                    # 配置类
│   │   ├── controller/                # 控制器层
│   │   ├── service/                   # 服务层
│   │   ├── mapper/                    # 数据访问层
│   │   ├── entity/                    # 实体类
│   │   ├── dto/                       # 数据传输对象
│   │   ├── vo/                        # 视图对象
│   │   ├── enums/                     # 枚举类
│   │   ├── exception/                 # 异常处理
│   │   └── utils/                     # 工具类
│   └── src/main/resources/
│       ├── application.yml            # 配置文件
│       ├── mapper/                    # MyBatis映射文件
│       └── static/                    # 静态资源
├── mens-fashion-ecommerce-frontend/    # 前端项目
│   ├── src/
│   │   ├── api/                       # API接口
│   │   ├── assets/                    # 静态资源
│   │   ├── components/                # 组件
│   │   ├── composables/               # 组合式函数
│   │   ├── router/                    # 路由配置
│   │   ├── store/                     # 状态管理
│   │   ├── utils/                     # 工具函数
│   │   └── views/                     # 页面组件
│   ├── vite.config.js                 # Vite配置
│   └── package.json                   # 项目配置
├── docs/                              # 文档
│   ├── api/                          # API文档
│   ├── database/                     # 数据库文档
│   └── deployment/                   # 部署文档
├── scripts/                          # 脚本
│   ├── generate-project.sh           # 项目生成脚本
│   └── database/                     # 数据库脚本
└── references/                       # 参考文档
    ├── backend-architecture.md       # 后端架构
    ├── frontend-architecture.md      # 前端架构
    ├── database-schema.md            # 数据库设计
    └── api-specification.md          # API规范
```

## 核心功能模块

### 1. 用户管理模块
- 用户注册、登录、退出
- 个人信息管理
- 地址管理
- 安全设置

### 2. 商品管理模块
- 商品分类管理
- 商品列表、搜索、筛选
- 商品详情展示
- 商品评价管理

### 3. 购物车模块
- 添加商品到购物车
- 修改商品数量
- 选择/取消选择商品
- 批量操作

### 4. 订单管理模块
- 创建订单
- 订单列表查询
- 订单详情查看
- 订单状态管理（取消、确认收货等）

### 5. 支付模块
- 多种支付方式集成（支付宝、微信）
- 支付状态查询
- 支付回调处理

### 6. 库存管理模块
- 库存查询
- 库存预警
- 库存调整记录

### 7. 营销模块
- 优惠券管理
- 促销活动
- 会员体系

## 技术亮点

### 后端技术亮点
1. **Spring Security + JWT**: 完整的认证授权体系
2. **MyBatis Plus**: 简化数据库操作，提高开发效率
3. **Redis缓存**: 提升系统性能，缓存热点数据
4. **统一异常处理**: 全局异常处理，友好的错误提示
5. **API文档**: 集成Swagger，自动生成API文档

### 前端技术亮点
1. **Vue3 Composition API**: 现代化的组件开发方式
2. **Element Plus**: 丰富的UI组件库
3. **Pinia状态管理**: 轻量级的状态管理方案
4. **响应式设计**: 支持多端适配
5. **TypeScript支持**: 类型安全，提高代码质量

## 快速开始

### 环境要求
- JDK 17+
- Maven 3.8+
- Node.js 16+
- MySQL 8.x
- Redis 6.x（可选）

### 部署步骤

1. **克隆项目**
   ```bash
   git clone <项目地址>
   cd mens-fashion-ecommerce
   ```

2. **初始化数据库**
   ```bash
   mysql -u root -p < scripts/database/init.sql
   ```

3. **启动后端服务**
   ```bash
   cd mens-fashion-ecommerce-backend
   mvn spring-boot:run
   ```

4. **启动前端服务**
   ```bash
   cd mens-fashion-ecommerce-frontend
   npm install
   npm run dev
   ```

5. **访问系统**
   - 前端地址: http://localhost:3000
   - 后端API文档: http://localhost:8080/swagger-ui.html

## 配置说明

### 后端配置
主要配置文件：`src/main/resources/application.yml`
- 数据库连接配置
- Redis配置
- JWT配置
- 文件上传配置
- 跨域配置

### 前端配置
主要配置文件：
- `vite.config.js`: 构建配置
- `.env.*`: 环境变量配置
- `src/assets/styles/variables.scss`: 样式变量

## 开发指南

### 后端开发
1. 实体类开发：在`entity`包中定义数据库表对应的实体类
2. 数据访问层：在`mapper`包中定义数据访问接口
3. 业务逻辑层：在`service`包中实现业务逻辑
4. 控制层：在`controller`包中定义API接口

### 前端开发
1. API接口：在`src/api`目录中定义API调用
2. 页面组件：在`src/views`目录中开发页面组件
3. 公共组件：在`src/components`目录中开发可复用组件
4. 状态管理：在`src/store`目录中定义状态管理

## 测试

### 后端测试
```bash
cd mens-fashion-ecommerce-backend
mvn test
```

### 前端测试
```bash
cd mens-fashion-ecommerce-frontend
npm run test
```

## 部署

### 后端部署
1. 打包项目
   ```bash
   mvn clean package -DskipTests
   ```
2. 运行JAR包
   ```bash
   java -jar target/ecommerce-backend-1.0.0.jar
   ```

### 前端部署
1. 构建项目
   ```bash
   npm run build
   ```
2. 部署到Nginx或CDN

## 维护与支持

### 监控指标
- 系统性能监控
- 错误日志监控
- 业务指标监控

### 安全建议
1. 定期更新依赖包
2. 配置合适的防火墙规则
3. 启用HTTPS
4. 定期备份数据库

## 贡献指南

欢迎提交Issue和Pull Request来改进本项目。

## 许可证

本项目采用MIT许可证。

## 联系方式

如有问题或建议，请通过以下方式联系：
- Email: support@mensfashion.com
- GitHub Issues: <项目地址>/issues

---

**注意**: 本技能生成的代码仅供参考，生产环境部署前请进行充分测试和安全评估。