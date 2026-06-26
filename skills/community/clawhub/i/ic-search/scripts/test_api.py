#!/usr/bin/env python3
"""
IC Search API 测试脚本 - 使用标准库
GET 请求模式
"""

import urllib.request
import urllib.error
import urllib.parse
import json

def test_api_search(search_msg, supply_type="nkwd"):
    """
    测试 IC Search API
    
    Args:
        search_msg (str): 搜索关键词
        supply_type (str): 鉴权 token（固定为 nkwd）
    
    Returns:
        dict: API 响应数据
    """
    base_url = "http://ip.icsdk.com:2022/api/v1/raw"
    
    # URL 编码 msg 参数
    encoded_msg = urllib.parse.quote(search_msg)
    
    # 构建完整 URL
    url = f"{base_url}?supply={supply_type}&msg={encoded_msg}"
    
    headers = {
        "Accept": "application/json"
    }
    
    try:
        req = urllib.request.Request(url, headers=headers, method='GET')
        with urllib.request.urlopen(req, timeout=10) as response:
            result = json.loads(response.read().decode('utf-8'))
            return result
    except urllib.error.URLError as e:
        print(f"请求失败：{e}")
        return None
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败：{e}")
        return None

def handle_response(response):
    """
    处理 API 响应
    """
    if response is None:
        return "请求失败"
    
    code = response.get('code')
    data = response.get('data')
    
    # 无权操作
    if code == 4004:
        return "您无权操作"
    
    # data 为 null，查询失败
    if data is None:
        return "查询失败"
    
    # 返回 data 内容
    if isinstance(data, dict) and 'string' in data:
        return data['string']
    return str(data)

def main():
    """测试函数"""
    print("=" * 60)
    print("IC Search API 测试 (GET 模式)")
    print("=" * 60)
    
    # 测试用例 1：查询库存
    print("\n[测试 1] 查询 STM32F103C8T6 库存")
    print("请求：GET http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=STM32F103C8T6")
    result = test_api_search("STM32F103C8T6", "nkwd")
    print(f"响应：{json.dumps(result, ensure_ascii=False, indent=2) if result else '无响应'}")
    print(f"处理结果：{handle_response(result)}")
    
    # 测试用例 2：查询价格
    print("\n[测试 2] 查询 TPS5430 价格")
    print("请求：GET http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=TPS5430")
    result = test_api_search("TPS5430", "nkwd")
    print(f"响应：{json.dumps(result, ensure_ascii=False, indent=2) if result else '无响应'}")
    print(f"处理结果：{handle_response(result)}")
    
    # 测试用例 3：包含空格的搜索内容
    print("\n[测试 3] 查询 5601230200 270 求购现货")
    url = "http://ip.icsdk.com:2022/api/v1/raw?supply=nkwd&msg=5601230200%20270%20 求购现货"
    print(f"请求：GET {url}")
    result = test_api_search("5601230200 270 求购现货", "nkwd")
    print(f"响应：{json.dumps(result, ensure_ascii=False, indent=2) if result else '无响应'}")
    print(f"处理结果：{handle_response(result)}")
    
    # 测试用例 4：无权操作测试
    print("\n[测试 4] 测试无权操作（4004）")
    test_response = {
        "code": 4004,
        "msg": "您无权操作",
        "data": None,
        "supply": "nkwd"
    }
    print(f"响应：{json.dumps(test_response, ensure_ascii=False, indent=2)}")
    print(f"处理结果：{handle_response(test_response)}")
    
    # 测试用例 5：data 为 null 测试
    print("\n[测试 5] 测试 data 为 null（查询失败）")
    test_response = {
        "code": 200,
        "msg": "success",
        "data": None,
        "supply": "nkwd"
    }
    print(f"响应：{json.dumps(test_response, ensure_ascii=False, indent=2)}")
    print(f"处理结果：{handle_response(test_response)}")
    
    # 测试用例 6：成功查询测试
    print("\n[测试 6] 测试成功查询")
    test_response = {
        "code": 200,
        "msg": "success",
        "data": {
            "string": "库存：5000 pcs\n价格：￥2.50/pcs\n供应商：深圳 XX 电子"
        },
        "supply": "nkwd"
    }
    print(f"响应：{json.dumps(test_response, ensure_ascii=False, indent=2)}")
    print(f"处理结果：{handle_response(test_response)}")
    
    print("\n" + "=" * 60)
    print("测试完成")
    print("=" * 60)

if __name__ == "__main__":
    main()
