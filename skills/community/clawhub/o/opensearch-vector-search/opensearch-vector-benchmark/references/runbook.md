# VectorDBBench Runbook

## 1. Confirm Isolation and Cost

Before any write:

- identify the AWS account, region, cluster/collection, and owner
- confirm the endpoint is a dedicated benchmark target
- confirm the benchmark index may be created, force-merged, and deleted
- estimate runtime and dataset, EC2, OpenSearch, EBS, OCU, S3, and transfer cost
- schedule a quiet test window and define an abort threshold

Suggested abort conditions include sustained write rejections, red cluster health, storage
watermarks, circuit-breaker events, client memory exhaustion, or unexpected production traffic.

## 2. Prepare the Client

Use Python 3.11 or newer and an isolated environment:

```bash
python3.11 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install 'vectordb-bench[opensearch]'
python --version
python -m pip freeze
vectordbbench awsopensearch --help
```

Prefer a dedicated EC2 client of 4xlarge class or larger. Place it in the same region and through
the same network path for every candidate. Verify CPU, memory, file descriptors, disk space, and
network throughput are not limiting the test.

Pin the exact VectorDBBench package version after validating its CLI. The upstream command surface
can change, so do not rely on copied examples alone.

If `vectordbbench --help` fails during import, do not debug or mutate a shared system Python
installation. Recreate the isolated environment and install a coherent pinned dependency set.
Older VectorDBBench installations can conflict with Pydantic v2, so a globally installed command
is not evidence that the benchmark client is ready.

## 3. Configure Authentication

For a managed domain, keep secrets out of shell history where possible:

```bash
export OPENSEARCH_USER='<benchmark-user>'
read -rsp 'OpenSearch password: ' OPENSEARCH_PASSWORD
export OPENSEARCH_PASSWORD
```

Use a benchmark-only principal with the minimum permissions required by VectorDBBench. The tool
creates and deletes its test index and changes index/cluster settings during some workflows.

For OpenSearch Serverless, use an EC2 instance role or another AWS credential-chain source. Grant
the IAM identity and AOSS data-access policy only the required benchmark collection permissions.

## 4. Capture a Manifest

Record:

- UTC timestamp, operator, purpose, and run label
- VectorDBBench and Python versions
- dataset case, metric, `k`, concurrency order, and repetitions
- endpoint class, region, OpenSearch version, and deployment type
- node/OCU configuration, storage, shards, replicas, and index mapping
- client EC2 type, OS, region/AZ, and network path
- batch size, indexing clients, HNSW values, quantization, mode, and oversampling
- force-merge policy, segment count, refresh interval, and warmup method

Use VectorDBBench `--note-file` when supported by the installed version. Do not include endpoint
credentials, tokens, account secrets, or private keys in the note.

## 5. Preflight

Check:

```text
GET /
GET /_cluster/health
GET /_cat/nodes?v
GET /_cat/indices?v
GET /_cluster/settings?include_defaults=true
GET /_plugins/_knn/stats
```

For AOSS, skip unsupported cluster-level APIs. Also verify enough free storage, green health for a
managed domain, no active shard relocation, stable CPU/JVM, and no competing indexing.

Generate the plan in dry-run mode:

```bash
python3 scripts/generate_benchmark_plan.py <options>
```

Inspect the resulting VectorDBBench configuration and verify the generated label is unique.

## 6. Execute

Generate the executable form only after preflight:

```bash
python3 scripts/generate_benchmark_plan.py <same-options> --phase run
```

Run one phase at a time:

- load-only: compare ingestion and index-build behavior
- query-only: reuse an existing test index with `--skip-drop-old --skip-load` and force merge off
- full: load, optimize, serial search, and concurrent search

Do not edit parameters between dry-run and run. Store stdout/stderr and result JSON with the
manifest. Monitor client CPU/memory/network and OpenSearch CPU/JVM, rejections, k-NN graph memory,
latency, IOPS, throughput, and queue depth.

## 7. On-Disk Checks

Estimate raw vector bytes:

```text
raw_vector_bytes = vector_count * dimensions * 4
```

Estimate this per shard copy and compare it with usable OS page cache after JVM heap, native graph
memory, and other processes. On-disk search has:

1. an approximate graph search over compressed vectors
2. optional full-precision rescore reads from storage

`oversample_factor=1.0` still performs rescore in the current VectorDBBench OpenSearch query.
Therefore, low CPU plus high read IOPS and high latency usually points to page-cache misses or
storage limits.

Use a consistent force merge. Multiple segments cause each query to search multiple subgraphs.
Avoid unnecessarily high `ef_construction` when measuring load and merge time.

## 8. Finish and Clean Up

- capture final cluster, k-NN, storage, and CloudWatch metrics
- copy result JSON and logs to the experiment artifact location
- verify all repeated runs are present before deleting anything
- delete only the dedicated benchmark index after explicit confirmation
- stop temporary EC2 and OpenSearch resources to prevent continued cost
- record failures and timeouts; do not silently discard them
