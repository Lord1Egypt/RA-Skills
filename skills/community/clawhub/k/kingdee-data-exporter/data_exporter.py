# -*- coding: utf-8 -*-
# 金蝶 K3Cloud 经营数据（多表）导出脚本
#
# 说明：
# - 本文件是一个自包含版本，用于随 Skill 目录一起发布
# - 配置位于同目录 `config.py`

import requests
import json
import sys
import os
import copy
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from config import KINGDEE_CONFIG, WECHAT_CONFIG

try:
    import pandas as pd
except ModuleNotFoundError:
    print("缺少依赖库 pandas。请执行：python -m pip install -r requirements.txt")
    raise


class SalesDataExporter:
    """销售单据数据导出器"""

    def __init__(self, start_date=None, end_date=None, no_wechat=False, org_numbers=None, only=None):
        self.kingdee_config = KINGDEE_CONFIG
        self.wechat_webhook = (WECHAT_CONFIG or {}).get("webhook", "")
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.base_url = self.kingdee_config["base_url"] + "/k3cloud/"

        self.no_wechat = no_wechat
        self.only = self._normalize_only(only)
        self.requested_org_numbers = self._parse_org_numbers(org_numbers) if org_numbers else None

        # 日期范围：默认 1-6 号导出上月整月，7 号及以后导出当月 1 号到今天
        if start_date and end_date:
            self.start_date = start_date
            self.end_date = end_date
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            self.period_name = start_dt.strftime("%Y年%m月")
            self.year = start_dt.year
            self.period = start_dt.month
        else:
            today = datetime.now()
            if today.day <= 6:
                first_day_this_month = today.replace(day=1)
                last_day_last_month = first_day_this_month - timedelta(days=1)
                first_day_last_month = last_day_last_month.replace(day=1)
                self.start_date = first_day_last_month.strftime("%Y-%m-%d")
                self.end_date = last_day_last_month.strftime("%Y-%m-%d")
                self.period_name = last_day_last_month.strftime("%Y年%m月")
                self.year = last_day_last_month.year
                self.period = last_day_last_month.month
            else:
                first_day_this_month = today.replace(day=1)
                self.start_date = first_day_this_month.strftime("%Y-%m-%d")
                self.end_date = today.strftime("%Y-%m-%d")
                self.period_name = today.strftime("%Y年%m月")
                self.year = today.year
                self.period = today.month

        # 默认不写死任何组织编码/公司名；登录后按 --org 或系统组织动态解析
        self.target_settle_org_numbers = []
        self.default_settle_org_id_map = {}
        self.sale_org_numbers = []
        self.inventory_org_number = None
        self.bill_configs = self._build_bill_configs()
        self.report_configs = self._build_report_configs()

        print(f"查询{self.period_name}数据，日期范围: {self.start_date} 至 {self.end_date}")

    def _build_bill_configs(self):
        sale_org_filter = self._build_org_filter("FSaleOrgId.FNumber", self.sale_org_numbers)
        settle_org_filter = self._build_org_filter("FSETTLEORGID.FNumber", self.target_settle_org_numbers)
        pay_org_filter = self._build_org_filter("FPAYORGID.FNumber", self.target_settle_org_numbers)
        purchase_org_filter = self._build_org_filter("FPurchaseOrgId.FNumber", self.target_settle_org_numbers)

        return [
            {
                "form_id": "SAL_OUTSTOCK",
                "bill_name": "销售出库单",
                "field_keys": "FBillNo,FDate,FCustomerID.FName,FBillTypeID.FName,FSaleDeptID.FName,FSalesManID.FName,FNote,FMaterialID.FName,FStockID.FName,FEntryTaxAmount,FAmount,FAllAmount,FEntryCostAmount",
                "filter_string": f"{sale_org_filter} AND FDate>='{self.start_date}' AND FDate<='{self.end_date}' AND FDocumentStatus='C'",
                "columns": ["单据编号", "日期", "客户", "单据类型", "销售部门", "销售员", "备注", "物料名称", "仓库", "税额", "金额", "价税合计", "总成本"],
            },
            {
                "form_id": "SAL_SaleOrder",
                "bill_name": "销售订单",
                "field_keys": "FDate,FBillTypeID.FName,FBillNo,FDocumentStatus,FCustId.FName,FSaleDeptId.FName,FSalerId.FName,FCreatorId.FName,FCloseStatus,FMaterialId.FNumber,FMaterialName,FUnitID.FName,FQty,FPrice,FEntryTaxAmount,FAllAmount,FDeliveryDate",
                "filter_string": f"{sale_org_filter} AND FDate>='{self.start_date}' AND FDate<='{self.end_date}'",
                "columns": ["日期", "单据类型", "单据编号", "单据状态", "客户", "销售部门", "销售员", "创建人", "关闭状态", "物料编码", "物料名称", "销售单位", "销售数量", "单价", "税额", "价税合计", "要货日期"],
            },
            {
                "form_id": "SAL_RETURNSTOCK",
                "bill_name": "销售退货单",
                "field_keys": "FBillNo,FDate,FRetcustId.FName,FBillTypeID.FName,FSaledeptid.FName,FSalesManId.FName,FHeadNote,FMaterialId.FName,FStockId.FName,FEntryTaxAmount,FAmount,FAllAmount,FEntryCostAmount",
                "filter_string": f"{sale_org_filter} AND FDate>='{self.start_date}' AND FDate<='{self.end_date}' AND FDocumentStatus='C'",
                "columns": ["单据编号", "日期", "退货客户", "单据类型", "销售部门", "销售员", "备注", "物料名称", "仓库", "税额", "金额", "价税合计", "总成本"],
            },
            {
                "form_id": "AR_receivable",
                "bill_name": "手工标准应收单",
                "field_keys": "FBillTypeID.FName,FBillNo,FDATE,FCUSTOMERID.FName,FSALEORGID.FName,FSALEDEPTID.FName,FMATERIALID.FName,FTAXAMOUNTFOR_D,FNoTaxAmountFor_D,FALLAMOUNTFOR_D,FCreatorId.FName,FAR_Remark",
                "filter_string": f"{self._build_org_filter('FSALEORGID.FNumber', self.target_settle_org_numbers)} AND FDATE>='{self.start_date}' AND FDATE<='{self.end_date}' AND FDocumentStatus='C' AND FBillTypeID.FName='手工标准应收单'",
                "columns": ["单据类型", "单据编号", "业务日期", "客户", "销售组织", "销售部门", "物料名称", "税额", "不含税金额", "价税合计", "创建人", "备注"],
            },
            {
                "form_id": "AP_Payable",
                "bill_name": "应付单",
                "field_keys": "FBillTypeID.FName,FDATE,FSUPPLIERID.FName,FBillNo,FSETTLEORGID.FName,FPURCHASEDEPTID.FName,FMATERIALID.FName,FCostName,FCOSTDEPARTMENTID.FName,FCreatorId.FName,FTAXAMOUNTFOR_D,FNOTAXAMOUNT_D,FALLAMOUNT_D,FAP_Remark",
                "filter_string": f"{settle_org_filter} AND FDATE>='{self.start_date}' AND FDATE<='{self.end_date}' AND FDOCUMENTSTATUS='C'",
                "columns": ["单据类型", "业务日期", "供应商", "单据编号", "结算组织", "采购部门", "物料名称", "费用项目名称", "费用承担部门", "创建人", "税额", "不含税金额本位币", "价税合计本位币", "备注"],
            },
            {
                "form_id": "PUR_PurchaseOrder",
                "bill_name": "采购订单",
                "field_keys": "FBillNo,FDate,FSupplierId.FName,FDocumentStatus,FPurchaseOrgId.FName,FPurchaserId.FName,FCreatorId.FName,FCloseStatus,F_TJKT_ChangeReason_re5,FMaterialId.FNumber,FMaterialName,FUnitId.FName,FQty,FDeliveryDate,FPrice,FEntryTaxAmount,FAllAmount,FGiveAway",
                "filter_string": f"{purchase_org_filter} AND FDate>='{self.start_date}' AND FDate<='{self.end_date}'",
                "columns": ["单据编号", "采购日期", "供应商", "单据状态", "采购组织", "采购员", "创建人", "关闭状态", "摘要", "物料编码", "物料名称", "采购单位", "采购数量", "交货日期", "单价", "税额", "价税合计", "是否赠品"],
            },
            {
                "form_id": "AP_PAYBILL",
                "bill_name": "付款单",
                "field_keys": "FBillTypeID.FName,FBillNo,FDATE,FCONTACTUNITTYPE,FCONTACTUNIT.FName,FREMARK,FSETTLETYPEID.FName,FPURPOSEID.FName,FPAYORGID.FName,FCOSTID.FName,FEXPENSEDEPTID_E.FName,FHANDLINGCHARGEFOR,FREALPAYAMOUNTFOR_D",
                "filter_string": f"{pay_org_filter} AND FDATE>='{self.start_date}' AND FDATE<='{self.end_date}' AND FDOCUMENTSTATUS='C'",
                "columns": ["单据类型", "单据编号", "业务日期", "往来单位类型", "往来单位", "备注", "结算方式", "付款用途", "付款组织", "费用项目", "费用承担部门", "手续费", "表体-实付金额"],
            },
            {
                "form_id": "AR_RECEIVEBILL",
                "bill_name": "收款单",
                "field_keys": "FBillTypeID.FName,FBillNo,FDATE,FCONTACTUNITTYPE,FSETTLETYPEID.FName,FPURPOSEID.FName,FPAYORGID.FName,FSALEDEPTID.FName,FCONTACTUNIT.FName,FREMARK,FHANDLINGCHARGEFOR,FREALRECAMOUNTFOR_D",
                "filter_string": f"{pay_org_filter} AND FDATE>='{self.start_date}' AND FDATE<='{self.end_date}' AND FDOCUMENTSTATUS='C'",
                "columns": ["单据类型", "单据编号", "业务日期", "往来单位类型", "结算方式", "收款用途", "收款组织", "销售部门", "往来单位", "备注", "手续费", "表体-实收金额"],
            },
            {
                "form_id": "AP_REFUNDBILL",
                "bill_name": "付款退款单",
                "field_keys": "FBillTypeID.FName,FBillNo,FDATE,FCONTACTUNIT.FName,FPAYUNIT.FName,FSETTLETYPEID.FName,FPURPOSEID.FName,FREALREFUNDAMOUNTFOR_D,FPAYORGID.FName,FDepartment.FName,FEXPENSEDEPTID_E.FName,FCOSTID.FName,FREMARK",
                "filter_string": f"{pay_org_filter} AND FDATE>='{self.start_date}' AND FDATE<='{self.end_date}' AND FDOCUMENTSTATUS='C'",
                "columns": ["单据类型", "单据编号", "业务日期", "往来单位", "付款单位", "结算方式", "原付款用途", "表体-实退金额", "付款组织", "部门", "费用承担部门", "费用项目", "备注"],
            },
            {
                "form_id": "AR_REFUNDBILL",
                "bill_name": "收款退款单",
                "field_keys": "FBillTypeID.FName,FBillNo,FDATE,FCONTACTUNIT.FName,FSETTLETYPEID.FName,FPURPOSEID.FName,FREFUNDAMOUNTFOR_E,FPAYORGID.FName,FSALEDEPTID.FName,FREMARK",
                "filter_string": f"{pay_org_filter} AND FDATE>='{self.start_date}' AND FDATE<='{self.end_date}' AND FDOCUMENTSTATUS='C'",
                "columns": ["单据类型", "单据编号", "业务日期", "往来单位", "结算方式", "原收款用途", "表体-实退金额", "付款组织", "销售部门", "备注"],
            },
            {
                "form_id": "AP_OtherPayable",
                "bill_name": "其他应付单",
                "field_keys": "FBillTypeID.FName,FBillNo,FDATE,FCONTACTUNITTYPE,FCONTACTUNIT.FName,FTOTALAMOUNTFOR_H,FCOSTNAME,FDEPARTMENTID.FName,FSETTLEORGID.FName,FCreatorId.FName",
                "filter_string": f"{settle_org_filter} AND FDATE>='{self.start_date}' AND FDATE<='{self.end_date}' AND FDOCUMENTSTATUS='C'",
                "columns": ["单据类型", "单据编号", "业务日期", "往来单位类型", "往来单位", "总金额", "费用项目名称", "申请部门", "结算组织", "创建人"],
            },
            {
                "form_id": "AR_OtherRecAble",
                "bill_name": "其他应收单",
                "field_keys": "FBillTypeID.FName,FBillNo,FDATE,FCONTACTUNITTYPE,FCONTACTUNIT.FName,FAMOUNTFOR,FCOSTNAME,FDEPARTMENTID.FName,FSETTLEORGID.FName,FCreatorId.FName",
                "filter_string": f"{settle_org_filter} AND FDATE>='{self.start_date}' AND FDATE<='{self.end_date}' AND FDOCUMENTSTATUS='C'",
                "columns": ["单据类型", "单据编号", "业务日期", "往来单位类型", "往来单位", "总金额", "费用项目名称", "申请部门", "结算组织", "创建人"],
            },
            {
                "form_id": "AP_AdjustExchangeRate",
                "bill_name": "应付调汇单",
                "field_keys": "FBillNo,FCONTACTUNITTYPE,FCONTACTUNIT.FName,FBUSINESSDEPTID.FName,FDATE,FADJEXCAMOUNT",
                "filter_string": f"{settle_org_filter} AND FDATE>='{self.start_date}' AND FDATE<='{self.end_date}' AND FDOCUMENTSTATUS='C'",
                "columns": ["单据编号", "往来单位类型", "往来单位", "业务部门", "业务日期", "调汇金额"],
            },
        ]

    def _build_report_configs(self):
        inventory_org_number = self.inventory_org_number or (self.target_settle_org_numbers[0] if self.target_settle_org_numbers else "")

        return [
            {
                "form_id": "AP_SumReport",
                "report_name": "应付款汇总表",
                "field_keys": "FCONTACTUNITNUMBER,FCONTACTUNITNAME,FSETTLEORGNAME,FINITAMOUNT,FAMOUNT,FREALAMOUNT,FOFFAMOUNT,FLEFTAMOUNT",
                "model": {
                    "FCONTACTUNITTYPE": "供应商",
                    "FUSEDATE": "true",
                    "FBeginDate": self.start_date,
                    "FEndDate": self.end_date,
                    "FSettleOrgLst": "1",
                    "FOutSettle": "true",
                    "FInSettle": "false",
                },
                "columns": ["往来单位编码", "往来单位名称", "结算组织", "(本位币)期初余额", "(本位币)本期应付", "(本位币)本期付款", "(本位币)本期冲销额", "(本位币)期末余额"],
            },
            {
                "form_id": "AR_SumReport",
                "report_name": "应收款汇总表",
                "field_keys": "FCONTACTUNITNUMBER,FCONTACTUNITNAME,FSETTLEORGNAME,FINITAMOUNTFOR,FAMOUNTFOR,FREALAMOUNTFOR,FOFFAMOUNTFOR,FLEFTAMOUNTFOR",
                "model": {
                    "FCONTACTUNITTYPE": "客户",
                    "FUSEDATE": "true",
                    "FBeginDate": self.start_date,
                    "FEndDate": self.end_date,
                    "FSettleOrgLst": "",
                    "FOutSettle": "true",
                    "FInSettle": "false",
                },
                "columns": ["往来单位编码", "往来单位名称", "结算组织", "(原币)期初余额", "(原币)本期应收", "(原币)本期收款", "(原币)本期冲销额", "(原币)期末余额"],
            },
            {
                "form_id": "HS_INOUTSTOCKSUMMARYRPT",
                "report_name": "存货收发存汇总表",
                "field_keys": "FMATERIALBASEID,FMATERIALNAME,FMATERIALGROUP,FSTOCKId,FINITQty,FINITPrice,FINITAMOUNT,FRECEIVEQty,FRECEIVEPrice,FRECEIVEAmount,FSENDQty,FSENDPrice,FSENDAmount,FENDQty,FENDPrice,FENDAmount",
                "model": {
                    "FACCTGSYSTEMID": {"FNumber": "KJHSTX01_SYS"},
                    "FACCTGORGID": {"FNumber": inventory_org_number},
                    "FACCTPOLICYID": {"FNumber": "KJZC01_SYS"},
                    "FYear": str(self.year),
                    "FPeriod": str(self.period),
                    "FENDYEAR": str(self.year),
                    "FEndPeriod": str(self.period),
                    "FCOMBOTotalType": "不汇总",
                    "FDimType": "FMATERIALID,FSTOCKID",
                    "FIsDisplayPeriod": True,
                },
                "columns": ["物料编码", "物料名称", "物料分组", "仓库", "期初数量", "期初单价", "期初金额", "收入数量", "收入单价", "收入金额", "发出数量", "发出单价", "发出金额", "期末数量", "期末单价", "期末金额"],
            },
            {
                "form_id": "HS_NoDimInOutStockDetailRpt",
                "report_name": "存货收发存明细表",
                "field_keys": "FPERIOD,FBILLDATE,FBILLNO,FBUSINESSTYPE,FBillFormName,FMATERIALID,FMATERIALNAME,FRECEIVEQty,FRECEIVEPrice,FRECEIVEAmount,FSENDQty,FSENDPrice,FSENDAmount,FENDQty,FENDPrice,FENDAmount",
                "model": {
                    "FACCTGSYSTEMID": {"FNumber": "KJHSTX01_SYS"},
                    "FACCTGORGID": {"FNumber": inventory_org_number},
                    "FACCTPOLICYID": {"FNumber": "KJZC01_SYS"},
                    "FYear": str(self.year),
                    "FENDYEAR": str(self.year),
                    "FPeriod": str(self.period),
                    "FEndPeriod": str(self.period),
                },
                "columns": ["期间", "单据日期", "单据编号", "业务类型", "单据类型", "物料编码", "物料名称", "收入数量", "收入单价", "收入金额", "发出数量", "发出单价", "发出金额", "期末数量", "期末单价", "期末金额"],
            },
            {
                "form_id": "CN_FundPositionReport",
                "report_name": "资金头寸表",
                "field_keys": "FRowTypeName,FBankName,FBankAcctName,FBankAcctNo,FPAYORGNAME,FINNERACCTNAME,FINNERACCTNO,FForCurrencyName,FForLastBal,FForTodayIn,FForTodayOut,FForTodayBal,FLocalCurrencyName,FLocalLastBal,FLocalTodayIn,FLocalTodayOut,FLocalTodayBal,FInCount,FOutCount",
                "model": {
                    "FOrgId": [{"FNumber": number} for number in self.target_settle_org_numbers],
                    "FStartDate": f"{self.start_date} 00:00:00",
                    "FEndDate": f"{self.end_date} 00:00:00",
                    "FNotAudit": False,
                    "FInNOut": True,
                    "FMyCurrency": False,
                    "FCurrencySubTotal": False,
                    "FSettleOrgBox": False,
                    "FPAYORGIDBOX": True,
                    "FMyCurrencySum": False,
                    "FMyPayOrg": False,
                    "FGroupCash": False,
                    "FOrgOrAccount": "0",
                    "FAllCashAccount": True,
                    "FAllBankAccount": False,
                    "FIsShowCancelBankAcnt": False,
                    "FINCLUDEEMPTY": False,
                },
                "columns": ["资金类别", "银行", "账户名称", "银行账号", "收付组织", "内部账户名称", "内部账户", "原币币别", "原币期初余额", "原币本日收入", "原币本日支出", "原币本日余额", "本位币币别", "本位币期初余额", "本位币本日收入", "本位币本日支出", "本位币本日余额", "收入笔数", "支出笔数"],
            },
        ]

    def _resolve_org_scope_after_login(self):
        if self.requested_org_numbers and self.requested_org_numbers != ["all"]:
            resolved_org_numbers = self.requested_org_numbers
        else:
            all_orgs = self.get_all_organizations()
            resolved_org_numbers = [o.get("number") for o in all_orgs if o.get("number")]
            resolved_org_numbers = [n for n in resolved_org_numbers if n]
            if self.requested_org_numbers == ["all"] and not resolved_org_numbers:
                raise RuntimeError("未能从金蝶查询到组织列表，无法使用 --org all")

        self.target_settle_org_numbers = resolved_org_numbers
        self.sale_org_numbers = list(resolved_org_numbers)
        self.inventory_org_number = resolved_org_numbers[0] if resolved_org_numbers else None
        self.bill_configs = self._build_bill_configs()
        self.report_configs = self._build_report_configs()

    def _normalize_only(self, only):
        if not only:
            return None
        if isinstance(only, str):
            parts = [p.strip() for p in only.split(",") if p.strip()]
        else:
            parts = [str(p).strip() for p in (only or []) if str(p).strip()]
        lowered = {p.lower() for p in parts}
        return lowered or None

    def _parse_org_numbers(self, org_numbers):
        if isinstance(org_numbers, str):
            raw = org_numbers.strip()
            if raw.lower() == "all":
                return ["all"]
            parts = [p.strip() for p in raw.split(",") if p.strip()]
            return parts
        return [str(x).strip() for x in (org_numbers or []) if str(x).strip()]

    def _build_org_filter(self, field_name, org_numbers):
        org_numbers = [str(x).strip() for x in (org_numbers or []) if str(x).strip()]
        if not org_numbers:
            return "1=1"
        if len(org_numbers) == 1:
            return f"{field_name}='{org_numbers[0]}'"
        in_values = ",".join([f"'{n}'" for n in org_numbers])
        return f"{field_name} IN ({in_values})"

    def resolve_settle_org_ids_by_numbers(self, org_numbers, default_map=None):
        """根据组织编码解析结算组织内码，并返回逗号拼接字符串。"""
        default_map = default_map or {}
        org_id_map = dict(default_map)

        need_query_numbers = [number for number in org_numbers if number not in org_id_map]

        if need_query_numbers:
            url = self.base_url + "Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.ExecuteBillQuery.common.kdsvc"
            in_values = ",".join([f"'{number}'" for number in need_query_numbers])
            data = {
                "FormId": "AP_Payable",
                "FieldKeys": "FSETTLEORGID,FSETTLEORGID.FNumber,FSETTLEORGID.FName",
                "FilterString": f"FSETTLEORGID.FNumber IN ({in_values})",
                "OrderString": "",
                "TopRowCount": 0,
                "StartRow": 0,
                "Limit": 2000,
            }
            payload = {"formid": "AP_Payable", "data": json.dumps(data, ensure_ascii=False)}

            try:
                response = self.session.post(url, json=payload, timeout=60)
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list):
                        for row in result:
                            if not isinstance(row, list) or len(row) < 2:
                                continue
                            org_id = str(row[0]).strip()
                            org_number = str(row[1]).strip()
                            if org_id and org_number and org_number not in org_id_map:
                                org_id_map[org_number] = org_id
                else:
                    print(f"  [WARN] 组织内码查询失败，状态码: {response.status_code}")
            except Exception as e:
                print(f"  [WARN] 组织内码查询异常: {e}")

        settle_org_ids = [org_id_map[number] for number in org_numbers if number in org_id_map and org_id_map[number]]
        settle_org_lst = ",".join(settle_org_ids)
        print(f"  -> 结算组织内码映射: {org_id_map}")
        print(f"  -> FSettleOrgLst: {settle_org_lst or '[空]'}")
        return settle_org_lst

    def build_ap_sum_report_model(self, settle_org_lst):
        """构建应付款汇总表Model。"""
        return {
            "FAffiliation": {"FNAME": ""},
            "FSTARTYEAR": str(self.year),
            "FENDYEAR": str(self.year),
            "FCONTACTUNITTYPE": "BD_Supplier",
            "FSTARTPERIOD": str(self.period),
            "FENDPERIOD": str(self.period),
            "FCONTACTUNITFrom": {"FNumber": ""},
            "FUSEDATE": "true",
            "FSettleOrgLst": settle_org_lst,
            "FCONTACTUNITTo": {"FNumber": ""},
            "FAccountSystem": {"FNumber": ""},
            "FInSettle": "true",
            "FOutSettle": "true",
            "FUSEPERIOD": "",
            "FNoShowForNoLeft": "false",
            "FNoShowForNoOccur": "false",
            "FNOAUDIT": "false",
            "FEndDate": self.end_date,
            "FBeginDate": self.start_date,
            "FNoShowForBoth": "false",
            "FCurrencyFrom": [{"FNumber": ""}],
            "FIncludePayEvaluate": "false",
            "FIncludePayEvaluate_New": "false",
            "FDEFAULTACCTCALENDARID": 0,
            "FOnlyShowPayEvaluate": "false",
            "FOnlyShowPayEvaluate_New": "false",
            "FShowLocal": "true",
            "FShowSumLocal": "false",
            "FNoPrePayment": "false",
            "FOnlyShowPrePayment": "false",
            "FShowAmountInCost": "false",
            "FCONTACTUNITMUL": "",
            "FMULCONTACT": "false",
            "FPRESETBASE1": [{"FNumber": ""}],
            "FPRESETBASE2": [{"FNumber": ""}],
            "FGROUPSUPPLIER": "false",
            "FPERIODAMOUNT": -999999999,
            "FTOPERIODAMOUNT": 999999999,
            "FCheckPeriod": "false",
            "FShowMatchBill": "true",
            "FDateRadioGrp": "",
        }

    def build_ar_sum_report_model(self, settle_org_lst):
        """构建应收款汇总表Model。"""
        return {
            "FAffiliation": {"FNAME": ""},
            "FSTARTYEAR": str(self.year),
            "FENDYEAR": str(self.year),
            "FCONTACTUNITTYPE": "BD_Customer",
            "FSTARTPERIOD": str(self.period),
            "FENDPERIOD": str(self.period),
            "FCONTACTUNITFrom": {"FNumber": ""},
            "FUSEDATE": "true",
            "FSettleOrgLst": settle_org_lst,
            "FCONTACTUNITTo": {"FNumber": ""},
            "FAccountSystem": {"FNumber": ""},
            "FInSettle": "true",
            "FOutSettle": "true",
            "FUSEPERIOD": "",
            "FNoShowForNoLeft": "false",
            "FNoShowForNoOccur": "false",
            "FNOAUDIT": "false",
            "FEndDate": self.end_date,
            "FBeginDate": self.start_date,
            "FNoShowForBoth": "false",
            "FCurrencyFrom": [{"FNumber": ""}],
            "FIncludePayEvaluate": "false",
            "FIncludePayEvaluate_New": "false",
            "FDEFAULTACCTCALENDARID": 0,
            "FOnlyShowPayEvaluate": "false",
            "FOnlyShowPayEvaluate_New": "false",
            "FShowLocal": "true",
            "FGroupCustomer": "false",
            "FShowSumLocal": "false",
            "FNoPreReceive": "false",
            "FOnlyShowPreReceive": "false",
            "FCONTACTUNITMUL": "",
            "FMULCONTACT": "false",
            "FPRESETBASE1": [{"FNumber": ""}],
            "FPRESETBASE2": [{"FNumber": ""}],
            "FEXCLUDEB2CAR": "false",
            "FPERIODAMOUNT": -999999999,
            "FTOPERIODAMOUNT": 999999999,
            "FCheckPeriod": "false",
            "FShowMatchBill": "true",
            "FDateRadioGrp": "",
        }

    def login_kingdee(self):
        """登录金蝶云"""
        login_data = {
            "acctid": self.kingdee_config["acctid"],
            "username": self.kingdee_config["username"],
            "password": self.kingdee_config["password"],
            "lcid": 2052,
        }

        url = self.base_url + "Kingdee.BOS.WebApi.ServicesStub.AuthService.ValidateUser.common.kdsvc"

        try:
            response = self.session.post(url, json=login_data, timeout=30)
            if response.status_code == 200:
                result = response.json()
                if result.get("LoginResultType") == 1:
                    print("登录成功")
                    return True
            print("登录失败")
            return False
        except Exception as e:
            print(f"登录异常: {e}")
            return False

    def get_all_organizations(self):
        """
        尝试从金蝶查询所有组织（用于 --org all / --list-orgs）。
        说明：不同环境的组织基础资料 FormId / 字段名可能有差异，这里做多种兜底尝试。
        """
        if not self.login_kingdee():
            raise RuntimeError("登录失败，无法查询组织列表")

        candidates = [
            ("ORG_Organizations", "FOrgId,FNumber,FName,FForbidStatus"),
            ("ORG_Organizations", "FOrgID,FNumber,FName,FForbidStatus"),
            ("BD_Organization", "FOrgId,FNumber,FName,FForbidStatus"),
            ("ORG_Organizations", "FNumber,FName"),
            ("BD_Organization", "FNumber,FName"),
        ]

        url = self.base_url + "Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.ExecuteBillQuery.common.kdsvc"

        for form_id, field_keys in candidates:
            data = {
                "formid": form_id,
                "data": json.dumps(
                    {
                        "FormId": form_id,
                        "FieldKeys": field_keys,
                        "FilterString": "",
                        "OrderString": "FNumber",
                        "TopRowCount": 0,
                        "StartRow": 0,
                        "Limit": 2000,
                    },
                    ensure_ascii=False,
                ),
            }
            try:
                resp = self.session.post(url, json=data, timeout=60)
                if resp.status_code != 200:
                    continue
                result = resp.json()
                if not isinstance(result, list):
                    continue

                rows = []
                for row in result:
                    if not isinstance(row, list) or len(row) < 2:
                        continue
                    number = str(row[1]).strip() if len(row) >= 2 else ""
                    name = str(row[2]).strip() if len(row) >= 3 else ""
                    org_id = str(row[0]).strip() if len(row) >= 1 else ""
                    rows.append({"id": org_id, "number": number, "name": name, "form_id": form_id})
                if any(r.get("number") for r in rows):
                    dedup = {}
                    for r in rows:
                        key = r.get("number") or r.get("name") or r.get("id")
                        if not key:
                            continue
                        dedup[key] = r
                    rows = list(dedup.values())
                    rows.sort(key=lambda x: x.get("number") or "")
                    return rows
            except Exception:
                continue

        raise RuntimeError("查询组织列表失败：请检查金蝶环境中组织基础资料的 FormId/字段是否不同")

    def get_bill_data_with_filter(self, form_id, field_keys, filter_string):
        """使用字段和过滤条件获取单据数据"""
        all_data = []
        start_row = 0
        limit = 2000

        url = self.base_url + "Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.ExecuteBillQuery.common.kdsvc"

        print("  正在获取数据...")

        while True:
            data = {
                "formid": form_id,
                "data": json.dumps(
                    {
                        "FormId": form_id,
                        "FieldKeys": field_keys,
                        "FilterString": filter_string,
                        "OrderString": "",
                        "TopRowCount": 0,
                        "StartRow": start_row,
                        "Limit": limit,
                    }
                ),
            }

            try:
                response = self.session.post(url, json=data, timeout=60)

                if response.status_code == 200:
                    result = response.json()

                    if isinstance(result, list) and len(result) > 0:
                        all_data.extend(result)
                        print(f"  已获取 {len(all_data)} 条数据...")

                        if len(result) < limit:
                            break

                        start_row += limit
                    else:
                        break
                else:
                    print(f"  API请求失败: {response.status_code}")
                    print(f"  响应内容: {response.text[:500]}")
                    break

            except Exception as e:
                print(f"  获取数据异常: {e}")
                import traceback

                traceback.print_exc()
                break

        print(f"  共获取到 {len(all_data)} 条数据")
        return all_data

    def get_report_data(self, form_id, field_keys, model):
        """使用GetSysReportData接口获取报表数据"""
        all_data = []
        start_row = 0
        limit = 10000

        url = self.base_url + "Kingdee.BOS.WebApi.ServicesStub.DynamicFormService.GetSysReportData.common.kdsvc"

        print("  正在获取报表数据...")

        while True:
            data = {
                "FieldKeys": field_keys,
                "SchemeId": "",
                "StartRow": start_row,
                "Limit": limit,
                "IsVerifyBaseDataField": True,
                "FilterString": [],
                "Model": model,
            }

            payload = {"formid": form_id, "data": json.dumps(data, ensure_ascii=False)}

            try:
                response = self.session.post(url, json=payload, timeout=120)

                if response.status_code == 200:
                    result = response.json()

                    if not result.get("Result", {}).get("IsSuccess", False):
                        error_msg = result.get("Result", {}).get("Message", "未知错误")
                        print(f"  API返回错误: {error_msg}")
                        print(f"  调试信息 - 完整响应: {json.dumps(result, ensure_ascii=False, indent=2)}")
                        break

                    rows = result.get("Result", {}).get("Rows", [])
                    row_count = result.get("Result", {}).get("RowCount", 0)

                    if rows and len(rows) > 0:
                        all_data.extend(rows)
                        print(f"  已获取 {len(all_data)} 条数据...")

                        if len(all_data) >= row_count or len(rows) < limit:
                            break

                        start_row += len(rows)
                    else:
                        break
                else:
                    print(f"  API请求失败: {response.status_code}")
                    print(f"  响应内容: {response.text[:500]}")
                    break

            except Exception as e:
                print(f"  获取报表数据异常: {e}")
                import traceback

                traceback.print_exc()
                break

        print(f"  共获取到 {len(all_data)} 条报表数据")
        return all_data

    def parse_report_to_dataframe(self, data, columns=None, form_id=None):
        """将报表数据解析为 DataFrame"""
        if not isinstance(data, list) or len(data) == 0:
            if columns:
                return pd.DataFrame(columns=columns)
            return pd.DataFrame()

        if columns:
            df = pd.DataFrame(data, columns=columns)
        else:
            df = pd.DataFrame(data)

        # 过滤 AP/AR 汇总表中的“小计/合计”等行（小计可能出现在前两列）
        if form_id in ("AP_SumReport", "AR_SumReport") and len(df.columns) >= 2:
            first_col = df.columns[0]
            second_col = df.columns[1]
            for col in (first_col, second_col):
                df = df[~(df[col].astype(str).str.contains("小计", na=False, regex=False))]
                df = df[~(df[col].astype(str).str.contains("合计", na=False, regex=False))]

        for col in df.columns:
            if "日期" in str(col) or "Date" in str(col):
                try:
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                    df[col] = df[col].dt.strftime("%Y-%m-%d")
                except Exception:
                    pass

        exclude_columns = []
        if form_id in ("AP_SumReport", "AR_SumReport") and len(df.columns) >= 3:
            exclude_columns = [df.columns[0], df.columns[1], df.columns[2]]
        if form_id == "HS_NoDimInOutStockDetailRpt" and len(df.columns) >= 1:
            if df.columns[0] not in exclude_columns:
                exclude_columns.append(df.columns[0])
        df = self._coerce_numeric_like_columns(df, exclude_columns=exclude_columns)

        if form_id in ("AP_SumReport", "AR_SumReport"):
            numeric_candidates = df.columns[3:]
        elif form_id == "HS_INOUTSTOCKSUMMARYRPT":
            numeric_candidates = [c for c in df.columns if c not in ["物料编码", "物料名称", "物料分组", "仓库"]]
        elif form_id == "HS_NoDimInOutStockDetailRpt":
            numeric_candidates = [c for c in df.columns if c not in ["期间", "单据日期", "单据编号", "业务类型", "单据类型", "物料编码", "物料名称"]]
        else:
            numeric_candidates = []

        for col in numeric_candidates:
            if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
                try:
                    df[col] = self._clean_numeric_series(df[col])
                except Exception:
                    pass

        return df

    def _clean_numeric_series(self, series):
        cleaned = self._normalize_numeric_text(series)
        return pd.to_numeric(cleaned, errors="coerce").fillna(0)

    def _normalize_numeric_text(self, series):
        if series is None:
            return series

        cleaned = series.astype(str)
        cleaned = cleaned.str.replace("\u00A0", "", regex=False)
        cleaned = cleaned.str.replace("\u3000", "", regex=False)
        cleaned = cleaned.str.replace(r"\s+", "", regex=True)
        cleaned = cleaned.str.strip()
        cleaned = cleaned.str.replace(",", "", regex=False)
        cleaned = cleaned.str.replace("，", "", regex=False)
        cleaned = cleaned.str.replace("￥", "", regex=False)
        cleaned = cleaned.str.replace("¥", "", regex=False)
        cleaned = cleaned.str.replace("$", "", regex=False)
        cleaned = cleaned.str.replace(r"^\((.*)\)$", r"-\1", regex=True)
        cleaned = cleaned.str.replace(r"^（(.*)）$", r"-\1", regex=True)
        cleaned = cleaned.str.replace(r"^(\d+(?:\.\d+)?)-$", r"-\1", regex=True)

        cleaned = cleaned.replace(
            {
                "": None,
                "None": None,
                "nan": None,
                "NaN": None,
                "-": None,
                "—": None,
                "–": None,
            }
        )
        return cleaned

    def _coerce_numeric_like_columns(self, df, exclude_columns=None):
        if df is None or df.empty:
            return df

        exclude_columns = set(exclude_columns or [])
        for col in df.columns:
            if col in exclude_columns:
                continue
            if pd.api.types.is_numeric_dtype(df[col]):
                continue
            if not pd.api.types.is_object_dtype(df[col]):
                continue

            series = df[col]
            cleaned = self._normalize_numeric_text(series)
            non_empty = cleaned.dropna()
            if non_empty.empty:
                continue

            numeric = pd.to_numeric(non_empty, errors="coerce")
            if numeric.notna().mean() >= 0.7:
                df[col] = self._clean_numeric_series(series)

        return df

    def build_fund_position_output(self, df):
        column_map = {
            "银行": "银行",
            "原币期初余额": "(原币)期初余额",
            "原币本日收入": "(原币)本期收入",
            "原币本日支出": "(原币)本期支出",
            "原币本日余额": "(原币)本期余额",
            "收入笔数": "收入笔数",
            "支出笔数": "支出笔数",
        }

        output_columns = list(column_map.values())
        if df is None or df.empty:
            return pd.DataFrame(columns=output_columns)

        df_selected = pd.DataFrame()
        for src_col, dst_col in column_map.items():
            if src_col in df.columns:
                df_selected[dst_col] = df[src_col]
            else:
                df_selected[dst_col] = 0

        numeric_cols = [col for col in df_selected.columns if col != "银行"]
        for col in numeric_cols:
            df_selected[col] = self._clean_numeric_series(df_selected[col])

        summary = {col: 0 for col in df_selected.columns}
        summary["银行"] = "合计"
        for col in numeric_cols:
            summary[col] = df_selected[col].sum()

        df_selected = pd.concat([df_selected, pd.DataFrame([summary])], ignore_index=True)

        for col in ["收入笔数", "支出笔数"]:
            if col in df_selected.columns:
                df_selected[col] = pd.to_numeric(df_selected[col], errors="coerce").fillna(0).astype(int)

        return df_selected[output_columns]

    def parse_data_to_dataframe(self, data, columns):
        """将数据解析为DataFrame，添加列名"""
        if not isinstance(data, list) or len(data) == 0:
            return pd.DataFrame(columns=columns)

        df = pd.DataFrame(data, columns=columns)

        date_columns = ["日期", "业务日期", "采购日期", "要货日期", "交货日期"]
        for col in date_columns:
            if col in df.columns:
                try:
                    df[col] = pd.to_datetime(df[col], errors="coerce")
                    df[col] = df[col].dt.strftime("%Y-%m-%d")
                except Exception as e:
                    print(f"  [WARN] 日期列 {col} 格式化失败: {e}")

        if "业务类型" in df.columns:
            business_type_map = {
                "NORMAL": "普通应付单",
                "DEFECT": "退货应付单",
                "CONSIGNMENT": "受托代销应付单",
                "COMMISSION": "委托代销应付单",
                "OTHERRECE": "其他应收单",
                "OTHERPAY": "其他应付单",
                "INITIALRECE": "期初应收单",
                "INITIALPAY": "期初应付单",
                "CG": "采购",
                "FY": "费用",
                "采购": "采购",
                "费用": "费用",
            }
            df["业务类型"] = df["业务类型"].map(lambda x: business_type_map.get(str(x), str(x)))

        if "往来单位类型" in df.columns:
            contact_type_map = {
                "BD_Customer": "客户",
                "BD_Supplier": "供应商",
                "HSWD01_SYS": "供应商",
                "ORG_Organizations": "组织机构",
                "BD_OtherOrg": "其他组织",
                "BD_Employee": "员工",
                "BD_Empinfo": "员工",
                "BD_BANK": "银行",
            }
            df["往来单位类型"] = df["往来单位类型"].map(lambda x: contact_type_map.get(str(x), str(x)))

        status_map = {
            "Z": "暂存",
            "A": "创建",
            "B": "审核中",
            "C": "已审核",
            "D": "重新审核",
        }
        close_status_map = {
            "A": "未关闭",
            "B": "已关闭",
        }
        giveaway_map = {
            "true": "是",
            "false": "否",
        }

        if "单据状态" in df.columns:
            df["单据状态"] = df["单据状态"].map(lambda x: status_map.get(str(x), str(x)))
        if "关闭状态" in df.columns:
            df["关闭状态"] = df["关闭状态"].map(lambda x: close_status_map.get(str(x), str(x)))
        if "是否赠品" in df.columns:
            df["是否赠品"] = df["是否赠品"].map(lambda x: giveaway_map.get(str(x).lower(), str(x)))

        return df

    def save_all_to_excel(self, dataframes_dict):
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"金蝶经营数据_{self.period_name}_{timestamp}.xlsx"

        try:
            with pd.ExcelWriter(filename, engine="openpyxl") as writer:
                for sheet_name, df in dataframes_dict.items():
                    df.to_excel(writer, sheet_name=sheet_name, index=False)

                    try:
                        ws = writer.sheets[sheet_name]
                        self._apply_excel_number_formats(sheet_name, df, ws)
                    except Exception as e:
                        print(f"  ! sheet {sheet_name} 数值格式设置失败: {e}")

            print(f"  Excel文件已生成: {filename}")
            return filename
        except Exception as e:
            print(f"  保存Excel失败: {e}")
            return None

    def _apply_excel_number_formats(self, sheet_name, df, ws):
        try:
            from openpyxl.styles import numbers
        except Exception:
            return

        if df is None or df.empty:
            return

        if sheet_name == "资金头寸表":
            amount_cols = ["(原币)期初余额", "(原币)本期收入", "(原币)本期支出", "(原币)本期余额"]
            count_cols = ["收入笔数", "支出笔数"]
        else:
            amount_cols = []
            count_cols = []

        for col_idx, col_name in enumerate(df.columns, start=1):
            series = df[col_name]
            if pd.api.types.is_integer_dtype(series):
                fmt = numbers.FORMAT_NUMBER_COMMA_SEPARATED1
            elif pd.api.types.is_float_dtype(series):
                fmt = "#,##0.00"
            else:
                fmt = None

            if sheet_name == "资金头寸表":
                if col_name in amount_cols:
                    fmt = "#,##0.00"
                if col_name in count_cols:
                    fmt = numbers.FORMAT_NUMBER_COMMA_SEPARATED1

            if not fmt:
                continue

            for row in range(2, 2 + len(df)):
                ws.cell(row=row, column=col_idx).number_format = fmt

    def _drop_rows_with_empty_contactunit_name(self, df, contactunit_name_col="往来单位名称"):
        if df is None or df.empty:
            return df
        if contactunit_name_col not in df.columns:
            return df
        series = df[contactunit_name_col]
        return df[series.notna() & (series.astype(str).str.strip() != "")]

    def send_summary_with_file(self, excel_file, bill_records):
        if self.no_wechat:
            print("  已跳过企业微信推送（--no-wechat）")
            return True
        if not self.wechat_webhook:
            print("  已跳过企业微信推送（WECHAT_CONFIG.webhook 为空）")
            return True

        try:
            file_size = os.path.getsize(excel_file)
            file_size_mb = file_size / (1024 * 1024)

            export_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            summary_lines = [
                "金蝶经营数据导出完成",
                "",
                f"数据周期: {self.period_name}",
                f"导出时间: {export_time}",
                "",
                "数据明细:",
            ]

            for idx, record in enumerate(bill_records, 1):
                summary_lines.append(f"  {idx}. {record['name']}: {record['count']} 条")

            summary_lines.append("")
            summary_lines.append("文件信息:")
            summary_lines.append(f"  文件名: {os.path.basename(excel_file)}")
            summary_lines.append(f"  大小: {file_size_mb:.2f} MB")

            summary_msg = "\n".join(summary_lines)

            payload = {"msgtype": "text", "text": {"content": summary_msg}}

            response = requests.post(self.wechat_webhook, json=payload, headers={"Content-Type": "application/json"})
            result = response.json()
            if result.get("errcode") == 0:
                print("  汇总消息发送成功")
                return True
            print(f"  汇总消息发送失败: {result}")
            return False
        except Exception as e:
            print(f"  发送汇总消息异常: {e}")
            return False

    def export_all_bills(self):
        print("=" * 60)
        print(f"销售单据数据导出 - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)

        try:
            if not self.login_kingdee():
                return False

            self._resolve_org_scope_after_login()

            all_dataframes = {}
            bill_records = []

            for config in self.bill_configs:
                form_id = config["form_id"]
                bill_name = config["bill_name"]
                if self.only and (form_id.lower() not in self.only) and (bill_name.lower() not in self.only):
                    continue
                field_keys = config["field_keys"]
                filter_string = config["filter_string"]
                columns = config["columns"]

                print(f"\n处理单据: {bill_name}")
                print("-" * 60)

                data = self.get_bill_data_with_filter(form_id, field_keys, filter_string)
                df = self.parse_data_to_dataframe(data, columns)

                record_count = len(df)
                bill_records.append({"name": bill_name, "count": record_count})
                all_dataframes[bill_name] = df

                if record_count == 0:
                    print(f"  [WARN] {bill_name} 无数据（将创建空表）")
                else:
                    print(f"  {bill_name} 获取到 {record_count} 条记录")

            for config in self.report_configs:
                form_id = config["form_id"]
                report_name = config["report_name"]
                if self.only and (form_id.lower() not in self.only) and (report_name.lower() not in self.only):
                    continue
                field_keys = config["field_keys"]
                model = copy.deepcopy(config["model"])
                columns = config["columns"]

                if form_id in ("AP_SumReport", "AR_SumReport"):
                    settle_org_lst = self.resolve_settle_org_ids_by_numbers(self.target_settle_org_numbers, self.default_settle_org_id_map)
                    if form_id == "AP_SumReport":
                        model = self.build_ap_sum_report_model(settle_org_lst)
                    else:
                        model = self.build_ar_sum_report_model(settle_org_lst)

                print(f"\n处理报表: {report_name}")
                print("-" * 60)

                data = self.get_report_data(form_id, field_keys, model)
                df = self.parse_report_to_dataframe(data, columns, form_id=form_id)

                if form_id in ("AR_SumReport", "AP_SumReport"):
                    df = self._drop_rows_with_empty_contactunit_name(df, contactunit_name_col="往来单位名称")

                if report_name == "资金头寸表":
                    df = self.build_fund_position_output(df)

                record_count = len(df)
                bill_records.append({"name": report_name, "count": record_count})
                all_dataframes[report_name] = df

                if record_count == 0:
                    print(f"  [WARN] {report_name} 无数据（将创建空表）")
                else:
                    print(f"  {report_name} 获取到 {record_count} 条记录")

            print("\n正在生成Excel文件...")
            excel_file = self.save_all_to_excel(all_dataframes)

            if not excel_file:
                print("  Excel生成失败")
                return False

            self.send_summary_with_file(excel_file, bill_records)

            print("\n生成的文件:")
            if os.path.exists(excel_file):
                print(f"  - {os.path.abspath(excel_file)}")

            print("=" * 60)
            print("导出任务完成")
            print("=" * 60)

            return True

        except Exception as e:
            print(f"导出任务异常: {e}")
            import traceback

            traceback.print_exc()
            return False


def main():
    start_date = None
    end_date = None
    no_wechat = False
    org_numbers = None
    only = None
    list_orgs = False
    show_config = False

    if "--start" in sys.argv:
        try:
            start_date = sys.argv[sys.argv.index("--start") + 1]
        except Exception:
            start_date = None
    if "--end" in sys.argv:
        try:
            end_date = sys.argv[sys.argv.index("--end") + 1]
        except Exception:
            end_date = None
    if "--no-wechat" in sys.argv:
        no_wechat = True
    if "--org" in sys.argv:
        try:
            org_numbers = sys.argv[sys.argv.index("--org") + 1]
        except Exception:
            org_numbers = None
    if "--only" in sys.argv:
        try:
            only = sys.argv[sys.argv.index("--only") + 1]
        except Exception:
            only = None
    if "--list-orgs" in sys.argv:
        list_orgs = True
    if "--show-config" in sys.argv:
        show_config = True

    exporter = SalesDataExporter(
        start_date=start_date,
        end_date=end_date,
        no_wechat=no_wechat,
        org_numbers=org_numbers,
        only=only,
    )

    if show_config:
        print("可用导出项（--only 可填 form_id 或名称，支持逗号分隔）：")
        print("-" * 60)
        for c in exporter.bill_configs:
            print(f"[BILL] {c['form_id']}  |  {c['bill_name']}")
        for c in exporter.report_configs:
            print(f"[RPT ] {c['form_id']}  |  {c['report_name']}")
        return

    if list_orgs:
        orgs = exporter.get_all_organizations()
        try:
            ts = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"组织列表_{ts}.xlsx"
            pd.DataFrame(orgs).to_excel(filename, index=False)
            print(f"组织列表已导出：{os.path.abspath(filename)}")
        except Exception as e:
            print(f"组织列表导出失败（将改为打印到控制台）：{e}")
            for o in orgs:
                print(f"{o.get('number')}\t{o.get('name')}")
        return

    success = exporter.export_all_bills()
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()

