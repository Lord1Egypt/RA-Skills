# Congress

Congress MCP — US Congress data via GovTrack API (free, no auth required)

## search_bills

Search US congressional bills by keyword. Returns bill type, number, title, status, sponsor, and int

## get_bill

Get full details for a congressional bill by its ID. Returns text, sponsors, cosponsors, committee a

## get_members

Get current members of Congress with their name, party, state, district (for representatives), and c

## get_votes

Get recent congressional votes on bills. Returns question, result, chamber, vote counts (yes/no/abst

```json
{
  "mcpServers": {
    "congress": {
      "url": "https://gateway.pipeworx.io/congress/mcp"
    }
  }
}
```
