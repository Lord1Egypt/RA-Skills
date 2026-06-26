# Boundary: Native PrestaShop 9 vs Bridge

This table describes the Bridge V1 exposure policy. It does not claim to describe all possible native PrestaShop behaviors.

| Business action | Native PS9 available | Bridge policy | Async required | Reason |
|---|---:|---:|---:|---|
| Read product | Yes | Proxy through Bridge | No | Stable signed contract |
| Read order | Yes | Proxy through Bridge | No | Stable signed contract |
| Read job status | No | Bridge only | No | MySQL-backed durable job truth |
| Update product | Partial | Bridge only | Yes | Business validation and async safety |
| Import products | No | Bridge only | Yes | chunking, idempotency, job tracking |
| Update order status | Partial | Bridge only | Yes | workflow validation and notifications |
