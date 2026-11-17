---
name: jep-guard
version: 3.0.0
description: Configure or inspect a local execution policy gate when the user requests JEP Guard protection.
---

Read README.md for the trust model, key provisioning and breaking migration requirements. Install with the lockfile and build locally. Starting the daemon and integrating execution hooks are explicit operator actions. Do not automatically change another runtime, approve commands, start background services, delete state or enable optional integrations.

Full mode only allows authenticated, policy-approved requests with valid bound capabilities. Passive mode does not protect execution. This is a local repair candidate with pending IPC and OpenClaw integration verification, not a security certification. Old cross-skill forwarding and external kernel integrations are disabled. Audit storage is local and must be protected and archived by the operator.
