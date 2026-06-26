# ClawHub Listing Source

Use this file as the canonical source for marketplace listing text.

## Display Name

MeshOps Control Plane

## Short Description

Distributed agent mesh for OpenClaw: ring-of-trust admission, CRDT-synced coordination across gateways, capability-contract routing, and governed task delegation.

## Long Description

MeshOps Control Plane (internally powered by the Ansible plugin) provides a secure, durable coordination layer for multi-gateway OpenClaw systems.

Core pillars:

1. Ring of Trust: invite and join handshake, auth-gate tickets, token lifecycle, and optional signature enforcement for capability manifests.
2. Mesh Sync: Yjs CRDT replicated state over Tailscale for resilient cross-node messages, tasks, and context.
3. Capability Contracts: publish and unpublish explicit delegation plus execution skill pairs with provenance and lifecycle evidence.
4. Lifecycle Operations: lock sweeper, retention policies, coordinator sweeps, receipts, and escalation controls.

This is the "ansible" from science fiction (one mind, many bodies), not the infrastructure automation product.

## Safety and Governance Highlights

- High-risk operations remain explicitly gated and caller-restricted.
- Approval artifacts are required for high-risk capability publishes.
- Durable shared state plus heartbeat reconcile protects against missed dispatch.
- Operator visibility contract (ACK, IN_PROGRESS, DONE/BLOCKED) is part of the skill behavior.

## Intended Audience

OpenClaw operators managing distributed agent systems across multiple gateways who need explicit trust controls, durable routing, and auditable delegation.
