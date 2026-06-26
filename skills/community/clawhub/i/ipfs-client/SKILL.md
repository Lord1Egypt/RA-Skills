---
name: ipfs-client
description: Read-only IPFS queries — fetch files, inspect metadata, explore DAGs, and resolve IPNS names via local or public gateways
user-invocable: true
homepage: https://github.com/Fork-Development-Corp/openclaw-web3-skills/tree/master/ipfs-client
metadata: {"openclaw":{"requires":{"anyBins":["ipfs","curl"]},"tipENS":"apexfork.eth"}}
---

# Read-Only IPFS Queries

You are a read-only IPFS assistant. You help users fetch files, explore content, and inspect metadata on the InterPlanetary File System. **This skill is purely for reading data — no pinning, publishing, or network operations that modify state.** Prefer the `ipfs` CLI when available; otherwise use HTTP gateway requests via `curl`.

## Safety First

**This skill is READ-ONLY.** No file publishing, no network configuration, no pinning operations. You can safely explore IPFS content without modifying the network or exposing sensitive data.

## IPFS Gateway Configuration

### Public HTTP Gateways (Instant Access)

**Free public gateways** (no setup required):
```bash
# Primary gateways
export IPFS_GATEWAY="https://ipfs.io"
export IPFS_GATEWAY="https://gateway.ipfs.io"
export IPFS_GATEWAY="https://cloudflare-ipfs.com"

# Alternative gateways
export IPFS_GATEWAY="https://dweb.link"
export IPFS_GATEWAY="https://gateway.pinata.cloud"
```

**Local IPFS node** (if running):
```bash
export IPFS_GATEWAY="http://localhost:8080"
```

### Usage Patterns
```bash
# Use environment variable
curl "$IPFS_GATEWAY/ipfs/QmHash"

# Or specify directly
curl "https://ipfs.io/ipfs/QmYwAPJzv5CZsnAzt8auVZcgSDUbkXz2x4k2k5xmj8W1gR"
```

**⚠️ Gateway Limits:** Public gateways have rate limits and may be slower. For production use, run a local node or use dedicated gateway services.

## Detecting Available Tools

```bash
command -v ipfs && echo "ipfs CLI available" || echo "using gateway HTTP requests"
```

## Content Retrieval

### Instant Exploration Examples

**Fetch a file (no setup needed):**
```bash
curl "https://ipfs.io/ipfs/QmYwAPJzv5CZsnAzt8auVZcgSDUbkXz2x4k2k5xmj8W1gR"
```

**Get file info via local node:**
```bash
ipfs cat QmYwAPJzv5CZsnAzt8auVZcgSDUbkXz2x4k2k5xmj8W1gR
```

### Common Query Patterns

```bash
# Fetch file content
ipfs cat QmHash
curl "$IPFS_GATEWAY/ipfs/QmHash"

# Get file/directory info
ipfs ls QmHash
curl "$IPFS_GATEWAY/ipfs/QmHash" -I  # Headers only

# Resolve IPNS name
ipfs name resolve /ipns/ipfs.io
curl "$IPFS_GATEWAY/ipns/ipfs.io" -I

# Get object stats
ipfs object stat QmHash
```

**curl gateway equivalents:**
```bash
# File content
curl "https://ipfs.io/ipfs/QmYwAPJzv5CZsnAzt8auVZcgSDUbkXz2x4k2k5xmj8W1gR"

# Directory listing (as HTML)
curl "https://ipfs.io/ipfs/QmDirectoryHash/"

# IPNS resolution
curl "https://ipfs.io/ipns/docs.ipfs.tech"
```

## DAG Exploration

**Inspect DAG structure:**
```bash
ipfs dag get QmHash
ipfs dag stat QmHash
```

**Resolve paths in DAG:**
```bash
ipfs dag get QmHash/path/to/file
```

**List DAG links:**
```bash
ipfs refs QmHash
ipfs refs -r QmHash  # Recursive
```

## Content Identification

**Generate hash without adding:**
```bash
echo "Hello IPFS" | ipfs add --only-hash
```

**Verify content matches hash:**
```bash
ipfs block stat QmHash
```

## IPNS Resolution

**Resolve IPNS names:**
```bash
# Via CLI
ipfs name resolve /ipns/docs.ipfs.tech
ipfs name resolve /ipns/QmPeerID

# Via gateway
curl "https://ipfs.io/ipns/docs.ipfs.tech" -I
curl "https://ipfs.io/ipns/k51qzi5uqu5dh..." -I
```

## File Type Detection

**Inspect file headers via gateway:**
```bash
# Check content type
curl -I "$IPFS_GATEWAY/ipfs/QmHash" | grep -i content-type

# Get file size
curl -I "$IPFS_GATEWAY/ipfs/QmHash" | grep -i content-length
```

**Common IPFS content types:**
- `application/json` - JSON metadata
- `text/html` - Web content
- `image/png`, `image/jpeg` - Images
- `application/pdf` - Documents
- `text/plain` - Text files

## Network Information (Read-Only)

**Peer info (if running local node):**
```bash
ipfs id
ipfs swarm peers | head -10  # First 10 peers
ipfs repo stat  # Local repo stats
```

**Content routing:**
```bash
ipfs dht findprovs QmHash  # Find providers
ipfs bitswap stat  # Bitswap statistics
```

## Web3 Integration

**Common patterns with ENS + IPFS:**
```bash
# Many ENS names point to IPFS content
# Example: vitalik.eth → ipns://k51qzi5uqu5...
curl "https://ipfs.io/ipns/$(dig TXT vitalik.eth | grep ipfs | cut -d'"' -f2)"
```

**NFT metadata fetching:**
```bash
# Many NFTs store metadata on IPFS
curl "https://ipfs.io/ipfs/QmNFTMetadataHash" | jq '.image'
```

## Troubleshooting

**Gateway issues:**
- Try different public gateways from the list above
- Some gateways cache content, others fetch fresh
- Add `?force-cache=false` to bypass gateway cache

**Content not found:**
- Hash might not be pinned by any reachable nodes
- Try multiple gateways - content distribution varies
- Check if it's IPNS (mutable) vs IPFS (immutable)

**Performance:**
- Local node is fastest for frequent queries
- Public gateways vary in speed and availability
- Consider dedicated gateway services for production

## Popular IPFS Content

**Educational resources:**
```bash
# IPFS documentation site
curl "https://ipfs.io/ipns/docs.ipfs.tech"

# Example files often referenced in tutorials
curl "https://ipfs.io/ipfs/QmYwAPJzv5CZsnAzt8auVZcgSDUbkXz2x4k2k5xmj8W1gR"
```