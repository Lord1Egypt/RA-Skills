# OpenSearch Vector Search Expert

An AI agent skill for Amazon OpenSearch vector search (k-NN). Provides comprehensive guidance on configuration, cluster tuning, quantization, cost optimization, instance sizing, and **live cluster analysis**.

Supports **[OpenClaw](https://openclaw.ai)** and **[Kiro](https://kiro.dev)**.

## Features

- **Vector Search Configuration** — FAISS/HNSW parameter tuning, disk mode, space type selection
- **Capacity Planning** — HNSW memory formula calculations, instance sizing recommendations
- **Quantization Techniques** — FP16, Byte, Binary, Product Quantization with recall/cost tradeoffs
- **Cost Estimation** — Real-time AWS pricing via Pricing API, monthly cost projections
- **Cluster Tuning** — JVM, thread pools, shard strategies, node roles
- **Performance Benchmarks** — QPS/latency/recall data for various configurations
- **VectorDBBench Runner Skill** — Reproducible benchmark planning for managed domains, Serverless, on-disk, quantization, and the OpenSearch s3vector engine
- **Live Cluster Analyzer** 🆕 — Connect to any OpenSearch cluster, auto-discover k-NN indices, analyze vector configs, and generate optimization recommendations (read-only)

## Install

### OpenClaw

One-line install via [clawhub](https://clawhub.ai):

```bash
npx clawhub@latest install opensearch-vector-search
```

Or manually:

```bash
cp -r . ~/.openclaw/skills/opensearch-vector-search/
```

The skill is automatically discovered by OpenClaw and activated when relevant questions are asked.

### Kiro

Kiro supports this skill in two ways:

#### Option 1 — Global Steering (Recommended)

Install once into `~/.kiro/steering/` and the skill applies to **all projects** automatically — no per-project setup needed.

```bash
# Clone this repo, then copy into Kiro's global steering directory
git clone https://github.com/norrishuang/opensearch-vector-search-skill.git
cd opensearch-vector-search-skill

mkdir -p ~/.kiro/steering
cp SKILL.md ~/.kiro/steering/opensearch-vector-search.md
cp -r references ~/.kiro/steering/opensearch-references
```

That's it. Next time you ask Kiro anything about OpenSearch vector search, this skill will be in context.

> **Note:** `~/.kiro/steering/` is Kiro's global steering directory — files here apply to every workspace. Steering files without a frontmatter block are always included. You can add a frontmatter header to control activation:
> ```markdown
> ---
> inclusion: always
> ---
> ```

#### Option 1b — Project-scoped Steering

If you only want the skill active for a specific project:

```bash
cd /path/to/your-project
mkdir -p .kiro/steering
cp /path/to/opensearch-vector-search-skill/SKILL.md .kiro/steering/opensearch-vector-search.md
cp -r /path/to/opensearch-vector-search-skill/references .kiro/steering/opensearch-references
```

#### Option 2 — Agent Skill Resource

Use as a named skill attached to a specific Kiro agent (defined in `.kiro/agents/<agent>.json`):

```bash
# Copy skill into the .kiro/skills directory of your project
mkdir -p <your-project>/.kiro/skills/opensearch-vector-search
cp SKILL.md <your-project>/.kiro/skills/opensearch-vector-search/SKILL.md
cp -r references <your-project>/.kiro/skills/opensearch-vector-search/references
cp -r scripts <your-project>/.kiro/skills/opensearch-vector-search/scripts
```

Then reference it in your agent JSON (`.kiro/agents/<agent>.json`):

```json
{
  "name": "my-opensearch-agent",
  "description": "Agent with OpenSearch vector search expertise",
  "prompt": "You are an OpenSearch expert. Use the opensearch-vector-search skill for guidance.",
  "tools": ["fs_read", "shell"],
  "resources": [
    "skill://.kiro/skills/opensearch-vector-search/SKILL.md"
  ]
}
```

> **Tip:** Option 1 (Steering) is simpler and works for general questions in any Kiro chat. Option 2 (Agent Skill) is better when you want the knowledge scoped to a specific agent.

## Project Structure

```
├── SKILL.md                              # Skill definition and workflows
├── references/
│   ├── vector-search.md                  # k-NN, HNSW, disk mode guide
│   ├── quantization-1bit-32x.md           # 1-bit SQ on-disk tuning and cost data
│   ├── quantization-techniques.md        # Compression techniques comparison
│   ├── cost-optimization.md              # Instance sizing, memory formulas, cost cases
│   ├── cluster-tuning.md                 # JVM, thread pools, node configuration
│   ├── performance-benchmarks.md         # QPS/latency/recall benchmark data
│   ├── indexing-strategies.md            # Index mapping, shard, lifecycle
│   ├── query-optimization.md             # Query tuning, caching, pagination
│   └── optimized-instances.md            # OR1/OR2/OM2/OI2 instance guide
├── scripts/
│   ├── get_opensearch_pricing.py         # AWS Pricing API query tool
│   └── analyze_cluster.py               # Live cluster analyzer (read-only)
└── opensearch-vector-benchmark/
    ├── SKILL.md                          # VectorDBBench workflow and safety guardrails
    ├── references/                       # Scenario, runbook, and result-analysis guidance
    └── scripts/
        └── generate_benchmark_plan.py    # Dry-run/run command generator
```

## VectorDBBench Skill

The bundled `opensearch-vector-benchmark` skill guides agents through controlled OpenSearch
vector benchmarks with [VectorDBBench](https://github.com/zilliztech/VectorDBBench). It separates
managed domains, OpenSearch Serverless, and the OpenSearch `s3vector` engine; captures experiment
context; and explains on-disk oversampling and page-cache effects.

Generate a safe dry-run plan:

```bash
python3 opensearch-vector-benchmark/scripts/generate_benchmark_plan.py \
  --deployment managed \
  --host search-example.us-east-1.es.amazonaws.com \
  --case-type Performance768D1M \
  --db-label baseline
```

The managed-domain baseline uses `NUM_PER_BATCH=20000` and 40 indexing clients. Serverless starts
with one indexing client. The script only generates commands and never connects to a cluster.

## Live Cluster Analyzer

Connect to an OpenSearch cluster and analyze vector search configurations:

```bash
# Full analysis
python3 scripts/analyze_cluster.py \
  --url https://my-cluster.us-east-1.es.amazonaws.com \
  -u admin -p MyPassword \
  --action all -f pretty

# Cluster overview only
python3 scripts/analyze_cluster.py \
  --url https://my-cluster:9200 \
  -u admin -p MyPassword \
  --action cluster-overview

# Specific index deep dive
python3 scripts/analyze_cluster.py \
  --url https://my-cluster:9200 \
  -u admin -p MyPassword \
  --action index-detail --index my_vectors
```

**What it analyzes:**
- Cluster health, node resources (memory/CPU/JVM), OpenSearch version
- Auto-discovers all k-NN enabled indices
- Vector field configs: engine, dimensions, HNSW params, quantization, disk mode
- Memory estimates using AWS official HNSW formula
- Shard distribution across nodes
- Auto-generated optimization recommendations with severity levels

**Safety:** This script is strictly **read-only**. It never creates, modifies, or deletes any indices or data.

### Requirements

```bash
pip install opensearch-py
```

## Cost Estimation

Query real-time AWS OpenSearch pricing:

```bash
# All instance prices in a region
python3 scripts/get_opensearch_pricing.py --region us-east-1

# Specific instance type
python3 scripts/get_opensearch_pricing.py --region us-east-1 --instance-type r7g.12xlarge --format json
```

Requires `boto3` and valid AWS credentials.

## Key Formulas

### HNSW Memory (AWS Official)

```
Unquantized:  Memory = 1.1 × (4 × d + 8 × m) × num_vectors × (replicas + 1)
FP16 (2x):    Memory = 1.1 × (2 × d + 8 × m) × num_vectors × (replicas + 1)
Byte (4x):    Memory = 1.1 × (1 × d + 8 × m) × num_vectors × (replicas + 1)
```

### Node Memory Allocation

```
JVM Heap = min(node_memory × 50%, 32GB)
KNN available = (node_memory - JVM Heap) × 75%
```

## License

MIT-0 — Free to use, modify, and redistribute. No attribution required.
