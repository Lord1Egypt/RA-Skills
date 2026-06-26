# Crates

Crates.io MCP — wraps the crates.io REST API v1 (free, no auth)

## search_crates

Search crates.io for Rust packages by keyword. Returns crate name, description, downloads, latest ve

## get_crate

Get full metadata for a specific crate (e.g., 'serde'). Returns description, downloads, latest versi

## get_versions

List all published versions for a crate in reverse chronological order. Returns version number, down

```json
{
  "mcpServers": {
    "crates": {
      "url": "https://gateway.pipeworx.io/crates/mcp"
    }
  }
}
```
