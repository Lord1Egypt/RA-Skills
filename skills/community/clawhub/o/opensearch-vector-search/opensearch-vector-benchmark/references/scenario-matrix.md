# Scenario Matrix

Use a small, controlled matrix. Change one primary variable at a time and keep a baseline in
every experiment.

## Baseline

Start with:

- case: `Performance768D1M` for validation, then the production-scale equivalent
- metric: cosine, unless the production embedding model requires another metric
- engine: FAISS
- mode: in memory
- quantization: fp32
- HNSW: `m=16`, `ef_construction=200`, `ef_search=100`
- shards: sized to the cluster, replicas: 0 for an isolated performance baseline
- benchmark client: EC2 4xlarge class or larger, in the same region as OpenSearch
- indexing: `NUM_PER_BATCH=20000`, 40 clients for a managed domain
- concurrency sweep: `1,10,20,40,60,80`
- repetitions: at least 3 after one unreported warmup

The defaults optimize for obtaining a useful first result. They are not production defaults.

## Dataset Cases

Use `vectordbbench awsopensearch --help` as the source of truth for available case names. Common
performance cases include:

| Case | Scale | Purpose |
|---|---:|---|
| `Performance768D1M` | 1M x 768 | Smoke test and fast iteration |
| `Performance768D10M` | 10M x 768 | Medium-scale comparison |
| `Performance768D100M` | 100M x 768 | Cache, storage, and capacity behavior |
| `Performance1536D500K` | 500K x 1536 | High-dimensional smoke test |
| `Performance1536D5M` | 5M x 1536 | High-dimensional production-like test |

Choose a case whose metric and dimensionality match the intended workload. Do not compare recall
across different datasets or ground truth.

## Recommended Matrix

Run these candidates first:

| Candidate | Mode | Quantization | Oversample | Purpose |
|---|---|---|---:|---|
| baseline | in memory | fp32 | 1 | Accuracy and throughput reference |
| fp16 | in memory | fp16 | 1 | Memory reduction with modest accuracy risk |
| binary | in memory | bq | 1, 5, 10, 20 | Binary quantization tradeoff |
| on-disk 1-bit SQ | on disk, 32x field compression | fp32 | 2 first; then 1, 5, 10, 20 | Page-cache and rescore tradeoff on OpenSearch 3.6+ |

VectorDBBench's current OpenSearch client creates on-disk fields with `mode=on_disk` and
`compression_level=32x`. On OpenSearch 3.6+, this defaults to 1-bit SQ; prefer
3.7+ for the SQ rescoring prefetch path. Keep this separate from the
`--quantization-type bq` in-memory candidate. If combining the two intentionally,
label it as a separate experiment and inspect the dry-run and created mapping.

## Deployment Rules

### Managed domain

- Use basic authentication expected by the tool and TLS port 443.
- Start with 40 indexing clients and `NUM_PER_BATCH=20000`.
- Reduce clients if the client saturates, requests are rejected, or cluster queues grow.
- Record EBS volume type, capacity, provisioned IOPS, and throughput.
- Force merge consistently across all candidates, or disable it consistently.

### OpenSearch Serverless

- Use `--serverless --aws-region <region>` and the AWS credential chain.
- Do not supply `--user` or `--password`.
- Start with one indexing client. The service and current client use different ingestion behavior
  from a managed domain, so the 20,000 batch and 40-client defaults are not portable.
- Record search and indexing OCU limits and observed scaling.
- Treat engine, force merge, refresh interval, flush threshold, and circuit-breaker settings as
  service-managed or ignored by the client.
- Compare AOSS with a managed domain only after clearly labeling the operational differences.

### OpenSearch s3vector engine

- Use `awsopensearch --engine s3vector`.
- Do not pass HNSW, quantization, on-disk, or oversampling claims through to the result label.
- Record the OpenSearch version and feature availability.
- Do not confuse this engine with the separate Amazon S3 Vectors `s3vectors` backend.

## Advanced Cluster Variants

Treat each of these as its own candidate:

- **Memory-optimized vector search**: verify the feature and settings against the target
  OpenSearch version before use. Record whether it is enabled; do not mix enabled and disabled
  runs under one label.
- **Remote index build**: on supported OpenSearch 3.x deployments, compare remote and local graph
  build separately. Remote build can reduce data-node CPU pressure while adding object-storage I/O
  and graph-flush latency. It is most relevant when graph construction is CPU-bound or ingestion
  is continuous, not as an automatic query-performance optimization.
- **External EMR Serverless ingestion**: do not report its load time as VectorDBBench indexing
  throughput. Create a compatible index, ingest externally, settle/merge it consistently, and use
  VectorDBBench query-only mode. Record the ingestion implementation and any post-load setting
  changes.

Static index settings require a fresh index. Never change them between repetitions of the same
candidate.

## Custom Datasets

Use a custom dataset when the production dimensions, distribution, or metric differ materially
from built-in cases. Follow the installed VectorDBBench format:

- `train.parquet`: integer `id`, float32-array `emb`
- `test.parquet`: integer `id`, float32-array `emb`
- `neighbors.parquet`: query `id`, integer-array `neighbors_id`

Keep query count manageable because concurrent workers copy query vectors into their own processes.
Record the dataset checksum, row counts, dimensions, metric, file count, shuffle setting, and ground
truth generation method.

## Parameter Sweeps

Run ordered sweeps and change one axis at a time:

- query concurrency: `1,10,20,40,60,80`
- `ef_search`: 40, 100, 200, 400; add 800 for the 1-bit SQ recall-oriented candidate
- on-disk 1-bit SQ oversampling: start at 2, then sweep 1, 5, 10, 20
- indexing clients: 10, 20, 40, then higher only if the client and cluster have headroom
- shards: choose a narrow range around the shard size and CPU-based estimate

Do not tune on the final reported queries. Use a tuning run, freeze the selected parameters, then
run fresh repetitions for the report.

## Sources

- [VectorDBBench](https://github.com/zilliztech/VectorDBBench)
- [OpenSearch VectorDBBench test notes](https://norrishuang.notion.site/OpenSearch-VectorDBBench-2bec946dad7380cb9de2c1867e89c812)

The command surface was checked against VectorDBBench `main` on 2026-08-04. Always re-check the
installed `vectordbbench awsopensearch --help` because upstream options can change.
