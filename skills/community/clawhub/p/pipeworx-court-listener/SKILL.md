# Court Listener

CourtListener MCP — Free Law Project's CourtListener API (free, no auth required for basic access)

## search_opinions

Search US court opinions by keyword (e.g., "qualified immunity", "Fourth Amendment"). Returns case n

## search_dockets

Search US court dockets by keyword. Returns case name, court, filing date, docket number, nature of 

## get_opinion

Get a specific court opinion by its CourtListener ID. Returns the full opinion text, author, date, a

```json
{
  "mcpServers": {
    "court-listener": {
      "url": "https://gateway.pipeworx.io/court-listener/mcp"
    }
  }
}
```
