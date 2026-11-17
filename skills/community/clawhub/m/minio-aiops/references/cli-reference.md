# minio-aiops CLI reference

> The CLI is a convenience subset; the full 48-tool surface is via the MCP
> server (`minio-aiops mcp`). CLI writes delegate to the governed MCP twins,
> so they are audited + undo-recorded identically.

## Setup & diagnostics

```bash
minio-aiops init                    # wizard: endpoint, TLS, region, access key; secret key → encrypted store
minio-aiops doctor                  # config + secrets + live/ready + S3 auth + metrics reachability
minio-aiops doctor --skip-auth      # config/secrets checks only (no network)
minio-aiops overview                # health + capacity headline + exposure headline
```

## Secrets (encrypted store)

```bash
minio-aiops secret set <target>     # store/replace a secret key (prompted hidden)
minio-aiops secret list             # names only — values never shown
minio-aiops secret rm <target>
minio-aiops secret migrate          # import legacy plaintext .env keys
minio-aiops secret rotate-password  # re-encrypt under a new master password
```

## Reads

```bash
minio-aiops health check            # live + ready + cluster write-quorum
minio-aiops health status           # nodes/drives/capacity/buckets/objects
minio-aiops capacity rca            # flagship: capacity findings, cause + action
minio-aiops capacity usage          # per-bucket usage, biggest first
minio-aiops heal status             # flagship: erasure-set quorum risk + heal backlog
minio-aiops heal drives             # per-drive usage, fullest first
minio-aiops heal nodes              # per-node drive counts
minio-aiops bucket ls                # --limit caps the listing
minio-aiops bucket info <bucket>    # policy/versioning/lifecycle/encryption/quota/tags
minio-aiops bucket audit            # flagship: ranked exposure findings
minio-aiops bucket ilm-gap          # flagship: ILM gaps + reclaimable estimate
minio-aiops bucket objects <bucket> # objects under a prefix (--prefix, --limit)
minio-aiops bucket uploads <bucket> # incomplete multipart uploads
```

## Writes (all take --dry-run; destructive ones double-confirm)

```bash
minio-aiops bucket versioning-set <bucket> Enabled|Suspended
minio-aiops bucket policy-set <bucket> --file policy.json
minio-aiops bucket lifecycle-set <bucket> --expire-days 90 --noncurrent-days 30 [--prefix logs/]
minio-aiops bucket quota-set <bucket> <size-bytes>     # 0 clears
minio-aiops bucket purge-uploads <bucket> [--older-than-days 7]   # double confirm
minio-aiops bucket delete <bucket>                     # double confirm; refused unless empty
```

## MCP server

```bash
export MINIO_AIOPS_MASTER_PASSWORD=...   # required non-interactively (no TTY)
minio-aiops mcp                          # or: minio-aiops-mcp
```

Common options: `--target/-t <name>` selects a configured target (default: the
first one); `--dry-run` previews a write without executing.

## Truncation

Listing commands (`bucket ls`, `bucket objects`, `bucket uploads`,
`capacity usage`, `bucket audit`, `bucket ilm-gap`) return a
`{..., "returned": N, "limit": L, "truncated": bool}` envelope and print a
trailing `… truncated` note when there is more data — re-run with a higher
`--limit` rather than treating the output as complete.
