#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""测试 ChromaDB 搜索"""

import sys
import os

# 设置编码
sys.stdout.reconfigure(encoding='utf-8')

print("✅ Python 脚本启动", flush=True)

try:
    from langchain_chroma import Chroma
    print("✅ langchain_chroma 导入成功", flush=True)
    
    chroma_dir = "C:/Users/Xiabi/.openclaw/workspace/chroma_db"
    db = Chroma(persist_directory=chroma_dir, collection_name="user_preferences")
    print(f"✅ ChromaDB 连接成功", flush=True)
    
    count = db._collection.count()
    print(f"📊 向量总数：{count}", flush=True)
    
    if count > 0:
        print("🔍 搜索'创业'...", flush=True)
        results = db.similarity_search("创业", k=5)
        print(f"✅ 找到 {len(results)} 条相关记忆", flush=True)
        
        for i, doc in enumerate(results, 1):
            source = doc.metadata.get("source", "Unknown")
            content = doc.page_content[:150].replace("\n", " ")
            print(f"{i}. [{source}] {content}...", flush=True)
    else:
        print("⚠️ 向量库为空", flush=True)
        
except Exception as e:
    print(f"❌ 错误：{e}", flush=True)
    import traceback
    traceback.print_exc()
