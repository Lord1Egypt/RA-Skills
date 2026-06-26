# Nex GDPR - GDPR Data Request Handler

GDPR Data Request Handler for agency operators running OpenClaw for clients. Automate compliance with data subject rights (Articles 15-21 of GDPR/AVG).

## Features

- **Request Management**: Register, track, and manage GDPR data subject requests
- **Data Discovery**: Scan OpenClaw sessions, logs, and databases for personal data
- **Automated Processing**: Handle access, erasure, portability, and rectification requests
- **Compliance Documentation**: Generate response letters and audit trails
- **Deadline Tracking**: Monitor 30-day GDPR response deadlines with extension support
- **PII Detection**: Identify personal information (emails, phone numbers, national IDs)
- **Retention Policies**: Configure and auto-clean data based on retention rules
- **Secure Deletion**: Overwrite data before deletion for compliance
- **Audit Trail**: Complete history of all actions taken on requests

## Installation

```bash
bash setup.sh
```

This creates:
- Data directory at `~/.nex-gdpr`
- SQLite database at `~/.nex-gdpr/gdpr.db`
- Virtual environment with dependencies
- Executable wrapper at `~/.local/bin/nex-gdpr`

## Quick Start

Register a GDPR access request:
```bash
nex-gdpr new --type access --name "Jan Peeters" --email "jan@example.be"
```

Scan for personal data:
```bash
nex-gdpr scan --request 1
```

Process the request:
```bash
nex-gdpr process 1
```

Show request details:
```bash
nex-gdpr show 1
```

List all requests:
```bash
nex-gdpr list
```

## Request Types

Supported GDPR Articles:

| Type | Article | Description | Command |
|------|---------|-------------|---------|
| ACCESS | 15 | Right to Access | Process and export all user data |
| ERASURE | 17 | Right to Erasure | Securely delete all personal data |
| PORTABILITY | 20 | Right to Data Portability | Export in machine-readable format |
| RECTIFICATION | 16 | Right to Rectification | Correct inaccurate data |
| RESTRICTION | 18 | Right to Restrict Processing | Pause data processing |
| OBJECTION | 21 | Right to Object | Handle objections to processing |

## Request Status Lifecycle

1. **RECEIVED**: Initial state when request is registered
2. **VERIFIED**: Identity of data subject confirmed
3. **IN_PROGRESS**: Active processing of request
4. **COMPLETED**: Request processed and responded to
5. **DENIED**: Request denied with documented reason
6. **EXPIRED**: Request deadline exceeded

## Compliance

- **GDPR Article 12**: Response within 1 month of receipt (30 days)
- **GDPR Article 12.3**: Extension by 2 months for complex requests (60 days)
- **GDPR Article 13-14**: Response letter requirements
- **Dutch AVG**: Full compliance with Dutch GDPR implementation

## Data Locations Scanned

- `~/.openclaw/sessions` - OpenClaw agent sessions
- `~/.claw/sessions` - Alternative Claw format
- `~/.nex-memory` - Agent memory files
- `~/.nex-logs` - Application logs
- `~/.nex-uploads` - User uploads
- Other nex-* skill databases (life-logger, inbox, notes)

Configurable via environment variables:
```bash
export OPENCLAW_SESSIONS="/custom/path/sessions"
export NEX_GDPR_SCAN_PATHS="/path1:/path2:/path3"
```

## Architecture

### Database Schema

**requests**
- id, request_type, data_subject_name, data_subject_email, data_subject_id
- received_date, deadline_date, extended_deadline
- status, verified, verification_method
- assigned_to, response_summary, completed_at
- denied_reason, notes, created_at, updated_at

**data_findings**
- id, request_id, data_source, file_path, data_type
- size_bytes, contains_pii, action_taken, action_date, notes

**audit_trail**
- id, request_id, action, actor, details, timestamp

**retention_policies**
- id, data_type, retention_days, auto_delete, last_cleanup

### Supported PII Patterns

The scanner detects:
- Email addresses
- Phone numbers (international formats)
- Belgian national numbers (YYYYMMDD)
- Belgian VAT numbers (BE########)
- Social security numbers
- Dates in common formats

## Examples

### Process an access request
```bash
# Register request
nex-gdpr new --type access --name "Jan Peeters" --email "jan@example.be"

# Scan for data
nex-gdpr scan --request 1

# Verify identity
nex-gdpr verify 1 --method "email confirmation"

# Process and generate export
nex-gdpr process 1

# Generate response letter
nex-gdpr letter 1

# Export compliance report
nex-gdpr export 1
```

### Handle an erasure request
```bash
# Register request
nex-gdpr new --type erasure --name "John Doe" --email "john@example.be"

# Scan for data
nex-gdpr scan --request 2

# Verify identity
nex-gdpr verify 2 --method "email confirmation"

# Process erasure
nex-gdpr process 2

# Show what was deleted
nex-gdpr findings 2

# Complete request
nex-gdpr complete 2
```

### Monitor compliance
```bash
# Show overdue requests
nex-gdpr overdue

# Show statistics
nex-gdpr stats

# Export report for client
nex-gdpr export 1
```

## Security Considerations

- **Audit Trail**: All actions are logged with actor and timestamp
- **Secure Deletion**: Uses 3-pass overwrite before file deletion
- **Encryption**: Export files should be encrypted before transmission
- **Access Control**: Ensure proper file permissions on `~/.nex-gdpr`
- **Backup**: Maintain backups of audit trail for compliance
- **No External Sharing**: All data stays local by default

## Configuration

Edit `lib/config.py` to customize:

```python
# Response deadline (GDPR requirement)
RESPONSE_DEADLINE_DAYS = 30

# Extension for complex requests
EXTENSION_DAYS = 60

# Default data retention
DEFAULT_RETENTION_DAYS = 365

# Audit trail retention (7 years recommended)
RETENTION_POLICIES["audit"] = 2555

# Scan paths (add custom paths)
SESSION_DIRS = [...]
DB_FILES = [...]
```

## Troubleshooting

### Database locked error
Wait for any background operations to complete, or delete the journal file:
```bash
rm ~/.nex-gdpr/gdpr.db-journal
```

### Python module not found
Ensure virtual environment is activated:
```bash
source ~/.nex-gdpr/venv/bin/activate
```

### Permission denied on exports
Check file permissions:
```bash
ls -la ~/.nex-gdpr/exports/
chmod 700 ~/.nex-gdpr/
```

### Scan finds no data
Verify scan paths exist:
```bash
ls ~/.openclaw/sessions
ls ~/.nex-memory
```

## License

MIT-0 License - No attribution required

## Support

Homepage: https://nex-ai.be

## Citation

If you use Nex GDPR in your organization, cite as:

```
Nex GDPR. (2026). GDPR Data Request Handler for OpenClaw agencies.
Nex AI, Belgium. https://nex-ai.be
```
