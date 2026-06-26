---
name: mcp-integration
description: Integrate AI agents with business data via Model Context Protocol. Query ads, analytics, CRM data through normalized interfaces. Use when connecting agents to business systems, enabling data access, or building MCP servers. Triggers on "MCP", "Model Context Protocol", "business data", "agent integration", "Claude MCP".
---

# MCP Integration

Model Context Protocol (MCP) connects AI agents to real business data through normalized interfaces.

## What is MCP?

**Model Context Protocol** is Anthropic's open standard for connecting AI models to external data sources and tools. It provides a unified way for agents to:

- Query databases and APIs
- Access files and resources
- Execute tools and functions
- Maintain context across sessions

## Why MCP Matters

**Before MCP:**
- Each integration = custom code
- Different APIs = different patterns
- Context lost between tools
- Security = ad-hoc per integration

**With MCP:**
- One protocol, many integrations
- Standard patterns for all sources
- Persistent context
- Built-in security model

## MCP Architecture

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│   Server    │────▶│  Resource   │
│  (Agent)    │     │   (MCP)     │     │  (Data)     │
└─────────────┘     └─────────────┘     └─────────────┘
                           │
                    ┌──────┴──────┐
                    │   Tools     │
                    │  Prompts    │
                    │  Resources  │
                    └─────────────┘
```

### Components

**1. MCP Server**
- Exposes resources and tools
- Handles authentication
- Manages connections

**2. MCP Client**
- Connects to servers
- Discovers capabilities
- Executes operations

**3. Resources**
- Files, databases, APIs
- Read/write operations
- Subscriptions for updates

**4. Tools**
- Executable functions
- Input/output schemas
- Side effects

**5. Prompts**
- Reusable prompt templates
- Parameterized
- Composable

## Integration Types

### 1. Database Integration

```python
# MCP Server for PostgreSQL
from mcp import Server

server = Server("postgres-integration")

@server.resource("postgres://users")
async def get_users():
    # Query users from database
    return await db.query("SELECT * FROM users")

@server.tool("query_users")
async def query_users(filters: dict):
    # Execute parameterized query
    return await db.query_with_filters(filters)
```

### 2. API Integration

```python
# MCP Server for REST API
@server.resource("api://customers")
async def get_customers():
    response = await httpx.get("https://api.example.com/customers")
    return response.json()

@server.tool("create_customer")
async def create_customer(data: dict):
    response = await httpx.post(
        "https://api.example.com/customers",
        json=data
    )
    return response.json()
```

### 3. File System Integration

```python
# MCP Server for file access
@server.resource("file://documents/{path}")
async def read_document(path: str):
    with open(f"documents/{path}") as f:
        return f.read()

@server.tool("write_document")
async def write_document(path: str, content: str):
    with open(f"documents/{path}", "w") as f:
        f.write(content)
    return {"status": "written"}
```

## Business Data Integration

### Ads Data

```python
# Google Ads MCP
@server.resource("ads://campaigns")
async def get_campaigns():
    """Get all ad campaigns with metrics"""
    campaigns = await ads_client.get_campaigns()
    return normalize_campaigns(campaigns)

@server.tool("optimize_budget")
async def optimize_budget(campaign_id: str):
    """Automatically adjust campaign budget"""
    # Analyze performance
    # Adjust spend allocation
    # Return optimization results
```

### Analytics Data

```python
# Analytics MCP
@server.resource("analytics://metrics")
async def get_metrics():
    """Get normalized metrics across platforms"""
    return {
        "google_analytics": await ga.get_metrics(),
        "mixpanel": await mixpanel.get_events(),
        "custom_events": await custom.get_events()
    }

@server.tool("query_analytics")
async def query_analytics(query: str):
    """Natural language analytics query"""
    # Parse query
    # Execute across platforms
    # Return unified results
```

### CRM Data

```python
# Salesforce MCP
@server.resource("crm://leads")
async def get_leads():
    """Get leads from CRM"""
    return await salesforce.query("SELECT Id, Name, Email FROM Lead")

@server.tool("create_lead")
async def create_lead(data: dict):
    """Create new lead in CRM"""
    lead = await salesforce.create("Lead", data)
    return lead
```

## Best Practices

### 1. Normalization

```python
# Normalize data from different sources
def normalize_campaign(data, source):
    schema = {
        "id": data.get("id") or data.get("campaign_id"),
        "name": data.get("name") or data.get("campaign_name"),
        "spend": data.get("spend") or data.get("cost"),
        "impressions": data.get("impressions") or data.get("views"),
        "clicks": data.get("clicks") or data.get("clicks_count"),
        "source": source
    }
    return schema
```

### 2. Error Handling

```python
@server.tool("risky_operation")
async def risky_operation(data: dict):
    try:
        result = await external_api.call(data)
        return {"success": True, "data": result}
    except APIError as e:
        return {
            "success": False,
            "error": str(e),
            "suggestion": "Try again with valid parameters"
        }
```

### 3. Caching

```python
from functools import lru_cache
from datetime import datetime, timedelta

cache = {}

@server.resource("api://expensive-data")
async def get_expensive_data():
    cache_key = "expensive-data"
    cached = cache.get(cache_key)
    
    if cached and cached["expires"] > datetime.now():
        return cached["data"]
    
    # Fetch fresh data
    data = await expensive_api_call()
    cache[cache_key] = {
        "data": data,
        "expires": datetime.now() + timedelta(hours=1)
    }
    return data
```

### 4. Security

```python
# Validate inputs
from pydantic import BaseModel

class QueryInput(BaseModel):
    table: str
    filters: dict
    limit: int = 100

@server.tool("safe_query")
async def safe_query(input: QueryInput):
    # Input is validated by Pydantic
    # SQL injection prevented
    return await db.query(input.table, input.filters, input.limit)
```

## Claude Desktop Integration

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "business-data": {
      "command": "python",
      "args": ["mcp_server.py"],
      "env": {
        "DATABASE_URL": "postgresql://...",
        "API_KEY": "..."
      }
    }
  }
}
```

## Common MCP Servers

### Official Servers

| Server | Description |
|--------|-------------|
| filesystem | File system access |
| postgres | PostgreSQL database |
| sqlite | SQLite database |
| github | GitHub API |
| google-drive | Google Drive |
| slack | Slack API |

### Custom Servers

Create custom servers for:
- Internal APIs
- Proprietary databases
- Custom tools
- Business-specific operations

## Debugging

### Server Logs

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("mcp_server")

@server.tool("debug_operation")
async def debug_operation(data: dict):
    logger.debug(f"Input: {data}")
    result = await process(data)
    logger.debug(f"Output: {result}")
    return result
```

### Connection Issues

```bash
# Test MCP server
python -m mcp.server --debug

# Test client connection
python -m mcp.client --url "ws://localhost:8080"
```

## Examples

### Query Multiple Data Sources

```python
@server.tool("cross_platform_query")
async def cross_platform_query(query: str):
    """Query across multiple platforms"""
    results = {}
    
    # Query each platform
    results["analytics"] = await analytics.query(query)
    results["crm"] = await crm.query(query)
    results["ads"] = await ads.query(query)
    
    # Merge results
    return merge_results(results)
```

### Automated Insights

```python
@server.tool("generate_insights")
async def generate_insights(data_source: str):
    """Generate insights from business data"""
    # Get data
    data = await get_data(data_source)
    
    # Analyze
    insights = []
    
    # Trend analysis
    if data["trend"] == "increasing":
        insights.append("Revenue trending up - consider scaling")
    
    # Anomaly detection
    if data["anomaly"]:
        insights.append(f"Anomaly detected: {data['anomaly']}")
    
    return {"insights": insights, "data": data}
```

## Resources

- **Anthropic MCP Docs:** https://modelcontextprotocol.io
- **Official Servers:** https://github.com/modelcontextprotocol/servers
- **Community Servers:** https://github.com/punkpeye/awesome-mcp-servers
