# Connecting Miro MCP to AI Coding Tools

This guide provides step-by-step setup instructions for connecting Miro MCP to 14+ MCP-compatible clients. The OAuth 2.1 flow is identical across all clients, but each tool has a slightly different UI. Refer to this guide for your specific client.

## Claude (Web & Desktop App)

Use this method for the standard Claude chat interface (works across web and desktop).

**Setup steps:**
1. Open Claude chat (web or desktop app)
2. In the message box, click the **+** (plus) icon
3. Select **"Add connectors"**
4. Search for **"Miro"** in the Web tab
5. Click the **+** icon on the Miro card
6. Click **"Connect"** on the following screen
7. Follow the **Miro OAuth flow** to authenticate and select your team
8. You'll see **"Connected to Miro"** confirmation
9. You can now reference board URLs in your prompts

**Example prompt:**
```
Summarize the content on this board: https://miro.com/app/board/uXjVGAeRkgI=/
```

## Lovable

Lovable integrates Miro MCP through its Settings → Integrations menu.

**Setup steps:**
1. Log into [lovable.dev](https://lovable.dev/)
2. Click your **profile** (top right)
3. Click **Settings** → **Integrations**
4. Scroll down to **"Your MCP Servers"**
5. Find **Miro** and click **"Set up"**
6. Click **"Connect"**
7. Follow the **Miro OAuth flow** and select your team
8. Done! You can now reference Miro boards in your prompts

**Example prompt:**
```
Build me a landing page based on the content of this board: https://miro.com/app/board/uXjVGAeRkgI=/
```

## Replit

Replit uses an integration button for quick MCP setup.

**Setup steps:**
1. Click the **"Install MCP Server"** button in Replit (found in integrations)
2. Click **"Test & Save"**
3. Click **"Authorize with OAuth"**
4. Follow the **Miro OAuth flow** and select your team
5. Once authorized, you can reference Miro boards in your Replit projects

**Example use case:**
- Create a Miro board with your project requirements
- Reference the board URL in your Replit AI agent
- Agent reads the board and generates code matching the requirements

## Cursor

Cursor uses a JSON config file for MCP setup.

**Setup steps:**
1. Open **Cursor Settings** → **Cursor Settings** (or settings.json)
2. Find the **MCP** section
3. Click **"Add a Custom MCP Server"**
4. Enter the following JSON:

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

5. Click the **"Authenticate"** button that appears next to miro-mcp
6. Follow the **Miro OAuth flow** in the browser window that opens
7. Return to Cursor and verify that **tools and prompts are enabled**
8. You're ready to start generating diagrams and code with Miro

**Example prompt:**
```
Create me a sequence diagram of the data flow for my Cursor + Miro workflow and add it to this board: https://miro.com/app/board/uXjVGAeRkgI=/
```

## VSCode & GitHub Copilot

VSCode integrates Miro MCP through GitHub's MCP Registry.

**Setup steps:**
1. Find **Miro's MCP Server** in [GitHub's MCP Registry](https://github.com/mcp/miroapp/mcp-server)
2. Click **"Install MCP server"**
3. Open the **Miro OAuth flow** and authenticate with your Miro account
4. Install the MCP app on your desired team
5. In VSCode, Copilot can now access Miro boards

**Using built-in prompts:**
- Type **`/`** to see available Miro prompts
- Click the **tools icon** to see available Miro tools

**Explicit tool reference (important):**
To ensure Copilot uses exactly the tools you want:
```
Use the create_diagram tool to create me a diagram of my codebase at ~/dev/codebase 
and add it to this Miro board: https://miro.com/app/board/uXjVGAeRkgI=/
```

**Important:** Ensure the board you're referencing is in the team you authenticated against.

## Claude Code (CLI)

Claude Code uses command-line MCP setup.

**Setup steps:**
1. Login to Claude Code:
   ```bash
   claude login
   ```

2. Add the Miro MCP to Claude Code:
   ```bash
   claude mcp add --transport http miro https://mcp.miro.com
   ```

3. Authenticate with Miro:
   ```bash
   /mcp auth
   ```

4. Follow the **Miro OAuth flow** in your browser and select your team

5. Once authenticated, use Miro MCP prompts:
   ```bash
   /miro-mcp:code_explain_on_board
   ```

**Referencing tools directly:**
```
Use the code_create_from_board tool to analyze this board and generate implementation docs:
https://miro.com/app/board/uXjVGAeRkgI=/
```

**See also:** [Claude Code MCP Docs](https://code.claude.com/docs/en/mcp) for latest MCP setup information.

## Gemini CLI

Gemini CLI has native Miro MCP support with video tutorial.

**Setup steps:**
1. Install Gemini CLI
2. Configure Miro MCP endpoint
3. Authenticate via OAuth flow
4. Start using Miro MCP in your Gemini CLI prompts

**Note:** Video tutorial available in official Miro MCP documentation.

## Windsurf

Windsurf uses JSON config similar to Cursor.

**Setup steps:**
1. Go to **Windsurf Settings** → **Windsurf Settings** → **Cascade** → **Manage MCPs**
2. Click **"Configure"**
3. Add the following JSON:

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

4. Go through the **Miro OAuth flow** and select your team
5. Start prompting Windsurf to use Miro MCP

**Example:**
```
code_create_from_board: Add a board URL like https://miro.com/app/board/uX1234567/
```

## Kiro CLI

Kiro CLI uses a dedicated MCP config file.

**Setup steps:**
1. After installing Kiro CLI, create/edit `.kiro/settings/mcp.json`:

```json
{
  "mcpServers": {
    "miro-mcp": {
      "url": "https://mcp.miro.com/",
      "oauthScopes": []
    }
  }
}
```

2. Go through the **Miro OAuth flow** and select your team
3. Start using Miro MCP in Kiro CLI:

```bash
code_explain_on_board https://miro.com/app/board/uX1234567/
```

## Amazon Q IDE Extension

Amazon Q integrates Miro MCP through IDE extension config.

**Setup steps:**
1. Install the **Amazon Q IDE Extension** for your editor
2. Open the extension settings
3. Add Miro MCP configuration:
   - **Transport:** HTTP
   - **URL:** `https://mcp.miro.com`
4. Click **Save**
5. Go through the **Miro OAuth flow** when prompted
6. Ready to start prompting Amazon Q with Miro boards

**See also:** [Amazon Q IDE Extension Docs](https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/q-in-IDE-setup.html)

## Kiro IDE

Kiro IDE has built-in Miro MCP support.

**Setup steps:**
1. Open Kiro IDE
2. Navigate to MCP settings
3. Add Miro MCP configuration
4. Authenticate via OAuth flow
5. Start using Miro with Kiro IDE

## Glean

Glean (enterprise search) has native Miro MCP integration.

**Setup steps:**
1. Contact your Glean administrator for Miro MCP enablement
2. Authenticate via OAuth flow
3. Miro boards become searchable/accessible in Glean

## Devin

Devin (AI agent) supports Miro MCP directly.

**Setup steps:**
1. Configure Miro MCP in Devin settings
2. Authenticate via OAuth flow
3. Devin can now read and write to Miro boards

## OpenAI Codex

OpenAI Codex (code LLM) can access Miro MCP via protocol-based integration.

**Setup steps:**
1. Configure MCP transport for Codex
2. Point to `https://mcp.miro.com/`
3. Authenticate via OAuth
4. Codex can now use Miro tools

## Configuration JSON Reference

Standard JSON configuration used across multiple clients:

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

**Fields:**
- `url`: Always `https://mcp.miro.com/` (Miro's hosted MCP server)
- `disabled`: Set to `false` to enable; `true` to temporarily disable
- `autoApprove`: Leave empty `[]` for standard OAuth flow; some clients allow auto-approving specific tools here

## Common Setup Issues

### OAuth Flow Not Opening
- **Cause:** Browser pop-up blocked or callback URL misconfigured
- **Solution:** Allow pop-ups for your IDE; check client documentation for callback URL settings

### "Team Not Found" or "Access Denied"
- **Cause:** You authenticated against a different team than the boards you're trying to access
- **Solution:** Re-authenticate and select the correct team during OAuth flow

### "Tools Not Available"
- **Cause:** MCP server not fully initialized or authentication not complete
- **Solution:** Restart your client, ensure MCP is enabled in settings, re-authenticate

### Network/Timeout Errors
- **Cause:** Network connectivity or firewall blocking `https://mcp.miro.com/`
- **Solution:** Check internet connection, verify firewall isn't blocking the MCP endpoint, try from different network

## Next Steps

- **Common workflows:** See [references/best-practices.md](best-practices.md) for workflow patterns using your specific client
- **Tools & prompts reference:** See [references/mcp-prompts.md](mcp-prompts.md) for available tools and usage
- **Troubleshooting:** See [references/mcp-connection.md](mcp-connection.md#troubleshooting-connection-issues) for detailed troubleshooting
