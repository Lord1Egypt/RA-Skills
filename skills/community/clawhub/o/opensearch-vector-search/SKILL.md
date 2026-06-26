---
name: opensearch-vector-search
version: 1.3.0
repository: https://github.com/norrishuang/opensearch-vector-search-skill
description: |
  Amazon OpenSearch vector search expert knowledge base. Comprehensive guidance on vector search configuration, cluster tuning, quantization, cost optimization, instance sizing, and pricing estimation.

  **Use this Skill when**:
  (1) User asks about OpenSearch vector search (k-NN) configuration, HNSW parameter tuning, disk mode
  (2) User needs vector search cluster sizing, capacity planning, instance recommendations
  (3) User asks about quantization techniques (Binary/Byte/FP16/Product Quantization)
  (4) User needs to estimate OpenSearch vector search costs or query pricing
  (5) User asks about OpenSearch indexing strategies, shard planning, query optimization
  (6) User mentions "vector database", "vector search", "k-NN", "knn_vector", "embedding search", "HNSW"
  (7) User mentions data scale (e.g. "100M vectors", "1 billion vectors") and needs cluster configuration advice
  (8) User asks about OpenSearch cluster JVM, memory, or thread pool configuration
  (9) Involves Amazon OpenSearch Service pricing, cost calculation, or instance comparison
  (10) User provides an OpenSearch cluster URL/credentials and wants vector configuration analysis or health check
requirements:
  env:
    - name: AWS_ACCESS_KEY_ID
      description: AWS credentials for pricing API (boto3). Only needed when running the pricing script.
      optional: true
    - name: AWS_SECRET_ACCESS_KEY
      description: AWS secret key. Only needed when running the pricing script.
      optional: true
  tools:
    - python3
    - boto3
    - opensearch-py
---

# OpenSearch Vector Search Expert

> **GitHub**: [norrishuang/opensearch-vector-search-skill](https://github.com/norrishuang/opensearch-vector-search-skill)
> — Issues, PRs, and new reference contributions are welcome!

## Safety Notes

- **Pricing script** (`scripts/get_opensearch_pricing.py`): Makes outbound HTTPS requests to the AWS Pricing API (`pricing.us-east-1.amazonaws.com`). Requires `boto3` and valid AWS credentials. The script is **read-only** (fetches public pricing data) and does not modify any AWS resources. Only run it when the user explicitly requests cost estimation.
- **Reference examples**: Code snippets in `references/` contain example API calls to `localhost:9200` (standard OpenSearch endpoint). These are **documentation examples only** — do NOT execute them automatically. Present them to the user as configuration references.
- **Cluster analyzer** (`scripts/analyze_cluster.py`): Connects to a user-provided OpenSearch cluster and performs **read-only** analysis. It NEVER creates, modifies, or deletes any indices or data. Only run it when the user explicitly provides cluster credentials (URL + username/password).

## Knowledge Base Structure

Read the corresponding reference file based on the question type:

| Question Type | Reference File | Keywords |
|--------------|----------------|----------|
| Vector search, k-NN, HNSW, disk mode | `references/vector-search.md` | vector, knn, hnsw, warmup, disk mode, on_disk |
| Quantization techniques | `references/quantization-techniques.md` | quantization, compression, binary, byte, fp16, product quantization |
| Cost optimization, instance sizing, memory calc | `references/cost-optimization.md` | cost, pricing, instance, memory calculation, cluster sizing, budget |
| Cluster tuning, JVM, thread pools | `references/cluster-tuning.md` | JVM, heap, thread pool, node role, shard allocation |
| Performance benchmarks, dataset sizing | `references/performance-benchmarks.md` | benchmark, QPS, latency, recall, dataset size |
| Indexing strategies, mapping | `references/indexing-strategies.md` | index, mapping, shard, replica, lifecycle |
| Query optimization | `references/query-optimization.md` | query, filter, aggregation, cache, pagination |
| Optimized instances (OR1/OR2/OM2/OI2) | `references/optimized-instances.md` | optimized, OR1, OR2, OM2, OI2, S3 durability, indexing throughput |
| Live cluster analysis | `scripts/analyze_cluster.py` | analyze cluster, connect, diagnose, review config, health check |

## Core Workflows

### 1. Answering Vector Search Configuration Questions

1. Read `references/vector-search.md`
2. Recommend in-memory mode or disk mode based on user scenario (latency requirements, data scale, QPS)
3. Provide specific mapping JSON configuration
4. Recommend FAISS engine + cosine similarity + 7/8 series instances

### 2. Capacity Planning & Instance Sizing (Most Common Scenario)

After user provides vector count and dimensions:

1. Read `references/cost-optimization.md` for memory calculation formulas and examples
2. Calculate using the standard HNSW memory formula (source: AWS official blog):
   ```
   Unquantized (float32):
     Memory = 1.1 × (4 × d + 8 × m) × num_vectors × (replicas + 1) bytes
   
   Quantized (FAISS engine, compressed vectors in memory):
     FP16 (2x):    Memory = 1.1 × (2 × d + 8 × m) × num_vectors × (replicas + 1)
     Byte (4x):    Memory = 1.1 × (1 × d + 8 × m) × num_vectors × (replicas + 1)
     Binary 4-bit: Memory = 1.1 × (d/2 + 8 × m) × num_vectors × (replicas + 1)
     Binary 2-bit: Memory = 1.1 × (d/4 + 8 × m) × num_vectors × (replicas + 1)
     Binary 1-bit: Memory = 1.1 × (d/8 + 8 × m) × num_vectors × (replicas + 1)
   
   Where: d=vector dimensions, m=HNSW connections (default 16), num_vectors=total vector count
   ```
3. Apply OpenSearch node memory allocation rules:
   ```
   JVM Heap = min(node_memory × 50%, 32GB)
   Remaining memory = node_memory - JVM Heap
   KNN available memory = remaining × 75%  (with knn.memory.circuit_breaker.limit=70%, ~35% of node memory)
   ```
4. Select instance type, ensuring total cluster KNN available memory > vector index memory requirement
5. Run pricing script for real-time pricing (see below)

### 3. Cost Estimation (with Real-Time Pricing)

When user needs cost estimation:

1. Complete capacity planning above
2. Run pricing script for real-time prices:
   ```bash
   python3 scripts/get_opensearch_pricing.py --region <region> --instance-type <type>
   ```
3. Calculate monthly cost:
   ```
   Instance cost = unit_price × node_count × (1 + replica_count)
   EBS cost = capacity(GB) × $0.08 + additional IOPS charges
   Total cost = Instance cost + EBS cost
   ```
4. Compare cost differences across quantization options

### 4. Live Cluster Analysis (When User Provides Cluster Credentials)

When the user provides an OpenSearch cluster URL and credentials, use the cluster analyzer to
connect and review their vector search configuration. This is **read-only** — never modify the cluster.

**Prerequisites**: User must explicitly provide:
- Cluster URL (e.g., `https://my-cluster.us-east-1.es.amazonaws.com`)
- Username and password (basic auth), OR `--no-auth` for clusters without authentication

**Workflow**:

1. **Ask for credentials** if not provided: URL, username, password
2. **Run cluster overview** to get health, nodes, and k-NN index list:
   ```bash
   python3 scripts/analyze_cluster.py --url <url> -u <user> -p <pass> --action cluster-overview -f pretty
   ```
3. **Analyze specific index** if user specifies one, or pick the most important k-NN index:
   ```bash
   python3 scripts/analyze_cluster.py --url <url> -u <user> -p <pass> --action index-detail --index <index_name> -f pretty
   ```
4. **Analyze shard distribution** for the target index:
   ```bash
   python3 scripts/analyze_cluster.py --url <url> -u <user> -p <pass> --action shard-analysis --index <index_name> -f pretty
   ```
5. **Run all analyses at once** (for a comprehensive report):
   ```bash
   python3 scripts/analyze_cluster.py --url <url> -u <user> -p <pass> --action all --index <index_name> -f pretty
   ```
6. **Interpret the JSON output** and present findings to the user:
   - Cluster health status and node resource utilization
   - Vector field configurations (engine, dimensions, HNSW params, quantization)
   - Memory estimates vs actual cluster capacity
   - Auto-generated recommendations (from the script)
7. **Provide actionable advice** based on findings:
   - Suggest better engine/quantization if needed (provide example mapping JSON)
   - Suggest instance resizing if memory is over/under-provisioned
   - Suggest shard rebalancing if distribution is uneven
   - **NEVER execute write operations** — only provide example configurations for the user to apply

**Cluster Analyzer Script Reference**:
```
Usage:
  python3 scripts/analyze_cluster.py --url <url> -u <user> -p <pass> [options]

Actions:
  --action cluster-overview   Cluster health, nodes, k-NN stats, and all k-NN index summary (default)
  --action index-detail       Deep dive into a specific index's vector config + memory estimates
  --action shard-analysis     Shard distribution and sizing for a specific index
  --action all                Run all analyses

Options:
  --index <name>     Target a specific index (required for index-detail and shard-analysis)
  --no-auth          Connect without authentication
  --verify-ssl       Verify SSL certificates (default: skip)
  --format pretty    Human-readable JSON output

Output: JSON with these top-level keys:
  - cluster_overview: health, version, nodes (memory/CPU/JVM), knn_stats
  - knn_indices: list of all k-NN enabled indices with vector field summaries
  - index_detail/index_details: vector field configs, memory estimates, search stats
  - shard_analysis/shard_analyses: shard distribution across nodes
  - recommendations: auto-generated optimization suggestions with severity levels
```

**Safety constraints for live cluster analysis**:
- The script is strictly **read-only** (uses only GET/CAT APIs)
- **NEVER** create, update, or delete indices on the user's cluster
- **NEVER** change cluster settings or mappings
- Only provide example JSON configurations for the user to review and apply themselves
- If the user asks to apply changes, provide the exact API calls/JSON but let the user execute them

### Pricing Script Usage

```bash
# Query all instance prices for a region
python3 scripts/get_opensearch_pricing.py --region us-east-1

# Query specific instance type (no .search suffix needed)
python3 scripts/get_opensearch_pricing.py --region us-east-1 --instance-type r7g.xlarge

# JSON format output (for calculations)
python3 scripts/get_opensearch_pricing.py --region us-east-1 --instance-type r7g.xlarge --format json
```

Output fields: instance_type, vcpu, memory_gib, price_per_hour_usd, price_per_month_usd, network

## Recommended Defaults

Always recommend these defaults unless user has specific requirements:

- **Engine**: FAISS
- **Similarity**: cosine
- **Instance family** (Gen 7+ only, never recommend older generations):
  - **Vector search (k-NN)**: r7g/r8g/r8gd (memory-optimized, lowest search latency; r8g Graviton4 ~30% faster than r7g)
  - **Indexing-heavy + vector**: OR2 (optimized, S3 durability, good memory-to-price ratio)
  - **Indexing-heavy (no vector)**: OM2 (highest indexing throughput, 15% faster than OR1)
  - **Large dataset with NVMe**: OI2 (storage-optimized, no EBS needed)
  - Do NOT recommend: r6g, r5, m5, c5, i3, or any older instance families
- **HNSW parameters**: ef_construction=512, m=16
- **Quantization preference**: Byte (4x) for production, Binary (32x) for aggressive cost optimization
- **Disk mode threshold**: Consider when data > 50M vectors and 100-200ms latency is acceptable

### Instance Selection Decision Tree

```
Is this primarily a vector search (k-NN) workload?
├─ YES → r7g/r8g/r8gd (best search latency, standard EBS; prefer r8g for Graviton4)
│        └─ Need S3 durability? → OR2 (accept 10s refresh interval tradeoff)
├─ Mixed (logs + vectors) → OR2 for log nodes, r7g/r8g for vector nodes
└─ NO (logs/observability/analytics)
   ├─ Write-heavy → OM2 (highest ingest throughput)
   ├─ Balanced → OR2 (good all-around with S3 durability)
   └─ Need NVMe IOPS → OI2
```

## Response Template

Organize cost/sizing answers in this structure:

1. **Requirements confirmation**: Vector count, dimensions, QPS, latency requirements
2. **Memory calculation**: Raw size → quantized size → required KNN memory
3. **Cluster configuration**: Instance type × count, shards, replicas
4. **Cost estimation**: Instance cost + EBS cost = monthly total
5. **Optimization suggestions**: Quantization comparison, Reserved Instance discounts
