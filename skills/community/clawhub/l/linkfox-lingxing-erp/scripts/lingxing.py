#!/usr/bin/env python3
"""
领星 OpenAPI CLI - 全模块查询接口

Usage:
    # 列出所有店铺（获取 SID）
    python3 lingxing.py --list-stores

    # 查询 SP 广告活动报表（SID 从环境变量自动注入）
    python3 lingxing.py --api spCampaignReports --params '{"report_date": "2024-01-01"}'

    # 自动翻页获取全部数据
    python3 lingxing.py --api spKeywordReports --params '{"report_date": "2024-01-01"}' --all

    # 查询产品列表
    python3 lingxing.py --api ProductLists --params '{"offset": 0, "length": 20}'

    # 查询利润报表
    python3 lingxing.py --api profitAsin --params '{"sids": "813", "start_date": "2024-01-01", "end_date": "2024-01-31"}'

    # 查询仓库列表
    python3 lingxing.py --api WarehouseLists --params '{"offset": 0, "length": 20}'

Environment:
    LINGXING_APP_ID     - 领星 AppID（必填）
    LINGXING_APP_SECRET - 领星 AppSecret（必填）
    LINGXING_SID        - 默认店铺 SID（选填；未在 --params 中指定 sid 时自动注入）
"""

import argparse
import base64
import hashlib
import json
import os
import sys
import time
import urllib.parse
from pathlib import Path
from typing import Optional

HOST = "https://openapi.lingxing.com"
TOKEN_CACHE_DIR = Path("/tmp")

# ─── API 路径映射 ────────────────────────────────────────────────────────────
# 默认路径: /pb/openapi/newad/<name>（仅适用于 newAd 系列接口）
# 所有非 newAd 接口必须在此注册

SPECIAL_PATHS = {
    # ── newAd 报表 - 特殊路径 ──
    "dspReportOrderList":           "/basicOpen/dspReport/order/list",
    "ProductAnalysisList":          "/basicOpen/adReport/productOrderAnalysis/list",
    # ── newAd 基础数据 - 特殊路径 ──
    "dspAccountList":               "/basicOpen/baseData/account/list",
    # ── newAd 报表下载 ──
    "abaReport":                    "/pb/openapi/newad/abaReport",

    # ── 基础数据 (BasicData) ──
    "AccoutLists":                  "/erp/sc/data/account/lists",
    "AllMarketplace":               "/erp/sc/data/seller/allMarketplace",
    "AttachmentDownload":           "/erp/sc/routing/common/file/download",
    "ConceptSellerLists":           "/erp/sc/data/seller/conceptLists",
    "Currency":                     "/erp/sc/routing/finance/currency/currencyMonth",
    "CustomAttachmentDownload":     "/erp/sc/routing/customized/file/download",
    "StateList":                    "/basicOpen/multiplatform/profit/report/stateList",
    "WorldStateLists":              "/erp/sc/data/worldState/lists",

    # ── 销售 (Sale) ──
    "mwsOrders":                    "/erp/sc/data/mws/orders",
    "mwsListing":                   "/erp/sc/data/mws/listing",
    "orderReturnInformation":       "/order/amzod/api/orderDetails/returnInformation",
    "scOrderSetRemark":             "/basicOpen/platformOrder/scOrder/setRemark",
    "OrderDetail":                  "/erp/sc/data/mws/orderDetail",
    "RefundOrder":                  "/basicOpen/openapi/salesOrder/refundOrder",
    "sale_ProductList":             "/listing/publish/openapi/amazon/product/list",
    "FBMOrderList":                 "/erp/sc/routing/order/Order/getOrderList",
    "FBMOrderDetail":               "/erp/sc/routing/order/Order/getOrderDetail",
    "MCFOrderList":                 "/order/amzod/api/orderList",
    "ProductInformation":           "/order/amzod/api/orderDetails/productInformation",
    "GetPrices":                    "/listing/listing/open/api/listing/getPrices",
    "LogisticsInformation":         "/order/amzod/api/orderDetails/logisticsInformation",
    "GetMerchantShippingGroup":     "/basicOpen/openapi/publish/manage/getMerchantShippingGroup",
    "GetFulfillmentResult":         "/pb/mp/order/getFulfillmentResult",
    "QueryProductList":             "/listing/publish/openapi/amazon/product/search",
    "PublishManageCategoryRoot":    "/basicOpen/openapi/publish/manage/categoryRoot",
    "PublishManageCategoryChildren": "/basicOpen/openapi/publish/manage/categoryChildren",
    "PublishManageGetProductType":  "/basicOpen/openapi/publish/manage/getProductType",
    "adjustPriceAdjustPriceManual": "/basicOpen/module/adjustPrice/AdjustPriceManual",
    "afterSaleList":                "/erp/sc/routing/amzod/order/afterSaleList",
    "fbaFeeDifferenceList":         "/basicOpen/openapi/sale/fbaFeeDifference/order/list",
    "fbaFeeDifferenceMskuList":     "/basicOpen/openapi/sale/fbaFeeDifference/msku/list",
    "globalTagPageList":            "/basicOpen/globalTag/listing/page/list",
    "listingOperateLogPageList":    "/basicOpen/listingManage/listingOperateLog/pageList",
    "promotionListingList":         "/basicOpen/promotion/listingList",
    "promotionListingDetailCoupon": "/basicOpen/promotion/listingDetailCoupon",
    "promotionListingDetailManage": "/basicOpen/promotion/listingDetailManage",
    "promotionListingDetailPrimeDiscount": "/basicOpen/promotion/listingDetailPrimeDiscount",
    "promotionListingDetailSecKill": "/basicOpen/promotion/listingDetailSecKill",
    "promotionalActivitiesCouponList": "/basicOpen/promotionalActivities/coupon/list",
    "promotionalActivitiesManageList": "/basicOpen/promotionalActivities/manage/list",
    "promotionalActivitiesSecKillList": "/basicOpen/promotionalActivities/secKill/list",
    "promotionalActivitiesVipDiscountList": "/basicOpen/promotionalActivities/vipDiscount/list",
    "queryListingRelationTagList":  "/basicOpen/listingManage/queryListingRelationTagList",
    "promotionCouponAllDetailBatch": "/promotionApi/open/promotion/couponAllDetailBatch",
    "promotionManagementAllDetailBatch": "/promotionApi/open/promotion/managementAllDetailBatch",
    "promotionPrimeDiscountAllDetailBatch": "/promotionApi/open/promotion/primeDiscountAllDetailBatch",
    "promotionSecKillAllDetailBatch": "/promotionApi/open/promotion/secKillAllDetailBatch",

    # ── 产品 (Product) ──
    "ProductLists":                 "/erp/sc/routing/data/local_inventory/productList",
    "ProductDetails":               "/erp/sc/routing/data/local_inventory/productInfo",
    "Brand":                        "/erp/sc/data/local_inventory/brand",
    "Category":                     "/erp/sc/routing/data/local_inventory/category",
    "UpcList":                      "/listing/publish/api/upc/upcList",
    "GetProductTag":                "/label/operation/v1/label/product/list",
    "GetPagingLogLists":            "/basicOpen/product/getPagingLogLists",
    "attributeList":                "/erp/sc/routing/storage/attribute/attributeList",
    "batchGetProductInfo":          "/erp/sc/routing/data/local_inventory/batchGetProductInfo",
    "bundledProductList":           "/erp/sc/routing/data/local_inventory/bundledProductList",
    "getTransparencyProductList":   "/basicOpen/product/getTransparencyProductList",
    "productAuxList":               "/erp/sc/routing/data/local_inventory/productAuxList",
    "spuInfo":                      "/erp/sc/routing/storage/spu/info",
    "spuList":                      "/erp/sc/routing/storage/spu/spuList",

    # ── 财务 (Finance) ──
    "profitAsin":                   "/erp/sc/routing/finance/ProfitState/profitAsin",
    "profitAsinSon":                "/erp/sc/routing/finance/ProfitState/profitAsinSon",
    "profitSettlement":             "/erp/sc/routing/finance/ProfitState/profitSettlement",
    "FianceProfitMsku":             "/erp/sc/routing/finance/ProfitState/profitMsku",
    "SettlementReport":             "/cost/center/api/settlement/report",
    "CostStream":                   "/cost/center/api/cost/stream",
    "OrderProfitListMSKU":          "/basicOpen/finance/mreport/OrderProfit",
    "InvoiceList":                  "/bd/profit/report/open/report/ads/invoice/list",
    "InvoiceDetail":                "/bd/profit/report/open/report/ads/invoice/detail",
    "InvoiceCampaignList":          "/bd/profit/report/open/report/ads/invoice/campaign/list",
    "QueryReceiptFundsList":        "/basicOpen/finance/queryReceiptFundsList",
    "RequestFundsOrderList":        "/basicOpen/finance/requestFunds/order/list",
    "SettlementExportUrlGet":       "/bd/sp/api/open/settlement/export/url/get",
    "bdASIN":                       "/bd/profit/report/open/report/asin/list",
    "bdMSKU":                       "/bd/profit/report/open/report/msku/list",
    "bdOrder":                      "/bd/profit/report/open/report/order/list",
    "bdParentASIN":                 "/bd/profit/report/open/report/parent/asin/list",
    "bdSKU":                        "/bd/profit/report/open/report/sku/list",
    "bdSeller":                     "/bd/profit/report/open/report/seller/list",
    "bdSellerSummary":              "/bd/profit/report/open/report/seller/summary/list",
    "centerOdsDetailQuery":         "/cost/center/ods/detail/query",
    "feeManagementList":            "/bd/fee/management/open/feeManagement/otherFee/list",
    "feeManagementType":            "/bd/fee/management/open/feeManagement/otherFee/type",
    "lazadaPayoutList":             "/basicOpen/finance/lazada/payout/list",
    "lazadaSettlementList":         "/basicOpen/finance/lazada/settlement/list",
    "profitReportOrderTranscationList": "/basicOpen/finance/profitReport/order/transcation/list",
    "receivableReportList":         "/bd/sp/api/open/monthly/receivable/report/list",
    "reportListDetail":             "/bd/sp/api/open/monthly/receivable/report/list/detail",
    "reportListDetailInfo":         "/bd/sp/api/open/monthly/receivable/report/list/detail/info",
    "requestFundsPoolCustomFeeList": "/basicOpen/finance/requestFundsPool/customFee/list",
    "requestFundsPoolInboundList":  "/basicOpen/finance/requestFundsPool/inbound/list",
    "requestFundsPoolLogisticsList": "/basicOpen/finance/requestFundsPool/logistics/list",
    "requestFundsPoolOtherFeeList": "/basicOpen/finance/requestFundsPool/otherFee/list",
    "requestFundsPoolPrepayList":   "/basicOpen/finance/requestFundsPool/prepay/list",
    "requestFundsPoolPurchaseList": "/basicOpen/finance/requestFundsPool/purchase/list",
    "settlementSummaryList":        "/bd/sp/api/open/settlement/summary/list",
    "settlementTransactionList":    "/bd/sp/api/open/settlement/transaction/detail/list",
    "shopeeAdjustmentList":         "/basicOpen/finance/shopee/adjustment/list",
    "shopeeIncomeList":             "/basicOpen/finance/shopee/income/list",
    "shopeePayoutList":             "/basicOpen/finance/shopee/payout/list",
    "summaryQuery":                 "/cost/center/ods/summary/query",

    # ── 统计 (Statistics) ──
    "AsinDailyLists":               "/erp/sc/data/sales_report/asinDailyLists",
    "AsinList":                     "/erp/sc/data/sales_report/asinList",
    "AsinListNew":                  "/bd/productPerformance/openApi/asinList",
    "StoreSales":                   "/erp/sc/data/sales_report/sales",
    "FBAStorageFeeLongTerm":        "/erp/sc/data/fba_report/storageFeeLongTerm",
    "FBAStorageFeeMonth":           "/erp/sc/data/fba_report/storageFeeMonth",
    "FbaStockAggregateListNew":     "/cost/center/openApi/fba/gather/query",
    "FbaStockDetailListNew":        "/cost/center/openApi/fba/detail/query",
    "FbaStockReportList":           "/erp/sc/routing/fba/fbaStockReport/getList",
    "LocalAggregateList":           "/erp/sc/routing/inventoryLog/WareHouseReport/getLocalWareHouseSummaryList",
    "LocalAggregateListNew":        "/inventory/center/openapi/storageReport/local/aggregate/list",
    "LocalDetailList":              "/erp/sc/routing/inventoryLog/WareHouseReport/getLocalWareHouseDetailList",
    "LocalDetailListNew":           "/inventory/center/openapi/storageReport/local/detail/page",
    "MonthRefund":                  "/erp/sc/routing/finance/Refund/profitMonthRefund",
    "OverseasAggregateList":        "/erp/sc/routing/inventoryLog/WareHouseReport/getOverSeaSummaryList",
    "OverseasAggregateListNew":     "/inventory/center/openapi/storageReport/overseas/aggregate/list",
    "OverseasDetailList":           "/erp/sc/routing/inventoryLog/WareHouseReport/getOverSeaDetailList",
    "OverseasDetailListNew":        "/inventory/center/openapi/storageReport/overseas/detail/page",
    "PlatformStatisticsSaleStatPageListV2": "/basicOpen/platformStatisticsV2/saleStat/pageList",
    "ProfitMsku":                   "/erp/sc/routing/finance/ProfitStatis/profitMsku",
    "PurchaseReportBuyerList":      "/basicOpen/report/purchase/buyer/list",
    "PurchaseReportProductList":    "/basicOpen/report/purchase/product/list",
    "PurchaseReportSupplierList":   "/basicOpen/report/purchase/supplier/list",
    "ReimbursementList":            "/basicOpen/openapi/mwsReport/reimbursementList",
    "ReturnOrderAnalysisLists":     "/basicOpen/salesAnalysis/returnOrder/analysisLists",
    "operateLogList":               "/basicOpen/operateManage/operateLog/list",
    "operateLogV2List":             "/basicOpen/operateManage/operateLog/list/v2",
    "performanceTrendByHour":       "/basicOpen/salesAnalysis/productPerformance/performanceTrendByHour",
    "AmazonReportExportTask":       "/basicOpen/report/amazonReportExportTask",
    "reportCreateReportExportTask": "/basicOpen/report/create/reportExportTask",
    "reportQueryReportExportTask":  "/basicOpen/report/query/reportExportTask",
    "statisticsOpenASIN":           "/bd/profit/statistics/open/asin/list",
    "statisticsOpenMSKU":           "/bd/profit/statistics/open/msku/list",
    "statisticsOpenParent":         "/bd/profit/statistics/open/parent/asin/list",
    "statisticsOpenSeller":         "/bd/profit/statistics/open/seller/list",

    # ── FBA发货 ──
    "FBAShipmentList":              "/erp/sc/data/fba_report/shipmentList",
    "FBAReceivedInventory":         "/erp/sc/data/fba_report/receivedInventory",
    "ShipmentPlanLists":            "/erp/sc/data/fba_report/shipmentPlanLists",
    "GetFbaProductList":            "/erp/sc/routing/fba/shipment/getFbaProductList",
    "GetInboundShipmentList":       "/erp/sc/routing/storage/shipment/getInboundShipmentList",
    "GetInboundShipmentListMwsDetailList": "/erp/sc/routing/storage/shipment/getInboundShipmentListMwsDetailList",
    "ShipFromAddressList":          "/erp/sc/routing/fba/shipment/shipFromAddressList",
    "BoxInfo":                      "/erp/sc/routing/fba/shipment/boxInfo",
    "GetHeadLogisticsFeeTypes":     "/erp/sc/routing/fba/shipment/getHeadLogisticsFeeTypes",
    "GetSeaTrackSupplierCarriers":  "/erp/sc/routing/fba/shipment/getSeaTrackSupplierCarriers",
    "QuerySTATaskList":             "/amzStaServer/openapi/inbound-plan/page",
    "StaTaskDetail":                "/amzStaServer/openapi/inbound-plan/detail",
    "getInboundShipmentListMwsDetail": "/erp/sc/routing/storage/shipment/getInboundShipmentListMwsDetail",

    # ── 亚马逊源表数据 (SourceData) ──
    "AllOrders":                    "/erp/sc/data/mws_report/allOrders",
    "FbaOrders":                    "/erp/sc/data/mws_report/fbaOrders",
    "RefundOrders":                 "/erp/sc/data/mws_report/refundOrders",
    "Transaction":                  "/erp/sc/data/mws_report/transaction",
    "ManageInventory":              "/erp/sc/data/mws_report/manageInventory",
    "DailyInventory":               "/erp/sc/data/mws_report/dailyInventory",
    "AfnFulfillableQuantity":       "/erp/sc/data/mws_report/getAfnFulfillableQuantity",
    "ReservedInventory":            "/erp/sc/data/mws_report/reservedInventory",
    "RemovalLists":                 "/erp/sc/data/fba_report/removalLists",
    "RemovalOrderListNew":          "/erp/sc/routing/data/order/removalOrderListNew",
    "RemovalShipmentList":          "/erp/sc/statistic/removalShipment/list",
    "SourceRemovalOrders":          "/erp/sc/data/mws_report/removalOrders",
    "AdjustmentList":               "/basicOpen/openapi/mwsReport/adjustmentList",
    "getAmazonFulfilledShipmentsList": "/erp/sc/data/mws_report/getAmazonFulfilledShipmentsList",
    "getFbaAgeList":                "/erp/sc/routing/fba/fbaStock/getFbaAgeList",
    "getFbaInventoryEventDetailList": "/erp/sc/data/mws_report/getFbaInventoryEventDetailList",
    "v1getAmazonFulfilledShipmentsList": "/erp/sc/data/mws_report_v1/getAmazonFulfilledShipmentsList",
    "v1getFbaInventoryEventDetailList": "/erp/sc/data/mws_report_v1/getFbaInventoryEventDetailList",
    "fbaExchangeOrderList":         "/erp/sc/routing/data/order/fbaExchangeOrderList",
    "fbmReturnOrderList":           "/erp/sc/routing/data/order/fbmReturnOrderList",

    # ── 补货建议 (FBASug) ──
    "GetSummaryList":               "/erp/sc/routing/restocking/analysis/getSummaryList",
    "ConfigASIN":                   "/erp/sc/routing/fbaSug/asin/getConfig",
    "ConfigMSKU":                   "/erp/sc/routing/fbaSug/msku/getConfig",
    "DailySalesInfoFeatureASIN":    "/erp/sc/routing/fbaSug/asin/getDailySalesInfoFeature",
    "DailySalesInfoFeatureMSKU":    "/erp/sc/routing/fbaSug/msku/getDailySalesInfoFeature",
    "InfoASIN":                     "/erp/sc/routing/fbaSug/asin/getInfo",
    "InfoMSKU":                     "/erp/sc/routing/fbaSug/msku/getInfo",
    "SourceListASIN":               "/erp/sc/routing/fbaSug/asin/getSourceList",
    "SourceListMSKU":               "/erp/sc/routing/fbaSug/msku/getSourceList",

    # ── 补货限制 (FBALimit) ──
    "GetIpiInfo":                   "/erp/sc/routing/fbaLimit/restock/getIpiInfo",
    "replenishmentRestrictionList": "/basicOpen/openapi/replenishmentRestriction/page/list",

    # ── 采购 (Purchase) ──
    "PurchaseOrderList":            "/erp/sc/routing/data/local_inventory/purchaseOrderList",
    "Supplier":                     "/erp/sc/data/local_inventory/supplier",
    "changeOrderList":              "/erp/sc/routing/purchase/purchaseChangeOrder/changeOrderList",
    "purchaseGetOrders":            "/erp/sc/routing/purchase/purchaseOutsourceOrder/getOrders",
    "getPurchasePlans":             "/erp/sc/routing/data/local_inventory/getPurchasePlans",
    "getPurchaseReturnOrderList":   "/erp/sc/routing/purchase/purchase_return_order/getPurchaseReturnOrderList",
    "purchaserLists":               "/erp/sc/routing/data/purchaser/lists",

    # ── 仓库 (Warehouse) ──
    "WarehouseLists":               "/erp/sc/data/local_inventory/warehouse",
    "WarehouseStatement":           "/erp/sc/routing/data/local_inventory/wareHouseStatement",
    "WarehouseStatementNew":        "/erp/sc/routing/inventoryLog/WareHouseInventory/wareHouseCenterStatement",
    "InventoryDetails":             "/erp/sc/routing/data/local_inventory/inventoryDetails",
    "inventoryBinDetails":          "/erp/sc/routing/data/local_inventory/inventoryBinDetails",
    "wareHouseBinStatement":        "/erp/sc/routing/data/local_inventory/wareHouseBinStatement",
    "warehouseBin":                 "/erp/sc/routing/data/local_inventory/warehouseBin",
    "FBAStock":                     "/erp/sc/routing/fba/fbaStock/fbaList",
    "FBAStock_v2":                  "/basicOpen/openapi/storage/fbaWarehouseDetail",
    "AwdWarehouseDetail":           "/basicOpen/openapi/storage/awdWarehouseDetail",
    "GetBatchDetailList":           "/erp/sc/routing/data/local_inventory/getBatchDetailList",
    "GetBatchStatementList":        "/erp/sc/routing/data/local_inventory/getBatchStatementList",
    "GetReceiveGoodRecords":        "/erp/sc/routing/owms/inbound/getReceiveGoodRecords",
    "PurchaseReceiptOrderList":     "/erp/sc/routing/deliveryReceipt/PurchaseReceiptOrder/getOrderList",
    "ReceiptOrderQcList":           "/erp/sc/routing/deliveryReceipt/ReceiptOrderQc/getOrderList",
    "WmsOrderList":                 "/erp/sc/routing/wms/order/wmsOrderList",
    "WmsOrderDetail":               "/basicOpen/wmsOrder/getWmsOrdersByOrderNumbers",
    "OverseaWarehouseMatchList":    "/basicOpen/overseaWarehouseSetting/matchList",
    "OverSeasStockDetail":          "/basicOpen/overSeaWarehouse/stockOrder/detail",
    "getProcessOrderLists":         "/erp/sc/routing/inventoryReceipt/StorageProcess/getOrderLists",
    "getStorageAdjustOrderList":    "/erp/sc/routing/inventoryReceipt/StorageAdjustment/getStorageAdjustOrderList",
    "getStorageAllocationList":     "/erp/sc/routing/inventoryReceipt/StorageAllocation/getStorageAllocationList",
    "ReturnList":                   "/pb/mp/returns/v2/list",
    "inboundgetOrders":             "/erp/sc/routing/storage/inbound/getOrders",
    "outboundgetOrders":            "/erp/sc/routing/storage/outbound/getOrders",
    "removalInboundList":           "/erp/sc/routing/owms/removalInbound/list",
    "matchSkuList":                 "/erp/sc/routing/owms/inbound/matchSkuList",
    "listInbound":                  "/erp/sc/routing/owms/inbound/listInbound",
    "checkGetOrderList":            "/erp/sc/routing/inventoryReceipt/InventoryCheck/getOrderList",
    "checkGetOrderDetail":          "/erp/sc/routing/inventoryReceipt/InventoryCheck/getOrderDetail",
    "getPackingData":               "/erp/sc/routing/owms/inbound/getPackingData",
    "qualityInspectionOrderDetail": "/basicOpen/qualityInspectionOrder/detail",

    # ── 客服 (Service) ──
    "FeedbackList":                 "/erp/sc/cs/feedback/list",
    "FeedbackListMws":              "/erp/sc/cs/feedback/listMws",
    "CustomerList":                 "/bd/crm/open/api/customer/list",
    "AfterSalesWorkOrderList":      "/pb/mp/returns/workOrder/list",
    "PerformanceNoticeList":        "/basicOpen/customerService/performanceNotice/list",
    "PerformanceNoticeDetail":      "/basicOpen/customerService/storeTarget/detail",
    "mailDetail":                   "/erp/sc/data/mail/detail",
    "mailLists":                    "/erp/sc/data/mail/lists",
    "review":                       "/erp/sc/v2/data/mws/reviews",
    "reviewDetail":                 "/erp/sc/cs/reviewReport/detail",
    "reviewLists":                  "/erp/sc/v2/cs/reviewReport/lists",
    "reviewV2":                     "/basicOpen/openapi/service/v3/data/mws/reviews",
    "feedbackDetail":               "/erp/sc/cs/feedbackReport/detail",
    "feedbackLists":                "/erp/sc/cs/feedbackReport/lists",
    "customerServiceCrmcustomerIndex": "/basicOpen/customerService/crm/customer/index",
    "customerServiceRmaManageList": "/basicOpen/customerService/rmaManage/list",
    "storePerformanceList":         "/basicOpen/customerService/storeTarget/list",
    "voiceOfBuyerList":             "/basicOpen/customerService/voiceOfBuyer/list",

    # ── 物流 (Logistics) ──
    "ChannelList":                  "/erp/sc/data/local_inventory/channelList",
    "QueryHeadLogisticsProvider":   "/basicOpen/logistics/headLogisticsProvider/query/list",
    "transportMethodList":          "/basicOpen/businessConfig/transportMethod/list",

    # ── 工具 (Tools) ──
    "CompetitiveMonitorList":       "/basicOpen/tool/competitiveMonitor/list",
    "GetKeywordList":               "/erp/sc/routing/tool/toolKeywordRank/getKeywordList",
    "warningMessageGoodsList":      "/basicOpen/settings/warningMessage/goodsList",
    "warningMessageInventoryList":  "/basicOpen/settings/warningMessage/inventoryList",

    # ── VC ──
    "vcOrderPageList":              "/basicOpen/platformOrder/vcOrder/pageList",
    "vcOrderPoDetail":              "/basicOpen/platformOrder/vcOrderPo/detail",
    "vcOrderDfDetail":              "/basicOpen/platformOrder/vcOrderDf/detail",
    "vcDeliverPageList":            "/basicOpen/openapi/getInvoice/page/list",
    "vcDeliverDetail":              "/basicOpen/openapi/getInvoice/detail",
    "listingManageVcListingPageList": "/basicOpen/listingManage/vcListing/pageList",
    "platformAuthVcSellerPageList": "/basicOpen/platformAuth/vcSeller/pageList",

    # ── 目标管理 (TargetManage) ──
    "StoreBatchSelect":             "/bd/goal/management/open/store/batchSelect",
    "UserBatchSelect":              "/bd/goal/management/open/user/batchSelect",

    # ── 多平台广告 (MultiPlatform/Advertisement) ──
    "queryCommonAdvertiserList":    "/basicOpen/multiplatform/ads/queryCommonAdvertiserList",
    "queryGmvStoreList":            "/basicOpen/multiplatform/ads/queryGmvStoreList",
    "queryTiktokAdGroupList":       "/basicOpen/multiplatform/ads/queryTiktokAdGroupList",
    "queryTiktokAdList":            "/basicOpen/multiplatform/ads/queryTiktokAdList",
    "queryAdvertiserList":          "/basicOpen/multiplatform/ads/queryAdvertiserList",
    "queryTiktokCampaignList":      "/basicOpen/multiplatform/ads/queryTiktokCampaignList",
    "queryGmvAdvertiserReportList": "/basicOpen/multiplatform/ads/queryGmvAdvertiserReportList",
    "queryGmvCampaignReportList":   "/basicOpen/multiplatform/ads/queryGmvCampaignReportList",
    "queryGmvItemGroupReportList":  "/basicOpen/multiplatform/ads/queryGmvItemGroupReportList",
    "queryAdGroupSvList":           "/basicOpen/multiplatform/ads/queryAdGroupSvList",
    "queryCampaignSpList":          "/basicOpen/multiplatform/ads/queryCampaignSpList",
    "queryGroupSpList":             "/basicOpen/multiplatform/ads/queryGroupSpList",
    "queryPageTypeSPList":          "/basicOpen/multiplatform/ads/queryPageTypeSPList",
    "queryReportPageTypeSvList":    "/basicOpen/multiplatform/ads/queryReportPageTypeSvList",
    "reportAdGroupSbList":          "/basicOpen/multiplatform/ads/reportAdGroupSbList",
    "reportAdItemSbList":           "/basicOpen/multiplatform/ads/reportAdItemSbList",
    "reportAdItemSpList":           "/basicOpen/multiplatform/ads/reportAdItemSpList",
    "reportAdItemSvList":           "/basicOpen/multiplatform/ads/reportAdItemSvList",
    "reportCampaignSbList":         "/basicOpen/multiplatform/ads/reportCampaignSbList",
    "reportCampaignSvList":         "/basicOpen/multiplatform/ads/reportCampaignSvList",
    "reportKeywordSbList":          "/basicOpen/multiplatform/ads/reportKeywordSbList",
    "reportKeywordSpList":          "/basicOpen/multiplatform/ads/reportKeywordSpList",
    "reportKeywordSvList":          "/basicOpen/multiplatform/ads/reportKeywordSvList",
    "reportPageTypeSbList":         "/basicOpen/multiplatform/ads/reportPageTypeSbList",
    "reportPlatformSbList":         "/basicOpen/multiplatform/ads/reportPlatformSbList",
    "reportPlatformSpList":         "/basicOpen/multiplatform/ads/reportPlatformSpList",
    "reportPlatformSvList":         "/basicOpen/multiplatform/ads/reportPlatformSvList",
    "reportSearchTrendsList":       "/basicOpen/multiplatform/ads/reportSearchTrendsList",

    # ── 多平台V2 (MultiPlatform/V2) - 查询类 ──
    "MultiPlatOrderV2":             "/pb/mp/order/v2/list",
    "StoreInfoV2":                  "/pb/mp/shop/v2/getSellerList",
    "PairListV2":                   "/pb/mp/listing/v2/getPairList",
    "QueryShippingListV2":          "/basicOpen/multiplatform/query/shippingList",
    "QueryShippingListPage":        "/cepf/warehouse/api/openApi/queryShippingListPage",
    "QueryWFSCargoPage":            "/cepf/warehouse/api/openApi/queryWFSCargoPage",
    "QueryWFSInventionPage":        "/cepf/warehouse/api/openApi/queryWFSInventionPage",
    "AliexpressListV2":             "/basicOpen/multiplatform/aliexpress/list/v2",
    "aliexpressList":               "/basicOpen/multiplatform/aliExpress/list",
    "eBayList":                     "/basicOpen/multiplatform/ebay/list",
    "walmartList":                  "/basicOpen/multiplatform/walmart/list",
    "TemuList":                     "/basicOpen/multiplatform/temu/list",
    "TemuCargo":                    "/basicOpen/multiplatform/temu/cargo",
    "TikTokList":                   "/basicOpen/multiplatform/tiktok/list",
    "SheinList":                    "/basicOpen/multiplatform/shein/list",
    "ShopifyVariantList":           "/basicOpen/multiplatform/shopify/variantList",
    "CoupangStockList":             "/basicOpen/multiplatform/coupang/stockSearch",
    "FbsStockList":                 "/basicOpen/multiplatform/fbs/stockSearch",
    "FbtStockList":                 "/basicOpen/multiplatform/fbt/stockSearch/v2",
    "FbtStockSearch":               "/basicOpen/multiplatform/fbt/stockSearch",
    "FullList":                     "/basicOpen/multiplatform/full/stockSearch",
    "WayfairStockList":             "/basicOpen/multiplatform/wayfair/stockSearch",
    "LineList":                     "/basicOpen/multiplatform/line/list",
    "addCargoGoodsList":            "/basicOpen/multiplatform/cargo/addCargoGoods/list",
    "WalmartPaymentQueryPage":      "/cepf/fms/openapi/walmartPayment/queryPage",
    "WalmartPaymentQueryReport":    "/cepf/fms/openapi/walmartPayment/queryReport",
    "WalmartCommentList":           "/basicOpen/multiplatform/walmart/queryCommentList",
    "profitReportMsku":             "/basicOpen/multiplatform/profit/report/msku",
    "profitReportOrder":            "/basicOpen/multiplatform/profit/report/order",
    "profitReportSeller":           "/basicOpen/multiplatform/profit/report/seller",
    "profitReportSku":              "/basicOpen/multiplatform/profit/report/sku",
    "newPlatformOrderList":         "/cepfPlatformOrder/open-api/newPlatformOrder/list",
    "addressReturnAddressList":     "/basicOpen/multiplatform/address/returnAddressList",
}

# ── 需要 GET 方法的接口（默认为 POST）──
GET_APIS = {
    "AccoutLists", "AllMarketplace", "ConceptSellerLists",
    "GetProductTag",
    "reviewLists",
    "getPackingData",
}

# ── 使用 page/page_size 分页的接口（默认用 offset/length）──
# 值为 (page_key, size_key)
PAGE_APIS = {
    "WmsOrderList":              ("page", "page_size"),
    "checkGetOrderList":         ("page", "page_size"),
    "checkGetOrderDetail":       ("page", "page_size"),
    "getStorageAdjustOrderList": ("page", "page_size"),
    "getStorageAllocationList":  ("page", "page_size"),
    "listInbound":               ("page", "page_size"),
    "FBMOrderList":              ("page", "length"),
    "QuerySTATaskList":          ("page", "length"),
    "PlatformStatisticsSaleStatPageListV2": ("page", "length"),
    "GetPagingLogLists":         ("page", "size"),
}

# ── 响应格式特殊的接口 ──
# cost center API 返回 data.records 或 data.row_data，而非直接 data
COST_CENTER_APIS = {
    "SettlementReport", "CostStream",
    "centerOdsDetailQuery", "summaryQuery",
    "FbaStockAggregateListNew", "FbaStockDetailListNew",
}

SUPPORTED_APIS = [
    # ── newAd 报表 (37个) ──
    "spCampaignReports", "campaignPlacementReports", "spAdGroupReports",
    "spProductAdReports", "spKeywordReports", "spTargetReports",
    "asinReports", "queryWordReports",
    "hsaCampaignReports", "hsaCampaignPlacementReports", "hsaAdGroupReports",
    "listHsaTargetingReport", "hsaQueryWordReports", "hsaPurchasedAsinReports",
    "listHsaProductAdReport", "listHsaKeywordPlacementReport",
    "sdCampaignReports", "sdAdGroupReports", "sdProductAdReports",
    "sdTargetReports", "sdAsinReports", "sdMatchTargetReports",
    "spCampaignHourData", "spAdPlacementHourData", "spAdGroupHourData",
    "spAdvertiseHourData", "spTargetHourData",
    "sbCampaignHourData", "sbAdGroupHourData", "sbTargetHourData", "sbAdPlacementHourData",
    "sdCampaignHourData", "sdAdGroupHourData", "sdAdvertiseHourData", "sdTargetHourData",
    "dspReportOrderList", "ProductAnalysisList",
    # ── newAd 基础数据 (20个) ──
    "dspAccountList", "portfolios",
    "spCampaigns", "spAdGroups", "spProductAds", "spKeywords", "spTargets",
    "spNegativeTargetsOrKeywords",
    "hsaCampaigns", "hsaAdGroups", "hsaProductAds", "sbTargeting",
    "hsaNegativeKeywords", "hsaNegativeTargets", "sbDivideAsinReports",
    "sdCampaigns", "sdAdGroups", "sdProductAds", "sdTargets", "sdNegativeTargets",
    # ── newAd 报表下载 ──
    "abaReport",
    # ── 基础数据 ──
    "AccoutLists", "AllMarketplace", "AttachmentDownload", "ConceptSellerLists",
    "Currency", "CustomAttachmentDownload", "StateList", "WorldStateLists",
    # ── 销售 ──
    "mwsOrders", "mwsListing", "orderReturnInformation", "scOrderSetRemark",
    "OrderDetail", "RefundOrder", "sale_ProductList", "FBMOrderList", "FBMOrderDetail",
    "MCFOrderList", "ProductInformation", "GetPrices", "LogisticsInformation",
    "GetMerchantShippingGroup", "GetFulfillmentResult", "QueryProductList",
    "PublishManageCategoryRoot", "PublishManageCategoryChildren", "PublishManageGetProductType",
    "adjustPriceAdjustPriceManual", "afterSaleList",
    "fbaFeeDifferenceList", "fbaFeeDifferenceMskuList",
    "globalTagPageList", "listingOperateLogPageList",
    "promotionListingList", "promotionListingDetailCoupon", "promotionListingDetailManage",
    "promotionListingDetailPrimeDiscount", "promotionListingDetailSecKill",
    "promotionalActivitiesCouponList", "promotionalActivitiesManageList",
    "promotionalActivitiesSecKillList", "promotionalActivitiesVipDiscountList",
    "queryListingRelationTagList",
    "promotionCouponAllDetailBatch", "promotionManagementAllDetailBatch",
    "promotionPrimeDiscountAllDetailBatch", "promotionSecKillAllDetailBatch",
    # ── 产品 ──
    "ProductLists", "ProductDetails", "Brand", "Category", "UpcList",
    "GetProductTag", "GetPagingLogLists",
    "attributeList", "batchGetProductInfo", "bundledProductList",
    "getTransparencyProductList", "productAuxList",
    "spuInfo", "spuList",
    # ── 财务 ──
    "profitAsin", "profitAsinSon", "profitSettlement", "FianceProfitMsku",
    "SettlementReport", "CostStream", "OrderProfitListMSKU",
    "InvoiceList", "InvoiceDetail", "InvoiceCampaignList",
    "QueryReceiptFundsList", "RequestFundsOrderList", "SettlementExportUrlGet",
    "bdASIN", "bdMSKU", "bdOrder", "bdParentASIN", "bdSKU", "bdSeller", "bdSellerSummary",
    "centerOdsDetailQuery", "feeManagementList", "feeManagementType",
    "lazadaPayoutList", "lazadaSettlementList",
    "profitReportOrderTranscationList",
    "receivableReportList", "reportListDetail", "reportListDetailInfo",
    "requestFundsPoolCustomFeeList", "requestFundsPoolInboundList",
    "requestFundsPoolLogisticsList", "requestFundsPoolOtherFeeList",
    "requestFundsPoolPrepayList", "requestFundsPoolPurchaseList",
    "settlementSummaryList", "settlementTransactionList",
    "shopeeAdjustmentList", "shopeeIncomeList", "shopeePayoutList",
    "summaryQuery",
    # ── 统计 ──
    "AsinDailyLists", "AsinList", "AsinListNew", "StoreSales",
    "FBAStorageFeeLongTerm", "FBAStorageFeeMonth",
    "FbaStockAggregateListNew", "FbaStockDetailListNew", "FbaStockReportList",
    "LocalAggregateList", "LocalAggregateListNew",
    "LocalDetailList", "LocalDetailListNew",
    "MonthRefund",
    "OverseasAggregateList", "OverseasAggregateListNew",
    "OverseasDetailList", "OverseasDetailListNew",
    "PlatformStatisticsSaleStatPageListV2", "ProfitMsku",
    "PurchaseReportBuyerList", "PurchaseReportProductList", "PurchaseReportSupplierList",
    "ReimbursementList", "ReturnOrderAnalysisLists",
    "operateLogList", "operateLogV2List", "performanceTrendByHour",
    "AmazonReportExportTask", "reportCreateReportExportTask", "reportQueryReportExportTask",
    "statisticsOpenASIN", "statisticsOpenMSKU", "statisticsOpenParent", "statisticsOpenSeller",
    # ── FBA发货 ──
    "FBAShipmentList", "FBAReceivedInventory", "ShipmentPlanLists",
    "GetFbaProductList", "GetInboundShipmentList", "GetInboundShipmentListMwsDetailList",
    "ShipFromAddressList", "BoxInfo", "GetHeadLogisticsFeeTypes",
    "GetSeaTrackSupplierCarriers", "QuerySTATaskList", "StaTaskDetail",
    "getInboundShipmentListMwsDetail",
    # ── 亚马逊源表数据 ──
    "AllOrders", "FbaOrders", "RefundOrders", "Transaction",
    "ManageInventory", "DailyInventory", "AfnFulfillableQuantity", "ReservedInventory",
    "RemovalLists", "RemovalOrderListNew", "RemovalShipmentList", "SourceRemovalOrders",
    "AdjustmentList", "getAmazonFulfilledShipmentsList",
    "getFbaAgeList", "getFbaInventoryEventDetailList",
    "v1getAmazonFulfilledShipmentsList", "v1getFbaInventoryEventDetailList",
    "fbaExchangeOrderList", "fbmReturnOrderList",
    # ── 补货建议 ──
    "GetSummaryList", "ConfigASIN", "ConfigMSKU",
    "DailySalesInfoFeatureASIN", "DailySalesInfoFeatureMSKU",
    "InfoASIN", "InfoMSKU", "SourceListASIN", "SourceListMSKU",
    # ── 补货限制 ──
    "GetIpiInfo", "replenishmentRestrictionList",
    # ── 采购 ──
    "PurchaseOrderList", "Supplier", "changeOrderList",
    "purchaseGetOrders", "getPurchasePlans", "getPurchaseReturnOrderList", "purchaserLists",
    # ── 仓库 ──
    "WarehouseLists", "WarehouseStatement", "WarehouseStatementNew",
    "InventoryDetails", "inventoryBinDetails", "wareHouseBinStatement", "warehouseBin",
    "FBAStock", "FBAStock_v2", "AwdWarehouseDetail",
    "GetBatchDetailList", "GetBatchStatementList", "GetReceiveGoodRecords",
    "PurchaseReceiptOrderList", "ReceiptOrderQcList",
    "WmsOrderList", "WmsOrderDetail",
    "OverseaWarehouseMatchList", "OverSeasStockDetail",
    "getProcessOrderLists", "getStorageAdjustOrderList", "getStorageAllocationList",
    "ReturnList", "inboundgetOrders", "outboundgetOrders",
    "removalInboundList", "matchSkuList", "listInbound",
    "checkGetOrderList", "checkGetOrderDetail", "getPackingData",
    "qualityInspectionOrderDetail",
    # ── 客服 ──
    "FeedbackList", "FeedbackListMws", "CustomerList", "AfterSalesWorkOrderList",
    "PerformanceNoticeList", "PerformanceNoticeDetail",
    "mailDetail", "mailLists", "review", "reviewDetail", "reviewLists", "reviewV2",
    "feedbackDetail", "feedbackLists",
    "customerServiceCrmcustomerIndex", "customerServiceRmaManageList",
    "storePerformanceList", "voiceOfBuyerList",
    # ── 物流 ──
    "ChannelList", "QueryHeadLogisticsProvider", "transportMethodList",
    # ── 工具 ──
    "CompetitiveMonitorList", "GetKeywordList",
    "warningMessageGoodsList", "warningMessageInventoryList",
    # ── VC ──
    "vcOrderPageList", "vcOrderPoDetail", "vcOrderDfDetail",
    "vcDeliverPageList", "vcDeliverDetail",
    "listingManageVcListingPageList", "platformAuthVcSellerPageList",
    # ── 目标管理 ──
    "StoreBatchSelect", "UserBatchSelect",
    # ── 多平台广告 ──
    "queryCommonAdvertiserList", "queryGmvStoreList",
    "queryTiktokAdGroupList", "queryTiktokAdList",
    "queryAdvertiserList", "queryTiktokCampaignList",
    "queryGmvAdvertiserReportList", "queryGmvCampaignReportList",
    "queryGmvItemGroupReportList",
    "queryAdGroupSvList", "queryCampaignSpList", "queryGroupSpList",
    "queryPageTypeSPList", "queryReportPageTypeSvList",
    "reportAdGroupSbList", "reportAdItemSbList", "reportAdItemSpList", "reportAdItemSvList",
    "reportCampaignSbList", "reportCampaignSvList",
    "reportKeywordSbList", "reportKeywordSpList", "reportKeywordSvList",
    "reportPageTypeSbList",
    "reportPlatformSbList", "reportPlatformSpList", "reportPlatformSvList",
    "reportSearchTrendsList",
    # ── 多平台V2 ──
    "MultiPlatOrderV2", "StoreInfoV2", "PairListV2",
    "QueryShippingListV2", "QueryShippingListPage",
    "QueryWFSCargoPage", "QueryWFSInventionPage",
    "AliexpressListV2", "aliexpressList", "eBayList", "walmartList",
    "TemuList", "TemuCargo", "TikTokList", "SheinList",
    "ShopifyVariantList", "CoupangStockList",
    "FbsStockList", "FbtStockList", "FbtStockSearch", "FullList",
    "WayfairStockList", "LineList", "addCargoGoodsList",
    "WalmartPaymentQueryPage", "WalmartPaymentQueryReport",
    "WalmartCommentList",
    "profitReportMsku", "profitReportOrder", "profitReportSeller", "profitReportSku",
    "newPlatformOrderList", "addressReturnAddressList",
]


# ─── HTTP 客户端（requests 优先，不可用时降级 urllib）────────────────────────

def _http_post(url: str, params: Optional[dict] = None,
               json_body: Optional[dict] = None,
               form_body: Optional[dict] = None,
               headers: Optional[dict] = None,
               timeout: int = 60) -> dict:
    req_headers = dict(headers or {})
    try:
        import requests as _req
        if form_body:
            resp = _req.post(url, params=params, data=form_body,
                             headers=req_headers, timeout=timeout)
        else:
            resp = _req.post(url, params=params, json=json_body,
                             headers=req_headers, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except ImportError:
        pass  # 降级到 urllib

    # urllib 降级路径
    import urllib.request, urllib.error
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    if form_body:
        data = urllib.parse.urlencode(form_body).encode()
        req_headers["Content-Type"] = "application/x-www-form-urlencoded"
    elif json_body is not None:
        data = json.dumps(json_body, ensure_ascii=False, sort_keys=True).encode()
        req_headers.setdefault("Content-Type", "application/json")
    else:
        data = b""
    req = urllib.request.Request(url, data=data, headers=req_headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')}") from e


def _http_get(url: str, params: Optional[dict] = None,
              headers: Optional[dict] = None, timeout: int = 60) -> dict:
    req_headers = dict(headers or {})
    try:
        import requests as _req
        resp = _req.get(url, params=params, headers=req_headers, timeout=timeout)
        resp.raise_for_status()
        return resp.json()
    except ImportError:
        pass

    import urllib.request, urllib.error
    if params:
        url = url + "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers=req_headers)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        raise RuntimeError(f"HTTP {e.code}: {e.read().decode(errors='replace')}") from e


# ─── AES / 签名 ──────────────────────────────────────────────────────────────

def _aes_encrypt(key: str, data: str) -> str:
    try:
        from Crypto.Cipher import AES
    except ImportError:
        print("Error: pycryptodome 未安装。请运行：pip install pycryptodome", file=sys.stderr)
        sys.exit(1)
    BLOCK = 16
    pad_len = BLOCK - len(data) % BLOCK
    padded = data + chr(pad_len) * pad_len
    return base64.b64encode(
        AES.new(key.encode(), AES.MODE_ECB).encrypt(padded.encode())
    ).decode()


def _generate_sign(app_id: str, params: dict) -> str:
    """领星签名：ASCII排序 → MD5大写 → AES-ECB-Base64"""
    parts = []
    for k in sorted(params.keys()):
        v = params[k]
        if v == "":
            continue
        if isinstance(v, (dict, list)):
            v_str = json.dumps(v, ensure_ascii=False, separators=(",", ":"), sort_keys=True)
        else:
            v_str = str(v)
        parts.append(f"{k}={v_str}")
    md5_upper = hashlib.md5("&".join(parts).encode()).hexdigest().upper()
    return _aes_encrypt(app_id, md5_upper)


def _sign_params(app_id: str, token: str, extra: Optional[dict] = None) -> dict:
    """构造公共签名参数（含 sign）。extra 是需要参与签名的业务参数。"""
    base = {
        "app_key":      app_id,
        "access_token": token,
        "timestamp":    str(int(time.time())),
    }
    sign_src = dict(extra or {})
    sign_src.update(base)
    base["sign"] = urllib.parse.quote(_generate_sign(app_id, sign_src), safe="")
    return base


# ─── Token 缓存 ───────────────────────────────────────────────────────────────

def _token_cache_path(app_id: str) -> Path:
    return TOKEN_CACHE_DIR / f"lingxing_token_{app_id[:8]}.json"


def _load_cached_token(app_id: str) -> Optional[str]:
    path = _token_cache_path(app_id)
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text())
        if data.get("expires_at", 0) > time.time() + 60:
            return data["access_token"]
    except Exception:
        pass
    return None


def _save_token(app_id: str, token: str, expires_in: int) -> None:
    path = _token_cache_path(app_id)
    path.write_text(json.dumps({"access_token": token, "expires_at": time.time() + expires_in}))


def get_access_token(app_id: str, app_secret: str) -> str:
    """获取 access_token，自动使用本地缓存（2小时有效）。"""
    cached = _load_cached_token(app_id)
    if cached:
        return cached
    resp = _http_post(
        f"{HOST}/api/auth-server/oauth/access-token",
        form_body={"appId": app_id, "appSecret": app_secret},
    )
    if str(resp.get("code")) != "200":
        raise RuntimeError(f"获取 token 失败: {resp}")
    data = resp["data"]
    _save_token(app_id, data["access_token"], int(data["expires_in"]))
    return data["access_token"]


# ─── 店铺列表 ─────────────────────────────────────────────────────────────────

def list_seller_stores(app_id: str, token: str) -> list:
    """
    GET /erp/sc/data/seller/lists
    返回 list[dict]，每个 dict 含 sid / name / seller_id / country / has_ads_setting / status
    """
    qp = _sign_params(app_id, token)
    resp = _http_get(
        f"{HOST}/erp/sc/data/seller/lists",
        params=qp,
        headers={"X-API-VERSION": "2"},
    )
    code = resp.get("code")
    if code == "403" or code == 403:
        raise PermissionError(
            "403 权限不足。SellerLists 接口需要 ERP 全量权限，"
            "当前 AppKey 可能仅授权了广告数据。\n"
            "解决方法：在领星 ERP → 开放接口 中为该 AppKey 添加「基础数据」权限，"
            "或在环境变量中直接设置 LINGXING_SID=<数字> 跳过自动发现。"
        )
    if code not in (0, "0"):
        raise RuntimeError(f"SellerLists 返回错误: {resp}")
    return resp.get("data") or []


def print_stores_table(stores: list) -> None:
    """打印店铺列表表格"""
    print(f"\n{'SID':>6}  {'店铺名':20}  {'Amazon Seller ID':18}  {'国家':6}  {'广告授权':6}  {'状态'}")
    print("-" * 75)
    for s in stores:
        ads = "✓" if s.get("has_ads_setting") == 1 else "✗"
        status_map = {0: "停止", 1: "正常", 2: "授权异常", 3: "欠费"}
        status = status_map.get(s.get("status"), str(s.get("status")))
        print(f"{s.get('sid',''):>6}  {str(s.get('name',''))[:20]:20}  "
              f"{s.get('seller_id',''):18}  {s.get('country',''):6}  "
              f"{ads:6}  {status}")
    print()
    print(f"提示：将常用 SID 设置为环境变量后无需每次在 --params 中传入：")
    print(f"  export LINGXING_SID=<sid>")


# ─── API 调用 ────────────────────────────────────────────────────────────────

def get_api_path(api_name: str) -> str:
    return SPECIAL_PATHS.get(api_name, f"/pb/openapi/newad/{api_name}")


def _extract_data(resp: dict, api_name: str) -> tuple:
    """从响应中提取 data 和 total，兼容不同响应格式。返回 (data_list, total)"""
    raw_data = resp.get("data")

    # cost center API: data 是 dict，实际数据在 records/row_data 下
    if api_name in COST_CENTER_APIS and isinstance(raw_data, dict):
        records = raw_data.get("records") or raw_data.get("row_data") or []
        total = raw_data.get("total") or resp.get("total") or 0
        return records, total

    # 标准格式
    data = raw_data if isinstance(raw_data, list) else []
    total = resp.get("total") or 0
    return data, total


def _check_response_ok(resp: dict, api_name: str) -> None:
    """检查响应状态码是否表示成功"""
    code = resp.get("code")
    # 标准格式: code=0; cost center / targetmanage: code=1
    if code in (0, "0", 1, "1"):
        return
    # 有些接口用 success=true
    if resp.get("success") is True:
        return
    raise RuntimeError(
        f"API 错误: code={code} msg={resp.get('message') or resp.get('msg')} "
        f"detail={resp.get('error_details')}"
    )


def call_api(app_id: str, token: str, api_name: str,
             body: dict, extra_headers: Optional[dict] = None) -> dict:
    """单次调用（含签名），自动判断 GET/POST"""
    is_get = api_name in GET_APIS
    qp = _sign_params(app_id, token, extra=None if is_get else body)
    headers = {"X-API-VERSION": "2"}
    if extra_headers:
        headers.update(extra_headers)

    url = HOST + get_api_path(api_name)

    if is_get:
        # GET: body 参数放到 query params
        qp.update(body)
        return _http_get(url, params=qp, headers=headers)
    else:
        return _http_post(url, params=qp, json_body=body, headers=headers)


def call_api_all(app_id: str, token: str, api_name: str,
                 body: dict, page_size: int = 100) -> list:
    """自动分页，拉取全部数据。支持 offset/length 和 page/page_size 两种模式。"""
    all_data = []

    if api_name in PAGE_APIS:
        # page/page_size 模式
        pk, sk = PAGE_APIS[api_name]
        page = body.get(pk, 1)
        while True:
            page_body = {**body, pk: page, sk: page_size}
            resp = call_api(app_id, token, api_name, page_body)
            _check_response_ok(resp, api_name)
            data, total = _extract_data(resp, api_name)
            all_data.extend(data)
            print(f"[分页] page={page} 获取{len(data)}条，累计{len(all_data)}/{total}", file=sys.stderr)
            if not data or len(all_data) >= total:
                break
            page += 1
    else:
        # offset/length 模式（默认）
        offset = body.get("offset", 0)
        while True:
            page_body = {**body, "offset": offset, "length": page_size}
            resp = call_api(app_id, token, api_name, page_body)
            _check_response_ok(resp, api_name)
            data, total = _extract_data(resp, api_name)
            all_data.extend(data)
            offset += len(data)
            print(f"[分页] {offset}/{total}", file=sys.stderr)
            if not data or offset >= total:
                break

    return all_data


# ─── 主程序 ───────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="领星 OpenAPI CLI - 全模块查询",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--api",
                       help=f"接口名。支持 {len(SUPPORTED_APIS)} 个接口，"
                            f"用 --api help 查看完整列表")
    group.add_argument("--list-stores", action="store_true",
                       help="列出所有已授权亚马逊店铺及其 SID（需 ERP 全量权限）")

    parser.add_argument("--params", default="{}",
                        help="请求参数 JSON。若 LINGXING_SID 已设置且未指定 sid，则自动注入。")
    parser.add_argument("--all", dest="fetch_all", action="store_true",
                        help="自动翻页获取全部数据")
    parser.add_argument("--page-size", type=int, default=100,
                        help="--all 模式每页条数（默认 100）")
    args = parser.parse_args()

    # ── help 模式 ──
    if args.api == "help":
        print("支持的接口列表:")
        for name in SUPPORTED_APIS:
            path = get_api_path(name)
            method = "GET" if name in GET_APIS else "POST"
            print(f"  {name:45s} {method:4s} {path}")
        return

    # ── 凭证 ──
    app_id     = os.environ.get("LINGXING_APP_ID")
    app_secret = os.environ.get("LINGXING_APP_SECRET")
    if not app_id or not app_secret:
        print("Error: 请设置环境变量:\n"
              "  export LINGXING_APP_ID=your_app_id\n"
              "  export LINGXING_APP_SECRET=your_app_secret",
              file=sys.stderr)
        sys.exit(1)

    # ── Token ──
    try:
        token = get_access_token(app_id, app_secret)
    except Exception as e:
        print(f"Error: 获取 access_token 失败: {e}", file=sys.stderr)
        sys.exit(1)

    # ── --list-stores ──
    if args.list_stores:
        try:
            stores = list_seller_stores(app_id, token)
            print_stores_table(stores)
        except PermissionError as e:
            print(f"Warning: {e}", file=sys.stderr)
            sys.exit(1)
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)
        return

    # ── --api ──
    if args.api not in SUPPORTED_APIS:
        print(f"Error: 不支持的接口 '{args.api}'", file=sys.stderr)
        print(f"共 {len(SUPPORTED_APIS)} 个接口，用 --api help 查看完整列表", file=sys.stderr)
        sys.exit(1)

    try:
        body = json.loads(args.params)
    except json.JSONDecodeError as e:
        print(f"Error: --params 不是合法 JSON: {e}", file=sys.stderr)
        sys.exit(1)

    # 自动注入 SID
    env_sid = os.environ.get("LINGXING_SID")
    if env_sid and "sid" not in body and "profile_id" not in body:
        try:
            body["sid"] = int(env_sid)
            print(f"[info] 已从环境变量注入 sid={body['sid']}", file=sys.stderr)
        except ValueError:
            print(f"Warning: LINGXING_SID='{env_sid}' 不是整数，已忽略", file=sys.stderr)

    try:
        if args.fetch_all:
            data = call_api_all(app_id, token, args.api, body, args.page_size)
            result = {"total": len(data), "data": data}
        else:
            result = call_api(app_id, token, args.api, body)
    except Exception as e:
        print(f"Error: API 调用失败: {e}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
