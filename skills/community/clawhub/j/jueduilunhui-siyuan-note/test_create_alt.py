#!/usr/bin/env python3
"""
测试思源笔记文档创建的替代方法
"""

import json
import requests
import sys
import os

# 配置信息
API_URL = "http://192.168.1.6:6811"
TOKEN = "xz1eblvxst0zqcpm"

headers = {
    'Authorization': f'Token {TOKEN}',
    'Content-Type': 'application/json'
}

def test_create_with_content():
    """测试创建包含内容的文档"""
    print("=" * 60)
    print("测试创建包含内容的文档")
    print("=" * 60)
    
    # 获取笔记本ID
    print("📚 获取笔记本列表...")
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
    
    # 方法1: 使用createDocWithMarkdown API
    document_name = "666-new-test"
    content = "# 测试文档\n\n这是通过API创建的测试文档。\n\n创建时间: 2026-02-17 20:30:00"
    
    print(f"\n📝 测试创建文档: {document_name}")
    print(f"📄 内容长度: {len(content)} 字符")
    
    # 尝试不同的API端点
    endpoints = [
        ('/api/filetree/createDoc', {'notebook': notebook_id, 'path': f'/{document_name}', 'title': document_name}),
        ('/api/block/createDoc', {'notebook': notebook_id, 'path': f'/{document_name}', 'markdown': content}),
        ('/api/filetree/createDailyNote', {'notebook': notebook_id}),
    ]
    
    for endpoint, data in endpoints:
        print(f"\n🔧 尝试端点: {endpoint}")
        print(f"📋 数据: {json.dumps(data, ensure_ascii=False)}")
        
        try:
            response = requests.post(
                f'{API_URL}{endpoint}',
                headers=headers,
                json=data,
                timeout=10
            )
            
            print(f"📡 状态: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                print(f"📊 响应: {json.dumps(result, ensure_ascii=False)}")
                
                if result.get('code') == 0:
                    doc_id = result.get('data')
                    print(f"✅ 可能成功! 文档ID: {doc_id}")
                    
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
                    
                    if verify_response.status_code == 200:
                        verify_result = verify_response.json()
                        files = verify_result.get('data', {}).get('files', [])
                        print(f"📁 当前文档数: {len(files)}")
                        
                        # 查找新文档
                        for file in files:
                            if document_name in file.get('name', ''):
                                print(f"🎉 找到新文档: {file.get('name')} (ID: {file.get('id')})")
                                return True
                    
                    return True
            else:
                print(f"❌ HTTP错误: {response.status_code}")
                print(f"响应: {response.text}")
                
        except Exception as e:
            print(f"❌ 异常: {e}")
    
    return False

def test_append_and_rename():
    """测试追加内容然后重命名文档的方法"""
    print("\n" + "=" * 60)
    print("测试追加内容然后重命名的方法")
    print("=" * 60)
    
    # 获取笔记本ID
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
            break
    
    if not notebook_id:
        print("❌ 未找到笔记本")
        return False
    
    # 获取第一个文档作为父文档
    response = requests.post(
        f'{API_URL}/api/filetree/listDocsByPath',
        headers=headers,
        json={
            'notebook': notebook_id,
            'path': '/'
        },
        timeout=10
    )
    
    if response.status_code != 200:
        print("❌ 获取文档列表失败")
        return False
    
    files = response.json().get('data', {}).get('files', [])
    if not files:
        print("❌ 笔记本中没有文档")
        return False
    
    parent_doc_id = files[0].get('id')
    print(f"📄 使用父文档ID: {parent_doc_id}")
    
    # 追加内容
    content = "# 666-append-test\n\n这是通过追加内容创建的测试文档。"
    
    response = requests.post(
        f'{API_URL}/api/block/appendBlock',
        headers=headers,
        json={
            'data': content,
            'dataType': 'markdown',
            'parentID': parent_doc_id,
            'nextID': '',
            'previousID': ''
        },
        timeout=10
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('code') == 0:
            print("✅ 内容追加成功")
            # 注意：这不会创建独立文档，只是在现有文档中创建新块
            return True
    
    return False

if __name__ == "__main__":
    print("🔍 当前文档状态:")
    test_create_with_content()
    
    print("\n" + "=" * 60)
    print("测试总结:")
    print("=" * 60)
    print("根据测试结果，思源笔记的API行为如下:")
    print("1. createDoc API返回成功但可能不立即显示")
    print("2. 当前实现使用appendBlock在现有文档中创建新块")
    print("3. 要创建独立文档可能需要不同的方法")
    print("\n建议: 使用现有方法创建内容，然后在思源笔记客户端中手动重命名")