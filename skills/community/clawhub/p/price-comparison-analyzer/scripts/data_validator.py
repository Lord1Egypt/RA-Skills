#!/usr/bin/env python3
"""
电商比价数据格式验证脚本

功能：
- 验证输入数据格式是否符合规范
- 检查必填字段
- 验证数据类型和取值范围
"""

import json
import sys
from typing import Dict, Any, List


def parse_args():
    """解析命令行参数"""
    if len(sys.argv) < 2:
        print("用法: python data_validator.py <product_data_json>")
        print("示例: python data_validator.py '{\"product_name\": \"iPhone 15\", \"price_list\": [5000, 5200]}'")
        sys.exit(1)
    
    try:
        return json.loads(sys.argv[1])
    except json.JSONDecodeError as e:
        print(f"JSON解析错误: {e}")
        sys.exit(1)


def validate_product_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    验证商品数据格式
    
    参数:
        data: 商品数据字典
        
    返回:
        包含 is_valid, errors, warnings 的验证结果
    """
    errors = []
    warnings = []
    
    # 验证必填字段
    required_fields = ["product_name", "price_list"]
    for field in required_fields:
        if field not in data:
            errors.append(f"缺少必填字段: {field}")
    
    # 验证 product_name
    if "product_name" in data:
        product_name = data["product_name"]
        if not isinstance(product_name, str) or len(product_name.strip()) == 0:
            errors.append("product_name 必须是非空字符串")
        elif len(product_name) < 3:
            warnings.append("product_name 过短，可能不够准确")
    
    # 验证 brand（如果存在）
    if "brand" in data:
        brand = data["brand"]
        if not isinstance(brand, str) or len(brand.strip()) == 0:
            errors.append("brand 必须是非空字符串")
    
    # 验证 key_specs（如果存在）
    if "key_specs" in data:
        key_specs = data["key_specs"]
        if not isinstance(key_specs, str) or len(key_specs.strip()) == 0:
            errors.append("key_specs 必须是非空字符串")
    
    # 验证 price_list
    if "price_list" in data:
        price_list = data["price_list"]
        if not isinstance(price_list, list):
            errors.append("price_list 必须是列表")
        elif len(price_list) == 0:
            errors.append("price_list 不能为空")
        else:
            # 验证每个价格
            for i, price in enumerate(price_list):
                if not isinstance(price, (int, float)):
                    errors.append(f"price_list[{i}] 必须是数字")
                elif price <= 0:
                    errors.append(f"price_list[{i}] 必须大于0")
                elif price > 10000000:  # 1千万
                    warnings.append(f"price_list[{i}] 价格异常高，请确认单位")
    
    # 验证 platform_info（如果存在）
    if "platform_info" in data:
        platform_info = data["platform_info"]
        if not isinstance(platform_info, list):
            errors.append("platform_info 必须是列表")
        else:
            for i, info in enumerate(platform_info):
                if not isinstance(info, dict):
                    errors.append(f"platform_info[{i}] 必须是字典")
                else:
                    # 验证必填字段
                    if "platform" not in info:
                        errors.append(f"platform_info[{i}] 缺少 platform 字段")
                    if "price" not in info:
                        errors.append(f"platform_info[{i}] 缺少 price 字段")
                    else:
                        price = info["price"]
                        if not isinstance(price, (int, float)) or price <= 0:
                            errors.append(f"platform_info[{i}].price 必须是有效数字")
    
    # 验证 platforms（如果存在）
    if "platforms" in data:
        platforms = data["platforms"]
        if not isinstance(platforms, list):
            errors.append("platforms 必须是列表")
        elif len(platforms) == 0:
            warnings.append("platforms 为空，将使用默认平台列表")
        else:
            valid_platforms = ["京东", "天猫", "拼多多", "抖音", "小红书", "亚马逊", "淘宝", "苏宁易购"]
            for platform in platforms:
                if platform not in valid_platforms:
                    warnings.append(f"platform '{platform}' 可能不是主流平台")
    
    # 验证 region（如果存在）
    if "region" in data:
        region = data["region"]
        if not isinstance(region, str) or len(region.strip()) == 0:
            errors.append("region 必须是非空字符串")
    
    # 验证 user_priority（如果存在）
    if "user_priority" in data:
        user_priority = data["user_priority"]
        valid_priorities = ["最低价优先", "官方/正品优先", "售后/发票优先"]
        if user_priority not in valid_priorities:
            warnings.append(f"user_priority '{user_priority}' 不是推荐值，推荐值: {valid_priorities}")
    
    # 判断是否有效
    is_valid = len(errors) == 0
    
    return {
        "is_valid": is_valid,
        "errors": errors,
        "warnings": warnings
    }


def main():
    """主函数"""
    # 解析输入
    input_data = parse_args()
    
    # 执行验证
    result = validate_product_data(input_data)
    
    # 输出结果
    print(json.dumps(result, ensure_ascii=False, indent=2))
    
    # 如果验证失败，返回非零退出码
    if not result["is_valid"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
