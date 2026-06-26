# Airtable

Airtable MCP Pack — wraps the Airtable REST API v0

## airtable_list_records

Fetch records from an Airtable table with optional filtering by formula (e.g., "{Status} = 'Done'").

## airtable_get_record

Retrieve a single record by ID from an Airtable table. Returns all field values and record metadata.

## airtable_create_record

Add a new record to an Airtable table with specified field values. Returns the created record ID and

## airtable_list_bases

List all Airtable bases you have access to. Returns base IDs, names, and workspace info. Use to expl

## airtable_get_base_schema

Get the structure of an Airtable base—all tables, field names, field types, and configurations. Use 

```json
{
  "mcpServers": {
    "airtable": {
      "url": "https://gateway.pipeworx.io/airtable/mcp"
    }
  }
}
```
