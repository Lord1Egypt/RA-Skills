# Project Nirvana — Installation Guide

Complete step-by-step setup for local inference + privacy protection.

## Prerequisites

- Docker & Docker Compose
- OpenClaw 2026.3.0+
- Node.js 18+
- 6GB+ RAM (for Qwen3.5 + inference)
- 30GB free disk (for models)

## Quick Install (3 minutes, no setup needed)

### Step 1: Start Ollama

```bash
docker run -d \
  --name ollama \
  --restart unless-stopped \
  -v ollama:/root/.ollama \
  -p 11434:11434 \
  ollama/ollama
```

### Step 2: Install Nirvana Plugin

```bash
openclaw plugins install ShivaClaw/nirvana
```

### Step 3: Restart OpenClaw

```bash
openclaw gateway restart
```

**That's it.** The bundled qwen2.5:7b model (~3.5GB) auto-pulls on first run (~5 min). You're now thinking locally. No API keys required.

---

## Optional: Add Cloud Fallback

After local is working, enable cloud for advanced queries:

```bash
openclaw config patch '{
  "nirvana": {
    "routing": {
      "cloudFallback": true,
      "cloudModels": ["anthropic/claude-haiku-4-5"]
    }
  }
}'
```

Then add your API key and restart.

## Detailed Setup (Docker Compose)

For full local sovereignty, use docker-compose:

```yaml
version: '3.8'

services:
  ollama:
    image: ollama/ollama:latest
    container_name: ollama
    restart: unless-stopped
    volumes:
      - ollama_data:/root/.ollama
    ports:
      - "11434:11434"
    environment:
      - OLLAMA_HOST=0.0.0.0:11434
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3

  qdrant:
    image: qdrant/qdrant:latest
    container_name: qdrant
    restart: unless-stopped
    volumes:
      - qdrant_data:/qdrant/storage
    ports:
      - "6335:6335"
    environment:
      - QDRANT_API_KEY=qdrant_key_v1

  falkordb:
    image: falkordb/falkordb:latest
    container_name: falkordb
    restart: unless-stopped
    ports:
      - "6380:6379"

  openclaw:
    image: openclaw:latest
    container_name: openclaw
    restart: unless-stopped
    depends_on:
      ollama:
        condition: service_healthy
    volumes:
      - ~/.openclaw:/home/node/.openclaw
      - ./workspace:/workspace
    ports:
      - "3000:3000"
      - "8080:8080"
    environment:
      - OLLAMA_ENDPOINT=http://ollama:11434
      - QDRANT_ENDPOINT=http://qdrant:6335
      - FALKORDB_ENDPOINT=http://falkordb:6379
    networks:
      - nirvana

volumes:
  ollama_data:
  qdrant_data:

networks:
  nirvana:
    driver: bridge
```

Deploy:
```bash
docker-compose up -d

# Verify all services are running
docker-compose ps

# Check Ollama health
curl http://localhost:11434/api/tags
```

## Verify Installation

### 1. Check Plugin Registration

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  http://localhost:3000/api/plugins/nirvana/health
```

Expected response:
```json
{
  "initialized": true,
  "ollama": {"healthy": true, "models": ["qwen3.5:9b"]},
  "router": {"localPercentage": 0},
  "metrics": {}
}
```

### 2. Test Local Inference

```bash
# Send a simple query through OpenClaw
curl -X POST \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is 2+2?", "provider": "local"}' \
  http://localhost:3000/api/query
```

### 3. Check Privacy Boundaries

Inspect `memory/nirvana-audit.log`:
```bash
tail -f memory/nirvana-audit.log
```

You should see entries like:
```json
{"timestamp": "2026-04-19T...", "event": "query", "provider": "local"}
```

(No cloud calls until needed)

## Advanced Configuration

### Custom Models

To use different local models:

```bash
# List available models at ollama.ai
docker exec ollama ollama list

# Pull a model
docker exec ollama ollama pull mistral:latest

# Update openclaw.json
{
  "nirvana": {
    "ollama": {
      "models": ["mistral:latest", "neural-chat:latest"]
    }
  }
}
```

### GPU Acceleration

For NVIDIA GPUs:

```yaml
services:
  ollama:
    image: ollama/ollama:latest
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

For AMD GPUs:

```bash
docker run -d \
  --device /dev/kfd \
  --device /dev/dri \
  --group-add video \
  ollama/ollama:rocm
```

### Custom Routing Logic

Edit `src/router.js` to customize routing:

```javascript
// In src/router.js applyRoutingLogic()
case 'custom':
  return this.routeCustom(analysis);
```

### Disable Privacy Enforcement (Not Recommended)

```json
{
  "nirvana": {
    "privacy": {
      "enforceContextBoundary": false
    }
  }
}
```

## Upgrading

### From Previous Version

```bash
# Stop OpenClaw
openclaw gateway stop

# Update plugin
openclaw plugins install ShivaClaw/nirvana@latest

# Migrate config (if needed)
# See MIGRATION.md

# Restart
openclaw gateway start
```

### Backup Before Upgrading

```bash
# Backup metrics and audit logs
cp memory/nirvana-metrics.json memory/nirvana-metrics.bak.json
cp memory/nirvana-audit.log memory/nirvana-audit.bak.log

# Backup models
docker exec ollama tar czf /root/.ollama/models.tar.gz /root/.ollama/models
docker cp ollama:/root/.ollama/models.tar.gz ./ollama-backup-$(date +%Y%m%d).tar.gz
```

## Troubleshooting

### Ollama connection refused

```bash
# Check if container is running
docker ps | grep ollama

# Restart
docker restart ollama

# Check logs
docker logs ollama
```

### Out of memory

```bash
# Check memory usage
docker stats ollama

# Options:
# 1. Use smaller model: qwen2.5:7b (3.5GB) instead of qwen3.5:9b
# 2. Add swap: docker update --memory-swap 8g ollama
# 3. Upgrade host RAM
```

### Slow inference

```bash
# Check if GPU is being used
docker exec ollama nvidia-smi

# Monitor latency
tail -f memory/nirvana-metrics.json

# If latency > 5s:
# - Check host CPU/memory
# - Consider smaller model
# - Enable response caching
```

### Privacy violations detected

```bash
# Check audit log
cat memory/nirvana-audit.log | grep "violation"

# Review what was stripped
grep "contextStripped" memory/nirvana-audit.log

# Increase strip depth (more aggressive)
{
  "nirvana": {
    "privacy": {
      "contextStripDepth": "aggressive"
    }
  }
}
```

## Performance Tuning

### For Speed (Latency < 1s)

```json
{
  "nirvana": {
    "ollama": {
      "maxConcurrentRequests": 1,
      "timeout": 5000
    },
    "routing": {
      "localThreshold": 0.95,
      "cachingEnabled": true,
      "cacheTTL": 7200000
    }
  }
}
```

### For Accuracy (Quality > Speed)

```json
{
  "nirvana": {
    "routing": {
      "localThreshold": 0.5,
      "routingLogic": "hybrid",
      "cloudModels": ["anthropic/claude-sonnet-4-6"]
    }
  }
}
```

### For Privacy (Maximum Protection)

```json
{
  "nirvana": {
    "privacy": {
      "contextStripDepth": "aggressive",
      "enforceContextBoundary": true,
      "auditLog": true,
      "allowManualOverride": false
    }
  }
}
```

## Next Steps

1. **Monitor metrics:** `watch -n 5 'tail memory/nirvana-metrics.json'`
2. **Check audit log:** Daily review of `memory/nirvana-audit.log`
3. **Tune routing:** Adjust `localThreshold` based on use patterns
4. **Integrate with Trident:** Connect memory plugin for full sovereignty
5. **Deploy to ThinkCentre:** Test on local hardware before production

## Support

- Docs: `README.md`
- Config: `config.schema.json`
- Code: `src/`
- Issues: GitHub Issues
