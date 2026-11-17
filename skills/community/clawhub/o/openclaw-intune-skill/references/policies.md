# Policies: Compliance, Configuration, Endpoint Security, Conditional Access, Filters

Call via `scripts/graph.sh`. Tier = safety tier from SKILL.md.
Conditional Access requires the `Policy.Read.All` / `Policy.ReadWrite.ConditionalAccess` permission (see README permission table).

## 1. Compliance policies

| # | Action | Method & Path | Tier |
|---|---|---|---|
| 1.1 | List | GET `/deviceManagement/deviceCompliancePolicies` | 0 |
| 1.2 | Details | GET `/deviceManagement/deviceCompliancePolicies/{id}` | 0 |
| 1.3 | Assignments | GET `/deviceManagement/deviceCompliancePolicies/{id}/assignments` | 0 |
| 1.4 | Device statuses | GET `/deviceManagement/deviceCompliancePolicies/{id}/deviceStatuses` | 0 |
| 1.5 | Create | POST `/deviceManagement/deviceCompliancePolicies` | 2 |
| 1.6 | Update | PATCH `/deviceManagement/deviceCompliancePolicies/{id}` | 2 |
| 1.7 | Delete | DELETE `/deviceManagement/deviceCompliancePolicies/{id}` | 2 |

Creating: the body needs a concrete `@odata.type` per platform, e.g.
`#microsoft.graph.windows10CompliancePolicy`, `…iosCompliancePolicy`,
`…androidCompliancePolicy`, `…macOSCompliancePolicy` — plus
`scheduledActionsForRule` (Graph rejects policies without at least one
scheduled action block). Ask the user for requirements first, show the
draft JSON summary, then create.

## 2. Configuration policies & profiles

| # | Action | Method & Path | Tier | Notes |
|---|---|---|---|---|
| 2.1 | List (Settings Catalog, modern) | GET `/deviceManagement/configurationPolicies` | 0 | Covers Endpoint Security, Admin Templates, Settings Catalog |
| 2.2 | List legacy profiles | GET `/deviceManagement/deviceConfigurations` | 0 | |
| 2.3 | Details | GET `/deviceManagement/configurationPolicies/{id}` | 0 | |
| 2.4 | Settings of a policy | GET `/deviceManagement/configurationPolicies/{id}/settings` | 0 | |
| 2.5 | Assignments | GET `/deviceManagement/configurationPolicies/{id}/assignments` | 0 | |
| 2.6 | Device status (legacy profile) | GET `/deviceManagement/deviceConfigurations/{id}/deviceStatuses` | 0 | |
| 2.7 | Create | POST `/deviceManagement/configurationPolicies` | 2 | |
| 2.8 | Delete | DELETE `/deviceManagement/configurationPolicies/{id}` | 2 | |

## 3. Endpoint Security (beta, template-family filters)

All: GET `/beta/deviceManagement/configurationPolicies?$filter=templateReference/templateFamily eq '{family}'` — Tier 0.

| Family value | Covers |
|---|---|
| `baseline` | Security baselines |
| `endpointSecurityDiskEncryption` | BitLocker / FileVault |
| `endpointSecurityFirewall` | Windows Firewall |
| `endpointSecurityAntivirus` | Microsoft Defender AV |
| `endpointSecurityAttackSurfaceReduction` | ASR rules |

## 4. Conditional Access

| # | Action | Method & Path | Tier | Notes |
|---|---|---|---|---|
| 4.1 | List policies | GET `/identity/conditionalAccess/policies` | 0 | Table: Name / State / Conditions / Grant controls |
| 4.2 | Details | GET `/identity/conditionalAccess/policies/{id}` | 0 | |
| 4.3 | Create | POST `/identity/conditionalAccess/policies` | 2 | Recommend `"state": "enabledForReportingButNotEnforced"` (report-only) first |
| 4.4 | Update | PATCH `/identity/conditionalAccess/policies/{id}` | 2 | Explain exactly what changes |
| 4.5 | **Delete** | DELETE `/identity/conditionalAccess/policies/{id}` | **3** | A wrong deletion can lock out or expose the whole tenant — user must type back the policy name |
| 4.6 | List named locations | GET `/identity/conditionalAccess/namedLocations` | 0 | |
| 4.7 | Create named location | POST `/identity/conditionalAccess/namedLocations` | 2 | IP example: `{"@odata.type":"#microsoft.graph.ipNamedLocation","displayName":"Office","isTrusted":true,"ipRanges":[{"@odata.type":"#microsoft.graph.iPv4CidrRange","cidrAddress":"192.168.1.0/24"}]}` |
| 4.8 | Authentication strengths | GET `/identity/conditionalAccess/authenticationStrength/policies` | 0 | |

⚠️ Warn the user before creating/enabling any CA policy that could block
the very account/app this skill uses.

## 5. Assignment filters & scope tags (beta)

| # | Action | Method & Path | Tier |
|---|---|---|---|
| 5.1 | List filters | GET `/beta/deviceManagement/assignmentFilters` | 0 |
| 5.2 | Filter details | GET `/beta/deviceManagement/assignmentFilters/{id}` | 0 |
| 5.3 | Create filter | POST `/beta/deviceManagement/assignmentFilters` | 2 |
| 5.4 | Preview filter result | POST `/beta/deviceManagement/assignmentFilters/{id}/getState` | 0 |
| 5.5 | List scope tags | GET `/beta/deviceManagement/roleScopeTags` | 0 |
| 5.6 | Create scope tag | POST `/beta/deviceManagement/roleScopeTags` | 2 |
