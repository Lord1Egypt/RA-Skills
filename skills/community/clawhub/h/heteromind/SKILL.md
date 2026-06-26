---
name: heteromind
description: Unified heterogeneous knowledge QA system. Automatically routes natural language queries to SQL databases, Knowledge Graphs, or table files using 4-layer detection (rule-based, LLM semantic, schema matching, entity verification). Supports multi-LLM providers and bilingual queries. Trigger on data queries, "how many", "show", aggregations, filters, joins, or structured information requests.
required_env_vars:
  - DEEPSEEK_API_KEY
  - OPENAI_API_KEY
optional_env_vars:
  - MYSQL_CONNECTION_STRING
  - POSTGRES_CONNECTION_STRING
  - CUSTOM_KG_ENDPOINT
  - WORKSPACE
  - TABLE_PATHS
---

# HeteroMind

Unified heterogeneous knowledge QA system with automatic source detection and multi-stage reasoning.

## Core Concept

Natural language queries are automatically routed to the appropriate knowledge source (SQL, Knowledge Graph, or Table files) without requiring users to specify the data source. A 4-layer detection architecture ensures accurate source identification, followed by multi-stage query generation with self-revision and voting.

```
User Query → Source Detection (4 layers) → Query Generation → Self-Revision → Voting → Execution → Answer
```

## When to Use

| Trigger | Action |
|---------|--------|
| "How many employees in X?" | NL2SQL engine |
| "Who is the founder of X?" | NL2SPARQL engine (KG) |
| "Which quarter had highest sales?" | TableQA engine |
| "Show average salary by department" | Auto-detect SQL |
| Queries with aggregations, filters, joins | Route to SQL |
| Entity relationship queries | Route to KG |
| Questions about CSV/Excel files | Route to TableQA |
| Multi-hop queries across sources | Decompose + fuse |

## Architecture

### 4-Layer Source Detection

```yaml
Layer 1 (15%): Rule-Based
  - 20+ keywords per source type
  - 7 regex patterns (aggregation, comparison, relation)
  - Fast pre-filtering

Layer 2 (35%): LLM Semantic
  - Intent classification
  - Entity/predicate detection
  - Multi-hop identification

Layer 3a (25%): SQL Schema Match
  - Inverted index on tables/columns
  - Automatic JOIN inference
  - Confidence scoring

Layer 3b (25%): KG Entity Link
  - Entity mention extraction
  - SPARQL endpoint lookup
  - Predicate pattern matching

Layer 3c (25%+30%): Entity Verification
  - Cross-source entity existence check
  - 30% score boost for verified entities

Layer 4: Multi-Source Fusion
  - Weighted aggregation
  - Execution plan generation
```

### Query Generation Pipeline

```
1. Schema/Entity Linking     → Identify relevant tables/columns/entities
2. Parallel Generation       → Generate 3 candidates concurrently
3. Multi-Round Revision      → 2 rounds of self-review
4. Validation               → Syntax and semantic checks
5. Voting                   → Select best candidate
6. Execution                → Run query
7. Result Verification      → Validate reasonableness
```

## Engines

### NL2SQL Engine

```python
from src.engines.nl2sql.multi_stage_engine import MultiStageNL2SQLEngine

engine = MultiStageNL2SQLEngine({
    "name": "sql_engine",
    "schema": schema,
    "llm_config": {
        "model": "deepseek-chat",
        "api_key": "sk-...",
    },
    "generation_config": {
        "num_candidates": 3,
        "max_revisions": 2,
        "parallel_generation": True,
    },
})

result = await engine.execute("How many employees in Engineering?", {})
```

**Features:**
- Schema linking (rule-based + LLM)
- Parallel SQL candidate generation
- Multi-round self-revision
- Voting mechanism
- Result verification

### NL2SPARQL Engine

```python
from src.engines.nl2sparql.multi_stage_engine import MultiStageNL2SPARQLEngine

engine = MultiStageNL2SPARQLEngine({
    "name": "sparql_engine",
    "endpoint_url": "https://dbpedia.org/sparql",
    "ontology": ontology,
    "llm_config": {"model": "gpt-4", "api_key": "sk-..."},
})

result = await engine.execute("Who founded Microsoft?", {})
```

**Features:**
- Entity linking to KG
- Ontology retrieval
- SPARQL generation with revision
- Multi-endpoint support

### TableQA Engine

```python
from src.engines.table_qa.multi_stage_engine import MultiStageTableQAEngine

engine = MultiStageTableQAEngine({
    "name": "table_engine",
    "table_path": "data/sales.csv",
    "llm_config": {"model": "deepseek-chat", "api_key": "sk-..."},
})

result = await engine.execute("Which quarter had highest sales?", {})
```

**Features:**
- Table schema analysis
- Query intent interpretation
- Pandas code generation
- Safe execution sandbox

## Multi-LLM Support

Override model and API key at runtime:

```python
# Initialize with default
engine = MultiStageNL2SQLEngine({
    "llm_config": {"model": "deepseek-chat", "api_key": "sk-deepseek-key"},
})

# Override per-call
result = await engine.execute(
    query="Complex query",
    context={},
    model="gpt-4-turbo",      # Override model
    api_key="sk-openai-key",  # Override API key
)
```

### Supported Providers

| Provider | Models | Configuration |
|----------|--------|---------------|
| DeepSeek | deepseek-chat | `base_url: https://api.deepseek.com/v1` |
| OpenAI | gpt-4, gpt-3.5-turbo | Default endpoint |
| Azure OpenAI | gpt-4 | `base_url: https://{resource}.openai.azure.com` |
| Local (Ollama) | llama2, mistral | `base_url: http://localhost:11434/v1` |

## Configuration

### LLM Configuration

```yaml
llm_config:
  model: deepseek-chat
  api_key: sk-...
  base_url: https://api.deepseek.com/v1  # Optional
  temperature: 0.1
  max_tokens: 500
  timeout: 30
```

### Generation Configuration

```yaml
generation_config:
  num_candidates: 3           # SQL/SPARQL candidates to generate
  max_revisions: 2            # Self-revision rounds
  parallel_generation: true   # Concurrent candidate generation
  voting_enabled: true        # Multi-candidate voting
```

### Source Detection Weights

```yaml
weights:
  rule_based: 0.15      # Layer 1
  llm_based: 0.35       # Layer 2
  schema_based: 0.25    # Layer 3a/3b
  verification: 0.25    # Layer 3c
verification_boost: 0.3  # 30% boost for verified entities
```

## Workflows

### Complete Query Flow

```python
from src.orchestrator import HeteroMindOrchestrator

orchestrator = HeteroMindOrchestrator({
    "source_detection": {
        "layer2": {"api_key": "sk-...", "model": "gpt-4"},
        "layer3": {"schemas": [schema], "kg_endpoints": [...]},
    },
    "engines": {
        "sql": [{"name": "default", "enabled": True}],
        "sparql": [{"name": "default", "enabled": True}],
        "table_qa": [{"name": "default", "enabled": True}],
    },
})

response = await orchestrator.query("How many employees in Engineering?")
print(f"Answer: {response.answer}")
print(f"Source: {response.sources}")
print(f"Confidence: {response.confidence:.2f}")
```

### Source Detection Only

```python
from src.classifier import SourceDetectorOrchestrator

detector = SourceDetectorOrchestrator({
    "layer2": {"api_key": "sk-...", "model": "gpt-4"},
    "layer3": {"schemas": [schema]},
})

decision = await detector.detect("How many employees?")
print(f"Primary Source: {decision.primary_source.value}")
print(f"Confidence: {decision.confidence:.2f}")
print(f"Execution Plan: {decision.execution_plan}")
```

## Test Results

| Engine | Tests | Passed | Accuracy | Avg Confidence | Avg Time |
|--------|-------|--------|----------|----------------|----------|
| SQL (NL2SQL) | 3 | 3 | 100.0% | 0.60 | 22.5s |
| SPARQL (NL2SPARQL) | 2 | 2 | 100.0% | 0.20 | 36.3s |
| TableQA | 3 | 3 | 100.0% | 0.62 | 24.2s |
| **Overall** | 8 | 8 | 100.0% | 0.51 | 26.6s |

## Environment Variables

### Required (for LLM-based generation)

| Variable | Description | Example |
|----------|-------------|---------|
| `DEEPSEEK_API_KEY` | DeepSeek API key | `sk-...` |
| `OPENAI_API_KEY` | OpenAI API key | `sk-...` |

### Optional (for specific features)

| Variable | Description | Example |
|----------|-------------|---------|
| `MYSQL_CONNECTION_STRING` | MySQL database connection | `mysql://user:pass@host/db` |
| `CUSTOM_KG_ENDPOINT` | Custom KG SPARQL endpoint | `https://example.com/sparql` |
| `WORKSPACE` | Base path for table file scanning | `/path/to/workspace` |

### Setup

```bash
# Copy example env file
cp .env.example .env

# Edit with your credentials
nano .env

# Load environment
export $(cat .env | xargs)
```

## Installation

```bash
cd HeteroMind
pip install -r requirements.txt
```

### Requirements

- Python 3.10+
- `aiohttp`, `pandas`, `openpyxl`
- OpenAI-compatible API key (optional)

## Project Structure

```
HeteroMind/
├── src/
│   ├── classifier/          # 4-layer source detection
│   │   ├── rule_detector.py      # Layer 1
│   │   ├── llm_detector.py       # Layer 2
│   │   ├── sql_schema_matcher.py # Layer 3a
│   │   ├── kg_entity_linker.py   # Layer 3b
│   │   ├── entity_verifier.py    # Layer 3c
│   │   └── source_fusion.py      # Layer 4
│   ├── engines/             # Query engines
│   │   ├── nl2sql/
│   │   ├── nl2sparql/
│   │   └── table_qa/
│   ├── decomposer/          # Task decomposition
│   ├── fusion/              # Result fusion
│   ├── generator/           # Answer generation
│   └── orchestrator.py      # Main orchestrator
├── config/
│   └── source_detection.yaml
├── tests/
│   └── test_data/
├── comprehensive_tests.py
└── SKILL.md
```

## Examples

### SQL: Aggregation with Filter

**Query:** "How many employees are in the Engineering department?"

**Generated SQL:**
```sql
SELECT COUNT(*) FROM employees e 
JOIN departments d ON e.department_id = d.id 
WHERE d.name = 'Engineering'
```

### SPARQL: Entity Relationship

**Query:** "Who is the founder of Microsoft?"

**Generated SPARQL:**
```sparql
SELECT ?founder WHERE {
    <http://dbpedia.org/resource/Microsoft> 
    <http://dbpedia.org/ontology/founder> ?founder
}
```

### TableQA: Aggregation

**Query:** "Which quarter had the highest sales in 2024?"

**Generated Code:**
```python
result = df.groupby('quarter')['sales'].sum().idxmax()
```

## Skill Contract

Skills that use HeteroMind should declare:

```yaml
heteromind:
  reads: [Database Schema, KG Ontology, Table Files]
  writes: [Generated SQL, SPARQL, Pandas Code]
  requires:
    - LLM API key (for generation stages)
    - Schema metadata (for source detection)
  postconditions:
    - Generated query passes validation
    - Result verified for reasonableness
```

## Integration Patterns

### With Agent Memory

Log query execution for audit:

```python
from src.orchestrator import HeteroMindOrchestrator

orchestrator = HeteroMindOrchestrator(config)
response = await orchestrator.query(query)

# Log to agent memory
memory.record({
    "action": "knowledge_query",
    "query": query,
    "source": response.sources,
    "confidence": response.confidence,
    "answer": response.answer,
})
```

### Multi-Source Fusion

For queries requiring multiple sources:

```python
# Query automatically detects hybrid need
response = await orchestrator.query(
    "Show employees who published papers"
)
# Routes to: SQL (employees) + KG (papers) + Fusion
```


## References

- `README.md` — Full documentation and API reference
- `USAGE.md` — Detailed usage guide with multi-LLM examples
- `config/source_detection.yaml` — Detection configuration
- `tests/test_data/` — Example schemas and test data

---

*Version: 0.1.0*  
*Last Updated: 2026-04-12*  
*Test Coverage: 100.0% accuracy on 8 test cases*
