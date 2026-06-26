# Connecting to Miro MCP

This guide walks you through connecting your MCP-compatible client to Miro's MCP Server and authenticating with OAuth 2.1.

## Prerequisites

Before you begin, ensure:

- **MCP-capable client:** You're using a tool with MCP client capabilities (Cursor, Claude Code, Replit, Lovable, VSCode, Windsurf, etc.)
- **Workspace access:** You have appropriate access permissions to your Miro workspace (at least member of the team)
- **OAuth 2.1 support:** Your client is updated to support OAuth 2.1 authentication
- **Network access:** Your client can reach `https://mcp.miro.com/`

## Configuration Steps

### 1. Open MCP Configuration

Open your MCP-compatible client's settings and navigate to the MCP configuration section. The exact location varies by client:
- **Cursor/Windsurf:** Settings → MCP
- **Lovable:** Settings → Integrations → Your MCP Servers
- **Claude Code:** Via CLI: `claude mcp add --transport http miro https://mcp.miro.com`
- **Replit:** Integration setup button
- **VSCode/Copilot:** MCP Registry installation

### 2. Add Miro MCP Configuration

Add the following JSON configuration to your MCP settings:

```json
{
  "mcpServers": {
    "miro-mcp": {
      "url": "https://mcp.miro.com/",
      "disabled": false,
      "autoApprove": []
    }
  }
}
```

**Configuration fields:**
- `url`: The Miro MCP Server endpoint (always `https://mcp.miro.com/`)
- `disabled`: Set to `false` to enable the connection
- `autoApprove`: Leave empty for standard OAuth flow

### 3. Click "Connect" and Authenticate

After adding the configuration:
1. Click the "Connect" or "Authenticate" button in your client
2. Your client will open a new window or redirect to Miro's OAuth server
3. If you're not logged into Miro, you'll be prompted to log in with your Miro account
4. Review the requested permissions (board access, data read/write)

## Miro OAuth 2.1 Flow

The OAuth flow has several key steps:

### Step 1: Authorization Request
Your client sends an authorization request to Miro with:
- `client_id` (generated dynamically)
- `redirect_uri` (callback URL in your client)
- `scope` (requested permissions: typically `boards:read boards:write`)
- `state` (random token for security, prevents CSRF)
- `response_type=code` (OAuth authorization code flow)

### Step 2: User Authentication & Consent
Miro's OAuth server:
- Authenticates the user (email/password or SSO if configured)
- Shows a consent screen with requested permissions
- User reviews and approves

### Step 3: Team Selection (CRITICAL)

A critical step unique to Miro MCP:

**The user must explicitly select which Miro team the MCP app can access.**

This is a security feature — MCP is team-scoped. The app can only read/write boards in the selected team.

- If you have access to multiple Miro teams, you'll see a dropdown
- Select the team containing the boards you want to access
- Click "Add" or "Continue"

**Important:** If you later try to access a board from a different team, you'll get an access error. Simply re-authenticate and select the correct team.

### Step 4: Authorization Code
After team selection, Miro redirects back to your client with:
- `code` (authorization code, valid for ~10 minutes)
- `state` (the same token sent in step 1; client verifies it matches)

### Step 5: Token Exchange
Your client exchanges the authorization code for tokens via a server-to-server request:
- Sends: `code`, `client_id`, `client_secret`, `redirect_uri`
- Receives: `access_token` (for API calls), `refresh_token` (for obtaining new access tokens)

### Step 6: Board Access
Your agent is now authenticated. API calls include the `access_token`:

```
Authorization: Bearer {access_token}
GET https://mcp.miro.com/v1/boards/{board_id}
```

## Team Selection: Why It Matters

**Scenario:** You have access to two Miro teams:
- Team A (containing boards for Project X)
- Team B (containing boards for Project Y)

During OAuth, you select **Team A**. Later, you try to access a board from **Team B**:

```
Agent: "Summarize this board: https://miro.com/app/board/team-b-board-id/"
Result: ❌ Access Denied (403 Forbidden)
```

Why? The MCP app is scoped to Team A; it doesn't have access to Team B's boards.

**Solution:** Re-authenticate and select Team B:
1. Click "Reconnect" or "Re-authenticate" in your client
2. Follow the OAuth flow again
3. Select **Team B** during team selection
4. Now you can access Team B's boards

You can re-authenticate multiple times to switch between teams, though this requires repeating the OAuth flow.

## Security & Rate Limits

### Authentication Security

- **OAuth 2.1:** Industry standard, secure authorization protocol
- **Dynamic client registration:** No static credentials stored long-term
- **Scope minimization:** Request only necessary permissions
- **Token expiry:** Access tokens expire (typically 1 hour); refresh tokens are used to obtain new ones
- **PKCE recommended:** Proof Key for Public Clients (PKCE) is recommended for added security

### Standard API Rate Limits

Standard API rate limits apply to all Miro MCP operations. Rate limits are:
- **Per-user** (counted across all tool calls by the same user)
- **Calculated from:** API request count, data volume, and time windows
- **Enforcement:** Returns 429 Too Many Requests if exceeded

### Tool-Specific Rate Limits

Some tools have stricter, tool-specific limits:
- **`context_get`** is the most restrictive (uses Miro AI credits)
- Other tools have standard limits
- Limits are subject to change; check Miro documentation for latest values

**If rate-limited:**
- Reduce parallel operations (especially `context_get`)
- Batch requests where possible
- Implement exponential backoff retry logic
- Contact Miro Developer Discord for guidance on limits

### Enterprise Security Compliance

- Meets enterprise security standards
- User permission-governed access
- Team-level audit trails
- Compliant with common standards (SOC 2, HIPAA-eligible, etc.)

## Troubleshooting Connection Issues

### Issue: "MCP Client Not Supported"
**Cause:** Your client doesn't have MCP capabilities or MCP is not enabled.

**Solution:**
- Verify your client supports MCP (see [mcp-overview.md](mcp-overview.md#supported-clients-verified))
- Check that your client is updated to the latest version
- Enable MCP in client settings if available

### Issue: "Remote Server Connection Not Supported"
**Cause:** Your client has MCP support but doesn't support remote connections (only local MCP servers).

**Solution:**
- Check your client's documentation for remote MCP server support
- Some clients only support local stdio-based MCP servers
- Contact the client's developers to request remote MCP support

### Issue: "Connection Timeout" or "Cannot Reach https://mcp.miro.com/"
**Cause:** Network connectivity issue.

**Solution:**
- Verify your internet connection
- Check if `https://mcp.miro.com/` is reachable from your network (no firewall blocks)
- Ensure your client is using a proxy correctly if required
- Try again from a different network

### Issue: "Invalid Team" or "Access Denied After OAuth"
**Cause:** You authenticated against one team but are trying to access boards from a different team.

**Solution:**
- See [Team Selection: Why It Matters](#team-selection-why-it-matters)
- Re-authenticate and select the correct team
- If unsure which team a board belongs to, check the board's team settings in Miro

### Issue: "OAuth Flow Not Opening" or "Callback Not Received"
**Cause:** Browser redirect or callback URL issue.

**Solution:**
- Ensure pop-ups are not blocked in your browser
- Check firewall/antivirus for blocking redirects
- Verify `redirect_uri` is correctly configured in your client
- Try a different browser if issue persists

### Issue: "Rate Limited (429)"
**Cause:** You've exceeded API rate limits.

**Solution:**
- Reduce the frequency of API calls
- Batch operations (e.g., `table_sync_rows` instead of individual updates)
- Implement exponential backoff retry logic
- Wait 60+ seconds before retrying
- Contact Miro Developer Discord for guidance on limits

## Using MCP Inspector for Debugging

For detailed connection diagnostics, use **MCP Inspector** (part of the MCP toolkit):

```bash
# Install MCP Inspector
npm install -g @modelcontextprotocol/inspector

# Start inspector (connects to your MCP server)
mcp-inspector https://mcp.miro.com/
```

MCP Inspector allows you to:
- Test tool calls directly
- View request/response details
- Debug authentication issues
- Inspect available tools and prompts

## Enterprise Setup: Enabling MCP for Your Organization

If you're on a **Miro Enterprise Plan**, your organization administrator must first enable Miro MCP Server before team members can use it.

**Admin steps:**
1. Log into your Miro organization's admin dashboard
2. Navigate to **Security** or **Integrations** settings
3. Find **MCP Server** or **Model Context Protocol**
4. Enable for your organization
5. Optionally restrict to specific teams

Once enabled by your admin, team members can authenticate normally using OAuth.

## Next Steps

- **Client-specific setup:** See [references/ai-coding-tools.md](ai-coding-tools.md) for step-by-step instructions for your specific client
- **Using the API:** See [references/mcp-prompts.md](mcp-prompts.md) for available tools and prompts
- **Best practices:** See [references/best-practices.md](best-practices.md) for workflow patterns and optimization
