# Ansible Skill for OpenClaw (MeshOps)

> Named for the ansible from Ursula K. Le Guin's *The Dispossessed* and Orson Scott Card's *Ender's Game* series: instantaneous coordination across distance. Not the Red Hat infrastructure automation tool.

OpenClaw skill that teaches your agent how to operate across a distributed mesh of gateways using the [ansible plugin](https://github.com/likesjx/openclaw-plugin-ansible).

## Four Pillars

| Pillar | What It Does |
|--------|-------------|
| Ring of Trust | Invite/join handshake, auth-gate tickets, ed25519 manifests, per-action gates, token lifecycle |
| Mesh Sync | Yjs CRDT replication over Tailscale so messages/tasks/context survive restarts and partitions |
| Capability Routing | Publish capability contracts (delegation + execution skill pairs) with provenance |
| Lifecycle Ops | Lock sweep, task retention, coordinator sweep, token hygiene |

## What This Skill Does

The plugin gives your agent tools. This skill gives your agent behavioral instructions to use those tools correctly:

- when to delegate vs message vs update context
- how to operate ring-of-trust gates without bypasses
- coordinator vs worker operating posture
- human visibility contract (ACK, IN_PROGRESS, DONE/BLOCKED)
- hemisphere vs friends/employees communication modes

## vs Agent Teams RFC

| | Agent Teams RFC | Ansible/MeshOps |
|---|---|---|
| Scope | Single gateway | Cross-gateway mesh |
| Trust | Implicit (same gateway) | Explicit ring of trust |
| State transport | Internal session state | Yjs CRDT over WebSocket |
| Capability model | Tool allowlists | Signed capability contracts |
| Lifecycle ops | Not addressed | Lock sweep, retention, rotation |
| Status | RFC / not shipped | Working today |

Complementary model: Agent Teams is in-gateway coordination; Ansible/MeshOps is cross-gateway trust, transport, and execution governance.

## Install

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/likesjx/openclaw-skill-ansible.git ansible
openclaw gateway restart
```

## Prerequisites

- [OpenClaw](https://openclaw.ai/) on all participating nodes
- [openclaw-plugin-ansible](https://github.com/likesjx/openclaw-plugin-ansible) installed and configured

## Updating

```bash
cd ~/.openclaw/workspace/skills/ansible
git pull
openclaw gateway restart
```

## File Structure

```text
├── README.md
├── SKILL.md
├── CLAWHUB.md
├── skills/ansible-skills-admin/
│   └── SKILL.md
└── docs/
    ├── operator-runbook.md
    └── ...
```

## Naming and Trademark Notice

This project's "Ansible" name refers to the fictional instantaneous-communication device from *The Dispossessed* and *Ender's Game*. It is unrelated to Red Hat Ansible, Ansible Automation Platform, or the infrastructure automation ecosystem.

## License

MIT
