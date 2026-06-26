# 乐企项目详细架构说明

## 一、项目概述

**open-leqi** 是百望乐企数字开放平台的发票管理系统，基于Spring Boot 2.7.x架构。

### 技术栈
- Java 1.8
- Spring Boot 2.7.196
- MyBatis-Plus
- 百望BOP SDK 3.4.822
- Maven多模块项目

## 二、模块划分

### 2.1 open-leqi-api (API模块)

**职责**: 定义Feign客户端接口，供外部系统调用

**包结构**:
```
com.baiwang.platform.openleqi
├── api/           # 29个Feign Client
│   ├── LqInvoiceMainClient.java
│   ├── LqInvoiceDetailClient.java
│   ├── LqWithholdDeductClient.java
│   └── ... (其他业务Client)
├── model/         # 163个数据模型
│   ├── dto/       # 数据传输对象
│   ├── request/   # 请求模型
│   └── response/  # 响应模型
└── farm/          # 农业相关API
```

### 2.2 open-leqi-service (服务模块)

**职责**: 实现核心业务逻辑

**包结构**:
```
com.baiwang.platform.openleqi
├── web/           # 60个Controller
│   ├── LqInvoiceMainController.java
│   ├── LqSyncController.java
│   ├── LqWithholdDeductController.java
│   └── ...
├── service/       # 业务服务
│   ├── impl/      # 122个Service实现
│   ├── message/   # 消息处理
│   └── nativeAutoFrameWork/ # 自动化框架
├── dao/           # 数据访问
│   ├── entity/    # 55个实体类
│   └── mapper/    # 54个Mapper接口
├── common/        # 508个公共类
├── config/        # 配置类
├── job/           # 19个定时任务
├── intergration/  # 48个集成类
└── deserializer/  # 反序列化器
```

### 2.3 startup (启动模块)

**职责**: 项目启动入口，配置类加载

## 三、核心数据流

### 3.1 发票开具流程
```
外部系统 → LqSyncController
        → LqSyncService.syncInvoice()
        → OFSClient调用乐企接口
        → 发票池(LqInvoicePoolTask)
        → 发票主表(LqInvoiceMain)
```

### 3.2 抵扣勾选流程
```
用户勾选 → LqWithholdDeductController
        → LqWithholdDeductService.deduct()
        → 更新LqInvoiceMain状态
        → LqStatResult统计
```

### 3.3 数据同步流程
```
OFS系统 → LqSyncController
       → LqSyncService.processSync()
       → 各业务Service处理
       → DAO更新数据库
```

## 四、核心数据表

| 表名 | 说明 | Entity |
|------|------|--------|
| lq_invoice_main | 发票主表 | LqInvoiceMain |
| lq_invoice_detail | 发票明细 | LqInvoiceDetail |
| lq_warrant_pool | 作废池 | LqWarrantPool |
| lq_stat_result | 统计结果 | LqStatResult |
| lq_sync_task | 同步任务 | LqSyncTask |

## 五、定时任务

| 任务类 | 功能 | Cron |
|--------|------|------|
| LqSyncTaskJob | 发票同步 | - |
| LqPoolTaskJob | 发票池处理 | - |
| LqStatResultJob | 统计结果 | - |

## 六、配置说明

### 6.1 配置文件位置
```
open-leqi-service/src/main/resources/
├── com/baiwang/platform/openleqi/dao/mapper/  # MyBatis XML
└── application.yml (需配置)
```

### 6.2 主要配置
```yaml
spring:
  datasource:
    url: jdbc:mysql://...
  redis:
    host: ...
```

## 七、API网关

### 7.1 主要端点
```
POST /web/lqInvoiceMain/queryPageList    # 发票分页查询
POST /web/lqSync/invoiceSync             # 发票同步
POST /web/lqWithholdDeduct/deduct        # 抵扣勾选
```

### 7.2 返回格式
```java
BWJsonResultDto<T>
├── code: 状态码
├── message: 消息
├── data: 数据
└── timestamp: 时间戳
```

## 八、扩展能力

### 8.1 农业发票
- `LqFarmInvoiceSyncController` - 农产品发票同步
- `LqFarmInvoiceDeductWeightService` - 农产品抵扣权重

### 8.2 成品油
- `LqOilInvoiceDeductController` - 成品油抵扣
- `LqOilSyncController` - 成品油同步

### 8.3 航空运输
- `LqAviationElemController` - 航空电子客票
- `LqAviationElemDetailController` - 航空明细

### 8.4 铁路运输
- `LqTrainElemController` - 铁路电子客票

### 8.5 二手车/新车
- `LqUsedCarDetailController` - 二手车
- `LqVehicleDetailController` - 新车
