---
name: open-leqi-assistant
description: |
  乐企(open-leqi)项目分析与代码定位助手技能。当用户询问关于乐企发票系统、勾选能力、抵扣功能、用票接口等问题时触发。本技能提供项目架构理解、代码快速定位、业务流程分析和问题诊断建议。
---

# 乐企(open-leqi)项目分析助手

## 技能概述

本技能基于百望乐企数字开放平台项目，专注于帮助开发者快速理解项目架构、定位代码、解答业务问题。

## 项目结构

```
D:/leqi/open-leqi/
├── open-leqi-api/          # API模块 - Feign客户端定义
│   └── src/main/java/com/baiwang/platform/openleqi/
│       ├── api/            # 29个Feign Client接口
│       ├── model/          # 数据模型(163个)
│       └── farm/           # 农业相关API
│
├── open-leqi-service/      # 服务模块 - 核心业务实现
│   └── src/main/java/com/baiwang/platform/openleqi/
│       ├── web/            # 60个Controller控制器
│       ├── service/impl/   # 122个Service实现
│       ├── dao/            # 数据访问层(109个)
│       ├── common/        # 公共工具(508个)
│       ├── config/        # 配置类
│       ├── job/           # 定时任务(19个)
│       └── intergration/  # 外部集成(48个)
│
└── startup/               # 启动模块
```

## 核心业务模块

### 发票管理
| 模块 | Controller | Service | Client | 说明 |
|------|-----------|---------|--------|------|
| 发票主表 | `LqInvoiceMainController` | `LqInvoiceMainService` | `LqInvoiceMainClient` | 全电发票核心数据 |
| 发票明细 | `LqInvoiceDetailController` | `LqInvoiceDetailService` | `LqInvoiceDetailClient` | 发票商品明细 |
| 发票抵扣 | `LqInvoiceDeductController` | `LqInvoiceDeductService` | `LqInvoiceDeductClient` | 增值税抵扣勾选 |
| 发票作废 | - | `LqWarrantPoolService` | `LqWarrantSyncClient` | 发票作废管理 |

### 勾选能力
| 模块 | Controller | Service | 说明 |
|------|-----------|---------|------|
| 抵扣勾选 | `LqWithholdDeductController` | `LqWithholdDeductService` | 勾选用于抵扣 |
| 退税勾选 | `LqWarrantDeductController` | `LqWarrantDeductService` | 勾选用于退税 |
| 不抵扣勾选 | `LqNotdeductInitTaskController` | `LqNotdeductInitTaskService` | 不抵扣处理 |
| 农产品抵扣 | `LqFarmInvoiceDeductWeightController` | `LqFarmInvoiceDeductWeightService` | 农产品加计扣除 |

### 用票能力
| 模块 | Controller | Service | 说明 |
|------|-----------|---------|------|
| 实时用票 | `LqSyncController` | `LqSyncService` | 发票开具 |
| 下载发票 | `LqDownloadTaskController` | `LqDownloadTaskService` | 发票下载 |
| 发票池 | `LqInvoicePoolTaskController` | `LqInvoicePoolTaskService` | 发票池管理 |

## 代码定位规则

### 根据功能查询Controller
```java
// 发票相关: 搜索 "LqInvoice*Controller"
com.baiwang.platform.openleqi.web.LqInvoiceMainController
com.baiwang.platform.openleqi.web.LqInvoiceDetailController
com.baiwang.platform.openleqi.web.LqInvoiceDeductController

// 勾选相关: 搜索 "Lq*DeductController" 或 "Lq*WarrantController"
com.baiwang.platform.openleqi.web.LqWithholdDeductController
com.baiwang.platform.openleqi.web.LqWarrantDeductController
```

### 根据功能查询Service
```java
// 服务接口: com.baiwang.platform.openleqi.service.Lq*Service
// 服务实现: com.baiwang.platform.openleqi.service.impl.Lq*ServiceImpl
```

### 根据功能查询DAO
```java
// Entity: com.baiwang.platform.openleqi.dao.entity.Lq*
// Mapper: com.baiwang.platform.openleqi.dao.mapper.Lq*Mapper
```

## 常用业务场景

### 场景1: 查询发票信息
1. Controller: `LqInvoiceMainController` → `/web/lqInvoiceMain/queryPageList`
2. Service: `LqInvoiceMainService`
3. DAO: `LqInvoiceMainMapper`

### 场景2: 抵扣勾选处理
1. Controller: `LqWithholdDeductController` → 抵扣接口
2. Service: `LqWithholdDeductService`
3. 核心方法: `deduct()` / `undoDeduct()`

### 场景3: 发票开具
1. Controller: `LqSyncController`
2. Service: `LqSyncService.syncInvoice()`
3. 调用链: OFS系统 → 乐企 → 返回结果

## 项目规范

### Spring Boot规范
- 使用`@RequiredArgsConstructor`代替构造函数注入
- 使用Lombok简化代码
- 分层清晰: Controller → Service → DAO

### 命名规范
- Controller: `Lq{业务}Controller` (例: `LqInvoiceMainController`)
- Service: `Lq{业务}Service` (例: `LqInvoiceMainService`)
- Entity: `Lq{业务}` (例: `LqInvoiceMain`)
- Mapper: `Lq{业务}Mapper` (例: `LqInvoiceMainMapper`)

### API规范
- 使用Swagger `@Api` `@ApiOperation` 注解
- 使用`BWJsonResultDto`统一返回格式
- 使用`@Validated`进行参数校验

## 外部依赖

- **百望BOP SDK**: `com.baiwang.bop:baiwang-bopsdk:3.4.822`
- **父工程**: `com.baiwang.basictools:bw-spring-boot-starter-parent-security:2.7.196`
- **数据库**: MyBatis-Plus

## 快速查询

当用户提问时，按以下顺序响应:
1. **理解问题**: 识别用户询问的业务场景
2. **定位代码**: 根据上表找到对应的Controller/Service/DAO
3. **给出路径**: 提供完整的文件路径
4. **分析问题**: 简要说明代码逻辑
5. **建议方案**: 提供问题解决思路

## 参考文档

- `references/project-architecture.md` - 详细项目架构说明
- `references/business-flows.md` - 业务流程图说明
- `references/api-guide.md` - API接口文档索引
