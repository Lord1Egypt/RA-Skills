# Vector Operations — Detailed Reference

Target collection must exist and be loaded.

> **Never use fake or placeholder vectors** (e.g., `[0.1, 0.2, ...]`). Always generate vectors from an embedding model. Use `pip install "pymilvus[model]"` for built-in embedding support, or use any external embedding model (OpenAI, Cohere, HuggingFace, etc.).

## Embedding Model Setup

```python
# Option 1: Built-in pymilvus embedding (pip install "pymilvus[model]")
from pymilvus import model
embedding_fn = model.dense.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Encode documents for insertion
doc_vectors = embedding_fn.encode_documents(["AI advances in 2024", "ML basics for beginners"])
# Encode queries for search (use the SAME model that encoded the stored documents)
query_vectors = embedding_fn.encode_queries(["What is artificial intelligence?"])

# Option 2: OpenAI embeddings (pip install openai)
from openai import OpenAI
openai_client = OpenAI()
response = openai_client.embeddings.create(input=["some text"], model="text-embedding-3-small")
vectors = [item.embedding for item in response.data]
```

## Insert

```python
docs = ["AI advances in 2024", "ML basics for beginners"]
vectors = embedding_fn.encode_documents(docs)

data = [
    {"id": 1, "text": docs[0], "embedding": vectors[0]},
    {"id": 2, "text": docs[1], "embedding": vectors[1]},
]
res = client.insert(collection_name="my_collection", data=data)
# Returns: {"insert_count": 2, "ids": [1, 2]}
```

## Upsert (insert or update if PK exists)

```python
res = client.upsert(collection_name="my_collection", data=data)
# Returns: {"upsert_count": 2}
```

## Search (vector similarity)

```python
query_vectors = embedding_fn.encode_queries(["What is artificial intelligence?"])

results = client.search(
    collection_name="my_collection",
    data=query_vectors,                 # Vectors from embedding model
    anns_field="embedding",             # Vector field name
    limit=10,                           # Top-K
    output_fields=["text", "id"],       # Fields to return
    filter='age > 20 and status == "active"',  # Optional scalar filter
    search_params={
        "metric_type": "COSINE",
        "params": {"nprobe": 10}        # Index-specific params
    }
)
# Returns: List[List[dict]]
# Each hit: {"id": 1, "distance": 0.95, "entity": {"text": "AI advances..."}}
```

## Hybrid Search (multi-vector with reranking)

```python
from pymilvus import AnnSearchRequest, RRFRanker, WeightedRanker

# dense_query_vector and sparse_query_vector come from your embedding models
req1 = AnnSearchRequest(
    data=[dense_query_vector],
    anns_field="dense_embedding",
    param={"metric_type": "COSINE", "params": {"nprobe": 10}},
    limit=10
)
req2 = AnnSearchRequest(
    data=[{1: 0.5, 100: 0.3}],          # Sparse vector
    anns_field="sparse_embedding",
    param={"metric_type": "IP"},
    limit=10
)

# RRF reranking
results = client.hybrid_search(
    collection_name="my_collection",
    reqs=[req1, req2],
    ranker=RRFRanker(k=60),
    limit=10,
    output_fields=["text"]
)

# Or weighted reranking
results = client.hybrid_search(
    collection_name="my_collection",
    reqs=[req1, req2],
    ranker=WeightedRanker(0.7, 0.3),
    limit=10
)
```

## Full-Text Search

Full-text search uses Milvus's built-in BM25 tokenizer to convert text into sparse vectors automatically.

### Setup: Collection with Full-Text Search

```python
from pymilvus import MilvusClient, DataType, Function, FunctionType

client = MilvusClient(uri="<USER_URI>", token="<USER_TOKEN>")

schema = client.create_schema()
schema.add_field("id", DataType.INT64, is_primary=True, auto_id=True)
schema.add_field("text", DataType.VARCHAR, max_length=1000, enable_analyzer=True)
schema.add_field("sparse", DataType.SPARSE_FLOAT_VECTOR)

# Define BM25 function to auto-convert text -> sparse vector
bm25_function = Function(
    name="text_bm25",
    input_field_names=["text"],
    output_field_names=["sparse"],
    function_type=FunctionType.BM25,
)
schema.add_function(bm25_function)

index_params = client.prepare_index_params()
index_params.add_index(field_name="sparse", index_type="AUTOINDEX", metric_type="BM25")

client.create_collection(collection_name="full_text_col", schema=schema, index_params=index_params)
```

### Search with Text

```python
results = client.search(
    collection_name="full_text_col",
    data=["machine learning algorithms"],   # Raw text query
    anns_field="sparse",
    limit=10,
    output_fields=["text"]
)
```

## Search Iterator (paginated search over large results)

```python
query_vectors = embedding_fn.encode_queries(["search query text"])

iterator = client.search_iterator(
    collection_name="my_collection",
    data=query_vectors,
    anns_field="embedding",
    batch_size=100,
    limit=10000,
    output_fields=["text"],
    search_params={"metric_type": "COSINE", "params": {"nprobe": 10}}
)

results = []
while True:
    batch = iterator.next()
    if not batch:
        break
    results.extend(batch)

iterator.close()
```

## Query Iterator (paginated filter-based retrieval)

```python
iterator = client.query_iterator(
    collection_name="my_collection",
    filter='age > 20',
    output_fields=["text", "age"],
    batch_size=100,
    limit=10000
)

results = []
while True:
    batch = iterator.next()
    if not batch:
        break
    results.extend(batch)

iterator.close()
```

## Query (filter-based retrieval)

```python
results = client.query(
    collection_name="my_collection",
    filter='id in [1, 2, 3]',
    output_fields=["text", "embedding"],
    limit=100
)
```

## Get (by primary key)

```python
results = client.get(
    collection_name="my_collection",
    ids=[1, 2, 3],
    output_fields=["text"]
)
```

## Delete

```python
# By primary keys
client.delete(collection_name="my_collection", ids=[1, 2, 3])

# By filter expression
client.delete(collection_name="my_collection", filter='status == "obsolete"')
```

## Filter Expression Syntax

| Expression | Example |
|---|---|
| Comparison | `age > 20` |
| Equality | `status == "active"` |
| IN list | `id in [1, 2, 3]` |
| AND/OR | `age > 20 and status == "active"` |
| String match | `text like "hello%"` |
| Array contains | `ARRAY_CONTAINS(tags, "ml")` |
| JSON field | `json_field["key"] > 100` |
| Match all | `id > 0` |

## Guidance

- **Never use fake or placeholder vectors.** Always generate vectors from an embedding model.
- The query embedding model must be the **same model** used to generate the stored vectors.
- The `data` parameter in search must match the collection's vector dimension exactly.
- For full-text search, pass raw text strings as `data` — Milvus handles tokenization via BM25.
- For large inserts, batch data into chunks (e.g., 1000 rows per batch).
- Always specify `output_fields` to control which fields are returned.
- For large result sets, use `search_iterator` or `query_iterator` instead of increasing `limit`.
- Always call `iterator.close()` when done to release server resources.
