---
name: ansible
description: MeshOps distributed coordination mesh for OpenClaw gateways: ring-of-trust admission, CRDT-synced state, capability-contract routing, and governed delegation. Named for the ansible from Ender's Game, not the infrastructure tool.
---

# Ansible - MeshOps Coordination Skill

## What This Is

Ansible is a distributed coordination layer that lets you operate across multiple OpenClaw gateways as one coordinated mesh.

Four pillars:

1. Ring of Trust: invite/join handshake, auth-gate WebSocket tickets, ed25519-signed capability manifests, per-action safety gates, and token lifecycle.
2. Mesh Sync: Yjs CRDT replication over Tailscale. Messages, tasks, context, and pulse remain durable across reconnects and restarts.
3. Capability Routing: publish/unpublish capability contracts. Each contract references a delegation skill (requester) and an execution skill (executor).
4. Lifecycle Ops: lock sweep, retention/pruning, coordinator sweep, and deployment hygiene.

## Relationship Modes

- Friends/Employees (default): other nodes are different agents. Provide context and communicate explicitly.
- Hemispheres (advanced): mirrored instances of the same identity. Shared intent and direct communication.

Default to Friends/Employees unless explicitly told a node is a hemisphere.

## Node Topology

- Backbone: always-on nodes (VPS/servers) that host Yjs WebSocket.
- Edge: intermittent nodes (laptops/desktops) that connect to backbone.

## Human Visibility Contract (Required on Pickup)

When taking coordination work, maintain explicit lifecycle updates:

1. ACK: confirm receipt and summarize intent.
2. IN_PROGRESS: emit progress updates at meaningful checkpoints.
3. DONE or BLOCKED: close with evidence, next action, and owner.

Use `conversation_id` consistently for all related updates.

## Ring of Trust - Behavioral Rules

- Unknown nodes require invite-based admission. Do not bypass.
- High-risk capability publishes require human approval artifacts.
- Respect caller gates (`OPENCLAW_ALLOWED_CALLERS`) and high-risk flags.
- Never expose tokens in plaintext messages/logs/shared state.
- When signature enforcement is on, only accept manifests signed by trusted publisher keys.

## Gateway Compatibility Contract

- Validate plugin is installed and readable before assuming tool availability.
- Verify tier assumptions (backbone vs edge) before mutating coordination settings.
- Treat gateway runtime as source of truth for active topology and health.

## Reliability Model

### Source of Truth

Shared Yjs state is authoritative.

### Delivery Semantics

- Durable: messages/tasks persist in shared state.
- Auto-dispatch: best-effort realtime injection into sessions.
- Heartbeat reconcile: periodic rescan recovers missed injections.
- Retry: transient dispatch failures retry with bounded backoff.
- Send receipts: notify configured operators when work is placed on mesh.

### Operating Rules

- Verify pending work with `ansible_status` and `ansible_read_messages`.
- If polling mode is used, always reply via `ansible_send_message`.
- Use `corr:<messageId>` for thread continuity.
- Listener behavior is optimization; sweep/reconcile is the backstop.

## Capability Contracts

- A capability is a contract, not just a label.
- Contract includes delegation and execution skill references.
- Publishing updates routing eligibility mesh-wide.
- Provenance is verified against trusted publisher keys when configured.
- High-risk contracts require explicit approval artifacts.
- Unpublish removes eligibility immediately.
- Lifecycle evidence must capture install/wire outcomes.

## Delegation Protocol

1. Requester creates task with objective, context, acceptance criteria, and target policy (`to_agents` or capability).
2. Executor claims task and sends acceptance/ETA signal.
3. Executor performs work, emits progress, and completes with structured result.
4. Requester reports final outcome to human and/or downstream agents.

## Coordinator Behavior

- Run sweep loops for stale locks, SLA drift, and backlog reconciliation.
- Prefer record-only escalation by default when blast radius is unclear.
- If DEGRADED, prioritize containment, visibility, and deterministic recovery.

## Available Tools

### Communication

| Tool | Purpose |
|------|---------|
| `ansible_send_message` | Send targeted or broadcast message across mesh |
| `ansible_read_messages` | Read unread messages (or full history) |
| `ansible_mark_read` | Mark messages as read |
| `ansible_delete_messages` | Admin-only emergency purge |

### Task Delegation

| Tool | Purpose |
|------|---------|
| `ansible_delegate_task` | Create task for another node/agent set |
| `ansible_claim_task` | Claim pending task |
| `ansible_update_task` | Update task status/progress |
| `ansible_complete_task` | Complete task and notify requester |
| `ansible_find_task` | Resolve task by ID/title |

### Context and Status

| Tool | Purpose |
|------|---------|
| `ansible_status` | Mesh health, unread, pending, and topology summary |
| `ansible_update_context` | Update shared context/threads/decisions |

### Coordination and Governance

| Tool | Purpose |
|------|---------|
| `ansible_get_coordination` | Read coordinator configuration |
| `ansible_set_coordination_preference` | Set node coordinator preference |
| `ansible_set_coordination` | Switch coordinator (guarded) |
| `ansible_set_retention` | Configure closed-task retention/pruning |
| `ansible_get_delegation_policy` | Read delegation policy plus ACKs |
| `ansible_set_delegation_policy` | Publish/update delegation policy |
| `ansible_ack_delegation_policy` | Acknowledge policy version |
| `ansible_lock_sweep_status` | Inspect lock sweep health |

### Capability Lifecycle

| Tool | Purpose |
|------|---------|
| `ansible_list_capabilities` | List published capability contracts |
| `ansible_capability_publish` | Publish/upgrade capability contract |
| `ansible_capability_unpublish` | Remove capability from routing |
| `ansible_capability_lifecycle_evidence` | Show install/wire evidence for version |
| `ansible_capability_health_summary` | Show success/error/latency summary |

## When to Use Ansible

Use Ansible when work crosses gateways, needs durable coordination, or requires auditable delegation contracts.

## Session Behavior

- Start by checking status and pending work.
- Prefer explicit delegation for capability-matched work.
- Keep humans in loop via lifecycle messages.

## Message Protocol v1

- Always include enough context for independent execution.
- Use stable correlation IDs (`corr`) and conversation IDs.
- Prefer structured payloads over freeform-only messaging.

## Setup Playbooks

Follow plugin setup and gateway runbooks for topology bootstrap, auth-gate, and trust settings.

## Delegation Management

- Keep delegation policy current and acknowledged across nodes.
- Treat capability publishes as contract releases.
- Roll back quickly when lifecycle evidence indicates drift or misfire.
