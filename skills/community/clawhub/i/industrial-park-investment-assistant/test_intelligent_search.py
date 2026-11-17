#!/usr/bin/env python3
"""
测试 intelligent_search 和 knowledge_base 模块
"""
import sys
import os

# 添加技能目录到路径
sys.path.insert(0, '/Users/mac/.workbuddy/skills/industrial-park-investment-assistant')

print("🧪 测试招商助手信息获取模块")
print("=" * 80)

# ============================================================
# 测试1: 测试 knowledge_base 模块
# ============================================================
print("\n📊 测试1: knowledge_base 模块")
print("-" * 80)

try:
    from knowledge_base import KnowledgeBase, CONFIG_FILE
    
    print(f"✅ knowledge_base 模块导入成功")
    print(f"📁 配置文件路径: {CONFIG_FILE}")
    print(f"📁 配置文件存在: {os.path.exists(CONFIG_FILE)}")
    
    # 初始化知识库
    print("\n🔄 正在初始化知识库...")
    kb = KnowledgeBase()
    print(f"✅ 知识库初始化成功")
    print(f"   数据源类型: {kb.source_type}")
    
    # 测试读取客户管理表
    print("\n🔄 正在读取客户管理表...")
    result = kb.get_all(sheet_name='客户管理')
    
    if isinstance(result, list):
        print(f"✅ 读取成功（本地文件模式）")
        print(f"   返回类型: list")
        print(f"   数据条数: {len(result)}")
        if len(result) > 0:
            print(f"   第一条数据示例: {result[0]}")
    elif isinstance(result, dict) and '_query_type' in result:
        print(f"✅ 读取成功（MCP模式）")
        print(f"   返回类型: dict (MCP查询参数)")
        print(f"   查询类型: {result['_query_type']}")
        print(f"   参数: {result}")
    else:
        print(f"⚠️  返回格式未知: {type(result)}")
        print(f"   内容: {result}")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# 测试2: 测试 intelligent_search 模块
# ============================================================
print("\n\n📊 测试2: intelligent_search 模块")
print("-" * 80)

try:
    from intelligent_search import intelligent_search
    
    print(f"✅ intelligent_search 模块导入成功")
    
    # 测试2.1: 查询客户（应该使用 knowledge_base）
    print("\n🔄 测试2.1: 查询客户（预期使用 knowledge_base）...")
    result1 = intelligent_search("查询客户 T1-601")
    print(f"✅ 查询完成")
    print(f"   数据源: {result1.get('data_source', 'unknown')}")
    print(f"   是否使用知识库: {result1.get('use_knowledge_base', False)}")
    print(f"   是否使用公开信息: {result1.get('use_public_info', False)}")
    
    # 测试2.2: 搜索企业动态（应该使用 WebSearch）
    print("\n🔄 测试2.2: 搜索企业动态（预期使用 WebSearch）...")
    result2 = intelligent_search("ABC公司最新融资动态")
    print(f"✅ 查询完成")
    print(f"   数据源: {result2.get('data_source', 'unknown')}")
    print(f"   是否使用知识库: {result2.get('use_knowledge_base', False)}")
    print(f"   是否使用公开信息: {result2.get('use_public_info', False)}")
    
    # 测试2.3: 研究企业（应该使用混合模式）
    print("\n🔄 测试2.3: 研究企业（预期使用混合模式）...")
    result3 = intelligent_search("研究一下ABC公司")
    print(f"✅ 查询完成")
    print(f"   数据源: {result3.get('data_source', 'unknown')}")
    print(f"   是否使用知识库: {result3.get('use_knowledge_base', False)}")
    print(f"   是否使用公开信息: {result3.get('use_public_info', False)}")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()

# ============================================================
# 总结
# ============================================================
print("\n\n" + "=" * 80)
print("📊 测试总结")
print("=" * 80)
print("""
✅ 如果所有测试都通过，说明：
  1. knowledge_base 模块工作正常
  2. intelligent_search 模块工作正常
  3. 数据源自动判断逻辑正常

📋 下一步：
  1. 在 WorkBuddy 中调用招商助手
  2. 输入 "@招商助手 查询客户 T1-601"
  3. 观察是否自动使用 knowledge_base 读取数据
  4. 输入 "@招商助手 ABC公司最新动态"
  5. 观察是否自动使用 WebSearch 搜索
""")
