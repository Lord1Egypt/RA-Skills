import chromadb
from scripts.chroma_compat import list_collection_names

client = chromadb.PersistentClient(path='./chroma_db')

# 检查集合是否存在
try:
    collection = client.get_collection('wangqi_knowledge')
    print(f'Collection: {collection.name}')
    print(f'Count: {collection.count()}')
    
    # 检索测试
    results = collection.query(
        query_texts=['痰湿质肥胖'],
        n_results=3
    )
    
    print('\n=== 检索结果 ===')
    for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
        title = meta.get('title', 'N/A')
        source_type = meta.get('source_type', 'N/A')
        print(f'\n[{i}] Title: {title}')
        print(f'    Type: {source_type}')
        print(f'    Content length: {len(doc)} chars')
        print(f'    Preview: {doc[:300]}...')
        
except Exception as e:
    print(f'Error: {e}')
    print('\nAvailable collections:')
    for name in list_collection_names(client.list_collections()):
        print(f'  - {name}')
