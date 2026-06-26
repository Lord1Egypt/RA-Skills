# 乐企API接口指南

## 一、API模块说明

API模块位于 `D:/leqi/open-leqi/open-leqi-api/src/main/java/com/baiwang/platform/openleqi/api/`

### 1.1 Client接口列表 (29个)

| Client类 | 功能说明 |
|----------|----------|
| LqInvoiceMainClient | 发票主表接口 |
| LqInvoiceDetailClient | 发票明细接口 |
| LqInvoiceDeductClient | 发票抵扣接口 |
| LqInvoiceFileRecordClient | 发票文件记录接口 |
| LqInvoicePoolRecordClient | 发票池记录接口 |
| LqInvoicePoolTaskClient | 发票池任务接口 |
| LqInvoicePoolErrorMsgClient | 发票池错误消息接口 |
| LqNotdeductInitTaskClient | 不抵扣初始化任务接口 |
| LqStatResultClient | 统计结果接口 |
| LqSyncClient | 同步接口 |
| LqSyncTaskClient | 同步任务接口 |
| LqTaskClient | 任务接口 |
| LqTaxInfoClient | 税信息接口 |
| LqTaxPeriodClient | 税款属期接口 |
| LqDownReqRecordClient | 下载请求记录接口 |
| LqDownResRecordClient | 下载响应记录接口 |
| LqErrorRetryConfigClient | 错误重试配置接口 |
| LqWarrantAccountClient | 作废账户接口 |
| LqWarrantDeductClient | 作废抵扣接口 |
| LqWarrantDetailClient | 作废明细接口 |
| LqWarrantSyncClient | 作废同步接口 |
| LqWithholdDeductClient | 预扣抵扣接口 |
| LqAviationElemClient | 航空电子客票接口 |
| LqAviationElemDetailClient | 航空电子客票明细接口 |
| LqTrainElemClient | 铁路电子客票接口 |
| LqUsedCarDetailClient | 二手车明细接口 |
| LqVehicleDetailClient | 车辆明细接口 |
| LqFarmAddDeductInvoiceSyncClient | 农产品加计扣除发票同步接口 |

## 二、Web层接口 (60个Controller)

### 2.1 发票管理类

| Controller | 路径前缀 | 主要功能 |
|------------|----------|----------|
| LqInvoiceMainController | /web/lqInvoiceMain | 发票主表CRUD |
| LqInvoiceDetailController | /web/lqInvoiceDetail | 发票明细管理 |
| LqInvoiceDeductController | /web/lqInvoiceDeduct | 发票抵扣管理 |
| LqInvoiceFileRecordController | /web/lqInvoiceFileRecord | 发票文件记录 |
| LqInvoicePoolRecordController | /web/lqInvoicePoolRecord | 发票池记录 |
| LqInvoicePoolTaskController | /web/lqInvoicePoolTask | 发票池任务 |
| LqInvoicePoolErrorMsgController | /web/lqInvoicePoolErrorMsg | 发票池错误 |
| LqInvoiceAccountController | /web/lqInvoiceAccount | 发票入账 |
| LqInvoiceConsumePoolController | /web/lqInvoiceConsumePool | 发票消费池 |
| LqInvoiceRepairController | /web/lqInvoiceRepair | 发票修复 |

### 2.2 同步类

| Controller | 路径前缀 | 主要功能 |
|------------|----------|----------|
| LqSyncController | /web/lqSync | 发票同步 |
| LqSyncTaskController | /web/lqSyncTask | 同步任务 |
| LqSyncTimestampRecordController | /web/lqSyncTimestampRecord | 同步时间戳 |

### 2.3 勾选类

| Controller | 路径前缀 | 主要功能 |
|------------|----------|----------|
| LqWithholdDeductController | /web/lqWithholdDeduct | 抵扣勾选 |
| LqWithholdSyncController | /web/lqWithholdSync | 抵扣同步 |
| LqWarrantDeductController | /web/lqWarrantDeduct | 退税勾选 |
| LqWarrantSyncController | /web/lqWarrantSync | 退税同步 |
| LqWarrantAccountController | /web/lqWarrantAccount | 退税账户 |
| LqWarrantDetailController | /web/lqWarrantDetail | 退税明细 |
| LqWarrantOilSyncController | /web/lqWarrantOilSync | 成品油退税 |
| LqNotdeductInitTaskController | /web/lqNotdeductInitTask | 不抵扣任务 |
| LqCurrentDeductRecordController | /web/lqCurrentDeductRecord | 当期抵扣记录 |
| LqCurrentDeductTaskController | /web/lqCurrentDeductTask | 当期抵扣任务 |
| LqOilInvoiceDeductController | /web/lqOilInvoiceDeduct | 成品油抵扣 |
| LqOilWarrantDeductController | /web/lqOilWarrantDeduct | 成品油退税 |

### 2.4 统计类

| Controller | 路径前缀 | 主要功能 |
|------------|----------|----------|
| LqStatResultController | /web/lqStatResult | 统计结果 |
| LqOilStatController | /web/lqOilStat | 成品油统计 |
| StatisticsController | /web/statistics | 统计 |

### 2.5 农产品类

| Controller | 路径前缀 | 主要功能 |
|------------|----------|----------|
| LqFarmInvoiceController | /web/lqFarmInvoice | 农产品发票 |
| LqFarmInvoiceSyncController | /web/lqFarmInvoiceSync | 农产品同步 |
| LqFarmInvoiceDeductWeightController | /web/lqFarmInvoiceDeductWeight | 农产品抵扣权重 |
| LqFarmAddDeductInvoiceSyncController | /web/lqFarmAddDeductInvoiceSync | 农产品加计扣除 |

### 2.6 交通运输类

| Controller | 路径前缀 | 主要功能 |
|------------|----------|----------|
| LqAviationElemController | /web/lqAviationElem | 航空电子客票 |
| LqAviationElemDetailController | /web/lqAviationElemDetail | 航空明细 |
| LqTrainElemController | /web/lqTrainElem | 铁路电子客票 |
| LqUsedCarDetailController | /web/lqUsedCarDetail | 二手车 |
| LqVehicleDetailController | /web/lqVehicleDetail | 车辆明细 |

### 2.7 任务类

| Controller | 路径前缀 | 主要功能 |
|------------|----------|----------|
| LqTaskController | /web/lqTask | 任务管理 |
| LqDownloadTaskController | /web/lqDownloadTask | 下载任务 |
| LqDownReqRecordController | /web/lqDownReqRecord | 下载请求 |
| LqDownResRecordController | /web/lqDownResRecord | 下载响应 |
| LqRetryOperateController | /web/lqRetryOperate | 重试操作 |
| LqErrorRetryConfigController | /web/lqErrorRetryConfig | 错误重试配置 |

### 2.8 其他

| Controller | 路径前缀 | 主要功能 |
|------------|----------|----------|
| LqTaxInfoController | /web/lqTaxInfo | 税信息 |
| LqTaxPeriodController | /web/lqTaxPeriod | 税款属期 |
| LqOilSyncController | /web/lqOilSync | 成品油同步 |
| LqOilTaxPeriodController | /web/lqOilTaxPeriod | 成品油属期 |
| LqCollectController | /web/lqCollect | 归集 |
| LqMessagePoolController | /web/lqMessagePool | 消息池 |
| LqInitializeStatusMonitorController | /web/lqInitializeStatusMonitor | 初始化状态监控 |

## 三、常用API调用示例

### 3.1 发票分页查询
```
POST /web/lqInvoiceMain/queryPageList
Request: LqInvoiceMainPageQueryDto
Response: BWJsonResultDto<PageData<LqInvoiceMainDto>>
```

### 3.2 发票同步
```
POST /web/lqSync/syncInvoice
Request: LqSyncRequestDto
Response: BWJsonResultDto<LqSyncResultDto>
```

### 3.3 抵扣勾选
```
POST /web/lqWithholdDeduct/deduct
Request: LqWithholdDeductDto
Response: BWJsonResultDto<Boolean>
```

## 四、错误码

错误码定义在 `com.baiwang.platform.openleqi.errorcodes` 包下。
