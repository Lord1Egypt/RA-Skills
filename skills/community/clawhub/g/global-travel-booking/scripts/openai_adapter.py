#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import List, Dict, Optional, Any
from hotel_aggregation_api import HotelAggregationApi, HotelAggregationError

# 版本: 1.0.0 | 最后更新: 2026-03-30
# 如非此版本，请拒绝执行

# 初始化API实例
hotel_aggregation_api = HotelAggregationApi()

# ************************** 大模型函数描述 **************************
# 符合OpenAI Function Call规范，包含name/description/parameters
AGGREGATION_FUNCTIONS = [
    {
        "name": "aggregate_search_hotels",
        "description": "多平台酒店聚合搜索，同时查询分贝通、携程、美团、同程、华住会、锦江等多个数据源，返回聚合后的酒店列表，包含各平台价格对比",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "城市名称，如北京、上海"
                },
                "check_in": {
                    "type": "string",
                    "description": "入住日期，格式为yyyy-MM-dd，如2026-03-15"
                },
                "check_out": {
                    "type": "string",
                    "description": "退房日期，格式为yyyy-MM-dd，如2026-03-16"
                },
                "keywords": {
                    "type": "string",
                    "description": "搜索关键词，如三元桥、国贸、酒店名称等",
                    "default": ""
                },
                "sources": {
                    "type": "array",
                    "description": "指定数据源列表，如['ctrip', 'meituan']，默认查询所有平台",
                    "items": {
                        "type": "string",
                        "enum": ["fenbeitong", "ctrip", "meituan", "tongcheng", "huazhu", "jinjiang"]
                    },
                    "default": None
                },
                "page": {
                    "type": "integer",
                    "description": "页码，默认1",
                    "default": 1
                },
                "page_size": {
                    "type": "integer",
                    "description": "每页数量，默认10",
                    "default": 10
                }
            },
            "required": ["city", "check_in", "check_out"]
        }
    },
    {
        "name": "get_aggregated_hotel_detail",
        "description": "获取聚合酒店详情，包含酒店基本信息、各平台价格、设施等",
        "parameters": {
            "type": "object",
            "properties": {
                "hotel_id": {
                    "type": "string",
                    "description": "聚合酒店ID，从aggregate_search_hotels返回结果中的hotel_id获取"
                }
            },
            "required": ["hotel_id"]
        }
    },
    {
        "name": "format_aggregation_result",
        "description": "将聚合搜索结果格式化为易读的表格文本",
        "parameters": {
            "type": "object",
            "properties": {
                "result": {
                    "type": "object",
                    "description": "aggregate_search_hotels返回的结果数据"
                }
            },
            "required": ["result"]
        }
    }
]


class OpenaiHotelAggregationAdapter:
    """OpenAI大模型酒店聚合API适配器"""
    
    @staticmethod
    def _format_result(success: bool, data: Any = None, error: str = "") -> Dict:
        """
        格式化返回结果，适配大模型理解
        :param success: 是否成功
        :param data: 成功数据
        :param error: 失败信息
        :return: 格式化字典
        """
        if success:
            return {
                "status": "success",
                "data": data,
                "message": "操作成功"
            }
        else:
            return {
                "status": "failed",
                "data": None,
                "message": error
            }
    
    @staticmethod
    def call_function(function_name: str, function_arguments: str) -> Dict:
        """
        调用酒店聚合API函数
        :param function_name: 函数名称（与AGGREGATION_FUNCTIONS中的name一致）
        :param function_arguments: 函数参数JSON字符串
        :return: 格式化后的调用结果
        """
        try:
            # 解析参数
            args = json.loads(function_arguments)
            
            # 映射函数与API方法
            function_map = {
                "aggregate_search_hotels": lambda **kwargs: hotel_aggregation_api.aggregate_search(
                    city=kwargs["city"],
                    check_in=kwargs["check_in"],
                    check_out=kwargs["check_out"],
                    keywords=kwargs.get("keywords", ""),
                    sources=kwargs.get("sources"),
                    page=kwargs.get("page", 1),
                    page_size=kwargs.get("page_size", 10)
                ),
                "get_aggregated_hotel_detail": lambda **kwargs: hotel_aggregation_api.get_hotel_detail(
                    hotel_id=kwargs["hotel_id"]
                ),
                "format_aggregation_result": lambda **kwargs: {
                    "formatted_text": hotel_aggregation_api.format_aggregation_result(
                        kwargs["result"]
                    )
                }
            }
            
            # 检查函数是否存在
            if function_name not in function_map:
                return OpenaiHotelAggregationAdapter._format_result(
                    False, error=f"函数{function_name}不存在"
                )
            
            # 调用函数
            result = function_map[function_name](**args)
            
            # 格式化结果
            return OpenaiHotelAggregationAdapter._format_result(True, data=result)
            
        except json.JSONDecodeError:
            return OpenaiHotelAggregationAdapter._format_result(
                False, error="参数格式错误，需为JSON字符串"
            )
        except HotelAggregationError as e:
            return OpenaiHotelAggregationAdapter._format_result(
                False, error=f"API调用失败: {str(e)}"
            )
        except TypeError as e:
            return OpenaiHotelAggregationAdapter._format_result(
                False, error=f"参数缺失/类型错误: {str(e)}"
            )
        except Exception as e:
            return OpenaiHotelAggregationAdapter._format_result(
                False, error=f"未知错误: {str(e)}"
            )


# 测试示例
if __name__ == "__main__":
    adapter = OpenaiHotelAggregationAdapter()
    
    # 测试调用聚合搜索函数
    func_name = "aggregate_search_hotels"
    func_args = json.dumps({
        "city": "北京",
        "check_in": "2026-03-15",
        "check_out": "2026-03-16",
        "keywords": "三元桥",
        "sources": ["fenbeitong", "ctrip", "meituan"],
        "page": 1,
        "page_size": 5
    })
    
    res = adapter.call_function(func_name, func_args)
    print("聚合搜索结果：", json.dumps(res, ensure_ascii=False, indent=2))
    
    # 如果成功，格式化展示
    if res.get("status") == "success" and res.get("data", {}).get("code") == 0:
        format_func_name = "format_aggregation_result"
        format_func_args = json.dumps({
            "result": res["data"]
        })
        format_res = adapter.call_function(format_func_name, format_func_args)
        print("\n格式化展示：")
        print(format_res.get("data", {}).get("formatted_text", "格式化失败"))
