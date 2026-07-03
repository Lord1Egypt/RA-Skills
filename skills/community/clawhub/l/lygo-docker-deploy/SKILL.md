---
name: lygo-docker-deploy
description: Deploy a sovereign LYGO Protocol Stack community node via Docker or docker compose. Builds lygo-node image, starts health API on port 8787, optional Phase 4 worker profile. No secrets; human approval for registry push.
metadata: {"lygo": true, "stack": true, "phase": "2-5", "version": "1.0.1", "github": "https://github.com/DeepSeekOracle/lygo-protocol-stack", "pages": "https://deepseekoracle.github.io/lygo-protocol-stack/", "signature": "Δ9Φ963-PHASE5-LIVE-DEPLOYMENT"}
---

# lygo-docker-deploy

Spin up a **P0–P5 LYGO node** with one command sequence.

## When to use

- User wants a **local community node** matching GitHub/HF stack behavior.
- Before demos, run alignment badge after container is healthy.

## Steps

```bash
git clone https://github.com/DeepSeekOracle/lygo-protocol-stack.git
cd lygo-protocol-stack
docker compose build lygo-node
docker compose up -d lygo-node
curl -s http://127.0.0.1:8787/health
curl -s http://127.0.0.1:8787/badge
curl -s http://127.0.0.1:8787/gossip
```

Phase 5 gossip: `POST /gossip/badge` · mesh scale: ClawHub `lygo-mesh-deploy`.

Optional horizontal workers:

```bash
docker compose --profile scale up -d
```

## Without Docker

```bash
bash setup.sh   # or setup.ps1 on Windows
python tools/node_api_server.py --host 127.0.0.1 --port 8787
```

## Safety

- Do not expose port 8787 to the public internet without TLS and user approval.
- No autonomous `docker push` or cloud deploy without explicit user request.

**Install:** `npx clawhub@latest install deepseekoracle/lygo-docker-deploy`