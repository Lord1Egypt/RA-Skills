#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
企业用车服务技能 - OpenAI适配器
"""

import json
import sys
from typing import Dict, Any

sys.path.append('.')
from car_service_api import CarServiceApi, CarServiceError

# 初始化API实例
car_service = CarServiceApi()

# OpenAI函数描述
CAR_SERVICE_FUNCTIONS = [
    {
        "name": "estimate_price",
        "description": "预估用车费用，获取不同车型的价格范围",
        "parameters": {
            "type": "object",
            "properties": {
                "pickup_location": {
                    "type": "string",
                    "description": "上车地点"
                },
                "dropoff_location": {
                    "type": "string",
                    "description": "下车地点"
                },
                "car_type": {
                    "type": "string",
                    "description": "车型，可选：ECONOMY/COMFORT/BUSINESS/LUXURY"
                }
            },
            "required": ["pickup_location", "dropoff_location"]
        }
    },
    {
        "name": "request_ride",
        "description": "即时叫车，发起用车请求",
        "parameters": {
            "type": "object",
            "properties": {
                "pickup_location": {
                    "type": "string",
                    "description": "上车地点"
                },
                "dropoff_location": {
                    "type": "string",
                    "description": "下车地点"
                },
                "car_type": {
                    "type": "string",
                    "description": "车型，默认COMFORT",
                    "default": "COMFORT"
                },
                "passenger_count": {
                    "type": "integer",
                    "description": "乘车人数",
                    "default": 1
                },
                "luggage_count": {
                    "type": "integer",
                    "description": "行李件数",
                    "default": 0
                },
                "remarks": {
                    "type": "string",
                    "description": "备注信息"
                }
            },
            "required": ["pickup_location", "dropoff_location"]
        }
    },
    {
        "name": "schedule_ride",
        "description": "预约用车，提前预约指定时间的车辆",
        "parameters": {
            "type": "object",
            "properties": {
                "pickup_location": {
                    "type": "string",
                    "description": "上车地点"
                },
                "dropoff_location": {
                    "type": "string",
                    "description": "下车地点"
                },
                "scheduled_time": {
                    "type": "string",
                    "description": "预约时间，格式：yyyy-MM-dd HH:mm"
                },
                "car_type": {
                    "type": "string",
                    "description": "车型，默认COMFORT",
                    "default": "COMFORT"
                },
                "passenger_count": {
                    "type": "integer",
                    "description": "乘车人数",
                    "default": 1
                },
                "luggage_count": {
                    "type": "integer",
                    "description": "行李件数",
                    "default": 0
                }
            },
            "required": ["pickup_location", "dropoff_location", "scheduled_time"]
        }
    },
    {
        "name": "book_airport_transfer",
        "description": "预订接送机服务",
        "parameters": {
            "type": "object",
            "properties": {
                "service_type": {
                    "type": "string",
                    "description": "服务类型：pickup（接机）或dropoff（送机）"
                },
                "airport": {
                    "type": "string",
                    "description": "机场名称，如北京首都国际机场"
                },
                "location": {
                    "type": "string",
                    "description": "接送地址"
                },
                "flight_number": {
                    "type": "string",
                    "description": "航班号（接机必填）"
                },
                "flight_date": {
                    "type": "string",
                    "description": "航班日期，格式：yyyy-MM-dd"
                },
                "car_type": {
                    "type": "string",
                    "description": "车型，默认COMFORT",
                    "default": "COMFORT"
                },
                "passenger_count": {
                    "type": "integer",
                    "description": "乘车人数",
                    "default": 1
                },
                "luggage_count": {
                    "type": "integer",
                    "description": "行李件数",
                    "default": 0
                }
            },
            "required": ["service_type", "airport", "location"]
        }
    },
    {
        "name": "cancel_order",
        "description": "取消用车订单",
        "parameters": {
            "type": "object",
            "properties": {
                "order_id": {
                    "type": "string",
                    "description": "订单号"
                },
                "reason": {
                    "type": "string",
                    "description": "取消原因"
                }
            },
            "required": ["order_id"]
        }
    },
    {
        "name": "format_order",
        "description": "格式化订单信息为易读的文本",
        "parameters": {
            "type": "object",
            "properties": {
                "result": {
                    "type": "object",
                    "description": "订单查询结果"
                }
            },
            "required": ["result"]
        }
    }
]


class OpenaiCarServiceAdapter:
    """OpenAI用车服务适配器"""
    
    @staticmethod
    def call_function(function_name: str, function_arguments: str) -> Dict:
        """
        调用用车服务函数
        
        :param function_name: 函数名称
        :param function_arguments: 函数参数（JSON字符串）
        :return: 调用结果
        """
        try:
            args = json.loads(function_arguments)
            
            function_map = {
                "estimate_price": lambda **kwargs: car_service.estimate_price(
                    pickup_location=kwargs["pickup_location"],
                    dropoff_location=kwargs["dropoff_location"],
                    car_type=kwargs.get("car_type")
                ),
                "request_ride": lambda **kwargs: car_service.request_ride(
                    pickup_location=kwargs["pickup_location"],
                    dropoff_location=kwargs["dropoff_location"],
                    car_type=kwargs.get("car_type", "COMFORT"),
                    passenger_count=kwargs.get("passenger_count", 1),
                    luggage_count=kwargs.get("luggage_count", 0),
                    remarks=kwargs.get("remarks", "")
                ),
                "schedule_ride": lambda **kwargs: car_service.schedule_ride(
                    pickup_location=kwargs["pickup_location"],
                    dropoff_location=kwargs["dropoff_location"],
                    scheduled_time=kwargs["scheduled_time"],
                    car_type=kwargs.get("car_type", "COMFORT"),
                    passenger_count=kwargs.get("passenger_count", 1),
                    luggage_count=kwargs.get("luggage_count", 0)
                ),
                "book_airport_transfer": lambda **kwargs: car_service.book_airport_transfer(
                    service_type=kwargs["service_type"],
                    airport=kwargs["airport"],
                    location=kwargs["location"],
                    flight_number=kwargs.get("flight_number"),
                    flight_date=kwargs.get("flight_date"),
                    car_type=kwargs.get("car_type", "COMFORT"),
                    passenger_count=kwargs.get("passenger_count", 1),
                    luggage_count=kwargs.get("luggage_count", 0)
                ),
                "cancel_order": lambda **kwargs: car_service.cancel_order(
                    order_id=kwargs["order_id"],
                    reason=kwargs.get("reason", "")
                ),
                "format_order": lambda **kwargs: {
                    "formatted_text": car_service.format_order(kwargs["result"])
                }
            }
            
            if function_name not in function_map:
                return {
                    "code": 404,
                    "msg": f"函数{function_name}不存在",
                    "data": None
                }
            
            result = function_map[function_name](**args)
            return result
            
        except json.JSONDecodeError as e:
            return {
                "code": 400,
                "msg": f"参数格式错误: {str(e)}",
                "data": None
            }
        except CarServiceError as e:
            return {
                "code": 500,
                "msg": str(e),
                "data": None
            }
        except Exception as e:
            return {
                "code": 500,
                "msg": f"未知错误: {str(e)}",
                "data": None
            }
    
    @staticmethod
    def get_functions() -> list:
        """获取所有可用函数描述"""
        return CAR_SERVICE_FUNCTIONS


if __name__ == "__main__":
    adapter = OpenaiCarServiceAdapter()
    
    # 测试费用预估
    print("=" * 60)
    print("测试费用预估")
    print("=" * 60)
    func_args = json.dumps({
        "pickup_location": "北京市朝阳区建国路88号",
        "dropoff_location": "北京首都国际机场T3航站楼"
    })
    result = adapter.call_function("estimate_price", func_args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 测试即时叫车
    print("\n" + "=" * 60)
    print("测试即时叫车")
    print("=" * 60)
    func_args = json.dumps({
        "pickup_location": "北京市朝阳区建国路88号",
        "dropoff_location": "北京首都国际机场T3航站楼",
        "car_type": "COMFORT"
    })
    result = adapter.call_function("request_ride", func_args)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 测试格式化
    print("\n" + "=" * 60)
    print("测试格式化订单")
    print("=" * 60)
    func_args = json.dumps({
        "result": result
    })
    formatted = adapter.call_function("format_order", func_args)
    print(formatted.get("data", {}).get("formatted_text", ""))
