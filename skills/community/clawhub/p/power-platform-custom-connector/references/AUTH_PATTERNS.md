# Authentication Patterns Reference

Connection parameter patterns for `apiProperties.json`. Each pattern shows the complete `connectionParameters` block.

**Source:** [PowerPlatformConnectors repo](https://github.com/microsoft/PowerPlatformConnectors) schemas and real connector examples.

---

## API Key Authentication

The most common pattern for Independent Publisher connectors. The key is passed as a header or query parameter.

### API Key in Header

```json
{
  "properties": {
    "connectionParameters": {
      "api_key": {
        "type": "securestring",
        "uiDefinition": {
          "constraints": {
            "clearText": false,
            "required": "true",
            "tabIndex": 2
          },
          "description": "Your API key from the service dashboard",
          "displayName": "API Key",
          "tooltip": "Provide your API key"
        }
      }
    },
    "iconBrandColor": "#da3b01",
    "capabilities": [],
    "publisher": "Your Name",
    "stackOwner": "Service Company Name"
  }
}
```

In `apiDefinition.swagger.json`, define the security scheme:

```json
"securityDefinitions": {
  "api_key": {
    "type": "apiKey",
    "in": "header",
    "name": "X-Api-Key"
  }
},
"security": [
  { "api_key": [] }
]
```

### API Key with Bearer Token Prefix

Some APIs expect `Authorization: Bearer <key>`. Use a policy template to inject the prefix:

```json
{
  "properties": {
    "connectionParameters": {
      "api_key": {
        "type": "securestring",
        "uiDefinition": {
          "constraints": { "clearText": false, "required": "true", "tabIndex": 2 },
          "description": "Bearer token for authentication",
          "displayName": "API Key",
          "tooltip": "Provide your API key"
        }
      }
    },
    "iconBrandColor": "#da3b01",
    "capabilities": [],
    "publisher": "Your Name",
    "stackOwner": "Service Company Name",
    "policyTemplateInstances": [
      {
        "templateId": "setheader",
        "title": "Set Authorization Header",
        "parameters": {
          "x-ms-apimTemplateParameter.name": "Authorization",
          "x-ms-apimTemplateParameter.value": "Bearer @connectionParameters('api_key')",
          "x-ms-apimTemplateParameter.existsAction": "override"
        }
      }
    ]
  }
}
```

With this approach, use `"securityDefinitions": {}` in the swagger since auth is handled by the policy template.

---

## OAuth 2.0 (Microsoft Entra ID / AAD)

Used for connectors accessing Azure services (Key Vault, Graph, etc.).

```json
{
  "properties": {
    "connectionParameters": {
      "token": {
        "type": "oauthSetting",
        "oAuthSettings": {
          "identityProvider": "aad",
          "clientId": "<<Enter your client ID>>",
          "scopes": [],
          "redirectMode": "GlobalPerConnector",
          "redirectUrl": "https://global.consent.azure-apim.net/redirect",
          "properties": {
            "IsFirstParty": "False"
          },
          "customParameters": {
            "loginUri": {
              "value": "https://login.windows.net"
            },
            "tenantId": {
              "value": "common"
            },
            "resourceUri": {
              "value": "https://vault.azure.net"
            }
          }
        }
      }
    },
    "iconBrandColor": "#007ee5"
  }
}
```

Matching swagger `securityDefinitions`:

```json
"securityDefinitions": {
  "oauth2_auth": {
    "type": "oauth2",
    "flow": "accessCode",
    "authorizationUrl": "https://login.windows.net/common/oauth2/authorize",
    "tokenUrl": "https://login.windows.net/common/oauth2/authorize",
    "scopes": {}
  }
},
"security": [
  { "oauth2_auth": [] }
]
```

### AAD with Dynamic Host URL

When the host URL depends on a connection parameter (e.g., Key Vault name):

```json
{
  "properties": {
    "connectionParameters": {
      "vaultName": {
        "type": "string",
        "uiDefinition": {
          "constraints": { "required": "true" },
          "description": "Name of your Key Vault",
          "displayName": "Vault Name",
          "tooltip": "Provide your Key Vault name"
        }
      },
      "token": {
        "type": "oauthSetting",
        "oAuthSettings": {
          "identityProvider": "aad",
          "clientId": "<<Enter your client ID>>",
          "scopes": [],
          "redirectMode": "GlobalPerConnector",
          "redirectUrl": "https://global.consent.azure-apim.net/redirect",
          "properties": { "IsFirstParty": "False" },
          "customParameters": {
            "loginUri": { "value": "https://login.windows.net" },
            "tenantId": { "value": "common" },
            "resourceUri": { "value": "https://vault.azure.net" }
          }
        }
      }
    },
    "policyTemplateInstances": [
      {
        "templateId": "dynamichosturl",
        "title": "Route to vault",
        "parameters": {
          "x-ms-apimTemplateParameter.urlTemplate": "https://@connectionParameters('vaultName').vault.azure.net"
        }
      }
    ]
  }
}
```

---

## OAuth 2.0 (Generic)

For non-Microsoft OAuth 2.0 providers (GitHub, Slack, Spotify, etc.).

```json
{
  "properties": {
    "connectionParameters": {
      "token": {
        "type": "oauthSetting",
        "oAuthSettings": {
          "identityProvider": "oauth2",
          "clientId": "<<Enter your client ID>>",
          "scopes": "read write",
          "redirectMode": "GlobalPerConnector",
          "redirectUrl": "https://global.consent.azure-apim.net/redirect",
          "properties": {
            "IsFirstParty": "False"
          },
          "customParameters": {
            "authorizationUrl": {
              "value": "https://provider.com/oauth/authorize"
            },
            "tokenUrl": {
              "value": "https://provider.com/oauth/token"
            },
            "refreshUrl": {
              "value": "https://provider.com/oauth/token"
            }
          }
        }
      }
    },
    "iconBrandColor": "#da3b01",
    "capabilities": [],
    "publisher": "Your Name",
    "stackOwner": "Provider Company Name"
  }
}
```

Matching swagger `securityDefinitions`:

```json
"securityDefinitions": {
  "oauth2_auth": {
    "type": "oauth2",
    "flow": "accessCode",
    "authorizationUrl": "https://provider.com/oauth/authorize",
    "tokenUrl": "https://provider.com/oauth/token",
    "scopes": {
      "read": "Read access",
      "write": "Write access"
    }
  }
}
```

**Important for Independent Publisher OAuth connectors:**
- Provide detailed step-by-step instructions in the readme for creating the OAuth app on the provider's platform
- Include screenshots if possible
- Document all required scopes and their purpose

---

## Basic Authentication

Username and password sent as Basic Auth header.

```json
{
  "properties": {
    "connectionParameters": {
      "username": {
        "type": "string",
        "uiDefinition": {
          "constraints": { "required": "true" },
          "description": "Your account username",
          "displayName": "Username",
          "tooltip": "Provide your username"
        }
      },
      "password": {
        "type": "securestring",
        "uiDefinition": {
          "constraints": { "clearText": false, "required": "true" },
          "description": "Your account password",
          "displayName": "Password",
          "tooltip": "Provide your password"
        }
      }
    },
    "iconBrandColor": "#da3b01",
    "capabilities": [],
    "publisher": "Your Name",
    "stackOwner": "Service Company Name"
  }
}
```

Matching swagger:

```json
"securityDefinitions": {
  "basic_auth": {
    "type": "basic"
  }
},
"security": [
  { "basic_auth": [] }
]
```

---

## Per-Connector Redirect URI (Mandatory)

Since February 2024, all OAuth 2.0 connectors must use per-connector redirect URIs.

- New connectors automatically get a unique redirect URI
- Existing connectors: edit in the Security tab, check "Update to unique redirect URL", and save
- **Always** set `"redirectMode": "GlobalPerConnector"` in apiProperties.json
- Remove the global redirect URI (`https://global.consent.azure-apim.net/redirect`) from your OAuth app after migration

---

## Multiple Authentication (Multi-Auth)

Multi-auth allows users to choose which authentication method to use when creating a connection. Use `connectionParameterSets` in `apiProperties.json` instead of `connectionParameters`.

**Important:** Multi-auth is **not supported in the Custom Connector Wizard**. Use [`paconn` CLI](https://learn.microsoft.com/en-us/connectors/custom-connectors/paconn-cli) to create or update connectors with multi-auth.

### Structure

```json
{
  "properties": {
    "connectionParameterSets": {
      "uiDefinition": {
        "displayName": "Authentication Type",
        "description": "Type of authentication to be used."
      },
      "values": [
        {
          "name": "api-key-auth",
          "uiDefinition": {
            "displayName": "Use API Key",
            "description": "Log in using an API Key."
          },
          "parameters": {
            "api_key": {
              "type": "securestring",
              "uiDefinition": {
                "constraints": { "clearText": false, "required": "true", "tabIndex": 2 },
                "schema": {
                  "description": "Enter your API key",
                  "type": "securestring"
                },
                "displayName": "API Key"
              }
            }
          }
        },
        {
          "name": "basic-auth",
          "uiDefinition": {
            "displayName": "Use Username and Password",
            "description": "Log in using your credentials."
          },
          "parameters": {
            "username": {
              "type": "string",
              "uiDefinition": {
                "displayName": "Username",
                "schema": {
                  "description": "Your account username",
                  "type": "string"
                },
                "tooltip": "Provide your username",
                "constraints": { "required": "true" }
              }
            },
            "password": {
              "type": "securestring",
              "uiDefinition": {
                "displayName": "Password",
                "schema": {
                  "description": "Your account password",
                  "type": "securestring"
                },
                "tooltip": "Provide your password",
                "constraints": { "required": "true" }
              }
            }
          }
        }
      ]
    },
    "iconBrandColor": "#da3b01",
    "capabilities": [],
    "publisher": "Your Name",
    "stackOwner": "Service Company Name"
  }
}
```

### Multi-Auth with Entra ID + Generic OAuth 2.0

You can have two OAuth `oauthSetting` parameter sets with different identity providers:

```json
"connectionParameterSets": {
  "uiDefinition": {
    "displayName": "Authentication Type",
    "description": "Type of authentication to be used."
  },
  "values": [
    {
      "name": "aad-auth",
      "uiDefinition": {
        "displayName": "Use Entra ID (shared application)",
        "description": "Log in using the standard shared app."
      },
      "parameters": {
        "token": {
          "type": "oauthSetting",
          "oAuthSettings": {
            "identityProvider": "aad",
            "clientId": "<<Enter your AAD client ID>>",
            "scopes": ["Group.ReadWrite.All offline_access"],
            "redirectMode": "GlobalPerConnector",
            "customParameters": {
              "loginUri": { "value": "https://login.windows.net" },
              "resourceUri": { "value": "https://graph.microsoft.com" },
              "tenantId": { "value": "common" }
            },
            "properties": { "IsFirstParty": "False" }
          }
        }
      }
    },
    {
      "name": "custom-oauth-auth",
      "uiDefinition": {
        "displayName": "Use custom OAuth app",
        "description": "Log in using your own OAuth application."
      },
      "parameters": {
        "token": {
          "type": "oauthSetting",
          "oAuthSettings": {
            "identityProvider": "oauth2",
            "clientId": "<<Enter your client ID>>",
            "redirectMode": "GlobalPerConnector",
            "customParameters": {
              "authorizationUrl": { "value": "https://provider.com/oauth/authorize" },
              "tokenUrl": { "value": "https://provider.com/oauth/token" },
              "refreshUrl": { "value": "https://provider.com/oauth/token" }
            }
          }
        }
      }
    }
  ]
}
```

### Key Differences from Single Auth

| Aspect | Single Auth | Multi-Auth |
|--------|-----------|------------|
| **Property** | `connectionParameters` | `connectionParameterSets` |
| **String descriptions** | Direct `description` property | Nested in `uiDefinition.schema.description` |
| **Wizard support** | Supported | **Not supported** — use paconn CLI |
| **Parameter structure** | Flat key-value | Wrapped inside `values[].parameters` |

**Source:** [Microsoft Docs — Multi-Auth](https://learn.microsoft.com/en-us/connectors/custom-connectors/multi-auth)

---

## Connection Parameter Types

| Type | Use For |
|------|---------|
| `string` | Plain text values (host names, account IDs) |
| `securestring` | Sensitive values (API keys, passwords, tokens) — masked in UI |
| `int` | Integer values |
| `bool` | Boolean flags |
| `oauthSetting` | OAuth 2.0 configuration object |
| `gatewaySetting` | On-premises data gateway configuration |

### Supported Identity Providers

| Provider | Use Case |
|----------|----------|
| `aad` | Microsoft Entra ID (Azure AD) |
| `aadcertificate` | AAD with certificate auth |
| `oauth2` | Generic OAuth 2.0 |
| `oauth2generic` | Generic OAuth 2.0 (alternative) |
| `facebook` | Facebook OAuth |
