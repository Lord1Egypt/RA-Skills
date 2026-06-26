# Amplitude

Amplitude MCP Pack

## amp_get_events

Get event counts and breakdowns for a date range (e.g., "2024-01-01" to "2024-01-31"). Returns frequ

## amp_get_active_users

Get active user counts by granularity (daily, weekly, or monthly) for a date range. Returns totals a

## amp_get_retention

Get user retention metrics for a cohort over time. Returns retention percentages by time period (e.g

## amp_user_search

Search for users by ID or property (e.g., email, user_id). Returns matching profiles with properties

## amp_get_user_activity

Get recent event activity timeline for a specific user. Returns events with timestamps, properties, 

```json
{
  "mcpServers": {
    "amplitude": {
      "url": "https://gateway.pipeworx.io/amplitude/mcp"
    }
  }
}
```
