# Cdc

CDC MCP — wraps CDC open data via Socrata API (data.cdc.gov)

## search_datasets

Search CDC public health datasets by keyword. Returns dataset names, descriptions, IDs, and update d

## get_dataset

Get rows from a specific CDC dataset by its Socrata dataset ID (four-by-four format like "xxxx-xxxx"

```json
{
  "mcpServers": {
    "cdc": {
      "url": "https://gateway.pipeworx.io/cdc/mcp"
    }
  }
}
```
