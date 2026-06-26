# Miro MCP Overview

## What is Miro MCP?

Miro MCP (Model Context Protocol) is a hosted server that gives AI agents and tools secure, enterprise-grade access to Miro boards within your organization. It enables AI assistants to read board context, create and modify diagrams, generate code, and collaborate on visual workspaces while maintaining fine-grained access controls and rate limiting.

**Key characteristics:**
- **Hosted by Miro** — No server setup required; agent connects to `https://mcp.miro.com/`
- **OAuth 2.1 authentication** — Dynamic client registration, no static API keys
- **Team-scoped access** — MCP app is bound to a specific Miro team; agents can only access boards in that team
- **Enterprise-grade security** — Compliant with enterprise security standards, user permission-governed, standard rate limiting
- **Beta status** — Feature set and UX subject to change; feedback welcomed

## Why Use Miro MCP?

### Secure Access
OAuth 2.1 with dynamic client registration means no long-lived credentials or API keys are stored. Each connection is authenticated per user, and access is governed by existing Miro workspace permissions. If a user doesn't have access to a board, the agent can't access it either.

### Full Workspace Access
Agents can read and write to Miro boards with the same permissions as the authenticated user. This includes reading document content (as HTML), prototype screens (as UI markup), and frames (as AI-summarized text), then creating diagrams, documents, and tables in response.

### Optimized for AI
Miro MCP is purpose-built for AI interactions. The tools and prompts are designed for efficient LLM processing, with built-in context exploration, structured data retrieval, and diagram generation via domain-specific language (DSL).

### Real-Time Collaboration
Agents can participate in live board collaboration, adding diagrams and suggestions as teams work. Changes are reflected immediately on the board, enabling real-time feedback loops.

## Use Cases

### Diagram Generation

Agents can generate visual diagrams on Miro boards from multiple sources:

- **From Code Repositories:** Point the agent to a GitHub URL or codebase → agent analyzes structure and generates architecture/system diagrams (UML class diagrams, sequence diagrams, ERD)
- **From Product Requirement Documents:** Share PRD text or upload to board → agent creates user flows, workflow diagrams, state machines
- **From Text Descriptions:** Describe a system verbally → agent visualizes it as architecture diagram, data flow diagram, or process flow
- **GitHub URLs:** Agent can directly analyze GitHub repos and generate system architecture diagrams

Diagram types supported: Flowchart, UML class diagram, UML sequence diagram, Entity-Relationship Diagram (ERD).

### Code Generation

Agents can generate working code and documentation from board content:

- **PRD to Implementation:** Board contains product requirements → agent generates comprehensive documentation, code structure recommendations, and implementation guidance
- **Diagram to Code:** Architecture diagram on board → agent generates code structure, class definitions, module organization matching the design
- **Prototype to Implementation:** Prototype screens on board → agent uses them as implementation guides, generates UI code, validation logic, data models
- **Iterative Refinement:** Read board context → suggest improvements → generate updated code or docs → update board with results

### Collaboration & Analysis

- **Board Summarization:** Summarize board content for stakeholders, extract key decisions, document agreements
- **Cross-functional Communication:** Diagrams bridge technical and non-technical team members
- **Meeting Notes:** Generate meeting notes from whiteboard sketches, action items from diagrams

## Security Model

### Authentication: OAuth 2.1 with Dynamic Client Registration

- **Per-user authentication** — Each agent connection is authenticated as a specific user
- **No static API keys** — Dynamic client registration means no long-lived credentials to store or rotate
- **Scope minimization** — Agent requests only necessary permissions (e.g., `boards:read`, `boards:write`)
- **Token expiry** — Access tokens expire; refresh tokens are used to obtain new ones without re-authentication

### Authorization & Permissions

- **User permission-governed** — Agent can only access boards the authenticated user has access to
- **Team-scoped** — MCP app is bound to a specific Miro team (selected during OAuth); agent only sees boards in that team
- **Fine-grained control** — Workspace admins control which teams enable MCP

### Enterprise Compliance

- **Enterprise security standards** — Designed to meet enterprise security requirements
- **Standard rate limiting** — Protected against overuse and abuse
- **Audit-ready** — User actions logged (team-level)

## Supported Clients (Verified)

As of February 2026, Miro MCP is tested and works with:

| Client | Type | Status |
|--------|------|--------|
| Cursor | IDE + MCP | ✅ Verified |
| Claude Code | CLI MCP client | ✅ Verified |
| Replit | Web IDE | ✅ Verified |
| Lovable | Web App Builder | ✅ Verified |
| VSCode + GitHub Copilot | Editor + AI | ✅ Verified |
| Windsurf | IDE + MCP | ✅ Verified |
| Gemini CLI | CLI | ✅ Verified |
| Kiro CLI | CLI | ✅ Verified |
| Amazon Q IDE Extension | IDE Extension | ✅ Verified |
| Claude (Web & Desktop) | Chat Interface | ✅ Verified |
| Kiro IDE | IDE | Supported |
| Glean | Enterprise Search | Supported |
| Devin | AI Agent | Supported |
| OpenAI Codex | Code LLM | Supported |

Each client has slightly different UI for MCP configuration, but the OAuth flow and capabilities are identical.

## Limitations & Current Focus

### Beta Status
Miro MCP is in **beta release**, intended for evaluation and feedback. Feature set and user experience may change in future releases. Feedback is actively solicited via official feedback form.

### Currently Supported Use Cases
The beta focuses on two main use cases:
1. **Generate diagrams** on a Miro board based on PRD, code, or text
2. **Generate code** based on Miro board content (PRDs, diagrams, images)

Additional use cases are under development. If you have requests, use the official feedback form.

### Rate Limits

- **Standard API rate limits** apply to all MCP operations (totaled per user across all tool calls)
- **Tool-specific limits** may be stricter; some tools have additional rate limits
- **`context_get` is the only tool that uses Miro AI credits** — all other tools are free
- **Rate limit changes:** Tool-specific limits are subject to change; check documentation for latest limits

If rate-limited:
- Reduce the amount of parallel operations
- Batch requests where possible (e.g., use `table_sync_rows` for bulk updates instead of individual calls)
- Wait before retrying
- Contact Miro Developer Discord for guidance on higher limits

## Next Steps

- **Getting Started:** See [references/mcp-connection.md](mcp-connection.md) for prerequisites and setup instructions
- **Choose Your Client:** See [references/ai-coding-tools.md](ai-coding-tools.md) for step-by-step setup for your specific MCP client
- **Explore Tools & Prompts:** See [references/mcp-prompts.md](mcp-prompts.md) for complete tool reference and usage examples
- **Learn Best Practices:** See [references/best-practices.md](best-practices.md) for workflow patterns and common gotchas
