#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快手生活服务 API 调用客户端

提供命令行接口快速调用快手生活服务 OpenAPI 接口
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import requests

# Import AccessTokenManager for automatic token management
from get_access_token import AccessTokenManager, load_current_context


class KuaishouClient:
    """快手生活服务 API 客户端"""

    BASE_URL = "https://lbs-open.kuaishou.com"
    
    def __init__(self, access_token: str):
        """
        初始化客户端
        
        Args:
            access_token: 访问令牌
        """
        self.access_token = access_token
        self.headers = {
            "Content-Type": "application/json",
            "access-token": access_token
        }
    
    def _get(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        发送 GET 请求
        
        Args:
            endpoint: API 端点
            params: 查询参数
            
        Returns:
            响应数据
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.get(url, headers=self.headers, params=params or {})
        return response.json()
    
    def _post(self, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        发送 POST 请求
        
        Args:
            endpoint: API 端点
            data: 请求数据
            
        Returns:
            响应数据
        """
        url = f"{self.BASE_URL}{endpoint}"
        response = requests.post(url, headers=self.headers, json=data or {})
        return response.json()
    
    # ==================== 商家账号管理 ====================
    
    def query_staff_user_info(self, staff_id: int) -> Dict:
        """
        查询商家某个子账号信息
        
        Args:
            staff_id: 子账号ID
            
        Returns:
            子账号信息
        """
        return self._post("/goodlife/v1/merchant/QueryStaffUserInfo", {"id": staff_id})
    
    def query_sub_accounts(
        self,
        staff_ks_user_id: str = "",
        current_page: int = 1,
        page_size: int = 10,
        **kwargs
    ) -> Dict:
        """
        查询商家子账号列表
        
        Args:
            staff_ks_user_id: 员工快手用户ID
            current_page: 当前页码
            page_size: 每页条数
            **kwargs: 其他查询参数
            
        Returns:
            子账号列表
        """
        data = {
            "staff_ks_user_id": staff_ks_user_id,
            "page_no": current_page,
            "page_size": page_size,
            "kwai_id": kwargs.get("kwai_id", ""),
            "remark": kwargs.get("remark", ""),
            "role_id": kwargs.get("role_id", ""),
            "mobile": kwargs.get("mobile", ""),
            "status": kwargs.get("status", ""),
            "data_resource_id": kwargs.get("data_resource_id", []),
            "data_type": kwargs.get("data_type", 0),
            "out_poi_id": kwargs.get("out_poi_id", "")
        }
        return self._post("/goodlife/v1/merchant/subAccounts", data)
    
    def query_todo_list(
        self,
        status: int = 1,
        current_page: int = 1,
        page_size: int = 10,
        **kwargs
    ) -> Dict:
        """
        查询商家待办事项列表
        
        Args:
            status: 状态(1:待处理)
            current_page: 当前页码
            page_size: 每页条数
            **kwargs: 其他查询参数
            
        Returns:
            待办事项列表
        """
        data = {
            "status": status,
            "currentPage": current_page,
            "pageSize": page_size,
            "kwaiId": kwargs.get("kwai_id", ""),
            "staffKsUserId": kwargs.get("staff_ks_user_id", ""),
            "remark": kwargs.get("remark", ""),
            "mobile": kwargs.get("mobile", ""),
            "dataResourceId": kwargs.get("data_resource_id", []),
            "dataType": kwargs.get("data_type", 0),
            "outPoiId": kwargs.get("out_poi_id", "")
        }
        return self._get("/goodlife/v1/workbench/todo_list", data)
    
    # ==================== 职人管理 ====================
    
    def query_artisan_list(
        self,
        current_page: int = 1,
        page_size: int = 10,
        city_code: str = "",
        uids: Optional[List[str]] = None
    ) -> Dict:
        """
        查询职人列表
        
        Args:
            current_page: 当前页码
            page_size: 每页条数
            city_code: 城市代码
            uids: 职人ID列表
            
        Returns:
            职人列表
        """
        data = {
            "uid": uids or [],
            "merchant_base_page_request": {
                "current_page": current_page,
                "page_size": page_size
            },
            "city_code": city_code
        }
        return self._post("/goodlife/v1/merchant/artisan_list", data)
    
    def query_auto_commission_info(self) -> Dict:
        """
        查询商家职人自动激励状态信息
        
        Returns:
            自动激励状态信息
        """
        return self._post("/goodlife/v1/artisan/QueryAutoCommissionInfo", {})
    
    def query_direct_commission(
        self,
        page: int = 1,
        page_size: int = 10,
        keyword: str = ""
    ) -> Dict:
        """
        查询职人的定向激励数据
        
        Args:
            page: 当前页码
            page_size: 每页条数
            keyword: 关键词
            
        Returns:
            定向激励数据
        """
        data = {
            "page": page,
            "page_size": page_size,
            "keyword": keyword
        }
        return self._post("/goodlife/rest/merchant/apicenter/artisan/direct/commission/page/query", data)
    
    # ==================== 经营数据查询 ====================
    
    def query_merchant_real_time_metric(self) -> Dict:
        """
        商家交易实时汇总信息
        
        Returns:
            实时汇总数据
        """
        data = {
            "distribute_type": "ALL",
            "module_key": "dataHomeTradeInfo"
        }
        return self._post("/goodlife/v1/merchant/QueryMerchantRealTimeMetric", data)
    
    def query_merchant_refund_info(self) -> Dict:
        """
        查询商家经营退款数据汇总
        
        Returns:
            退款数据汇总
        """
        data = {
            "metric_param": {
                "metric_key": "getLocallifeMerchantRefundInfo"
            }
        }
        return self._post("/goodlife/v1/metric/queryMetric", data)
    
    def query_artisan_data_overview(
        self,
        begin_date: str,
        end_date: str,
        artisan_id: Optional[str] = None
    ) -> Dict:
        """
        查询商家经营职人数据汇总或某个职人的经营数据汇总
        
        Args:
            begin_date: 开始日期(YYYYMMDD)
            end_date: 结束日期(YYYYMMDD)
            artisan_id: 职人ID(可选,传入则查询该职人数据)
            
        Returns:
            职人数据汇总
        """
        params = [
            {
                "param_name": "beginDate",
                "param_value": [end_date,begin_date]
            },
            {
                "param_name": "endDate",
                "param_value": [end_date,begin_date]
            }
        ]
        
        if artisan_id:
            params.append({
                "param_name": "artisanId",
                "param_value": [artisan_id]
            })
        
        data = {
            "metric_param": {
                "metric_key": "merchantArtisanDataHomePageOverview",
                "param": params
            }
        }
        return self._post("/goodlife/v1/metric/queryMetric", data)
    
    # ==================== 门店与评价管理 ====================
    
    def query_poi_rating_score(self, out_poi_id: str) -> Dict:
        """
        查询某个门店的用户评价评分
        
        Args:
            out_poi_id: 外部门店ID
            
        Returns:
            门店评分信息
        """
        return self._get(
            "/goodlife/rest/merchant/apicenter/pc/comment/poiRatingScore",
            {"out_poi_id": out_poi_id}
        )
    
    def query_poi_comment_list(self) -> Dict:
        """
        查询某个门店下最新的某些条件的评论
        
        Returns:
            评论列表
        """
        return self._get("/goodlife/rest/merchant/apicenter/pc/comment/poiCommentList")
    
    def query_comment_analysis(self) -> Dict:
        """
        查询评价分析
        
        Returns:
            评价分析数据
        """
        return self._post("/goodlife/rest/merchant/apicenter/metric/queryMetrics", {})
    
    # ==================== 商品激励管理 ====================
    
    def query_item_commission(
        self,
        page: int = 1,
        page_size: int = 10,
        commission_status: int = 10,
        item_id: str = ""
    ) -> Dict:
        """
        查询商家商品基础激励的总体状态
        
        Args:
            page: 当前页码
            page_size: 每页条数
            commission_status: 激励状态(10:激励中)
            item_id: 商品ID
            
        Returns:
            商品激励状态
        """
        params = {
            "page": page,
            "page_size": page_size,
            "commission_status": commission_status,
            "item_id": item_id,
            "scene": "itemBaseCommissionPage",
            "access-token": self.access_token
        }
        return self._get(
            "/goodlife/rest/merchant/apicenter/artisan/item/commission/page/query",
            params
        )
    
    # ==================== 物料与官号 ====================
    
    def query_qrcode_list(
        self,
        current_page: int = 1,
        page_size: int = 10,
        poi_ids: Optional[List[str]] = None
    ) -> Dict:
        """
        扫码物料
        
        Args:
            current_page: 当前页码
            page_size: 每页条数
            poi_ids: 门店ID列表
            
        Returns:
            物料列表
        """
        data = {
            "page_req": {
                "current_page": current_page,
                "page_size": page_size
            },
            "poi_ids": poi_ids or []
        }
        return self._post("/goodlife/rest/merchant/apicenter/poi/qrCode/list", data)
    
    def query_official_account(self) -> Dict:
        """
        查询官号
        
        Returns:
            官号信息
        """
        return self._post("/goodlife/rest/merchant/apicenter/officialAccount/queryOfficialAccountCardInfo", {})
    
    # ==================== 门店管理 ====================
    
    def query_poi_manage_list(
        self,
        poi_id: int,
        page: int = 1,
        page_size: int = 10
    ) -> Dict:
        """
        查询门店认领的审核信息
        
        Args:
            poi_id: 门店ID
            page: 当前页码
            page_size: 每页条数
            
        Returns:
            审核信息
        """
        data = {
            "poiId": poi_id,
            "page": page,
            "pageSize": page_size
        }
        return self._post("/goodlife/shopManage/poiMangeList", data)
    
    # ==================== 商家资质信息 ====================
    
    def query_all_contracts(self) -> Dict:
        """
        查询商家所有的合同信息
        
        Returns:
            合同信息列表
        """
        return self._get("/goodlife/queryMerchantAllContract")
    
    def query_brand_info_list(self) -> Dict:
        """
        查询商家的品牌资质列表
        
        Returns:
            品牌资质列表，其中某些字段值的含义：
            validStatus: 0:生效中 1:未生效
            applyStatus: 1:审核中 2:审核成功 3:审核失败
        """
        return self._get("/goodlife/invest/queryBrandInfoList")
    
    def query_merchant_area_list(self) -> Dict:
        """
        查询商家的区域列表
        
        Returns:
            区域列表
        """
        return self._post("/goodlife/merchantArea/queryList", {})
    
    # ==================== 应用授权 ====================
    
    def query_developer_auth_list(self) -> Dict:
        """
        查询已授权 & 未授权的应用列表
        
        Returns:
            应用列表
        """
        return self._get("/goodlife/rest/merchant/apicenter/developer/auth/list")


def print_json(data: Dict):
    """格式化输出 JSON"""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="快手生活服务 API 调用工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    

    
    # 子命令
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # ========== 商家账号管理 ==========
    
    # 查询子账号信息
    staff_info = subparsers.add_parser("staff-info", help="查询商家某个子账号信息")
    staff_info.add_argument("--id", type=int, required=True, help="子账号ID")
    
    # 查询子账号列表
    staff_list = subparsers.add_parser("staff-list", help="查询商家子账号列表")
    staff_list.add_argument("--staff-ks-user-id", default="", help="员工快手用户ID")
    staff_list.add_argument("--page", type=int, default=1, help="当前页码")
    staff_list.add_argument("--page-size", type=int, default=10, help="每页条数")
    
    # 查询待办事项
    todo_list = subparsers.add_parser("todo-list", help="查询商家待办事项列表")
    todo_list.add_argument("--status", type=int, default=1, help="状态(1:待处理)")
    todo_list.add_argument("--page", type=int, default=1, help="当前页码")
    todo_list.add_argument("--page-size", type=int, default=10, help="每页条数")
    
    # ========== 职人管理 ==========
    
    # 查询职人列表
    artisan_list = subparsers.add_parser("artisan-list", help="查询职人列表")
    artisan_list.add_argument("--page", type=int, default=1, help="当前页码")
    artisan_list.add_argument("--page-size", type=int, default=10, help="每页条数")
    artisan_list.add_argument("--city-code", default="", help="城市代码")
    
    # 查询自动激励状态
    subparsers.add_parser("auto-commission", help="查询商家职人自动激励状态信息")
    
    # 查询定向激励
    direct_commission = subparsers.add_parser("direct-commission", help="查询职人的定向激励数据")
    direct_commission.add_argument("--page", type=int, default=1, help="当前页码")
    direct_commission.add_argument("--page-size", type=int, default=10, help="每页条数")
    direct_commission.add_argument("--keyword", default="", help="关键词")
    
    # ========== 经营数据查询 ==========
    
    # 商家交易实时汇总
    subparsers.add_parser("real-time-metric", help="商家交易实时汇总信息")
    
    # 退款数据汇总
    subparsers.add_parser("refund-info", help="查询商家经营退款数据汇总")
    
    # 职人数据汇总
    artisan_data = subparsers.add_parser("artisan-data", help="查询商家经营职人数据汇总")
    artisan_data.add_argument("--begin-date", required=True, help="开始日期(YYYYMMDD)")
    artisan_data.add_argument("--end-date", required=True, help="结束日期(YYYYMMDD)")
    artisan_data.add_argument("--artisan-id", help="职人ID(可选)")
    
    # ========== 门店与评价管理 ==========
    
    # 门店评分
    poi_rating = subparsers.add_parser("poi-rating", help="查询某个门店的用户评价评分")
    poi_rating.add_argument("--poi-id", required=True, help="外部门店ID")
    
    # 评论列表
    subparsers.add_parser("comment-list", help="查询门店评论列表")
    
    # 评价分析
    subparsers.add_parser("comment-analysis", help="查询评价分析")
    
    # ========== 商品激励管理 ==========
    
    item_commission = subparsers.add_parser("item-commission", help="查询商家商品基础激励的总体状态")
    item_commission.add_argument("--page", type=int, default=1, help="当前页码")
    item_commission.add_argument("--page-size", type=int, default=10, help="每页条数")
    item_commission.add_argument("--status", type=int, default=10, help="激励状态(10:激励中)")
    item_commission.add_argument("--item-id", default="", help="商品ID")
    
    # ========== 物料与官号 ==========
    
    qrcode = subparsers.add_parser("qrcode", help="扫码物料")
    qrcode.add_argument("--page", type=int, default=1, help="当前页码")
    qrcode.add_argument("--page-size", type=int, default=10, help="每页条数")
    
    subparsers.add_parser("official-account", help="查询官号")
    
    # ========== 门店管理 ==========
    
    poi_manage = subparsers.add_parser("poi-manage", help="查询门店认领的审核信息")
    poi_manage.add_argument("--poi-id", type=int, required=True, help="门店ID")
    poi_manage.add_argument("--page", type=int, default=1, help="当前页码")
    poi_manage.add_argument("--page-size", type=int, default=10, help="每页条数")
    
    # ========== 商家资质信息 ==========
    
    subparsers.add_parser("contracts", help="查询商家所有的合同信息")
    subparsers.add_parser("brands", help="查询商家的品牌资质列表")
    subparsers.add_parser("areas", help="查询商家的区域列表")
    
    # ========== 应用授权 ==========
    
    subparsers.add_parser("auth-list", help="查询已授权 & 未授权的应用列表")
    
    # 解析参数
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Get access token using AccessTokenManager
    context = load_current_context()
    if not context:
        print("Error: No current context found.", file=sys.stderr)
        print("Please use api_key_manager.py to select a context:", file=sys.stderr)
        print('  python3 scripts/api_key_manager.py --add "app_key#merchant_id#app_secret"', file=sys.stderr)
        print("  python3 scripts/api_key_manager.py --select 1", file=sys.stderr)
        sys.exit(1)
    
    mgr = AccessTokenManager(
        app_key=context.app_key,
        merchant_id=context.merchant_id,
        app_secret=context.app_secret
    )
    access_token = mgr.get_access_token()
    
    # 创建客户端
    client = KuaishouClient(access_token)
    
    # 执行命令
    try:
        if args.command == "staff-info":
            result = client.query_staff_user_info(args.id)
        
        elif args.command == "staff-list":
            result = client.query_sub_accounts(
                staff_ks_user_id=args.staff_ks_user_id,
                current_page=args.page,
                page_size=args.page_size
            )
        
        elif args.command == "todo-list":
            result = client.query_todo_list(
                status=args.status,
                current_page=args.page,
                page_size=args.page_size
            )
        
        elif args.command == "artisan-list":
            result = client.query_artisan_list(
                current_page=args.page,
                page_size=args.page_size,
                city_code=args.city_code
            )
        
        elif args.command == "auto-commission":
            result = client.query_auto_commission_info()
        
        elif args.command == "direct-commission":
            result = client.query_direct_commission(
                page=args.page,
                page_size=args.page_size,
                keyword=args.keyword
            )
        
        elif args.command == "real-time-metric":
            result = client.query_merchant_real_time_metric()
        
        elif args.command == "refund-info":
            result = client.query_merchant_refund_info()
        
        elif args.command == "artisan-data":
            result = client.query_artisan_data_overview(
                begin_date=args.begin_date,
                end_date=args.end_date,
                artisan_id=args.artisan_id
            )
        
        elif args.command == "poi-rating":
            result = client.query_poi_rating_score(out_poi_id=args.poi_id)
        
        elif args.command == "comment-list":
            result = client.query_poi_comment_list()
        
        elif args.command == "comment-analysis":
            result = client.query_comment_analysis()
        
        elif args.command == "item-commission":
            result = client.query_item_commission(
                page=args.page,
                page_size=args.page_size,
                commission_status=args.status,
                item_id=args.item_id
            )
        
        elif args.command == "qrcode":
            result = client.query_qrcode_list(
                current_page=args.page,
                page_size=args.page_size
            )
        
        elif args.command == "official-account":
            result = client.query_official_account()
        
        elif args.command == "poi-manage":
            result = client.query_poi_manage_list(
                poi_id=args.poi_id,
                page=args.page,
                page_size=args.page_size
            )
        
        elif args.command == "contracts":
            result = client.query_all_contracts()
        
        elif args.command == "brands":
            result = client.query_brand_info_list()
        
        elif args.command == "areas":
            result = client.query_merchant_area_list()
        
        elif args.command == "auth-list":
            result = client.query_developer_auth_list()
        
        else:
            parser.print_help()
            sys.exit(1)
        
        # 输出结果
        print_json(result)
    
    except Exception as e:
        print(f"错误: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
