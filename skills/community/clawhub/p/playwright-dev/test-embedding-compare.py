#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阿里云 Embedding API 两种调用方法对比测试
虾虾专用测试脚本～才不是专门为你写的呢！
"""

import time
import json
import sys

# 设置 UTF-8 编码
sys.stdout.reconfigure(encoding='utf-8')

# 配置
API_KEY = "sk-1f3847debc3e492e81f64115b20c6d82"
TEST_TEXTS = ["阿里云 Embedding API 测试", "今天是 2026 年 3 月 14 日", "向量模型真好用"]

print("=" * 70)
print("虾虾测试报告 - 阿里云 Embedding API 两种方法对比")
print("=" * 70)
print()

# ============================================================
# 方法 1: dashscope 库（上次的方法）
# ============================================================
print("【方法 1】dashscope 库（阿里云官方库）")
print("-" * 70)

try:
    import dashscope
    from dashscope import TextEmbedding
    
    dashscope.api_key = API_KEY
    
    start_time = time.time()
    
    response = TextEmbedding.call(
        model="text-embedding-v3",
        input=TEST_TEXTS
    )
    
    end_time = time.time()
    
    if response.status_code == 200:
        embeddings = response.output["embeddings"]
        usage = response.usage
        
        print(f"状态：成功")
        print(f"耗时：{(end_time - start_time)*1000:.2f} ms")
        print(f"返回数量：{len(embeddings)} 个向量")
        print(f"向量维度：{len(embeddings[0]['embedding'])} 维")
        print(f"模型：{response.output.get('model', 'text-embedding-v3')}")
        print(f"token 数：{usage.get('total_tokens', 'N/A')}")
        print(f"前 5 个向量值：{embeddings[0]['embedding'][:5]}")
        
        dashscope_result = {
            "success": True,
            "time_ms": round((end_time - start_time)*1000, 2),
            "count": len(embeddings),
            "dimensions": len(embeddings[0]['embedding']),
            "model": response.output.get('model', 'text-embedding-v3'),
            "tokens": usage.get('total_tokens', 0),
            "first_5_values": embeddings[0]['embedding'][:5]
        }
    else:
        print(f"失败 - {response.code} - {response.message}")
        dashscope_result = {"success": False, "error": str(response.code)}
        
except Exception as e:
    print(f"错误：{e}")
    dashscope_result = {"success": False, "error": str(e)}

print()

# ============================================================
# 方法 2: openai 库（今晚的方法）
# ============================================================
print("【方法 2】openai 库（OpenAI 兼容接口）")
print("-" * 70)

try:
    from openai import OpenAI
    
    client = OpenAI(
        api_key=API_KEY,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    
    start_time = time.time()
    
    response = client.embeddings.create(
        model="text-embedding-v3",
        input=TEST_TEXTS
    )
    
    end_time = time.time()
    
    embeddings = response.data
    usage = response.usage
    
    print(f"状态：成功")
    print(f"耗时：{(end_time - start_time)*1000:.2f} ms")
    print(f"返回数量：{len(embeddings)} 个向量")
    print(f"向量维度：{len(embeddings[0].embedding)} 维")
    print(f"模型：{response.model}")
    print(f"token 数：{usage.total_tokens}")
    print(f"前 5 个向量值：{embeddings[0].embedding[:5]}")
    
    openai_result = {
        "success": True,
        "time_ms": round((end_time - start_time)*1000, 2),
        "count": len(embeddings),
        "dimensions": len(embeddings[0].embedding),
        "model": response.model,
        "tokens": usage.total_tokens,
        "first_5_values": embeddings[0].embedding[:5]
    }
    
except Exception as e:
    print(f"错误：{e}")
    openai_result = {"success": False, "error": str(e)}

print()

# ============================================================
# 对比总结
# ============================================================
print("=" * 70)
print("对比总结")
print("=" * 70)
print()

# 对比表格
print("| 项目 | dashscope 库 | openai 库 |")
print("|------|-------------|----------|")
print(f"| 状态 | {'成功' if dashscope_result.get('success') else '失败'} | {'成功' if openai_result.get('success') else '失败'} |")
print(f"| 耗时 | {dashscope_result.get('time_ms', 'N/A')} ms | {openai_result.get('time_ms', 'N/A')} ms |")
print(f"| 返回数量 | {dashscope_result.get('count', 'N/A')} | {openai_result.get('count', 'N/A')} |")
print(f"| 向量维度 | {dashscope_result.get('dimensions', 'N/A')} | {openai_result.get('dimensions', 'N/A')} |")
print(f"| token 数 | {dashscope_result.get('tokens', 'N/A')} | {openai_result.get('tokens', 'N/A')} |")
print(f"| 依赖库 | dashscope | openai |")
print()

# 向量对比
if dashscope_result.get('success') and openai_result.get('success'):
    print("向量值对比（前 3 个）：")
    print(f"  dashscope: {dashscope_result['first_5_values'][:3]}")
    print(f"  openai:    {openai_result['first_5_values'][:3]}")
    
    # 检查是否一致
    match = dashscope_result['first_5_values'] == openai_result['first_5_values']
    print(f"  向量一致：{match}")
    print()

# 优缺点分析
print("优缺点分析：")
print()
print("【dashscope 库】")
print("  优点：")
print("    - 阿里云官方库，原生支持")
print("    - 功能更全面（支持更多阿里云模型）")
print("    - 文档更详细")
print("  缺点：")
print("    - 需要单独安装（pip install dashscope）")
print("    - 接口相对复杂")
print()
print("【openai 库】")
print("  优点：")
print("    - 通用接口，兼容性好")
print("    - 代码更简洁")
print("    - 容易切换其他兼容 API")
print("  缺点：")
print("    - 需要配置 base_url")
print("    - 不是官方库")
print()

# 推荐
print("虾虾推荐：")
if dashscope_result.get('success') and openai_result.get('success'):
    print("  两种方法都能用！看你的需求：")
    print("  - 如果只用阿里云 -> 用 dashscope 库")
    print("  - 如果要兼容多个 API -> 用 openai 库")
    print("  - 虾虾更喜欢 openai 库，代码更简洁！")
else:
    print("  哪个能用用哪个！")

print()
print("=" * 70)
