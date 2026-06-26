---
name: m365-planner
description: Manage Microsoft 365 Planner plans, buckets, and tasks via Microsoft Graph API. Use when creating, listing, updating, or deleting Planner resources. Supports group-based plan management, task assignment, progress tracking, and recurring tasks. Requires Azure AD app registration with Group.Read.All and Tasks.ReadWrite.All permissions.
license: MIT
version: 1.2.3
---

# M365 Planner Skill

Manage Microsoft 365 Planner through Microsoft Graph API.

## What's New in v1.2.3

- 🌍 **English Documentation** – Complete translation for international ClawHub availability
- 🔧 **Portability** – Env path now uses `os.homedir()` instead of hardcoded paths
- 🧹 **Security Cleanup** – Full audit for sensitive data (no IDs, names, domains)
- 📦 **ClawHub-ready** – Tarball created, node_modules excluded

## What's New in v1.2.2

- 🔧 **Portability** – Env path now uses `os.homedir()` instead of hardcoded `/home/claw/.openclaw/.env`
- 🧹 **Security Cleanup** – Full audit for sensitive data (no IDs, names, domains)
- 📦 **ClawHub-ready** – Tarball created, node_modules excluded

## What's New in v1.2.1

- ✅ **Generic Scripts** – No hardcoded Group-IDs or Plan names anymore
- ✅ **Command-Line Parameters** – All scripts accept IDs as arguments
- ✅ **List Plans Improved** – Shows all groups when no ID provided
- ✅ **Flexible Cleanup** – Works with any plans/buckets
- ✅ **ClawHub-ready** – No project-specific data included

## What's New in v1.1.0

- ✅ **Node.js Scripts** – Standalone scripts without `mgc` CLI
- ✅ **If-Match Header Support** – Correct ETag handling for updates/deletes
- ✅ **Group-Based API** – Direct access via M365 Group-ID
- ✅ **Recurring Tasks** – Note about native Planner recurrence feature
- ✅ **Cleanup Scripts** – Automated task cleanup

## Prerequisites

1. Azure AD App Registration (see Setup below)
2. Node.js v18+ with `@microsoft/microsoft-graph-client` and `axios`
3. M365 Group (not Security Group or Distribution List!)

## Quick Start

```bash
# Test connection
node scripts/test-connection.js

# List all plans
node scripts/list_plans.js

# List plans for specific group
node scripts/list_plans.js <group-id>

# Create plan
node scripts/create_plan.js "Project Name" <group-id>

# Create task
node scripts/create_task.js <plan-id> <bucket-id> "Task Title"

# Delete completed tasks
node scripts/cleanup_verlaengerungen.js <group-id> "<plan-name>" "<bucket-name>"
```

## Setup: Azure AD App Registration

### Step 1: Create App Registration

**Azure Portal:**
1. https://portal.azure.com → Azure Active Directory → App registrations
2. "New registration"
3. Name: `M365-Planner-Integration`
4. Supported account types: `Accounts in this organizational directory only`
5. Redirect URI: None (Client Credentials Flow)

**Or via Azure CLI:**
```bash
az login
az ad app create --display-name "M365-Planner-Integration" --sign-in-audience "AzureADMyOrg"
```
Note the **Application (client) ID** from the output.

### Step 2: Add API Permissions

**Important:** Use **Application Permissions** (not Delegated)!

**Azure Portal:**
1. App → API permissions → Add a permission
2. Microsoft Graph → Application permissions
3. Add:
   - `Group.Read.All` (not Group.ReadWrite.All – sufficient for Planner)
   - `Tasks.ReadWrite.All`
4. **Grant Admin Consent:** Click "Grant admin consent for [Tenant]"!

**Or via Azure CLI:**
```bash
APP_ID="your-app-id"

# Group.Read.All
az ad app permission add \
  --id $APP_ID \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions 5b567253-7703-48e2-861c-caed61531407=Role

# Tasks.ReadWrite.All
az ad app permission add \
  --id $APP_ID \
  --api 00000003-0000-0000-c000-000000000000 \
  --api-permissions bdfbf15f-ee85-495a-99a9-ef9b2abb1dcb=Role

# Admin Consent
az ad app permission admin-consent --id $APP_ID
```

### Step 3: Create Client Secret

**Azure Portal:**
1. App → Certificates & secrets → Client secrets → New client secret
2. Description: `OpenClaw Integration`
3. Expires: 24 months (Maximum)
4. **Copy values immediately!** – Only shown once

**Or via Azure CLI:**
```bash
az ad app credential reset \
  --id $APP_ID \
  --append \
  --display-name "OpenClaw Integration"
```

### Step 4: Configure Environment

Store credentials in `~/.openclaw/.env`:

```bash
# Microsoft 365 Planner Credentials
M365_CLIENT_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
M365_CLIENT_SECRET="your-secret-value"
M365_TENANT_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

**Secure permissions:**
```bash
chmod 600 ~/.openclaw/.env
```

### Step 5: Test Connection

```bash
node scripts/test-connection.js
```

Expected output:
```
✅ Access Token successfully received!
📋 Test: M365 Groups...
   3 groups found:
   - My Team ✅ M365/Planner-capable
✅ Connection successful!
```

## Important Notes

### M365 Groups vs. Security Groups

**Planner ONLY works with M365 Groups!**

- ✅ **M365 Group** – Has Exchange mailbox, Teams, Planner (recognizable by mail attribute)
- ❌ **Security Group** – Only for permissions, no Planner
- ❌ **Distribution List** – Only for email distribution, no Planner

**Check groups:**
```bash
node scripts/test-connection.js
```
Shows all groups with status "✅ M365/Planner-capable".

**Create M365 Group (if none exists):**
- Microsoft 365 Admin Center → Groups → Add a group
- Or Teams: Create new team (automatically creates M365 Group)

### If-Match Header (ETag)

**All update and delete operations require the `If-Match` header!**

Planner uses Optimistic Concurrency Control. Requests fail without ETag.

**Delete Example:**
```javascript
// Wrong ❌
await client.api(`/planner/tasks/${taskId}`).delete();

// Correct ✅
const task = await client.api(`/planner/tasks/${taskId}`).get();
await client.api(`/planner/tasks/${taskId}`)
    .headers({ 'If-Match': task['@odata.etag'] })
    .delete();
```

**Update Example:**
```javascript
const task = await client.api(`/planner/tasks/${taskId}`).get();
await client.api(`/planner/tasks/${taskId}`)
    .headers({ 'If-Match': task['@odata.etag'] })
    .update({ percentComplete: 50 });
```

### Group-Based API Endpoints

**Do NOT use:**
```
GET /planner/plans  ❌ (requires complex filter)
```

**Use:**
```
GET /groups/{group-id}/planner/plans  ✅
```

**Example:**
```javascript
const plans = await client.api(`/groups/${groupId}/planner/plans`).get();
```

### Recurring Tasks

**Microsoft Planner supports native recurring tasks!**

In Planner Web UI or Mobile App:
1. Open task
2. Click "Repeat"
3. Choose frequency: Daily, Weekly, Monthly, Yearly, Custom

**Example:**
- "Domain renewal example.com" → Repeat yearly
- "Check backup" → Repeat weekly

⚠️ **API Limitation:** The Graph API does not support creating recurring tasks directly.
Recurring tasks must be set up via Planner UI.

## Common Operations

### Plans

| Operation | Script |
|-----------|--------|
| List all plans | `node scripts/list_plans.js` |
| Create plan | `node scripts/create_plan.js <name> <group-id>` |
| Delete plan | `node scripts/delete_plan.js <plan-id>` |

### Buckets

| Operation | Script |
|-----------|--------|
| List buckets | Integrated in `list_plans.js` |
| Create bucket | `node scripts/create_bucket.js <plan-id> <name>` |
| Delete bucket | `node scripts/delete_bucket.js <bucket-id>` |

### Tasks

| Operation | Script |
|-----------|--------|
| List tasks | Integrated in `list_plans.js` |
| Create task | `node scripts/create_task.js <plan-id> <bucket-id> <title>` |
| Update task | `node scripts/update_task.js <task-id> --percent-complete 50` |
| Delete task | `node scripts/delete_task.js <task-id>` |
| Cleanup | `node scripts/cleanup_verlaengerungen.js <group-id> "<plan-name>" "<bucket-name>"` |

## Helper Scripts

### test-connection.js
Tests connection to Microsoft Graph:
- Request access token
- Display tenant information
- List available M365 Groups
- Check Planner capability

```bash
node scripts/test-connection.js
```

### list_plans.js
Shows all plans in an M365 Group with:
- Buckets and their tasks
- Task status (completed/in progress/open)
- Percentage progress indicator

```bash
# Without argument: Shows all available groups
node scripts/list_plans.js

# With Group ID: Shows plans for specific group
node scripts/list_plans.js <group-id>
```

### create_plan.js
Creates a new plan with default buckets:
- To Do
- In Progress  
- Done

```bash
node scripts/create_plan.js "Project Alpha" <group-id>
```

### cleanup_verlaengerungen.js
Cleans up completed tasks from a bucket:
- Deletes tasks with 100% progress
- Keeps open tasks
- Correct If-Match header handling

```bash
node scripts/cleanup_verlaengerungen.js <group-id> "<plan-name>" "<bucket-name>"
```

**Example:**
```bash
node scripts/cleanup_verlaengerungen.js abc-123 "My Project" "Completed"
```

## Troubleshooting

### Error: Insufficient privileges

**Cause:** Admin consent not granted

**Solution:**
```bash
az ad app permission admin-consent --id <app-id>
```
Or in Azure Portal: API permissions → Grant admin consent

### Error: Group not found

**Cause:** Planner only works with M365 Groups

**Solution:**
1. Check if it's an M365 Group (has mail attribute)
2. Security Groups/Distribution Lists don't work
3. Create new M365 Group (Teams or Admin Center)

### Error: The If-Match header must be specified

**Cause:** Update/Delete without ETag

**Solution:**
```javascript
// First get task for ETag
const task = await client.api(`/planner/tasks/${id}`).get();
// Then update/delete with If-Match header
await client.api(`/planner/tasks/${id}`)
    .headers({ 'If-Match': task['@odata.etag'] })
    .delete();
```

### Error: This entity set must be queried with a filter

**Cause:** `/planner/plans` endpoint requires filter

**Solution:** Use group-based endpoint:
```javascript
// Wrong ❌
const plans = await client.api('/planner/plans').get();

// Correct ✅
const plans = await client.api(`/groups/${groupId}/planner/plans`).get();
```

### Error: Cannot find module '@microsoft/microsoft-graph-client'

**Cause:** Node.js packages not installed

**Solution:**
```bash
cd ~/.openclaw/workspace/skills/m365-planner
npm install
```

## Dependencies

Install packages locally in skill directory:

```bash
cd ~/.openclaw/workspace/skills/m365-planner
npm install @microsoft/microsoft-graph-client axios
```

## References

- [Planner API Overview](references/planner-api.md)
- [Setup Guide](references/setup-guide.md)
- [Common Patterns](references/common-patterns.md)
- [Microsoft Graph API Docs](https://docs.microsoft.com/en-us/graph/api/overview)
- [Planner REST API Reference](https://docs.microsoft.com/en-us/graph/api/resources/planner-overview)

## Changelog

### v1.2.3 (2026-04-18)
- 🌍 **English Documentation** – Complete translation for international ClawHub availability
- 🔧 **Portability** – Env path uses `os.homedir()` for cross-system compatibility
- 🧹 **Security Audit** – No hardcoded IDs, names, or domains

### v1.2.2 (2026-04-18)
- 🔧 **Portability** – Env path now uses `os.homedir()` instead of hardcoded `/home/claw/.openclaw/.env`
- 🧹 **Security Cleanup** – Full audit for sensitive data (no IDs, names, domains)
- 📦 **ClawHub-ready** – Tarball created, node_modules excluded

### v1.2.1 (2026-04-18)
- ✅ **Generic Scripts** – No hardcoded Group-IDs or Plan names anymore
- ✅ **Command-Line Parameters** – All scripts accept IDs as arguments
- ✅ **List Plans Improved** – Shows all groups when no ID provided
- ✅ **Flexible Cleanup** – Works with any plans/buckets
- ✅ **ClawHub-ready** – No project-specific data included

### v1.1.0 (2026-04-17)
- ✅ Node.js Scripts instead of mgc CLI
- ✅ If-Match Header Support for updates/deletes
- ✅ Group-based API Endpoints
- ✅ Test-Connection Script with M365 Group Detection
- ✅ List Plans Script with Bucket/Task overview
- ✅ Cleanup Script for completed tasks
- ✅ Documentation for recurring tasks (native Planner feature)
- ✅ Troubleshooting Section expanded

### v1.0.0 (2023-01-19)
- Initial version with mgc CLI
- Azure AD Setup Guide
- Basic CRUD operations
