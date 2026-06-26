# Best Practices for Miro MCP

This guide covers real-world workflow patterns, common gotchas, and optimization strategies based on the Miro MCP documentation.

## Workflow Patterns

### Pattern 1: Code → Diagram (Code Explanation)

**Goal:** Visualize code architecture on a Miro board.

**Steps:**
1. Provide code repository URL or codebase path to agent
2. Agent uses `code_explain_on_board` prompt
3. Agent analyzes code structure (classes, dependencies, data flows)
4. Agent uses `diagram_get_dsl` to fetch diagram syntax
5. Agent uses `diagram_create` with UML/flowchart to visualize
6. Agent uses `doc_create` to add explanatory documentation

**When to use:**
- Onboarding new team members
- Documenting existing systems
- Architecture review and analysis

**Example:**
```
Agent: "Analyze ~/dev/myapp codebase and create architecture diagrams on this board"
Result: UML class diagrams, sequence diagrams, and explanatory docs added to board
```

### Pattern 2: PRD → Code (Code Generation)

**Goal:** Generate implementation guidance from product requirements on a board.

**Steps:**
1. Create/share PRD document on Miro board
2. Use `code_create_from_board` prompt
3. Agent uses `context_explore` to find key documents
4. Agent uses `context_get` to read PRD details
5. Agent analyzes requirements and recommends doc types
6. Agent generates implementation docs, code structure, guidance
7. Agent uses `doc_create` to add generated docs to board

**When to use:**
- Starting a new feature implementation
- Generating specification documents
- Creating implementation roadmaps

**Example:**
```
Agent: "This board has our PRD. Generate implementation docs and code guidance."
Result: Detailed implementation guide, code structure recommendations, and task breakdown
```

### Pattern 3: Board Search + Create (Discovery & Creation)

**Goal:** Find relevant content, then create new artifacts based on findings.

**Steps:**
1. Use `context_explore` to discover board structure
2. Use `board_list_items` to list specific item types
3. Use `context_get` selectively to read key items
4. Analyze findings and determine needed artifacts
5. Use `diagram_create`, `doc_create`, or `table_create` to add results

**When to use:**
- Summarizing existing board work
- Creating derivative documents
- Analyzing and responding to board content

**Example:**
```
Agent: "Summarize this prototype and suggest improvements"
Steps: Explore board → find prototype screens → read UI structure → suggest improvements → create feedback doc
```

### Pattern 4: Iterative Design Feedback

**Goal:** Continuous improvement loop with agent feedback.

**Steps:**
1. Board contains design/requirements/code
2. Agent reads board content using `context_get`
3. Agent analyzes and suggests improvements
4. Agent creates feedback document with `doc_create`
5. Team reviews feedback on board
6. Team updates board content
7. Repeat for refinement

**When to use:**
- Design review cycles
- Requirements refinement
- Code review and optimization

**Example:**
```
Iteration 1: Agent analyzes design → suggests UX improvements
Iteration 2: Team updates design → Agent suggests data model improvements
Iteration 3: Team updates data model → Agent suggests code architecture
```

## Common Gotchas

### Gotcha 1: Team Mismatch

**Problem:**
```
Agent: "Summarize this board: https://miro.com/app/board/team-b-board/"
Result: ❌ 403 Forbidden - Access Denied
```

**Cause:** You authenticated MCP against Team A, but are trying to access a Team B board.

**Solution:**
- Check which team the board belongs to
- Re-authenticate and select the correct team
- MCP can be re-authenticated multiple times to switch teams

**Prevention:**
- Verify board team before referencing it
- Document which team contains which boards
- When switching teams, explicitly note the re-authentication

### Gotcha 2: OAuth Token Expiry

**Problem:**
```
Agent: "Update the task list on this board"
Result: ❌ 401 Unauthorized - Token Expired
```

**Cause:** OAuth access token has expired (typically after 1 hour).

**Solution:**
- Client will automatically use refresh token to get new access token
- If refresh token expired, re-authenticate via OAuth flow
- Most clients handle this automatically; manual re-auth is rare

**Prevention:**
- Ensure your client is configured to auto-refresh tokens
- Periodically re-authenticate for long-running sessions

### Gotcha 3: Remote Server Support

**Problem:**
```
Error: "MCP client doesn't support remote connections"
```

**Cause:** Your client has MCP support but only for local stdio-based servers, not remote HTTP servers.

**Solution:**
- Check client documentation for remote MCP support
- Contact client developers to request remote MCP support
- Some clients (like Cursor, Replit) support remote; others don't (yet)

**Prevention:**
- Verify client supports remote MCP before setup
- Test OAuth flow early to catch this

### Gotcha 4: Tool Availability / Implicit Tool Usage

**Problem (VSCode/Copilot specific):**
```
Agent: "Create a diagram from this board"
Result: ❌ Copilot uses search tool instead of diagram_create
```

**Cause:** Copilot doesn't automatically use Miro tools; you must explicitly reference them.

**Solution:**
```
Explicit: "Use the diagram_create tool to create a UML diagram..."
Result: ✅ Copilot uses the correct tool
```

**Prevention:**
- For VSCode/Copilot: Always explicitly name the tool you want
- Other clients (Cursor, Claude Code) usually auto-detect better

### Gotcha 5: Rate Limiting

**Problem:**
```
Agent: "Read all 100 items from this board and analyze each"
Result: ❌ 429 Too Many Requests after ~10 items
```

**Cause:** Rapid, parallel `context_get` calls exceeded rate limits. `context_get` is the most expensive operation.

**Solution:**
- Batch `context_get` calls sequentially, not in parallel
- Use `board_list_items` to discover items first (no limit)
- Cache frequently accessed data locally
- For bulk updates, use `table_sync_rows` instead of individual updates

**Prevention:**
- Understand that `context_get` is expensive (uses AI credits)
- When analyzing many items, process sequentially
- Implement rate limit retry logic (exponential backoff)

## Optimization Strategies

### 1. Minimize `context_get` Calls

`context_get` is the only tool using Miro AI credits and has stricter rate limits.

**Bad:**
```
for each item in board:
  context_get(item)  # ❌ Rapid parallel calls → rate limited
```

**Good:**
```
board_list_items(board)  # ✅ Fast, no credits
for key_item in [important_items]:
  context_get(key_item)  # ✅ Selective, sequential
```

### 2. Batch Operations

Use `table_sync_rows` for bulk updates instead of individual row updates.

**Bad:**
```
for each row in rows_to_update:
  table_update(row)  # ❌ Many API calls
```

**Good:**
```
table_sync_rows(rows_to_update)  # ✅ Single call, upsert semantics
```

### 3. Pagination

Use cursor-based pagination to handle large boards efficiently.

**Bad:**
```
all_items = board_list_items(board, limit=999999)  # ❌ Timeout/error
```

**Good:**
```
cursor = None
while True:
  items, cursor = board_list_items(board, limit=100, cursor=cursor)
  process(items)
  if not cursor: break  # ✅ Handle large boards gracefully
```

### 4. Local Caching

Cache frequently accessed board content locally to avoid repeated API calls.

**Example:**
```python
cache = {}
def get_document(board_id, doc_id):
  key = f"{board_id}:{doc_id}"
  if key not in cache:
    cache[key] = context_get(board_id, doc_id)
  return cache[key]
```

### 5. Error Handling & Retry Logic

Implement exponential backoff for rate-limited requests.

**Example:**
```python
import time
def call_with_backoff(func, *args, max_retries=3, initial_wait=1):
  for attempt in range(max_retries):
    try:
      return func(*args)
    except RateLimitError:
      wait = initial_wait * (2 ** attempt)
      time.sleep(wait)
  raise Exception("Max retries exceeded")
```

## Enterprise Considerations

### Admin Enablement

If your organization is on **Miro Enterprise Plan:**
1. Admin must enable Miro MCP Server in your organization
2. Optionally restrict to specific teams
3. Once enabled, team members can authenticate normally

### Audit & Compliance

- MCP actions are logged at the team level
- User actions are traceable (which user performed which action)
- Suitable for enterprise compliance and audit requirements

### Team Isolation

- MCP is team-scoped (cannot access multiple teams simultaneously)
- If you need access to multiple teams, re-authenticate for each team
- Useful for separating client work, projects, or organizational units

## Security Best Practices

### Token Management

- **Never store access tokens** in code or version control
- **Let your client handle token refresh** — don't manage tokens manually
- **Re-authenticate periodically** if using for long sessions
- **Use PKCE** (Proof Key for Public Clients) when available

### Scope Minimization

- Request only necessary permissions (e.g., `boards:read` if read-only)
- Don't request `boards:write` if you only need to read
- Limits potential impact if credentials are compromised

### Workspace Permissions

- MCP respects existing Miro workspace permissions
- If you don't have access to a board in Miro, MCP won't either
- Use Miro's permission model as your access control

## Real-World Tips

### Tip 1: Start with context_explore

Always start with `context_explore` to understand board structure before diving into details.

```
Safe: context_explore → board_list_items → context_get (selective)
Risky: context_explore → context_get (all items) ← rate limit risk
```

### Tip 2: Use Descriptive Titles

When creating diagrams or documents, use clear titles for easy reference.

```
✅ "Architecture Diagram - User Service"
❌ "Diagram 1"
```

### Tip 3: Version Your Documents

For important documents, include version info or timestamps.

```
Agent creates: "Implementation Guide v1.0 (generated 2026-02-15)"
Later update: "Implementation Guide v1.1 (generated 2026-02-16)"
```

### Tip 4: Document Assumptions

When generating code guidance or documentation, note assumptions.

```
"Generated implementation guide assumes:
- Node.js 18+
- PostgreSQL 14+
- React 18+
See ASSUMPTIONS section below."
```

### Tip 5: Iterative Feedback Loops

Use agent feedback loops for continuous refinement.

```
Agent analyzes → suggests improvements → creates feedback doc
Team reviews feedback → updates board
Agent re-analyzes → suggests next improvements
```

## Performance Considerations

### Board Size

- Small boards (<100 items): No special handling needed
- Medium boards (100-1000 items): Use pagination, avoid parallel `context_get`
- Large boards (1000+ items): Implement filtering, caching, and batching

### API Response Times

- `board_list_items`: Fast (no processing)
- `context_explore`: Fast (high-level)
- `context_get`: Slow (uses AI credits)
- `diagram_create`: Medium (diagram generation)

### Cost Optimization

- **Free operations:** `board_list_items`, `context_explore`, diagram/doc/table creation
- **Paid operations:** `context_get` only (uses Miro AI credits)
- **Strategy:** Minimize `context_get` calls, use discovery tools first

## Next Steps

- **Tools reference:** See [references/mcp-prompts.md](mcp-prompts.md) for complete tool documentation
- **API details:** See [references/rest-api-essentials.md](rest-api-essentials.md) for low-level API reference
- **Client setup:** See [references/ai-coding-tools.md](ai-coding-tools.md) for your specific MCP client
