# Hook Manifest

version: 1
type: skill
entry: scripts/diagnose.js
compatibility:
  min_openclaw: "2026.3.0"
  max_openclaw: "2026.4.0"
permissions:
  - node:exec
  - system:cron
description: "Node Connection Doctor - Diagnose and fix OpenClaw node connection issues"
