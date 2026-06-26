---
name: milvus
description: Operate Milvus vector database with pymilvus Python SDK. Use when the user wants to connect to Milvus, create collections, insert vectors, perform similarity search, hybrid search, full-text search, manage indexes, partitions, databases, or RBAC via Python code.
license: Apache-2.0
compatibility: Requires Python 3.8+ and pymilvus (pip install pymilvus). Runs on macOS and Linux.
metadata:
  author: zilliztech
  version: "1.0.0"
allowed-tools: Bash Read Write
---

# Milvus Vector Database Skill

Operate [Milvus](https://milvus.io/) vector databases directly through Python code using the `pymilvus` SDK. Covers the full lifecycle — connecting, schema design, collection management, vector CRUD, search, hybrid search, full-text search, indexing, partitions, databases, and RBAC.

## When to Use

Use this skill when the user wants to:
- Connect to a Milvus instance (local, standalone, cluster, or Milvus Lite)
- Create collections with custom schemas
- Insert, upsert, search, query, get, or delete vectors
- Perform hybrid search with reranking
- Perform full-text search (BM25)
- Manage indexes, partitions, databases
- Set up users, roles, and access control (RBAC)
- Build RAG pipelines, semantic search, or recommendation systems with Milvus
- Iterate over large result sets with search/query iterators

## Requirements

- Python 3.8+
- `pymilvus` (`pip install pymilvus`)
- A running Milvus instance, or use Milvus Lite (embedded, file-based) for development

## Capabilities Overview

| Area | What You Can Do |
|------|----------------|
| **Connection** | Connect to Milvus Lite, Standalone, Cluster, or Zilliz Cloud |
| **Collections** | Create (quick or custom schema), list, describe, drop, rename, truncate, load, release |
| **Vectors** | Insert, upsert, search, hybrid search, query, get, delete |
| **Full-Text Search** | BM25-based keyword search with sparse vectors |
| **Iterators** | Paginated search and query over large datasets |
| **Indexes** | Create (AUTOINDEX, HNSW, IVF_FLAT, etc.), list, describe, drop |
| **Partitions** | Create, list, load, release, drop |
| **Databases** | Create, list, switch, drop |
| **RBAC** | Users, roles, privileges management |

---

## Connection

> **IMPORTANT: Before writing any connection code, you MUST ask the user for their connection details.** Ask:
> 1. **Deployment type** — Milvus Lite (local file), Standalone/Cluster (self-hosted), or Zilliz Cloud (managed)?
> 2. **URI** — For self-hosted: host and port (e.g., `http://localhost:19530`). For Zilliz Cloud: the endpoint URL.
> 3. **Authentication** — Token, API key, or username/password if required.
> 4. **Database name** — If not using the default database.
>
> **Never assume or hardcode connection parameters.** Use Milvus Lite (`uri="./milvus.db"`) only if the user explicitly wants local/embedded mode for development.

```python
from pymilvus import MilvusClient

# Milvus Lite (embedded, file-based — great for dev/test)
client = MilvusClient(uri="./milvus.db")

# Standalone / Cluster Milvus (ask user for actual host:port and credentials)
client = MilvusClient(uri="<USER_URI>", token="<USER_TOKEN>")

# Zilliz Cloud (ask user for endpoint and API key)
client = MilvusClient(uri="<USER_ZILLIZ_ENDPOINT>", token="<USER_API_KEY>")
```

**Parameters:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `uri` | str | `"./file.db"` for Milvus Lite, `"http://host:19530"` for server |
| `token` | str | API key or `"username:password"` |
| `user` | str | Username (alternative to token) |
| `password` | str | Password (alternative to token) |
| `db_name` | str | Target database (default: `"default"`) |
| `timeout` | float | Operation timeout in seconds |

### Async Client

```python
from pymilvus import AsyncMilvusClient

async with AsyncMilvusClient(uri="<USER_URI>") as client:
    results = await client.search(collection_name="my_collection", data=[query_vector], limit=10)
```

---

## Collection Management

### Quick Create (auto schema + auto index + auto load)

```python
client.create_collection(
    collection_name="my_collection",
    dimension=768,
    metric_type="COSINE"  # Optional: "COSINE" (default), "L2", "IP"
)
```

This automatically creates an `id` field (INT64, primary key, auto_id), a `vector` field (FLOAT_VECTOR), AUTOINDEX, and auto-loads the collection.

### Custom Schema Create

```python
from pymilvus import DataType

schema = client.create_schema(auto_id=False, enable_dynamic_field=True)
schema.add_field("id", DataType.INT64, is_primary=True)
schema.add_field("text", DataType.VARCHAR, max_length=512)
schema.add_field("embedding", DataType.FLOAT_VECTOR, dim=768)

index_params = client.prepare_index_params()
index_params.add_index(field_name="embedding", index_type="AUTOINDEX", metric_type="COSINE")

client.create_collection(collection_name="my_collection", schema=schema, index_params=index_params)
```

**See [references/collection.md](references/collection.md) for data types, add_field parameters, and all collection operations.**

### Other Collection Operations

```python
client.list_collections()
client.describe_collection(collection_name="my_collection")
client.has_collection(collection_name="my_collection")
client.rename_collection(old_name="old", new_name="new")
client.drop_collection(collection_name="my_collection")
client.truncate_collection(collection_name="my_collection")
client.load_collection(collection_name="my_collection")
client.release_collection(collection_name="my_collection")
client.get_load_state(collection_name="my_collection")
client.get_collection_stats(collection_name="my_collection")
```

- Quick create is best for prototyping; use custom schema for production.
- A collection must be **loaded** before search or query.
- Use `enable_dynamic_field=True` to allow inserting fields not defined in the schema.

---

## Vector Operations

**See [references/vector.md](references/vector.md) for hybrid search, full-text search, iterators, filter syntax, and detailed examples.**

### Insert / Upsert

```python
# Vectors must come from an embedding model — never use fake/placeholder vectors
from pymilvus import model

embedding_fn = model.dense.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

docs = ["AI advances in 2024", "ML basics for beginners"]
vectors = embedding_fn.encode_documents(docs)

data = [
    {"id": 1, "text": docs[0], "embedding": vectors[0]},
    {"id": 2, "text": docs[1], "embedding": vectors[1]},
]
client.insert(collection_name="my_collection", data=data)
client.upsert(collection_name="my_collection", data=data)
```

### Search (vector similarity)

```python
# Use the same embedding model to encode the query
query_vectors = embedding_fn.encode_queries(["What is artificial intelligence?"])

results = client.search(
    collection_name="my_collection",
    data=query_vectors,
    anns_field="embedding",
    limit=10,
    output_fields=["text", "id"],
    filter='age > 20 and status == "active"',
    search_params={"metric_type": "COSINE", "params": {"nprobe": 10}}
)
```

### Query / Get / Delete

```python
# Query by filter
client.query(collection_name="my_collection", filter='id in [1, 2, 3]', output_fields=["text"], limit=100)

# Get by primary key
client.get(collection_name="my_collection", ids=[1, 2, 3], output_fields=["text"])

# Delete
client.delete(collection_name="my_collection", ids=[1, 2, 3])
client.delete(collection_name="my_collection", filter='status == "obsolete"')
```

- **Never use fake or placeholder vectors** (e.g., `[0.1, 0.2, ...]`). Always generate vectors from an embedding model.
- Use `pip install "pymilvus[model]"` for built-in embedding functions, or use any embedding model (OpenAI, Cohere, etc.).
- Vector dimension in search must match the collection schema exactly.
- The query embedding model must be the **same model** used to generate the stored vectors.
- For large inserts, batch data into chunks (e.g., 1000 rows per batch).
- For large result sets, use iterators — see [references/vector.md](references/vector.md).

---

## Index Management

**See [references/index.md](references/index.md) for index types, metric types, and parameters.**

```python
index_params = client.prepare_index_params()
index_params.add_index(
    field_name="embedding",
    index_type="HNSW",
    metric_type="COSINE",
    params={"M": 16, "efConstruction": 256}
)
client.create_index(collection_name="my_collection", index_params=index_params)

client.list_indexes(collection_name="my_collection")
client.describe_index(collection_name="my_collection", index_name="my_index")
client.drop_index(collection_name="my_collection", index_name="my_index")
```

- `AUTOINDEX` is recommended for most use cases.
- An index is required before loading a collection.

---

## Additional Features

| Feature | Reference |
|---------|-----------|
| Partition Management | [references/partition.md](references/partition.md) |
| Database Management | [references/database.md](references/database.md) |
| User & Role Management (RBAC) | [references/user-role.md](references/user-role.md) |
| Common Patterns (RAG, Semantic Search) | [references/patterns.md](references/patterns.md) |

---

## General Guidance

- **Always ask the user for connection details** (URI, token/credentials) before writing connection code. Never assume or hardcode connection parameters.
- **Never generate fake or placeholder vectors.** Always use an embedding model to produce real vectors. Suggest `pip install "pymilvus[model]"` for built-in embedding functions.
- For quick prototyping, use **Milvus Lite** (`uri="./file.db"`) — no server needed, but only if the user explicitly requests local/embedded mode.
- A collection must be **loaded into memory** before search/query.
- The vector dimension in search data must **exactly match** the collection schema.
- The query embedding model must be the **same model** used to generate the stored vectors.
- Before any destructive operation (drop collection, drop database, delete vectors), always confirm with the user.
- Use `enable_dynamic_field=True` when the schema may evolve.
- Prefer `AUTOINDEX` unless the user has specific performance requirements.
- Use `truncate_collection` to clear all data without dropping the collection.
- For large datasets, use iterators (`search_iterator`, `query_iterator`) instead of increasing limit.
