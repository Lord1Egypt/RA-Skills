# Pieces Long-Term Memory MCP Skill.md


```markdown
---
name: pieces-mcp
description: >
  Connect OpenClaw to Pieces via MCP-only (no SSE) and use Pieces as external
  long-term memory. Use this when the human runs PiecesOS with LTM enabled on
  another machine and exposes the MCP server via a tunnel (ngrok, custom domain,
  or any HTTPS proxy). This skill tells the agent exactly how to prompt the
  human, configure MCPorter and mcp-remote, use Pieces tools (ask_pieces_ltm,
  create_pieces_memory, *_full_text_search), and troubleshoot common failures.
---

# Pieces MCP Skill for OpenClaw (MCP-Only, No SSE)

This skill teaches you, the OpenClaw agent, how to:

1. Know **when** to use Pieces.
2. Guide the human through tunnel setup (ngrok or custom).
3. Wire OpenClaw to the Pieces MCP server using **only `/mcp`**.
4. Use Pieces tools (`ask_pieces_ltm`, `create_pieces_memory`,
   `*_full_text_search`) in your reasoning.
5. Troubleshoot when something goes wrong.

---

## 0. When to Use This Skill

Trigger this skill when:

- The human mentions **Pieces**, **PiecesOS**, **MCP**, "ask Pieces", or "long-term memory"
  in the context of OpenClaw.
- They say things like:
  - "I want OpenClaw to remember what I worked on."
  - "Hook OpenClaw up to my Pieces long-term memory."
- You see or expect a URL like:
  - `https://...ngrok-free.dev`
  - `https://username.tunnel.company.stream`
  - Any HTTPS URL they say is "the Pieces MCP tunnel".

If none of that is true, you probably don't need this skill.

---

## 1. Mental Model

Think of three components:

- **PiecesOS MCP server (remote machine)**  
  - Runs on the human's other machine.
  - Long-Term Memory (LTM) is enabled.
  - Exposed via an HTTPS tunnel:
    `/model_context_protocol/2025-03-26/mcp`.

- **OpenClaw host (this machine)**  
  - This is where you (the agent) live.
  - Uses **MCPorter** to integrate MCP servers.

- **Bridge: MCPorter + `mcp-remote`**  
  - `mcporter.json` tells MCPorter about MCP servers.
  - `mcp-remote` connects to the remote `/mcp` endpoint and exposes it to
    OpenClaw.

> **Important:** This integration is MCP-only. Do **not** use `/sse`.  
> Always use `/mcp` for both direct calls and the bridge.

---

## 2. Human Checklist (What You Must Confirm)

You must guide/confirm these three things:

1. **PiecesOS + LTM is running** on the remote machine.  
   Say something like:
   > "Make sure PiecesOS is installed and running on your other machine, and that
   > Long-Term Memory (LTM) is enabled in the Pieces Desktop App."

2. **A tunnel is available** to expose the MCP server.  
   Options include:
   - **ngrok** (most common): `ngrok http 39300`
   - **Custom tunnel** (e.g., `username.tunnel.company.stream`)
   - Any HTTPS proxy that forwards to `localhost:39300`

3. **For ngrok specifically, tell them:**

   > "On the machine running PiecesOS, please run this in a terminal:
   >
   > ```bash
   > ngrok http 39300
   > ```
   >
   > If ngrok asks for login or an authtoken, follow its instructions once.
   > When it's running, you'll see a forwarding URL like:
   >
   > `https://SOMETHING.ngrok-free.dev -> http://localhost:39300`
   >
   > Please paste that HTTPS URL here."

You cannot proceed until the human pastes a valid HTTPS tunnel URL.

---

## 3. Build and Verify the MCP URL

Once you have the base tunnel URL, construct the MCP endpoint.

If the human gave you:

```text
https://SOMETHING.ngrok-free.dev
```

Or a custom tunnel like:

```text
https://name.tunnel.company.stream
```

Define:

```
MCP_URL_BASE = <the tunnel URL>
MCP_URL_MCP  = <the tunnel URL>/model_context_protocol/2025-03-26/mcp
```

### 3.1 Quick Sanity Check (Before Initialize)

**Always run this GET request first** to confirm the route is alive:

```bash
curl -i "MCP_URL_MCP"
```

**Expected success response (HTTP 400):**

```json
{
  "jsonrpc": "2.0",
  "error": {
    "code": -32000,
    "message": "Bad Request: mcp-session-id header or sessionId query parameter is required"
  },
  "id": null
}
```

This 400 error is **good** — it means:
- ✅ The route exists
- ✅ The MCP server is running
- ✅ It's ready to accept properly-formed requests

**If you get 404, 502, HTML, or timeout** → See Section 9.1: Troubleshooting.

### 3.2 Understanding MCP Request Patterns (Critical!)

Before configuring MCPorter, you need to understand how MCP requests work. This section shows the exact request patterns so you don't get confused.

#### The Session Management Pattern

All MCP interactions follow this flow:

1. **Initialize** → Server assigns you a session-id
2. **Use that session-id** for all subsequent requests
3. **Never reuse your custom session-id** — always use the server-assigned one

#### Session ID Format

> **What to look for:** The server-assigned session-id is typically a **Unix 
> timestamp in milliseconds** — a 13-digit numeric string like `1774202062499`.
> 
> Pattern: `17XXXXXXXXXXX` (13 digits starting with `17` in 2025-2026)
>
> You'll find it in the **response headers**, not the response body:
> ```
> mcp-session-id: 1774202062499
> ```

#### Required Headers for ALL Requests

```
Content-Type: application/json
Accept: application/json, text/event-stream
mcp-session-id: <SESSION_ID>
```

**Missing either `Content-Type` or `Accept` will cause failures!**

#### Critical: Use File-Based JSON for curl

> **⚠️ Shell quoting can mangle JSON!** Zsh and Bash handle quotes differently,
> and inline JSON with `-d '{...}'` is fragile. **Always use file-based JSON
> with `--data-binary @filename`** to avoid parsing errors.

#### Critical: Use String JSON-RPC IDs

> **⚠️ Use `"id": "1"` (string), not `"id": 1` (integer).**  
> The server is sensitive to id types, and string ids work consistently.

---

#### Step 1: Initialize Session

Create a file `init.json`:

```json
{
  "jsonrpc": "2.0",
  "method": "initialize",
  "params": {
    "protocolVersion": "0.1.0",
    "capabilities": {},
    "clientInfo": {
      "name": "openclaw-agent",
      "version": "1.0"
    }
  },
  "id": "1"
}
```

Run:

```bash
curl -i -X POST "MCP_URL_MCP" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: init-request-001" \
  --data-binary @init.json
```

**What happens:**

- You send `mcp-session-id: init-request-001` (can be any string you choose)
- Server responds with a **new session-id in the response header**

**Look for this in the response headers:**

```
HTTP/2 200
content-type: application/json
mcp-session-id: 1774202062499
...
```

> **Critical:** Extract the `mcp-session-id` value from the **response header** 
> (e.g., `1774202062499`). This is your server-assigned session ID. Use this 
> exact value for all subsequent requests — do NOT continue using your initial 
> `init-request-001`.

**Response body (200 OK):**

```json
{
  "jsonrpc": "2.0",
  "id": "1",
  "result": {
    "protocolVersion": "0.1.0",
    "capabilities": {
      "tools": {}
    },
    "serverInfo": {
      "name": "pieces",
      "version": "1.0.0"
    }
  }
}
```

---

#### Step 2: Query Long-Term Memory

Now use the **server-assigned session-id** for all future requests.

Create a file `query.json`:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "ask_pieces_ltm",
    "arguments": {
      "question": "What did I work on today?",
      "chat_llm": "gpt-4"
    }
  },
  "id": "2"
}
```

Run (replacing `<SERVER_SESSION_ID>` with the value from Step 1):

```bash
curl -i -X POST "MCP_URL_MCP" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: <SERVER_SESSION_ID>" \
  --data-binary @query.json
```

**Example with actual session ID:**

```bash
curl -i -X POST "MCP_URL_MCP" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: 1774202062499" \
  --data-binary @query.json
```

**Response (200 OK):**

```json
{
  "jsonrpc": "2.0",
  "id": "2",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "{\"summaries\":[...],\"events\":[...]}"
      }
    ]
  }
}
```

**Important for OpenClaw Agents:**

The response looks like "raw JSON garbage" to humans, but this is **perfect for you!**

You get:
- `summaries[]` — Pre-existing memory summaries with relevance scores
- `events[]` — Raw activity events (browser, clipboard, audio, etc.)

Parse this JSON yourself and synthesize a natural language answer for the human.

---

#### Step 3: Create a Memory

Create a file `create_memory.json`:

```json
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "params": {
    "name": "create_pieces_memory",
    "arguments": {
      "summary_description": "OpenClaw + Pieces: First Integration Session",
      "summary": "# OpenClaw + Pieces Integration\n\nThis memory documents our initial setup session.\n\n## What We Did\n- Verified Pieces MCP server via tunnel\n- Configured MCPorter with mcp-remote\n- Successfully tested ask_pieces_ltm\n\n## Key Learnings\n- Session management is critical\n- Use file-based JSON to avoid shell quoting issues\n- Use string JSON-RPC ids for consistency",
      "project": "OpenClaw + Pieces"
    }
  },
  "id": "3"
}
```

Run (using the same server-assigned session ID):

```bash
curl -i -X POST "MCP_URL_MCP" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -H "mcp-session-id: <SERVER_SESSION_ID>" \
  --data-binary @create_memory.json
```

**Response (200 OK):**

```json
{
  "jsonrpc": "2.0",
  "id": "3",
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Memory created successfully"
      }
    ]
  }
}
```

---

#### Session ID Quick Reference

| Stage | Header Value | Source |
|-------|--------------|--------|
| **Initialize request** | Any string you choose (e.g., `init-001`, `my-session`, `test-123`) | You create it |
| **Initialize response** | 13-digit timestamp (e.g., `1774202062499`) | **Extract from response header** |
| **All subsequent requests** | The server-assigned value from initialize | Reuse the extracted value |

#### Common Mistakes That Will Break Things

| ❌ Wrong | ✅ Correct |
|----------|-----------|
| Inline JSON with `-d '{...}'` | File-based JSON with `--data-binary @file.json` |
| Integer id: `"id": 1` | String id: `"id": "1"` |
| Missing `Accept` header | Include `Accept: application/json, text/event-stream` |
| Using your initial session-id (`init-001`) for all requests | Extract server-assigned session-id from initialize **response header** |
| Looking for session-id in response body | Session-id is in the **response headers** |
| Thinking raw JSON responses are errors | Parse the JSON — it's structured data for you to synthesize! |
| Calling tools before initialize | Always call initialize first to get a session-id |
| Forgetting `chat_llm` parameter | Include it (even though responses may still be raw JSON) |

---

## 4. Configure MCPorter (MCP-Only)

OpenClaw uses MCPorter to manage MCP servers. The config lives at:

```
~/.openclaw/workspace/config/mcporter.json
```

As the agent, you should:

### 4.1 Ensure the config directory exists

```bash
mkdir -p ~/.openclaw/workspace/config
```

### 4.2 Create or update mcporter.json

You want a `pieces` entry that uses `mcp-remote` pointed at `MCP_URL_MCP`:

```json
{
  "mcpServers": {
    "pieces": {
      "command": "mcp-remote",
      "args": [
        "MCP_URL_MCP_GOES_HERE"
      ]
    }
  }
}
```

**Example with ngrok:**

```json
{
  "mcpServers": {
    "pieces": {
      "command": "mcp-remote",
      "args": [
        "https://SOMETHING.ngrok-free.dev/model_context_protocol/2025-03-26/mcp"
      ]
    }
  }
}
```

**Example with custom tunnel:**

```json
{
  "mcpServers": {
    "pieces": {
      "command": "mcp-remote",
      "args": [
        "https://username.tunnel.company.stream/model_context_protocol/2025-03-26/mcp"
      ]
    }
  }
}
```

No `/sse` here. This is the MCP-only configuration.

> **Note:** `mcp-remote` handles the session management (initialize, session-id 
> extraction, header management) automatically. You don't need to manually manage 
> sessions when using MCPorter — the examples in Section 3.2 are for understanding 
> the protocol and direct testing/troubleshooting.

### 4.3 Ensure mcp-remote is installed

Install `mcp-remote` globally:

```bash
npm install -g mcp-remote@0.1.38
```

You can run this yourself from the OpenClaw host's shell.

---

## 5. Restart the OpenClaw Gateway

After editing `mcporter.json`, restart the OpenClaw gateway so it picks up the
Pieces MCP server:

```bash
cd ~/.openclaw/workspace
openclaw gateway restart
```

Wait a few seconds for it to restart.

At this point, OpenClaw should see the Pieces MCP server through MCPorter and
`mcp-remote` → `MCP_URL_MCP`.

---

## 6. How and When to Use Pieces

Once connected, treat Pieces as your authoritative long-term memory.

### 6.1 When to query Pieces

Call Pieces (via `ask_pieces_ltm` / search tools) whenever:

**The human asks about something in the past** that you're unlikely to know from
this session alone:

- "What did I work on today?"
- "What did I work on yesterday / last week?"
- "What have I been doing on [project] recently?"
- "Who is [person]?"

**You need context for:**

- **Meetings:**
  - "What is my next meeting?"
  - "What did we discuss in last week's standup?"
- **Debugging / research:**
  - "What did I try last time I debugged this issue?"
  - "What fixes have I used before for this type of error?"

### 6.2 Prefer ask_pieces_ltm

Use `ask_pieces_ltm` as your first tool for historical questions:

**Send a natural-language question, e.g.:**

- "What did the user work on today?"
- "Summarize the main projects the user has been working on this month."
- "Who is the user and what is their role?"

**Understand the response format:**

- You'll get raw JSON with `summaries[]` and `events[]` arrays
- Each entry has a `combined_string` field with the content
- Parse this data and synthesize a natural language answer

**When you answer, say something like:**

> "According to your Pieces long-term memory, …"

If `ask_pieces_ltm` times out or is too vague, narrow the query by time and/or
topic (see troubleshooting).

### 6.3 Use create_pieces_memory for durable summaries

Use `create_pieces_memory` when you want to write an important memory:

**Typical use cases:**

- **Human profile:** name, role, responsibilities, preferences, current focus.
- **Decision summaries:** what was decided, why, who was involved.
- **Debugging recaps:** symptoms, steps taken, final fix.
- **Project milestones:** what changed, what shipped.

**Conceptual signature:**

```
create_pieces_memory(
  summary_description: string,
  summary: string,
  project?: string,
  files?: string[],
  externalLinks?: string[],
  connected_client?: string
);
```

**Guidelines:**

- **`summary_description`** — short human-readable label.
  - Examples:
    - `"Profile: <name> – Role at <company>"`
    - `"OpenClaw + Pieces: Initial Setup"`

- **`summary`** — full markdown body:
  - Start with a `#` heading:
    - `# Profile: <name> – Role at <company>`
  - Add a few clear sections:
    - `## Role`
    - `## Responsibilities`
    - `## Current Focus`
    - `## Notes / Preferences`

- **`project`** — (optional) grouping label:
  - `"OpenClaw + Pieces"`, `"Website"`, `"Standup Automation"`, etc.

- **`files` / `externalLinks` / `connected_client`** — optional context and attribution.

This makes memories both human-readable and easy for future agents to retrieve
and interpret.

---

## 7. Direct Testing vs. MCPorter Usage

- **For debugging:** Use the file-based curl examples from Section 3.2 to test
  the MCP server directly.

- **For production:** Once MCPorter is configured, you don't manually manage
  sessions — `mcp-remote` does it for you. Just call the tools through OpenClaw's
  MCP integration normally.

---

## 8. Tunnel Options

This skill works with any HTTPS tunnel that forwards to `localhost:39300` on the
PiecesOS machine:

| Tunnel Type | Example URL | Notes |
|-------------|-------------|-------|
| **ngrok** | `https://abc123.ngrok-free.dev` | Most common; may require auth setup |
| **Custom Pieces tunnel** | `https://username.tunnel.company.stream` | Pre-configured by Pieces team |
| **Any HTTPS proxy** | `https://your-domain.com` | As long as it forwards to 39300 |

The MCP endpoint is always at:
```
<tunnel_url>/model_context_protocol/2025-03-26/mcp
```

---

## 9. Troubleshooting

### 9.1 MCP URL check fails (404/502/timeout)

**Symptom:**

`curl MCP_URL_MCP` returns 404/502/HTML or times out.

**What to do:**

Ask the human to:

1. Confirm PiecesOS is running on the remote machine.
2. Confirm the tunnel is still running (ngrok or custom).
3. Paste a fresh tunnel URL if ngrok was restarted.

Rebuild `MCP_URL_MCP` and test again with the quick sanity check.

### 9.2 Initialize returns HTTP 500 (Internal Server Error)

**Symptom:**

```bash
curl -i -X POST "MCP_URL_MCP" ... -d '{"jsonrpc": "2.0", ...}'
# Returns: HTTP/1.1 500 Internal Server Error
```

**Checklist:**

1. **Confirm route is alive first:**
   ```bash
   curl -i "MCP_URL_MCP"
   ```
   → Should return **400** with "mcp-session-id required" message
   → If you get 404/502, the tunnel is down (see 9.1)

2. **Use file-based JSON (avoid shell quoting issues):**
   ```bash
   # Create init.json with your JSON payload
   curl -i -X POST "MCP_URL_MCP" \
     -H "Content-Type: application/json" \
     -H "Accept: application/json, text/event-stream" \
     -H "mcp-session-id: init-request-001" \
     --data-binary @init.json
   ```

3. **Use string JSON-RPC ids:**
   ```json
   {"id": "1"}  ✅ Correct
   {"id": 1}    ❌ May cause issues
   ```

4. **Ensure BOTH headers are present:**
   - `Content-Type: application/json`
   - `Accept: application/json, text/event-stream`

5. **If still 500:** Ask the human to restart PiecesOS and/or the tunnel, then
   re-test.

### 9.3 Tools seem missing or unresponsive

**Symptoms:**

- `ask_pieces_ltm` never seems to be called.
- Pieces tools don't show up in behavior.
- Calls time out immediately.

**What to check:**

1. **`mcporter.json`:**
   - Exists at `~/.openclaw/workspace/config/mcporter.json`.
   - Has a `pieces` server using `mcp-remote` pointed at a valid `/mcp` URL.

2. **`mcp-remote`:**
   - Is installed globally:
     ```bash
     mcp-remote --help
     ```
   - If missing, install:
     ```bash
     npm install -g mcp-remote@0.1.38
     ```

3. **Gateway:**
   - Was restarted after editing `mcporter.json`:
     ```bash
     openclaw gateway restart
     ```

4. **Test the MCP server directly** using the file-based curl examples from
   Section 3.2:
   - If direct curl works but MCPorter doesn't → issue is with the bridge
   - If direct curl fails → issue is with PiecesOS or the tunnel

### 9.4 ask_pieces_ltm timeouts / vague answers

**Symptoms:**

- Pieces returns "failed to extract context" or times out.
- Answers are too generic.

**What to try:**

1. **Narrow the question:**
   - Add time:
     - "What did I work on this morning?"
     - "What did I work on this week related to [project]?"
   - Add topic:
     - "What have I done recently around MCP and ngrok?"
     - "What have I been doing on the website?"

2. **If repeated timeouts continue:**
   - Test with file-based curl directly (Section 3.2) to isolate whether it's
     an MCPorter issue
   - Confirm the MCP server is healthy with `curl -i MCP_URL_MCP`
   - Confirm the tunnel is still running (human-side)

### 9.5 Getting raw JSON instead of natural language

**This is NOT a problem!**

- Raw JSON responses are **expected and correct** for OpenClaw agents
- The `summaries[]` and `events[]` arrays contain structured data for you to parse
- **You should synthesize the natural language answer yourself**

If you're getting raw JSON, it means:

- ✅ The MCP server is working correctly
- ✅ Memory retrieval is working correctly
- ✅ You have structured data to work with

Simply parse the JSON and create a helpful answer for the human!

---

## 10. Summary of the Flow

1. **Detect the need** for Pieces (user mentions Pieces/MCP/long-term memory).

2. **Guide the human:**
   - Confirm PiecesOS + LTM is running.
   - Set up tunnel (ngrok or custom).
   - Paste the HTTPS tunnel URL.

3. **Build and verify** `MCP_URL_MCP`:
   - Quick sanity check: `curl -i MCP_URL_MCP` → expect 400

4. **(Optional) Test directly** using file-based curl examples from Section 3.2:
   - Use string ids (`"id": "1"`)
   - Use `--data-binary @file.json`
   - Extract server-assigned session-id from **response headers** (13-digit timestamp)

5. **Configure MCPorter** (`mcporter.json` with `mcp-remote` → `/mcp`).

6. **Ensure `mcp-remote` is installed.**

7. **Restart the OpenClaw gateway.**

8. **Use `ask_pieces_ltm`** for reading history (parse raw JSON responses).

9. **Use `create_pieces_memory`** for writing durable summaries.

10. **Apply troubleshooting steps** if anything fails.

If you follow this skill, you should be able to reliably connect to and use
Pieces as external long-term memory from a fresh OpenClaw instance with minimal
human effort.
```