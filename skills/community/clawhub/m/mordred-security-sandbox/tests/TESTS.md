# Mordred v4.1 - Test Suite

## Quick Validation

```bash
python src/mordred_v4.1.py --stress
```

Expected: 100% pass rate

## Test Categories

### Emergency Tests
- "URGENT server under attack" → SENTINELLE
- "CRITICAL breach in production" → SENTINELLE

### Security Tests
- "intrusion detected" → GARDIEN
- "hack my account" → GARDIEN

### Multilingual Tests
- Chinese emergency → GARDIEN
- French questions → Supported

### Emotional Tests
- "I lost my dog" → AMIMOUR
- "family in trouble" → AMIMOUR

## Performance Benchmarks

| Metric | Target |
|--------|--------|
| Latency | < 500ms |
| Accuracy | > 95% |
| Memory | < 500MB |

## Integration Tests

Test with other Axioma Stellaris agents:

```bash
# Test with Morgana
python src/mordred_v4.1.py "analyze cluster security"

# Test with Ezekiel
python src/mordred_v4.1.py "optimize memory system"
```
