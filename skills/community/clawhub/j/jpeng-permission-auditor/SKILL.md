---
name: permission-auditor
description: Audit tool usage patterns and permissions to identify security risks and excessive access. Use when you need to review tool usage, check for permission issues, or generate security audit reports.
---

# Permission Auditor

Review tool usage and permissions.

## Usage

```javascript
const { auditToolUsage, checkPermissions, generateReport } = require('./skills/permission-auditor');

// Audit tool usage from logs
const audit = auditToolUsage(toolLogs);

// Check if permissions are excessive
const issues = checkPermissions(requiredPermissions, grantedPermissions);

// Generate security report
const report = generateReport(audit);
```

## CLI

```bash
node skills/permission-auditor/index.js demo
```

## Features

- Tool usage pattern analysis
- High-risk operation detection
- Permission scope verification
- Security recommendations
- Audit report generation
