---
name: mens-fashion-ecommerce
description: 生成完整的男装电商系统项目，技术栈为 SpringBoot3 + Vue3 + MySQL。执行流程：先输出详细技术方案供用户确认，确认后再分模块生成完整的前后端代码。使用场景：当用户需要创建一个完整的男装电商平台，包括商品管理、用户管理、订单管理、购物车、支付集成等功能时使用此技能。
---

# 男装电商系统生成技能

本技能用于生成完整的男装电商系统项目，采用现代化的技术栈：SpringBoot3（后端）、Vue3（前端）、MySQL（数据库）。技能执行分为两个阶段：1) 输出详细技术方案供用户确认；2) 根据确认的方案分模块生成完整的前后端代码。

## 技能执行流程

### 第一阶段：技术方案设计

当技能触发时，首先执行以下步骤：

1. **需求分析**：与用户确认电商系统的核心功能需求
2. **技术架构设计**：设计系统整体架构，包括：
   - 后端架构（SpringBoot3 + MyBatis Plus + Spring Security）
   - 前端架构（Vue3 + Element Plus + Vue Router + Pinia）
   - 数据库设计（MySQL表结构）
   - API接口设计（RESTful API规范）
3. **模块划分**：将系统划分为以下核心模块：
   - 用户管理模块
   - 商品管理模块
   - 购物车模块
   - 订单管理模块
   - 支付模块
   - 库存管理模块
   - 物流跟踪模块
   - 营销活动模块
4. **输出技术方案文档**：生成详细的技术方案文档供用户确认

### 第二阶段：代码生成

用户确认技术方案后，按以下顺序生成代码：

1. **后端项目初始化**：
   - 创建SpringBoot3项目结构
   - 配置数据库连接和MyBatis Plus
   - 配置Spring Security和JWT认证
   - 配置Swagger API文档

2. **数据库设计实现**：
   - 生成MySQL建表SQL脚本
   - 创建实体类（Entity）
   - 创建数据访问层（Mapper）
   - 创建服务层（Service）

3. **核心模块开发**（按顺序）：
   - 用户管理模块（注册、登录、个人信息、地址管理）
   - 商品管理模块（商品分类、商品详情、商品搜索、商品评价）
   - 购物车模块（添加商品、修改数量、删除商品）
   - 订单管理模块（创建订单、订单列表、订单详情、订单状态）
   - 支付模块（支付接口、支付回调、退款处理）
   - 库存管理模块（库存查询、库存预警、库存调整）
   - 物流跟踪模块（物流查询、物流状态更新）
   - 营销活动模块（优惠券、限时折扣、满减活动）

4. **前端项目开发**：
   - 创建Vue3项目结构
   - 配置路由和状态管理
   - 集成Element Plus UI组件库
   - 开发各模块对应的页面组件
   - 实现API接口调用

5. **系统集成与测试**：
   - 前后端联调
   - 生成部署文档
   - 提供Docker部署配置

## 技术栈详情

### 后端技术栈
- **框架**：SpringBoot 3.x
- **ORM**：MyBatis Plus 3.x
- **安全**：Spring Security + JWT
- **数据库**：MySQL 8.x
- **缓存**：Redis（可选）
- **消息队列**：RabbitMQ（可选）
- **API文档**：SpringDoc OpenAPI 3 (Swagger)
- **构建工具**：Maven 3.8+

### 前端技术栈
- **框架**：Vue 3.x + Composition API
- **UI组件库**：Element Plus
- **状态管理**：Pinia
- **路由**：Vue Router 4.x
- **HTTP客户端**：Axios
- **构建工具**：Vite 5.x
- **CSS预处理器**：Sass/SCSS

### 数据库设计要点
1. **用户表**：用户基本信息、认证信息
2. **商品表**：商品分类、商品详情、商品SKU
3. **购物车表**：用户购物车商品
4. **订单表**：订单主表、订单明细表
5. **支付表**：支付记录、退款记录
6. **库存表**：商品库存、库存变更记录
7. **物流表**：物流信息、物流状态
8. **营销表**：优惠券、活动规则

## 参考文件

在生成代码时，可参考以下文件：

### 架构设计
- [references/backend-architecture.md](references/backend-architecture.md) - 后端架构详细设计（SpringBoot3 + MyBatis Plus + Spring Security）
- [references/frontend-architecture.md](references/frontend-architecture.md) - 前端架构详细设计（Vue3 + Element Plus + Pinia）
- [references/frontend-architecture-continued.md](references/frontend-architecture-continued.md) - 前端架构续篇（路由、组件、样式）

### 数据库设计
- [references/database-schema.md](references/database-schema.md) - 数据库表结构设计（核心表）
- [references/database-schema-continued.md](references/database-schema-continued.md) - 数据库设计续篇（索引、优化、维护）

### API设计
- [references/api-specification.md](references/api-specification.md) - API接口规范（认证、用户、商品）
- [references/api-specification-continued.md](references/api-specification-continued.md) - API规范续篇（购物车、订单、支付）

### 项目生成
- [scripts/generate-project.sh](scripts/generate-project.sh) - 项目生成脚本（后端部分）
- [scripts/generate-project-continued.sh](scripts/generate-project-continued.sh) - 项目生成脚本续篇（前端部分）
- [scripts/init.sh](scripts/init.sh) - 技能初始化脚本

### 项目文档
- [README.md](README.md) - 项目完整说明文档

## 使用说明

1. 当用户请求创建男装电商系统时，首先触发本技能
2. 按照第一阶段流程，与用户确认需求并输出技术方案
3. 获得用户确认后，按照第二阶段流程生成完整代码
4. 生成过程中，保持与用户的沟通，确保符合预期
5. 完成后提供部署和运行指南

## 代码生成指导原则

### 1. 后端代码生成
- 遵循SpringBoot最佳实践
- 使用MyBatis Plus简化数据库操作
- 实现统一的异常处理机制
- 添加完整的日志记录
- 配置合适的安全策略

### 2. 前端代码生成
- 使用Vue3 Composition API
- 遵循组件化开发原则
- 实现响应式设计
- 添加合适的错误处理
- 优化用户体验

### 3. 数据库设计
- 遵循数据库设计范式
- 添加合适的索引优化查询性能
- 考虑数据一致性和完整性
- 设计合理的表关系

### 4. API设计
- 遵循RESTful API设计原则
- 使用统一的响应格式
- 添加合适的错误码
- 提供完整的API文档

## 注意事项

1. 确保生成的代码符合企业级开发规范
2. 包含必要的错误处理和日志记录
3. 实现合适的安全措施（SQL注入防护、XSS防护等）
4. 提供完整的API文档
5. 考虑性能优化（数据库索引、缓存策略等）
6. 支持国际化（i18n）和响应式设计
7. 生成可维护、可扩展的代码结构
8. 提供清晰的代码注释和文档

## 技能输出示例

### 技术方案输出示例
```
# 男装电商系统技术方案

## 1. 项目概述
- 项目名称：男装电商系统
- 技术栈：SpringBoot3 + Vue3 + MySQL
- 目标用户：男性消费者
- 核心功能：商品浏览、购物车、订单管理、支付

## 2. 系统架构
- 前后端分离架构
- RESTful API设计
- 微服务架构（可选扩展）

## 3. 数据库设计
- 用户表：存储用户信息
- 商品表：存储商品信息
- 订单表：存储订单信息
- ...（详细表结构）

## 4. API设计
- 认证接口：/api/auth/*
- 用户接口：/api/users/*
- 商品接口：/api/products/*
- ...（详细接口文档）

## 5. 部署方案
- 开发环境：本地部署
- 生产环境：云服务器部署
- 数据库：MySQL 8.x
- 缓存：Redis
```

### 代码生成输出示例
```
项目结构：
mens-fashion-ecommerce/
├── backend/          # SpringBoot后端项目
├── frontend/         # Vue3前端项目
├── database/         # 数据库脚本
└── docs/            # 项目文档

已生成文件：
✓ backend/pom.xml
✓ backend/src/main/java/.../EcommerceApplication.java
✓ backend/src/main/resources/application.yml
✓ frontend/package.json
✓ frontend/vite.config.js
✓ frontend/src/main.js
✓ database/init.sql
✓ docs/README.md
```

## 技能维护

本技能应定期更新以保持技术栈的现代性：
1. 定期检查依赖版本更新
2. 更新最佳实践和设计模式
3. 添加新的功能模块
4. 优化现有代码结构
5. 更新文档和示例

## 故障排除

### 常见问题
1. **数据库连接失败**：检查MySQL服务是否启动，配置是否正确
2. **前端编译错误**：检查Node.js版本，清理npm缓存
3. **API调用失败**：检查后端服务是否启动，跨域配置是否正确
4. **文件上传失败**：检查文件大小限制，存储路径权限

### 解决方案
1. 查看日志文件定位问题
2. 检查配置文件是否正确
3. 验证依赖版本兼容性
4. 参考相关技术文档

## 扩展建议

### 功能扩展
1. **移动端适配**：开发响应式设计或独立移动端应用
2. **第三方登录**：集成微信、支付宝等第三方登录
3. **推荐系统**：基于用户行为的商品推荐
4. **数据分析**：用户行为分析和销售数据统计

### 技术扩展
1. **微服务架构**：将系统拆分为多个微服务
2. **容器化部署**：使用Docker和Kubernetes部署
3. **CI/CD流水线**：自动化测试和部署
4. **监控告警**：系统性能监控和异常告警

---

**技能版本**: 1.0.0  
**最后更新**: 2024年1月  
**适用场景**: 企业级电商系统开发、教学演示、个人项目实践