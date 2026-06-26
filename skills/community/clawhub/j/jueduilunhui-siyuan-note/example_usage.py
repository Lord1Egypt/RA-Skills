#!/usr/bin/env python3
"""
思源笔记技能使用示例
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from siyuan_note import SiYuanNote, ConversationData

def example_1_test_connection():
    """示例1：测试连接"""
    print("=" * 60)
    print("示例1：测试思源笔记连接")
    print("=" * 60)
    
    siyuan = SiYuanNote()
    
    if siyuan.test_connection():
        print("✅ 连接成功！")
    else:
        print("❌ 连接失败")
    
    return siyuan

def example_2_query_notebooks():
    """示例2：查询笔记本"""
    print("\n" + "=" * 60)
    print("示例2：查询思源笔记笔记本")
    print("=" * 60)
    
    siyuan = SiYuanNote()
    
    # 获取所有笔记本
    notebooks = siyuan.get_notebooks()
    
    if notebooks:
        print(f"✅ 找到 {len(notebooks)} 个笔记本:")
        for i, notebook in enumerate(notebooks, 1):
            print(f"  {i}. {notebook['name']} (ID: {notebook['id']})")
    else:
        print("❌ 未找到笔记本")
    
    return siyuan

def example_3_query_documents():
    """示例3：查询文档"""
    print("\n" + "=" * 60)
    print("示例3：查询思源笔记文档")
    print("=" * 60)
    
    siyuan = SiYuanNote()
    
    # 获取默认笔记本的文档
    notebook_id = siyuan.get_notebook_id("其他")
    
    if notebook_id:
        print(f"✅ 找到笔记本 '其他' (ID: {notebook_id})")
        
        documents = siyuan.get_documents(notebook_id)
        
        if documents:
            print(f"✅ 找到 {len(documents)} 个文档:")
            for i, doc in enumerate(documents, 1):
                doc_name = doc.get('name', '').replace('.sy', '')
                print(f"  {i}. {doc_name} (ID: {doc.get('id')})")
        else:
            print("❌ 未找到文档")
    else:
        print("❌ 未找到笔记本 '其他'")
    
    return siyuan

def example_4_search_content():
    """示例4：搜索内容"""
    print("\n" + "=" * 60)
    print("示例4：搜索思源笔记内容")
    print("=" * 60)
    
    siyuan = SiYuanNote()
    
    # 搜索关键词
    query = "OpenChat"
    results = siyuan.search_content(query)
    
    if results:
        print(f"✅ 找到 {len(results)} 个包含 '{query}' 的内容:")
        for i, block in enumerate(results[:5], 1):  # 只显示前5个
            content = block.get('content', '')[:100] + "..." if len(block.get('content', '')) > 100 else block.get('content', '')
            print(f"  {i}. {content}")
        
        if len(results) > 5:
            print(f"  ... 还有 {len(results) - 5} 个结果")
    else:
        print(f"❌ 未找到包含 '{query}' 的内容")
    
    return siyuan

def example_5_sync_conversation():
    """示例5：同步对话"""
    print("\n" + "=" * 60)
    print("示例5：同步对话到思源笔记")
    print("=" * 60)
    
    siyuan = SiYuanNote()
    
    # 创建示例对话数据
    conversation_data = {
        'summary': '思源笔记技能测试对话',
        'messages': [
            {
                'role': 'user',
                'content': '你好，请测试思源笔记同步功能'
            },
            {
                'role': 'assistant',
                'content': '好的，我正在测试思源笔记同步功能。\n\n**测试项目:**\n1. 连接测试 ✅\n2. 笔记本查询 ✅\n3. 文档查询 ✅\n4. 内容搜索 ✅\n5. 对话同步 🔄'
            },
            {
                'role': 'user',
                'content': '请将这段对话同步到思源笔记'
            },
            {
                'role': 'assistant',
                'content': '正在同步到思源笔记...\n\n**目标位置:**\n- 笔记本: 其他\n- 文档: openchat\n\n同步完成后，您可以在思源笔记中查看这段对话记录。'
            }
        ],
        'conclusion': '思源笔记同步功能测试完成，所有功能正常。',
        'metadata': {
            'test_type': '功能验证',
            'test_time': '2026-02-17 20:00:00'
        }
    }
    
    # 同步对话
    success = siyuan.sync_conversation(conversation_data)
    
    if success:
        print("✅ 对话同步成功！")
        print("请查看思源笔记中的 '其他' 笔记本下的 'openchat' 文档")
    else:
        print("❌ 对话同步失败")
    
    return siyuan

def example_6_create_new_document():
    """示例6：创建新文档"""
    print("\n" + "=" * 60)
    print("示例6：创建新文档")
    print("=" * 60)
    
    siyuan = SiYuanNote()
    
    # 创建新文档
    new_doc_name = "OpenClaw测试文档"
    new_doc_content = """# OpenClaw测试文档

## 简介
这是一个通过OpenClaw创建的测试文档。

## 功能测试
- ✅ 文档创建功能
- ✅ 内容写入功能
- ✅ Markdown格式支持

## 使用说明
此文档用于测试OpenClaw与思源笔记的集成功能。

---
"""
    
    doc_id = siyuan.create_document("其他", new_doc_name, new_doc_content)
    
    if doc_id:
        print(f"✅ 文档创建成功: {new_doc_name}")
        print(f"文档ID: {doc_id}")
    else:
        print(f"❌ 文档创建失败: {new_doc_name}")
    
    return siyuan

def example_7_get_status():
    """示例7：获取状态"""
    print("\n" + "=" * 60)
    print("示例7：获取思源笔记连接状态")
    print("=" * 60)
    
    siyuan = SiYuanNote()
    
    # 测试连接
    connected = siyuan.test_connection()
    
    print(f"连接状态: {'✅ 已连接' if connected else '❌ 未连接'}")
    print(f"API地址: {siyuan.siyuan_config.api_url}")
    print(f"默认笔记本: {siyuan.sync_config.notebook_name}")
    print(f"默认文档: {siyuan.sync_config.document_name}")
    print(f"操作次数: {siyuan.operation_count}")
    print(f"错误次数: {siyuan.error_count}")
    
    if siyuan.last_operation_time:
        print(f"最后操作时间: {siyuan.last_operation_time}")
    
    return siyuan

def main():
    """主函数"""
    print("思源笔记技能使用示例")
    print("=" * 60)
    
    # 运行所有示例
    examples = [
        example_1_test_connection,
        example_2_query_notebooks,
        example_3_query_documents,
        example_4_search_content,
        example_5_sync_conversation,
        example_6_create_new_document,
        example_7_get_status
    ]
    
    for i, example_func in enumerate(examples, 1):
        try:
            example_func()
            print()  # 空行分隔
        except Exception as e:
            print(f"❌ 示例 {i} 执行失败: {e}")
            print()
    
    print("=" * 60)
    print("所有示例执行完成！")
    print("=" * 60)

if __name__ == "__main__":
    main()