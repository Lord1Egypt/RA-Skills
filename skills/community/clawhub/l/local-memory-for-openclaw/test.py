#!/usr/bin/env python3
from lib.memory_manager import memory_manager

print("=== 测试本地记忆功能 ===")

# 测试添加记忆
print("\n1. 测试添加记忆：")
mem_id1 = memory_manager.add_memory("我喜欢用TypeScript写代码", "preference")
mem_id2 = memory_manager.add_memory("我的服务器IP是43.142.69.254，SSH端口2222", "fact")
mem_id3 = memory_manager.add_memory("接下来要开发本地记忆技能，预计2天完成", "todo")
print(f"添加成功，记忆ID: {mem_id1}, {mem_id2}, {mem_id3}")

# 测试搜索记忆
print("\n2. 测试搜索记忆：")
results = memory_manager.search_memories("服务器")
for res in results:
    print(f"相似度: {res['similarity']:.2f}, 内容: {res['content']}")

# 测试获取上下文
print("\n3. 测试获取相关上下文：")
context = memory_manager.get_relevant_context("我要连接服务器")
print(context)

# 测试列出所有记忆
print("\n4. 测试列出所有记忆：")
mems = memory_manager.list_all_memories()
for mem in mems:
    print(f"ID: {mem['id']}, 内容: {mem['content']}, 创建时间: {mem['created_at']}")

# 测试删除记忆
print("\n5. 测试删除记忆：")
result = memory_manager.delete_memory(mem_id3)
print(f"删除成功: {result}")

# 测试自动提取记忆
print("\n6. 测试自动提取记忆：")
user_msg = "我平时喜欢用Python写算法相关的代码"
assistant_reply = "好的，我记住了，你喜欢用Python写算法代码。"
extracted = memory_manager.extract_memories_from_conversation(user_msg, assistant_reply)
print(f"提取到的记忆ID: {extracted}")

print("\n=== 所有测试通过！===")
memory_manager.close()
