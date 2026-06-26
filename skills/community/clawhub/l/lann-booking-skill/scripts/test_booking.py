#!/usr/bin/env python3
"""
兰泰式按摩预约 API 测试脚本

本脚本用于测试直连 API 模式的预约功能，包含多种测试场景。

使用方法:
    python test_booking.py

依赖:
    pip install requests

配置:
    修改 API_ENDPOINT 变量以使用不同的 API 地址
"""

import requests
import json
from datetime import datetime, timedelta

# API 配置
API_ENDPOINT = "https://open.lannlife.com/mcp/book/create"
HEADERS = {
    "Content-Type": "application/json"
}

# 测试数据
TEST_MOBILE = "13812345678"
TEST_STORE = "淮海店"
TEST_SERVICE = "传统古法全身按摩-90分钟"
TEST_COUNT = 2
# 生成明天的时间（ISO 8601 格式）
TEST_TIME = (datetime.now() + timedelta(days=1, hours=14)).strftime("%Y-%m-%dT%H:%M:%S")


def print_separator(title=""):
    """打印分隔线"""
    print("\n" + "=" * 60)
    if title:
        print(f"  {title}")
        print("=" * 60)


def print_result(response, test_name):
    """打印测试结果"""
    print(f"\n测试: {test_name}")
    print(f"状态码: {response.status_code}")
    try:
        result = response.json()
        print(f"响应内容:")
        print(json.dumps(result, indent=2, ensure_ascii=False))

        if result.get("success"):
            print(f"✅ 测试通过 - {result.get('message', '成功')}")
        else:
            print(f"❌ 测试失败 - {result.get('message', '未知错误')}")
    except Exception as e:
        print(f"响应解析失败: {e}")
        print(f"原始响应: {response.text}")


def create_booking(mobile, store_name, service_name, count, book_time, test_name="创建预约"):
    """
    调用预约 API

    Args:
        mobile: 手机号
        store_name: 门店名称
        service_name: 服务名称
        count: 人数
        book_time: 预约时间（ISO 8601 格式）
        test_name: 测试名称
    """
    payload = {
        "mobile": mobile,
        "storeName": store_name,
        "serviceName": service_name,
        "count": count,
        "bookTime": book_time
    }

    print(f"\n请求参数:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    try:
        response = requests.post(
            API_ENDPOINT,
            headers=HEADERS,
            json=payload,
            timeout=10
        )
        print_result(response, test_name)
        return response
    except requests.exceptions.Timeout:
        print(f"\n❌ 测试失败 - 请求超时")
        return None
    except requests.exceptions.ConnectionError:
        print(f"\n❌ 测试失败 - 连接错误，请检查网络连接或 API Endpoint")
        return None
    except Exception as e:
        print(f"\n❌ 测试失败 - {str(e)}")
        return None


def test_valid_booking():
    """测试 1: 有效的预约请求"""
    print_separator("测试 1: 有效的预约请求")
    create_booking(
        mobile=TEST_MOBILE,
        store_name=TEST_STORE,
        service_name=TEST_SERVICE,
        count=TEST_COUNT,
        book_time=TEST_TIME,
        test_name="有效预约"
    )


def test_invalid_phone():
    """测试 2: 无效的手机号"""
    print_separator("测试 2: 无效的手机号")
    create_booking(
        mobile="12345",  # 无效手机号
        store_name=TEST_STORE,
        service_name=TEST_SERVICE,
        count=TEST_COUNT,
        book_time=TEST_TIME,
        test_name="无效手机号"
    )


def test_invalid_store():
    """测试 3: 不存在的门店"""
    print_separator("测试 3: 不存在的门店")
    create_booking(
        mobile=TEST_MOBILE,
        store_name="不存在的门店",
        service_name=TEST_SERVICE,
        count=TEST_COUNT,
        book_time=TEST_TIME,
        test_name="不存在的门店"
    )


def test_invalid_service():
    """测试 4: 不存在的服务"""
    print_separator("测试 4: 不存在的服务")
    create_booking(
        mobile=TEST_MOBILE,
        store_name=TEST_STORE,
        service_name="不存在的服务",
        count=TEST_COUNT,
        book_time=TEST_TIME,
        test_name="不存在的服务"
    )


def test_invalid_count():
    """测试 5: 无效的人数"""
    print_separator("测试 5: 无效的人数")
    create_booking(
        mobile=TEST_MOBILE,
        store_name=TEST_STORE,
        service_name=TEST_SERVICE,
        count=25,  # 超过最大人数限制
        book_time=TEST_TIME,
        test_name="无效人数（超过限制）"
    )


def test_past_time():
    """测试 6: 过去的时间"""
    print_separator("测试 6: 过去的时间")
    past_time = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%dT%H:%M:%S")
    create_booking(
        mobile=TEST_MOBILE,
        store_name=TEST_STORE,
        service_name=TEST_SERVICE,
        count=TEST_COUNT,
        book_time=past_time,
        test_name="过去的时间"
    )


def test_missing_parameters():
    """测试 7: 缺少必填参数"""
    print_separator("测试 7: 缺少必填参数")
    payload = {
        "mobile": TEST_MOBILE,
        "storeName": TEST_STORE
        # 缺少 serviceName, count, bookTime
    }

    print(f"\n请求参数:")
    print(json.dumps(payload, indent=2, ensure_ascii=False))

    try:
        response = requests.post(
            API_ENDPOINT,
            headers=HEADERS,
            json=payload,
            timeout=10
        )
        print_result(response, "缺少必填参数")
    except Exception as e:
        print(f"\n❌ 测试失败 - {str(e)}")


def test_different_stores():
    """测试 8: 不同门店的预约"""
    print_separator("测试 8: 不同门店的预约")

    stores = [
        "花木店",
        "新天地店",
        "陆家嘴中心店",
        "静安寺（CP静安）店"
    ]

    for store in stores:
        print(f"\n--- 测试门店: {store} ---")
        create_booking(
            mobile=TEST_MOBILE,
            store_name=store,
            service_name=TEST_SERVICE,
            count=1,
            book_time=TEST_TIME,
            test_name=f"门店: {store}"
        )


def test_different_services():
    """测试 9: 不同服务的预约"""
    print_separator("测试 9: 不同服务的预约")

    services = [
        "泰式精油全身护理-90分钟",
        "古法·重点加强-120分钟",
        "椰香按摩-90分钟",
        "泰式深度拉伸（60分钟）"
    ]

    for service in services:
        print(f"\n--- 测试服务: {service} ---")
        create_booking(
            mobile=TEST_MOBILE,
            store_name=TEST_STORE,
            service_name=service,
            count=1,
            book_time=TEST_TIME,
            test_name=f"服务: {service}"
        )


def main():
    """主函数 - 运行所有测试"""
    print("=" * 60)
    print("  兰泰式按摩预约 API 测试套件")
    print("=" * 60)
    print(f"\nAPI Endpoint: {API_ENDPOINT}")
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"默认手机号: {TEST_MOBILE}")
    print(f"默认门店: {TEST_STORE}")
    print(f"默认服务: {TEST_SERVICE}")
    print(f"默认人数: {TEST_COUNT}")
    print(f"默认时间: {TEST_TIME}")

    print("\n提示: 这些测试会实际调用 API，请确保:")
    print("  1. 网络连接正常")
    print("  2. API Endpoint 配置正确")
    print("  3. 测试数据符合业务规则")

    input("\n按 Enter 键开始测试...")

    # 运行测试
    test_valid_booking()
    test_invalid_phone()
    test_invalid_store()
    test_invalid_service()
    test_invalid_count()
    test_past_time()
    test_missing_parameters()
    test_different_stores()
    test_different_services()

    print_separator("测试完成")
    print("\n所有测试已执行完毕。")
    print("请检查上方的测试结果，确认 API 行为是否符合预期。")


if __name__ == "__main__":
    main()
