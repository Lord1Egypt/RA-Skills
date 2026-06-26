# 乐企业务流程序列

## 一、发票开具流程

### 1.1 全电发票开具
```
┌─────────┐    ┌──────────────┐    ┌────────────────┐    ┌─────────────┐    ┌──────────┐
│ 直连单位 │ → │ LqSyncController │ → │ LqSyncService   │ → │ OFS系统     │ → │ 乐企平台 │
└─────────┘    └──────────────┘    └────────────────┘    └─────────────┘    └──────────┘
     │                                                                              ↓
     │         ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
     └────────→│ LqInvoicePool  │ ← │ LqInvoiceMain  │ ← │ 数据库写入     │
               │ TaskService    │    │ Service        │    │ LqInvoiceMain  │
               └────────────────┘    └────────────────┘    └────────────────┘
```

### 1.2 核心代码路径
```
Controller: D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/web/LqSyncController.java
Service:   D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/service/LqSyncService.java
```

## 二、抵扣勾选流程

### 2.1 增值税抵扣勾选
```
┌─────────┐    ┌──────────────────────┐    ┌───────────────────────┐    ┌──────────────┐
│ 纳税人  │ → │ LqWithholdDeduct     │ → │ LqWithholdDeduct      │ → │ LqInvoiceMain│
│         │    │ Controller           │    │ Service               │    │ 更新状态     │
└─────────┘    └──────────────────────┘    └───────────────────────┘    └──────────────┘
                                                                                  ↓
     ┌────────────────┐    ┌────────────────┐    ┌────────────────┐
     │ LqStatResult   │ ← │ 统计计算        │ ← │ 勾选确认        │
     │ Service        │    │                │    │                │
     └────────────────┘    └────────────────┘    └────────────────┘
```

### 2.2 核心代码路径
```
Controller: D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/web/LqWithholdDeductController.java
Service:   D:/leqi/open-leqi/open-leqi-service/src/main/java/com/baiwang/platform/openleqi/service/LqWithholdDeductService.java
```

## 三、退税勾选流程

### 3.1 勾选用于退税
```
┌─────────┐    ┌────────────────────┐    ┌──────────────────────┐    ┌──────────────┐
│ 纳税人  │ → │ LqWarrantDeduct     │ → │ LqWarrantDeduct      │ → │ LqInvoiceMain│
│         │    │ Controller         │    │ Service              │    │ 更新状态     │
└─────────┘    └────────────────────┘    └──────────────────────┘    └──────────────┘
```

## 四、农产品抵扣流程

### 4.1 农产品加计扣除
```
┌─────────────┐    ┌────────────────────────────┐    ┌─────────────────────────────┐
│ 农产品发票  │ → │ LqFarmInvoiceDeductWeight   │ → │ 扣除金额计算                 │
│ 入账        │    │ Controller                │    │                             │
└─────────────┘    └────────────────────────────┘    └─────────────────────────────┘
```

## 五、发票作废流程

### 5.1 作废流程
```
┌─────────┐    ┌────────────────┐    ┌───────────────┐    ┌────────────────┐
│ 直连单位│ → │ LqWarrantSync   │ → │ LqWarrantPool │ → │ 发票状态变更   │
│         │    │ Controller     │    │ Service       │    │                │
└─────────┘    └────────────────┘    └───────────────┘    └────────────────┘
```

## 六、查询统计流程

### 6.1 统计结果查询
```
┌─────────┐    ┌──────────────────┐    ┌────────────────┐    ┌──────────────┐
│ 查询请求│ → │ LqStatResult     │ → │ LqStatResult   │ → │ 返回统计结果 │
│         │    │ Controller       │    │ Service        │    │              │
└─────────┘    └──────────────────┘    └────────────────┘    └──────────────┘
```

## 七、关键接口清单

| 接口 | Controller | 主要方法 | 说明 |
|------|------------|----------|------|
| 发票同步 | LqSyncController | syncInvoice() | 发票开具同步 |
| 发票查询 | LqInvoiceMainController | queryPageList() | 发票分页查询 |
| 抵扣勾选 | LqWithholdDeductController | deduct() | 抵扣勾选 |
| 撤销抵扣 | LqWithholdDeductController | undoDeduct() | 撤销抵扣 |
| 退税勾选 | LqWarrantDeductController | warrantDeduct() | 退税勾选 |
| 发票作废 | LqWarrantSyncController | warrant() | 发票作废 |
| 统计查询 | LqStatResultController | query() | 统计结果查询 |

## 八、数据流向总图

```
                    ┌─────────────────────────────────────────────────────────┐
                    │                    外部系统                              │
                    │  (电票平台/OFS/电子税务局)                               │
                    └───────────────────────┬─────────────────────────────────┘
                                            │
                                            ▼
                    ┌─────────────────────────────────────────────────────────┐
                    │              open-leqi-service                          │
                    │  ┌─────────────────────────────────────────────────────┐ │
                    │  │                   Web Layer (60 Controllers)       │ │
                    │  │   LqSyncController | LqInvoiceMainController ...   │ │
                    │  └─────────────────────────────────────────────────────┘ │
                    │                          │                              │
                    │                          ▼                              │
                    │  ┌─────────────────────────────────────────────────────┐ │
                    │  │               Service Layer (225 Services)          │ │
                    │  │   LqSyncService | LqInvoiceMainService ...          │ │
                    │  └─────────────────────────────────────────────────────┘ │
                    │                          │                              │
                    │                          ▼                              │
                    │  ┌─────────────────────────────────────────────────────┐ │
                    │  │                 DAO Layer (109 Mappers)             │ │
                    │  │   LqInvoiceMainMapper | LqSyncTaskMapper ...        │ │
                    │  └─────────────────────────────────────────────────────┘ │
                    └─────────────────────────────────────────────────────────┘
                                            │
                                            ▼
                    ┌─────────────────────────────────────────────────────────┐
                    │                      数据库                             │
                    │  lq_invoice_main | lq_invoice_detail | lq_stat_result   │
                    └─────────────────────────────────────────────────────────┘
```
