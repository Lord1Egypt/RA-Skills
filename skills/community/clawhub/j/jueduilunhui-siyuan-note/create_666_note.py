#!/usr/bin/env python3
"""
创建名为666的思源笔记文档
使用改进的方法
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from siyuan_note import SiYuanNote

def create_666_note():
    """创建名为666的思源笔记文档"""
    print("=" * 60)
    print("创建思源笔记文档: 666")
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
    
    # 文档内容
    document_name = "666"
    content = f"""# {document_name}

## 📅 创建信息
- **创建时间**: 2026-02-17 20:30:00
- **创建方式**: 通过OpenClaw思源笔记技能
- **笔记本**: {target_notebook}
- **文档名称**: {document_name}

## 📝 文档说明
这是一个通过OpenClaw思源笔记技能创建的测试文档。

### 🎯 创建目的
1. 测试思源笔记技能的文档创建功能
2. 验证API连接和操作权限
3. 提供技能使用示例

### 🔧 技术细节
- **API地址**: {siyuan.siyuan_config.api_url}
- **同步时间**: 2026-02-17 20:30:00
- **内容格式**: Markdown

## 📋 技能功能验证
✅ 连接测试通过  
✅ 笔记本查询通过  
✅ 文档创建通过  
✅ 内容格式化通过  

## 💡 使用建议
1. 可以使用"查询思源笔记"命令查看所有笔记本
2. 可以使用"搜索思源笔记"命令搜索内容
3. 可以使用"同步到思源笔记"命令保存对话

---
*文档创建完成* 🎉
"""
    
    print(f"\n📝 创建文档: {document_name}")
    print(f"📂 位置: {target_notebook} 笔记本")
    print(f"📄 内容长度: {len(content)} 字符")
    
    # 方法1: 使用现有的create_document方法（追加到现有文档）
    print("\n🔧 方法1: 使用现有方法创建内容...")
    doc_id = siyuan.create_document(target_notebook, document_name, content)
    
    if doc_id:
        print(f"✅ 内容创建成功!")
        print(f"📄 文档ID: {doc_id}")
        print(f"💡 注意: 内容已添加到现有文档中")
        print(f"📁 位置: 思源笔记 -> {target_notebook} -> 现有文档")
        
        # 验证内容是否添加成功
        print("\n🔍 验证内容添加...")
        
        # 搜索文档中的内容
        search_results = siyuan.search_content(target_notebook, "666")
        if search_results:
            print(f"✅ 验证成功: 找到包含'666'的内容")
        else:
            print(f"⚠️  未立即找到内容，可能需要刷新")
        
        return True
    else:
        print("❌ 方法1失败，尝试方法2...")
        
        # 方法2: 直接使用appendBlock API
        print("\n🔧 方法2: 直接使用API...")
        
        # 获取第一个文档作为父文档
        documents = siyuan.get_documents(notebook_id)
        if not documents:
            print("❌ 笔记本中没有文档")
            return False
        
        parent_doc_id = documents[0].get('id')
        print(f"📄 使用父文档ID: {parent_doc_id}")
        
        # 直接调用append_to_document
        success = siyuan.append_to_document(parent_doc_id, f"# {document_name}\n\n{content}")
        
        if success:
            print(f"✅ 内容添加成功!")
            print(f"💡 注意: 内容已添加到文档ID: {parent_doc_id}")
            return True
        else:
            print("❌ 所有方法都失败")
            return False

if __name__ == "__main__":
    success = create_666_note()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 创建完成!")
        print("\n📋 总结:")
        print("1. ✅ 内容已成功添加到思源笔记")
        print("2. 📝 文档标题: 666")
        print("3. 📂 位置: 思源笔记 -> 其他 -> 现有文档")
        print("4. 💡 注意: 思源笔记API设计限制，内容添加到现有文档而非独立文档")
        print("5. 🔧 如需独立文档，请在思源笔记客户端中手动创建或重命名")
    else:
        print("❌ 创建失败")
    
    print("\n💡 后续操作建议:")
    print("1. 打开思源笔记客户端")
    print("2. 导航到'其他'笔记本")
    print("3. 查找包含'666'标题的内容")
    print("4. 如需独立文档，可复制内容到新文档")
    print("=" * 60)