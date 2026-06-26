# Keyco Data Integrity Guidelines

Keyco's value proposition depends on a trustworthy audit trail. Several operations that look like ordinary CRUD are intentionally restricted.

## Operations You Should NEVER Attempt

### 1. Manually setting DUB location

There is no CLI command or API endpoint for this. DUB location is derived from:
- GPS heartbeats from Active DUBs (BLE)
- BLE gateway proximity detections
- QR/NFC scan events with device geolocation
- Explicit lifecycle events (e.g., TRANSFER)

If the user asks to "move" an asset or "update its location," the correct flow is either:
- Create a lifecycle event (`keyco lifecycles create --event-type TRANSFER ...`) documenting the move
- Trigger a physical scan at the new location
- Register a BLE gateway at the new location

### 2. Marking workflows complete out-of-band

Workflows advance only when verified DUB scan events happen in the real world. This ensures the workflow history reflects what actually occurred, not what an admin wished had occurred.

### 3. Advancing workflow steps without a scan

Same rationale as above. If a user needs to correct a workflow state, they should use the dashboard's manual-override flow (which logs an admin action in the audit log) — not the CLI.

## If a User Has a Legitimate Override Need

Direct them to: **support@keycomagix.com**

Real scenarios that require an override:
- Physical DUB tag destroyed — need to re-associate a replacement
- Incorrect initial assignment during bulk import
- Data migration from legacy system

In these cases, support can log a corrective action in the audit trail.

## What IS Safe to Automate

- Creating lifecycle events (they are themselves the audit trail)
- Assigning/unassigning DUBs to users
- Creating/deleting groups
- Running analytics
- Managing API keys, notifications, templates

These operations are fully supported via the CLI and don't bypass any integrity checks.
