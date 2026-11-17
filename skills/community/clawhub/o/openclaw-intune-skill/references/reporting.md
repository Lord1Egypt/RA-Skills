# Reporting, Audit Logs, Settings Catalog Search, GPO Analytics

Call via `scripts/graph.sh`. Tier = safety tier from SKILL.md.
Sign-in logs and directory audits require the `AuditLog.Read.All` permission
(see README permission table).

## 1. Fleet reports

| # | Report | Method & Path | Notes |
|---|---|---|---|
| 1.1 | Compliance summary | GET `/deviceManagement/managedDevices?$select=complianceState` | Aggregate client-side: X compliant, Y non-compliant, Z in grace period |
| 1.2 | OS distribution | GET `/deviceManagement/managedDevices?$select=operatingSystem` | Group by OS: "42 Windows, 15 iOS, 8 Android, 3 macOS" |
| 1.3 | Stale devices | GET `/deviceManagement/managedDevices?$filter=lastSyncDateTime lt {ISO8601}&$select=deviceName,lastSyncDateTime,userPrincipalName` | Compute the cutoff date (e.g. 30 days ago) as `2026-06-06T00:00:00Z` — always ISO 8601 UTC with `Z` |
| 1.4 | Non-compliant devices | GET `/deviceManagement/managedDevices?$filter=complianceState eq 'noncompliant'&$select=deviceName,complianceState,userPrincipalName,operatingSystem` | |
| 1.5 | Export job (async, beta) | POST `/beta/deviceManagement/reports/exportJobs` — body `{"reportName":"Devices","filter":"","select":["DeviceName","OS","ComplianceState"]}` | **Tier 1** (POST, but a read-only export — quick confirm). Poll GET `/beta/deviceManagement/reports/exportJobs/{id}` until `status=completed`, then download from `url` |

Pagination matters here most: fleets >1000 devices span multiple pages —
`graph.sh` merges them, but never summarize from a single raw page.

## 2. Intune audit logs

| # | Action | Method & Path |
|---|---|---|
| 2.1 | List audit events | GET `/deviceManagement/auditEvents` — table: Date / Activity / Actor / Target / Result |
| 2.2 | Filter by date range | GET `/deviceManagement/auditEvents?$filter=activityDateTime gt {start} and activityDateTime lt {end}` — ISO 8601 UTC; compute "letzte Woche" etc. from today |
| 2.3 | Filter by actor | GET `/deviceManagement/auditEvents?$filter=actor/userPrincipalName eq '{upn}'` |
| 2.4 | Event details | GET `/deviceManagement/auditEvents/{id}` |

## 3. Entra ID audit & sign-in logs (needs `AuditLog.Read.All`)

| # | Action | Method & Path |
|---|---|---|
| 3.1 | Directory audits (device category) | GET `/auditLogs/directoryAudits?$filter=category eq 'Device'` |
| 3.2 | Sign-ins via Intune | GET `/auditLogs/signIns?$filter=appDisplayName eq 'Microsoft Intune'` |

## 4. Settings Catalog search & GPO analytics (beta)

| # | Action | Method & Path | Notes |
|---|---|---|---|
| 4.1 | Search settings | GET `/beta/deviceManagement/configurationSettings?$search="{term}"` | Answers "Kann Intune Einstellung X konfigurieren?" |
| 4.2 | GPO migration reports | GET `/beta/deviceManagement/groupPolicyMigrationReports` | For on-prem GPO → Intune migration questions |
| 4.3 | Migration report details | GET `/beta/deviceManagement/groupPolicyMigrationReports/{id}` | Which GPO settings are supported, which not, alternatives |
| 4.4 | Uploaded ADMX definition files | GET `/beta/deviceManagement/groupPolicyUploadedDefinitionFiles` | |
