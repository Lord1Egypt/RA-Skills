---
name: m365-mcp
description: Production-grade Microsoft 365 MCP server with delegated OAuth, multi-account support, pagination, rate limiting, and 47 tools covering email, calendar, contacts, OneDrive, Teams, tasks, and users.
metadata:
  openclaw:
    homepage: https://github.com/sam2kb/m365-mcp#readme
    requires:
      bins:
        - m365-mcp
        - m365-mcp-auth
    envVars:
      - name: M365_ACCOUNT
        required: false
        description: Optional account name selected from the local account store.
      - name: M365_TIMEZONE
        required: false
        description: Optional IANA timezone for calendar operations; defaults to UTC.
      - name: M365_MCP_AUTH_DIR
        required: false
        description: Optional absolute path for the local OAuth account and token store.
      - name: M365_MCP_READ_ONLY
        required: false
        description: Set true to request read-only scopes and disable all mutating tools.
      - name: M365_MCP_DIRECTORY_READ
        required: false
        description: Opt in to delegated User.Read.All for organization directory tools; requires admin consent.
    install:
      - kind: node
        package: "@sam2kb/m365-mcp"
        bins:
          - m365-mcp
          - m365-mcp-auth
---

# m365-mcp

Production-grade Microsoft 365 MCP server combining the best of office365-connector (delegated OAuth, multi-account) and mcp-microsoft365 (MCP protocol, full scope), with production-ready features: pagination, rate limiting, retry logic, and full TypeScript.

## Requirements

- Node.js 18+
- Azure Entra ID App Registration with delegated Microsoft Graph permissions
- Device code OAuth (no client-credentials, no tenant-wide access)

## Capabilities

### Email (9 tools)

- List, read, send, reply, search, move, delete, mark read/unread, list folders

### Calendar (10 tools)

- List events with organizer/response status, read event notes, today view, week view, create (with Teams meeting), update, explicit organizer cancellation, attendee decline, free/busy

List, get, create, and update accept an optional calendar ID. Note reads include
body format, full length, and truncation status. Do not write truncated notes
back as a complete body. When replacing online-meeting notes, preserve the
meeting details in the body.

### Contacts (12 tools)

- Rich contact CRUD, exact category assignment and any/all filtering, category enumeration, folder-scoped contacts, contact-folder CRUD, and relevance-ranked People API recipient search across mailbox and optional directory sources. People results support fuzzy search, identity-type filters, relevance scores, and optional profile details. Private Outlook Contact Lists and their membership are not exposed by Microsoft Graph.

### OneDrive (5 tools)

- List files, search, read content, metadata, create folders

### Teams (3 tools)

- List chats, read messages, send messages

### Tasks (5 tools)

- List lists, list tasks, create, update, delete

### Users (3 tools)

- List org users, profile lookup, manager lookup

## Security and consent

- OAuth and API requests use `login.microsoftonline.com` and `graph.microsoft.com`.
  File reads also use HTTPS download URLs supplied by Graph, including OneDrive
  and SharePoint hosts. Off-origin downloads do not receive the Graph bearer token.
- Device-code OAuth grants delegated access as the signed-in user. Read tools can
  expose private mail, files, calendars, contacts, Teams chats, tasks, and user data.
- Send, reply, move, create, update, cancel, decline, and delete tools change real Microsoft 365
  data. Configure the MCP client to require explicit user approval for those tools.
- Tools publish standard MCP read-only, destructive, idempotent, and open-world
  annotations so compatible clients can apply confirmation policies.
- Set `M365_MCP_READ_ONLY=true` for an enforced least-privilege mode. It requests
  read-only OAuth scopes, omits mutating tools from discovery, and rejects direct
  calls to them.
- Refresh and access tokens are stored as plaintext JSON under
  `~/.m365-mcp/auth/` (or `M365_MCP_AUTH_DIR`), protected with directory mode
  `0700` and file mode `0600` where supported. Protect that directory and revoke
  the app's Microsoft account consent if a token or device is compromised.
- File reads stop at `maxBytes` (50,000 by default; maximum 1,000,000).
- Set `M365_MCP_DIRECTORY_READ=true` during login and server startup to request
  organization directory access with admin consent. Sign in again after changing
  scope settings or an account's tenant/client registration.

## Setup

ClawHub installs the prebuilt npm package automatically. For a manual install:

```bash
npm install --global @sam2kb/m365-mcp

# Add account
m365-mcp-auth add work <tenantId> <clientId> you@company.com

# Authenticate
m365-mcp-auth login --account=work
```

Then configure `m365-mcp` as a stdio MCP server in your client.

See the [project README](https://github.com/sam2kb/m365-mcp#readme) for the full Azure setup guide.
