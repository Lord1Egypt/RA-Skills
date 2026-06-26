# Deployment Patterns - MinIO

Use this guide to select a deployment shape before any data migration or production cutover.

## Pattern Matrix

| Pattern | Best For | Tradeoffs | First Checks |
|---------|----------|-----------|--------------|
| Single Node | Labs, low-risk internal tools | Simple but no distributed durability | Disk health, backup cadence, TLS enabled |
| Distributed Erasure Set | Production object workloads | More moving parts and network sensitivity | Node count parity, clock sync, network path quality |
| Tenant Style Isolation | Multi-team environments | Higher operational overhead | Per-tenant policy boundaries, quota model, monitoring split |

## Capacity and Durability Baseline

Before provisioning:
- estimate object growth for 90 days and 12 months
- reserve headroom for rebuild and healing operations
- validate target IO profile with representative object sizes

Before cutover:
- confirm versioning defaults for critical buckets
- confirm object lock and retention requirements
- confirm backup and restore test has passed

## TLS and Endpoint Design

- Assign stable DNS names per environment.
- Use certificates with correct SAN coverage for API and console endpoints.
- Validate chain trust from every client environment that will run `mc`.

## Networking Guardrails

- Keep east-west traffic predictable between storage nodes.
- Avoid mixed latency paths inside one distributed set.
- Monitor packet loss and clock skew continuously.

## Change Rollout Strategy

Use progressive rollout:
1. Pilot one low-risk bucket.
2. Validate reads, writes, policies, and lifecycle behavior.
3. Expand by workload class, not by all buckets at once.

Stop rollout immediately if validation fails.
Fix root cause before resuming.
