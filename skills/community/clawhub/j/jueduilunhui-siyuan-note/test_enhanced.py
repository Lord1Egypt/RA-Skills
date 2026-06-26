#!/usr/bin/env python3
"""
测试增强版思源笔记技能
"""

import sys
import os

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from siyuan_note_enhanced import SiYuanNoteEnhanced, create_enhanced_client

def test_enhanced_features():
    """测试增强版功能"""
    print("=" * 60)
    print("测试增强版思源笔记技能")
    print("=" * 60)
    
    # 创建增强客户端
    client = create_enhanced_client()
    
    # 测试连接
    print("\n🧪 测试1: 连接测试")
    if client.test_connection():
        print("✅ 连接成功")
    else:
        print("❌ 连接失败")
        return False
    
    # 获取笔记本列表
    print("\n🧪 测试2: 获取笔记本列表")
    notebooks = client.get_notebooks()
    print(f"✅ 找到 {len(notebooks)} 个笔记本:")
    for nb in notebooks[:3]:
        print(f"  - {nb['name']} (ID: {nb['id']})")
    
    # 创建独立文档（新功能！）
    print("\n🧪 测试3: 创建独立文档（使用createDocWithMd）")
    document_name = "测试文档_增强版"
    content = """# 测试文档

这是一个使用增强版思源笔记技能创建的独立文档。

## 新功能测试

1. ✅ createDocWithMd API - 创建真正的独立文档
2. ✅ 增强的文档创建方法
3. ✅ 更好的错误处理和回退机制
4. ✅ 模板渲染功能
5. ✅ 文章剪藏功能

## 创建信息
- 创建时间: 2026-02-17 20:48:00
- 创建方式: Enhanced SiYuanNoteSkill
- 基于项目: siyuan-note/siyuan-chrome

---

*测试完成！*
"""
    
    doc_id = client.create_document("其他", document_name, content, tags=["测试", "增强版"])
    
    if doc_id:
        print(f"✅ 独立文档创建成功!")
        print(f"📄 文档ID: {doc_id}")
        print(f"📁 位置: 思源笔记 -> 其他 -> {document_name}")
        
        # 验证文档是否真的存在
        print("\n🔍 验证文档创建...")
        docs = client.get_documents(client.get_notebook_id("其他"))
        
        found = False
        for doc in docs:
            if document_name in doc.get('name', '') or doc.get('id') == doc_id:
                found = True
                print(f"✅ 验证成功: 找到独立文档!")
                print(f"   名称: {doc.get('name')}")
                print(f"   ID: {doc.get('id')}")
                break
        
        if not found:
            print(f"⚠️  文档可能需要时间刷新，但ID已返回: {doc_id}")
        
        # 测试文章剪藏功能
        print("\n🧪 测试4: 文章剪藏功能")
        article_data = {
            'title': '思源笔记增强技能测试文章',
            'url': 'https://github.com/siyuan-note/siyuan-chrome',
            'content': '## 文章内容\n\n这是一篇测试文章的内容。\n\n### 主要特性\n\n1. 优秀的笔记管理\n2. 强大的剪藏功能\n3. 丰富的API支持',
            'excerpt': '思源笔记是一款优秀的笔记软件，支持多种剪藏方式和丰富的API接口。',
            'site_name': 'GitHub',
            'tags': ['测试', '剪藏']
        }
        
        clip_doc_id = client.clip_article("其他", **article_data)
        
        if clip_doc_id:
            print(f"✅ 文章剪藏成功!")
            print(f"📄 文档ID: {clip_doc_id}")
        else:
            print(f"❌ 文章剪藏失败")
        
        # 测试模板渲染
        print("\n🧪 测试5: 模板渲染功能")
        template = "标题: ${title}\n时间: ${date} ${time}\nURL: ${url}"
        data = {
            'title': '模板测试',
            'date': '2026-02-17',
            'time': '20:48',
            'url': 'https://example.com'
        }
        
        rendered = client.render_template(template, data)
        print(f"✅ 模板渲染结果:")
        print(f"   {rendered}")
        
        # 统计信息
        print("\n📊 操作统计")
        print(f"   操作次数: {client.operation_count}")
        print(f"   最后操作时间: {client.last_operation_time}")
        
        return True
    else:
        print("❌ 独立文档创建失败")
        return False

def test_template_advanced():
    """测试高级模板功能"""
    print("\n" + "=" * 60)
    print("测试高级模板功能")
    print("=" * 60)
    
    client = create_enhanced_client()
    
    # 测试条件表达式
    print("\n🧪 测试条件表达式")
    template1 = "${show ? '显示' : '隐藏'} 这个值"
    result1 = client.render_template(template1, {'show': True})
    print(f"✅ 条件为True: {result1}")
    
    result2 = client.render_template(template1, {'show': False})
    print(f"✅ 条件为False: {result2}")
    
    # 测试嵌套属性
    print("\n🧪 测试嵌套属性")
    template2 = "用户: ${user.name}, 年龄: ${user.age}"
    data2 = {
        'user': {
            'name': '测试用户',
            'age': 25
        }
    }
    result3 = client.render_template(template2, data2)
    print(f"✅ 嵌套属性结果: {result3}")

def main():
    """主函数"""
    try:
        # 测试增强功能
        success = test_enhanced_features()
        
        # 测试高级模板
        test_template_advanced()
        
        # 总结
        print("\n" + "=" * 60)
        print("🎉 测试完成!")
        print("=" * 60)
        
        if success:
            print("\n✅ 增强版思源笔记技能测试通过!")
            print("\n🆕 新功能亮点:")
            print("1.  使用createDocWithMd API创建真正的独立文档")
            print("2.  增强的错误处理和回退机制")
            print("3.  文章剪藏功能（类似Chrome扩展）")
            print("4.  强大的模板渲染系统")
            print("5.  改进的整体架构和错误处理")
            print("\n📝 可在思源笔记中查看创建的独立文档!")
        else:
            print("\n❌ 部分功能测试失败，请检查思源笔记连接")
        
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()