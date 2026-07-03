# Pipedrive Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `pipedrive`

x402 availability: not enabled for this product.

## `convert_lead`

Action slug: `convert-lead`

Price: `5` credits

Convert a lead by UUID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `data` | `object` | no | Raw conversion body. |
| `lead_id` | `string` | yes | Lead UUID. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |

Sample parameters:

```json
{
  "data": {},
  "lead_id": "example lead id",
  "options": {}
}
```

Generated JSON parameter schema:

```json
{
  "data": {
    "description": "Raw conversion body.",
    "required": false,
    "type": "object"
  },
  "lead_id": {
    "description": "Lead UUID.",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  }
}
```

## `create_lead`

Action slug: `create-lead`

Price: `5` credits

Create a lead. Requires add permission and title plus person_id or organization_id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `data` | `object` | no | Raw JSON body. Keys here win over convenience fields. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `organization_id` | `integer` | no | Associated organization id. Supply person_id or organization_id. |
| `owner_id` | `integer` | no | Owner user id. |
| `person_id` | `integer` | no | Associated person id. Supply person_id or organization_id. |
| `title` | `string` | yes | Lead title. |
| `value` | `object` | no | Lead monetary value object with amount and currency. |

Sample parameters:

```json
{
  "data": {},
  "options": {},
  "organization_id": 1,
  "owner_id": 1,
  "person_id": 1,
  "title": "example title",
  "value": {}
}
```

Generated JSON parameter schema:

```json
{
  "data": {
    "description": "Raw JSON body. Keys here win over convenience fields.",
    "required": false,
    "type": "object"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "organization_id": {
    "description": "Associated organization id. Supply person_id or organization_id.",
    "required": false,
    "type": "integer"
  },
  "owner_id": {
    "description": "Owner user id.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Associated person id. Supply person_id or organization_id.",
    "required": false,
    "type": "integer"
  },
  "title": {
    "description": "Lead title.",
    "required": true,
    "type": "string"
  },
  "value": {
    "description": "Lead monetary value object with amount and currency.",
    "required": false,
    "type": "object"
  }
}
```

## `create_note`

Action slug: `create-note`

Price: `5` credits

Create a note linked to one record. Requires add permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | `string` | yes | Note content. |
| `data` | `object` | no | Raw JSON body. Keys here win over convenience fields. |
| `deal_id` | `integer` | no | Associated deal id. |
| `lead_id` | `string` | no | Associated lead UUID. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `organization_id` | `integer` | no | Public organization id; connector sends org_id where required. |
| `person_id` | `integer` | no | Associated person id. |

Sample parameters:

```json
{
  "content": "Draft marketing copy to check for banned phrases.",
  "data": {},
  "deal_id": 1,
  "lead_id": "example lead id",
  "options": {},
  "organization_id": 1,
  "person_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "content": {
    "description": "Note content.",
    "required": true,
    "type": "string"
  },
  "data": {
    "description": "Raw JSON body. Keys here win over convenience fields.",
    "required": false,
    "type": "object"
  },
  "deal_id": {
    "description": "Associated deal id.",
    "required": false,
    "type": "integer"
  },
  "lead_id": {
    "description": "Associated lead UUID.",
    "required": false,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "organization_id": {
    "description": "Public organization id; connector sends org_id where required.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Associated person id.",
    "required": false,
    "type": "integer"
  }
}
```

## `create_record`

Action slug: `create-record`

Price: `5` credits

Create one core resource record. Requires add permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `data` | `object` | no | Raw JSON body. Keys here win over convenience fields. |
| `deal_id` | `integer` | no | Associated deal id for activity records. |
| `name` | `string` | no | Person, organization, product, or file name. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `organization_id` | `integer` | no | Public organization id; connector sends org_id where required. |
| `owner_id` | `integer` | no | Owner user id. |
| `person_id` | `integer` | no | Associated person id. |
| `pipeline_id` | `integer` | no | Pipeline id for deals. |
| `resource` | `string` | yes | Core resource to create. |
| `stage_id` | `integer` | no | Stage id for deals. |
| `subject` | `string` | no | Activity subject. |
| `title` | `string` | no | Deal title. |
| `value` | `object` | no | Deal monetary amount. Accepts either a number or object form {amount, currency}; object form is normalized to numeric value plus currency. |

Sample parameters:

```json
{
  "data": {},
  "deal_id": 1,
  "name": "example name",
  "options": {},
  "organization_id": 1,
  "owner_id": 1,
  "person_id": 1,
  "pipeline_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "data": {
    "description": "Raw JSON body. Keys here win over convenience fields.",
    "required": false,
    "type": "object"
  },
  "deal_id": {
    "description": "Associated deal id for activity records.",
    "required": false,
    "type": "integer"
  },
  "name": {
    "description": "Person, organization, product, or file name.",
    "required": false,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "organization_id": {
    "description": "Public organization id; connector sends org_id where required.",
    "required": false,
    "type": "integer"
  },
  "owner_id": {
    "description": "Owner user id.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Associated person id.",
    "required": false,
    "type": "integer"
  },
  "pipeline_id": {
    "description": "Pipeline id for deals.",
    "required": false,
    "type": "integer"
  },
  "resource": {
    "description": "Core resource to create.",
    "enum": [
      "deal",
      "person",
      "organization",
      "activity",
      "product"
    ],
    "required": true,
    "type": "string"
  },
  "stage_id": {
    "description": "Stage id for deals.",
    "required": false,
    "type": "integer"
  },
  "subject": {
    "description": "Activity subject.",
    "required": false,
    "type": "string"
  },
  "title": {
    "description": "Deal title.",
    "required": false,
    "type": "string"
  },
  "value": {
    "description": "Deal monetary amount. Accepts either a number or object form {amount, currency}; object form is normalized to numeric value plus currency.",
    "required": false,
    "type": "object"
  }
}
```

## `create_webhook`

Action slug: `create-webhook`

Price: `5` credits

Subscribe an HTTPS URL to Pipedrive change events. Requires add permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `event_action` | `string` | yes | Trigger action. |
| `event_object` | `string` | yes | Resource to watch. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `subscription_url` | `string` | yes | Publicly reachable HTTPS URL Pipedrive will POST events to. |
| `user_id` | `integer` | no | Owner user for the webhook. |
| `webhook_name` | `string` | no | Human-readable webhook name. |
| `webhook_version` | `string` | no | Payload version. Defaults to 2.0. |

Sample parameters:

```json
{
  "event_action": "create",
  "event_object": "activity",
  "options": {},
  "subscription_url": "https://example.com",
  "user_id": 1,
  "webhook_name": "example webhook name",
  "webhook_version": "1.0"
}
```

Generated JSON parameter schema:

```json
{
  "event_action": {
    "description": "Trigger action.",
    "enum": [
      "create",
      "change",
      "delete",
      "*"
    ],
    "required": true,
    "type": "string"
  },
  "event_object": {
    "description": "Resource to watch.",
    "enum": [
      "activity",
      "deal",
      "lead",
      "note",
      "organization",
      "person",
      "pipeline",
      "product",
      "stage",
      "user",
      "*"
    ],
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "subscription_url": {
    "description": "Publicly reachable HTTPS URL Pipedrive will POST events to.",
    "required": true,
    "type": "string"
  },
  "user_id": {
    "description": "Owner user for the webhook.",
    "required": false,
    "type": "integer"
  },
  "webhook_name": {
    "description": "Human-readable webhook name.",
    "required": false,
    "type": "string"
  },
  "webhook_version": {
    "description": "Payload version. Defaults to 2.0.",
    "enum": [
      "1.0",
      "2.0"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `delete_file`

Action slug: `delete-file`

Price: `5` credits

Delete a Pipedrive file. Requires delete permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `pipedrive_file_id` | `integer` | yes | Pipedrive file id. |

Sample parameters:

```json
{
  "pipedrive_file_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "pipedrive_file_id": {
    "description": "Pipedrive file id.",
    "required": true,
    "type": "integer"
  }
}
```

## `delete_lead`

Action slug: `delete-lead`

Price: `5` credits

Delete a lead by UUID. Requires delete permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `lead_id` | `string` | yes | Lead UUID. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |

Sample parameters:

```json
{
  "lead_id": "example lead id",
  "options": {}
}
```

Generated JSON parameter schema:

```json
{
  "lead_id": {
    "description": "Lead UUID.",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  }
}
```

## `delete_note`

Action slug: `delete-note`

Price: `5` credits

Delete a note by id. Requires delete permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `note_id` | `integer` | yes | Note id. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |

Sample parameters:

```json
{
  "note_id": 1,
  "options": {}
}
```

Generated JSON parameter schema:

```json
{
  "note_id": {
    "description": "Note id.",
    "required": true,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  }
}
```

## `delete_record`

Action slug: `delete-record`

Price: `5` credits

Delete one core resource record. Requires delete permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `activity_id` | `integer` | no | Activity id when resource is activity. |
| `deal_id` | `integer` | no | Deal id when resource is deal. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `organization_id` | `integer` | no | Organization id when resource is organization. |
| `person_id` | `integer` | no | Person id when resource is person. |
| `product_id` | `integer` | no | Product id when resource is product. |
| `resource` | `string` | yes | Core resource to delete. |

Sample parameters:

```json
{
  "activity_id": 1,
  "deal_id": 1,
  "options": {},
  "organization_id": 1,
  "person_id": 1,
  "product_id": 1,
  "resource": "deal"
}
```

Generated JSON parameter schema:

```json
{
  "activity_id": {
    "description": "Activity id when resource is activity.",
    "required": false,
    "type": "integer"
  },
  "deal_id": {
    "description": "Deal id when resource is deal.",
    "required": false,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "organization_id": {
    "description": "Organization id when resource is organization.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Person id when resource is person.",
    "required": false,
    "type": "integer"
  },
  "product_id": {
    "description": "Product id when resource is product.",
    "required": false,
    "type": "integer"
  },
  "resource": {
    "description": "Core resource to delete.",
    "enum": [
      "deal",
      "person",
      "organization",
      "activity",
      "product"
    ],
    "required": true,
    "type": "string"
  }
}
```

## `delete_webhook`

Action slug: `delete-webhook`

Price: `5` credits

Delete a Pipedrive webhook subscription. Requires delete permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `webhook_id` | `integer` | yes | Webhook id. |

Sample parameters:

```json
{
  "options": {},
  "webhook_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "webhook_id": {
    "description": "Webhook id.",
    "required": true,
    "type": "integer"
  }
}
```

## `download_file`

Action slug: `download-file`

Price: `5` credits

Download a Pipedrive file into AgentPMT File Manager.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `attachment_expiration_minutes` | `integer` | no | Signed URL TTL minutes from 10 to 1440. |
| `ingest_expiration_days` | `integer` | no | File Manager expiration days from 1 to 7. |
| `pipedrive_file_id` | `integer` | yes | Pipedrive file id. |

Sample parameters:

```json
{
  "attachment_expiration_minutes": 10,
  "ingest_expiration_days": 1,
  "pipedrive_file_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "attachment_expiration_minutes": {
    "description": "Signed URL TTL minutes from 10 to 1440.",
    "maximum": 1440,
    "minimum": 10,
    "required": false,
    "type": "integer"
  },
  "ingest_expiration_days": {
    "description": "File Manager expiration days from 1 to 7.",
    "maximum": 7,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "pipedrive_file_id": {
    "description": "Pipedrive file id.",
    "required": true,
    "type": "integer"
  }
}
```

## `get_file`

Action slug: `get-file`

Price: `5` credits

Fetch Pipedrive file metadata by id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `pipedrive_file_id` | `integer` | yes | Pipedrive file id. |

Sample parameters:

```json
{
  "options": {},
  "pipedrive_file_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "pipedrive_file_id": {
    "description": "Pipedrive file id.",
    "required": true,
    "type": "integer"
  }
}
```

## `get_lead`

Action slug: `get-lead`

Price: `5` credits

Fetch one lead by UUID.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `lead_id` | `string` | yes | Lead UUID. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |

Sample parameters:

```json
{
  "lead_id": "example lead id",
  "options": {}
}
```

Generated JSON parameter schema:

```json
{
  "lead_id": {
    "description": "Lead UUID.",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  }
}
```

## `get_note`

Action slug: `get-note`

Price: `5` credits

Fetch one note by id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `note_id` | `integer` | yes | Note id. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |

Sample parameters:

```json
{
  "note_id": 1,
  "options": {}
}
```

Generated JSON parameter schema:

```json
{
  "note_id": {
    "description": "Note id.",
    "required": true,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  }
}
```

## `get_pipeline`

Action slug: `get-pipeline`

Price: `5` credits

Fetch one pipeline by id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `pipeline_id` | `integer` | yes | Pipeline id. |

Sample parameters:

```json
{
  "options": {},
  "pipeline_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "pipeline_id": {
    "description": "Pipeline id.",
    "required": true,
    "type": "integer"
  }
}
```

## `get_record`

Action slug: `get-record`

Price: `5` credits

Fetch one core resource record by id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `activity_id` | `integer` | no | Activity id when resource is activity. |
| `custom_fields` | `array` | no | Custom field hash keys to return. |
| `deal_id` | `integer` | no | Deal id when resource is deal. |
| `include` | `array` | no | Public alias mapped to Pipedrive include_fields where supported. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `organization_id` | `integer` | no | Organization id when resource is organization. |
| `person_id` | `integer` | no | Person id when resource is person. |
| `product_id` | `integer` | no | Product id when resource is product. |
| `resource` | `string` | yes | Core resource to fetch. |

Sample parameters:

```json
{
  "activity_id": 1,
  "custom_fields": [
    "example custom field"
  ],
  "deal_id": 1,
  "include": [
    "example include"
  ],
  "options": {},
  "organization_id": 1,
  "person_id": 1,
  "product_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "activity_id": {
    "description": "Activity id when resource is activity.",
    "required": false,
    "type": "integer"
  },
  "custom_fields": {
    "description": "Custom field hash keys to return.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "deal_id": {
    "description": "Deal id when resource is deal.",
    "required": false,
    "type": "integer"
  },
  "include": {
    "description": "Public alias mapped to Pipedrive include_fields where supported.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "organization_id": {
    "description": "Organization id when resource is organization.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Person id when resource is person.",
    "required": false,
    "type": "integer"
  },
  "product_id": {
    "description": "Product id when resource is product.",
    "required": false,
    "type": "integer"
  },
  "resource": {
    "description": "Core resource to fetch.",
    "enum": [
      "deal",
      "person",
      "organization",
      "activity",
      "product"
    ],
    "required": true,
    "type": "string"
  }
}
```

## `get_stage`

Action slug: `get-stage`

Price: `5` credits

Fetch one stage by id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `stage_id` | `integer` | yes | Stage id. |

Sample parameters:

```json
{
  "options": {},
  "stage_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "stage_id": {
    "description": "Stage id.",
    "required": true,
    "type": "integer"
  }
}
```

## `item_search`

Action slug: `item-search`

Price: `5` credits

Search across Pipedrive item types by term.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | `string` | no | Cursor for pagination. |
| `exact_match` | `boolean` | no | Search for an exact phrase only. |
| `fields` | `array` | no | Fields to search in. |
| `item_types` | `array` | no | Item types to include. |
| `limit` | `integer` | no | Page size from 1 to 500. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `search_for_related_items` | `boolean` | no | Include related items in results. |
| `term` | `string` | yes | Search term. |

Sample parameters:

```json
{
  "cursor": "example cursor",
  "exact_match": true,
  "fields": [
    "example field"
  ],
  "item_types": [
    "deal"
  ],
  "limit": 1,
  "options": {},
  "search_for_related_items": true,
  "term": "example term"
}
```

Generated JSON parameter schema:

```json
{
  "cursor": {
    "description": "Cursor for pagination.",
    "required": false,
    "type": "string"
  },
  "exact_match": {
    "description": "Search for an exact phrase only.",
    "required": false,
    "type": "boolean"
  },
  "fields": {
    "description": "Fields to search in.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "item_types": {
    "description": "Item types to include.",
    "items": {
      "enum": [
        "deal",
        "person",
        "organization",
        "product",
        "lead",
        "file",
        "activity",
        "project"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "limit": {
    "description": "Page size from 1 to 500.",
    "maximum": 500,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "search_for_related_items": {
    "description": "Include related items in results.",
    "required": false,
    "type": "boolean"
  },
  "term": {
    "description": "Search term.",
    "required": true,
    "type": "string"
  }
}
```

## `link_remote_file`

Action slug: `link-remote-file`

Price: `5` credits

Link a Google Drive file to a Pipedrive deal, person, or organization. Requires add permission plus an active Google Drive integration in Pipedrive.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `deal_id` | `integer` | no | Associate to this deal id. Supply exactly one of deal_id, person_id, or organization_id. |
| `file_name_override` | `string` | no | Optional file title override. |
| `organization_id` | `integer` | no | Associate to this organization id. Supply exactly one of deal_id, person_id, or organization_id. |
| `person_id` | `integer` | no | Associate to this person id. Supply exactly one of deal_id, person_id, or organization_id. |
| `remote_id` | `string` | yes | Google Drive remote file id visible to the connected Pipedrive Google Drive integration. |
| `remote_location` | `string` | yes | Remote provider. Currently only googledrive is supported. |

Sample parameters:

```json
{
  "deal_id": 1,
  "file_name_override": "example file name override",
  "organization_id": 1,
  "person_id": 1,
  "remote_id": "example remote id",
  "remote_location": "googledrive"
}
```

Generated JSON parameter schema:

```json
{
  "deal_id": {
    "description": "Associate to this deal id. Supply exactly one of deal_id, person_id, or organization_id.",
    "required": false,
    "type": "integer"
  },
  "file_name_override": {
    "description": "Optional file title override.",
    "required": false,
    "type": "string"
  },
  "organization_id": {
    "description": "Associate to this organization id. Supply exactly one of deal_id, person_id, or organization_id.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Associate to this person id. Supply exactly one of deal_id, person_id, or organization_id.",
    "required": false,
    "type": "integer"
  },
  "remote_id": {
    "description": "Google Drive remote file id visible to the connected Pipedrive Google Drive integration.",
    "required": true,
    "type": "string"
  },
  "remote_location": {
    "description": "Remote provider. Currently only googledrive is supported.",
    "enum": [
      "googledrive"
    ],
    "required": true,
    "type": "string"
  }
}
```

## `list_fields`

Action slug: `list-fields`

Price: `5` credits

List field metadata for deals, persons, organizations, activities, or products.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | `string` | no | Cursor for pagination. |
| `limit` | `integer` | no | Page size from 1 to 500. |
| `module` | `string` | yes | Module name. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |

Sample parameters:

```json
{
  "cursor": "example cursor",
  "limit": 1,
  "module": "deals",
  "options": {}
}
```

Generated JSON parameter schema:

```json
{
  "cursor": {
    "description": "Cursor for pagination.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Page size from 1 to 500.",
    "maximum": 500,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "module": {
    "description": "Module name.",
    "enum": [
      "deals",
      "persons",
      "organizations",
      "activities",
      "products"
    ],
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  }
}
```

## `list_files`

Action slug: `list-files`

Price: `5` credits

List files with optional record filters.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `activity_id` | `integer` | no | Activity filter. |
| `deal_id` | `integer` | no | Deal filter. |
| `lead_id` | `string` | no | Lead UUID filter. |
| `limit` | `integer` | no | Page size from 1 to 500. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `organization_id` | `integer` | no | Public organization id; connector sends org_id where required. |
| `person_id` | `integer` | no | Person filter. |
| `product_id` | `integer` | no | Product filter. |
| `sort_by` | `string` | no | Sort field name. |
| `sort_direction` | `string` | no | Sort direction. |
| `start` | `integer` | no | Offset for v1 pagination. |

Sample parameters:

```json
{
  "activity_id": 1,
  "deal_id": 1,
  "lead_id": "example lead id",
  "limit": 1,
  "options": {},
  "organization_id": 1,
  "person_id": 1,
  "product_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "activity_id": {
    "description": "Activity filter.",
    "required": false,
    "type": "integer"
  },
  "deal_id": {
    "description": "Deal filter.",
    "required": false,
    "type": "integer"
  },
  "lead_id": {
    "description": "Lead UUID filter.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Page size from 1 to 500.",
    "maximum": 500,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "organization_id": {
    "description": "Public organization id; connector sends org_id where required.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Person filter.",
    "required": false,
    "type": "integer"
  },
  "product_id": {
    "description": "Product filter.",
    "required": false,
    "type": "integer"
  },
  "sort_by": {
    "description": "Sort field name.",
    "required": false,
    "type": "string"
  },
  "sort_direction": {
    "description": "Sort direction.",
    "enum": [
      "asc",
      "desc"
    ],
    "required": false,
    "type": "string"
  },
  "start": {
    "description": "Offset for v1 pagination.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

## `list_leads`

Action slug: `list-leads`

Price: `5` credits

List leads with filters and pagination.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `filter_id` | `integer` | no | Filter id. |
| `limit` | `integer` | no | Page size from 1 to 500. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `organization_id` | `integer` | no | Organization filter. |
| `owner_id` | `integer` | no | Owner user id filter. |
| `person_id` | `integer` | no | Person filter. |
| `sort_by` | `string` | no | Sort field name. |
| `sort_direction` | `string` | no | Sort direction. |
| `start` | `integer` | no | Offset for v1 pagination. |

Sample parameters:

```json
{
  "filter_id": 1,
  "limit": 1,
  "options": {},
  "organization_id": 1,
  "owner_id": 1,
  "person_id": 1,
  "sort_by": "example sort by",
  "sort_direction": "asc"
}
```

Generated JSON parameter schema:

```json
{
  "filter_id": {
    "description": "Filter id.",
    "required": false,
    "type": "integer"
  },
  "limit": {
    "description": "Page size from 1 to 500.",
    "maximum": 500,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "organization_id": {
    "description": "Organization filter.",
    "required": false,
    "type": "integer"
  },
  "owner_id": {
    "description": "Owner user id filter.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Person filter.",
    "required": false,
    "type": "integer"
  },
  "sort_by": {
    "description": "Sort field name.",
    "required": false,
    "type": "string"
  },
  "sort_direction": {
    "description": "Sort direction.",
    "enum": [
      "asc",
      "desc"
    ],
    "required": false,
    "type": "string"
  },
  "start": {
    "description": "Offset for v1 pagination.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  }
}
```

## `list_notes`

Action slug: `list-notes`

Price: `5` credits

List notes with optional record filters.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `deal_id` | `integer` | no | Deal filter. |
| `lead_id` | `string` | no | Lead UUID filter. |
| `limit` | `integer` | no | Page size from 1 to 500. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `organization_id` | `integer` | no | Public organization id; connector sends org_id where required. |
| `person_id` | `integer` | no | Person filter. |
| `sort_by` | `string` | no | Sort field name. |
| `sort_direction` | `string` | no | Sort direction. |
| `start` | `integer` | no | Offset for v1 pagination. |
| `user_id` | `integer` | no | User filter. |

Sample parameters:

```json
{
  "deal_id": 1,
  "lead_id": "example lead id",
  "limit": 1,
  "options": {},
  "organization_id": 1,
  "person_id": 1,
  "sort_by": "example sort by",
  "sort_direction": "asc"
}
```

Generated JSON parameter schema:

```json
{
  "deal_id": {
    "description": "Deal filter.",
    "required": false,
    "type": "integer"
  },
  "lead_id": {
    "description": "Lead UUID filter.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Page size from 1 to 500.",
    "maximum": 500,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "organization_id": {
    "description": "Public organization id; connector sends org_id where required.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Person filter.",
    "required": false,
    "type": "integer"
  },
  "sort_by": {
    "description": "Sort field name.",
    "required": false,
    "type": "string"
  },
  "sort_direction": {
    "description": "Sort direction.",
    "enum": [
      "asc",
      "desc"
    ],
    "required": false,
    "type": "string"
  },
  "start": {
    "description": "Offset for v1 pagination.",
    "minimum": 0,
    "required": false,
    "type": "integer"
  },
  "user_id": {
    "description": "User filter.",
    "required": false,
    "type": "integer"
  }
}
```

## `list_pipelines`

Action slug: `list-pipelines`

Price: `5` credits

List pipelines.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | `string` | no | Cursor for pagination. |
| `limit` | `integer` | no | Page size from 1 to 500. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |

Sample parameters:

```json
{
  "cursor": "example cursor",
  "limit": 1,
  "options": {}
}
```

Generated JSON parameter schema:

```json
{
  "cursor": {
    "description": "Cursor for pagination.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Page size from 1 to 500.",
    "maximum": 500,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  }
}
```

## `list_records`

Action slug: `list-records`

Price: `5` credits

List one core resource: deal, person, organization, activity, or product.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | `string` | no | Cursor for v2 pagination. |
| `custom_fields` | `array` | no | Custom field hash keys to return. |
| `deal_id` | `integer` | no | Deal filter for supported resources. |
| `filter_id` | `integer` | no | Pipedrive filter id. |
| `include` | `array` | no | Public alias mapped to Pipedrive include_fields where supported. |
| `limit` | `integer` | no | Page size from 1 to 500. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `organization_id` | `integer` | no | Public organization id; connector sends org_id where required. |
| `owner_id` | `integer` | no | Owner user id filter. |
| `person_id` | `integer` | no | Person filter for supported resources. |
| `pipeline_id` | `integer` | no | Pipeline filter for deals. |
| `resource` | `string` | yes | Core resource to list. |
| `sort_by` | `string` | no | Sort field name. |
| `sort_direction` | `string` | no | Sort direction. |
| `stage_id` | `integer` | no | Stage filter for deals. |
| `status` | `string` | no | Status filter for supported resources. |
| `updated_since` | `string` | no | ISO-8601 timestamp for incremental pulls. |

Sample parameters:

```json
{
  "cursor": "example cursor",
  "custom_fields": [
    "example custom field"
  ],
  "deal_id": 1,
  "filter_id": 1,
  "include": [
    "example include"
  ],
  "limit": 1,
  "options": {},
  "organization_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "cursor": {
    "description": "Cursor for v2 pagination.",
    "required": false,
    "type": "string"
  },
  "custom_fields": {
    "description": "Custom field hash keys to return.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "deal_id": {
    "description": "Deal filter for supported resources.",
    "required": false,
    "type": "integer"
  },
  "filter_id": {
    "description": "Pipedrive filter id.",
    "required": false,
    "type": "integer"
  },
  "include": {
    "description": "Public alias mapped to Pipedrive include_fields where supported.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "limit": {
    "description": "Page size from 1 to 500.",
    "maximum": 500,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "organization_id": {
    "description": "Public organization id; connector sends org_id where required.",
    "required": false,
    "type": "integer"
  },
  "owner_id": {
    "description": "Owner user id filter.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Person filter for supported resources.",
    "required": false,
    "type": "integer"
  },
  "pipeline_id": {
    "description": "Pipeline filter for deals.",
    "required": false,
    "type": "integer"
  },
  "resource": {
    "description": "Core resource to list.",
    "enum": [
      "deal",
      "person",
      "organization",
      "activity",
      "product"
    ],
    "required": true,
    "type": "string"
  },
  "sort_by": {
    "description": "Sort field name.",
    "required": false,
    "type": "string"
  },
  "sort_direction": {
    "description": "Sort direction.",
    "enum": [
      "asc",
      "desc"
    ],
    "required": false,
    "type": "string"
  },
  "stage_id": {
    "description": "Stage filter for deals.",
    "required": false,
    "type": "integer"
  },
  "status": {
    "description": "Status filter for supported resources.",
    "required": false,
    "type": "string"
  },
  "updated_since": {
    "description": "ISO-8601 timestamp for incremental pulls.",
    "required": false,
    "type": "string"
  }
}
```

## `list_stages`

Action slug: `list-stages`

Price: `5` credits

List stages, optionally filtered by pipeline_id.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | `string` | no | Cursor for pagination. |
| `limit` | `integer` | no | Page size from 1 to 500. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `pipeline_id` | `integer` | no | Pipeline filter. |

Sample parameters:

```json
{
  "cursor": "example cursor",
  "limit": 1,
  "options": {},
  "pipeline_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "cursor": {
    "description": "Cursor for pagination.",
    "required": false,
    "type": "string"
  },
  "limit": {
    "description": "Page size from 1 to 500.",
    "maximum": 500,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "pipeline_id": {
    "description": "Pipeline filter.",
    "required": false,
    "type": "integer"
  }
}
```

## `list_users`

Action slug: `list-users`

Price: `5` credits

List Pipedrive users.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |

Sample parameters:

```json
{
  "options": {}
}
```

Generated JSON parameter schema:

```json
{
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  }
}
```

## `list_webhooks`

Action slug: `list-webhooks`

Price: `5` credits

List Pipedrive webhook subscriptions.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `user_id` | `integer` | no | Filter webhooks by user id. |

Sample parameters:

```json
{
  "options": {},
  "user_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "user_id": {
    "description": "Filter webhooks by user id.",
    "required": false,
    "type": "integer"
  }
}
```

## `search_leads`

Action slug: `search-leads`

Price: `5` credits

Search leads by term.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | `string` | no | Cursor for v2 pagination. |
| `exact_match` | `boolean` | no | Search for an exact phrase only. |
| `fields` | `array` | no | Fields to search in. |
| `include` | `array` | no | Public alias mapped to Pipedrive include_fields where supported. |
| `limit` | `integer` | no | Page size from 1 to 500. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `term` | `string` | yes | Search term. |

Sample parameters:

```json
{
  "cursor": "example cursor",
  "exact_match": true,
  "fields": [
    "example field"
  ],
  "include": [
    "example include"
  ],
  "limit": 1,
  "options": {},
  "term": "example term"
}
```

Generated JSON parameter schema:

```json
{
  "cursor": {
    "description": "Cursor for v2 pagination.",
    "required": false,
    "type": "string"
  },
  "exact_match": {
    "description": "Search for an exact phrase only.",
    "required": false,
    "type": "boolean"
  },
  "fields": {
    "description": "Fields to search in.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "include": {
    "description": "Public alias mapped to Pipedrive include_fields where supported.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "limit": {
    "description": "Page size from 1 to 500.",
    "maximum": 500,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "term": {
    "description": "Search term.",
    "required": true,
    "type": "string"
  }
}
```

## `search_records`

Action slug: `search-records`

Price: `5` credits

Search deal, person, organization, or product records by term. Activity is not searchable.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `cursor` | `string` | no | Cursor for v2 pagination. |
| `exact_match` | `boolean` | no | Search for an exact phrase only. |
| `fields` | `array` | no | Fields to search in. Allowed values depend on the resource. |
| `include` | `array` | no | Public alias mapped to Pipedrive include_fields for deal, person, and product searches. |
| `limit` | `integer` | no | Page size from 1 to 500. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `organization_id` | `integer` | no | Organization filter for deal and person searches. |
| `person_id` | `integer` | no | Person filter for deal searches. |
| `resource` | `string` | yes | Core resource to search. |
| `status` | `string` | no | Status filter for deal searches. |
| `term` | `string` | yes | Search term. |

Sample parameters:

```json
{
  "cursor": "example cursor",
  "exact_match": true,
  "fields": [
    "example field"
  ],
  "include": [
    "example include"
  ],
  "limit": 1,
  "options": {},
  "organization_id": 1,
  "person_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "cursor": {
    "description": "Cursor for v2 pagination.",
    "required": false,
    "type": "string"
  },
  "exact_match": {
    "description": "Search for an exact phrase only.",
    "required": false,
    "type": "boolean"
  },
  "fields": {
    "description": "Fields to search in. Allowed values depend on the resource.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "include": {
    "description": "Public alias mapped to Pipedrive include_fields for deal, person, and product searches.",
    "items": {
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "limit": {
    "description": "Page size from 1 to 500.",
    "maximum": 500,
    "minimum": 1,
    "required": false,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "organization_id": {
    "description": "Organization filter for deal and person searches.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Person filter for deal searches.",
    "required": false,
    "type": "integer"
  },
  "resource": {
    "description": "Core resource to search.",
    "enum": [
      "deal",
      "person",
      "organization",
      "product"
    ],
    "required": true,
    "type": "string"
  },
  "status": {
    "description": "Status filter for deal searches.",
    "required": false,
    "type": "string"
  },
  "term": {
    "description": "Search term.",
    "required": true,
    "type": "string"
  }
}
```

## `update_file`

Action slug: `update-file`

Price: `5` credits

Rename or update a Pipedrive file description. Requires edit permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `file_description` | `string` | no | New file description. |
| `file_name_override` | `string` | no | New file name. |
| `pipedrive_file_id` | `integer` | yes | Pipedrive file id. |

Sample parameters:

```json
{
  "file_description": "example file description",
  "file_name_override": "example file name override",
  "pipedrive_file_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "file_description": {
    "description": "New file description.",
    "required": false,
    "type": "string"
  },
  "file_name_override": {
    "description": "New file name.",
    "required": false,
    "type": "string"
  },
  "pipedrive_file_id": {
    "description": "Pipedrive file id.",
    "required": true,
    "type": "integer"
  }
}
```

## `update_lead`

Action slug: `update-lead`

Price: `5` credits

Update a lead by UUID. Requires edit permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `data` | `object` | no | Raw JSON body. Keys here win over convenience fields. |
| `lead_id` | `string` | yes | Lead UUID. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `title` | `string` | no | Lead title. |
| `value` | `object` | no | Lead monetary value object with amount and currency. |

Sample parameters:

```json
{
  "data": {},
  "lead_id": "example lead id",
  "options": {},
  "title": "example title",
  "value": {}
}
```

Generated JSON parameter schema:

```json
{
  "data": {
    "description": "Raw JSON body. Keys here win over convenience fields.",
    "required": false,
    "type": "object"
  },
  "lead_id": {
    "description": "Lead UUID.",
    "required": true,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "title": {
    "description": "Lead title.",
    "required": false,
    "type": "string"
  },
  "value": {
    "description": "Lead monetary value object with amount and currency.",
    "required": false,
    "type": "object"
  }
}
```

## `update_note`

Action slug: `update-note`

Price: `5` credits

Update a note by id. Requires edit permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `content` | `string` | no | Note content. |
| `data` | `object` | no | Raw JSON body. Keys here win over convenience fields. |
| `note_id` | `integer` | yes | Note id. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |

Sample parameters:

```json
{
  "content": "Draft marketing copy to check for banned phrases.",
  "data": {},
  "note_id": 1,
  "options": {}
}
```

Generated JSON parameter schema:

```json
{
  "content": {
    "description": "Note content.",
    "required": false,
    "type": "string"
  },
  "data": {
    "description": "Raw JSON body. Keys here win over convenience fields.",
    "required": false,
    "type": "object"
  },
  "note_id": {
    "description": "Note id.",
    "required": true,
    "type": "integer"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  }
}
```

## `update_record`

Action slug: `update-record`

Price: `5` credits

Update one core resource record. Requires edit permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `activity_id` | `integer` | no | Activity id when resource is activity. |
| `data` | `object` | no | Raw JSON body. Keys here win over convenience fields. |
| `deal_id` | `integer` | no | Deal id when resource is deal. |
| `name` | `string` | no | Person, organization, product, or file name. |
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |
| `organization_id` | `integer` | no | Organization id when resource is organization, or associated organization id for supported body updates. |
| `person_id` | `integer` | no | Person id when resource is person. |
| `product_id` | `integer` | no | Product id when resource is product. |
| `resource` | `string` | yes | Core resource to update. |
| `subject` | `string` | no | Activity subject. |
| `title` | `string` | no | Deal title. |
| `value` | `object` | no | Deal monetary amount. Accepts either a number or object form {amount, currency}; object form is normalized to numeric value plus currency. |

Sample parameters:

```json
{
  "activity_id": 1,
  "data": {},
  "deal_id": 1,
  "name": "example name",
  "options": {},
  "organization_id": 1,
  "person_id": 1,
  "product_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "activity_id": {
    "description": "Activity id when resource is activity.",
    "required": false,
    "type": "integer"
  },
  "data": {
    "description": "Raw JSON body. Keys here win over convenience fields.",
    "required": false,
    "type": "object"
  },
  "deal_id": {
    "description": "Deal id when resource is deal.",
    "required": false,
    "type": "integer"
  },
  "name": {
    "description": "Person, organization, product, or file name.",
    "required": false,
    "type": "string"
  },
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  },
  "organization_id": {
    "description": "Organization id when resource is organization, or associated organization id for supported body updates.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Person id when resource is person.",
    "required": false,
    "type": "integer"
  },
  "product_id": {
    "description": "Product id when resource is product.",
    "required": false,
    "type": "integer"
  },
  "resource": {
    "description": "Core resource to update.",
    "enum": [
      "deal",
      "person",
      "organization",
      "activity",
      "product"
    ],
    "required": true,
    "type": "string"
  },
  "subject": {
    "description": "Activity subject.",
    "required": false,
    "type": "string"
  },
  "title": {
    "description": "Deal title.",
    "required": false,
    "type": "string"
  },
  "value": {
    "description": "Deal monetary amount. Accepts either a number or object form {amount, currency}; object form is normalized to numeric value plus currency.",
    "required": false,
    "type": "object"
  }
}
```

## `upload_file`

Action slug: `upload-file`

Price: `5` credits

Upload an AgentPMT File Manager file to Pipedrive as an attachment. Requires add permission.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `activity_id` | `integer` | no | Associate to activity id. |
| `deal_id` | `integer` | no | Associate to deal id. |
| `file_id` | `string` | yes | AgentPMT File Manager file id. |
| `file_name_override` | `string` | no | Optional file name override. |
| `lead_id` | `string` | no | Associate to lead UUID. |
| `organization_id` | `integer` | no | Public organization id; connector sends org_id where required. |
| `person_id` | `integer` | no | Associate to person id. |
| `product_id` | `integer` | no | Associate to product id. |

Sample parameters:

```json
{
  "activity_id": 1,
  "deal_id": 1,
  "file_id": "example file id",
  "file_name_override": "example file name override",
  "lead_id": "example lead id",
  "organization_id": 1,
  "person_id": 1,
  "product_id": 1
}
```

Generated JSON parameter schema:

```json
{
  "activity_id": {
    "description": "Associate to activity id.",
    "required": false,
    "type": "integer"
  },
  "deal_id": {
    "description": "Associate to deal id.",
    "required": false,
    "type": "integer"
  },
  "file_id": {
    "description": "AgentPMT File Manager file id.",
    "required": true,
    "type": "string"
  },
  "file_name_override": {
    "description": "Optional file name override.",
    "required": false,
    "type": "string"
  },
  "lead_id": {
    "description": "Associate to lead UUID.",
    "required": false,
    "type": "string"
  },
  "organization_id": {
    "description": "Public organization id; connector sends org_id where required.",
    "required": false,
    "type": "integer"
  },
  "person_id": {
    "description": "Associate to person id.",
    "required": false,
    "type": "integer"
  },
  "product_id": {
    "description": "Associate to product id.",
    "required": false,
    "type": "integer"
  }
}
```

## `who_am_i`

Action slug: `who-am-i`

Price: `5` credits

Return the connected Pipedrive user and company details.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `options` | `object` | no | Additional query parameters that do not override connector-set parameters. |

Sample parameters:

```json
{
  "options": {}
}
```

Generated JSON parameter schema:

```json
{
  "options": {
    "description": "Additional query parameters that do not override connector-set parameters.",
    "required": false,
    "type": "object"
  }
}
```
