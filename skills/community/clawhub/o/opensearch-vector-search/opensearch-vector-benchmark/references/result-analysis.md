# Result Analysis

## Validity Gate

Reject or clearly qualify a comparison when any of these differ unintentionally:

- dataset, dimensions, metric, ground truth, `k`, or payload
- OpenSearch version, deployment type, node/OCU shape, storage, or network path
- shards, replicas, segment count, merge policy, or warmup state
- VectorDBBench version, benchmark client size, batch size, or indexing clients
- query concurrency order, duration, timeout, or repetition count
- HNSW, quantization, mode, rescore, or oversampling settings

Confirm the benchmark client stayed below saturation. Client CPU, memory pressure, network, or
process limits can cap QPS independently of OpenSearch.

## Metrics

Report at least:

- recall at the benchmark `k`
- serial latency and concurrent latency percentiles
- QPS at each concurrency, not only maximum QPS
- indexing throughput, load time, optimization/merge time, and searchable readiness
- failed requests, timeouts, rejections, and incomplete runs
- index size and storage amplification
- client CPU/memory/network
- OpenSearch CPU/JVM/GC, k-NN graph memory, cache events, search/index queues
- storage read/write IOPS, throughput, queue depth, and burst balance where relevant
- estimated hourly and monthly infrastructure cost

Apply a recall threshold before comparing throughput. A faster candidate that misses the required
recall is not a winner.

## Repetitions

Run at least three measured repetitions after warmup. For each metric report:

- median
- minimum and maximum, or coefficient of variation
- number of successful and failed runs

Investigate large variance before drawing conclusions. Preserve timeout and failure results.

## On-Disk Diagnosis

On-disk mode stores a compressed graph for approximate search and reads full-precision vectors
during rescore. The critical memory pools are different:

- native/off-heap k-NN memory holds graph data
- OS page cache may hold full-precision vector files used for rescore

Use:

```text
raw_vector_bytes = vector_count * dimensions * 4
```

If the relevant shard data cannot fit in usable page cache, random reads increase. Typical evidence:

- QPS collapses as data scale grows
- latency and read IOPS rise
- CPU remains low
- `oversample_factor` increases the effect by expanding the rescore candidate set

`oversample_factor=1.0` does not disable rescore. If testing rescore disabled requires a tool or
code change, label that candidate separately and document the exact query body.

Force merge can reduce the number of segment subgraphs searched per query. Keep the merge policy
and final segment count identical across candidates.

## Summary Table

Use one row per candidate and repetition aggregate:

| Candidate | Recall@k | Peak QPS | p50 | p95 | p99 | Load time | Index size | Read IOPS | Cost/hour | Notes |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|

Then state:

1. the recall-qualified winner for latency
2. the recall-qualified winner for throughput
3. the best cost/performance candidate
4. the bottleneck evidence
5. the confidence and limitations

Do not reuse published benchmark numbers as predictions for a different cluster. Use them only to
form hypotheses that the user's own controlled run can test.
