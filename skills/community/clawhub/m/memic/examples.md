# Memic SDK — Copy-Paste Examples

## Upload and Search (5 lines)

```python
from memic import Memic

client = Memic()  # reads MEMIC_API_KEY env var
file = client.upload_file("report.pdf")  # waits until processed
results = client.search(query="quarterly revenue", top_k=5)
for r in results:
    print(f"[{r.score:.2f}] {r.file_name} p{r.page_number}: {r.content[:100]}")
```

## RAG Context for OpenAI / Anthropic / Any LLM

```python
from memic import Memic

memic = Memic()

def get_context(question: str) -> str:
    """Get relevant context from your documents for an LLM prompt."""
    results = memic.search(query=question, top_k=5, min_score=0.6)
    return "\n\n".join([
        f"[{r.file_name}, Page {r.page_number}]\n{r.content}"
        for r in results
    ])

# Use with any LLM
context = get_context("What are the contract renewal terms?")
prompt = f"Answer based on this context:\n\n{context}\n\nQuestion: What are the contract renewal terms?"
```

## Filtered Search (by reference, page range, category)

```python
from memic import Memic, MetadataFilters, PageRange

client = Memic()

# Search within a specific document's first 20 pages
results = client.search(
    query="liability clause",
    filters=MetadataFilters(
        reference_id="contract_2024_v2",
        page_range=PageRange(gte=1, lte=20),
    )
)
```

## Search Specific Files Only

```python
results = client.search(
    query="budget allocation",
    file_ids=["file-id-1", "file-id-2"],
    top_k=3,
)
```

## Hybrid Search (Documents + Database)

```python
client = Memic()

results = client.search(query="Top 10 customers by revenue")

# Memic auto-routes: documents → semantic search, databases → Text2SQL
if results.routing:
    print(f"Route: {results.routing.route}")  # "semantic", "structured", or "hybrid"

# Document chunks
for r in results.results.semantic:
    print(f"[Doc] {r.file_name}: {r.content[:100]}")

# Database rows
if results.has_structured:
    print(f"SQL: {results.routing.sql_generated}")
    for row in results.results.structured.rows:
        print(f"[DB] {row}")
```

## Chat (Built-in RAG + LLM)

```python
client = Memic()

response = client._request(
    "POST", "/sdk/chat",
    json={"question": "Summarize the Q4 results", "top_k": 5}
)
print(response["answer"])
# Also returns: citations, model, question
```

## Check File Processing Status

```python
client = Memic()

file = client.get_file_status("file-id-here")
print(f"Status: {file.status}")           # e.g. "ready", "parsing_started"
print(f"Processing: {file.status.is_processing}")
print(f"Failed: {file.status.is_failed}")
print(f"Chunks: {file.total_chunks}")
```

## Error Handling

```python
from memic import Memic, AuthenticationError, NotFoundError, APIError

client = Memic()

try:
    results = client.search(query="test")
except AuthenticationError:
    print("Bad API key — check MEMIC_API_KEY")
except NotFoundError:
    print("Resource not found")
except APIError as e:
    print(f"API error {e.status_code}: {e.message}")
```
