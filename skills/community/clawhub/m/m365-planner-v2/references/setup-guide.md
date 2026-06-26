# Detailed Setup Guide

## Azure AD App Registration - Step by Step

### 1. Portal Method (Browser)

1. Go to https://portal.azure.com → Azure Active Directory → App registrations
2. Click "New registration"
3. Enter:
   - Name: `M365-Planner-Integration`
   - Supported account types: `Accounts in this organizational directory only`
   - Redirect URI: None (for client credentials flow)
4. Click "Register"
5. Note the **Application (client) ID** and **Directory (tenant) ID**

### 2. Add API Permissions

1. Go to "API permissions" → "Add a permission"
2. Select "Microsoft Graph" → "Application permissions"
3. Add:
   - `Group.ReadWrite.All`
   - `Tasks.ReadWrite`
4. Click "Grant admin consent for [tenant]"

### 3. Create Client Secret

1. Go to "Certificates & secrets" → "Client secrets" → "New client secret"
2. Description: `OpenClaw Integration`
3. Expires: Select duration (24 months max)
4. Copy the **Value** (shown only once!)

### 4. Environment Configuration

Create `~/.openclaw/.env`:

```bash
# M365 Planner Integration
M365_CLIENT_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
M365_CLIENT_SECRET="your-secret-value"
M365_TENANT_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

### 5. Test Authentication

```bash
# Using mgc with client credentials
mgc login --strategy ClientSecret \
  --client-id $M365_CLIENT_ID \
  --client-secret $M365_CLIENT_SECRET \
  --tenant-id $M365_TENANT_ID

# Verify access
mgc me get
```

## Finding Group IDs

Planner plans require M365 groups. Find your groups:

```bash
# List all groups
mgc groups list --output table --select displayName,id

# Or use Azure CLI
az ad group list --query "[].{Name:displayName, ID:id}" -o table
```

## Common Issues

### "Insufficient privileges"
Solution: Grant admin consent in Azure Portal → API permissions → Grant admin consent

### "Group not found"
Solution: Ensure you're using an M365 group, not a security group or distribution list

### "Invalid authentication token"
Solution: Token expired. Re-run `mgc login`
