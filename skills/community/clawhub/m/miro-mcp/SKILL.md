---
name: miro-mcp
description: Connect OpenClaw agents to Miro via Model Context Protocol (MCP). Use when generating diagrams, visualizing code, brainstorming board layouts, or integrating Miro into AI-powered design workflows. Supports OAuth 2.1 authentication, 14+ MCP-compatible clients (Cursor, Claude Code, Replit, Lovable, VSCode/Copilot, Gemini CLI, Windsurf, Kiro CLI, Amazon Q, others). Best for design thinking, architecture visualization, project planning, collaborative ideation.
---

# Miro MCP Integration

## Quick Start

Miro MCP enables AI agents to read from and write to Miro boards via the Model Context Protocol—an open standard for AI-external system integration. Your agent can generate diagrams, analyze board content, and create code from visual designs.

**Prerequisites:**
- MCP-capable client (Cursor, Claude Code, Replit, Lovable, VSCode, etc.)
- OAuth 2.1 support in your client
- Active Miro workspace access

**Minimal Setup:**
1. Add MCP configuration: `url: https://mcp.miro.com/`
2. Click "Connect" and authenticate via OAuth 2.1
3. Select your Miro team during OAuth flow
4. Start prompting with board URLs

**Quick Example:**
```
Prompt: "Summarize the content on this board: https://miro.com/app/board/uXjVGAeRkgI=/"
Result: Agent reads board items and returns a summary
```

See [references/mcp-connection.md](references/mcp-connection.md) for detailed setup instructions per client.

## Core Capabilities

Miro MCP supports two primary use cases: **diagram generation** and **code generation**.

### Diagram Generation

Generate visual diagrams directly on Miro boards from code, PRDs, or text descriptions:
- **From Code:** Provide repository URLs or code snippets → agent generates architecture/data flow diagrams (UML, flowchart, ERD)
- **From PRDs:** Share product requirement documents → agent creates visual workflows, user flows, state diagrams
- **From Text:** Describe a system → agent visualizes it as architecture or sequence diagram
- **From GitHub URLs:** Agent analyzes GitHub repos and generates architectural diagrams

Tool: Use `code_explain_on_board` prompt or `diagram_create` tool with DSL (flowchart, UML class/sequence, ERD).

### Code Generation

Generate working code from board content:
- **PRD to Code:** Board contains product requirements → agent generates documentation + implementation guidance
- **Diagram to Code:** Architecture diagram on board → agent generates code structure matching the design
- **Prototype to Code:** Prototype screens on board → agent uses them as implementation guides

Tool: Use `code_create_from_board` prompt to analyze board and generate docs/code.

### Collaboration Features

- Read board context (frames, documents, prototypes, diagrams, tables, images)
- Write new diagrams and documents to boards
- Update existing board content via find-and-replace
- Access board items with cursor-based pagination
- Team-scoped access (MCP app is team-specific)

## Supported Clients

Miro MCP has been tested and verified with 14+ MCP-compatible clients:

| Client | Method | Notes |
|--------|--------|-------|
| **Cursor** | Config file + OAuth | JSON config in settings |
| **Claude Code** | CLI: `claude mcp add` | Command-line setup |
| **Replit** | Web UI + OAuth | Install button integration |
| **Lovable** | Web UI + OAuth | Settings → Integrations |
| **VSCode/GitHub Copilot** | MCP Registry + OAuth | GitHub MCP Registry link |
| **Windsurf** | Config file + OAuth | JSON config in settings |
| **Gemini CLI** | CLI setup | Video tutorial available |
| **Kiro CLI** | Config file + OAuth | .kiro/settings/mcp.json |
| **Amazon Q IDE** | Settings + OAuth | IDE extension config |
| **Claude (Web/Desktop)** | Connectors + OAuth | Add connectors in chat |
| **Kiro IDE** | Built-in | Native MCP support |
| **Glean** | Native | MCP integration ready |
| **Devin** | Native | Native MCP support |
| **OpenAI Codex** | Protocol-based | Direct MCP access |

See [references/ai-coding-tools.md](references/ai-coding-tools.md) for step-by-step setup per client.

## Configuration Guidance

### OAuth 2.1 Flow Overview

Miro MCP uses OAuth 2.1 with dynamic client registration for secure authentication:

1. **Request authorization** → Your client constructs an auth URL with `client_id`, `redirect_uri`, `scope`
2. **Miro OAuth server** → User logs in (or confirms existing session) and consents to requested permissions
3. **Team Selection** (critical) → User explicitly selects which Miro team the MCP app can access
4. **Authorization code** → Miro redirects back with `authorization_code`
5. **Token exchange** → Your client exchanges code for `access_token` and `refresh_token`
6. **Board access** → Agent includes `access_token` in API calls to Miro MCP Server

**Why team selection matters:** MCP is team-scoped. If you reference a board from a different team than the one you authenticated against, you'll get access errors. Simply re-authenticate and select the correct team.

### Configuration JSON

Standard JSON configuration (valid for most clients):

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

### Rate Limits

- **Standard API limits** apply to all operations (counted per user across all tool calls)
- **Tool-specific limits** may be stricter (subject to change)
- **`context_get` is expensive** — uses Miro AI credits (only tool that does)
- **Optimization:** Batch operations, avoid parallel `context_get` calls, cache frequently accessed content

### Enterprise Notes

If you're on **Miro Enterprise Plan**, your admin must first enable Miro MCP Server in your organization before you can use it. Contact your Miro administrator for enablement.

## Common Workflows

### Workflow 1: Architecture Diagram from Codebase

```
User prompt: "Analyze my codebase at ~/dev/myapp and create an architecture diagram on this board: [board-URL]"

Agent steps:
1. Read codebase structure
2. Analyze dependencies and modules
3. Use code_explain_on_board to generate UML diagram
4. Create diagram on Miro board via diagram_create tool
```

### Workflow 2: Code Generation from PRD

```
User prompt: "This board has our PRD. Generate implementation docs and code guidance."

Agent steps:
1. Use context_explore to find PRD document on board
2. Use context_get to read PRD details
3. Use code_create_from_board prompt
4. Generate docs and implementation guidance
5. Create doc_create items on board with generated content
```

### Workflow 3: Iterative Design Feedback

```
User prompt: "Summarize this prototype and suggest improvements"

Agent steps:
1. Use context_explore to find prototype screens
2. Use context_get to read screen details/markup
3. Analyze and suggest UX improvements
4. Use doc_create to add feedback document to board
```

## REST API Direct Integration (Automation & Scripting)

Beyond MCP, Miro's **REST API** enables programmatic board automation via curl/bash scripting. Useful for:
- Bulk board creation and templating
- Automated shape/content generation
- Integration with OpenClaw workflows
- Custom CI/CD board generation
- Template recreation and versioning

### Authentication

Use OAuth 2.1 Bearer tokens:
```bash
curl -H "Authorization: Bearer $ACCESS_TOKEN" https://api.miro.com/v2/...
```

Tokens obtained via OAuth flow (see OAuth setup in SKILL.md), valid for defined scope.

### Board Creation

```bash
curl -X POST https://api.miro.com/v2/boards \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "My Board",
    "description": "Auto-generated template"
  }' | jq '.id'
```

### Shape Creation (Key API Format)

**Correct nested structure** (discovered via Phase B testing):

```bash
curl -X POST https://api.miro.com/v2/boards/{board_id}/shapes \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "shapeType": "rectangle",
      "content": "Label text"
    },
    "geometry": {
      "width": 200,
      "height": 100
    },
    "position": {
      "x": 0,
      "y": 0,
      "origin": "center"
    },
    "style": {
      "fillColor": "#3b82f6",
      "borderColor": "#1e40af",
      "borderWidth": 2
    }
  }'
```

**Shape types:** rectangle, circle, ellipse, diamond, triangle, pentagon, hexagon, etc.

### Text Elements

```bash
curl -X POST https://api.miro.com/v2/boards/{board_id}/text \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "<b>Bold</b> and <i>italic</i> text",
    "geometry": {
      "width": 300,
      "height": 100
    },
    "position": {
      "x": 0,
      "y": 0,
      "origin": "center"
    },
    "style": {
      "fontSize": 24,
      "color": "#000000",
      "fontFamily": "Arial",
      "textAlign": "center"
    }
  }'
```

### Performance & Scale

- **Shape creation speed:** ~46ms per shape (tested)
- **Batch operations:** Can rapidly create 10-20+ shapes per second
- **Rate limits:** Standard Miro API limits apply (generous for most use cases)
- **Script execution:** Bash/curl scripts complete full board creation (40+ elements) in < 5 seconds

### Template Recreation Pattern

Effective structure for reusable templates:

```
1. Board creation (metadata)
2. Section headers (color-coded background + text)
3. Content containers (boxes, cards, lists)
4. Visual hierarchy (title → sections → items)
5. Guides (methodology, examples, legends)
```

See `miro-journey-map-recreation.sh` in workspace for working example.

### Common REST API Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/boards` | Create board |
| GET | `/boards/{id}` | Get board info |
| POST | `/boards/{id}/shapes` | Add shape |
| POST | `/boards/{id}/text` | Add text |
| POST | `/boards/{id}/frames` | Add frame (container) |
| GET | `/boards/{id}/items` | List board items |
| PATCH | `/boards/{id}/items/{id}` | Update item |
| DELETE | `/boards/{id}/items/{id}` | Delete item |

### Practical Example: Color-Coded Sections

```bash
# Create section background
curl -X POST https://api.miro.com/v2/boards/$BOARD_ID/shapes \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"data\": {\"shapeType\": \"rectangle\"},
    \"geometry\": {\"width\": 1400, \"height\": 120},
    \"position\": {\"x\": 0, \"y\": -400, \"origin\": \"center\"},
    \"style\": {\"fillColor\": \"#3b82f6\", \"borderWidth\": 2}
  }"

# Add section title
curl -X POST https://api.miro.com/v2/boards/$BOARD_ID/text \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{
    \"content\": \"<b>Section Title</b>\",
    \"geometry\": {\"width\": 1300, \"height\": 100},
    \"position\": {\"x\": -650, \"y\": -400, \"origin\": \"center\"},
    \"style\": {\"fontSize\": 28, \"color\": \"#ffffff\"}
  }"
```

### Key Learnings

- **API structure matters:** Correct nesting of `data`, `geometry`, `position`, `style` is critical
- **Bash automation works reliably:** No need for SDK when direct API is clear
- **Color palettes are key:** Consistent colors (Blue, Purple, Green, Yellow) make templates professional
- **Positioning uses center origin:** (0, 0) is canvas center; adjust x/y for grid layout
- **Template scripts are reusable:** Save working scripts; iterate on color/content/layout

## Resource Links

- **Setup by Client:** See [references/ai-coding-tools.md](references/ai-coding-tools.md) for detailed step-by-step instructions for all 14 supported clients
- **Connection Details:** See [references/mcp-connection.md](references/mcp-connection.md) for OAuth flow, prerequisites, troubleshooting, and enterprise setup
- **MCP Overview:** See [references/mcp-overview.md](references/mcp-overview.md) for what MCP is, why it matters, security model, and capabilities overview
- **Tools & Prompts:** See [references/mcp-prompts.md](references/mcp-prompts.md) for complete tool reference (14 tools), built-in prompts, and rate limit details
- **Best Practices:** See [references/best-practices.md](references/best-practices.md) for workflow patterns, common gotchas (team mismatch, OAuth expiry, rate limits), and optimization strategies
- **REST API Essentials:** See [references/rest-api-essentials.md](references/rest-api-essentials.md) for tool-by-tool API reference, error handling, cost model, and real-world examples
- **REST API Automation Scripts:** See `/Users/bigbubba/.openclaw/workspace/miro-journey-map-recreation.sh` for working template recreation example
