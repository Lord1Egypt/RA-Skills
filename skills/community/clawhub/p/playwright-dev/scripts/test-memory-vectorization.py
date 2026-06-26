# 测试 MEMORY.md 向量化流程
# 用法：python test-memory-vectorization.py

import os
import sys
from pathlib import Path

# 添加工作目录
workspace = Path(__file__).parent
sys.path.insert(0, str(workspace))

# 加载环境变量
from dotenv import load_dotenv
load_dotenv(workspace / '.env')

print("=" * 60)
print("MEMORY.md 向量化流程测试")
print("=" * 60)

# 步骤 1：检查环境配置
print("\n[步骤 1] 检查环境配置...")
aliyun_key = os.getenv('ALIYUN_API_KEY')
chroma_dir = os.getenv('CHROMA_PERSIST_DIR', './chroma_db')

if not aliyun_key or aliyun_key == 'sk-xxxxxxxxxxxxxxxx':
    print("[ERROR] ALIYUN_API_KEY 未配置")
    print("   请在 .env 文件中设置正确的阿里云 API Key")
    print("   获取地址：https://dashscope.console.aliyun.com/apiKey")
    sys.exit(1)
else:
    print(f"[OK] ALIYUN_API_KEY: {aliyun_key[:10]}...{aliyun_key[-4:]}")

print(f"[OK] CHROMA_PERSIST_DIR: {chroma_dir}")

# 步骤 2：检查 MEMORY.md 文件
print("\n[步骤 2] 检查 MEMORY.md 文件...")
memory_path = workspace / 'MEMORY.md'
if not memory_path.exists():
    print(f"[ERROR] MEMORY.md 不存在：{memory_path}")
    sys.exit(1)
else:
    content = memory_path.read_text(encoding='utf-8')
    print(f"[OK] MEMORY.md 存在")
    print(f"   文件大小：{len(content)} 字符")
    print(f"   文件路径：{memory_path}")

# 步骤 3：测试阿里云 Embedding API
print("\n[步骤 3] 测试阿里云 Embedding API...")
try:
    import dashscope
    from dashscope import TextEmbedding
    
    # 测试向量化
    test_text = "测试文本向量化"
    response = TextEmbedding.call(
        model=TextEmbedding.models.text_embedding_v2,
        input=test_text,
        api_key=aliyun_key
    )
    
    if response.status_code == 200:
        embedding = response.output['embeddings'][0]['embedding']
        print(f"[OK] Embedding API 调用成功")
        print(f"   模型：text_embedding_v2")
        print(f"   向量维度：{len(embedding)}")
    else:
        print(f"[ERROR] Embedding API 调用失败：{response.code} - {response.message}")
        sys.exit(1)
        
except Exception as e:
    print(f"[ERROR] 导入或调用失败：{e}")
    print("   请安装依赖：pip install dashscope")
    sys.exit(1)

# 步骤 4：检查 Chroma 数据库
print("\n[步骤 4] 检查 Chroma 数据库...")
try:
    import chromadb
    from chromadb.config import Settings
    
    chroma_path = workspace / chroma_dir
    print(f"   Chroma 路径：{chroma_path}")
    
    # 连接数据库
    client = chromadb.PersistentClient(path=str(chroma_path))
    print(f"[OK] Chroma 数据库连接成功")
    
    # 列出所有集合
    collections = client.list_collections()
    print(f"   现有集合数：{len(collections)}")
    for col in collections:
        print(f"   - {col.name}: {col.count()} 条记录")
    
except Exception as e:
    print(f"[ERROR] Chroma 检查失败：{e}")
    print("   请安装依赖：pip install langchain-chroma")
    sys.exit(1)

# 步骤 5：执行向量化
print("\n[步骤 5] 执行 MEMORY.md 向量化...")
try:
    from langchain_text_splitters import RecursiveCharacterTextSplitter
    from langchain_community.embeddings import DashScopeEmbeddings
    from langchain_chroma import Chroma
    
    # 1. 读取并分割文本
    print("   读取 MEMORY.md...")
    text = memory_path.read_text(encoding='utf-8')
    
    print("   分割文本...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
        separators=["\n\n", "\n", "。", "！", "？", " ", ""]
    )
    chunks = splitter.split_text(text)
    print(f"   分割为 {len(chunks)} 个片段")
    
    # 2. 创建 embeddings
    print("   创建 Embedding...")
    embeddings = DashScopeEmbeddings(
        model="text-embedding-v2",
        dashscope_api_key=aliyun_key
    )
    
    # 3. 存储到 Chroma
    print("   存储到 Chroma...")
    collection_name = "openclaw_memory"
    try:
        collection = client.get_collection(collection_name)
        client.delete_collection(collection_name)
        print("   删除旧集合...")
    except:
        pass
    
    vectorstore = Chroma.from_texts(
        texts=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        persist_directory=str(chroma_path),
        metadatas=[{"source": "MEMORY.md", "chunk_id": i} for i in range(len(chunks))]
    )
    
    print(f"[OK] 向量化完成")
    print(f"   集合名称：{collection_name}")
    print(f"   向量数量：{vectorstore._collection.count()}")
    
except Exception as e:
    print(f"[ERROR] 向量化失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 步骤 6：测试搜索
print("\n[步骤 6] 测试向量搜索...")
try:
    # 搜索测试
    query = "记忆"
    print(f"   搜索查询：\"{query}\"")
    
    results = vectorstore.similarity_search(query, k=3)
    
    print(f"[OK] 搜索成功，找到 {len(results)} 条结果")
    for i, doc in enumerate(results, 1):
        print(f"\n   结果 {i}:")
        print(f"   来源：{doc.metadata.get('source', '未知')}")
        print(f"   内容：{doc.page_content[:100]}...")
        
except Exception as e:
    print(f"[ERROR] 搜索测试失败：{e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# 完成
print("\n" + "=" * 60)
print("[SUCCESS] 所有测试通过！MEMORY.md 向量化流程正常")
print("=" * 60)
print("\n总结:")
print("1. [OK] 环境配置正确")
print("2. [OK] MEMORY.md 文件存在")
print("3. [OK] 阿里云 Embedding API 可用")
print("4. [OK] Chroma 数据库连接正常")
print("5. [OK] 向量化流程成功")
print("6. [OK] 向量搜索测试通过")
print("\n下一步:")
print("- 可以正式运行 vectorize_memory.py 脚本")
print("- 或让阿香自动调用向量搜索功能")
