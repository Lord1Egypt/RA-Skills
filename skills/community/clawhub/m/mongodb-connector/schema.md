# MongoDB Connector Schema

This generated reference belongs to the adjacent `SKILL.md`. Use it for exact action names, action slugs, parameter summaries, sample parameters, and generated JSON parameter schemas.

Product slug: `mongodb-connector`

x402 availability: not enabled for this product.

## `aggregate`

Action slug: `aggregate`

Price: `5` credits

Run an aggregation pipeline. Supports $search, $vectorSearch, $geoNear, $lookup, CSV/JSON export.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `export_format` | `string` | no | Export file format |
| `output` | `array` | no | Output modes |
| `pipeline` | `array` | yes | Aggregation pipeline stages |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "export_format": "json",
  "output": [
    "inline"
  ],
  "pipeline": [
    {}
  ]
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "export_format": {
    "description": "Export file format",
    "enum": [
      "json",
      "csv"
    ],
    "required": false,
    "type": "string"
  },
  "output": {
    "description": "Output modes",
    "items": {
      "enum": [
        "inline",
        "export"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "pipeline": {
    "description": "Aggregation pipeline stages",
    "items": {
      "type": "object"
    },
    "required": true,
    "type": "array"
  }
}
```

## `bulk_write`

Action slug: `bulk-write`

Price: `5` credits

Execute mixed batch of insert, update, replace, and delete operations

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `operations` | `array` | yes | Operations: [{operation: insert_one\|update_one\|update_many\|replace_one\|delete_one\|delete_many, ...params}] |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "operations": [
    {}
  ]
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "operations": {
    "description": "Operations: [{operation: insert_one|update_one|update_many|replace_one|delete_one|delete_many, ...params}]",
    "items": {
      "type": "object"
    },
    "required": true,
    "type": "array"
  }
}
```

## `count_documents`

Action slug: `count-documents`

Price: `5` credits

Count documents matching a filter

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `filter` | `object` | no | MongoDB query filter |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "filter": {}
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "filter": {
    "description": "MongoDB query filter",
    "required": false,
    "type": "object"
  }
}
```

## `create_collection`

Action slug: `create-collection`

Price: `5` credits

Create a collection with optional schema validation, capping, or time series config

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `collection_options` | `object` | no | Options: validator, capped, timeseries, collation, etc. |
| `database` | `string` | yes | Database name |

Sample parameters:

```json
{
  "collection": "example collection",
  "collection_options": {},
  "database": "example database"
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "collection_options": {
    "description": "Options: validator, capped, timeseries, collation, etc.",
    "required": false,
    "type": "object"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  }
}
```

## `create_index`

Action slug: `create-index`

Price: `5` credits

Create an index (single, compound, text, geospatial, hashed, wildcard)

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `index_keys` | `array` | yes | Index keys [[field, 1/-1]] |
| `index_name` | `string` | no | Index name |
| `index_options` | `object` | no | Options (unique, sparse, TTL, partial, etc.) |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "index_keys": [
    [
      "example index key"
    ]
  ],
  "index_name": "example index name",
  "index_options": {}
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "index_keys": {
    "description": "Index keys [[field, 1/-1]]",
    "items": {
      "type": "array"
    },
    "required": true,
    "type": "array"
  },
  "index_name": {
    "description": "Index name",
    "required": false,
    "type": "string"
  },
  "index_options": {
    "description": "Options (unique, sparse, TTL, partial, etc.)",
    "required": false,
    "type": "object"
  }
}
```

## `create_search_index`

Action slug: `create-search-index`

Price: `5` credits

Create an Atlas Search or Vector Search index

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `index_name` | `string` | no | Index name |
| `search_index_definition` | `object` | yes | Search index definition (mappings or vector fields) |
| `search_index_type` | `string` | no | Index type (default: search) |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "index_name": "example index name",
  "search_index_definition": {},
  "search_index_type": "search"
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "index_name": {
    "description": "Index name",
    "required": false,
    "type": "string"
  },
  "search_index_definition": {
    "description": "Search index definition (mappings or vector fields)",
    "required": true,
    "type": "object"
  },
  "search_index_type": {
    "description": "Index type (default: search)",
    "enum": [
      "search",
      "vectorSearch"
    ],
    "required": false,
    "type": "string"
  }
}
```

## `delete_documents`

Action slug: `delete-documents`

Price: `5` credits

Delete one or many documents

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `filter` | `object` | no | Match filter |
| `many` | `boolean` | no | Delete all matches (default: false) |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "filter": {},
  "many": true
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "filter": {
    "description": "Match filter",
    "required": false,
    "type": "object"
  },
  "many": {
    "description": "Delete all matches (default: false)",
    "required": false,
    "type": "boolean"
  }
}
```

## `distinct`

Action slug: `distinct`

Price: `5` credits

Get distinct values for a field

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `field_name` | `string` | yes | Field name |
| `filter` | `object` | no | MongoDB query filter |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "field_name": "example field name",
  "filter": {}
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "field_name": {
    "description": "Field name",
    "required": true,
    "type": "string"
  },
  "filter": {
    "description": "MongoDB query filter",
    "required": false,
    "type": "object"
  }
}
```

## `drop_collection`

Action slug: `drop-collection`

Price: `5` credits

Drop a collection

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database"
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  }
}
```

## `drop_index`

Action slug: `drop-index`

Price: `5` credits

Drop an index from a collection

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `index_name` | `string` | yes | Index name to drop |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "index_name": "example index name"
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "index_name": {
    "description": "Index name to drop",
    "required": true,
    "type": "string"
  }
}
```

## `drop_search_index`

Action slug: `drop-search-index`

Price: `5` credits

Drop an Atlas Search or Vector Search index

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `index_name` | `string` | yes | Index name to drop |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "index_name": "example index name"
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "index_name": {
    "description": "Index name to drop",
    "required": true,
    "type": "string"
  }
}
```

## `estimated_count`

Action slug: `estimated-count`

Price: `5` credits

Fast approximate document count using collection metadata

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database"
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  }
}
```

## `find_documents`

Action slug: `find-documents`

Price: `5` credits

Query documents with filter, projection, sort, and pagination. Supports CSV/JSON export.

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `export_format` | `string` | no | Export file format |
| `filter` | `object` | no | MongoDB query filter |
| `limit` | `integer` | no | Max documents (1-1000, default 20) |
| `output` | `array` | no | Output modes: inline, export, or both |
| `projection` | `object` | no | Fields to include/exclude |
| `skip` | `integer` | no | Documents to skip |
| `sort` | `array` | no | Sort as [[field, direction]] (1=asc, -1=desc) |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "export_format": "json",
  "filter": {},
  "limit": 1,
  "output": [
    "inline"
  ],
  "projection": {},
  "skip": 1
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "export_format": {
    "description": "Export file format",
    "enum": [
      "json",
      "csv"
    ],
    "required": false,
    "type": "string"
  },
  "filter": {
    "description": "MongoDB query filter",
    "required": false,
    "type": "object"
  },
  "limit": {
    "description": "Max documents (1-1000, default 20)",
    "required": false,
    "type": "integer"
  },
  "output": {
    "description": "Output modes: inline, export, or both",
    "items": {
      "enum": [
        "inline",
        "export"
      ],
      "type": "string"
    },
    "required": false,
    "type": "array"
  },
  "projection": {
    "description": "Fields to include/exclude",
    "required": false,
    "type": "object"
  },
  "skip": {
    "description": "Documents to skip",
    "required": false,
    "type": "integer"
  },
  "sort": {
    "description": "Sort as [[field, direction]] (1=asc, -1=desc)",
    "items": {
      "type": "array"
    },
    "required": false,
    "type": "array"
  }
}
```

## `find_one_and_delete`

Action slug: `find-one-and-delete`

Price: `5` credits

Atomically find and delete a document, returning it

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `filter` | `object` | no | Match filter |
| `projection` | `object` | no | Fields to return |
| `sort` | `array` | no | Sort to determine which doc |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "filter": {},
  "projection": {},
  "sort": [
    [
      "example sort"
    ]
  ]
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "filter": {
    "description": "Match filter",
    "required": false,
    "type": "object"
  },
  "projection": {
    "description": "Fields to return",
    "required": false,
    "type": "object"
  },
  "sort": {
    "description": "Sort to determine which doc",
    "items": {
      "type": "array"
    },
    "required": false,
    "type": "array"
  }
}
```

## `find_one_and_update`

Action slug: `find-one-and-update`

Price: `5` credits

Atomically find and update a document, returning it

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `filter` | `object` | no | Match filter |
| `projection` | `object` | no | Fields to return |
| `return_document` | `string` | no | Return doc before or after update |
| `sort` | `array` | no | Sort to determine which doc |
| `update` | `object` | yes | Update operations |
| `upsert` | `boolean` | no | Create if no match |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "filter": {},
  "projection": {},
  "return_document": "before",
  "sort": [
    [
      "example sort"
    ]
  ],
  "update": {},
  "upsert": true
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "filter": {
    "description": "Match filter",
    "required": false,
    "type": "object"
  },
  "projection": {
    "description": "Fields to return",
    "required": false,
    "type": "object"
  },
  "return_document": {
    "description": "Return doc before or after update",
    "enum": [
      "before",
      "after"
    ],
    "required": false,
    "type": "string"
  },
  "sort": {
    "description": "Sort to determine which doc",
    "items": {
      "type": "array"
    },
    "required": false,
    "type": "array"
  },
  "update": {
    "description": "Update operations",
    "required": true,
    "type": "object"
  },
  "upsert": {
    "description": "Create if no match",
    "required": false,
    "type": "boolean"
  }
}
```

## `insert_documents`

Action slug: `insert-documents`

Price: `5` credits

Insert one or more documents

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `document` | `object` | no | Single document to insert |
| `documents` | `array` | no | Multiple documents to insert |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "document": {},
  "documents": [
    {}
  ]
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "document": {
    "description": "Single document to insert",
    "required": false,
    "type": "object"
  },
  "documents": {
    "description": "Multiple documents to insert",
    "items": {
      "type": "object"
    },
    "required": false,
    "type": "array"
  }
}
```

## `list_collections`

Action slug: `list-collections`

Price: `5` credits

List collections in a database

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `database` | `string` | yes | Database name |

Sample parameters:

```json
{
  "database": "example database"
}
```

Generated JSON parameter schema:

```json
{
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  }
}
```

## `list_databases`

Action slug: `list-databases`

Price: `5` credits

List all accessible databases

Parameters:

This action does not require parameters.

Sample parameters:

```json
{}
```

Generated JSON parameter schema:

```json
{}
```

## `list_indexes`

Action slug: `list-indexes`

Price: `5` credits

List all indexes on a collection

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database"
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  }
}
```

## `list_search_indexes`

Action slug: `list-search-indexes`

Price: `5` credits

List Atlas Search and Vector Search indexes

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database"
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  }
}
```

## `replace_document`

Action slug: `replace-document`

Price: `5` credits

Replace a single document

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `document` | `object` | yes | Replacement document |
| `filter` | `object` | no | Match filter |
| `upsert` | `boolean` | no | Create if no match |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "document": {},
  "filter": {},
  "upsert": true
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "document": {
    "description": "Replacement document",
    "required": true,
    "type": "object"
  },
  "filter": {
    "description": "Match filter",
    "required": false,
    "type": "object"
  },
  "upsert": {
    "description": "Create if no match",
    "required": false,
    "type": "boolean"
  }
}
```

## `run_command`

Action slug: `run-command`

Price: `5` credits

Run any MongoDB database command (dbStats, collStats, serverStatus, etc.)

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `command` | `object` | yes | MongoDB command document |
| `database` | `string` | yes | Database name |

Sample parameters:

```json
{
  "command": {},
  "database": "example database"
}
```

Generated JSON parameter schema:

```json
{
  "command": {
    "description": "MongoDB command document",
    "required": true,
    "type": "object"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  }
}
```

## `update_documents`

Action slug: `update-documents`

Price: `5` credits

Update one or many documents

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `filter` | `object` | no | Match filter |
| `many` | `boolean` | no | Update all matches (default: false) |
| `update` | `object` | yes | Update operations ($set, $inc, etc.) |
| `upsert` | `boolean` | no | Create if no match |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "filter": {},
  "many": true,
  "update": {},
  "upsert": true
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "filter": {
    "description": "Match filter",
    "required": false,
    "type": "object"
  },
  "many": {
    "description": "Update all matches (default: false)",
    "required": false,
    "type": "boolean"
  },
  "update": {
    "description": "Update operations ($set, $inc, etc.)",
    "required": true,
    "type": "object"
  },
  "upsert": {
    "description": "Create if no match",
    "required": false,
    "type": "boolean"
  }
}
```

## `update_search_index`

Action slug: `update-search-index`

Price: `5` credits

Update an Atlas Search or Vector Search index definition

Parameters:

| Parameter | Type | Required | Description |
|---|---|---|---|
| `collection` | `string` | yes | Collection name |
| `database` | `string` | yes | Database name |
| `index_name` | `string` | yes | Index name to update |
| `search_index_definition` | `object` | yes | New index definition |

Sample parameters:

```json
{
  "collection": "example collection",
  "database": "example database",
  "index_name": "example index name",
  "search_index_definition": {}
}
```

Generated JSON parameter schema:

```json
{
  "collection": {
    "description": "Collection name",
    "required": true,
    "type": "string"
  },
  "database": {
    "description": "Database name",
    "required": true,
    "type": "string"
  },
  "index_name": {
    "description": "Index name to update",
    "required": true,
    "type": "string"
  },
  "search_index_definition": {
    "description": "New index definition",
    "required": true,
    "type": "object"
  }
}
```
