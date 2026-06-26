#!/usr/bin/env python3
"""
Test script for vector service.

Usage:
    # Test with running service
    python test-vector.py "编程语言偏好"
    
    # Test local encoding (no service required)
    python test-vector.py --local "编程语言偏好"
"""

import argparse
import json
import sys
import http.client
from typing import Optional

try:
    from sentence_transformers import SentenceTransformer
    import numpy as np
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False


# Sample test documents
TEST_DOCS = [
    {
        "id": "doc1",
        "content": "用户喜欢使用 TypeScript 进行前端开发，认为 TypeScript 的类型系统大大提高了代码质量。",
        "metadata": {"tags": ["编程语言", "前端"], "location": "preferences"}
    },
    {
        "id": "doc2", 
        "content": "用户偏好 Python 用于数据分析和机器学习项目，熟悉 pandas、numpy 和 scikit-learn。",
        "metadata": {"tags": ["编程语言", "数据科学"], "location": "preferences"}
    },
    {
        "id": "doc3",
        "content": "用户经常使用 Rust 编写高性能系统程序，对内存安全和并发编程有深入了解。",
        "metadata": {"tags": ["编程语言", "系统编程"], "location": "preferences"}
    },
    {
        "id": "doc4",
        "content": "用户每天早上 8 点起床，喜欢喝咖啡，然后开始工作。",
        "metadata": {"tags": ["生活习惯", "日常"], "location": "daily"}
    },
    {
        "id": "doc5",
        "content": "用户对 React 框架非常熟悉，经常使用 Next.js 构建全栈应用。",
        "metadata": {"tags": ["前端", "框架"], "location": "skills"}
    }
]


def test_local(query: str):
    """Test vector search locally without service."""
    if not HAS_TRANSFORMERS:
        print("Error: sentence-transformers not installed. Run: pip install sentence-transformers numpy")
        sys.exit(1)
    
    # Use mirror if huggingface.co is unreachable
    import os
    if 'HF_ENDPOINT' not in os.environ:
        os.environ['HF_ENDPOINT'] = 'https://hf-mirror.com'
    
    print(f"Loading model...")
    model = SentenceTransformer('BAAI/bge-small-zh-v1.5')
    
    # Index documents
    print(f"\nIndexing {len(TEST_DOCS)} test documents...")
    doc_texts = [doc['content'] for doc in TEST_DOCS]
    doc_embeddings = model.encode(doc_texts, normalize_embeddings=True)
    
    # Encode query
    print(f"\nQuery: {query}")
    query_embedding = model.encode([query], normalize_embeddings=True)[0]
    
    # Calculate similarities
    similarities = []
    for i, doc in enumerate(TEST_DOCS):
        sim = float(np.dot(query_embedding, doc_embeddings[i]))
        similarities.append({
            'id': doc['id'],
            'content': doc['content'][:50] + '...',
            'score': sim,
            'metadata': doc['metadata']
        })
    
    # Sort by score
    similarities.sort(key=lambda x: x['score'], reverse=True)
    
    print("\n=== Search Results ===")
    for i, result in enumerate(similarities, 1):
        print(f"\n{i}. [{result['score']:.4f}] {result['id']}")
        print(f"   Content: {result['content']}")
        print(f"   Tags: {result['metadata'].get('tags', [])}")
    
    # Check if top result matches expected
    top_result = similarities[0]
    if 'TypeScript' in top_result['content'] or 'Python' in top_result['content']:
        print(f"\n✓ Test PASSED: Top result is relevant to programming language preferences")
    else:
        print(f"\n✗ Test FAILED: Top result should be about programming languages")
    
    return similarities


def test_service(query: str, host: str = '127.0.0.1', port: int = 8765):
    """Test vector service via HTTP."""
    
    def make_request(endpoint: str, data: dict) -> dict:
        conn = http.client.HTTPConnection(host, port)
        try:
            conn.request('POST', endpoint, 
                        body=json.dumps(data),
                        headers={'Content-Type': 'application/json'})
            response = conn.getresponse()
            return json.loads(response.read().decode('utf-8'))
        finally:
            conn.close()
    
    # Health check
    try:
        conn = http.client.HTTPConnection(host, port)
        conn.request('GET', '/health')
        response = conn.getresponse()
        health = json.loads(response.read().decode('utf-8'))
        conn.close()
        print(f"Service health: {health}")
    except Exception as e:
        print(f"Error: Cannot connect to vector service at {host}:{port}")
        print(f"Make sure to start it first: python vector-service.py")
        sys.exit(1)
    
    # Index documents
    print(f"\nIndexing {len(TEST_DOCS)} test documents...")
    for doc in TEST_DOCS:
        result = make_request('/index', {
            'id': doc['id'],
            'content': doc['content'],
            'metadata': doc['metadata']
        })
        print(f"  Indexed: {doc['id']}")
    
    # Search
    print(f"\nQuery: {query}")
    result = make_request('/search', {
        'query': query,
        'topK': 5
    })
    
    print("\n=== Search Results ===")
    for i, item in enumerate(result.get('results', []), 1):
        print(f"\n{i}. [{item['score']:.4f}] {item['id']}")
        if item.get('metadata'):
            print(f"   Tags: {item['metadata'].get('tags', [])}")
    
    # Check if top result matches expected
    results = result.get('results', [])
    if results:
        top_id = results[0]['id']
        if top_id in ['doc1', 'doc2', 'doc3']:
            print(f"\n✓ Test PASSED: Top result is relevant to programming language preferences")
        else:
            print(f"\n✗ Test FAILED: Top result should be about programming languages")
    
    return results


def main():
    parser = argparse.ArgumentParser(description='Test vector service')
    parser.add_argument('query', help='Search query')
    parser.add_argument('--local', action='store_true', help='Test locally without service')
    parser.add_argument('--host', default='127.0.0.1', help='Service host')
    parser.add_argument('--port', type=int, default=8765, help='Service port')
    args = parser.parse_args()
    
    if args.local:
        test_local(args.query)
    else:
        test_service(args.query, args.host, args.port)


if __name__ == '__main__':
    main()