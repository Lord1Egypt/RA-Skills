# Modular Processing Script Suite

This directory contains utility scripts for implementing modular processing patterns.

## Scripts

- `modular_split.py` - Decompose tasks into functional modules
- `sparse_activate.py` - Activate only relevant submodules
- `async_run.py` - Execute modules asynchronously
- `resource_monitor.py` - Track efficiency gains and metrics

## Usage

```bash
# Decompose a task into modules
python scripts/modular_split.py --task "analyze chart and explain trend"

# Activate sparse subset of modules
python scripts/sparse_activate.py --modules "visual,language" --task "chart analysis"

# Run modules asynchronously
python scripts/async_run.py --module visual --module language

# Monitor resource usage
python scripts/resource_monitor.py --report
```

## Notes

These scripts simulate brain-inspired modular processing at the workflow level.
For actual model-level sparse activation, see references/neural-sparse-coding.md.
