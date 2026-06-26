# GrayMatter architecture

## Overview

GrayMatter is the durable memory layer for agentic workflows.

It separates into two practical operating modes:
- **Cloud** for shared production memory and graph state
- **Light** for local/offline `MemoryEntry`-first memory

That split is intentional.
It keeps the production path powerful while making the local path simple enough to run anywhere.

## Core concepts

### MemoryEntry

`MemoryEntry` is the base durable memory primitive.

Recommended durable types:
- `decision`
- `todo`
- `context`
- `artifact`
- `preference`

Design goal:
- short, explicit, reusable memory items
- not giant transcripts
- not vague chat residue

### Graph state

Graph state is the higher-order coordination layer.
Use it when relations matter, not just isolated memory entries.

Examples:
- workflow ownership
- bot coordination
- entity relationships
- operational state that links multiple objects

Recommended concurrency split:
- use `MemoryEntry` for compact facts, decisions, todos, artifacts, and handoffs
- use graph state for ownership, dependencies, and multi-object workflow coordination

## Mode 1: GrayMatter Cloud

Backed by production ValkyrAI/api-0 endpoints.

Primary endpoints:
- `/MemoryEntry`
- `/MemoryEntry/query`
- `/SwarmOps/graph`

Use cloud mode when you need:
- shared durable memory
- cross-agent coordination
- graph-backed operational state
- production auth and centralized persistence
- live schema awareness across the organization's available business objects

Default auth posture for Cloud mode:
- prompt the user once for api-0 username/password
- exchange for session
- store the session securely in macOS/iCloud Keychain
- reuse it automatically on later runs

Manual JWT handling should not be the normal user path.

## Mode 2: GrayMatter Light

A local/offline mode built around a minimal ThorAPI-powered `MemoryEntry` surface.

Target characteristics:
- minimal schema
- easy local startup
- no required external auth
- small demo/dev footprint
- straightforward upgrade path to cloud mode

## Design principles

1. **Memory first**
   Start with `MemoryEntry`. Do not overbuild graph complexity into the light path.

2. **Deterministic writes**
   Prefer short, structured, durable facts.

3. **Production and local parity where it matters**
   Keep the local model conceptually aligned with the cloud model so data and habits transfer cleanly.

4. **Graceful fallback**
   If cloud writes fail, keep a viable local/offline path.

5. **ThorAPI-native evolution**
   Use ThorAPI as the generator and schema backbone for the light path.

## Recommended repo direction

Current repo direction:
- keep the skill and shell helpers production-ready
- keep the mode split clear: hosted api-0 for Cloud, local ThorAPI for Light
- keep `gm-light-up` as the runnable GrayMatter Light local service
- keep the generated `api.hbs.yaml` template, rendered `api.yaml`, and MCP contract mapping in sync
- include query/create demos and migration notes from Light to Cloud
