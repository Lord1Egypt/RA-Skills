---
name: helm-evidence
description: Check and verify AI-number figures from extracted reviewer files with Helm, offline via helmd. Never paste raw extract numbers; quote exit codes.
license: Apache-2.0
metadata:
  openclaw:
    requires:
      bins:
        - helmd
---

# Helm evidence checking

Helm recomputes AI-number figures from a reviewer's own extract files and
compares them to asserted values. Everything runs offline through `helmd`; no
daemon is required for the two verbs below.

## Rules

1. Never paste raw extract numbers into chat. Reference the input file and the
   exit code instead.
2. Quote exit codes when reporting a result. A bare "it matched" is not a
   citable result.
3. `helmd verify <bundle.json> --keys <publicKeys.json>` before any "VALID"
   claim. Exit 0 means the signed bundle verified offline; say that, with the
   exit code.
4. `--no-anchor` semantics: use it only when the pack has no asserted value
   yet. It runs a recompute-only pass (check exits 2) and never anchors a
   per-file value.

## Quick reference

```
helmd check <pack_id> <input.json> [--out <bundle.json>] [--json]
helmd check <pack_id> --glob "extracts/*.json" [--out-dir <dir>] [--json]
helmd verify <bundle.json> --keys <publicKeys.json> [--json]
helmd list-scenarios --json
helmd status --json
```

Exit codes for `check`: 0 match, 1 differs, 2 no asserted value
(recompute-only), 3 insufficient input, 4 usage error, 5 scope disagreement.
Exit codes for `verify`: 0 valid, 1 invalid, 2 usage error (verification never
attempted).
