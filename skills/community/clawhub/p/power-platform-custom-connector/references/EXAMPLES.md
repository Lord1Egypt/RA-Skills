# Examples Reference

Complete working connector examples. All patterns sourced from the [microsoft/PowerPlatformConnectors](https://github.com/microsoft/PowerPlatformConnectors) repository and official Microsoft documentation.

---

## Example 1: Minimal Independent Publisher Connector (API Key)

A basic connector with two operations using API Key authentication. This is the starting point for most Independent Publisher connectors.

### apiDefinition.swagger.json

```json
{
  "swagger": "2.0",
  "info": {
    "version": "1.0.0",
    "title": "Weather Service",
    "description": "Get current weather data and forecasts for any location worldwide.",
    "contact": {
      "name": "Your Name",
      "url": "https://github.com/yourusername",
      "email": "you@example.com"
    }
  },
  "host": "api.weatherservice.com",
  "basePath": "/v1",
  "schemes": ["https"],
  "consumes": ["application/json"],
  "produces": ["application/json"],
  "securityDefinitions": {
    "api_key": {
      "type": "apiKey",
      "in": "header",
      "name": "X-Api-Key"
    }
  },
  "security": [
    { "api_key": [] }
  ],
  "paths": {
    "/weather/current": {
      "get": {
        "operationId": "GetCurrentWeather",
        "summary": "Get current weather",
        "description": "Retrieves the current weather conditions for a specified location.",
        "x-ms-visibility": "important",
        "parameters": [
          {
            "name": "city",
            "in": "query",
            "type": "string",
            "required": true,
            "x-ms-summary": "City",
            "description": "The city name to get weather for"
          },
          {
            "name": "units",
            "in": "query",
            "type": "string",
            "required": false,
            "default": "metric",
            "x-ms-summary": "Units",
            "description": "Temperature units (metric or imperial)",
            "x-ms-visibility": "advanced",
            "enum": ["metric", "imperial"]
          }
        ],
        "responses": {
          "200": {
            "description": "Success",
            "schema": {
              "$ref": "#/definitions/CurrentWeather"
            }
          }
        }
      }
    },
    "/weather/forecast": {
      "get": {
        "operationId": "GetForecast",
        "summary": "Get weather forecast",
        "description": "Retrieves the weather forecast for the next 5 days.",
        "parameters": [
          {
            "name": "city",
            "in": "query",
            "type": "string",
            "required": true,
            "x-ms-summary": "City",
            "description": "The city name to get the forecast for"
          },
          {
            "name": "days",
            "in": "query",
            "type": "integer",
            "required": false,
            "default": 5,
            "x-ms-summary": "Days",
            "description": "Number of forecast days (1-5)",
            "x-ms-visibility": "advanced"
          }
        ],
        "responses": {
          "200": {
            "description": "Success",
            "schema": {
              "$ref": "#/definitions/Forecast"
            }
          }
        }
      }
    }
  },
  "definitions": {
    "CurrentWeather": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "x-ms-summary": "City"
        },
        "temperature": {
          "type": "number",
          "format": "float",
          "x-ms-summary": "Temperature"
        },
        "description": {
          "type": "string",
          "x-ms-summary": "Conditions"
        },
        "humidity": {
          "type": "integer",
          "x-ms-summary": "Humidity (%)"
        }
      }
    },
    "Forecast": {
      "type": "object",
      "properties": {
        "city": {
          "type": "string",
          "x-ms-summary": "City"
        },
        "days": {
          "type": "array",
          "items": {
            "$ref": "#/definitions/ForecastDay"
          }
        }
      }
    },
    "ForecastDay": {
      "type": "object",
      "properties": {
        "date": {
          "type": "string",
          "format": "date",
          "x-ms-summary": "Date"
        },
        "high": {
          "type": "number",
          "format": "float",
          "x-ms-summary": "High Temperature"
        },
        "low": {
          "type": "number",
          "format": "float",
          "x-ms-summary": "Low Temperature"
        },
        "description": {
          "type": "string",
          "x-ms-summary": "Conditions"
        }
      }
    }
  },
  "x-ms-connector-metadata": [
    { "propertyName": "Website", "propertyValue": "https://weatherservice.com" },
    { "propertyName": "Privacy policy", "propertyValue": "https://weatherservice.com/privacy" },
    { "propertyName": "Categories", "propertyValue": "Data;Lifestyle and Entertainment" }
  ]
}
```

### apiProperties.json

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
          "description": "Your API key from the Weather Service dashboard (Settings > API Keys)",
          "displayName": "API Key",
          "tooltip": "Provide your Weather Service API key"
        }
      }
    },
    "iconBrandColor": "#da3b01",
    "capabilities": [],
    "publisher": "Your Name",
    "stackOwner": "Weather Service Inc."
  }
}
```

---

## Example 2: OAuth 2.0 (AAD) with Dynamic Host URL

Based on the AzureKeyVault pattern from the PowerPlatformConnectors repo.

### apiProperties.json

```json
{
  "properties": {
    "connectionParameters": {
      "vaultName": {
        "type": "string",
        "uiDefinition": {
          "constraints": { "required": "true" },
          "description": "Specify the name of your Key Vault",
          "displayName": "Key Vault Name",
          "tooltip": "Provide your Key Vault name"
        }
      },
      "token": {
        "type": "oauthSetting",
        "oAuthSettings": {
          "identityProvider": "aad",
          "clientId": "<<Enter your client ID>>",
          "scopes": [],
          "redirectMode": "Global",
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
    "iconBrandColor": "#007ee5",
    "policyTemplateInstances": [
      {
        "templateId": "dynamichosturl",
        "title": "Route to keyvault",
        "parameters": {
          "x-ms-apimTemplateParameter.urlTemplate": "https://@connectionParameters('vaultName').vault.azure.net"
        }
      }
    ]
  }
}
```

### apiDefinition.swagger.json (key paths)

```json
{
  "swagger": "2.0",
  "info": {
    "title": "Azure Key Vault [Sample]",
    "description": "A sample connector for the Azure Key Vault service.",
    "version": "1.0"
  },
  "host": "placeholder.vault.azure.net",
  "basePath": "/",
  "schemes": ["https"],
  "securityDefinitions": {
    "oauth2_auth": {
      "type": "oauth2",
      "flow": "accessCode",
      "authorizationUrl": "https://login.windows.net/common/oauth2/authorize",
      "tokenUrl": "https://login.windows.net/common/oauth2/authorize",
      "scopes": {}
    }
  },
  "security": [{ "oauth2_auth": [] }],
  "paths": {
    "/keys": {
      "get": {
        "operationId": "ListKeys",
        "summary": "List keys",
        "description": "List keys in the specified vault.",
        "parameters": [
          {
            "name": "api-version",
            "in": "query",
            "type": "string",
            "default": "7.0",
            "required": true,
            "x-ms-visibility": "internal",
            "x-ms-summary": "API Version"
          }
        ],
        "responses": {
          "200": {
            "description": "Success",
            "schema": {
              "type": "object",
              "properties": {
                "value": {
                  "type": "array",
                  "items": {
                    "type": "object",
                    "properties": {
                      "kid": { "type": "string", "x-ms-summary": "Key ID" },
                      "attributes": {
                        "type": "object",
                        "properties": {
                          "enabled": { "type": "boolean", "x-ms-summary": "Enabled" },
                          "created": { "type": "integer", "x-ms-summary": "Created" }
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

---

## Example 3: Connector with Custom Code

An Independent Publisher connector that uses `script.csx` to transform responses.

### apiProperties.json

```json
{
  "properties": {
    "connectionParameters": {
      "api_key": {
        "type": "securestring",
        "uiDefinition": {
          "constraints": { "clearText": false, "required": "true", "tabIndex": 2 },
          "description": "Your API key",
          "displayName": "API Key",
          "tooltip": "Provide your API key"
        }
      }
    },
    "iconBrandColor": "#da3b01",
    "capabilities": [],
    "publisher": "Your Name",
    "stackOwner": "AI Service Inc.",
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

### script.csx

```csharp
public class Script : ScriptBase
{
    public override async Task<HttpResponseMessage> ExecuteAsync()
    {
        switch (this.Context.OperationId)
        {
            case "AnalyzeText":
                return await HandleAnalyzeText().ConfigureAwait(false);
            default:
                return await this.Context.SendAsync(
                    this.Context.Request, this.CancellationToken
                ).ConfigureAwait(false);
        }
    }

    private async Task<HttpResponseMessage> HandleAnalyzeText()
    {
        // Forward the request to the backend
        var response = await this.Context.SendAsync(
            this.Context.Request, this.CancellationToken
        ).ConfigureAwait(false);

        if (response.IsSuccessStatusCode)
        {
            var content = await response.Content.ReadAsStringAsync().ConfigureAwait(false);
            var result = JObject.Parse(content);

            // Flatten nested response for better Power Automate usability
            var simplified = new JObject
            {
                ["text"] = result["input"]?["text"],
                ["sentiment"] = result["analysis"]?["sentiment"]?["label"],
                ["confidence"] = result["analysis"]?["sentiment"]?["score"],
                ["language"] = result["analysis"]?["language"]
            };

            response.Content = CreateJsonContent(simplified.ToString());
        }

        return response;
    }
}
```

---

## Example 4: README Template (Independent Publisher)

```markdown
# Weather Service
Get current weather data and forecasts for any location worldwide.

## Publisher: Your Name

## Prerequisites
- A Weather Service account ([sign up here](https://weatherservice.com/signup))
- An API key (see Obtaining Credentials below)

## Supported Operations

### Get Current Weather
Retrieves the current weather conditions for a specified city.

**Inputs:**
- **City** (required): The city name
- **Units** (optional): Temperature units — metric (default) or imperial

**Output:** City, Temperature, Conditions, Humidity

### Get Weather Forecast
Retrieves the weather forecast for up to 5 days.

**Inputs:**
- **City** (required): The city name
- **Days** (optional): Number of forecast days (1-5, default 5)

**Output:** Array of daily forecasts with Date, High/Low Temperature, Conditions

## Obtaining Credentials
1. Create an account at [weatherservice.com/signup](https://weatherservice.com/signup)
2. Navigate to **Settings > API Keys**
3. Click **Generate New Key**
4. Copy the key and use it when creating the connection in Power Automate

## Known Issues and Limitations
- Rate limited to 60 requests per minute per API key
- City names must be in English
- Forecast limited to 5 days maximum

## Deployment Instructions
Run the following commands:
```
paconn create --api-def apiDefinition.swagger.json --api-prop apiProperties.json
```
```

---

## Example 5: Dynamic Dropdown Values

Operation that populates a dropdown from another API endpoint:

```json
{
  "/projects/{projectId}/tasks": {
    "get": {
      "operationId": "ListTasks",
      "summary": "List tasks in a project",
      "parameters": [
        {
          "name": "projectId",
          "in": "path",
          "type": "string",
          "required": true,
          "x-ms-summary": "Project",
          "x-ms-dynamic-values": {
            "operationId": "ListProjects",
            "value-path": "id",
            "value-title": "name",
            "value-collection": "projects",
            "parameters": {}
          },
          "x-ms-dynamic-list": {
            "operationId": "ListProjects",
            "itemsPath": "projects",
            "itemValuePath": "id",
            "itemTitlePath": "name",
            "parameters": {}
          }
        }
      ],
      "responses": {
        "200": {
          "description": "Success",
          "schema": {
            "type": "object",
            "properties": {
              "tasks": {
                "type": "array",
                "items": { "$ref": "#/definitions/Task" }
              }
            }
          }
        }
      }
    }
  },
  "/projects": {
    "get": {
      "operationId": "ListProjects",
      "summary": "List projects",
      "x-ms-visibility": "internal",
      "responses": {
        "200": {
          "description": "Success",
          "schema": {
            "type": "object",
            "properties": {
              "projects": {
                "type": "array",
                "items": {
                  "type": "object",
                  "properties": {
                    "id": { "type": "string" },
                    "name": { "type": "string" }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
```

Note: The `ListProjects` operation is marked `x-ms-visibility: "internal"` because it's only called to populate the dropdown, not by users directly.

---

## paconn CLI Quick Reference

```bash
# Install
pip install paconn

# Login
paconn login

# Create a new connector
paconn create --api-def apiDefinition.swagger.json --api-prop apiProperties.json

# Create with custom code and icon
paconn create --api-def apiDefinition.swagger.json --api-prop apiProperties.json \
  --script script.csx --icon icon.png

# Update an existing connector
paconn update --api-def apiDefinition.swagger.json --api-prop apiProperties.json \
  --connector-id <connector-id>

# Download an existing connector
paconn download --connector-id <connector-id> --dest ./my-connector

# Validate files against schemas
# Use VS Code with the repo's .vscode/settings.json for live validation
```
