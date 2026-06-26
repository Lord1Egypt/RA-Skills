# OpenAPI Extensions Reference

Complete reference for Power Platform `x-ms-*` OpenAPI extensions used in `apiDefinition.swagger.json`.

**Source:** [Microsoft Docs — OpenAPI Extensions](https://learn.microsoft.com/en-us/connectors/custom-connectors/openapi-extensions)

---

## Display & Visibility Extensions

### summary (standard OpenAPI)

Title for the action shown in the designer. Use sentence case.

```json
"post": {
  "summary": "Send an email",
  "operationId": "SendEmail"
}
```

### x-ms-summary

Display name for parameters and schema properties. Use Title Case.

```json
{
  "name": "recipient",
  "in": "query",
  "type": "string",
  "x-ms-summary": "Recipient Email",
  "description": "The email address to send to"
}
```

For schema properties:

```json
"properties": {
  "score": {
    "type": "number",
    "format": "float",
    "x-ms-summary": "Sentiment Score",
    "description": "A value between 0 and 1 indicating sentiment"
  }
}
```

### x-ms-visibility

Controls how operations and parameters appear in the designer.

| Value | Behavior |
|-------|----------|
| `"important"` | Always shown first to the user |
| `"advanced"` | Hidden under "Show advanced options" menu |
| `"internal"` | Hidden from user. **Must** have a default value if also `required` |
| *(absent)* | Displayed normally |

```json
{
  "name": "api-version",
  "in": "query",
  "type": "string",
  "default": "2024-01-01",
  "required": true,
  "x-ms-visibility": "internal",
  "x-ms-summary": "API Version"
}
```

---

## Trigger Extensions

### x-ms-trigger

Marks an operation as a trigger. Without this, the operation is treated as an action.

| Value | Description |
|-------|-------------|
| `"single"` | Returns a single object response |
| `"batch"` | Returns an array response |

```json
"post": {
  "operationId": "OnNewItem",
  "summary": "When a new item is created",
  "x-ms-trigger": "single",
  "parameters": [...]
}
```

### x-ms-trigger-hint

User-facing hint explaining how to fire the trigger for testing.

```json
"x-ms-trigger-hint": "To see it work, add a task in Outlook."
```

### x-ms-notification-content

Defines the schema of the webhook notification payload that the external service POSTs to the callback URL. Placed at the **path level** (siblings with the HTTP methods).

```json
"/webhooks": {
  "x-ms-notification-content": {
    "description": "Webhook notification payload",
    "schema": {
      "$ref": "#/definitions/WebhookPayload"
    }
  },
  "post": {
    "operationId": "CreateWebhook",
    "x-ms-trigger": "single",
    "parameters": [...]
  }
}
```

### x-ms-notification-url

Boolean flag on a parameter/field indicating that the platform should inject the callback URL here. Used inside the webhook registration request body.

```json
"schema": {
  "type": "object",
  "properties": {
    "callbackUrl": {
      "type": "string",
      "x-ms-notification-url": true,
      "x-ms-visibility": "internal"
    }
  }
}
```

### x-ms-operation-context

Simulates trigger firing for testing trigger-dependent flows.

```json
"x-ms-operation-context": {
  "simulate": {
    "operationId": "GetItems_V2",
    "parameters": { "$top": 1 }
  }
}
```

---

## Dynamic Values & Schema Extensions

### x-ms-dynamic-values

Populates a dropdown list from another operation's response (e.g., list of folders, categories).

```json
{
  "name": "folderId",
  "in": "query",
  "type": "string",
  "x-ms-summary": "Folder",
  "x-ms-dynamic-values": {
    "operationId": "ListFolders",
    "value-path": "id",
    "value-title": "name",
    "value-collection": "folders",
    "parameters": {
      "accountId": { "parameter": "accountId" }
    }
  }
}
```

| Property | Required | Description |
|----------|----------|-------------|
| `operationId` | Yes | Operation that returns the list |
| `parameters` | Yes | Input parameters for the dynamic operation |
| `value-collection` | No | Path to array in response. Omit if response IS the array |
| `value-path` | No | Path to value within each item |
| `value-title` | No | Path to display text within each item |

### x-ms-dynamic-list

Enhanced version of `x-ms-dynamic-values` with unambiguous parameter references. Use **both** `x-ms-dynamic-values` and `x-ms-dynamic-list` together for forward compatibility.

```json
"x-ms-dynamic-list": {
  "operationId": "ListFolders",
  "itemsPath": "folders",
  "itemValuePath": "id",
  "itemTitlePath": "name",
  "parameters": {
    "accountId": {
      "parameterReference": "body/accountId"
    }
  }
}
```

Key differences from `x-ms-dynamic-values`:
- Uses `itemsPath` instead of `value-collection`
- Uses `itemValuePath` instead of `value-path`
- Uses `itemTitlePath` instead of `value-title`
- Uses `parameterReference` (full path) instead of `parameter` (name only)

### x-ms-dynamic-schema

Dynamic schema — the form changes based on a user's prior selection (e.g., selecting a table changes available columns).

```json
"schema": {
  "type": "object",
  "x-ms-dynamic-schema": {
    "operationId": "GetTableSchema",
    "parameters": {
      "tableId": { "parameter": "tableId" }
    },
    "value-path": "schema"
  }
}
```

### x-ms-dynamic-properties

Enhanced version of `x-ms-dynamic-schema` with unambiguous parameter references. Use **both** together.

```json
"x-ms-dynamic-properties": {
  "operationId": "GetTableSchema",
  "parameters": {
    "tableId": {
      "parameterReference": "body/tableId"
    }
  },
  "itemValuePath": "schema"
}
```

---

## Connector & Operation Metadata Extensions

### x-ms-connector-metadata

**Required** at the swagger root level. Provides metadata for the connector listing.

```json
"x-ms-connector-metadata": [
  { "propertyName": "Website", "propertyValue": "https://myservice.com" },
  { "propertyName": "Privacy policy", "propertyValue": "https://myservice.com/privacy" },
  { "propertyName": "Categories", "propertyValue": "AI;Business Intelligence" }
]
```

Categories must be semicolon-separated. Common values: `AI`, `Business Intelligence`, `Business Management`, `Collaboration`, `Commerce`, `Communication`, `Content and Files`, `Data`, `Finance`, `Human Resources`, `IT Operations`, `Internet of Things`, `Lifestyle and Entertainment`, `Marketing`, `Productivity`, `Sales and CRM`, `Security`, `Social Media`, `Website`.

### x-ms-api-annotation

Versioning and lifecycle management for operations.

```json
"x-ms-api-annotation": {
  "family": "ListItems",
  "revision": 2,
  "status": "Production",
  "replacement": {
    "api": "MyServiceV2",
    "operationId": "ListItems_V2"
  }
}
```

### x-ms-capabilities

At connector level — declares test connection support:

```json
"x-ms-capabilities": {
  "testConnection": {
    "operationId": "GetCurrentUser"
  }
}
```

At operation level — declares chunked upload support:

```json
"x-ms-capabilities": {
  "chunkTransfer": true
}
```

### x-ms-url-encoding

For path parameters that need double URL encoding (e.g., paths with `/` in them).

```json
{
  "name": "filePath",
  "in": "path",
  "type": "string",
  "x-ms-url-encoding": "double"
}
```

---

## Copilot Studio / AI Extensions

### x-ms-name-for-model

LLM-friendly operation name, typically snake_case. Helps Copilot Studio identify the right action.

```json
"x-ms-name-for-model": "search_documents"
```

### x-ms-description-for-model

LLM-friendly description with usage context and constraints.

```json
"x-ms-description-for-model": "Searches for documents matching the query. Use when user asks to find or look up documents. Returns max 10 results."
```

### x-ms-safe-operation

Marks a POST operation as non-modifying (safe to call without user confirmation in Copilot).

```json
"x-ms-safe-operation": true
```

### x-ms-media-kind

Declares that an operation deals with media content.

```json
"x-ms-media-kind": "image"
```

Values: `"image"`, `"audio"`

### x-ms-no-generic-test

Skips automatic generic testing for an operation during certification.

```json
"x-ms-no-generic-test": true
```

---

## Extended Format Types

Power Platform extends standard Swagger `format` values:

| Format | Type | Description |
|--------|------|-------------|
| `date-no-tz` | `string` | Date without timezone |
| `email` | `string` | Email address with validation |
| `html` | `string` | Rich HTML content (renders in designer) |
| `uri` | `string` | URI/URL with validation |
| `uuid` | `string` | UUID/GUID format |
| `byte` | `string` | Base64-encoded binary |
| `binary` | `string` | Raw binary content |
