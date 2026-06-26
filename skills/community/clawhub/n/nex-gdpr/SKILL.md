---
name: nex-gdpr
description: GDPR and AVG (Belgian data protection law) compliance handler for agency operators, data controllers, and organizations managing data subject requests. Register and manage all types of data subject requests (inzageverzoek, verwijderverzoek, recht op gegevensoverdracht) as required under GDPR Articles 15-21 and Belgian AVG regulations. Automatically scan and discover personal data across OpenClaw sessions, agent memory, application logs, and skill databases. Process Right of Access requests by compiling complete personal data exports in machine-readable formats. Handle Right of Erasure requests with secure 3-pass file deletion and audit logging. Support Right to Data Portability with JSON format exports. Generate compliant response letters in both Dutch (AVG) and English (GDPR) with formal documentation. Track 30-day legal response deadlines with extension options for complex requests. Maintain immutable audit trails of every action taken on data subject requests for regulatory compliance and dispute resolution. Manage data retention policies and auto-cleanup schedules. Perfect for Belgian agencies, service providers, and organizations operating under GDPR/AVG who need systematic compliance processes.
version: 1.0.0
metadata:
  clawdbot:
    emoji: "🛡"
    requires:
      bins:
        - python3
      env:
        - OPENCLAW_SESSIONS
        - NEX_GDPR_SCAN_PATHS
    primaryEnv: ""
    homepage: https://nex-ai.be
    files:
      - "nex-gdpr.py"
      - "lib/*"
      - "setup.sh"
---

# Nex GDPR

GDPR Data Request Handler for agency operators running OpenClaw for clients. Automate compliance with data subject rights (Articles 15-21 of GDPR/AVG). Register requests, scan for personal data, process erasure/access/portability, generate response letters, and maintain audit trails.

## When to Use

Use this skill when you need to:

- **Register and manage GDPR data subject requests** (inzageverzoek, verwijderverzoek, etc.)
- **Process Right to Access requests** (Article 15 - inzagerecht): Locate all personal data and compile export packages
- **Process Right to Erasure requests** (Article 17 - verwijderrecht): Identify and securely delete personal data
- **Process Right to Data Portability requests** (Article 20 - recht op gegevensoverdracht): Export in machine-readable format
- **Process Right to Rectification requests** (Article 16 - recht op correctie): Track and apply corrections
- **Track Right to Restriction of Processing** (Article 18 - recht op beperking)
- **Handle Right to Object** (Article 21 - recht van verzet)
- **Scan for personal data** across OpenClaw sessions, logs, and databases
- **Generate compliance response letters** in Dutch and English
- **Maintain audit trails** for every action taken
- **Monitor compliance deadlines** (30-day GDPR response deadline)
- **Manage data retention policies** and auto-cleanup
- **Export compliance reports** for documentation

Trigger phrases: "GDPR request", "data subject request", "inzageverzoek", "verwijderverzoek", "right to access", "right to erasure", "data portability", "personal data", "PII", "AVG", "persoonsgegevens", "erasure request", "portability request", "how many GDPR requests", "overdue requests", "audit trail", "compliance documentation"

Example use cases:
- "Register a new GDPR access request for jan@example.be"
- "Scan for all data related to jan@example.be"
- "Process the access request for request #42"
- "Which GDPR requests are overdue?"
- "Generate a response letter for the Jan Peeters request"
- "Show the audit trail for request #42"
- "Export compliance report for request #42"
- "Show GDPR statistics and compliance status"

## Quick Setup

If the database does not exist yet, run the setup script:

```bash
bash setup.sh
```

This creates the data directory, installs dependencies, and initializes the database.

## Available Commands

### Request Management

**Register a new request:**
```bash
nex-gdpr new --type access --name "Jan Peeters" --email "jan@example.be" --id "user_jan_123"
```

Request types: `ACCESS`, `ERASURE`, `PORTABILITY`, `RECTIFICATION`, `RESTRICTION`, `OBJECTION`

**List all requests:**
```bash
nex-gdpr list
nex-gdpr list --status VERIFIED
nex-gdpr list --type ERASURE
```

**Show request details:**
```bash
nex-gdpr show 42
```

Shows request status, deadline, findings, and audit trail.

### Data Discovery & Scanning

**Scan for user data:**
```bash
nex-gdpr scan "jan@example.be"
nex-gdpr scan --request 42
```

Scans OpenClaw sessions, agent memory, logs, and databases for personal data.

**Show findings for a request:**
```bash
nex-gdpr findings 42
```

### Request Processing

**Process a request:**
```bash
nex-gdpr process 42
```

Automatically:
- Scans for all user data
- For ACCESS: Creates export ZIP package
- For ERASURE: Securely deletes personal data (with logging)
- For PORTABILITY: Exports machine-readable JSON format
- Marks request as COMPLETED

**Verify request identity:**
```bash
nex-gdpr verify 42 --method "email confirmation"
```

**Deny a request:**
```bash
nex-gdpr deny 42 --reason "Identity could not be verified"
```

**Complete a request:**
```bash
nex-gdpr complete 42
```

### Compliance & Monitoring

**Show overdue requests:**
```bash
nex-gdpr overdue
```

Highlights requests past the 30-day GDPR response deadline.

**Generate response letter:**
```bash
nex-gdpr letter 42
```

Outputs formal response letter in Dutch and English (Article 15-21 compliant).

**Export compliance report:**
```bash
nex-gdpr export 42
```

Exports complete request report (JSON) with findings and audit trail.

**Show audit trail:**
```bash
nex-gdpr audit 42
```

Displays all actions taken on the request (verification, processing, approvals).

**Show GDPR statistics:**
```bash
nex-gdpr stats
```

Displays request counts by status/type, overdue requests, PII findings, and data volumes.

### Data Retention

**Show retention policies:**
```bash
nex-gdpr retention show
```

**Set retention policy:**
```bash
nex-gdpr retention set --type sessions --days 180 --auto-delete
```

**Run cleanup:**
```bash
nex-gdpr cleanup --dry-run
nex-gdpr cleanup --execute
```

## Architecture

### Storage
- **SQLite Database** at `~/.nex-gdpr/gdpr.db`
- Tables: `requests`, `data_findings`, `audit_trail`, `retention_policies`
- Indexes on status, type, deadline for fast queries

### Data Scanning
- **OpenClaw Sessions**: Scans `.openclaw/sessions` and `.claw/sessions`
- **Agent Memory**: Scans `.nex-memory` directory
- **Logs**: Scans `.nex-logs` for user references
- **Other Databases**: Scans other nex-* skill databases
- **PII Detection**: Email, phone, national numbers, VAT numbers

### Request Processing
- **ACCESS**: Creates ZIP export of all found data
- **ERASURE**: Securely deletes files (3-pass overwrite)
- **PORTABILITY**: Exports JSON format with metadata
- **RECTIFICATION**: Tracks corrections to personal data
- All actions logged with timestamps and actor information

### Compliance
- **30-day Response Deadline**: Automatically calculated from GDPR Article 12
- **60-day Extension**: For complex requests (logged and tracked)
- **Audit Trail**: Every action recorded (scanning, verification, processing, completion)
- **Response Letters**: Generated in Dutch (AVG) and English (GDPR)
- **Retention Policies**: Configurable per data type (default 1 year, audit 7 years)

## Data Locations Scanned

The scanner searches the following locations for personal data:
- `~/.openclaw/sessions` - OpenClaw session files
- `~/.claw/sessions` - Alternative Claw sessions
- `~/.nex-memory` - Agent memory files
- `~/.nex-logs` - Application logs
- `~/.nex-uploads` - Uploaded files
- Other nex-* skill databases (life-logger, inbox, notes, etc.)

Configurable via environment variables:
```bash
export OPENCLAW_SESSIONS="/custom/sessions/path"
export NEX_GDPR_SCAN_PATHS="/path1:/path2:/path3"
```

## GDPR Articles Supported

- **Article 15**: Right of access by the data subject
- **Article 16**: Right to rectification
- **Article 17**: Right to erasure (right to be forgotten)
- **Article 18**: Right to restrict processing
- **Article 20**: Right to data portability
- **Article 21**: Right to object

## Privacy & Security

- All personal data exports are encrypted and stored in `~/.nex-gdpr/exports/`
- Erasure operations use secure deletion (3-pass overwrite)
- Audit trail cannot be modified (append-only)
- All operations require explicit status changes
- No automatic external sharing (all data stays local)

## Configuration

Configuration is stored in `lib/config.py`:
- `DATA_DIR`: `~/.nex-gdpr` (customizable)
- `RESPONSE_DEADLINE_DAYS`: 30 (GDPR requirement)
- `EXTENSION_DAYS`: 60 (for complex requests)
- `DEFAULT_RETENTION_DAYS`: 365 (1 year default)

## Exit Codes

- `0`: Success
- `1`: Error or validation failure

## Notes

- Designed for agency operators managing multiple clients under GDPR
- All timestamps are ISO 8601 format with timezone
- Data findings include PII detection (email, phone, national numbers)
- Retention cleanup is manual (scheduled via cron or trigger command)
- Export packages are ZIP files with manifest and data files
- Responses are compliant with Belgian GDPR (AVG) regulations

## Support

For issues or questions:
- Homepage: https://nex-ai.be
- License: MIT-0 (free and open source)
