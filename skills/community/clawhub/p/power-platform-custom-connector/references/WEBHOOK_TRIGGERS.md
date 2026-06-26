# Webhook Triggers Reference

Webhook trigger patterns for Power Platform custom connectors. Webhooks allow flows to be triggered when an external service sends a notification.

**Source:** [Microsoft Docs — Use a webhook as a trigger](https://learn.microsoft.com/en-us/connectors/custom-connectors/create-webhook-trigger)

---

## How Webhook Triggers Work

1. **Registration:** When a user creates a flow with the trigger, the platform POSTs to your webhook registration endpoint, including a callback URL
2. **Notification:** When the event occurs, the external service POSTs the event data to the callback URL
3. **Deletion:** When the user deletes/modifies the flow, the platform DELETEs the webhook using the URL from the `Location` header

---

## Required Swagger Components

Three parts are needed in `apiDefinition.swagger.json`:

### 1. Webhook Registration (POST)

```json
"/webhooks": {
  "x-ms-notification-content": {
    "description": "Webhook event payload",
    "schema": {
      "$ref": "#/definitions/WebhookEvent"
    }
  },
  "post": {
    "operationId": "OnNewEvent",
    "summary": "When an event occurs",
    "description": "Triggers when a new event is created in the service.",
    "x-ms-trigger": "single",
    "x-ms-trigger-hint": "To see it work, create a new event in the service.",
    "parameters": [
      {
        "name": "body",
        "in": "body",
        "required": true,
        "schema": {
          "$ref": "#/definitions/WebhookRegistrationRequest"
        }
      }
    ],
    "responses": {
      "201": {
        "description": "Webhook created"
      }
    }
  }
}
```

### 2. Webhook Deletion (DELETE)

```json
"/webhooks/{webhookId}": {
  "delete": {
    "operationId": "DeleteWebhook",
    "summary": "Delete webhook",
    "description": "Removes the webhook registration.",
    "x-ms-visibility": "internal",
    "parameters": [
      {
        "name": "webhookId",
        "in": "path",
        "required": true,
        "type": "string",
        "description": "ID of the webhook to delete"
      }
    ],
    "responses": {
      "200": { "description": "Webhook deleted" }
    }
  }
}
```

### 3. Definitions

```json
"definitions": {
  "WebhookRegistrationRequest": {
    "type": "object",
    "required": ["callbackUrl"],
    "properties": {
      "callbackUrl": {
        "type": "string",
        "x-ms-notification-url": true,
        "x-ms-visibility": "internal",
        "description": "Callback URL for webhook notifications"
      },
      "eventType": {
        "type": "string",
        "x-ms-summary": "Event Type",
        "description": "Type of event to subscribe to",
        "enum": ["created", "updated", "deleted"]
      }
    }
  },
  "WebhookEvent": {
    "type": "object",
    "properties": {
      "id": {
        "type": "string",
        "x-ms-summary": "Event ID"
      },
      "type": {
        "type": "string",
        "x-ms-summary": "Event Type"
      },
      "data": {
        "type": "object",
        "x-ms-summary": "Event Data"
      },
      "timestamp": {
        "type": "string",
        "format": "date-time",
        "x-ms-summary": "Timestamp"
      }
    }
  }
}
```

---

## Key Extension Properties

| Extension | Location | Purpose |
|-----------|----------|---------|
| `x-ms-trigger` | On the POST operation | `"single"` (object response) or `"batch"` (array response) |
| `x-ms-trigger-hint` | On the POST operation | User instruction for testing |
| `x-ms-notification-content` | At the path level (sibling to `post`) | Schema of the notification payload |
| `x-ms-notification-url` | On the callback URL property | Tells the platform to inject the callback URL here |
| `x-ms-visibility: "internal"` | On the callback URL property | Hides callback URL from the user |

---

## Critical: Location Header Requirement

The API **must** return a `Location` HTTP header in the 201 response when the webhook is created. This URL is used by the platform to DELETE the webhook later.

Example response from the API:
```http
HTTP/1.1 201 Created
Location: https://api.myservice.com/webhooks/hook_abc123
Content-Type: application/json

{
  "id": "hook_abc123",
  "active": true
}
```

Without the `Location` header, the platform cannot clean up webhooks when flows are deleted or modified.

---

## Complete GitHub Webhook Example

From the Microsoft tutorial — a complete webhook trigger for GitHub push events:

### Registration Endpoint

```json
"/repos/{owner}/{repo}/hooks": {
  "x-ms-notification-content": {
    "description": "Details for Webhook",
    "schema": {
      "$ref": "#/definitions/WebhookPushResponse"
    }
  },
  "post": {
    "description": "Creates a Github webhook",
    "summary": "Triggers when a PUSH event occurs",
    "operationId": "webhook-trigger",
    "x-ms-trigger": "single",
    "parameters": [
      {
        "name": "owner",
        "in": "path",
        "description": "Name of the owner of targeted repository",
        "required": true,
        "type": "string"
      },
      {
        "name": "repo",
        "in": "path",
        "description": "Name of the repository",
        "required": true,
        "type": "string"
      },
      {
        "name": "body",
        "in": "body",
        "description": "Webhook configuration",
        "schema": {
          "$ref": "#/definitions/WebhookRequestBody"
        }
      }
    ],
    "responses": {
      "201": {
        "description": "Created",
        "schema": {
          "$ref": "#/definitions/WebhookCreationResponse"
        }
      }
    }
  }
}
```

### Deletion Endpoint

```json
"/repos/{owner}/{repo}/hooks/{hook_Id}": {
  "delete": {
    "description": "Deletes a Github webhook",
    "operationId": "DeleteTrigger",
    "parameters": [
      {
        "name": "owner",
        "in": "path",
        "required": true,
        "type": "string"
      },
      {
        "name": "repo",
        "in": "path",
        "required": true,
        "type": "string"
      },
      {
        "name": "hook_Id",
        "in": "path",
        "required": true,
        "type": "string"
      }
    ],
    "responses": {
      "200": { "description": "Deleted" }
    }
  }
}
```

### Webhook Registration Body

```json
"WebhookRequestBody": {
  "type": "object",
  "required": ["name", "config"],
  "properties": {
    "name": {
      "type": "string",
      "default": "web",
      "x-ms-visibility": "internal"
    },
    "active": {
      "type": "boolean",
      "default": true,
      "x-ms-visibility": "internal"
    },
    "events": {
      "type": "array",
      "items": { "type": "string" },
      "default": ["push"],
      "x-ms-visibility": "internal"
    },
    "config": {
      "type": "object",
      "required": ["url"],
      "properties": {
        "url": {
          "type": "string",
          "x-ms-notification-url": true,
          "x-ms-visibility": "internal"
        }
      }
    }
  }
}
```

Note how `name`, `active`, `events`, and `config.url` are all marked `x-ms-visibility: "internal"` — the user only sees the `owner` and `repo` path parameters.

---

## Batch Triggers

For APIs that return an array of events, use `"x-ms-trigger": "batch"` and define the response as an array:

```json
"post": {
  "operationId": "OnNewItems",
  "summary": "When new items are added",
  "x-ms-trigger": "batch",
  "responses": {
    "200": {
      "description": "Success",
      "schema": {
        "type": "array",
        "items": { "$ref": "#/definitions/Item" }
      }
    }
  }
}
```

---

## Polling Trigger Alternative

If the API doesn't support webhooks, use polling with `x-ms-operation-context`:

```json
"get": {
  "operationId": "GetNewItems",
  "summary": "When a new item is created (polling)",
  "x-ms-trigger": "batch",
  "x-ms-trigger-hint": "Polls every few minutes for new items.",
  "parameters": [
    {
      "name": "since",
      "in": "query",
      "type": "string",
      "format": "date-time",
      "x-ms-visibility": "internal"
    }
  ]
}
```

The platform handles the polling interval automatically.
