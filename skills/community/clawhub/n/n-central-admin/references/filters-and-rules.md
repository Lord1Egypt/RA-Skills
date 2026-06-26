# Filters and Rules

## Filters: targeting engine

Filters define *which devices* match criteria (OS, class, hardware/software, custom properties, etc.). They are reusable across rules, dashboards, and tasks.

## Filter construction

- Start with baseline dimensions: customer/site, device class, OS family.
- Add operational dimensions: role, patch group, custom property tags.
- Use advanced expressions for precision.

### Expression logic

- Supported boolean logic: `AND`, `OR`.
- Group with parentheses for precedence.
- Criteria variables can be A-Z, a-z, or single digits.
- Example: `(A AND B) OR (C AND D) OR (1 AND 2)`.

## Rule system: automation core

Rules are buckets that collect devices from one or more filters and trigger configured actions.

### Rule-triggering events (key behavior)

Rules can reevaluate/apply on events such as:
- device import,
- asset updates relevant to filter fields,
- first agent install on existing device,
- feature enable/disable,
- license mode change,
- rule update,
- new customer association,
- primary property changes (class/OS/etc).

### Rule tabs/sections to configure

- **Devices to Target**: choose one or more filters.
- **Install/Features**: install required managed features where applicable.
- **Tasks**: automation/scheduled actions tied to matching devices.
- **Notification**: assign notification profile.
- **Grant/Propagation**: control where rule is applied.

### Multi-filter behavior

When multiple filters are selected in a rule, matching is effectively **OR** between filters.

### Dual-list selector behavior (Devices to Target and similar fields)

In rule configuration and other assignment dialogs, N-central often uses left/right selector lists.

- `>`: add highlighted item(s) to the selected (right) list.
- `>>`: add all currently listed items to the selected (right) list.
- `<`: remove highlighted item(s) from the selected (right) list.
- `<<`: remove all currently listed items from the selected (right) list.

Treat `>>` and `<<` as bulk actions and verify resulting target counts before save.

### Rule visibility modes

- **Public rule**: broadly visible/editable per role hierarchy.
- **Private rule**: visible to creator and higher permissions; admins may not view each other's private rules.

## Infinite-loop prevention

Some monitoring-service-related filters are excluded from add/remove service operations in rules to prevent recursive loops. If expected filter is missing, check loop-protection exclusions.

## Rule-not-firing checklist

1. Verify scope and grants (SO/Customer/Site).
2. Verify filter actually matches intended devices right now.
3. Verify filter fields include attributes changed by incoming events.
4. Confirm features/services required by the action are installed.
5. Confirm rule not blocked by excluded loop-prone filters.
6. Check associations on a target device (Monitoring tab) and audit logs.
7. Trigger a safe reevaluation event if needed (minor rule edit/save).

## Filter/rule design patterns

- **Pilot + promote**: validate on one site, then clone/propagate.
- **One intent per rule**: avoid giant mixed-purpose rules.
- **Explicit ownership**: include owner/team in description.
- **Date/version stamp**: include revision token in description for change tracking.
