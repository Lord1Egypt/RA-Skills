# Policy Templates Reference

Policy templates transform requests and responses without custom code. Defined in `apiProperties.json` under `policyTemplateInstances`.

**Source:** [PowerPlatformConnectors repo](https://github.com/microsoft/PowerPlatformConnectors) and `paconn-apiProperties.schema.json`.

---

## When to Use Policy Templates vs Custom Code

| Use Case | Policy Templates | Custom Code (script.csx) |
|----------|-----------------|--------------------------|
| Inject headers | `setheader` | Not needed |
| Dynamic host URL | `dynamichosturl` | Not needed |
| Add default query params | `setqueryparameter` | Not needed |
| Simple string replacement | `stringreplace` | Not needed |
| Complex response transformation | Too limited | **Use custom code** |
| Multi-call orchestration | Not possible | **Use custom code** |
| Conditional logic per operation | Not possible | **Use custom code** |
| Pagination link rewriting | `updatenextlink` | Not needed |

**Rule:** Start with policy templates. Only use custom code when templates can't handle the transformation.

---

## Policy Template Structure

```json
{
  "properties": {
    "policyTemplateInstances": [
      {
        "templateId": "<template-id>",
        "title": "Human-readable description",
        "parameters": {
          "x-ms-apimTemplateParameter.<param>": "<value>"
        }
      }
    ]
  }
}
```

---

## Available Policy Templates

### dynamichosturl

Routes requests to a host URL constructed from connection parameters. Essential when the API endpoint varies per user/tenant.

```json
{
  "templateId": "dynamichosturl",
  "title": "Route to user's instance",
  "parameters": {
    "x-ms-apimTemplateParameter.urlTemplate": "https://@connectionParameters('instanceName').service.com"
  }
}
```

**Example — Azure Key Vault:**
```json
{
  "templateId": "dynamichosturl",
  "title": "Route to keyvault",
  "parameters": {
    "x-ms-apimTemplateParameter.urlTemplate": "https://@connectionParameters('keyVaultName').vault.azure.net"
  }
}
```

When using `dynamichosturl`, set `host` in swagger to a placeholder that will be overridden:
```json
"host": "placeholder.service.com"
```

### setheader

Injects or overrides a request header.

```json
{
  "templateId": "setheader",
  "title": "Set Content-Type Header",
  "parameters": {
    "x-ms-apimTemplateParameter.name": "Content-Type",
    "x-ms-apimTemplateParameter.value": "application/json",
    "x-ms-apimTemplateParameter.existsAction": "override",
    "x-ms-apimTemplateParameter.newValue": "application/json"
  }
}
```

**Common use — Bearer token from connection parameter:**
```json
{
  "templateId": "setheader",
  "title": "Set Authorization Header",
  "parameters": {
    "x-ms-apimTemplateParameter.name": "Authorization",
    "x-ms-apimTemplateParameter.value": "Bearer @connectionParameters('api_key')",
    "x-ms-apimTemplateParameter.existsAction": "override"
  }
}
```

**`existsAction` values:**
- `"override"` — Replace existing header
- `"skip"` — Keep existing header
- `"append"` — Add as additional header value

### setqueryparameter

Adds a default query parameter to all requests.

```json
{
  "templateId": "setqueryparameter",
  "title": "Set API Version",
  "parameters": {
    "x-ms-apimTemplateParameter.name": "api-version",
    "x-ms-apimTemplateParameter.value": "2024-01-01",
    "x-ms-apimTemplateParameter.existsAction": "override"
  }
}
```

### routerequesttoendpoint

Redirects requests to a different backend path or URL.

```json
{
  "templateId": "routerequesttoendpoint",
  "title": "Route to v2 endpoint",
  "parameters": {
    "x-ms-apimTemplateParameter.newPath": "/api/v2/@connectionParameters('endpoint')",
    "x-ms-apimTemplateParameter.httpMethod": "@Request.OriginalHTTPMethod"
  }
}
```

### setproperty

Sets or modifies a property in the request or response body.

```json
{
  "templateId": "setproperty",
  "title": "Set request property",
  "parameters": {
    "x-ms-apimTemplateParameter.newPath": "body.$.format",
    "x-ms-apimTemplateParameter.newValue": "json"
  }
}
```

### stringreplace

Replaces strings in request or response content.

```json
{
  "templateId": "stringreplace",
  "title": "Fix response URLs",
  "parameters": {
    "x-ms-apimTemplateParameter.target": "body",
    "x-ms-apimTemplateParameter.oldValue": "http://",
    "x-ms-apimTemplateParameter.newValue": "https://"
  }
}
```

### stringtoarray

Converts a delimited string into an array.

```json
{
  "templateId": "stringtoarray",
  "title": "Convert tags to array",
  "parameters": {
    "x-ms-apimTemplateParameter.propertyPath": "body.$.tags",
    "x-ms-apimTemplateParameter.delimiter": ","
  }
}
```

### convertarraytoobject

Converts an array of items into a keyed object.

```json
{
  "templateId": "convertarraytoobject",
  "title": "Convert array to keyed object",
  "parameters": {
    "x-ms-apimTemplateParameter.propertyPath": "body.$.items",
    "x-ms-apimTemplateParameter.keyProperty": "id"
  }
}
```

### convertobjecttoarray

Converts a keyed object into an array of items.

```json
{
  "templateId": "convertobjecttoarray",
  "title": "Convert object to array",
  "parameters": {
    "x-ms-apimTemplateParameter.propertyPath": "body.$.data"
  }
}
```

### pollingtrigger

Configures polling trigger behavior (interval, state tracking).

```json
{
  "templateId": "pollingtrigger",
  "title": "Poll for new items",
  "parameters": {
    "x-ms-apimTemplateParameter.triggerConfig": {
      "type": "polling",
      "interval": "PT1M"
    }
  }
}
```

### updatenextlink

Fixes pagination `nextLink` URLs that need routing through the connector proxy.

```json
{
  "templateId": "updatenextlink",
  "title": "Fix pagination links",
  "parameters": {
    "x-ms-apimTemplateParameter.linkedProperty": "@odata.nextLink"
  }
}
```

### encodepropertyvalue

URL-encodes a property value.

```json
{
  "templateId": "encodepropertyvalue",
  "title": "Encode file path",
  "parameters": {
    "x-ms-apimTemplateParameter.propertyPath": "body.$.filePath"
  }
}
```

### setvaluefromurl

Sets a parameter value by fetching it from an external URL.

```json
{
  "templateId": "setvaluefromurl",
  "title": "Fetch config from URL",
  "parameters": {
    "x-ms-apimTemplateParameter.url": "https://config.service.com/settings",
    "x-ms-apimTemplateParameter.destinationProperty": "body.$.config"
  }
}
```

---

## Combining Multiple Policy Templates

You can use multiple policy templates together. They execute in order:

```json
"policyTemplateInstances": [
  {
    "templateId": "dynamichosturl",
    "title": "Route to user instance",
    "parameters": {
      "x-ms-apimTemplateParameter.urlTemplate": "https://@connectionParameters('instance').myservice.com"
    }
  },
  {
    "templateId": "setheader",
    "title": "Set Authorization",
    "parameters": {
      "x-ms-apimTemplateParameter.name": "Authorization",
      "x-ms-apimTemplateParameter.value": "Bearer @connectionParameters('api_key')",
      "x-ms-apimTemplateParameter.existsAction": "override"
    }
  },
  {
    "templateId": "setheader",
    "title": "Set Accept Header",
    "parameters": {
      "x-ms-apimTemplateParameter.name": "Accept",
      "x-ms-apimTemplateParameter.value": "application/json",
      "x-ms-apimTemplateParameter.existsAction": "override"
    }
  }
]
```

---

## Referencing Connection Parameters

Use `@connectionParameters('paramName')` to reference values from connection parameters:

```
@connectionParameters('api_key')          → value of the api_key parameter
@connectionParameters('instanceName')     → value of the instanceName parameter
```

These references work in policy template `parameters` values and in `dynamichosturl` URL templates.
