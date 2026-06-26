---
name: Prethereum
description: Verifiable proofs for any computation. Ed25519 over SHA-256. TEE-backed signing, offline verification.
requires:
  - node >= 20
  - npm
env:
  - OCC_NOTARY_URL (optional, override notary endpoint)
network:
  commit: Sends user-provided bytes to the Nitro Enclave notary over HTTPS. Receives a signed proof. No data is persisted.
  verify: Fully offline. No network calls.
  health: Empty GET to notary /health. No payload.
config_paths: []
source: https://github.com/mikeargento/prethereum
license: Apache-2.0
---

# Prethereum

Verifiable proofs for any computation. Commit bytes, receive an Ed25519 signature over a SHA-256 digest. The proof is self-contained JSON. Verification is offline.

## Security Model

**Data flow:**

- **Commit** sends only the bytes you explicitly provide to the notary. The tool does not scan, enumerate, or read files beyond what is specified.
- **Verify** is fully local. No data leaves your machine.
- **Health** sends an empty GET. No payload.

**Notary behavior:**

The notary runs inside an AWS Nitro Enclave (hardware-isolated TEE). It receives bytes, computes a SHA-256 digest, signs with Ed25519, returns the proof. The enclave has no persistent storage. Nothing is logged, stored, or forwarded.

**Do not commit secrets.** Bytes transit over HTTPS. Do not send credentials, private keys, or sensitive PII.

## Network Behavior

| Operation | Direction | Payload | Persistence |
|-----------|-----------|---------|-------------|
| **Commit** | Client -> Notary | User-provided bytes (HTTPS) | None |
| **Verify** | Local only | None | N/A |
| **Health** | Client -> Notary | Empty GET | None |

## Requirements

- Node.js >= 20
- npm

## Installation

```
npm install prethereum
```

For the MCP server, install globally with a pinned version:

```
npm install -g @prethereum/mcp@0.1.0
```

All packages are open source (Apache-2.0). Inspect before installing:

```
npm pack @prethereum/mcp@0.1.0 && tar -xzf prethereum-mcp-0.1.0.tgz
```

## Quick Start

```typescript
import { Constructor, StubHost } from "prethereum";

const host = await StubHost.create();
const ctor = new Constructor(host);

const proof = await ctor.commit(
  Buffer.from("Hello, world")
);
```

## Verification

```typescript
import { verify } from "prethereum";

const result = await verify({ proof, bytes });
// result.valid === true | false
```

## HTTP API

```bash
curl -X POST http://localhost:3030/commit \
  -H "Content-Type: application/octet-stream" \
  --data-binary @output.json
```

## Packages

| Package | Description |
|---------|-------------|
| `prethereum` | Core library + stub for development |
| `@prethereum/nitro` | AWS Nitro Enclaves adapter |
| `@prethereum/mcp` | MCP server for Claude |
| `@prethereum/cli` | CLI: commit, verify, serve |
| `@prethereum/adapter-kit` | TEE builder kit + compliance suite |

## Source Code

- Repository: [github.com/mikeargento/prethereum](https://github.com/mikeargento/prethereum)
- MCP source: [packages/occ-mcp](https://github.com/mikeargento/prethereum/tree/main/packages/occ-mcp)

## References

- `references/protocol.md` - wire format and verification spec
