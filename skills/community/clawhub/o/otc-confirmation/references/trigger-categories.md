# OTC Trigger Categories

This document defines which operations require OTC confirmation.

## Category 1: External Operations

Operations that leave the machine or are visible to others:

- **Email**: Sending emails via any method (SMTP, CLI tools, API)
- **Social Media**: Posting to Twitter/X, Facebook, LinkedIn, etc.
- **Messaging**: Sending messages to external chat platforms
- **API Calls**: POST/PUT/DELETE requests to third-party services
- **File Uploads**: Uploading files to cloud storage or public servers
- **Webhooks**: Triggering external webhooks or notifications

## Category 2: Dangerous Local Operations

Operations that are destructive or hard to reverse:

- **File Deletion**:
  - Recursive force deletion of directories
  - Bulk file removal operations
  - Deleting entire project or data directories

- **System Configuration**:
  - Modifying system files under `/etc`
  - Changing system-wide settings
  - Editing firewall rules
  - Modifying network configuration

- **Service Management**:
  - Stopping critical services
  - Restarting production services
  - Disabling system daemons

- **Permission Changes**:
  - Recursive permission changes on directories
  - Recursive ownership changes

- **Disk Operations**:
  - Formatting drives
  - Partitioning disks
  - Mounting/unmounting filesystems

## Category 3: Security Rule Modifications

Operations that change the confirmation mechanism itself:

- **SOUL.md Changes**: Any edits to OTC mechanism, trigger conditions, or email configuration
- **AGENTS.md Changes**: Modifications to security rules or confirmation workflows
- **OTC Configuration**: Changes to openclaw.json OTC settings
- **Access Control**: Modifying user permissions or authentication rules

## Category 4: Absolute Denials (No OTC Offered)

Operations that are too dangerous to allow even with confirmation.
These are **always refused outright** — no confirmation code is offered:

- Wiping or formatting system drives
- Deleting root-level system directories
- Overwriting boot sectors or partition tables
- Any irreversible operation that would render the system unbootable

## Decision Examples

### Requires OTC ✅

- Sending an email to a colleague
- Deleting an old project directory
- Restarting a web server
- Modifying the OTC configuration itself

### Does NOT Require OTC ❌

- Reading files or listing directories
- Creating new files or folders
- Copying or backing up files
- Running diagnostic commands (ps, df, etc.)

### Absolute Denial 🚫

- Wiping entire disks or system partitions
- Deleting critical OS directories
- Any command designed to destroy the system
