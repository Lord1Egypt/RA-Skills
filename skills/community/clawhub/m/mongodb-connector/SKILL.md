---
name: mongodb-connector
description: "MongoDB Connector: Connect to a user's cloud-hosted MongoDB instance and run 24 permission-gated database operations. Use when an agent needs mongodb connector, query mongodb collections, export data as csv or json, run aggregation pipelines, atlas vector search for rag, aggregate, database, collection through AgentPMT-hosted remote tool calls. Discovery terms: mongodb connector, query mongodb collections, export data as csv or json, run aggregation pipelines, atlas vector search for rag."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/mongodb-connector
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/mongodb-connector"}}
---
# MongoDB Connector

## Freshness
Last updated: `2026-06-09`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
Connect your own MongoDB database and query, insert, update, delete, and aggregate documents without leaving your workflow. Browse databases and collections, inspect indexes, and run full aggregation pipelines including joins, grouping, and windowed analytics. Create and manage Atlas Search indexes for full-text search and Atlas Vector Search indexes for semantic similarity and RAG applications. Export query results as downloadable CSV or JSON files for use in spreadsheets, dashboards, or data pipelines. Execute atomic find-and-modify operations and batch mixed writes in a single round trip with bulk_write. Manage collection lifecycles with create, drop, and schema validation. Access is fully permission-gated with four levels — read, write, delete, and admin — so you stay in control of what agents can do with your data. Works with MongoDB Atlas and any cloud-hosted or publicly accessible MongoDB instance.

## Product Instructions
### MongoDB

Connect to a cloud-hosted MongoDB database and run queries, inserts, updates, deletes, aggregations, index management, Atlas Search, and Vector Search. Export results as CSV or JSON files. Supports MongoDB Atlas and any publicly accessible MongoDB instance.

#### Permissions

Access is controlled by a `permissions` array injected by the platform:
- `read` (default if omitted): find, count, list, aggregate, distinct
- `write`: insert, update, replace, find_one_and_update, bulk_write
- `delete`: delete documents, find_one_and_delete
- `admin`: indexes, search indexes, create/drop collection, run_command

#### Output Modes

`find_documents` and `aggregate` support an `output` array:
- `["inline"]` (default): return documents in the response
- `["export"]`: save results as a file (CSV or JSON)
- `["inline", "export"]`: both

Use `export_format` to choose `csv` or `json` (default: `json`).

#### Read Actions

##### `find_documents`
Required: `database`, `collection`
Optional: `filter`, `projection`, `sort` ([[field, 1/-1]]), `limit` (1-1000, default 20), `skip`, `output`, `export_format`

Example: `{"action":"find_documents","database":"mydb","collection":"users","filter":{"status":"active"},"limit":10}`

##### `count_documents`
Required: `database`, `collection`
Optional: `filter`

##### `estimated_count`
Required: `database`, `collection`
Fast approximate count using collection metadata (no filter support).

##### `list_databases`
No required params.

##### `list_collections`
Required: `database`

##### `aggregate`
Required: `database`, `collection`, `pipeline`
Optional: `output`, `export_format`

Supports all pipeline stages including `$search`, `$vectorSearch`, `$geoNear`, `$lookup`, `$graphLookup`, `$sample`.

Example: `{"action":"aggregate","database":"mydb","collection":"orders","pipeline":[{"$group":{"_id":"$status","count":{"$sum":1}}}]}`

Vector search example: `{"action":"aggregate","database":"mydb","collection":"docs","pipeline":[{"$vectorSearch":{"index":"vector_idx","path":"embedding","queryVector":[0.1,0.2,...],"numCandidates":100,"limit":10}}]}`

##### `distinct`
Required: `database`, `collection`, `field_name`
Optional: `filter`

##### `list_indexes`
Required: `database`, `collection`
Returns all indexes on a collection with key specs, options, and names.

##### `list_search_indexes`
Required: `database`, `collection`
Returns Atlas Search and Vector Search indexes.

#### Write Actions

##### `insert_documents`
Required: `database`, `collection`, `document` (single) or `documents` (array)

##### `update_documents`
Required: `database`, `collection`, `update`
Optional: `filter`, `upsert`, `many` (default false)

##### `replace_document`
Required: `database`, `collection`, `document`
Optional: `filter`, `upsert`

##### `find_one_and_update`
Atomically find and update a document, returning it.
Required: `database`, `collection`, `update`
Optional: `filter`, `projection`, `sort`, `upsert`, `return_document` ("before" or "after", default "before")

##### `find_one_and_delete`
Atomically find and delete a document, returning it.
Required: `database`, `collection`
Optional: `filter`, `projection`, `sort`

##### `bulk_write`
Execute mixed batch operations in a single round trip.
Required: `database`, `collection`, `operations`

Each operation: `{"operation": "insert_one|update_one|update_many|replace_one|delete_one|delete_many", ...params}`

Example: `{"action":"bulk_write","database":"mydb","collection":"users","operations":[{"operation":"insert_one","document":{"name":"Alice"}},{"operation":"update_one","filter":{"name":"Bob"},"update":{"$set":{"active":true}}}]}`

#### Delete Actions

##### `delete_documents`
Required: `database`, `collection`
Optional: `filter`, `many` (default false)

#### Admin Actions

##### `create_index`
Required: `database`, `collection`, `index_keys`
Optional: `index_name`, `index_options`

Supports all index types: single field, compound, text (`[["field","text"]]`), geospatial (`[["location","2dsphere"]]`), hashed, wildcard.

##### `drop_index`
Required: `database`, `collection`, `index_name`

##### `create_search_index`
Create an Atlas Search or Vector Search index.
Required: `database`, `collection`, `search_index_definition`
Optional: `index_name`, `search_index_type` ("search" or "vectorSearch")

Vector index example: `{"action":"create_search_index","database":"mydb","collection":"docs","search_index_type":"vectorSearch","index_name":"vec_idx","search_index_definition":{"fields":[{"type":"vector","path":"embedding","numDimensions":1536,"similarity":"cosine"}]}}`

##### `update_search_index`
Required: `database`, `collection`, `index_name`, `search_index_definition`

##### `drop_search_index`
Required: `database`, `collection`, `index_name`

##### `create_collection`
Required: `database`, `collection`
Optional: `collection_options` (validator, capped, timeseries, clusteredIndex, collation, expireAfterSeconds)

##### `drop_collection`
Required: `database`, `collection`

##### `run_command`
Run any MongoDB database command.
Required: `database`, `command`

Example: `{"action":"run_command","database":"mydb","command":{"dbStats":1}}`
Example: `{"action":"run_command","database":"mydb","command":{"collStats":"users"}}`

#### Notes
- Filters use standard MongoDB query syntax: $eq, $gt, $lt, $in, $regex, $near, $geoWithin, etc.
- Updates use $set, $unset, $inc, $push, $pull, etc.
- Sort uses 1 for ascending, -1 for descending
- Aggregation pipelines with $out or $merge require write permission
- Max 1000 documents returned per find or aggregate call
- Atlas Search and Vector Search require search indexes (use create_search_index)
- Geospatial queries require 2dsphere or 2d indexes (use create_index)

## When To Use
- Use this skill for `MongoDB Connector` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: mongodb connector, query mongodb collections, export data as csv or json, run aggregation pipelines, atlas vector search for rag, aggregate, database, collection.
- Supported action names: `aggregate`, `bulk_write`, `count_documents`, `create_collection`, `create_index`, `create_search_index`, `delete_documents`, `distinct`, `drop_collection`, `drop_index`, `drop_search_index`, `estimated_count`, `find_documents`, `find_one_and_delete`, `find_one_and_update`, `insert_documents`, `list_collections`, `list_databases`, `list_indexes`, `list_search_indexes`, `replace_document`, `run_command`, `update_documents`, `update_search_index`.

## Use Cases
- Query MongoDB collections
- Export data as CSV or JSON
- Run aggregation pipelines
- Atlas Vector Search for RAG
- Full-text search with Atlas Search
- Insert and update documents
- Bulk write operations
- Manage indexes
- Create vector search indexes
- Geospatial queries
- Schema validation
- Database administration

## Related Product Skills
- File Management: ../file-management (ClawHub: `file-management`, page: https://clawhub.ai/agentpmt/file-management; skills.sh: `npx skills add AgentPMT/agent-skills --skill file-management`)

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `24`.
x402 availability: not enabled for this product.

- `aggregate` (action slug: `aggregate`): Run an aggregation pipeline. Supports $search, $vectorSearch, $geoNear, $lookup, CSV/JSON export. Price: `5` credits. Parameters: `collection`, `database`, `export_format`, `output`, `pipeline`.
- `bulk_write` (action slug: `bulk-write`): Execute mixed batch of insert, update, replace, and delete operations Price: `5` credits. Parameters: `collection`, `database`, `operations`.
- `count_documents` (action slug: `count-documents`): Count documents matching a filter Price: `5` credits. Parameters: `collection`, `database`, `filter`.
- `create_collection` (action slug: `create-collection`): Create a collection with optional schema validation, capping, or time series config Price: `5` credits. Parameters: `collection`, `collection_options`, `database`.
- `create_index` (action slug: `create-index`): Create an index (single, compound, text, geospatial, hashed, wildcard) Price: `5` credits. Parameters: `collection`, `database`, `index_keys`, `index_name`, `index_options`.
- `create_search_index` (action slug: `create-search-index`): Create an Atlas Search or Vector Search index Price: `5` credits. Parameters: `collection`, `database`, `index_name`, `search_index_definition`, `search_index_type`.
- `delete_documents` (action slug: `delete-documents`): Delete one or many documents Price: `5` credits. Parameters: `collection`, `database`, `filter`, `many`.
- `distinct` (action slug: `distinct`): Get distinct values for a field Price: `5` credits. Parameters: `collection`, `database`, `field_name`, `filter`.
- `drop_collection` (action slug: `drop-collection`): Drop a collection Price: `5` credits. Parameters: `collection`, `database`.
- `drop_index` (action slug: `drop-index`): Drop an index from a collection Price: `5` credits. Parameters: `collection`, `database`, `index_name`.
- `drop_search_index` (action slug: `drop-search-index`): Drop an Atlas Search or Vector Search index Price: `5` credits. Parameters: `collection`, `database`, `index_name`.
- `estimated_count` (action slug: `estimated-count`): Fast approximate document count using collection metadata Price: `5` credits. Parameters: `collection`, `database`.
- `find_documents` (action slug: `find-documents`): Query documents with filter, projection, sort, and pagination. Supports CSV/JSON export. Price: `5` credits. Parameters: `collection`, `database`, `export_format`, `filter`, `limit`, `output`, `projection`, `skip`, plus 1 more.
- `find_one_and_delete` (action slug: `find-one-and-delete`): Atomically find and delete a document, returning it Price: `5` credits. Parameters: `collection`, `database`, `filter`, `projection`, `sort`.
- `find_one_and_update` (action slug: `find-one-and-update`): Atomically find and update a document, returning it Price: `5` credits. Parameters: `collection`, `database`, `filter`, `projection`, `return_document`, `sort`, `update`, `upsert`.
- `insert_documents` (action slug: `insert-documents`): Insert one or more documents Price: `5` credits. Parameters: `collection`, `database`, `document`, `documents`.
- `list_collections` (action slug: `list-collections`): List collections in a database Price: `5` credits. Parameters: `database`.
- `list_databases` (action slug: `list-databases`): List all accessible databases Price: `5` credits. Parameters: none.
- `list_indexes` (action slug: `list-indexes`): List all indexes on a collection Price: `5` credits. Parameters: `collection`, `database`.
- `list_search_indexes` (action slug: `list-search-indexes`): List Atlas Search and Vector Search indexes Price: `5` credits. Parameters: `collection`, `database`.
- `replace_document` (action slug: `replace-document`): Replace a single document Price: `5` credits. Parameters: `collection`, `database`, `document`, `filter`, `upsert`.
- `run_command` (action slug: `run-command`): Run any MongoDB database command (dbStats, collStats, serverStatus, etc.) Price: `5` credits. Parameters: `command`, `database`.
- `update_documents` (action slug: `update-documents`): Update one or many documents Price: `5` credits. Parameters: `collection`, `database`, `filter`, `many`, `update`, `upsert`.
- `update_search_index` (action slug: `update-search-index`): Update an Atlas Search or Vector Search index definition Price: `5` credits. Parameters: `collection`, `database`, `index_name`, `search_index_definition`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "mongodb-connector"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "mongodb-connector"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "mongodb-connector"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "mongodb-connector"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "mongodb-connector"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "mongodb-connector"
  }
}
```

## Call This Tool
Product slug: `mongodb-connector`

Marketplace page: https://www.agentpmt.com/marketplace/mongodb-connector

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "MongoDB-Connector",
    "arguments": {
      "action": "aggregate",
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
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "mongodb-connector",
  "parameters": {
    "action": "aggregate",
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
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `aggregate` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/mongodb-connector
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
