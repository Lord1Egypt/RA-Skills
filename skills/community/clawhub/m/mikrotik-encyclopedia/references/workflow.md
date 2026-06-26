# MikroTik Encyclopedia Workflow

## Core stance

Use official MikroTik docs plus local observed state together.

Default order:
1. check `.MikroTik-Encyclopedia/` cache/notes
2. check official docs when needed
3. inspect live device state
4. answer or act
5. record durable learnings

## When docs lookup is mandatory

Do a docs lookup before answering or acting when any of these are true:
- the user asks about RouterOS command syntax or feature semantics
- the task involves firewall, NAT, bridge, VLAN, CAPsMAN, routing, DHCP, DNS, queues, or management services
- the task involves a version-sensitive feature or a behavior you are not highly confident about
- the task involves live SSH/API access and the command path or safety boundaries matter

## Cache-first rule

Before fetching docs, check whether the needed material already exists under:
- `.MikroTik-Encyclopedia/docs/help.mikrotik.com/docs/...`
- `.MikroTik-Encyclopedia/notes/devices/...`
- `.MikroTik-Encyclopedia/notes/patterns/...`
- `.MikroTik-Encyclopedia/inventory/...`

If the local cache is good enough, use it.
If not, fetch/check the official docs and then cache what you used.

## How to cache docs

Use `scripts/cache_doc.py`.

Typical usage:

```bash
python3 scripts/cache_doc.py \
  --url 'https://help.mikrotik.com/docs/display/ROS/Filter' \
  --root '<workspace>/.MikroTik-Encyclopedia'
```

The script will:
- fetch the page
- convert it into a normalized markdown-ish cache file
- place it under `.MikroTik-Encyclopedia/docs/help.mikrotik.com/docs/...`
- add metadata such as source URL and fetch timestamp

## How to store local knowledge

### Device notes

Use `.MikroTik-Encyclopedia/notes/devices/<device-name>.md` for:
- device purpose
- management access path
- role in topology
- sensitive boundaries
- discovered quirks

### Pattern notes

Use `.MikroTik-Encyclopedia/notes/patterns/<topic>.md` for:
- recurring RouterOS command patterns
- repeated gotchas
- safe command sequences
- environment-specific design conventions

### Inventory files

Use `.MikroTik-Encyclopedia/inventory/` for:
- topology
- access inventory
- documentation index

## Distinguish evidence types

When writing notes, label information mentally as one of:
- **Official docs** — from MikroTik documentation
- **Observed local state** — from live device inspection
- **Inference/recommendation** — your judgment based on docs + local state

Do not blur these together.

## Recommended answer style

When it helps, mention whether your answer is based on:
- cached official docs
- freshly checked official docs
- live device inspection
- best-practice inference

## High-sensitivity areas

Treat these as high-sensitivity even when you have live access:
- edge firewall/router changes
- CAPsMAN or wireless policy changes
- bridge/VLAN changes
- DNS/DHCP changes
- management-service exposure
- changes that could strand access

For these, prefer docs lookup even if you think you remember the command.
