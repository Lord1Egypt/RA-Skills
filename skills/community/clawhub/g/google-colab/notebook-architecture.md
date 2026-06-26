# Notebook Architecture - Google Colab

## Cell Contract Pattern

Use this sequence for reproducible notebooks:

1. **Environment cell**
- print Python version and runtime type
- install pinned dependencies
- verify imports

2. **Config cell**
- define paths, seeds, and key toggles in one place
- avoid redefining config in later cells

3. **Data load and validation cell**
- load from approved source
- validate required columns and row counts
- fail fast with clear message if schema mismatch

4. **Transform cell**
- deterministic preprocessing
- explicit handling for nulls and categorical mapping

5. **Train or inference cell**
- log hyperparameters and runtime checkpoints
- capture exceptions with minimal retry logic

6. **Evaluate and export cell**
- compute primary metrics
- export model and reports with metadata bundle

## Metadata Bundle

Every notebook run should emit a metadata dict with:
- notebook id or link
- runtime class
- dependency snapshot
- dataset version and split seed
- primary metrics

This bundle is the minimal evidence required to compare runs.
