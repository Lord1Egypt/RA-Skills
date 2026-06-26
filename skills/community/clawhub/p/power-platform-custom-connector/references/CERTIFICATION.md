# Certification & Submission Reference

Detailed certification workflows for Independent Publisher and Verified Publisher connectors. This file supplements the summary and PR checklist in the main SKILL.md.

---

## Solution Checker

Run [Solution Checker](https://learn.microsoft.com/en-us/power-apps/maker/data-platform/use-powerapps-checker) from the Power Apps maker portal before submitting:

1. Go to **make.powerapps.com** → **Solutions** → select your solution → **Run checker**
2. Review and resolve all **Critical** and **High** severity issues
3. Low/Medium issues are advisory but should be addressed when possible

```bash
# Alternative: export connector as a solution, then run Solution Checker via CLI
# pac solution check --path <solution-zip-path>
```

---

## Agent Action Requirements (Copilot Studio)

If the connector will be used as an agent action in Copilot Studio:

- Follow [Responsible AI guidelines](https://learn.microsoft.com/en-us/connectors/custom-connectors/certification-submission#step-3-agent-action-requirements)
- No inappropriate, offensive, or harmful content in connector metadata
- Operation descriptions must accurately reflect what the operation does
- Summaries and descriptions must be clear enough for an AI agent to select the correct operation

---

## Independent Publisher Certification Process

> **Note:** OAuth connectors are currently **unsupported** for Independent Publisher certification.

### Prerequisites

- Verified credentials via [OneVet](https://aka.ms/onevetsignup) with Microsoft Authenticator
- Read and agree to the [Independent Publisher Manifesto](https://github.com/microsoft/PowerPlatformConnectors/wiki/Independent-Publisher-Connector-Manifesto)

### Step 1 — Verify the connector doesn't already exist

- Search the [PowerPlatformConnectors repo](https://github.com/microsoft/PowerPlatformConnectors) to confirm the connector isn't already submitted or in progress
- Check both `independent-publisher-connectors/` and `certified-connectors/` directories
- Also check open PRs for in-progress submissions

### Step 2 — Submit a proposal PR

- Create a PR to `microsoft/PowerPlatformConnectors` on the `dev` branch
- Include only a `readme.md` describing the connector (operations, auth type, use cases)
- Title the PR: `[Proposal] ConnectorName (Independent Publisher)`
- Wait for review and approval from the Connector Certification Team

### Step 3 — Build the connector

After proposal approval, build the full connector:

| File | Required | Purpose |
|------|----------|---------|
| `apiDefinition.swagger.json` | **Yes** | OpenAPI 2.0 definition |
| `apiProperties.json` | **Yes** | Connection parameters and configuration |
| `readme.md` | **Yes** | Documentation following the template |
| `icon.png` | Optional | Connector icon (generic icon assigned automatically for IP) |
| `script.csx` | Optional | C# custom code for request/response transformation |

- `iconBrandColor` **must** be `#da3b01`
- The `(Independent Publisher)` suffix goes on the **PR title** (see Step 2), not the connector title in the OpenAPI definition
- Test thoroughly: ≥10 successful calls per operation
- Capture screenshots of 3+ unique operations working in a Flow

### Step 4 — Submit artifacts to the PR

- Update the proposal PR with all connector files
- Place files in `independent-publisher-connectors/YourConnector/`
- Include screenshots as PR attachments or in the PR description

### Step 5 — OneVet identity verification

- The Connector Certification Team will trigger a OneVet verification
- Respond to the verification request using Microsoft Authenticator
- This step proves you are a real person and not a bot
- Verification must be completed before the PR can be merged

### Step 6 — Certification and deployment

- The team reviews the connector, runs automated validation, and may request changes
- Once approved, the connector enters the deployment pipeline
- **Deployment timeline:** ~15 business days after final approval, deployed on Fridays
- The connector becomes available in Power Automate, Power Apps, and Logic Apps

---

## Verified Publisher Certification Process

### Prerequisites

- [Microsoft Partner Center](https://partner.microsoft.com/) account
- You own or operate the underlying API/service
- Custom icon prepared (see Icon Requirements below)

### Icon Requirements

- **Required** for Verified Publishers (Independent Publishers get a generic icon)
- Dimensions: 100×100 px to 230×230 px
- Format: PNG
- Background color must **not** be `#FFFFFF` (white) or `#007ee5` (default blue)
- Logo should not fill more than 70% of the image area
- Must not be the default Power Platform placeholder icon

### Step 1 — Prepare connector artifacts

Build and test all connector files:

| File | Required | Purpose |
|------|----------|---------|
| `apiDefinition.swagger.json` | **Yes** | OpenAPI 2.0 definition |
| `apiProperties.json` | **Yes** | Connection parameters and configuration |
| `readme.md` | **Yes** | Documentation following the template |
| `icon.png` | **Yes** | Custom connector icon (see requirements above) |
| `script.csx` | Optional | C# custom code for request/response transformation |

### Step 2 — Run Solution Checker

- Import the connector into a Power Platform environment as a solution
- Run Solution Checker and resolve all Critical/High issues
- See the Solution Checker section above for details

### Step 3 — Prepare the intro.md artifact

Create an `intro.md` file following this structure:

```markdown
## Connector Name

Description of the service and what the connector enables.

## Prerequisites

- An account with [Service Name](https://service.com)
- API credentials (describe how to obtain)

## How to get credentials

Step-by-step instructions for obtaining API keys, OAuth app setup, etc.

## Known issues and limitations

- List any current limitations
- Or: "There are no known issues at this time."
```

### Step 4 — Package the connector

```powershell
# 1. Export your connector as a managed solution (.zip) from Power Platform
# 2. Export the companion flow solution if applicable (.zip)
# 3. Create the package structure:
#    package/
#    ├── intro.md
#    └── <solution-export>.zip
#
# 4. Zip the package/ directory into package.zip

Compress-Archive -Path package/* -DestinationPath package.zip
```

### Step 5 — Validate the package

```powershell
# Download and run the ConnectorPackageValidator
# https://github.com/microsoft/PowerPlatformConnectors/blob/dev/scripts/ConnectorPackageValidator.ps1

.\ConnectorPackageValidator.ps1 -PackagePath .\package.zip
```

The validator checks:
- Package structure is correct (intro.md + solution zip(s))
- Solution files are valid
- Required metadata is present

### Step 6 — Upload and submit

```powershell
# Upload package.zip to Azure Blob Storage and generate a SAS URL
# The SAS URL must be valid for at least 15 days

# Using Azure CLI:
az storage blob upload `
  --account-name <storage-account> `
  --container-name <container> `
  --name package.zip `
  --file package.zip

# Generate SAS URL (valid for 30 days):
az storage blob generate-sas `
  --account-name <storage-account> `
  --container-name <container> `
  --name package.zip `
  --permissions r `
  --expiry (Get-Date).AddDays(30).ToString("yyyy-MM-ddTHH:mm:ssZ") `
  --full-uri
```

- Submit via [Microsoft Partner Center](https://partner.microsoft.com/)
- Provide the SAS URL, Client ID, and Client Secret (for OAuth connectors)
- **Deployment timeline:** ~15 business days after final approval, deployed on Fridays

---

## Connection Parameter Examples

These are common `connectionParameters` patterns used in `apiProperties.json` for certification. Each pattern must match the auth type declared in `securityDefinitions`.

### API Key

```json
"connectionParameters": {
  "api_key": {
    "type": "securestring",
    "uiDefinition": {
      "displayName": "API Key",
      "description": "The API key for this connector.",
      "tooltip": "Provide your API key.",
      "constraints": {
        "tabIndex": 2,
        "clearText": false,
        "required": "true"
      }
    }
  }
}
```

### Basic Auth

```json
"connectionParameters": {
  "username": {
    "type": "string",
    "uiDefinition": {
      "displayName": "Username",
      "description": "The username for this connection.",
      "tooltip": "Provide your username.",
      "constraints": {
        "tabIndex": 1,
        "required": "true"
      }
    }
  },
  "password": {
    "type": "securestring",
    "uiDefinition": {
      "displayName": "Password",
      "description": "The password for this connection.",
      "tooltip": "Provide your password.",
      "constraints": {
        "tabIndex": 2,
        "clearText": false,
        "required": "true"
      }
    }
  }
}
```

### OAuth 2.0 (Azure AD) — Verified Publisher only

```json
"connectionParameters": {
  "token": {
    "type": "oauthSetting",
    "oAuthSettings": {
      "identityProvider": "aad",
      "clientId": "<<CLIENT_ID>>",
      "scopes": [],
      "redirectMode": "GlobalPerConnector",
      "redirectUrl": "https://global.consent.azure-apim.net/redirect/<<CONNECTOR_NAME>>",
      "properties": {
        "IsFirstParty": "False"
      },
      "customParameters": {
        "resourceUri": {
          "value": "https://graph.microsoft.com"
        },
        "loginUri": {
          "value": "https://login.microsoftonline.com"
        },
        "loginUriAAD": {
          "value": "https://login.microsoftonline.com"
        }
      }
    }
  }
}
```

### Generic OAuth 2.0 — Verified Publisher only

```json
"connectionParameters": {
  "token": {
    "type": "oauthSetting",
    "oAuthSettings": {
      "identityProvider": "oauth2",
      "clientId": "<<CLIENT_ID>>",
      "scopes": ["read", "write"],
      "redirectMode": "GlobalPerConnector",
      "redirectUrl": "https://global.consent.azure-apim.net/redirect/<<CONNECTOR_NAME>>",
      "customParameters": {
        "authorizationUrl": {
          "value": "https://api.example.com/oauth/authorize"
        },
        "tokenUrl": {
          "value": "https://api.example.com/oauth/token"
        },
        "refreshUrl": {
          "value": "https://api.example.com/oauth/token"
        }
      }
    }
  }
}
```

> **Reminder:** `redirectMode` must be `"GlobalPerConnector"` (not `"Global"`) — mandatory since February 2024. OAuth connectors are currently **unsupported** for Independent Publisher certification.

---

## Office Hours

The Connector Certification Team holds open office hours every **Tuesday, 3:30–4:30 PM UTC**. Use these to:

- Ask questions about the certification process
- Get feedback on in-progress submissions
- Troubleshoot validation or deployment issues
- Clarify requirements for edge cases
