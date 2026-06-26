# Heartbeat Recipes - Google Reviews

Use these cadence patterns as defaults, then tune by risk and volume.

## Cadence Profiles

| Profile | Heartbeat | Deep Report | Best For |
|---------|-----------|-------------|----------|
| Watch | Every 12h | Weekly | Low volume brands |
| Balanced | Every 6h | Twice weekly | Most SMB monitoring |
| Critical | Every 1-2h | Daily | High-stakes launches or incidents |

## Heartbeat Payload

Keep each heartbeat cycle lightweight:
- New review count by brand/source
- Rating deltas vs baseline
- Negative-review spike detection
- Connector health status

If no meaningful change, emit compact no-change status and skip long narrative.

## Cooldown Rules

- Default duplicate-alert cooldown: 24h per brand + theme pair.
- Escalate immediately if severity upgrades from medium to high.
- Reset cooldown when a new root-cause theme appears.

## Failure Handling

When one source fails:
1. Mark source `degraded`
2. Continue healthy sources
3. Add outage note to the report
4. Retry on next cycle with bounded attempts
