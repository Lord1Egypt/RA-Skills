# HeteroMind Usage Guide

## Quick Start

### Basic Usage with Default LLM

```python
import asyncio
from src.engines.nl2sql.multi_stage_engine import MultiStageNL2SQLEngine

# Initialize with default LLM configuration
engine = MultiStageNL2SQLEngine({
    "name": "sql_engine",
    "schema": schema,
    "llm_config": {
        "model": "deepseek-chat",
        "api_key": "sk-your-api-key",
        "base_url": "https://api.deepseek.com/v1",
    },
})

# Execute query
result = await engine.execute("How many employees in Engineering?", {})
print(f"Generated SQL: {result.generated_sql}")
```

### Using Different LLM Providers

#### DeepSeek

```python
engine = MultiStageNL2SQLEngine({
    "name": "sql_engine",
    "schema": schema,
    "llm_config": {
        "model": "deepseek-chat",
        "api_key": "sk-...",
        "base_url": "https://api.deepseek.com/v1",
    },
})
```

#### OpenAI GPT-4

```python
engine = MultiStageNL2SQLEngine({
    "name": "sql_engine",
    "schema": schema,
    "llm_config": {
        "model": "gpt-4",
        "api_key": "sk-...",
    },
})
```

#### Azure OpenAI

```python
engine = MultiStageNL2SQLEngine({
    "name": "sql_engine",
    "schema": schema,
    "llm_config": {
        "model": "gpt-4",
        "api_key": "your-azure-key",
        "base_url": "https://your-resource.openai.azure.com/v1",
    },
})
```

#### Local LLM (Ollama)

```python
engine = MultiStageNL2SQLEngine({
    "name": "sql_engine",
    "schema": schema,
    "llm_config": {
        "model": "llama2",
        "base_url": "http://localhost:11434/v1",
        "api_key": "not-needed",  # Ollama doesn't require API key
    },
})
```

### Per-Call LLM Override

Override model and API key at runtime without reinitializing the engine:

```python
# Initialize with default LLM
engine = MultiStageNL2SQLEngine({
    "name": "sql_engine",
    "schema": schema,
    "llm_config": {
        "model": "deepseek-chat",
        "api_key": "sk-deepseek-key",
    },
})

# Use default LLM
result1 = await engine.execute("Query 1", {})

# Override with GPT-4 for specific query
result2 = await engine.execute(
    query="Query 2",
    context={},
    model="gpt-4-turbo",
    api_key="sk-openai-key",
)

# Override with different model for another query
result3 = await engine.execute(
    query="Query 3",
    context={},
    model="claude-3-sonnet",
    api_key="sk-anthropic-key",
)
```

### Multi-Engine Setup with Different LLMs

```python
from src.engines.nl2sql.multi_stage_engine import MultiStageNL2SQLEngine
from src.engines.nl2sparql.multi_stage_engine import MultiStageNL2SPARQLEngine
from src.engines.table_qa.multi_stage_engine import MultiStageTableQAEngine

# SQL Engine with DeepSeek
sql_engine = MultiStageNL2SQLEngine({
    "name": "sql_engine",
    "schema": sql_schema,
    "llm_config": {
        "model": "deepseek-chat",
        "api_key": "sk-deepseek-key",
    },
})

# SPARQL Engine with GPT-4
sparql_engine = MultiStageNL2SPARQLEngine({
    "name": "sparql_engine",
    "ontology": kg_ontology,
    "llm_config": {
        "model": "gpt-4",
        "api_key": "sk-openai-key",
    },
})

# TableQA Engine with local LLM
table_engine = MultiStageTableQAEngine({
    "name": "table_engine",
    "table_path": "data.csv",
    "llm_config": {
        "model": "llama2",
        "base_url": "http://localhost:11434/v1",
    },
})
```

## Configuration Options

### LLM Configuration Parameters

| Parameter | Required | Description | Example |
|-----------|----------|-------------|---------|
| `model` | Yes | Model name | `"gpt-4"`, `"deepseek-chat"`, `"claude-3"` |
| `api_key` | Yes* | API key for authentication | `"sk-..."` |
| `base_url` | No | Custom API endpoint | `"https://api.deepseek.com/v1"` |
| `temperature` | No | Sampling temperature (0.0-1.0) | `0.1` for deterministic |
| `max_tokens` | No | Max response tokens | `500` |
| `timeout` | No | Request timeout in seconds | `30` |

*Required for cloud providers, optional for local LLMs

### Generation Configuration Parameters

| Parameter | Default | Description |
|-----------|---------|-------------|
| `num_candidates` | 3 | Number of SQL/SPARQL candidates to generate |
| `max_revisions` | 2 | Maximum self-revision rounds |
| `parallel_generation` | True | Enable parallel candidate generation |
| `voting_enabled` | True | Enable multi-candidate voting |

## Best Practices

### 1. Choose the Right Model

- **Simple queries**: Use cost-effective models like `deepseek-chat` or `gpt-3.5-turbo`
- **Complex queries**: Use powerful models like `gpt-4` or `claude-3-opus`
- **Schema linking**: Can use smaller models (high pattern matching)
- **Query generation**: Use larger models for better accuracy

### 2. API Key Management

```python
import os

# Load from environment variable
engine = MultiStageNL2SQLEngine({
    "name": "sql_engine",
    "schema": schema,
    "llm_config": {
        "model": "gpt-4",
        "api_key": os.getenv("OPENAI_API_KEY"),
    },
})
```

### 3. Cost Optimization

```python
# Use cheaper model for most queries
default_engine = MultiStageNL2SQLEngine({
    "llm_config": {"model": "deepseek-chat", "api_key": "..."},
})

# Override with expensive model only for complex queries
result = await default_engine.execute(
    complex_query,
    {},
    model="gpt-4",
    api_key="...",
)
```

### 4. Error Handling

```python
try:
    result = await engine.execute(query, {}, model="gpt-4", api_key="...")
    if result.success:
        print(f"Success: {result.generated_sql}")
    else:
        print(f"Error: {result.error}")
except Exception as e:
    print(f"Exception: {e}")
```

## Troubleshooting

### Invalid API Key

```
Error: 401 Unauthorized
```

**Solution**: Check that `api_key` is correct and has sufficient credits.

### Model Not Found

```
Error: 404 Model not found
```

**Solution**: Verify `model` name is correct for the provider.

### Rate Limiting

```
Error: 429 Too Many Requests
```

**Solution**: 
- Reduce `num_candidates`
- Add retry logic with backoff
- Use `timeout` parameter

### Local LLM Connection Failed

```
Error: Connection refused
```

**Solution**: 
- Ensure Ollama/local LLM server is running
- Check `base_url` is correct
- Verify port is not blocked by firewall

## Examples

### Example 1: Multi-Provider Fallback

```python
async def execute_with_fallback(query, schema):
    providers = [
        {"model": "gpt-4", "api_key": os.getenv("OPENAI_API_KEY")},
        {"model": "deepseek-chat", "api_key": os.getenv("DEEPSEEK_API_KEY")},
        {"model": "llama2", "base_url": "http://localhost:11434/v1"},
    ]
    
    engine = MultiStageNL2SQLEngine({
        "name": "sql_engine",
        "schema": schema,
    })
    
    for provider in providers:
        try:
            result = await engine.execute(query, {}, **provider)
            if result.success:
                return result
        except Exception as e:
            print(f"Provider {provider['model']} failed: {e}")
    
    raise Exception("All providers failed")
```

### Example 2: Batch Processing with Different Models

```python
async def process_queries(queries, schema):
    engine = MultiStageNL2SQLEngine({
        "name": "sql_engine",
        "schema": schema,
        "llm_config": {"model": "deepseek-chat", "api_key": "..."},
    })
    
    results = []
    for query in queries:
        # Use GPT-4 for complex queries
        if len(query.split()) > 15:
            result = await engine.execute(
                query, {},
                model="gpt-4",
                api_key="...",
            )
        else:
            result = await engine.execute(query, {})
        
        results.append(result)
    
    return results
```

---

For more information, see [README.md](README.md).
