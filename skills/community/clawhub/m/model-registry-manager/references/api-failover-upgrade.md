# API Failover Upgrade Notes

This reference is retained only as a historical note.

Current policy:
- `model-registry-manager` no longer carries generic failover policy guidance.
- It no longer defines retry ladders, fallback-routing semantics, or circuit-breaker defaults.
- The skill is now focused on model discovery, deduplication, probe validation, unusable-model cleanup, and registry sync only.
