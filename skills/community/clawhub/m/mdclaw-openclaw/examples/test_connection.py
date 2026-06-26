#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MDClaw OpenClaw 连接测试脚本

用于测试 API 连接和基本功能
"""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mdclaw_client import MDClawClient


def test_client_init():
    """测试 1: 客户端初始化"""
    print("=" * 60)
    print("测试 1: 客户端初始化")
    print("=" * 60)

    try:
        client = MDClawClient()
        print(f"✅ 客户端初始化成功")
        print(f"   网关地址: {client.GATEWAY_URL}")
        print(f"   API Key: {client.api_key[:10]}..." if client.api_key else "   API Key: (未设置)")
        return True
    except ValueError as e:
        print(f"❌ 客户端初始化失败: {e}")
        return False
    except Exception as e:
        print(f"❌ 客户端初始化失败: {e}")
        return False


def test_text_to_image():
    """测试 2: 文生图"""
    print("\n" + "=" * 60)
    print("测试 2: 文生图")
    print("=" * 60)

    try:
        client = MDClawClient()
        result = client.text_to_image(
            prompt="测试图片",
            aspect_ratio="1:1"
        )

        if result.get('success'):
            print(f"✅ 文生图测试成功")
            print(f"   图片URL: {result['result']['image_urls'][0]}")
            return True
        else:
            print(f"❌ 文生图测试失败: {result.get('error')}")
            return False
    except Exception as e:
        print(f"❌ 文生图测试异常: {e}")
        return False


def test_text_to_speech():
    """测试 3: 文字转语音"""
    print("\n" + "=" * 60)
    print("测试 3: 文字转语音")
    print("=" * 60)

    try:
        client = MDClawClient()
        result = client.text_to_speech("这是一段测试语音")

        if result.get('success'):
            print(f"✅ 文字转语音测试成功")
            print(f"   音频URL: {result['result']['audio_url']}")
            return True
        else:
            print(f"❌ 文字转语音测试失败: {result.get('error')}")
            return False
    except Exception as e:
        print(f"❌ 文字转语音测试异常: {e}")
        return False


def test_video_status():
    """测试 4: 视频状态查询"""
    print("\n" + "=" * 60)
    print("测试 4: 视频状态查询")
    print("=" * 60)

    try:
        client = MDClawClient()
        # 用一个假的 task_id 测试 API 响应
        result = client.video_status("test_task_id_123")

        print(f"✅ 视频状态查询成功")
        print(f"   响应: {json.dumps(result, indent=2, ensure_ascii=False)}")
        return True
    except Exception as e:
        print(f"❌ 视频状态查询异常: {e}")
        return False


def test_ai_search():
    """测试 5: AI 搜索"""
    print("\n" + "=" * 60)
    print("测试 5: AI 搜索")
    print("=" * 60)

    try:
        client = MDClawClient()
        result = client.ai_search("今天天气怎么样")

        if result.get('success'):
            print(f"✅ AI 搜索测试成功")
            print(f"   结果: {result.get('result', {}).get('answer', 'N/A')[:100]}...")
            return True
        else:
            print(f"❌ AI 搜索测试失败: {result.get('error')}")
            return False
    except Exception as e:
        print(f"❌ AI 搜索测试异常: {e}")
        return False


def test_error_handling():
    """测试 6: 错误处理"""
    print("\n" + "=" * 60)
    print("测试 6: 错误处理")
    print("=" * 60)

    try:
        # 测试无 API Key 时的错误处理
        original_key = os.environ.get('MDCLAW_API_KEY')
        if original_key:
            del os.environ['MDCLAW_API_KEY']

        try:
            client = MDClawClient()
            print(f"❌ 应该抛出 ValueError 但没有")
            return False
        except ValueError as e:
            print(f"✅ 正确抛出 ValueError: {str(e)[:50]}...")
            return True
        finally:
            if original_key:
                os.environ['MDCLAW_API_KEY'] = original_key
    except Exception as e:
        print(f"❌ 错误处理测试异常: {e}")
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("MDClaw OpenClaw 连接测试")
    print("=" * 60)

    if not os.getenv('MDCLAW_API_KEY'):
        print("⚠️ 请设置环境变量 MDCLAW_API_KEY")
        print("   export MDCLAW_API_KEY='你的API Key'")
        return

    tests = [
        ("客户端初始化", test_client_init),
        ("文生图", test_text_to_image),
        ("文字转语音", test_text_to_speech),
        ("视频状态查询", test_video_status),
        ("AI 搜索", test_ai_search),
        ("错误处理", test_error_handling),
    ]

    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n❌ 测试 '{name}' 执行时发生异常: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, False))

    # 打印测试总结
    print("\n" + "=" * 60)
    print("测试总结")
    print("=" * 60)

    passed = 0
    failed = 0

    for name, result in results:
        status = "✅ 通过" if result else "❌ 失败"
        print(f"{name}: {status}")
        if result:
            passed += 1
        else:
            failed += 1

    print("\n" + "=" * 60)
    print(f"总计: {len(results)} 个测试")
    print(f"通过: {passed} 个")
    print(f"失败: {failed} 个")
    print(f"成功率: {passed/len(results)*100:.1f}%")
    print("=" * 60)

    sys.exit(0 if failed == 0 else 1)


if __name__ == "__main__":
    main()
