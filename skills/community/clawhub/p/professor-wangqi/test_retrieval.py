import chromadb
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = chromadb.PersistentClient(path='./chroma_db')
collection = client.get_collection('wangqi_knowledge')

# Generate embedding
api_key = os.getenv('EMBEDDING_API_KEY') or os.getenv('API_KEY')
base_url = os.getenv('EMBEDDING_BASE_URL') or os.getenv('BASE_URL')
model = os.getenv('EMBEDDING_MODEL', 'text-embedding-nomic-embed-text-v1.5')
oc = OpenAI(api_key=api_key, base_url=base_url)

query = '痰湿质肥胖'
response = oc.embeddings.create(model=model, input=[query])
query_embedding = response.data[0].embedding

results = collection.query(
    query_embeddings=[query_embedding],
    n_results=3
)

for i, (doc, meta) in enumerate(zip(results['documents'][0], results['metadatas'][0]), 1):
    title = meta.get('title', 'N/A')[:50]
    print(f'[{i}] {title}')
    print(f'    Content length: {len(doc)}')
    print(f'    Preview: {doc[:200]}...')
    print()
