# OpenSearch 1-Bit Scalar Quantization (32x On-Disk)

Use this reference only for the 1-bit, 32x compression scenario. Do not generalize
these settings or benchmark results to FP16, byte quantization, legacy binary
quantization (BQ), or other compression levels.

## Terminology and Version Boundary

- OpenSearch 3.6 introduced 1-bit scalar quantization (SQ). For new 1-bit indexes,
  prefer SQ over legacy low-bit BQ.
- Starting in 3.6, disk-based vector search defaults to SQ. Use OpenSearch 3.7 or
  newer when possible because the SQ rescoring path includes I/O prefetch.
- `mode: on_disk` with `compression_level: 32x` keeps a 1-bit code and the HNSW
  graph in memory while retaining full-precision vectors on disk for rescoring.
- The explicit encoder name is `sq`, not `binary`:

```json
{
  "type": "knn_vector",
  "dimension": 768,
  "space_type": "cosinesimil",
  "method": {
    "name": "hnsw",
    "engine": "faiss",
    "parameters": {
      "encoder": {
        "name": "sq",
        "parameters": {
          "bits": 1
        }
      },
      "ef_construction": 200,
      "m": 16
    }
  }
}
```

For disk-based search, use the field-level form:

```json
{
  "type": "knn_vector",
  "dimension": 768,
  "mode": "on_disk",
  "compression_level": "32x",
  "space_type": "cosinesimil"
}
```

Check the created mapping and the target OpenSearch version. Do not label a run as
1-bit SQ merely because its domain or benchmark label contains `ondisk`.

## Memory Model

Estimate HNSW memory as:

```text
memory_bytes =
  1.1 * (dimension / 8 + 8 * m) * vectors * (replicas + 1)
```

For 100M vectors, 768 dimensions, `m=16`, and no replicas:

- 1-bit code: `768 / 8 = 96` bytes/vector
- HNSW links: `8 * 16 = 128` bytes/vector
- Estimated KNN memory: `1.1 * (96 + 128) * 100M = 22.9 GiB`

The `32x` claim applies to the vector payload (`3072 B` FP32 to `96 B` 1-bit),
not to total index memory. HNSW links do not compress, so total estimated KNN
memory falls from 327.8 GiB to 22.9 GiB, about 14.3x for this shape.

## Reproducible 100M Baseline

The following is an observed starting point, not a universal default:

| Item | Value |
|---|---|
| OpenSearch | 3.7 |
| Dataset | LAION 100M, 768 dimensions |
| Node | 1 x `r8g.4xlarge.search`, 123.6 GiB RAM, 16 vCPU |
| Storage | 787 GB gp3 |
| Index | FAISS HNSW, on-disk 32x, 12 shards, 0 replicas |
| Build parameters | `m=16`, `ef_construction=200` |
| Query starting point | `ef_search=200`, `oversample_factor=2` |
| Methodology | Warm page cache with 2-3 unreported runs before measurement |

VectorDBBench's OpenSearch client uses `--on-disk` to create the 32x field.
Keep `--quantization-type fp32` for this candidate unless intentionally testing
a separate BQ combination; the field's on-disk SQ is distinct from the CLI's
in-memory `--quantization-type bq` candidate.

Observed results after warmup:

| k | ef_search | Oversample | Max QPS | Recall | Serial P95 |
|---:|---:|---:|---:|---:|---:|
| 100 | 200 | 2 | 674.86 | 0.9525 | 10.6 ms |
| 10 | 200 | 2 | 780.95 | 0.9546 | 8.6 ms |
| 100 | 800 | 2 | 376.90 | 0.9617 | 14.4 ms |
| 100 | 800 | 1 | 389.57 | 0.9342 | 13.7 ms |

Start with `ef_search=200` and `oversample_factor=2` for the throughput/recall
balance. Use `ef_search=800`, `oversample_factor=2` only when the additional
recall is worth the throughput loss. Sweep parameters on the target dataset;
both parameters were effective in this 1-bit SQ test.

Single-node throughput saturated near 675 QPS for `k=100`; increasing client
concurrency raised latency without increasing throughput. Scale beyond that
point with replicas or additional nodes, then remeasure.

## Cost Comparison

Observed sizing and on-demand estimates for 100M x 768 dimensions in
`us-east-1`, using 730 hours/month:

| Metric | FP32 in memory | FP16 (2x) | 1-bit SQ on-disk (32x) |
|---|---:|---:|---:|
| Estimated KNN memory | 327.8 GiB | 170.5 GiB | 22.9 GiB |
| Storage | ~50 GB | ~50 GB | ~372 GB |
| Example deployment | 1 x r8g.16xlarge | 3 x r8g.4xlarge | 1 x r8g.4xlarge |
| Estimated monthly cost | ~$4,424 | ~$3,330 | ~$1,137 |
| Relative cost | 1.00x | 0.75x | 0.26x |
| QPS per $1K/month | 520 | 328 | 594 |

The 1-bit on-disk estimate is about 74% below the FP32 example. Its economics
come from replacing RAM with gp3 storage: the measured index occupied about
372 GB, while the in-memory code plus graph required about 22.9 GiB.

Apply these caveats whenever citing the table:

1. Only the 1-bit on-disk column was measured in the same 2026-08 test. FP32
   and FP16 throughput came from other runs or estimates.
2. The source's cross-column recall values used different or unverified query
   settings, so do not claim that 1-bit SQ is more accurate than FP32.
3. Prices are point-in-time on-demand assumptions and exclude transfer,
   cross-AZ replicas, snapshots, and commitment discounts. Refresh prices
   before making a current cost claim.
4. OpenSearch 3.3 produced only 2.84 QPS in the same memory-starved on-disk
   shape. Do not apply the 3.7 result to versions before 3.6.

## Recommendation Rules

- Recommend this path for new, cost-sensitive 1-bit deployments on OpenSearch
  3.6+, preferably 3.7+.
- Reindex when moving from legacy BQ to SQ; the encoder is an index-time choice.
- Validate top-k recall, QPS, P95/P99, KNN memory, page-cache warmup, and EBS
  read behavior on production-shaped data.
- Test radial or `min_score` recall separately when the application performs
  deduplication. The top-k results above do not validate radial search.
- Never linearly extrapolate the single-node 100M QPS result to billion-scale
  datasets or multi-shard fan-out.
