#!/usr/bin/env python3
"""
调试createDocWithMd API
"""

import json
import requests

API_URL = "http://192.168.1.6:6811"
TOKEN = "xz1eblvxst0zqcpm"

headers = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json'
}

def test_createDocWithMd():
    """测试createDocWithMd API"""
    print("=" * 60)
    print("调试createDocWithMd API")
    print("=" * 60)
    
    # 获取笔记本ID
    print("\n1️⃣ 获取笔记本列表...")
    response = requests.post(
        f'{API_URL}/api/notebook/lsNotebooks',
        headers=headers,
        json={},
        timeout=10
    )
    
    notebooks = response.json().get('data', {}).get('notebooks', [])
    notebook_id = None
    for nb in notebooks:
        if nb['name'] == "其他":
            notebook_id = nb['id']
            print(f"✅ 找到笔记本: {nb['name']} (ID: {nb['id']})")
            break
    
    if not notebook_id:
        print("❌ 未找到笔记本")
        return False
    
    # 测试不同的createDocWithMd参数组合
    from datetime import datetime
    document_name = f"调试测试_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    test_cases = [
        {
            'name': '基本参数',
            'params': {
                'notebook': notebook_id,
                'path': f'/{document_name}',
                'markdown': f'# {document_name}\\n\\n这是测试内容。'
            }
        },
        {
            'name': '包含parentID',
            'params': {
                'notebook': notebook_id,
                'path': f'/{document_name}',
                'markdown': f'# {document_name}\\n\\n这是测试内容。',
                'parentID': ''
            }
        },
        {
            'name': '包含tags',
            'params': {
                'notebook': notebook_id,
                'path': f'/{document_name}',
                'markdown': f'# {document_name}\\n\\n这是测试内容。',
                'tags': ['测试', '调试']
            }
        },
        {
            'name': '完整参数（基于Chrome扩展）',
            'params': {
                'notebook': notebook_id,
                'path': f'/{document_name}',
                'markdown': f'# {document_name}\\n\\n这是测试内容。',
                'withMath': False,
                'tags': ['测试', '调试'],
                'clippingHref': '',
                'listDocTree': True
            }
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\n{i}️⃣ 测试: {test_case['name']}")
        print(f"📋 参数: {json.dumps(test_case['params'], ensure_ascii=False)}")
        
        try:
            response = requests.post(
                f'{API_URL}/api/filetree/createDocWithMd',
                headers=headers,
                json=test_case['params'],
                timeout=10
            )
            
            print(f"📡 HTTP状态: {response.status_code}")
            print(f"📊 响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
            
            result = response.json()
            if result.get('code') == 0:
                doc_id = result.get('data')
                if doc_id:
                    print(f"✅ 成功! 文档ID: {doc_id}")
                    
                    # 验证文档
                    verify_response = requests.post(
                        f'{API_URL}/api/filetree/listDocsByPath',
                        headers=headers,
                        json={
                            'notebook': notebook_id,
                            'path': '/'
                        },
                        timeout=10
                    )
                    
                    docs = verify_response.json().get('data', {}).get('files', [])
                    for doc in docs:
                        if document_name in doc.get('name', ''):
                            print(f"✅ 验证成功: 文档存在于列表中")
                            print(f"   名称: {doc.get('name')}")
                            print(f"   ID: {doc.get('id')}")
                    
                else:
                    print(f"⚠️  返回成功但data为null")
            else:
                print(f"❌ API错误: {result.get('msg')}")
                
        except Exception as e:
            print(f"❌ 异常: {e}")
    
    # 尝试使用createDoc API
    print(f"\n🆕 测试: createDoc API")
    try:
        response = requests.post(
            f'{API_URL}/api/filetree/createDoc',
            headers=headers,
            json={
                'notebook': notebook_id,
                'path': f'/{document_name}_createDoc',
                'title': document_name + '_createDoc'
            },
            timeout=10
        )
        
        print(f"📡 HTTP状态: {response.status_code}")
        print(f"📊 响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
    except Exception as e:
        print(f"❌ 异常: {e}")
    
    # 尝试使用createDailyNote API
    print(f"\n🆕 测试: createDailyNote API")
    try:
        response = requests.post(
            f'{API_URL}/api/filetree/createDailyNote',
            headers=headers,
            json={
                'notebook': notebook_id,
                'date': '20260217'
            },
            timeout=10
        )
        
        print(f"📡 HTTP状态: {response.status_code}")
        print(f"📊 响应内容: {json.dumps(response.json(), ensure_ascii=False, indent=2)}")
        
        result = response.json()
        if result.get('code') == 0:
            doc_id = result.get('data')
            print(f"✅ 成功! 文档ID: {doc_id}")
        
    except Exception as e:
        print(f"❌ 异常: {e}")

if __name__ == "__main__":
    test_createDocWithMd()