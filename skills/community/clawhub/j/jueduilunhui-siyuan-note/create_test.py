#!/usr/bin/env python3
"""
测试创建思源笔记文档
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from siyuan_note import SiYuanNote

def test_create_document():
    """测试创建文档功能"""
    print("=" * 60)
    print("测试创建思源笔记文档")
    print("=" * 60)
    
    # 初始化
    siyuan = SiYuanNote()
    
    # 测试连接
    print("🧪 测试连接...")
    if not siyuan.test_connection():
        print("❌ 连接失败")
        return False
    
    print("✅ 连接成功")
    
    # 获取笔记本列表
    print("\n📚 获取笔记本列表...")
    notebooks = siyuan.get_notebooks()
    print(f"✅ 找到 {len(notebooks)} 个笔记本")
    
    # 查找'其他'笔记本
    target_notebook = "其他"
    notebook_id = None
    for nb in notebooks:
        if nb['name'] == target_notebook:
            notebook_id = nb['id']
            print(f"✅ 找到笔记本: {nb['name']} (ID: {nb['id']})")
            break
    
    if not notebook_id:
        print(f"❌ 未找到笔记本: {target_notebook}")
        return False
    
    # 创建新文档
    document_name = "666"
    content = "这是通过OpenClaw思源笔记技能创建的测试文档。\n\n创建时间: 2026-02-17 20:30:00\n\n## 测试内容\n这是一个测试文档，用于验证思源笔记技能的创建功能。"
    
    print(f"\n📝 创建新文档: {document_name}")
    print(f"📂 位置: {target_notebook} 笔记本")
    
    doc_id = siyuan.create_document(target_notebook, document_name, content)
    
    if doc_id:
        print(f"✅ 文档创建成功!")
        print(f"📄 文档ID: {doc_id}")
        print(f"📁 位置: 思源笔记 -> {target_notebook} -> {document_name}")
        
        # 验证文档是否存在
        print("\n🔍 验证文档创建...")
        documents = siyuan.get_documents(notebook_id)
        found = False
        for doc in documents:
            if doc['name'] == document_name:
                found = True
                print(f"✅ 验证成功: 找到文档 {document_name}")
                print(f"📄 文档信息: ID={doc['id']}, 名称={doc['name']}")
                break
        
        if not found:
            print(f"⚠️  文档创建成功但未在列表中立即找到，可能需要刷新")
        
        return True
    else:
        print("❌ 文档创建失败")
        return False

if __name__ == "__main__":
    success = test_create_document()
    print("\n" + "=" * 60)
    if success:
        print("🎉 测试完成 - 文档创建成功!")
    else:
        print("❌ 测试完成 - 文档创建失败")
    print("=" * 60)