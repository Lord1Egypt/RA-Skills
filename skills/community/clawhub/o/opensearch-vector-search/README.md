# OpenSearch Vector Search Expert

An [OpenClaw](https://openclaw.ai) AgentSkill for Amazon OpenSearch vector search (k-NN). Provides comprehensive guidance on configuration, cluster tuning, quantization, cost optimization, instance sizing, and **live cluster analysis**.

## Features

- **Vector Search Configuration** — FAISS/HNSW parameter tuning, disk mode, space type selection
- **Capacity Planning** — HNSW memory formula calculations, instance sizing recommendations
- **Quantization Techniques** — FP16, Byte, Binary, Product Quantization with recall/cost tradeoffs
- **Cost Estimation** — Real-time AWS pricing via Pricing API, monthly cost projections
- **Cluster Tuning** — JVM, thread pools, shard strategies, node roles
- **Performance Benchmarks** — QPS/latency/recall data for various configurations
- **Live Cluster Analyzer** 🆕 — Connect to any OpenSearch cluster, auto-discover k-NN indices, analyze vector configs, and generate optimization recommendations (read-only)

## Install

```bash
npx clawhub@latest install opensearch-vector-search
```

Or manually copy to your OpenClaw skills directory:

```bash
cp -r . ~/.openclaw/skills/opensearch-vector-search/
```

## Project Structure

```
├── SKILL.md                              # Skill definition and workflows
├── references/
│   ├── vector-search.md                  # k-NN, HNSW, disk mode guide
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
```

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
