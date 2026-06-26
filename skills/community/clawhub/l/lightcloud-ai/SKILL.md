---
name: lightcloud-api
description: Integrate with Qingyun/Lightcloud (轻云) API to manage form documents - fetch access tokens, retrieve, create, update, and delete form data. Use this skill when users request to interact with Qingyun/Lightcloud API, get access tokens, retrieve/create/update/delete form data, or work with Qingyun documents. Triggers include mentions of "轻云", "yunzhijia", "qingyun", "lightcloud", or requests to fetch/create/update/delete form data, access tokens, or document operations from Qingyun platform.
---

# Lightcloud API Integration

Provides seamless integration with Qingyun/Lightcloud (轻云) open API using curl/PowerShell commands that work cross-platform without requiring Python. Supports full CRUD operations on form documents.

## Installation

### Method 1: Command Line Installation (Recommended)

#### Using curl
```bash
# Download and install the skill
curl -L -o lightcloud-api.skill https://your-domain.com/skills/lightcloud-api.skill

# Or if you have the skill file locally
cp lightcloud-api.skill ~/.claude/skills/
```

#### Using wget
```bash
wget -O lightcloud-api.skill https://your-domain.com/skills/lightcloud-api.skill
cp lightcloud-api.skill ~/.claude/skills/
```

### Method 2: Manual Installation

1. Download the `lightcloud-api.skill` file
2. Copy it to your Claude Code skills directory:
   - **Mac/Linux**: `~/.claude/skills/`
   - **Windows**: `%USERPROFILE%\.claude\skills\`
3. Restart Claude Code or reload skills

### Method 3: OpenClaw Integration

This skill is compatible with [OpenClaw](https://github.com/openclaw/openclaw), the popular open-source Claude Code alternative.

#### Install in OpenClaw
```bash
# Navigate to OpenClaw skills directory
cd ~/.openclaw/skills/

# Download the skill
curl -L -O https://your-domain.com/skills/lightcloud-api.skill

# Or copy from local
cp /path/to/lightcloud-api.skill .

# Restart OpenClaw to load the skill
```

#### Verify Installation
After installation, test with natural language:
```
"获取轻云的access token"
"从轻云获取表单数据"
```

### Installation Verification

Test the skill is working:
```bash
# In Claude Code or OpenClaw, simply say:
"帮我获取轻云的access token"
```

If the skill responds with API call instructions, it's working correctly.

### Uninstallation

To remove the skill:
```bash
rm ~/.claude/skills/lightcloud-api.skill
# Or on Windows:
del %USERPROFILE%\.claude\skills\lightcloud-api.skill
```

## Quick Start

### 1. Get Access Token

#### Bash/Mac/Linux (curl)

First, generate a timestamp (must be within 3 minutes):
```bash
timestamp=$(($(date +%s) * 1000))
```

Then call the API:
```bash
curl -X POST "https://www.yunzhijia.com/gateway/oauth2/token/getAccessToken" \
  -H "Content-Type: application/json" \
  -d '{
    "appId": "YOUR_APP_ID",
    "eid": "YOUR_EID",
    "secret": "YOUR_SECRET",
    "timestamp": '$timestamp',
    "scope": "team"
  }'
```

#### Windows PowerShell

First, generate a timestamp:
```powershell
$timestamp = [int64](Get-Date -UFormat %s) * 1000
```

Then call the API:
```powershell
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    appId = "YOUR_APP_ID"
    eid = "YOUR_EID"
    secret = "YOUR_SECRET"
    timestamp = $timestamp
    scope = "team"
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://www.yunzhijia.com/gateway/oauth2/token/getAccessToken" `
  -Method POST -Headers $headers -Body $body
```

**Required parameters:**
- `appId`: Light application ID (轻应用id)
- `eid`: Team ID (团队id)
- `secret`: Application secret (轻应用secret)
- `timestamp`: Current Beijing time, Unix timestamp in milliseconds (13 digits), valid for 3 minutes
- `scope`: Authorization level (use "team")

**Response:**
```json
{
  "data": {
    "accessToken": "xxx",
    "expireIn": 7200,
    "refreshToken": "xxx"
  },
  "errorCode": 0,
  "success": true
}
```

### 2. Retrieve Form Data

#### Bash/Mac/Linux (curl)

```bash
curl -X POST "https://www.yunzhijia.com/gateway/lightcloud/data/list?accessToken=YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "eid": "YOUR_EID",
    "formCodeId": "YOUR_FORM_CODE_ID",
    "formInstIds": ["FORM_ID_1", "FORM_ID_2"]
  }'
```

#### Windows PowerShell

```powershell
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    eid = "YOUR_EID"
    formCodeId = "YOUR_FORM_CODE_ID"
    formInstIds = @("FORM_ID_1", "FORM_ID_2")
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://www.yunzhijia.com/gateway/lightcloud/data/list?accessToken=YOUR_ACCESS_TOKEN" `
  -Method POST -Headers $headers -Body $body
```

**Required parameters:**
- `accessToken`: Access token from step 1 (in URL query parameter)
- `eid`: Workspace eid (工作圈eid)
- `formCodeId`: Form code ID (表单codeId)
- `formInstIds`: Array of form instance IDs (单据id数组)

**Optional parameters:**
- `oid`: Query user openid (查询人openid)

### 3. Delete Form Documents

#### Bash/Mac/Linux (curl)

```bash
curl -X POST "https://www.yunzhijia.com/gateway/lightcloud/data/batchDelete?accessToken=YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "eid": "YOUR_EID",
    "formCodeId": "YOUR_FORM_CODE_ID",
    "formInstIds": ["FORM_ID_1", "FORM_ID_2"]
  }'
```

#### Windows PowerShell

```powershell
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    eid = "YOUR_EID"
    formCodeId = "YOUR_FORM_CODE_ID"
    formInstIds = @("FORM_ID_1", "FORM_ID_2")
} | ConvertTo-Json

Invoke-RestMethod -Uri "https://www.yunzhijia.com/gateway/lightcloud/data/batchDelete?accessToken=YOUR_ACCESS_TOKEN" `
  -Method POST -Headers $headers -Body $body
```

**Required parameters:**
- `accessToken`: Access token (in URL)
- `eid`: Workspace eid (工作圈eid)
- `formCodeId`: Form code ID (表单codeId)
- `formInstIds`: Array of form instance IDs to delete (单据id数组)

**Optional parameters:**
- `oid`: Deleter openid (删除人openid) - required for workflow documents

### 4. Create/Update Form Documents

#### Bash/Mac/Linux (curl)

```bash
curl -X POST "https://www.yunzhijia.com/gateway/lightcloud/data/batchSave?accessToken=YOUR_ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "eid": "YOUR_EID",
    "formCodeId": "YOUR_FORM_CODE_ID",
    "oid": "YOUR_OID",
    "data": [
      {
        "formInstId": "FORM_INST_ID",
        "widgetValue": {
          "_S_TITLE": "Document Title",
          "Te_0": "Text field value"
        },
        "details": {
          "Dd_0": {
            "widgetValue": [
              {
                "_id_": "1",
                "Te_0": "Detail field value"
              }
            ]
          }
        }
      }
    ]
  }'
```

#### Windows PowerShell

```powershell
$headers = @{
    "Content-Type" = "application/json"
}

$body = @{
    eid = "YOUR_EID"
    formCodeId = "YOUR_FORM_CODE_ID"
    oid = "YOUR_OID"
    data = @(
        @{
            formInstId = "FORM_INST_ID"
            widgetValue = @{
                "_S_TITLE" = "Document Title"
                "Te_0" = "Text field value"
            }
            details = @{
                "Dd_0" = @{
                    widgetValue = @(
                        @{
                            "_id_" = "1"
                            "Te_0" = "Detail field value"
                        }
                    )
                }
            }
        }
    )
} | ConvertTo-Json -Depth 10

Invoke-RestMethod -Uri "https://www.yunzhijia.com/gateway/lightcloud/data/batchSave?accessToken=YOUR_ACCESS_TOKEN" `
  -Method POST -Headers $headers -Body $body
```

**Required parameters:**
- `accessToken`: Access token (in URL)
- `eid`: Workspace eid (工作圈eid)
- `formCodeId`: Form code ID (表单codeId)
- `oid`: Creator openid (新增人openid)
- `data`: Array of form instances (单据实例数组)

**Data structure:**
- `formInstId`: Form instance ID - required for updates, omit for new documents
- `widgetValue`: Main form fields (主表单控件字段)
  - `_S_TITLE`: Document title
  - Other field codeIds and values
- `details`: Detail/form grid fields (明细控件字段)
  - Key is detail widget codeId
  - `widgetValue`: Array of detail rows
    - `_id_`: Row ID (required)
    - Other field codeIds and values

## Common User Requests

**"获取轻云的access token"**
→ Provide user with curl/PowerShell command with placeholders for credentials

**"从轻云获取单据数据"**
→ First help get access token, then provide form retrieval command

**"帮我调用轻云API获取表单数据"**
→ Two-step process: authenticate, then fetch forms using appropriate platform commands

**"删除轻云单据"**
→ Provide batch delete command with user's access token and form IDs

**"创建新的轻云表单"**
→ Help construct batchSave request with widget values

**"更新轻云表单数据"**
→ Use batchSave with formInstId to update existing documents

**"批量操作轻云单据"**
→ Determine operation type (fetch/delete/save) and execute appropriate API call

## Workflow

1. **Identify platform**: Detect if user is on Bash/Mac/Linux or Windows PowerShell
2. **Collect credentials**: Ask user for appId, eid, and secret if not provided
3. **Generate timestamp**: Create current timestamp in milliseconds
4. **Get access token**: Execute appropriate command for platform
5. **Parse token**: Extract accessToken from response
6. **Fetch form data**: Use token to retrieve documents
7. **Present results**: Display data in user-friendly format

## Important Notes

- **No Python required**: Uses native curl (Bash/Mac/Linux) or Invoke-RestMethod (PowerShell)
- **Cross-platform**: Works on Windows, Mac, and Linux
- **Timestamp validity**: Must be within 3 minutes or request will be rejected
- **Token expiration**: Access tokens expire based on `expireIn` field (typically 7200 seconds)
- **Batch retrieval**: formInstIds accepts array for multiple forms
- **Error handling**: Check `success` field in response

## One-Liner Commands

For quick execution, use these complete one-liners:

### Get Access Token (Bash)
```bash
curl -X POST "https://www.yunzhijia.com/gateway/oauth2/token/getAccessToken" -H "Content-Type: application/json" -d '{"appId":"YOUR_APP_ID","eid":"YOUR_EID","secret":"YOUR_SECRET","timestamp":'$(($(date +%s) * 1000))',"scope":"team"}'
```

### Get Access Token (PowerShell)
```powershell
$body = @{appId="YOUR_APP_ID";eid="YOUR_EID";secret="YOUR_SECRET";timestamp=[int64](Get-Date -UFormat %s)*1000;scope="team"} | ConvertTo-Json; Invoke-RestMethod -Uri "https://www.yunzhijia.com/gateway/oauth2/token/getAccessToken" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body
```

### Delete Forms (Bash)
```bash
curl -X POST "https://www.yunzhijia.com/gateway/lightcloud/data/batchDelete?accessToken=YOUR_TOKEN" -H "Content-Type: application/json" -d '{"eid":"YOUR_EID","formCodeId":"YOUR_FORM_ID","formInstIds":["ID1","ID2"]}'
```

### Delete Forms (PowerShell)
```powershell
$body = @{eid="YOUR_EID";formCodeId="YOUR_FORM_ID";formInstIds=@("ID1","ID2")} | ConvertTo-Json; Invoke-RestMethod -Uri "https://www.yunzhijia.com/gateway/lightcloud/data/batchDelete?accessToken=YOUR_TOKEN" -Method POST -Headers @{"Content-Type"="application/json"} -Body $body
```

## API Reference

For detailed API documentation including:
- Complete request/response formats
- Field type definitions
- System reserved fields
- Error codes and troubleshooting

See [references/api_reference.md](references/api_reference.md)

## Platform Compatibility

### Claude Code
✅ **Fully Compatible**
- Native skill support
- Automatic loading from `~/.claude/skills/`
- Natural language triggers

### OpenClaw
✅ **Fully Compatible**
- OpenClaw 1.0+ supported
- Install to `~/.openclaw/skills/`
- All features work identically
- Community-tested and verified

### Other Platforms
✅ **Standards Compliant**
- Works with any platform supporting Claude Code skill format
- No platform-specific dependencies
- Pure curl/PowerShell implementation

## Troubleshooting

### Installation Issues

**Skill not loading?**
```bash
# Check skill file exists
ls -la ~/.claude/skills/lightcloud-api.skill

# Verify file integrity
file ~/.claude/skills/lightcloud-api.skill
# Should show: Zip archive data

# Reinstall if needed
rm ~/.claude/skills/lightcloud-api.skill
# Then reinstall using method above
```

**OpenClaw not recognizing skill?**
```bash
# Ensure OpenClaw skills directory exists
mkdir -p ~/.openclaw/skills

# Copy skill to OpenClaw directory
cp ~/.claude/skills/lightcloud-api.skill ~/.openclaw/skills/

# Restart OpenClaw
```

### API Issues

**Token expired?**
- Tokens typically expire in 2 hours (7200 seconds)
- Get a new token using the access token endpoint

**Timestamp errors?**
- Ensure timestamp is within 3 minutes
- Use automatic timestamp generation in commands

**Platform detection wrong?**
- Skill auto-detects Bash vs PowerShell
- Manual override: specify platform in request

## Support

- **Issues**: Report bugs on GitHub Issues
- **Feature Requests**: Submit via GitHub Discussions
- **Community**: Join OpenClaw Discord for help

## License

MIT License - Free to use, modify, and distribute
