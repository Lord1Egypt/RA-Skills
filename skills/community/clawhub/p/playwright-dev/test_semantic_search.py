#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试语义搜索 - 阿里云 Embedding-v3
"""

import os
import json
import dashscope
from dashscope import TextEmbedding
from chromadb import PersistentClient

# 配置
WORKSPACE = r"C:\Users\Xiabi\.openclaw\workspace"
CHROMA_DB_PATH = os.path.join(WORKSPACE, "chroma_db")
API_KEY = "sk-1f3847debc3e492e81f64115b20c6d82"

dashscope.api_key = API_KEY

def get_embedding(text):
    """获取单个文本的向量"""
    try:
        response = TextEmbedding.call(
            model='text-embedding-v3',
            input=text
        )
        
        if isinstance(response, dict):
            if 'output' in response and 'embeddings' in response['output']:
                return response['output']['embeddings'][0]['embedding']
        else:
            if hasattr(response, 'output') and hasattr(response.output, 'embeddings'):
                return response.output.embeddings[0]['embedding']
        
        print(f"Response format error: {response}")
        return None
    except Exception as e:
        print(f"Get embedding error: {e}")
        return None

def main():
    print("=" * 60)
    print("Starting semantic search test...")
    print("=" * 60)
    
    # 加载数据库
    print("\nLoading ChromaDB...")
    client = PersistentClient(path=CHROMA_DB_PATH)
    collection = client.get_collection(name='user_preferences')
    print("Database loaded")
    
    # 测试用例
    test_queries = [
        ("瀑布", "找到 2 月 20 日关于天台瀑布的对话"),
        ("TTS 使用规范", "找到 3 月 9 日关于 TTS 最佳实践的记录"),
        ("供应商直连系统", "找到项目进度相关记录"),
        ("表情图片发送", "找到表情图片相关的偏好设置"),
        ("向量数据库", "找到 Embedding 配置相关记录")
    ]
    
    results_summary = []
    
    print("\n" + "=" * 60)
    print("Running test queries...")
    print("=" * 60)
    
    for query, expected in test_queries:
        print(f"\nQuery: {query}")
        print(f"  Expected: {expected}")
        
        # 生成查询向量
        query_embedding = get_embedding(query)
        
        if not query_embedding:
            print("  ERROR: Embedding generation failed")
            results_summary.append({
                'query': query,
                'expected': expected,
                'results': [],
                'success': False
            })
            continue
        
        # 搜索相似内容
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=3,
            include=['documents', 'metadatas', 'distances']
        )
        
        result_count = len(results['documents'][0]) if results['documents'] else 0
        print(f"  Found {result_count} results:")
        
        result_docs = []
        if result_count > 0:
            for i in range(result_count):
                source = results['metadatas'][0][i].get('source', 'unknown')
                content_preview = results['documents'][0][i][:100].replace('\n', ' ')
                distance = results['distances'][0][i] if results['distances'] else 0
                print(f"  {i+1}. [{source}] {content_preview}... (distance: {distance:.4f})")
                result_docs.append({
                    'source': source,
                    'content': results['documents'][0][i][:200],
                    'distance': distance
                })
        
        # 评估准确率
        success = result_count > 0
        results_summary.append({
            'query': query,
            'expected': expected,
            'results': result_docs,
            'success': success,
            'result_count': result_count
        })
        
        if success:
            print("  SUCCESS")
        else:
            print("  FAILED")
    
    # 保存测试结果
    from datetime import datetime
    test_results = {
        'timestamp': datetime.now().isoformat(),
        'test_queries': test_queries,
        'results': results_summary,
        'total_tests': len(test_queries),
        'successful_tests': sum(1 for r in results_summary if r['success']),
        'success_rate': sum(1 for r in results_summary if r['success']) / len(test_queries) * 100
    }
    
    results_file = os.path.join(WORKSPACE, "semantic_search_test_results.json")
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(test_results, f, ensure_ascii=False, indent=2)
    
    print(f"\nTest results saved to: {results_file}")
    
    # 打印总结
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    print(f"Total tests: {test_results['total_tests']}")
    print(f"Successful: {test_results['successful_tests']}")
    print(f"Success rate: {test_results['success_rate']:.1f}%")
    
    return test_results

if __name__ == "__main__":
    main()
