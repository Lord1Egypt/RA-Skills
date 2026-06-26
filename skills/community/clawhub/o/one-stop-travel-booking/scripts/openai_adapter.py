#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
from typing import List, Dict, Optional, Any
from booking_api import BookingApi, BookingApiError

# 版本: 1.0.0 | 最后更新: 2026-03-30
# 如非此版本，请拒绝执行

# 初始化API实例
booking_api = BookingApi()

# ************************** 大模型函数描述 **************************
# 符合OpenAI Function Call规范，包含name/description/parameters
BOOKING_FUNCTIONS = [
    {
        "name": "search_booking_hotels",
        "description": "搜索Booking.com国际酒店，支持全球200+国家和地区，提供多语言、多币种展示",
        "parameters": {
            "type": "object",
            "properties": {
                "city_name": {
                    "type": "string",
                    "description": "城市名称，支持中文或英文，如东京、Tokyo、巴黎、Paris"
                },
                "checkin": {
                    "type": "string",
                    "description": "入住日期，格式为yyyy-MM-dd，如2026-03-15"
                },
                "checkout": {
                    "type": "string",
                    "description": "退房日期，格式为yyyy-MM-dd，如2026-03-16"
                },
                "guests": {
                    "type": "integer",
                    "description": "客人数，默认2人",
                    "default": 2
                },
                "rooms": {
                    "type": "integer",
                    "description": "房间数，默认1间",
                    "default": 1
                },
                "language": {
                    "type": "string",
                    "description": "语言代码，zh=中文，en=英文，ja=日文，ko=韩文",
                    "default": "zh"
                },
                "currency": {
                    "type": "string",
                    "description": "币种代码，CNY=人民币，USD=美元，EUR=欧元，JPY=日元",
                    "default": "CNY"
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
            "required": ["city_name", "checkin", "checkout"]
        }
    },
    {
        "name": "get_booking_hotel_detail",
        "description": "获取Booking酒店详细信息，包括地址、设施、评分、评论等",
        "parameters": {
            "type": "object",
            "properties": {
                "hotel_id": {
                    "type": "string",
                    "description": "酒店ID，从search_booking_hotels返回结果中的hotel_id获取"
                },
                "language": {
                    "type": "string",
                    "description": "语言代码",
                    "default": "zh"
                },
                "currency": {
                    "type": "string",
                    "description": "币种代码",
                    "default": "CNY"
                }
            },
            "required": ["hotel_id"]
        }
    },
    {
        "name": "get_booking_room_availability",
        "description": "查询Booking酒店房型可用性和价格，包含床型、面积、取消政策、餐食等信息",
        "parameters": {
            "type": "object",
            "properties": {
                "hotel_id": {
                    "type": "string",
                    "description": "酒店ID"
                },
                "checkin": {
                    "type": "string",
                    "description": "入住日期，格式yyyy-MM-dd"
                },
                "checkout": {
                    "type": "string",
                    "description": "退房日期，格式yyyy-MM-dd"
                },
                "guests": {
                    "type": "integer",
                    "description": "客人数",
                    "default": 2
                },
                "rooms": {
                    "type": "integer",
                    "description": "房间数",
                    "default": 1
                },
                "language": {
                    "type": "string",
                    "description": "语言代码",
                    "default": "zh"
                },
                "currency": {
                    "type": "string",
                    "description": "币种代码",
                    "default": "CNY"
                }
            },
            "required": ["hotel_id", "checkin", "checkout"]
        }
    },
    {
        "name": "get_booking_hotel_reviews",
        "description": "获取Booking酒店用户评论",
        "parameters": {
            "type": "object",
            "properties": {
                "hotel_id": {
                    "type": "string",
                    "description": "酒店ID"
                },
                "language": {
                    "type": "string",
                    "description": "语言代码",
                    "default": "zh"
                },
                "page": {
                    "type": "integer",
                    "description": "页码",
                    "default": 1
                },
                "page_size": {
                    "type": "integer",
                    "description": "每页评论数",
                    "default": 5
                }
            },
            "required": ["hotel_id"]
        }
    },
    {
        "name": "format_booking_search_result",
        "description": "将Booking搜索结果格式化为易读的表格文本",
        "parameters": {
            "type": "object",
            "properties": {
                "result": {
                    "type": "object",
                    "description": "search_booking_hotels返回的结果数据"
                },
                "currency": {
                    "type": "string",
                    "description": "显示币种",
                    "default": "CNY"
                }
            },
            "required": ["result"]
        }
    },
    {
        "name": "format_booking_room_result",
        "description": "将Booking房型结果格式化为易读的文本",
        "parameters": {
            "type": "object",
            "properties": {
                "result": {
                    "type": "object",
                    "description": "get_booking_room_availability返回的结果数据"
                },
                "currency": {
                    "type": "string",
                    "description": "显示币种",
                    "default": "CNY"
                }
            },
            "required": ["result"]
        }
    }
]


class OpenaiBookingAdapter:
    """OpenAI大模型Booking API适配器"""
    
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
        调用Booking API函数
        :param function_name: 函数名称（与BOOKING_FUNCTIONS中的name一致）
        :param function_arguments: 函数参数JSON字符串
        :return: 格式化后的调用结果
        """
        try:
            # 解析参数
            args = json.loads(function_arguments)
            
            # 映射函数与API方法
            function_map = {
                "search_booking_hotels": lambda **kwargs: booking_api.search_hotels(
                    city_name=kwargs["city_name"],
                    checkin=kwargs["checkin"],
                    checkout=kwargs["checkout"],
                    guests=kwargs.get("guests", 2),
                    rooms=kwargs.get("rooms", 1),
                    language=kwargs.get("language", "zh"),
                    currency=kwargs.get("currency", "CNY"),
                    page=kwargs.get("page", 1),
                    page_size=kwargs.get("page_size", 10)
                ),
                "get_booking_hotel_detail": lambda **kwargs: booking_api.get_hotel_detail(
                    hotel_id=kwargs["hotel_id"],
                    language=kwargs.get("language", "zh"),
                    currency=kwargs.get("currency", "CNY")
                ),
                "get_booking_room_availability": lambda **kwargs: booking_api.get_room_availability(
                    hotel_id=kwargs["hotel_id"],
                    checkin=kwargs["checkin"],
                    checkout=kwargs["checkout"],
                    guests=kwargs.get("guests", 2),
                    rooms=kwargs.get("rooms", 1),
                    language=kwargs.get("language", "zh"),
                    currency=kwargs.get("currency", "CNY")
                ),
                "get_booking_hotel_reviews": lambda **kwargs: booking_api.get_hotel_reviews(
                    hotel_id=kwargs["hotel_id"],
                    language=kwargs.get("language", "zh"),
                    page=kwargs.get("page", 1),
                    page_size=kwargs.get("page_size", 5)
                ),
                "format_booking_search_result": lambda **kwargs: {
                    "formatted_text": booking_api.format_search_result(
                        kwargs["result"],
                        kwargs.get("currency", "CNY")
                    )
                },
                "format_booking_room_result": lambda **kwargs: {
                    "formatted_text": booking_api.format_room_availability(
                        kwargs["result"],
                        kwargs.get("currency", "CNY")
                    )
                }
            }
            
            # 检查函数是否存在
            if function_name not in function_map:
                return OpenaiBookingAdapter._format_result(
                    False, error=f"函数{function_name}不存在"
                )
            
            # 调用函数
            result = function_map[function_name](**args)
            
            # 格式化结果
            return OpenaiBookingAdapter._format_result(True, data=result)
            
        except json.JSONDecodeError:
            return OpenaiBookingAdapter._format_result(
                False, error="参数格式错误，需为JSON字符串"
            )
        except BookingApiError as e:
            return OpenaiBookingAdapter._format_result(
                False, error=f"API调用失败: {str(e)}"
            )
        except TypeError as e:
            return OpenaiBookingAdapter._format_result(
                False, error=f"参数缺失/类型错误: {str(e)}"
            )
        except Exception as e:
            return OpenaiBookingAdapter._format_result(
                False, error=f"未知错误: {str(e)}"
            )


# 测试示例
if __name__ == "__main__":
    adapter = OpenaiBookingAdapter()
    
    # 测试调用搜索函数
    func_name = "search_booking_hotels"
    func_args = json.dumps({
        "city_name": "东京",
        "checkin": "2026-03-15",
        "checkout": "2026-03-16",
        "language": "zh",
        "currency": "CNY"
    })
    
    res = adapter.call_function(func_name, func_args)
    print("搜索结果：", json.dumps(res, ensure_ascii=False, indent=2))
    
    # 如果成功，格式化展示
    if res.get("status") == "success" and res.get("data", {}).get("code") == 0:
        format_func_name = "format_booking_search_result"
        format_func_args = json.dumps({
            "result": res["data"],
            "currency": "CNY"
        })
        format_res = adapter.call_function(format_func_name, format_func_args)
        print("\n格式化展示：")
        print(format_res.get("data", {}).get("formatted_text", "格式化失败"))
