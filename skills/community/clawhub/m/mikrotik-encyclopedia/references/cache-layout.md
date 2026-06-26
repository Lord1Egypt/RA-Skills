# `.MikroTik-Encyclopedia/` Cache Layout

Use this directory as the workspace-local data root for the skill.

## Directory tree

```text
.MikroTik-Encyclopedia/
  docs/
    help.mikrotik.com/
      docs/
        ... cached official docs pages ...
  notes/
    devices/
      ... per-device notes ...
    patterns/
      ... reusable RouterOS notes ...
  inventory/
    access.md
    topology.md
    doc-index.md
```

## Placement rules

### `docs/`
Store cached copies of official MikroTik docs here.

Mirror the official docs path as much as practical.
Example:

```text
https://help.mikrotik.com/docs/display/ROS/Filter
->
.MikroTik-Encyclopedia/docs/help.mikrotik.com/docs/display/ROS/Filter.md
```

### `notes/devices/`
Store environment-specific device notes here.

Suggested filenames:
- `server-room-main-mikrotik-poe-firewall.md`
- `livingroom-mikrotik-rb5009-switch-and-mini-docker-host.md`
- `server-room-mikrotik-wifi-access-point.md`

### `notes/patterns/`
Store reusable operational notes here.

Examples:
- `firewall-input-review.md`
- `capsman-basics.md`
- `bridge-vlan-gotchas.md`
- `service-exposure-checklist.md`

### `inventory/`
Store environment-wide inventories here.

Suggested files:
- `access.md`
- `topology.md`
- `doc-index.md`

## Cache philosophy

Do not mirror the whole docs site eagerly.
Cache only the pages you actually consulted and expect to be useful later.
