---
name: nango-api-integration
description: Connect AI agents to 700+ external APIs using Nango. Handles OAuth, authentication flows, and tool calling for any API. Use when integrating agents with external services (Google, Slack, GitHub, Salesforce, etc.), setting up API access for agents, or when you need OAuth/API key management for AI tools. Triggers on "nango", "api integration", "oauth for agents", "connect api", "external api access".
---

# Nango API Integration for AI Agents

Nango provides unified API access for AI agents with OAuth handling, 700+ pre-built integrations, and MCP server support. This skill helps you connect your agent to any external API.

## Why Nango for Agents?

- **700+ APIs pre-integrated** - No need to build each integration from scratch
- **2800+ pre-built actions** - Ready-to-use API operations
- **MCP servers per app** - Model Context Protocol support
- **1:1 API access** - No abstraction layer, you see exact API requests
- **White-label OAuth** - Embeddable auth flows
- **Any backend language** - Works with Python, Node, etc.
- **AI-generated code** - Write integration logic with AI

## Quick Start

### Step 1: Create Nango Account

1. Go to https://nango.dev
2. Sign up for a free account
3. Create a new project
4. Get your API key from Settings

### Step 2: Install Nango SDK

```bash
# Python
pip install nango

# Node.js
npm install @nangohq/node-client
```

### Step 3: Configure Environment

Add to your environment:

```bash
NANGO_SECRET_KEY=your-secret-key-here
NANGO_HOST=https://api.nango.dev  # or self-hosted
```

## Integration Patterns

### Pattern 1: OAuth Flow

For APIs requiring OAuth (Google, Slack, GitHub, etc.):

```python
from nango import Nango

nango = Nango()

# Get OAuth URL
auth_url = nango.get_auth_url(
    provider="google",
    redirect_uri="https://your-app.com/callback"
)

# User visits auth_url, authorizes, returns with code
# Exchange code for connection
connection = nango.create_connection(
    provider="google",
    code="auth_code_from_callback",
    connection_id="user-google-123"
)

# Now make API calls
result = nango.proxy(
    provider="google",
    endpoint="/gmail/v1/users/me/messages",
    connection_id="user-google-123"
)
```

### Pattern 2: API Key

For APIs using API keys (Stripe, OpenAI, etc.):

```python
from nango import Nango

nango = Nango()

# Set API key for provider
nango.set_credentials(
    provider="stripe",
    connection_id="user-stripe-123",
    credentials={"api_key": "sk_test_xxx"}
)

# Make calls
customers = nango.proxy(
    provider="stripe",
    endpoint="/v1/customers",
    connection_id="user-stripe-123"
)
```

### Pattern 3: MCP Server

For Model Context Protocol integration:

```python
# Get MCP server configuration for a provider
mcp_config = nango.get_mcp_server(
    provider="github",
    connection_id="user-github-123"
)

# Use with MCP-compatible agents
# The config includes tools, resources, and prompts
```

## Popular API Integrations

| Provider | Use Case | Auth Type |
|----------|----------|-----------|
| Google | Gmail, Calendar, Drive | OAuth |
| Slack | Messages, Channels | OAuth |
| GitHub | Repos, Issues, PRs | OAuth |
| Salesforce | CRM Data | OAuth |
| Stripe | Payments | API Key |
| Notion | Notes, Databases | OAuth |
| Linear | Issues, Projects | OAuth |
| HubSpot | CRM, Marketing | OAuth |

## Creating Custom Integrations

### Template for New Provider

```typescript
// integrations/my-custom-api.ts
import { NangoIntegration } from '@nangohq/types';

export default NangoIntegration({
  // Provider name
  provider: 'my-custom-api',
  
  // Authentication type
  auth: {
    type: 'api_key', // or 'oauth2', 'basic'
    credentials: {
      api_key: { type: 'string', required: true }
    }
  },
  
  // Available actions
  actions: {
    list_items: {
      endpoint: '/items',
      method: 'GET',
      output: { type: 'array' }
    },
    create_item: {
      endpoint: '/items',
      method: 'POST',
      input: { type: 'object' },
      output: { type: 'object' }
    }
  }
});
```

### Deploy Custom Integration

```bash
# Deploy to Nango
nango deploy integrations/my-custom-api.ts
```

## Error Handling

```python
from nango import Nango, NangoError

try:
    result = nango.proxy(
        provider="github",
        endpoint="/repos/owner/repo/issues",
        connection_id="user-github-123"
    )
except NangoError as e:
    if e.code == "auth_expired":
        # Re-authorize
        auth_url = nango.get_auth_url("github")
        print(f"Please re-authorize: {auth_url}")
    elif e.code == "rate_limited":
        # Wait and retry
        time.sleep(e.retry_after)
    else:
        raise
```

## Best Practices for Agents

### 1. Connection Management

- Store connection IDs with user context
- Check connection health before operations
- Implement re-auth flows automatically

### 2. Error Recovery

- Handle rate limits gracefully
- Cache frequently accessed data
- Provide clear error messages to users

### 3. Security

- Never expose API keys in prompts
- Use environment variables for secrets
- Implement permission scoping

### 4. Performance

- Batch operations when possible
- Use webhooks instead of polling
- Implement request caching

## MCP Integration for OpenClaw

To use Nango with OpenClaw agents:

```python
# In your OpenClaw skill or tool
from nango import Nango

class NangoTool:
    def __init__(self):
        self.nango = Nango()
    
    def call_api(self, provider: str, endpoint: str, connection_id: str, **params):
        """Generic API calling tool for any provider."""
        return self.nango.proxy(
            provider=provider,
            endpoint=endpoint,
            connection_id=connection_id,
            params=params
        )
    
    def list_providers(self):
        """List all available providers."""
        return self.nango.list_providers()
    
    def get_provider_actions(self, provider: str):
        """Get available actions for a provider."""
        return self.nango.get_actions(provider)
```

## Common Issues

### Issue: "Connection not found"
- Ensure connection_id matches what was created
- Check if credentials expired

### Issue: "Provider not supported"
- Check full list at https://nango.dev/integrations
- Create custom integration for unsupported providers

### Issue: "Rate limited"
- Implement exponential backoff
- Consider upgrading Nango plan

## Resources

- **Nango Dashboard**: https://app.nango.dev
- **Documentation**: https://docs.nango.dev
- **Integration Catalog**: https://nango.dev/integrations
- **GitHub**: https://github.com/NangoHQ/nango
- **Community**: https://nango.dev/community

## Pricing

- **Free Tier**: 10,000 API calls/month
- **Pro**: $49/month for 100,000 calls
- **Enterprise**: Custom pricing for unlimited

Free tier is sufficient for development and small projects.