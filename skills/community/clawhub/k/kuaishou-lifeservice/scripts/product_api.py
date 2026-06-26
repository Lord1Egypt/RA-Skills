#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kwai Life Product API Script
All product domain APIs aggregated in one file.
"""

import os
import sys
import requests
import json
import argparse
from typing import Dict, Any, List, Optional
from urllib.parse import quote
from datetime import datetime, timedelta
import time

# Add the scripts directory to the path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import AccessTokenManager for automatic token management
from get_access_token import AccessTokenManager, load_current_context


class KwaiLifeBaseClient:
    """Base client with common functionality"""
    
    def __init__(self, access_token: str):
        self.access_token = access_token
        self.headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Accept": "application/json;charset=UTF-8",
            "access-token": access_token,
        }
    
    def _check_error(self, result: Dict[str, Any]) -> None:
        """Check for API errors."""
        # result: 0 means success, 1 means error in some APIs
        if "result" in result and result["result"] == 1:
            error_msg = result.get("error_msg", "Unknown error")
            raise RuntimeError(f"API error: {error_msg}")
        
        if "data" in result:
            data = result["data"]
            if "error_code" in data and data["error_code"] != 0:
                description = data.get("description", "Unknown error")
                error_code = data.get("error_code", -1)
                raise RuntimeError(f"Business error: {description} (code: {error_code})")


class ItemListQueryClient(KwaiLifeBaseClient):
    """Item List Query API Client"""
    
    BASE_URL = "https://lbs-open.kwailocallife.com/goodlife/v1/item/itemlist/batch/query"
    
    # 商品状态映射
    STATUS_MAP = {
        0: "未知",
        1: "已上架",
        2: "已下架",
        3: "已删除",
        4: "待审核",
        5: "审核失败"
    }
    
    # 商品状态图标映射
    STATUS_ICON_MAP = {
        0: "❓",
        1: "✅",
        2: "⚠️",
        3: "❌",
        4: "🕐",
        5: "⛔"
    }
    
    # 商品类型映射
    ITEM_TYPE_MAP = {
        1: "团购券",
        2: "代金券",
        3: "次卡",
        4: "储值卡"
    }
    
    # 审核状态映射 (check_status字段)
    AUDIT_STATUS_MAP = {
        1: "审核中",
        2: "审核通过",
        4: "审核驳回"
    }
    
    def query_item_list(
        self,
        cursor: int = 0,
        size: int = 20,
        product_ids: Optional[List[int]] = None,
        start_time: Optional[int] = None,
        end_time: Optional[int] = None,
        out_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """Batch query product list.
        
        Note: If product_ids is not provided, start_time and end_time are required.
              If not provided, they will default to the last 7 days.
        """
        data = {
            "cursor": cursor,
            "size": size
        }
        
        # 如果没有指定 product_ids 和 out_ids，则 start_time 和 end_time 必须有值
        # 如果用户未提供，默认为最近7天
        if not product_ids and not out_ids:
            # 7天的毫秒数
            seven_days_ms = 7 * 24 * 60 * 60 * 1000
            
            if start_time is None and end_time is None:
                # 两个都没有：默认最近7天
                now = datetime.now()
                end_time = int(now.timestamp() * 1000)
                start_time = end_time - seven_days_ms
            elif start_time is not None and end_time is None:
                # 只有 start_time：end_time = start_time + 7天
                end_time = start_time + seven_days_ms
            elif start_time is None and end_time is not None:
                # 只有 end_time：start_time = end_time - 7天
                start_time = end_time - seven_days_ms
            # 如果两个都有值，直接使用，不做处理
        
        if product_ids:
            data["product_id"] = product_ids
        if start_time is not None:
            data["start_time"] = start_time
        if end_time is not None:
            data["end_time"] = end_time
        if out_ids:
            data["out_id"] = out_ids
        
        response = requests.post(
            self.BASE_URL, 
            json=data, 
            headers=self.headers, 
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        self._check_error(result)
        
        if "data" in result:
            # 优化返回数据,添加状态说明
            data = result["data"]
            if "item_list" in data and isinstance(data["item_list"], list):
                for item in data["item_list"]:
                    # 添加状态中文描述
                    status = item.get("status", 0)
                    item["status_text"] = self.STATUS_MAP.get(status, f"未知状态({status})")
                    
                    # 添加商品类型中文描述
                    item_type = item.get("item_type", 0)
                    item["item_type_text"] = self.ITEM_TYPE_MAP.get(item_type, f"未知类型({item_type})")
                    
                    # 价格转换（分 -> 元）
                    if "min_price" in item:
                        item["min_price_yuan"] = item["min_price"] / 100
                    if "max_price" in item:
                        item["max_price_yuan"] = item["max_price"] / 100

                    # 时间戳转换（毫秒时间戳 -> 年月日格式）
                    if "sold_start_time" in item and item["sold_start_time"]:
                        try:
                            dt = datetime.fromtimestamp(item["sold_start_time"] / 1000)
                            item["sold_start_time"] = dt.strftime("%Y-%m-%d %H:%M:%S")
                        except (ValueError, TypeError, OSError):
                            item["sold_start_time"] = ""
                    else:
                        item["sold_start_time"] = ""
                    
                    if "sold_end_time" in item and item["sold_end_time"]:
                        try:
                            dt = datetime.fromtimestamp(item["sold_end_time"] / 1000)
                            item["sold_end_time"] = dt.strftime("%Y-%m-%d %H:%M:%S")
                        except (ValueError, TypeError, OSError):
                            item["sold_end_time"] = ""
                    else:
                        item["sold_end_time"] = ""
            
            return data
        return {}


class ItemPOIQueryClient(KwaiLifeBaseClient):
    """Item POI Query API Client"""
    
    BASE_URL = "https://lbs-open.kwailocallife.com/goodlife/v1/item/poi/query"
    
    def query_item_poi(
        self,
        item_id: Optional[int] = None,
        page_num: int = 1,
        page_size: int = 10
    ) -> Dict[str, Any]:
        """Query item-associated store information."""
        params = {
            "page_num": page_num,
            "page_size": page_size
        }
        
        if item_id is not None:
            params["item_id"] = item_id
        
        response = requests.get(
            self.BASE_URL, 
            params=params, 
            headers=self.headers, 
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        self._check_error(result)
        
        if "data" in result:
            return result["data"]
        return {}


def format_item_detail_markdown(item: Dict[str, Any]) -> str:
    """Format single item detail as markdown"""
    lines = []
    
    # Title
    lines.append("## 📦 商品详情\n")
    
    # Basic Info Table
    lines.append("| 字段 | 值 |")
    lines.append("|------|-----|")
    
    item_id = item.get("product_id", item.get("item_id", "N/A"))
    title = item.get("product_name", item.get("title", "N/A"))
    out_id = item.get("out_product_id", item.get("out_id", "N/A"))
    status = item.get("status", 0)
    status_text = item.get("status_text", "未知")
    status_icon = ItemListQueryClient.STATUS_ICON_MAP.get(status, "❓")
    
    # 类目路径 - 支持 category_detail 和 category_info 两种格式
    category_path = "N/A"
    if "category_detail" in item:
        cat_info = item["category_detail"]
        first_name = cat_info.get("first_cname", "")
        second_name = cat_info.get("second_cname", "")
        third_name = cat_info.get("third_cname", "")
        category_path = f"{first_name} → {second_name} → {third_name}" if first_name else "N/A"
    elif "category_info" in item:
        cat_info = item["category_info"]
        first_name = cat_info.get("first_category_name", "")
        second_name = cat_info.get("second_category_name", "")
        third_name = cat_info.get("third_category_name", "")
        category_path = f"{first_name} → {second_name} → {third_name}" if first_name else "N/A"
    
    # 商品类型 - 支持 product_type 和 item_type 两种格式
    product_type = item.get("product_type", item.get("item_type", 0))
    product_type_text = ItemListQueryClient.ITEM_TYPE_MAP.get(product_type, f"未知类型({product_type})")
    
    lines.append(f"| **商品 ID** | {item_id} |")
    lines.append(f"| **商品名称** | {title} |")
    lines.append(f"| **外部商品 ID** | {out_id} |")
    lines.append(f"| **状态** | {status_icon} {status_text} |")
    lines.append(f"| **类别** | {category_path} |")
    lines.append(f"| **商品类型** | {product_type_text} |")
    
    lines.append("")
    
    # Sales Time Section
    lines.append("### 📅 销售时间")
    sold_start = item.get("sold_start_time", "")
    sold_end = item.get("sold_end_time", "")

    lines.append(f"- **开售时间**: {sold_start}")
    lines.append(f"- **结束时间**: {sold_end}")
    
    # SKU Information
    lines.append("### 💰 SKU 信息")
    sku_list = item.get("sku", item.get("sku_infos", []))
    if isinstance(sku_list, list) and len(sku_list) > 0:
        sku = sku_list[0]  # Display first SKU
        
        lines.append("| 字段 | 值 |")
        lines.append("|------|-----|")
        lines.append(f"| SKU ID | {sku.get('sku_id', 'N/A')} |")
        lines.append(f"| SKU 名称 | {sku.get('sku_name', sku.get('title', 'N/A'))} |")
        lines.append(f"| 外部 SKU ID | {sku.get('out_sku_id', 'N/A')} |")
        
        # Price formatting (support both origin_amount/origin_price and actual_amount/actual_price)
        original_price = sku.get("origin_amount", sku.get("origin_price", 0))
        actual_price = sku.get("actual_amount", sku.get("actual_price", 0))
        lines.append(f"| 原价 | ¥{original_price / 100:.2f} |")
        lines.append(f"| 实际价 | ¥{actual_price / 100:.2f} |")
    else:
        lines.append("无 SKU 信息")
    
    lines.append("")
    
    # Inventory Information
    lines.append("### 📦 库存信息")
    sku_list = item.get("sku", item.get("sku_infos", []))
    if isinstance(sku_list, list) and len(sku_list) > 0:
        sku = sku_list[0]
        stock = sku.get("stock", {})
        
        lines.append("| 字段 | 值 |")
        lines.append("|------|-----|")
        lines.append(f"| 可售库存 | {stock.get('avail_qty', sku.get('available_stock', 'N/A'))} |")
        lines.append(f"| 总库存 | {stock.get('stock_qty', sku.get('total_stock', 'N/A'))} |")
        lines.append(f"| 已售数量 | {stock.get('sold_qty', sku.get('sold_num', 'N/A'))} |")
    else:
        lines.append("无库存信息")
    
    lines.append("")
    
    # Attribute Configuration
    lines.append("### ⚙️ 属性配置")
    buy_limit_type = item.get("buy_limit_type", 0)
    buy_limit_text = "限购" if buy_limit_type == 1 else "不限购"
    lines.append(f"- **购买限制**: {buy_limit_text}")
    
    # 券码有效期
    sku_list = item.get("sku", item.get("sku_infos", []))
    if isinstance(sku_list, list) and len(sku_list) > 0:
        sku = sku_list[0]
        valid_days = sku.get("valid_days", "N/A")
        if valid_days != "N/A":
            lines.append(f"- **券码有效期**: 购买后 {valid_days} 天有效")
    
    lines.append("")
    
    # Audit Status
    lines.append("### ✅ 审核状态")
    check_status = item.get("check_status", 0)
    check_status_text = ItemListQueryClient.AUDIT_STATUS_MAP.get(check_status, f"未知状态({check_status})")
    lines.append(f"- **审核状态**: {check_status_text}")
    
    lines.append("")
    lines.append("---")
    
    return "\n".join(lines)


class ItemSKUListQueryClient(KwaiLifeBaseClient):
    """Item SKU List Query API Client"""
    
    BASE_URL = "https://lbs-open.kwailocallife.com/goodlife/v1/item/itemskulist/batch/query"
    
    def query_item_sku_list(
        self,
        poi_id: Optional[int] = None,
        cursor: Optional[int] = None,
        size: Optional[int] = None
    ) -> Dict[str, Any]:
        """Batch query store-dimension product information."""
        data = {}
        
        if poi_id is not None:
            data["poi_id"] = poi_id
        if cursor is not None:
            data["cursor"] = cursor
        if size is not None:
            data["size"] = size
        
        response = requests.post(
            self.BASE_URL, 
            json=data, 
            headers=self.headers, 
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        
        self._check_error(result)
        
        if "data" in result:
            return result["data"]
        return {}


def main():
    parser = argparse.ArgumentParser(
        description="Kwai Life Product API - All product domain interfaces"
    )
    parser.add_argument(
        "--api", 
        required=True,
        choices=["item_list", "item_poi", "item_sku_list"],
        help="API to call: item_list, item_poi, item_sku_list"
    )
    # Item list query arguments
    parser.add_argument("--cursor", type=int, default=0, help="Query cursor")
    parser.add_argument("--size", type=int, default=20, help="Page size")
    parser.add_argument("--product_ids", "-pids", nargs="+", type=int, help="List of product IDs")
    parser.add_argument("--start_time", type=int, help="Start timestamp")
    parser.add_argument("--end_time", type=int, help="End timestamp")
    parser.add_argument("--out_ids", "-oids", nargs="+", help="List of external product IDs")
    
    # Item POI query arguments
    parser.add_argument("--item_id", type=int, help="Item ID")
    parser.add_argument("--page_num", type=int, default=1, help="Page number")
    parser.add_argument("--page_size", type=int, default=10, help="Page size")
    
    # Item SKU list query arguments
    parser.add_argument("--poi_id", type=int, help="POI ID")
    
    args = parser.parse_args()
    
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
    
    try:
        if args.api == "item_list":
            client = ItemListQueryClient(access_token)
            results = client.query_item_list(
                cursor=args.cursor,
                size=args.size,
                product_ids=args.product_ids,
                start_time=args.start_time,
                end_time=args.end_time,
                out_ids=args.out_ids
            )
            
            # 如果指定了单个商品ID，使用markdown格式输出
            if args.product_ids and len(args.product_ids) == 1:
                if "item_list" in results and isinstance(results["item_list"], list) and len(results["item_list"]) > 0:
                    item = results["item_list"][0]
                    print(format_item_detail_markdown(item))
                else:
                    print("未找到指定商品信息")
            else:
                # 格式化输出商品列表，突出显示状态
                if "item_list" in results and isinstance(results["item_list"], list):
                    print(f"\n{'='*80}")
                    print(f"📦 查询到 {len(results['item_list'])} 个商品")
                    print(f"{'='*80}\n")
                    
                    for idx, item in enumerate(results["item_list"], 1):
                        status_text = item.get("status_text", "未知状态")
                        item_id = item.get("item_id", "N/A")
                        title = item.get("title", "无标题")
                        item_type_text = item.get("item_type_text", "未知类型")
                        
                        # 根据状态设置标识符
                        if item.get("status") == 1:
                            status_icon = "✅"
                        elif item.get("status") == 2:
                            status_icon = "⚠️"
                        elif item.get("status") == 3:
                            status_icon = "❌"
                        else:
                            status_icon = "❓"
                        
                        print(f"{idx}. {status_icon} [{status_text}] {title}")
                        print(f"   商品ID: {item_id}")
                        print(f"   商品类型: {item_type_text}")
                        
                        if "min_price_yuan" in item:
                            print(f"   价格: ¥{item['min_price_yuan']:.2f}")
                        
                        print()
                    
                    print(f"\n{'='*80}")
                    print(f"💡 状态说明: ✅ 已上架 | ⚠️ 已下架 | ❌ 已删除 | ❓ 其他状态")
                    print(f"{'='*80}\n")
                
                # 同时输出完整的JSON数据
                print("\n📋 完整JSON数据:")
                print(json.dumps(results, ensure_ascii=False, indent=2))
            
        elif args.api == "item_poi":
            client = ItemPOIQueryClient(access_token)
            results = client.query_item_poi(
                item_id=args.item_id,
                page_num=args.page_num,
                page_size=args.page_size
            )
            print(json.dumps(results, ensure_ascii=False, indent=2))
            
        elif args.api == "item_sku_list":
            client = ItemSKUListQueryClient(access_token)
            results = client.query_item_sku_list(
                poi_id=args.poi_id,
                cursor=args.cursor if args.cursor != 0 else None,
                size=args.size if args.size != 20 else None
            )
            print(json.dumps(results, ensure_ascii=False, indent=2))
        
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}", file=sys.stderr)
        sys.exit(1)
    except RuntimeError as e:
        print(f"API error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
