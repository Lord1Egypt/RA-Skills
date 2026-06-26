# UI Navigation and Operating Model

## N-central hierarchy (mental model)

- **Service Organization (SO)**: top-level MSP scope.
- **Customer**: client organization.
- **Site**: location/subdivision under customer.
- **Device**: monitored endpoint, server, network device, mobile/cloud resource.

Operate from the narrowest scope possible unless intentionally making global changes.

## Primary UI areas

- **Configuration**: rules, filters, monitoring templates, scheduled tasks, notifications, repository artifacts.
- **Devices**: inventory and per-device details/actions.
- **Monitoring/Dashboards**: status and health views.
- **Patch/Security/Backup areas**: workload-specific controls.

## Left navigation path map (common admin tasks)

Use this path format for click guidance: `Area > Sub-area > Page`.

- `Configuration > Monitoring > Rules`: create/edit rules, grants, and target bindings.
- `Configuration > Filters`: build/test reusable targeting filters.
- `Configuration > Monitoring > Service Templates`: manage monitoring template baselines.
- `Configuration > Monitoring > Notifications`: assign notification profiles and escalation behavior.
- `Configuration > Scheduled Tasks > Add/Delete`: create/run one-time or recurring tasks, including Automation Policy tasks.
- `Configuration > Scheduled Tasks > Profiles`: manage reusable task profiles that rules can apply.
- `Configuration > Scheduled Tasks > Script/Software Repository`: manage policy/script artifacts used by tasks.
- `Views > All Devices` (label may vary): find endpoints and open Device Details for per-device tools/actions.

Navigation notes:
- Exact left-nav labels vary by N-central version, enabled modules, and role permissions.
- If a path is missing, verify scope first (SO/Customer/Site), then confirm role permissions.

## Canonical workflows

### Onboard and monitor new device classes
1. Build target filter.
2. Build/clone service template.
3. Create rule binding filter + template + notifications.
4. Grant/propagate appropriately.
5. Validate on sampled devices.

### Run maintenance/remediation at scale
1. Select policy/script/task type.
2. Target via explicit device set or filter snapshot.
3. Schedule with timezone/offline settings.
4. Track run state and verify outcomes.

### Incident response on one device
1. Open Device Details.
2. Use Overview + Monitoring for symptom triage.
3. Use Tools tab (process/service/command/file/task execution).
4. Record notes and close with validation proof.

## Permissions and ownership behavior

- Rules and filters are account-based; higher permission levels can generally edit lower-level artifacts.
- Default/system filters are not editable; clone first.
- If an object is grayed out at lower scope, it may have been created at a higher level.

## Recommended naming convention

`<scope>-<platform/group>-<intent>-<frequency>`

Examples:
- `SO-WindowsServers-PatchCycle-Weekly`
- `CUSTA-Laptops-AVQuickScan-Daily`
- `SITE3-NetworkDevices-SNMPBaseline-Monthly`

## Change control checklist

- Confirm scope level.
- Confirm target preview count and composition.
- Confirm notifications/ticketing side effects.
- Confirm rollback path (disable rule, unschedule task, remove template association).
- Capture audit note (who/why/when).
