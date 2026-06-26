# Project Nirvana — Migration Guide

How to migrate from cloud-only to local-first inference.

## Migration Path

### Phase 1: Install & Test (1-2 hours)

1. Install Nirvana via ClawHub (see INSTALL.md)
2. Test local inference on simple queries
3. Verify privacy boundaries are enforced
4. Monitor metrics for local routing %

### Phase 2: Gradual Rollout (1 week)

1. Day 1-2: Local threshold at 0.95 (only simple queries)
2. Day 3-4: Lower to 0.85 (medium + simple queries)
3. Day 5-6: Lower to 0.75 (most queries local)
4. Day 7: Lower to 0.70 (hybrid with validation)

### Phase 3: Full Deployment (day 8+)

- Monitor metrics daily
- Adjust `localThreshold` based on accuracy
- Archive cloud query logs for cost analysis
- Document any model-specific issues

## Data Migration

### Migrate Metrics & Audit Logs

```bash
# Backup cloud-era logs (optional)
mkdir -p archive/cloud-era/$(date +%Y%m%d)
cp memory/metrics.json archive/cloud-era/$(date +%Y%m%d)/
cp memory/audit.log archive/cloud-era/$(date +%Y%m%d)/

# Start fresh Nirvana logs
rm memory/nirvana-metrics.json memory/nirvana-audit.log
```

### Migrate Cached Responses

If you have cached cloud responses:

```bash
# Extract from old cache
python3 scripts/extract-cache.py memory/old-cache.db

# Import into Nirvana cache
python3 scripts/import-cache.py memory/nirvana-cache.json
```

(Scripts provided in plugin repo)

## Configuration Migration

### From: All Cloud

```json
{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-haiku-4-5"
    }
  }
}
```

### To: Local-First

```json
{
  "agents": {
    "defaults": {
      "model": "ollama/qwen3.5:9b",
      "fallbacks": [
        "anthropic/claude-haiku-4-5",
        "google/gemini-2.5-flash"
      ]
    }
  },
  "nirvana": {
    "ollama": {
      "enabled": true,
      "endpoint": "http://ollama:11434",
      "models": ["qwen3.5:9b"]
    },
    "routing": {
      "localFirst": true,
      "localThreshold": 0.80,
      "cloudFallback": true
    },
    "privacy": {
      "enforceContextBoundary": true
    }
  }
}
```

## Performance Comparison

### Before Migration (Cloud-Only)

- Latency: 2-5 seconds (API call + network)
- Cost: $0.05-0.15 per query (Haiku pricing)
- Privacy: Identity exported to third parties
- Uptime: Dependent on API availability

### After Migration (Local-First)

- Latency: 0.5-2 seconds (local inference)
- Cost: $0 per query (your hardware)
- Privacy: Identity stays local, never exported
- Uptime: Only depends on your hardware

### Expected Results

- **80%+ local routing** for typical agent workloads
- **40-60% reduction in latency** average
- **50%+ cost savings** (if heavily using cloud APIs)
- **Privacy gain:** Zero identity files exported

## Troubleshooting Migration

### Issue: Models failing locally but working in cloud

**Cause:** Local model lacks training for specific domain

**Solution:** 
```json
{
  "nirvana": {
    "routing": {
      "routingLogic": "domain-confidence",
      "domainThresholds": {
        "biology": 0.9,
        "crypto": 0.8,
        "general": 0.7
      }
    }
  }
}
```

### Issue: High false positive cloud fallbacks

**Cause:** `localThreshold` too high (router being too conservative)

**Solution:** Lower threshold gradually
```bash
# Day 1
localThreshold: 0.95

# Day 3
localThreshold: 0.85

# Day 7
localThreshold: 0.75
```

### Issue: Privacy violations still occurring

**Cause:** `contextStripDepth` not aggressive enough

**Solution:**
```json
{
  "nirvana": {
    "privacy": {
      "contextStripDepth": "aggressive"
    }
  }
}
```

### Issue: Local inference timing out

**Cause:** Model too large for available RAM

**Solution:** Use smaller model
```json
{
  "nirvana": {
    "ollama": {
      "models": ["qwen2.5:7b"],
      "timeout": 10000
    }
  }
}
```

## Rollback Plan

If migration causes issues:

```bash
# Revert to cloud-only (keep local running in background)
openclaw config patch '{
  "agents": {
    "defaults": {
      "model": "anthropic/claude-haiku-4-5",
      "fallbacks": []
    }
  },
  "nirvana": {
    "routing": {
      "localFirst": false,
      "cloudFallback": true
    }
  }
}'

# Restart
openclaw gateway restart

# Later: re-enable local gradually
openclaw config patch '{
  "nirvana": {
    "routing": {
      "localFirst": true,
      "localThreshold": 0.95
    }
  }
}'
```

## Success Criteria

Migration is successful when:

1. ✅ Local routing > 80% of queries
2. ✅ No privacy violations in audit log
3. ✅ Average latency < 2 seconds
4. ✅ Response quality comparable to cloud (human eval)
5. ✅ Zero identity files exported to third parties
6. ✅ Model-specific weaknesses documented and mitigated

## Post-Migration Optimization

### Optimize Local Models

```bash
# Profile model performance
docker exec ollama ollama show qwen3.5:9b

# Benchmark on your hardware
python3 scripts/benchmark.py --model qwen3.5:9b --queries 100

# Profile latency by query type
tail -f memory/nirvana-metrics.json | jq '.queryLatencies | group_by(.type)'
```

### Archive Cloud Costs

Calculate savings:

```bash
# Count cloud queries
grep '"provider":"cloud"' memory/nirvana-audit.log | wc -l

# Estimate cost savings
echo "Cloud queries: $(grep '"provider":"cloud"' memory/nirvana-audit.log | wc -l)"
echo "Estimated savings: $(grep '"provider":"cloud"' memory/nirvana-audit.log | wc -l | awk '{print $1 * 0.15 " USD"}')"
```

### Document Model Limitations

Keep a running log:

```markdown
# Model Limitations Log

## Qwen3.5:9b

### Works Well For
- General Q&A
- Simple analysis
- Code generation (Python, JS)
- Creative writing

### Weak On
- Deep mathematical reasoning
- Complex financial modeling
- Cutting-edge biotech (post-training data)

### Workarounds
- For math: route to Claude for validation
- For finance: use hybrid (local + cloud validation)
- For biotech: keep recent papers in context
```

## Cost Savings Report

Template for tracking savings:

```markdown
# Nirvana Migration — Cost Savings Report

## Before (Pure Cloud)

- API calls/month: 10,000
- Cost per query (Haiku): $0.015
- Monthly cost: $150
- Privacy: Exported identity + memory

## After (Local-First)

- API calls/month: 2,000 (20% cloud fallback)
- Cost per query: $0 (local), $0.015 (fallback)
- Monthly cost: $30
- Privacy: Zero exports, encrypted audit trail

## Net Savings

- Monthly: $120
- Annual: $1,440
- Privacy: Invaluable
```

## Next Steps

1. Plan migration timeline (7-day rollout recommended)
2. Set up metrics monitoring (dashboard or grep)
3. Document domain-specific routing needs
4. Train team on local-first workflow
5. Archive cloud costs for ROI calculation

## Support

- Issues: GitHub Issues
- Questions: Moltbook @clawofshiva
- Docs: README.md, INSTALL.md
