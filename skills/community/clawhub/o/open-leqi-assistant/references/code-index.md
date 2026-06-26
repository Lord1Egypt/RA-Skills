# 乐企项目代码位置索引

## 一、源码根目录

```
D:/leqi/open-leqi/
```

## 二、API模块 (open-leqi-api)

### 2.1 包根目录
```
D:/leqi/open-leqi/open-leqi-api/src/main/java/com/baiwang/platform/openleqi/
```

### 2.2 API层 (Feign Client)
```
D:/leqi/open-leqi/open-leqi-api/src/main/java/com/baiwang/platform/openleqi/api/
```

| 功能 | 文件路径 |
|------|----------|
| 发票主表Client | `D:/leqi/open-leqi/open-leqi-api/src/main/java/com/baiwang/platform/openleqi/api/LqInvoiceMainClient.java` |
| 发票明细Client | `D:/leqi/open-leqi/open-leqi-api/src/main/java/com/baiwang/platform/openleqi/api/LqInvoiceDetailClient.java` |
| 抵扣勾选Client | `D:/leqi/open-leqi/open-leqi-api/src/main/java/com/baiwang/platform/openleqi/api/LqWithholdDeductClient.java` |
| 退税勾选Client | `D:/leqi/open-leqi/open-leqi-api/src/main/java/com/baiwang/platform/openleqi/api/LqWarrantDeductClient.java` |

### 2.3 模型层
```
D:/leqi/open-leqi/open-leqi-api/src/main/java/com/baiwang/platform/openleqi/model/
```
- DTO定义
- 请求/响应模型

## 三、服务模块 (open-leqi-service)

### 3.1 包根目录
```
D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/
```

### 3.2 Web层 (Controller)
```
D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/web/
```

| 功能 | 文件路径 |
|------|----------|
| 发票主表 | `D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/web/LqInvoiceMainController.java` |
| 发票明细 | `D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/web/LqInvoiceDetailController.java` |
| 发票同步 | `D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/web/LqSyncController.java` |
| 抵扣勾选 | `D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/web/LqWithholdDeductController.java` |
| 退税勾选 | `D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/web/LqWarrantDeductController.java` |
| 统计结果 | `D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/web/LqStatResultController.java` |
| 农产品抵扣 | `D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/web/LqFarmInvoiceDeductWeightController.java` |
| 航空客票 | `D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/web/LqAviationElemController.java` |
| 铁路客票 | `D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/web/LqTrainElemController.java` |

### 3.3 Service层
```
D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/service/
├── LqInvoiceMainService.java
├── LqInvoiceDetailService.java
├── LqSyncService.java
├── LqWithholdDeductService.java
├── LqWarrantDeductService.java
├── LqStatResultService.java
└── impl/  # Service实现
```

### 3.4 DAO层
```
D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/dao/
├── entity/   # 实体类 (55个)
└── mapper/   # Mapper接口 (54个)
```

### 3.5 公共类
```
D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/common/
```
- 508个公共类
- 工具类、通用组件

### 3.6 配置类
```
D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/config/
```

### 3.7 定时任务
```
D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/job/
```

### 3.8 集成类
```
D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/intergration/
```

## 四、资源文件

```
D:/leqi/open-leqi/open-leqi-service/src/main/resources/com/baiwang/platform/openleqi/dao/mapper/
```
- 47个MyBatis XML映射文件

## 五、快速定位规则

### 按业务功能
| 业务功能 | Controller | Service | DAO Entity |
|----------|------------|---------|------------|
| 发票管理 | LqInvoiceMainController | LqInvoiceMainService | LqInvoiceMain |
| 发票同步 | LqSyncController | LqSyncService | LqSyncTask |
| 抵扣勾选 | LqWithholdDeductController | LqWithholdDeductService | LqInvoiceMain |
| 退税勾选 | LqWarrantDeductController | LqWarrantDeductService | LqInvoiceMain |
| 统计 | LqStatResultController | LqStatResultService | LqStatResult |
| 农产品 | LqFarmInvoiceDeductWeightController | LqFarmInvoiceDeductWeightService | - |

### 按技术层面
| 层面 | 路径模式 |
|------|----------|
| API Client | `open-leqi-api/.../api/*Client.java` |
| Web Controller | `open-leqi-service/.../web/*Controller.java` |
| Service | `open-leqi-service/.../service/*Service.java` |
| Service Impl | `open-leqi-service/.../service/impl/*ServiceImpl.java` |
| Entity | `open-leqi-service/.../dao/entity/*.java` |
| Mapper | `open-leqi-service/.../dao/mapper/*Mapper.java` |
| Mapper XML | `open-leqi-service/src/main/resources/com/.../dao/mapper/*.xml` |
