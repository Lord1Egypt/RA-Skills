# HeteroMind

**Unified Heterogeneous Knowledge QA System**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![ClawHub](https://img.shields.io/badge/ClawHub-skill-green.svg)](https://clawhub.ai/)

HeteroMind is a multi-source knowledge QA system that automatically routes natural language queries to appropriate knowledge sources (SQL databases, Knowledge Graphs, Table files) without requiring users to specify the data source.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| **Auto Source Detection** | 4-layer detection architecture automatically identifies SQL, SPARQL, or Table QA |
| **Multi-language Support** | Supports both Chinese and English queries |
| **Multi-stage Reasoning** | Schema Linking → Query Generation → Self-Revision → Voting → Execution |
| **Parallel Execution** | Concurrent candidate generation for improved efficiency |
| **Self-Revision** | Multi-round review and improvement of generated queries |
| **Voting Mechanism** | Multi-candidate voting to select the best result |

---

## 🏗️ Architecture

### 4-Layer Source Detection

```
User Query
    ↓
┌─────────────────────────────────────────┐
│ Layer 1: Rule-Based (15%)                │ ← Keywords, patterns
├─────────────────────────────────────────┤
│ Layer 2: LLM Semantic (35%)              │ ← Intent understanding
├─────────────────────────────────────────┤
│ Layer 3a: SQL Schema Match (25%)         │ ← Database schema matching
├─────────────────────────────────────────┤
│ Layer 3b: KG Entity Link (25%)           │ ← Entity linking to KG
├─────────────────────────────────────────┤
│ Layer 3c: Entity Verification (25%+30%)  │ ← Verify entities exist
└─────────────────────────────────────────┘
    ↓
Layer 4: Multi-Source Fusion → Final Decision + Execution Plan
```

### Query Execution Pipeline

```
Source Selected
    ↓
1. Schema/Entity Linking
2. Parallel Candidate Generation (3 candidates)
3. Multi-Round Self-Revision (2 rounds)
4. Validation (syntax & semantic)
5. Voting (select best candidate)
6. Execution (run query)
7. Result Verification
    ↓
Natural Language Answer
```

---

## 📦 Installation

```bash
# Clone or download the skill
cd HeteroMind

# Install dependencies
pip install -r requirements.txt
```

### Requirements

- Python 3.10+
- `aiohttp` - Async HTTP client
- `pandas` - Data manipulation
- `openpyxl` - Excel support
- `openai` - LLM API client (optional, for LLM-based detection)

---

## 🚀 Quick Start

### Basic Usage

```python
import asyncio
from src.orchestrator import HeteroMindOrchestrator

# Configuration
config = {
    "source_detection": {
        "layer2": {
            "api_key": "your-api-key",
            "model": "deepseek-chat",
            "base_url": "https://api.deepseek.com/v1",
        },
        "layer3": {
            "schemas": [{"database": "mydb", "tables": [...]}],
            "kg_endpoints": [
                {"name": "dbpedia", "url": "https://dbpedia.org/sparql"}
            ],
        },
    },
    "engines": {
        "sql": [{"name": "default", "enabled": True}],
        "sparql": [{"name": "default", "enabled": True}],
        "table_qa": [{"name": "default", "enabled": True}],
    },
}

async def main():
    orchestrator = HeteroMindOrchestrator(config)
    
    # Execute query with default LLM
    response = await orchestrator.query("How many employees are in Engineering?")
    print(f"Answer: {response.answer}")
    print(f"Source: {response.sources}")
    print(f"Confidence: {response.confidence:.2f}")
    
    # Execute query with specific model override
    response = await orchestrator.query(
        query="Show total sales by region",
        model="gpt-4-turbo",      # Override model
        api_key="sk-...",         # Override API key
    )

asyncio.run(main())
```

### Source Detection Only

```python
from src.classifier import SourceDetectorOrchestrator
import json

# Load schema
with open('tests/test_data/company_db_schema.json') as f:
    schema = json.load(f)

# Create detector
detector = SourceDetectorOrchestrator({
    "layer2": {
        "api_key": "sk-...",
        "model": "deepseek-chat",
    },
    "layer3": {
        "schemas": [schema],
    },
})

# Detect source
decision = await detector.detect("How many employees in Engineering?")

print(f"Primary Source: {decision.primary_source.value}")
print(f"Confidence: {decision.confidence:.2f}")
print(f"Reasoning: {decision.reasoning}")
```

---

## 📊 Supported Knowledge Sources

### 1. SQL Database (NL2SQL)

Supports MySQL, PostgreSQL, SQLite, and other relational databases.

**Example Queries:**
- "How many employees are in the Engineering department?"
- "Show average salary by department, top 3"

**Multi-stage Flow:**
1. Schema Linking - Identify relevant tables/columns
2. Query Generation - Generate 3 candidate SQL queries in parallel
3. Self-Revision - Multi-round review and improvement
4. Voting - Select the best candidate
5. Execution - Run the query

### 2. Knowledge Graph (NL2SPARQL)

Supports any SPARQL endpoint: DBpedia, Wikidata, custom KGs.

**Example Queries:**
- "Who is the founder of Microsoft?"
- "What companies are headquartered in Seattle?"

**Multi-stage Flow:**
1. Entity Linking - Link entities to KG
2. Ontology Retrieval - Get relevant predicates
3. Query Generation - Generate candidate SPARQL
4. Self-Revision - Review and improve
5. Voting - Select the best candidate

### 3. Table Files (TableQA)

Supports CSV, Excel, and other tabular files.

**Example Queries:**
- "Which quarter had the highest sales in 2024?"
- "Show total sales by region"

**Multi-stage Flow:**
1. Schema Analysis - Analyze table structure
2. Query Interpretation - Understand query intent
3. Code Generation - Generate Pandas code
4. Self-Revision - Review and improve code
5. Execution - Safely execute code

---

## 🧪 Testing

### Run Test Suite

```bash
cd HeteroMind
python3 comprehensive_tests.py
```

This will:
- Test all 3 engines (SQL, SPARQL, TableQA)
- Run 8 test cases total
- Generate detailed reports:
  - `tests/comprehensive_test_results.json` - JSON format results
  - `tests/comprehensive_test_report.md` - Markdown format report

### Test Data

Test data is located in `tests/test_data/`:

| File | Description |
|------|-------------|
| `company_db_schema.json` | SQL database schema |
| `sales_quarterly.csv` | Sample sales data (32 rows) |
| `kg_ontology.json` | Knowledge graph ontology |

---

## 🔧 Configuration

### LLM Configuration

Supports multiple LLM providers. Configure at initialization or per-call:

#### Global Configuration (Engine Initialization)

```python
from src.engines.nl2sql.multi_stage_engine import MultiStageNL2SQLEngine

# DeepSeek
engine = MultiStageNL2SQLEngine({
    "name": "sql_engine",
    "schema": schema,
    "llm_config": {
        "model": "deepseek-chat",
        "api_key": "sk-...",
        "base_url": "https://api.deepseek.com/v1",
    },
})

# GPT-4
engine = MultiStageNL2SQLEngine({
    "name": "sql_engine",
    "schema": schema,
    "llm_config": {
        "model": "gpt-4",
        "api_key": "sk-...",
    },
})

# Claude (via Anthropic)
engine = MultiStageNL2SQLEngine({
    "name": "sql_engine",
    "schema": schema,
    "llm_config": {
        "model": "claude-3-sonnet-20240229",
        "api_key": "sk-ant-...",
    },
})
```

#### Per-Call Override (Runtime)

```python
# Override model and API key at execution time
result = await engine.execute(
    query="How many employees?",
    context={},
    model="gpt-4-turbo",      # Override model
    api_key="sk-...",         # Override API key
)
```

#### Supported Providers

| Provider | Models | Configuration |
|----------|--------|---------------|
| **DeepSeek** | deepseek-chat, deepseek-coder | `base_url: https://api.deepseek.com/v1` |
| **OpenAI** | gpt-4, gpt-3.5-turbo | Default endpoint |
| **Azure OpenAI** | gpt-4, gpt-35-turbo | `base_url: https://{resource}.openai.azure.com` |
| **Anthropic** | claude-3-opus, claude-3-sonnet | Use OpenAI-compatible wrapper |
| **Local LLM** | Any OpenAI-compatible | `base_url: http://localhost:11434/v1` (Ollama) |


### 🔒 Security Best Practices

**Never commit API keys to version control!**

```bash
# ✅ Recommended: Use environment variables
export DEEPSEEK_API_KEY="sk-..."
export OPENAI_API_KEY="sk-..."

# ✅ Use .env file (add to .gitignore)
echo "DEEPSEEK_API_KEY=sk-..." >> .env

# ❌ Never hardcode API keys in code
llm_config = {"api_key": "sk-REAL-KEY-HERE"}  # DON'T DO THIS
```

**API Key Protection:**
- HeteroMind automatically sanitizes outputs to prevent credential leakage
- LLM prompts include security instructions to never output API keys
- Use environment variables or secure vaults for credential storage

### Generation Parameters

```python
generation_config = {
    "num_candidates": 3,        # Number of candidates to generate
    "max_revisions": 2,         # Maximum revision rounds
    "parallel_generation": True, # Enable parallel generation
    "voting_enabled": True,     # Enable voting mechanism
}
```

### Source Detection Weights

```python
weights = {
    "rule_based": 0.15,      # Layer 1: Keyword/pattern matching
    "llm_based": 0.35,       # Layer 2: LLM semantic classification
    "schema_based": 0.25,    # Layer 3a/3b: Schema/entity matching
    "verification": 0.25,    # Layer 3c: Entity verification
}
```

---

## 📁 Project Structure

```
HeteroMind/
├── README.md                    # This file
├── SKILL.md                     # ClawHub skill descriptor
├── requirements.txt             # Python dependencies
├── comprehensive_tests.py       # Comprehensive test suite
├── config/
│   ├── source_detection.yaml    # Source detection configuration
│   └── sources.yaml             # Knowledge source connections
├── src/
│   ├── __init__.py
│   ├── orchestrator.py          # Main orchestrator
│   ├── classifier/              # 4-layer source detection
│   │   ├── models.py            # Data models
│   │   ├── rule_detector.py     # Layer 1: Rule-based
│   │   ├── llm_detector.py      # Layer 2: LLM-based
│   │   ├── sql_schema_matcher.py # Layer 3a: SQL schema
│   │   ├── kg_entity_linker.py  # Layer 3b: KG entity linking
│   │   ├── entity_verifier.py   # Layer 3c: Entity verification
│   │   ├── source_fusion.py     # Layer 4: Multi-source fusion
│   │   └── orchestrator.py      # Detection orchestrator
│   ├── decomposer/              # Task decomposition
│   ├── engines/                 # Query engines
│   │   ├── base.py              # Base classes
│   │   ├── nl2sql/              # NL2SQL engine
│   │   ├── nl2sparql/           # NL2SPARQL engine
│   │   └── table_qa/            # TableQA engine
│   ├── fusion/                  # Result fusion
│   └── generator/               # Answer generation
└── tests/
    ├── README.md                # Test documentation
    └── test_data/               # Test data files
```

---

## 📈 Performance

| Metric | Value |
|--------|-------|
| Average Response Time (SQL) | ~22s |
| Average Response Time (KG/Table) | ~30s |
| Source Detection Time | <0.1s |
| Candidates Generated | 3 per query |
| Revision Rounds | 2 (configurable) |
| Confidence Range | 0.2 - 1.0 |

### Test Results

| Engine | Tests | Passed | Accuracy | Avg Confidence |
|--------|-------|--------|----------|----------------|
| **SQL (NL2SQL)** | 3 | 3 | 100.0% | 0.60 |
| **SPARQL (NL2SPARQL)** | 2 | 2 | 100.0% | 0.20 |
| **TableQA** | 3 | 3 | 100.0% | 0.62 |
| **Overall** | 8 | 8 | 100.0% | 0.51 |

---

## 👥 Author

**Coin Lab, Southeast University**

---

## 🙏 Acknowledgments

- DeepSeek for providing LLM API
- DBpedia and Wikidata for open knowledge graphs
- OpenClaw community for skill development framework

