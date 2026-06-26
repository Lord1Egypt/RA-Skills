# Device Details Tabs and Tools

Device Details is the single-pane operational console for one endpoint.

## Core tabs

- **Overview**: active issues, system info, patch summary, process/service snapshots, ticket summaries.
- **Tools**: direct support actions without full remote control session.
- **Monitoring**: service state, rule/task/notification associations (associations are read-only), service template bindings.
- **Asset**: hardware/software inventory.
- **Notes**: technician notes and context.
- **Settings**: properties, local agent, monitoring options, downtime/maintenance windows, security, patching, backup, custom details.
- **Remote Control Settings**: enable/configure remote access capability.
- **Reports**: device-level reporting outputs.
- **Backup Dashboard**: backup status and health.

## Upper-right quick actions

- **Remote control menu** (enabled state required).
- **Task/config menu** (scheduled tasks, patch, maintenance windows).
- **Audit trail** (action history, searchable).
- **PSA/ticket menu** where integration is enabled.

## Tools tab capability matrix

Availability depends on OS, installed agent/features, and role permissions.

### Typical Windows toolset

- Services (Windows service control)
- Processes (review/start/end)
- Registry
- Applications (install/patch actions)
- Startup Applications
- Printers/queues
- Command Prompt / command line
- File System manager
- Task Execution (run script/automation policy on demand)

### Typical macOS toolset

- Processes
- Command Line
- File System manager
- Task Execution (script/automation policy where supported)

## Monitoring tab details

- **Status**: service-level health and direct service drilldown.
- **Associations**: linked rules/scheduled tasks/notifications (read-only context).
- **Service Templates**: template associations and per-template drilldown.

## Settings tab details

- Device properties (name, address, class, OS, license mode)
- Local agent status/config
- Monitoring options (e.g., SNMP/VMware/backup-related options)
- Downtime + maintenance window settings
- Security Manager settings
- Patch Management settings
- Backup Management settings
- NetPath/custom details (where enabled)

## Operational playbooks from Device Details

### Fast remediation loop
1. Overview: identify active issue.
2. Monitoring: locate failing service + linked associations.
3. Tools: run focused remediation command/policy.
4. Settings: adjust persistent configuration if root cause is policy/config.
5. Audit trail + notes: document action and verify recovery.

### Patch exception handling
1. Review patch summary on Overview.
2. Check Patch Management settings.
3. Launch targeted patch task from quick menu.
4. Confirm service states and ticket closure criteria.

### Backup incident triage
1. Check Backup Dashboard status.
2. Verify Backup Management configuration.
3. Trigger backup/export task if needed.
4. Document outcome in Notes and audit trail.

## Why actions may be unavailable

- Feature/agent not installed.
- Device OS not supported for that tool.
- Task type restricted to higher scope.
- Managed product/license not enabled.
- Role/permission restrictions.
