# PigX 技术指南概述

> 适配 5.0 以上单体和微服务版本 | 版本 V5.11

## 关于 PIG 商业版

PIG 商业版是一款久经市场验证的企业级微服务开发平台，深度融合微服务、容器、DevOps 等云原生技术，为企业提供开箱即用的一站式数字化解决方案。

### 商业版核心价值

- **降本增效**：提供丰富的开箱即用企业级功能模块，支持灵活配置与二次开发
- **快速交付**：基于 Spring Cloud 2025 的成熟微服务框架，配合低代码生成器
- **专业保障**：提供企业级安全加固、性能优化、技术支持，8000+ 工单经验保驾护航

## 后端技术栈

| 分类 | 内容 |
|------|------|
| 编程语言 | Java 8(EOF)、**Java 17/21/25** |
| 开发框架 | Spring Boot 2.7(EOF)、**3.5** |
| 微服务框架 | Spring Cloud 2021(EOF)、**2025** \| Spring Cloud Alibaba **2025** |
| 安全框架 | Spring Authorization Server |
| 任务调度 | Quartz、XXL-JOB |
| 数据库支持 | **MySQL8**、Oracle 12C+、SQL Server 2017+、PostgreSQL 16+、达梦8、TiDB 4 |
| 持久层框架 | MyBatis & MyBatis Plus |
| 数据库连接池 | Druid |
| 服务注册与发现 | Nacos |
| 客户端负载均衡 | Spring Cloud Loadbalancer |
| 熔断组件 | Sentinel |
| 网关组件 | Spring Cloud Gateway |
| 日志管理 | Logback |
| 运行容器 | Undertow |
| 分布式事务 | Seata |
| 工作流 | Flowable 7 |

## 前端技术栈

- Vue 3.5 + TypeScript + TailwindCSS
- Element Plus UI 组件库
- Pinia 状态管理
- Vue Router 路由

## 模块结构说明

| 模块 | 说明 | 端口 |
|------|------|------|
| pigx-ui | 前端工程 | 8080 |
| pigx-boot | 单体模式启动器 | 9999 |
| pigx-auth | 授权服务提供 | 3000 |
| pigx-app-server | 移动端服务 | 7060 |
| pigx-common | 系统公共模块 | - |
| pigx-register | 注册中心、配置中心 | 8848 |
| pigx-flow | Flowable 工作流引擎 | - |
| pigx-gateway | Spring Cloud Gateway 网关 | 9999 |
| pigx-upms | 通用用户权限管理模块 | - |
| pigx-visual | 图形化模块 | - |

## 认证授权实现

采用 Spring Authorization Server 实现 OAuth 2.0 认证授权：

- 支持多种认证方式：用户名密码、短信验证码、社交账号
- 细粒度的权限控制：基于 RBAC 模型
- 全方位的安全防护：防 XSS 攻击、SQL 注入、CSRF 攻击
- 分布式 Token 管理：天生支持多节点部署
- 密码安全存储：BCrypt 加密

## 权限管理实现

基于角色的访问控制方法（RBAC）：

- 多租户用户、角色、部门、权限管理
- 简化权限管理
- 减少权限赋予错误
- 提高系统安全性
- 支持扩展性

## 多租户实现

通过重写 MyBatis-Plus 多租户插件和 Spring Data Redis 模块实现：

- 数据库数据隔离
- 缓存数据隔离
- 开发过程无感知

## 低代码生成模块

### 微服务构建器

使用 PIGX Maven Archetype 快速搭建业务微服务：

```bash
mvn archetype:generate \
  -DgroupId=com.pig4cloud \
  -DartifactId=demo \
  -Dversion=5.11.0 \
  -Dpackage=com.pig4cloud.pigx.demo \
  -DarchetypeGroupId=com.pig4cloud.archetype \
  -DarchetypeArtifactId=pigx-gen \
  -DarchetypeVersion=5.11.0 \
  -DarchetypeCatalog=local
```

### 代码生成器

- 高度自定义：支持多种数据库类型
- 灵活的代码生成方式：直接写入 IDE 或导出 zip
- 即时预览：生成代码前查看效果

## 前端能力

### 可定制工作台

- 高度可定制性：拖拽式布局设计
- 多端适配：PC、平板、手机
- 组件丰富：数十种常用组件

### 深色外观支持

- Dark Mode 深色调优化
- 降低视觉疲劳

### 国际化支持

- 全面语言支持：中文、英文
- 灵活配置方式
- 动态语言切换

## 协同办公工作流

基于 Flowable 7 工作流引擎：

- 拖拽式流程设计器
- 可视化表单构建器
- 支持条件分支、并行审批、会签加签、自动催办

## 消息推送模块

- 统一接口
- 多渠道支持：短信、邮件、站内通知、WebHook
- 灵活配置
- 扩展性强

## 分布式任务调度

支持 Quartz、XXL-JOB 实现分布式定时任务管理。