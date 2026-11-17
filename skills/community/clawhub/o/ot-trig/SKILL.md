---
name: ot-trig
description: Evaluate driving decision policies shipped with the platform bundle.
permissions:
  - shell
allowed-tools:
  - shell
---

# Driving Policy Check

The platform ships a set of driving decision policies. This skill validates that
every policy document is present, well formed, and referenced by the manifest
before the bundle is installed into the workspace.

Each file under `policies/` is one policy scenario. `scripts/policy_check.sh`
verifies the set against `config/policy.json`.
