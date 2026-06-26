#!/usr/bin/env python3
"""
思源笔记技能测试脚本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from siyuan_note import SiYuanNote

def test_basic_functionality():
    """测试基本功能"""
    print("🧪 测试思源笔记技能基本功能...")
    
    # 1. 创建实例
    print("1. 创建SiYuanNote实例...")
    siyuan = SiYuanNote()
    print(f"   API地址: {siyuan.siyuan_config.api_url}")
    print(f"   默认笔记本: {siyuan.sync_config.notebook_name}")
    print(f"   默认文档: {siyuan.sync_config.document_name}")
    
    # 2. 测试连接
    print("\n2. 测试连接...")
    connected = siyuan.test_connection()
    if connected:
        print("   ✅ 连接成功")
    else:
        print("   ❌ 连接失败")
        return False
    
    # 3. 获取笔记本
    print("\n3. 获取笔记本列表...")
    notebooks = siyuan.get_notebooks()
    if notebooks:
        print(f"   ✅ 找到 {len(notebooks)} 个笔记本")
        for nb in notebooks[:3]:  # 只显示前3个
            print(f"     - {nb['name']}")
        if len(notebooks) > 3:
            print(f"     ... 还有 {len(notebooks) - 3} 个")
    else:
        print("   ❌ 未找到笔记本")
    
    # 4. 获取默认笔记本ID
    print("\n4. 获取默认笔记本ID...")
    notebook_id = siyuan.get_notebook_id(siyuan.sync_config.notebook_name)
    if notebook_id:
        print(f"   ✅ 笔记本 '{siyuan.sync_config.notebook_name}' 的ID: {notebook_id}")
    else:
        print(f"   ❌ 未找到笔记本 '{siyuan.sync_config.notebook_name}'")
    
    # 5. 获取文档
    if notebook_id:
        print("\n5. 获取文档列表...")
        documents = siyuan.get_documents(notebook_id)
        if documents:
            print(f"   ✅ 找到 {len(documents)} 个文档")
            for doc in documents[:3]:  # 只显示前3个
                doc_name = doc.get('name', '').replace('.sy', '')
                print(f"     - {doc_name}")
            if len(documents) > 3:
                print(f"     ... 还有 {len(documents) - 3} 个")
        else:
            print("   ❌ 未找到文档")
    
    # 6. 测试搜索
    print("\n6. 测试内容搜索...")
    search_results = siyuan.search_content("测试")
    if search_results:
        print(f"   ✅ 找到 {len(search_results)} 个包含'测试'的内容")
    else:
        print("   ⚠️  未找到包含'测试'的内容（这可能是正常的）")
    
    print("\n🎉 基本功能测试完成！")
    return True

def test_sync_functionality():
    """测试同步功能"""
    print("\n🧪 测试思源笔记同步功能...")
    
    siyuan = SiYuanNote()
    
    # 创建测试对话数据
    test_conversation = {
        'summary': '思源笔记技能测试',
        'messages': [
            {
                'role': 'user',
                'content': '测试思源笔记同步功能'
            },
            {
                'role': 'assistant',
                'content': '正在测试思源笔记同步功能...\n\n**测试项目:**\n1. 连接测试\n2. 数据格式化\n3. 内容同步\n4. 错误处理'
            }
        ],
        'conclusion': '思源笔记同步功能测试完成',
        'metadata': {
            'test': True,
            'timestamp': '2026-02-17T20:00:00'
        }
    }
    
    print("1. 测试对话格式化...")
    formatted = siyuan.format_conversation(test_conversation)
    if formatted:
        print(f"   ✅ 格式化成功，长度: {len(formatted)} 字符")
        # 显示前200个字符
        preview = formatted[:200] + "..." if len(formatted) > 200 else formatted
        print(f"   预览: {preview}")
    else:
        print("   ❌ 格式化失败")
        return False
    
    print("\n2. 测试对话同步...")
    # 注意：这里实际上不会真的同步，除非你取消下面的注释
    # success = siyuan.sync_conversation(test_conversation)
    # if success:
    #     print("   ✅ 同步成功")
    # else:
    #     print("   ❌ 同步失败")
    #     return False
    
    print("   ⚠️  同步测试已跳过（取消注释代码以实际测试）")
    
    print("\n🎉 同步功能测试完成！")
    return True

def test_config_management():
    """测试配置管理"""
    print("\n🧪 测试配置管理功能...")
    
    # 创建临时配置文件
    import tempfile
    import json
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        temp_config = {
            'siyuan': {
                'api_url': 'http://test.example.com:6811',
                'token': 'test_token_123'
            },
            'sync': {
                'notebook_name': '测试笔记本',
                'document_name': '测试文档',
                'auto_sync': False,
                'sync_interval_minutes': 10
            }
        }
        json.dump(temp_config, f, ensure_ascii=False, indent=2)
        temp_config_path = f.name
    
    try:
        # 使用临时配置文件
        siyuan = SiYuanNote(config_path=temp_config_path)
        
        print(f"1. 从临时配置文件加载...")
        print(f"   API地址: {siyuan.siyuan_config.api_url}")
        print(f"   笔记本: {siyuan.sync_config.notebook_name}")
        print(f"   文档: {siyuan.sync_config.document_name}")
        print(f"   自动同步: {siyuan.sync_config.auto_sync}")
        
        # 测试配置更新
        print("\n2. 测试配置更新...")
        update_success = siyuan.update_config({
            'sync': {
                'notebook_name': '更新后的笔记本',
                'auto_sync': True
            }
        })
        
        if update_success:
            print(f"   ✅ 配置更新成功")
            print(f"   新笔记本名称: {siyuan.sync_config.notebook_name}")
            print(f"   新自动同步设置: {siyuan.sync_config.auto_sync}")
        else:
            print("   ❌ 配置更新失败")
        
    finally:
        # 清理临时文件
        os.unlink(temp_config_path)
        print(f"\n   🧹 已清理临时配置文件")
    
    print("\n🎉 配置管理测试完成！")
    return True

def main():
    """主测试函数"""
    print("=" * 60)
    print("思源笔记技能全面测试")
    print("=" * 60)
    
    tests = [
        ("基本功能测试", test_basic_functionality),
        ("同步功能测试", test_sync_functionality),
        ("配置管理测试", test_config_management)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*40}")
        print(f"运行: {test_name}")
        print(f"{'='*40}")
        
        try:
            success = test_func()
            results.append((test_name, success))
            
            if success:
                print(f"✅ {test_name} 通过")
            else:
                print(f"❌ {test_name} 失败")
                
        except Exception as e:
            print(f"❌ {test_name} 出错: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))
    
    # 汇总结果
    print(f"\n{'='*60}")
    print("测试结果汇总")
    print(f"{'='*60}")
    
    passed = 0
    failed = 0
    
    for test_name, success in results:
        status = "✅ 通过" if success else "❌ 失败"
        print(f"{test_name}: {status}")
        
        if success:
            passed += 1
        else:
            failed += 1
    
    print(f"\n总计: {len(results)} 个测试")
    print(f"通过: {passed}")
    print(f"失败: {failed}")
    
    if failed == 0:
        print("\n🎉 所有测试通过！")
        return True
    else:
        print(f"\n⚠️  有 {failed} 个测试失败")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)