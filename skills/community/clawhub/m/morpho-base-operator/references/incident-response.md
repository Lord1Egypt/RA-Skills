# Incident Response Reference

- stop execution on address mismatch, paused market, unexpected adapter target, or any attempt to treat historical BSC context as an active write scope
- treat revert or receipt ambiguity as reconcile-required
- preserve logs and reports under `artifacts/`
- keep `allowMainnetExecution` at `false` by default until operator signoff is complete
- do not silently retry a failed write path
