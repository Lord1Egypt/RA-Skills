---
name: greenhelix-mcp-server-development
version: "1.3.1"
description: "MCP Server Development & Monetization Guide: Build, Publish, and Profit from the Tool Integration Standard. Complete guide to building, publishing, and monetizing MCP servers. Covers the MCP specification, server development patterns, registry publishing, enterprise governance, and business models for the tool integration standard powering 10,000+ servers."
license: MIT
compatibility: [openclaw]
author: felix-agent
type: guide
tags: [mcp, model-context-protocol, tool-integration, agent-infrastructure, monetization, greenhelix, openclaw, ai-agent, guide]
price_usd: 49.0
content_type: markdown
executable: false
install: none
credentials: [STRIPE_API_KEY]
metadata:
  openclaw:
    requires:
      env:
        - STRIPE_API_KEY
    primaryEnv: STRIPE_API_KEY
---
# MCP Server Development & Monetization Guide: Build, Publish, and Profit from the Tool Integration Standard

> **Notice**: This is an educational guide with illustrative code examples.
> It does not execute code or install dependencies.
> All examples use the GreenHelix sandbox (https://sandbox.greenhelix.net) which
> provides 500 free credits — no API key required to get started.
>
> **Referenced credentials** (you supply these in your own environment):
> - `STRIPE_API_KEY`: Stripe API key for card payment processing (scoped to payment intents only)


The Model Context Protocol has become the standard interface between AI models and external tools. In under eighteen months, the ecosystem has grown from a single Anthropic specification to over 10,000 registered servers, adopted by every major AI platform -- Claude, GPT, Gemini, Copilot, and dozens of open-source frameworks. MCP servers are the new APIs. They are how AI agents read databases, call services, execute code, and interact with the physical world. If you can build an API, you can build an MCP server. If you can build an MCP server, you can monetize it. This guide covers both: the engineering of production-grade MCP servers and the business models that turn them into revenue. It starts with the protocol architecture, moves through implementation in Python and TypeScript, covers advanced patterns like authentication, streaming, and composition, then walks through registry publishing, enterprise governance, monetization strategies, and production operations. Every chapter includes working code. By the end, you will have the knowledge to build, publish, and profit from MCP servers.
1. [MCP Architecture Deep Dive](#chapter-1-mcp-architecture-deep-dive)
2. [Building Your First MCP Server](#chapter-2-building-your-first-mcp-server)

## What You'll Learn
- Chapter 1: MCP Architecture Deep Dive
- Chapter 2: Building Your First MCP Server
- Chapter 3: Advanced Server Patterns
- Chapter 4: Publishing to the MCP Registry
- Chapter 5: Enterprise MCP Governance
- Chapter 6: Monetization Strategies
- Chapter 7: Production Operations
- Chapter 8: Case Studies
- What's Next

## Full Guide

# MCP Server Development & Monetization Guide: Build, Publish, and Profit from the Tool Integration Standard

The Model Context Protocol has become the standard interface between AI models and external tools. In under eighteen months, the ecosystem has grown from a single Anthropic specification to over 10,000 registered servers, adopted by every major AI platform -- Claude, GPT, Gemini, Copilot, and dozens of open-source frameworks. MCP servers are the new APIs. They are how AI agents read databases, call services, execute code, and interact with the physical world. If you can build an API, you can build an MCP server. If you can build an MCP server, you can monetize it. This guide covers both: the engineering of production-grade MCP servers and the business models that turn them into revenue. It starts with the protocol architecture, moves through implementation in Python and TypeScript, covers advanced patterns like authentication, streaming, and composition, then walks through registry publishing, enterprise governance, monetization strategies, and production operations. Every chapter includes working code. By the end, you will have the knowledge to build, publish, and profit from MCP servers.

---

## Table of Contents

1. [MCP Architecture Deep Dive](#chapter-1-mcp-architecture-deep-dive)
2. [Building Your First MCP Server](#chapter-2-building-your-first-mcp-server)
3. [Advanced Server Patterns](#chapter-3-advanced-server-patterns)
4. [Publishing to the MCP Registry](#chapter-4-publishing-to-the-mcp-registry)
5. [Enterprise MCP Governance](#chapter-5-enterprise-mcp-governance)
6. [Monetization Strategies](#chapter-6-monetization-strategies)
7. [Production Operations](#chapter-7-production-operations)
8. [Case Studies](#chapter-8-case-studies)

---

## Chapter 1: MCP Architecture Deep Dive

### What MCP Actually Is

The Model Context Protocol is a client-server protocol that standardizes how AI models interact with external data sources and tools. Before MCP, every AI platform had its own way of defining tool interfaces. OpenAI used function calling with JSON Schema. Anthropic used tool use with a similar but incompatible schema. LangChain had its own tool abstraction. Every integration was bespoke. MCP replaces this fragmentation with a single protocol that any client can speak to any server.

The protocol has three roles:

- **Host**: The application that contains the AI model. Claude Desktop, VS Code with Copilot, a custom LangChain app -- these are hosts. The host manages the lifecycle of MCP connections and mediates between the model and the servers.
- **Client**: A protocol client that lives inside the host. Each client maintains a one-to-one connection with a single MCP server. The client handles capability negotiation, request routing, and response marshaling.
- **Server**: A lightweight program that exposes tools, resources, and prompts through the MCP protocol. This is what you build. A server might wrap a database, an API, a file system, a computation engine, or any other capability that an AI model needs to access.

The separation between host and client matters for security. The host controls which servers the model can access, what permissions each server has, and whether to require human approval for sensitive operations. The client is a protocol implementation detail -- you rarely interact with it directly.

### The Transport Layer

MCP is transport-agnostic. The protocol defines the message format and semantics; the transport defines how those messages move between client and server. Three transports are in common use as of April 2026.

**stdio (Standard Input/Output)**

The simplest transport. The host launches the server as a subprocess. Messages flow over stdin and stdout as newline-delimited JSON. stderr is reserved for logging. This is how most local MCP servers work -- Claude Desktop, for example, spawns each configured server as a child process and communicates over pipes.

```
Host Process
    |
    +-- spawns --> Server Process
    |                  |
    stdin  <---------> stdout  (JSON-RPC messages)
    stderr ----------> (logging)
```

Advantages: Zero network configuration. No ports to open. No TLS to configure. The operating system handles the IPC. Process isolation is automatic -- if the server crashes, the host detects the broken pipe and can restart it.

Disadvantages: Only works for local servers. Cannot be shared across machines. Cannot be load-balanced. Each host-server pair requires a separate process.

When to use: Local development. Personal tools. Servers that access local files or databases. Servers where latency must be minimal (no network hop).

**HTTP with Server-Sent Events (SSE)**

The original remote transport in the MCP specification. The client connects to the server over HTTP. The server uses Server-Sent Events (SSE) to push notifications and responses back to the client. This transport enables remote servers, shared servers, and server-to-client notifications.

The connection flow:

1. Client sends HTTP GET to the server's SSE endpoint (typically `/sse`).
2. Server responds with `Content-Type: text/event-stream` and keeps the connection open.
3. Server sends an `endpoint` event containing a URL for the client to POST requests to.
4. Client sends JSON-RPC requests via HTTP POST to that endpoint.
5. Server sends JSON-RPC responses and notifications via the SSE stream.

```python
# Simplified SSE transport flow
# Server side
@app.get("/sse")
async def sse_endpoint():
    async def event_stream():
        yield f"event: endpoint\ndata: /messages/{session_id}\n\n"
        while True:
            message = await outgoing_queue.get()
            yield f"event: message\ndata: {json.dumps(message)}\n\n"
    return StreamingResponse(event_stream(), media_type="text/event-stream")

@app.post("/messages/{session_id}")
async def handle_message(session_id: str, request: Request):
    body = await request.json()
    # Process JSON-RPC request, put response on outgoing_queue
```

Advantages: Works over the network. Supports server-to-client push. Compatible with existing HTTP infrastructure (load balancers, proxies, CDNs).

Disadvantages: SSE is unidirectional (server-to-client only), so the client must use a separate HTTP POST channel for requests. This creates two connections per session. Some proxies and firewalls struggle with long-lived SSE connections. Connection resumption after network interruption requires custom logic.

When to use: Remote servers behind a web server. Servers that need to push updates. Production deployments where you already have HTTP infrastructure.

**Streamable HTTP**

The newest transport, introduced in the MCP specification revision of March 2026. Streamable HTTP simplifies the SSE transport by using a single HTTP endpoint for both requests and responses. The client sends a POST request. The server can respond with either a regular JSON response (for simple request-response patterns) or upgrade to SSE for streaming responses and follow-up notifications.

```
Client                              Server
  |                                    |
  |  POST /mcp                         |
  |  {"jsonrpc":"2.0","method":"..."}  |
  |----------------------------------->|
  |                                    |
  |  200 OK                            |
  |  Content-Type: text/event-stream   |
  |  (or application/json for simple)  |
  |<-----------------------------------|
```

Advantages: Single endpoint. Backward-compatible with simple HTTP clients. Supports streaming when needed. Easier to deploy behind reverse proxies. No persistent connection required for basic operations.

Disadvantages: Newer, so not all clients support it yet. Streaming mode still has the SSE proxy compatibility issues.

When to use: New remote deployments. Servers that need to work with both streaming-capable and simple HTTP clients.

### The Message Format: JSON-RPC 2.0

Every MCP message is a JSON-RPC 2.0 message. This is not a custom format -- it is the same JSON-RPC used by Ethereum, Language Server Protocol, and dozens of other systems. The format has three message types.

**Request**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "query_database",
    "arguments": {
      "sql": "SELECT count(*) FROM users"
    }
  }
}
```

The `id` field correlates requests with responses. The `method` field identifies the operation. The `params` field carries the operation-specific data.

**Response**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "content": [
      {
        "type": "text",
        "text": "Query returned 42,531 rows."
      }
    ]
  }
}
```

**Error Response**

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "error": {
    "code": -32602,
    "message": "Invalid params",
    "data": "Column 'nonexistent' does not exist in table 'users'"
  }
}
```

Standard JSON-RPC error codes apply: -32700 (parse error), -32600 (invalid request), -32601 (method not found), -32602 (invalid params), -32603 (internal error). MCP adds no custom error codes -- use the standard codes plus descriptive messages and data fields.

**Notification**

```json
{
  "jsonrpc": "2.0",
  "method": "notifications/tools/list_changed"
}
```

Notifications have no `id` field and expect no response. They are fire-and-forget messages used for events like "the tool list has changed" or "a resource has been updated."

### Capabilities Negotiation

When a client connects to a server, the first message exchange is capabilities negotiation via the `initialize` method. The client sends its capabilities; the server responds with its own.

```json
// Client -> Server
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "initialize",
  "params": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "roots": { "listChanged": true },
      "sampling": {}
    },
    "clientInfo": {
      "name": "claude-desktop",
      "version": "1.5.0"
    }
  }
}

// Server -> Client
{
  "jsonrpc": "2.0",
  "id": 1,
  "result": {
    "protocolVersion": "2025-03-26",
    "capabilities": {
      "tools": { "listChanged": true },
      "resources": { "subscribe": true, "listChanged": true },
      "prompts": { "listChanged": true },
      "logging": {}
    },
    "serverInfo": {
      "name": "database-server",
      "version": "2.1.0"
    }
  }
}
```

After the server responds, the client sends an `initialized` notification to confirm the handshake is complete. Only then can the client call tools, read resources, or use prompts.

Key fields in the server capabilities:

- `tools`: The server exposes callable tools. `listChanged` means the server will notify the client if the tool list changes at runtime.
- `resources`: The server exposes readable resources (files, database records, API responses). `subscribe` means the client can subscribe to resource change notifications.
- `prompts`: The server exposes prompt templates that the model can use.
- `logging`: The server supports structured logging that the client can consume.

Capabilities negotiation is important because it allows both sides to adapt. A server that exposes only tools does not need to handle resource subscriptions. A client that does not support sampling will never receive sampling requests from the server.

### The Three Primitives: Tools, Resources, and Prompts

MCP servers expose capabilities through three primitives. Understanding which primitive to use for which purpose is the most important design decision you will make.

**Tools**

Tools are functions that the AI model can call. They take structured input, perform an action, and return a result. Tools are the most common primitive and the one you will use most often.

A tool has:
- A name (string, unique within the server)
- A description (string, used by the model to decide when to call the tool)
- An input schema (JSON Schema, validated before execution)
- A handler function (your code that executes when the tool is called)

```python
@server.tool()
async def query_database(sql: str) -> str:
    """Execute a read-only SQL query against the analytics database.

    Use this tool when the user asks about data, metrics, counts,
    or any question that can be answered with a database query.
    Only SELECT statements are allowed.
    """
    if not sql.strip().upper().startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")
    result = await db.execute(sql)
    return format_result(result)
```

Tools are model-controlled -- the AI model decides when to call them based on the description and the current conversation context. The host may require human approval before executing a tool call (this is configurable per-server and per-tool).

When to use tools: Any operation that has side effects (creating records, sending emails, modifying state). Any computation that the model cannot do itself (database queries, API calls, mathematical operations). Any action where the model needs to act on behalf of the user.

**Resources**

Resources are data that the AI model can read. They are identified by URIs and return content in a structured format. Resources are like GET endpoints in a REST API -- they retrieve data without modifying anything.

A resource has:
- A URI (string, following the `scheme://path` pattern)
- A name (string, human-readable)
- A description (string, optional)
- A MIME type (string, optional)
- Content (text or binary, returned when the resource is read)

```python
@server.resource("config://app/settings")
async def get_app_settings() -> str:
    """Current application configuration settings."""
    settings = await load_settings()
    return json.dumps(settings, indent=2)
```

Resources can also be dynamic using URI templates:

```python
@server.resource("db://tables/{table_name}/schema")
async def get_table_schema(table_name: str) -> str:
    """Schema definition for a database table."""
    schema = await db.get_schema(table_name)
    return json.dumps(schema, indent=2)
```

Resources are application-controlled -- the host application decides when to expose them to the model, often by attaching them to the conversation context. The model does not call resources directly; instead, the host includes resource content in the model's context window.

When to use resources: Configuration data. Reference documentation. Database schemas. File contents. Anything the model needs to read but should not modify.

**Prompts**

Prompts are reusable templates that the AI model or the user can invoke. They generate structured message sequences that set up the model's context for a specific task.

A prompt has:
- A name (string, unique within the server)
- A description (string, explains what the prompt does)
- Arguments (list of named parameters, some required, some optional)
- A handler that returns a list of messages

```python
@server.prompt()
async def analyze_table(table_name: str, question: str) -> list:
    """Analyze a database table to answer a specific question."""
    schema = await db.get_schema(table_name)
    sample = await db.execute(f"SELECT * FROM {table_name} LIMIT 5")
    return [
        {
            "role": "user",
            "content": f"Here is the schema for {table_name}:\n{schema}\n\n"
                       f"Sample data:\n{sample}\n\n"
                       f"Question: {question}"
        }
    ]
```

Prompts are user-controlled -- the user explicitly selects them (like choosing a slash command). They are useful for workflows that require a specific context setup.

When to use prompts: Complex workflows that need specific context. Onboarding sequences. Analysis templates where the model needs schema + sample data + instructions.

### Server Lifecycle

An MCP server goes through a defined lifecycle:

1. **Initialization**: Client sends `initialize` with its capabilities. Server responds with its capabilities and info. Client sends `initialized` notification.
2. **Operation**: Client and server exchange requests, responses, and notifications. The client can call tools, read resources, and invoke prompts. The server can send logging messages and change notifications.
3. **Shutdown**: Client sends a shutdown request or closes the transport. The server cleans up resources and exits.

For stdio servers, the lifecycle is tied to the process lifetime. When the host terminates the subprocess, the server is gone. For HTTP servers, sessions can persist across multiple HTTP connections, and the server process can serve multiple clients simultaneously.

The lifecycle matters for resource management. If your server opens database connections, file handles, or network sockets during initialization, it must close them during shutdown. The Python and TypeScript SDKs provide lifecycle hooks for this purpose.

```python
from contextlib import asynccontextmanager
from mcp.server import Server

@asynccontextmanager
async def server_lifespan(server: Server):
    # Startup: open connections
    db = await create_db_pool()
    server.state["db"] = db
    try:
        yield
    finally:
        # Shutdown: close connections
        await db.close()
```

---

## Chapter 2: Building Your First MCP Server

### Environment Setup

You need Python 3.10 or later for the Python SDK, or Node.js 18 or later for the TypeScript SDK. Both SDKs are actively maintained and track the latest protocol specification.

**Python**

```bash
pip install mcp
```

The `mcp` package includes the server framework, all three transports (stdio, SSE, streamable HTTP), and the client library for testing. It pulls in `pydantic` for schema validation and `httpx` for HTTP transport.

**TypeScript**

```bash
npm install @modelcontextprotocol/sdk
```

The TypeScript SDK includes the same server framework, transports, and client library.

### A Minimal Python MCP Server

Here is the simplest possible MCP server -- a single tool that adds two numbers:

```python
"""minimal_server.py -- A minimal MCP server with one tool."""

from mcp.server.fastmcp import FastMCP

server = FastMCP("calculator")

@server.tool()
async def add(a: float, b: float) -> str:
    """Add two numbers together.

    Use this tool when the user asks you to add, sum, or total
    two numeric values.
    """
    result = a + b
    return str(result)

if __name__ == "__main__":
    server.run(transport="stdio")
```

That is 15 lines of code. Let us break down what each part does.

`FastMCP("calculator")` creates a server instance with the name "calculator". This name appears in capabilities negotiation and helps the client identify the server.

`@server.tool()` registers the decorated function as a tool. The function name becomes the tool name. The docstring becomes the tool description. The function signature is automatically converted to a JSON Schema input schema -- `a: float, b: float` becomes:

```json
{
  "type": "object",
  "properties": {
    "a": { "type": "number" },
    "b": { "type": "number" }
  },
  "required": ["a", "b"]
}
```

The return type `str` means the tool returns text content. MCP tools always return content blocks -- text, images, or embedded resources. The SDK handles wrapping your string return value into the proper content block format.

`server.run(transport="stdio")` starts the server using the stdio transport. It reads JSON-RPC messages from stdin and writes responses to stdout.

### Running and Testing Locally

**With Claude Desktop**

Add the server to your Claude Desktop configuration file (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["/path/to/minimal_server.py"]
    }
  }
}
```

Restart Claude Desktop. The calculator tool will appear in the tools list. Ask Claude "What is 17.5 plus 23.8?" and it will call the `add` tool.

**With the MCP Inspector**

The MCP Inspector is a web-based debugging tool that connects to your server and lets you interact with it directly:

```bash
npx @modelcontextprotocol/inspector python minimal_server.py
```

This opens a browser interface where you can see the server's capabilities, call tools manually, browse resources, and view the raw JSON-RPC messages.

**With the Python Client Library**

For automated testing, use the MCP client library:

```python
"""test_minimal_server.py -- Test the calculator server."""

import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def test_add():
    server_params = StdioServerParameters(
        command="python",
        args=["minimal_server.py"],
    )
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # List tools
            tools = await session.list_tools()
            assert len(tools.tools) == 1
            assert tools.tools[0].name == "add"

            # Call the add tool
            result = await session.call_tool("add", {"a": 17.5, "b": 23.8})
            assert result.content[0].text == "41.3"

asyncio.run(test_add())
```

### A TypeScript MCP Server

The equivalent server in TypeScript:

```typescript
// minimal_server.ts -- A minimal MCP server with one tool.

import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "calculator",
  version: "1.0.0",
});

server.tool(
  "add",
  "Add two numbers together. Use this tool when the user asks you to add, sum, or total two numeric values.",
  {
    a: z.number().describe("First number"),
    b: z.number().describe("Second number"),
  },
  async ({ a, b }) => ({
    content: [{ type: "text", text: String(a + b) }],
  })
);

async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main();
```

The TypeScript SDK uses Zod for schema definition instead of Python type hints. The structure is the same: create a server, register tools, connect a transport.

### Defining Tools with Schemas

Real tools need more sophisticated input schemas. Here is a database query tool with proper validation:

```python
"""db_server.py -- MCP server for database access."""

from dataclasses import dataclass, field
from typing import Optional
from mcp.server.fastmcp import FastMCP

server = FastMCP("database")

# Allowed tables for security
ALLOWED_TABLES = {"users", "orders", "products", "analytics"}

# Maximum rows to return
MAX_ROWS = 1000

@server.tool()
async def query_database(
    sql: str,
    max_rows: int = 100,
    format: str = "table",
) -> str:
    """Execute a read-only SQL query against the analytics database.

    Use this tool to answer questions about users, orders, products,
    or analytics data. Only SELECT statements are allowed.
    Dangerous operations (DROP, DELETE, UPDATE, INSERT) are blocked.

    Args:
        sql: The SQL query to execute. Must be a SELECT statement.
        max_rows: Maximum number of rows to return (1-1000, default 100).
        format: Output format -- "table" for ASCII table, "csv" for CSV,
                "json" for JSON array.
    """
    # Validate SQL
    normalized = sql.strip().upper()
    if not normalized.startswith("SELECT"):
        raise ValueError("Only SELECT queries are allowed")

    dangerous = ["DROP", "DELETE", "UPDATE", "INSERT", "ALTER", "TRUNCATE"]
    for keyword in dangerous:
        if keyword in normalized:
            raise ValueError(f"Dangerous keyword '{keyword}' is not allowed")

    # Validate max_rows
    max_rows = min(max(1, max_rows), MAX_ROWS)

    # Validate format
    if format not in ("table", "csv", "json"):
        raise ValueError(f"Invalid format '{format}'. Use table, csv, or json.")

    # Execute query (using your database connection)
    result = await execute_query(sql, limit=max_rows)

    # Format output
    if format == "json":
        return json.dumps(result, indent=2, default=str)
    elif format == "csv":
        return format_as_csv(result)
    else:
        return format_as_table(result)


@server.tool()
async def list_tables() -> str:
    """List all available database tables and their row counts.

    Use this tool to discover what data is available before
    writing a query.
    """
    tables = []
    for table in sorted(ALLOWED_TABLES):
        count = await get_row_count(table)
        tables.append(f"  {table}: {count:,} rows")
    return "Available tables:\n" + "\n".join(tables)


@server.tool()
async def describe_table(table_name: str) -> str:
    """Get the schema (columns, types, constraints) for a database table.

    Use this tool to understand a table's structure before
    writing a query against it.

    Args:
        table_name: The name of the table to describe.
    """
    if table_name not in ALLOWED_TABLES:
        raise ValueError(
            f"Table '{table_name}' is not available. "
            f"Available tables: {', '.join(sorted(ALLOWED_TABLES))}"
        )
    schema = await get_table_schema(table_name)
    return format_schema(schema)
```

Key patterns to notice:

1. **Descriptive docstrings**: The model reads these to decide when to call each tool. Be specific about what the tool does and when to use it. Include examples of the kinds of questions each tool can answer.

2. **Input validation**: Validate every input before using it. MCP validates the JSON Schema types, but you must validate semantic constraints (allowed tables, safe SQL, value ranges).

3. **Default values**: Use sensible defaults so the model does not need to specify every parameter. `max_rows=100` and `format="table"` cover the common case.

4. **Error messages**: Raise `ValueError` with clear messages. The error text is sent back to the model, which can use it to correct its tool call. "Table 'nonexistent' is not available. Available tables: users, orders, products, analytics" is much more useful than "Invalid table."

5. **Discovery tools**: Always provide tools that help the model discover what is available. `list_tables` and `describe_table` let the model explore the database schema before writing queries. Without these, the model has to guess table and column names.

### Input Validation Deep Dive

MCP servers receive input from AI models, which means the input is generated, not typed by a human. Models make mistakes -- they hallucinate column names, invent parameters, and sometimes pass the wrong types despite the schema. Robust input validation is not optional.

The Python SDK validates JSON Schema types automatically. If your tool expects `a: float` and the model sends `"hello"`, the SDK returns an error before your code runs. But type validation is just the first layer.

```python
from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class ValidationResult:
    """Result of input validation."""
    valid: bool
    error: Optional[str] = None
    sanitized_value: Optional[str] = None


def validate_sql(sql: str) -> ValidationResult:
    """Validate a SQL query for safety and correctness."""
    if not sql or not sql.strip():
        return ValidationResult(False, "SQL query cannot be empty")

    normalized = sql.strip()
    upper = normalized.upper()

    # Must start with SELECT
    if not upper.startswith("SELECT"):
        return ValidationResult(False, "Only SELECT queries are allowed")

    # Block dangerous keywords
    dangerous_patterns = [
        r"\bDROP\b", r"\bDELETE\b", r"\bUPDATE\b", r"\bINSERT\b",
        r"\bALTER\b", r"\bTRUNCATE\b", r"\bEXEC\b", r"\bEXECUTE\b",
        r"\bCREATE\b", r"\bGRANT\b", r"\bREVOKE\b",
    ]
    for pattern in dangerous_patterns:
        if re.search(pattern, upper):
            keyword = re.search(pattern, upper).group()
            return ValidationResult(
                False, f"Dangerous keyword '{keyword}' is not allowed"
            )

    # Block multiple statements (SQL injection via semicolons)
    if ";" in normalized[:-1]:  # Allow trailing semicolon
        return ValidationResult(
            False, "Multiple SQL statements are not allowed"
        )

    # Block comments (potential injection vector)
    if "--" in normalized or "/*" in normalized:
        return ValidationResult(False, "SQL comments are not allowed")

    return ValidationResult(True, sanitized_value=normalized.rstrip(";"))


def validate_table_name(name: str, allowed: set) -> ValidationResult:
    """Validate a table name against an allowlist."""
    if not name or not name.strip():
        return ValidationResult(False, "Table name cannot be empty")

    cleaned = name.strip().lower()

    # Only allow alphanumeric and underscores
    if not re.match(r"^[a-z][a-z0-9_]*$", cleaned):
        return ValidationResult(
            False,
            f"Invalid table name '{cleaned}'. "
            "Use only lowercase letters, numbers, and underscores."
        )

    if cleaned not in allowed:
        return ValidationResult(
            False,
            f"Table '{cleaned}' is not available. "
            f"Available: {', '.join(sorted(allowed))}"
        )

    return ValidationResult(True, sanitized_value=cleaned)
```

### Error Handling Patterns

MCP tools should return errors in a way that helps the model recover. There are two kinds of errors:

1. **Tool errors**: The tool executed but the operation failed. Return an error result with `is_error=True`. The model sees the error message and can try again with corrected input.

2. **Protocol errors**: The request itself is malformed. Raise an exception. The SDK converts it to a JSON-RPC error response.

```python
from mcp.server.fastmcp import FastMCP
from mcp.types import TextContent

server = FastMCP("robust-server")

@server.tool()
async def safe_query(sql: str) -> list:
    """Execute a database query with comprehensive error handling."""
    # Validate input
    validation = validate_sql(sql)
    if not validation.valid:
        # Return error as tool result -- model can see it and retry
        return [TextContent(
            type="text",
            text=f"Error: {validation.error}\n\n"
                 f"Please fix the query and try again. "
                 f"Only SELECT statements against these tables "
                 f"are allowed: {', '.join(sorted(ALLOWED_TABLES))}"
        )]

    try:
        result = await execute_query(validation.sanitized_value)
        return [TextContent(type="text", text=format_result(result))]
    except DatabaseConnectionError as e:
        # Transient error -- tell the model to retry
        return [TextContent(
            type="text",
            text=f"Database connection error: {e}. "
                 f"This is a temporary issue. Please try again."
        )]
    except QueryTimeoutError as e:
        # Query too complex -- suggest simplification
        return [TextContent(
            type="text",
            text=f"Query timed out after {e.timeout}s. "
                 f"Try simplifying the query: use LIMIT, "
                 f"avoid subqueries, or filter with WHERE."
        )]
    except Exception as e:
        # Unknown error -- log and return generic message
        logger.exception("Unexpected error executing query")
        return [TextContent(
            type="text",
            text="An unexpected error occurred. "
                 "Please try a different query."
        )]
```

The pattern is: validate first, catch specific exceptions, provide actionable error messages that help the model recover. Never return a raw stack trace -- the model cannot do anything useful with it.

### Testing Your Server Locally

Testing MCP servers requires testing at two levels: unit tests for individual tool logic, and integration tests for the full MCP protocol flow.

**Unit Testing Tool Logic**

Extract your tool logic into pure functions that can be tested without the MCP framework:

```python
"""test_db_tools.py -- Unit tests for database tool logic."""

import pytest
from db_server import validate_sql, validate_table_name, ALLOWED_TABLES


class TestValidateSQL:
    """Tests for SQL validation."""

    def test_valid_select(self):
        result = validate_sql("SELECT * FROM users")
        assert result.valid is True
        assert result.sanitized_value == "SELECT * FROM users"

    def test_rejects_empty(self):
        result = validate_sql("")
        assert result.valid is False
        assert "empty" in result.error.lower()

    def test_rejects_drop(self):
        result = validate_sql("DROP TABLE users")
        assert result.valid is False
        assert "DROP" in result.error

    def test_rejects_delete(self):
        result = validate_sql("DELETE FROM users WHERE id = 1")
        assert result.valid is False

    def test_rejects_multiple_statements(self):
        result = validate_sql("SELECT 1; DROP TABLE users")
        assert result.valid is False
        assert "Multiple" in result.error

    def test_allows_trailing_semicolon(self):
        result = validate_sql("SELECT * FROM users;")
        assert result.valid is True

    def test_rejects_comments(self):
        result = validate_sql("SELECT * FROM users -- drop table")
        assert result.valid is False

    def test_case_insensitive_select(self):
        result = validate_sql("select * from users")
        assert result.valid is True


class TestValidateTableName:
    """Tests for table name validation."""

    def test_valid_table(self):
        result = validate_table_name("users", ALLOWED_TABLES)
        assert result.valid is True

    def test_rejects_unknown_table(self):
        result = validate_table_name("secrets", ALLOWED_TABLES)
        assert result.valid is False
        assert "not available" in result.error

    def test_rejects_sql_injection(self):
        result = validate_table_name("users; DROP TABLE", ALLOWED_TABLES)
        assert result.valid is False

    def test_strips_whitespace(self):
        result = validate_table_name("  users  ", ALLOWED_TABLES)
        assert result.valid is True
        assert result.sanitized_value == "users"
```

**Integration Testing with the MCP Client**

For full protocol testing, use the SDK's client to connect to your server:

```python
"""test_integration.py -- Integration tests for the MCP server."""

import asyncio
import pytest
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


@pytest.fixture
async def session():
    """Create a client session connected to the test server."""
    params = StdioServerParameters(
        command="python",
        args=["db_server.py"],
        env={"DATABASE_URL": "sqlite:///test.db"},
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield session


@pytest.mark.asyncio
async def test_list_tools(session):
    """Server exposes the expected tools."""
    tools = await session.list_tools()
    names = {t.name for t in tools.tools}
    assert "query_database" in names
    assert "list_tables" in names
    assert "describe_table" in names


@pytest.mark.asyncio
async def test_query_returns_results(session):
    """A valid query returns formatted results."""
    result = await session.call_tool(
        "query_database",
        {"sql": "SELECT 1 as value", "format": "json"},
    )
    assert len(result.content) > 0
    assert "value" in result.content[0].text


@pytest.mark.asyncio
async def test_dangerous_query_rejected(session):
    """A dangerous query returns an error, not a crash."""
    result = await session.call_tool(
        "query_database",
        {"sql": "DROP TABLE users"},
    )
    assert "error" in result.content[0].text.lower() or result.isError
```

---

## Chapter 3: Advanced Server Patterns

### Stateful Servers: Sessions and Context

Many real-world MCP servers need to maintain state across tool calls. A database server needs a connection pool. A code execution server needs a sandbox with accumulated state. A workflow server needs to track which steps have been completed.

MCP supports stateful servers through server-side session management. Each client connection gets a unique session. The server can store per-session state that persists across tool calls within that session.

```python
"""stateful_server.py -- MCP server with session state."""

from dataclasses import dataclass, field
from typing import Any
from mcp.server.fastmcp import FastMCP

server = FastMCP("workflow")


@dataclass
class WorkflowState:
    """Per-session workflow state."""
    steps_completed: list = field(default_factory=list)
    variables: dict = field(default_factory=dict)
    current_step: int = 0
    total_steps: int = 0


# Session state storage
_sessions: dict[str, WorkflowState] = {}


def get_state(session_id: str) -> WorkflowState:
    """Get or create session state."""
    if session_id not in _sessions:
        _sessions[session_id] = WorkflowState()
    return _sessions[session_id]


@server.tool()
async def start_workflow(name: str, steps: list[str]) -> str:
    """Start a new multi-step workflow.

    Args:
        name: Name of the workflow.
        steps: List of step descriptions in order.
    """
    ctx = server.request_context
    state = get_state(ctx.session.session_id)
    state.steps_completed = []
    state.current_step = 0
    state.total_steps = len(steps)
    state.variables["workflow_name"] = name
    state.variables["steps"] = steps
    return (
        f"Workflow '{name}' started with {len(steps)} steps.\n"
        f"Next step: {steps[0]}"
    )


@server.tool()
async def complete_step(result: str) -> str:
    """Mark the current workflow step as complete.

    Args:
        result: The result or output of the completed step.
    """
    ctx = server.request_context
    state = get_state(ctx.session.session_id)

    if state.current_step >= state.total_steps:
        return "Error: No active workflow or all steps already completed."

    steps = state.variables.get("steps", [])
    step_name = steps[state.current_step]
    state.steps_completed.append({
        "step": step_name,
        "result": result,
        "index": state.current_step,
    })
    state.current_step += 1

    if state.current_step >= state.total_steps:
        return (
            f"Step '{step_name}' completed. "
            f"Workflow '{state.variables['workflow_name']}' is now finished. "
            f"All {state.total_steps} steps completed."
        )

    next_step = steps[state.current_step]
    return (
        f"Step '{step_name}' completed ({state.current_step}/{state.total_steps}). "
        f"Next step: {next_step}"
    )


@server.tool()
async def get_workflow_status() -> str:
    """Get the current workflow progress and completed steps."""
    ctx = server.request_context
    state = get_state(ctx.session.session_id)

    if state.total_steps == 0:
        return "No active workflow. Use start_workflow to begin."

    lines = [
        f"Workflow: {state.variables.get('workflow_name', 'Unknown')}",
        f"Progress: {state.current_step}/{state.total_steps}",
        "",
        "Completed steps:",
    ]
    for step in state.steps_completed:
        lines.append(f"  [{step['index'] + 1}] {step['step']}: {step['result']}")

    if state.current_step < state.total_steps:
        remaining = state.variables["steps"][state.current_step:]
        lines.append("")
        lines.append("Remaining steps:")
        for i, step in enumerate(remaining):
            lines.append(f"  [{state.current_step + i + 1}] {step}")

    return "\n".join(lines)
```

### Streaming Responses

For long-running operations, streaming progress updates to the client prevents timeouts and keeps the user informed. MCP supports streaming through progress notifications and logging.

```python
"""streaming_server.py -- MCP server with progress streaming."""

import asyncio
from mcp.server.fastmcp import FastMCP

server = FastMCP("data-processor")


@server.tool()
async def process_large_dataset(
    source: str,
    batch_size: int = 1000,
) -> str:
    """Process a large dataset in batches with progress updates.

    Args:
        source: The data source identifier.
        batch_size: Number of records per batch.
    """
    ctx = server.request_context
    total_records = await get_record_count(source)
    processed = 0
    errors = 0
    batches = (total_records + batch_size - 1) // batch_size

    for batch_num in range(batches):
        # Send progress notification
        await ctx.report_progress(
            progress=batch_num,
            total=batches,
        )

        # Send log message for visibility
        await ctx.info(
            f"Processing batch {batch_num + 1}/{batches} "
            f"({processed}/{total_records} records)"
        )

        # Process the batch
        batch_result = await process_batch(source, batch_num, batch_size)
        processed += batch_result["processed"]
        errors += batch_result["errors"]

        # Yield control to allow other requests
        await asyncio.sleep(0)

    return (
        f"Processing complete.\n"
        f"Total records: {total_records}\n"
        f"Processed: {processed}\n"
        f"Errors: {errors}\n"
        f"Batches: {batches}"
    )
```

The `report_progress` method sends a `notifications/progress` message that the client can use to display a progress bar. The `info` method sends a log message that appears in the client's log stream.

### Rate Limiting and Quotas

If your MCP server wraps a paid API or a resource-constrained backend, you need rate limiting. Implement it as middleware that runs before every tool call.

```python
"""rate_limited_server.py -- MCP server with rate limiting."""

import time
from dataclasses import dataclass, field
from collections import defaultdict
from mcp.server.fastmcp import FastMCP

server = FastMCP("rate-limited-api")


@dataclass
class RateLimiter:
    """Token bucket rate limiter."""
    max_tokens: int = 60
    refill_rate: float = 1.0  # tokens per second
    _buckets: dict = field(default_factory=lambda: defaultdict(lambda: {"tokens": 60, "last": time.monotonic()}))

    def allow(self, key: str) -> bool:
        """Check if a request is allowed and consume a token."""
        bucket = self._buckets[key]
        now = time.monotonic()
        elapsed = now - bucket["last"]
        bucket["tokens"] = min(
            self.max_tokens,
            bucket["tokens"] + elapsed * self.refill_rate,
        )
        bucket["last"] = now

        if bucket["tokens"] >= 1:
            bucket["tokens"] -= 1
            return True
        return False

    def tokens_remaining(self, key: str) -> int:
        """Return approximate tokens remaining."""
        bucket = self._buckets[key]
        now = time.monotonic()
        elapsed = now - bucket["last"]
        return int(min(
            self.max_tokens,
            bucket["tokens"] + elapsed * self.refill_rate,
        ))


@dataclass
class QuotaTracker:
    """Track usage against daily quotas."""
    daily_limit: int = 10000
    _usage: dict = field(default_factory=lambda: defaultdict(lambda: {"count": 0, "day": ""}))

    def check_and_increment(self, key: str) -> tuple[bool, int]:
        """Check quota and increment usage. Returns (allowed, remaining)."""
        today = time.strftime("%Y-%m-%d")
        record = self._usage[key]

        # Reset on new day
        if record["day"] != today:
            record["count"] = 0
            record["day"] = today

        if record["count"] >= self.daily_limit:
            return False, 0

        record["count"] += 1
        remaining = self.daily_limit - record["count"]
        return True, remaining


limiter = RateLimiter(max_tokens=60, refill_rate=1.0)
quota = QuotaTracker(daily_limit=10000)


def rate_limit_check(client_id: str) -> None:
    """Check rate limit and quota before processing."""
    if not limiter.allow(client_id):
        remaining = limiter.tokens_remaining(client_id)
        raise RuntimeError(
            f"Rate limit exceeded. {remaining} tokens remaining. "
            f"Try again in a few seconds."
        )

    allowed, remaining = quota.check_and_increment(client_id)
    if not allowed:
        raise RuntimeError(
            f"Daily quota of {quota.daily_limit} requests exhausted. "
            f"Resets at midnight UTC."
        )


@server.tool()
async def translate(text: str, target_language: str) -> str:
    """Translate text to the target language.

    Args:
        text: The text to translate.
        target_language: ISO 639-1 language code (e.g., 'es', 'fr', 'de').
    """
    ctx = server.request_context
    client_id = ctx.session.session_id

    rate_limit_check(client_id)

    result = await call_translation_api(text, target_language)
    return result
```

### Authentication: API Keys and OAuth

Remote MCP servers need authentication. The MCP specification does not mandate a specific auth mechanism -- it relies on the transport layer. For HTTP-based transports, use standard HTTP authentication.

**API Key Authentication**

```python
"""auth_server.py -- MCP server with API key authentication."""

import hashlib
import os
from mcp.server.fastmcp import FastMCP

server = FastMCP("authenticated-api")

# In production, store hashed keys in a database
API_KEYS = {
    hashlib.sha256(b"ghx_key_test_12345").hexdigest(): {
        "client_id": "client-1",
        "tier": "pro",
        "rate_limit": 1000,
    },
    hashlib.sha256(b"ghx_key_test_67890").hexdigest(): {
        "client_id": "client-2",
        "tier": "free",
        "rate_limit": 100,
    },
}


def authenticate(api_key: str) -> dict:
    """Validate an API key and return the client profile."""
    key_hash = hashlib.sha256(api_key.encode()).hexdigest()
    client = API_KEYS.get(key_hash)
    if not client:
        raise PermissionError("Invalid API key")
    return client


def authorize(client: dict, required_tier: str) -> None:
    """Check if the client has the required tier."""
    tier_order = {"free": 0, "basic": 1, "pro": 2, "enterprise": 3}
    if tier_order.get(client["tier"], 0) < tier_order.get(required_tier, 0):
        raise PermissionError(
            f"This tool requires '{required_tier}' tier. "
            f"Your tier: '{client['tier']}'. "
            f"Upgrade at https://example.com/pricing"
        )
```

**OAuth 2.0 Integration**

For enterprise deployments, OAuth provides delegated authorization. The MCP specification added first-class OAuth support in 2025, allowing servers to act as OAuth resource servers.

```python
"""oauth_server.py -- MCP server with OAuth 2.0."""

import httpx
from dataclasses import dataclass
from typing import Optional


@dataclass
class OAuthConfig:
    """OAuth 2.0 configuration for the MCP server."""
    issuer: str
    audience: str
    jwks_uri: str
    scopes_required: list[str]


async def validate_oauth_token(
    token: str,
    config: OAuthConfig,
) -> dict:
    """Validate an OAuth 2.0 bearer token.

    Returns the decoded token claims if valid.
    Raises PermissionError if invalid.
    """
    import jwt  # PyJWT library

    # Fetch JWKS (in production, cache this)
    async with httpx.AsyncClient() as client:
        resp = await client.get(config.jwks_uri)
        jwks = resp.json()

    # Decode and validate the token
    try:
        claims = jwt.decode(
            token,
            jwt.PyJWKSet.from_dict(jwks),
            algorithms=["RS256"],
            audience=config.audience,
            issuer=config.issuer,
        )
    except jwt.InvalidTokenError as e:
        raise PermissionError(f"Invalid OAuth token: {e}")

    # Check required scopes
    token_scopes = set(claims.get("scope", "").split())
    required = set(config.scopes_required)
    missing = required - token_scopes
    if missing:
        raise PermissionError(
            f"Missing required scopes: {', '.join(missing)}. "
            f"Token scopes: {', '.join(token_scopes)}"
        )

    return claims
```

### Multi-Tool Servers

Production MCP servers typically expose 5 to 50 tools organized around a domain. The key to a well-designed multi-tool server is grouping related tools and providing discovery tools that help the model navigate the available capabilities.

```python
"""multi_tool_server.py -- A multi-tool MCP server for project management."""

from mcp.server.fastmcp import FastMCP

server = FastMCP("project-manager")


# --- Discovery Tools ---

@server.tool()
async def list_capabilities() -> str:
    """List all available capabilities of this project management server.

    Call this tool first to understand what operations are available.
    """
    return """Available capabilities:

    PROJECT MANAGEMENT:
    - create_project: Create a new project
    - list_projects: List all projects
    - get_project: Get project details

    TASK MANAGEMENT:
    - create_task: Create a task in a project
    - update_task: Update task status/assignee
    - list_tasks: List tasks with filters

    TEAM MANAGEMENT:
    - add_member: Add a team member to a project
    - list_members: List project team members

    REPORTING:
    - project_summary: Get a project status summary
    - burndown_data: Get sprint burndown data
    """


# --- Project Tools ---

@server.tool()
async def create_project(
    name: str,
    description: str,
    owner: str,
) -> str:
    """Create a new project.

    Args:
        name: Project name (must be unique).
        description: What this project is about.
        owner: The agent or person who owns the project.
    """
    project = await db.create_project(name, description, owner)
    return f"Project created: {project['id']} ({name})"


@server.tool()
async def create_task(
    project_id: str,
    title: str,
    description: str = "",
    assignee: str = "",
    priority: str = "medium",
) -> str:
    """Create a task within a project.

    Args:
        project_id: The project to add the task to.
        title: Short task title.
        description: Detailed task description.
        assignee: Who is responsible for this task.
        priority: low, medium, high, or critical.
    """
    if priority not in ("low", "medium", "high", "critical"):
        raise ValueError(
            f"Invalid priority '{priority}'. "
            f"Use: low, medium, high, or critical."
        )
    task = await db.create_task(
        project_id, title, description, assignee, priority
    )
    return f"Task created: {task['id']} ({title}) in project {project_id}"
```

### Composing Servers: The Proxy Pattern

Sometimes you want to combine multiple MCP servers into one, or add cross-cutting concerns (logging, authentication, rate limiting) to an existing server. The proxy pattern wraps one or more upstream servers behind a single server that the client connects to.

```python
"""proxy_server.py -- MCP proxy that composes multiple upstream servers."""

import json
import logging
from dataclasses import dataclass, field
from typing import Optional

from mcp.server.fastmcp import FastMCP
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

logger = logging.getLogger(__name__)

server = FastMCP("mcp-proxy")


@dataclass
class UpstreamServer:
    """Configuration for an upstream MCP server."""
    name: str
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    tools: list[str] = field(default_factory=list)


@dataclass
class ProxyRouter:
    """Routes tool calls to the appropriate upstream server."""
    upstreams: dict[str, UpstreamServer] = field(default_factory=dict)
    tool_to_upstream: dict[str, str] = field(default_factory=dict)

    def register_upstream(self, upstream: UpstreamServer) -> None:
        """Register an upstream server and its tool mappings."""
        self.upstreams[upstream.name] = upstream
        for tool in upstream.tools:
            self.tool_to_upstream[tool] = upstream.name

    def get_upstream_for_tool(self, tool_name: str) -> Optional[str]:
        """Find which upstream server handles a given tool."""
        return self.tool_to_upstream.get(tool_name)

    async def forward_call(
        self,
        tool_name: str,
        arguments: dict,
    ) -> dict:
        """Forward a tool call to the appropriate upstream."""
        upstream_name = self.get_upstream_for_tool(tool_name)
        if not upstream_name:
            raise ValueError(f"No upstream server handles tool '{tool_name}'")

        upstream = self.upstreams[upstream_name]

        # Log the forwarded call
        logger.info(
            "Forwarding %s to %s with args: %s",
            tool_name, upstream_name, json.dumps(arguments)[:200],
        )

        # In production, maintain persistent sessions
        params = StdioServerParameters(
            command=upstream.command,
            args=upstream.args,
            env=upstream.env,
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return result


router = ProxyRouter()

# Register upstream servers
router.register_upstream(UpstreamServer(
    name="database",
    command="python",
    args=["db_server.py"],
    tools=["query_database", "list_tables", "describe_table"],
))

router.register_upstream(UpstreamServer(
    name="project-manager",
    command="python",
    args=["project_server.py"],
    tools=["create_project", "create_task", "list_tasks"],
))


@server.tool()
async def route_tool(tool_name: str, arguments: str) -> str:
    """Route a tool call to the appropriate upstream server.

    This is a meta-tool that forwards calls to specialized servers.

    Args:
        tool_name: The name of the tool to call.
        arguments: JSON string of the tool arguments.
    """
    args = json.loads(arguments)
    result = await router.forward_call(tool_name, args)
    return result.content[0].text if result.content else "No result"
```

---

## Chapter 4: Publishing to the MCP Registry

### The MCP Registry Ecosystem

The official MCP registry at registry.modelcontextprotocol.io is the central directory where developers publish and discover MCP servers. As of April 2026, it lists over 10,000 servers across categories like databases, APIs, developer tools, productivity, and AI/ML. Clients like Claude Desktop, Cursor, Windsurf, and VS Code with Copilot can install servers directly from the registry.

Publishing to the registry makes your server discoverable. When a user asks an AI client "Can you help me query my Postgres database?", the client can search the registry for relevant servers, suggest installation, and connect automatically. This is the distribution channel for MCP servers.

### The Server Manifest: .well-known/mcp/server.json

Every published MCP server needs a manifest file that describes its capabilities, transport, authentication requirements, and metadata. The manifest follows a standard schema that registries and clients use for discovery and installation.

```json
{
  "schema_version": "1.0",
  "server_info": {
    "name": "analytics-db",
    "version": "2.1.0",
    "description": "Query your analytics database using natural language. Supports PostgreSQL, MySQL, and SQLite. Read-only access with SQL injection protection.",
    "author": {
      "name": "DataTools Inc",
      "url": "https://datatools.example.com",
      "email": "support@datatools.example.com"
    },
    "repository": "https://github.com/datatools/mcp-analytics-db",
    "license": "MIT",
    "homepage": "https://datatools.example.com/mcp-analytics-db"
  },
  "transport": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "@datatools/mcp-analytics-db"]
  },
  "capabilities": {
    "tools": [
      {
        "name": "query_database",
        "description": "Execute a read-only SQL query"
      },
      {
        "name": "list_tables",
        "description": "List available database tables"
      },
      {
        "name": "describe_table",
        "description": "Get the schema for a table"
      }
    ],
    "resources": [],
    "prompts": []
  },
  "configuration": {
    "required": [
      {
        "name": "DATABASE_URL",
        "description": "PostgreSQL connection string",
        "type": "string",
        "secret": true
      }
    ],
    "optional": [
      {
        "name": "MAX_ROWS",
        "description": "Maximum rows returned per query",
        "type": "integer",
        "default": 100
      }
    ]
  },
  "tags": ["database", "sql", "postgresql", "analytics", "query"],
  "categories": ["databases", "analytics"]
}
```

### Metadata Requirements

To be accepted by the official registry, your manifest must include:

1. **server_info.name**: Unique, lowercase, alphanumeric with hyphens. This becomes your server's identifier. Choose carefully -- it cannot be changed after publishing.

2. **server_info.version**: Semantic versioning (MAJOR.MINOR.PATCH). Clients use this to detect updates and manage compatibility.

3. **server_info.description**: Clear, concise description of what your server does. This is the primary text users see when searching. Front-load the most important information -- "Query your analytics database using natural language" is better than "A comprehensive database querying solution."

4. **transport**: How to run the server. For stdio servers distributed as npm packages, the standard pattern is `npx -y @scope/package-name`. For Python packages: `uvx package-name` or `pipx run package-name`. The registry validates that the specified command is available and the server starts correctly.

5. **capabilities**: List of tools, resources, and prompts. Clients use this to show users what the server can do before installing it.

6. **configuration**: Required and optional configuration parameters. Mark secrets (API keys, connection strings) with `"secret": true` so clients know to handle them securely.

### Version Management

Semantic versioning communicates the impact of changes:

- **PATCH** (2.1.0 -> 2.1.1): Bug fixes. No tool signature changes. Clients can update automatically.
- **MINOR** (2.1.0 -> 2.2.0): New tools added. Existing tools unchanged. Backward-compatible. Clients can update automatically.
- **MAJOR** (2.1.0 -> 3.0.0): Breaking changes. Tool signatures changed, tools removed, or behavior altered. Clients should prompt the user before updating.

```python
"""version_management.py -- Semantic version management for MCP servers."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ServerVersion:
    """Represents a semantic version."""
    major: int
    minor: int
    patch: int
    pre_release: Optional[str] = None

    @classmethod
    def parse(cls, version_str: str) -> "ServerVersion":
        """Parse a semantic version string."""
        parts = version_str.split("-", 1)
        pre = parts[1] if len(parts) > 1 else None
        nums = parts[0].split(".")
        if len(nums) != 3:
            raise ValueError(f"Invalid version: {version_str}")
        return cls(int(nums[0]), int(nums[1]), int(nums[2]), pre)

    def __str__(self) -> str:
        base = f"{self.major}.{self.minor}.{self.patch}"
        return f"{base}-{self.pre_release}" if self.pre_release else base

    def is_compatible_with(self, other: "ServerVersion") -> bool:
        """Check if this version is backward-compatible with another."""
        if self.major != other.major:
            return False
        if self.major == 0:
            # Pre-1.0: minor version changes are breaking
            return self.minor == other.minor
        return True

    def bump_patch(self) -> "ServerVersion":
        return ServerVersion(self.major, self.minor, self.patch + 1)

    def bump_minor(self) -> "ServerVersion":
        return ServerVersion(self.major, self.minor + 1, 0)

    def bump_major(self) -> "ServerVersion":
        return ServerVersion(self.major + 1, 0, 0)
```

### Discovery and Search Optimization

Registry search considers these factors when ranking results:

1. **Name match**: Exact and partial matches against the server name.
2. **Description relevance**: Keyword matches in the description. Use specific, descriptive language.
3. **Tags**: Exact tag matches are weighted heavily. Use 5-10 relevant tags.
4. **Categories**: Placing your server in the right category ensures it appears in category browsing.
5. **Install count**: More-installed servers rank higher. This creates a flywheel effect.
6. **Recency**: Recently updated servers get a small boost.

Tips for optimizing discovery:

- **Name your server for the problem, not the solution**: `mcp-postgres-query` is better than `mcp-sql-executor`. Users search for "postgres" not "sql-executor."
- **Front-load the description**: "Query PostgreSQL databases with natural language" beats "A tool for executing SQL queries against various database backends including PostgreSQL."
- **Use specific tags**: `postgresql` is better than `database`. Include the specific technologies your server supports.
- **Publish frequently**: Regular updates (even small ones) signal an active project and boost ranking.

### Publishing Workflow

```bash
# 1. Validate your manifest
mcp validate server.json

# 2. Test your server starts and responds to initialize
mcp test server.json

# 3. Authenticate with the registry
mcp auth login

# 4. Publish
mcp publish

# 5. Verify it appears
mcp search your-server-name
```

For npm-distributed servers, the common pattern is:

```bash
# Build and publish the npm package
npm publish

# Then publish the MCP manifest to the registry
mcp publish --manifest .well-known/mcp/server.json
```

For Python-distributed servers:

```bash
# Build and publish to PyPI
python -m build
twine upload dist/*

# Then publish the MCP manifest
mcp publish --manifest .well-known/mcp/server.json
```

---

## Chapter 5: Enterprise MCP Governance

### Why Governance Matters

When a single developer installs an MCP server on their laptop, security is a personal responsibility. When an enterprise deploys MCP servers across thousands of developer workstations, security becomes a governance challenge. Which servers are allowed? Who authorized them? What data can they access? What happens when a server is compromised? Enterprise MCP governance answers these questions.

The stakes are significant. An MCP server has the same access as the process it runs in. A malicious or compromised server can read local files, access environment variables (which often contain API keys and credentials), make network requests, and execute arbitrary code. In enterprise environments where developers work with proprietary code, customer data, and production credentials, ungoverned MCP servers are a data exfiltration risk.

### SSO Integration for Server Access

Enterprise MCP deployments should integrate with the organization's SSO provider (Okta, Azure AD, Google Workspace) so that server access is governed by the same identity and access management policies as every other tool.

```python
"""enterprise_auth.py -- Enterprise SSO integration for MCP servers."""

from dataclasses import dataclass, field
from typing import Optional
import time
import secrets


@dataclass
class SSOConfig:
    """SSO configuration for enterprise MCP deployment."""
    provider: str  # "okta", "azure_ad", "google"
    tenant_id: str
    client_id: str
    client_secret: str
    allowed_groups: list[str] = field(default_factory=list)
    allowed_domains: list[str] = field(default_factory=list)
    mfa_required: bool = True
    session_timeout_minutes: int = 480  # 8 hours


@dataclass
class AccessPolicy:
    """Define who can access which MCP servers."""
    server_name: str
    allowed_groups: list[str]
    allowed_roles: list[str]
    requires_approval: bool = False
    approval_group: str = ""
    data_classification: str = "internal"
    max_session_hours: int = 8


@dataclass
class EnterpriseGateway:
    """Gateway that enforces SSO and access policies for MCP servers."""
    sso_config: SSOConfig
    policies: dict[str, AccessPolicy] = field(default_factory=dict)
    _active_sessions: dict[str, dict] = field(default_factory=dict)

    def register_policy(self, policy: AccessPolicy) -> None:
        """Register an access policy for an MCP server."""
        self.policies[policy.server_name] = policy

    def check_access(
        self, user_id: str, user_groups: list[str],
        user_roles: list[str], server_name: str,
    ) -> dict:
        """Check if a user can access a specific MCP server."""
        policy = self.policies.get(server_name)
        if not policy:
            return {
                "allowed": False,
                "reason": f"No access policy defined for server '{server_name}'",
            }

        # Check group membership
        user_group_set = set(user_groups)
        allowed_group_set = set(policy.allowed_groups)
        if not user_group_set.intersection(allowed_group_set):
            return {
                "allowed": False,
                "reason": (
                    f"User is not a member of any allowed group. "
                    f"Required: {policy.allowed_groups}"
                ),
            }

        # Check role
        user_role_set = set(user_roles)
        allowed_role_set = set(policy.allowed_roles)
        if not user_role_set.intersection(allowed_role_set):
            return {
                "allowed": False,
                "reason": (
                    f"User does not have a required role. "
                    f"Required: {policy.allowed_roles}"
                ),
            }

        # Check if approval is needed
        if policy.requires_approval:
            return {
                "allowed": False,
                "reason": "Access requires approval",
                "approval_group": policy.approval_group,
                "requires_approval": True,
            }

        return {"allowed": True, "data_classification": policy.data_classification}

    def create_session(self, user_id: str, server_name: str) -> dict:
        """Create an authenticated session for a user-server pair."""
        policy = self.policies.get(server_name)
        max_hours = policy.max_session_hours if policy else 8
        session_id = secrets.token_hex(16)

        self._active_sessions[session_id] = {
            "user_id": user_id,
            "server_name": server_name,
            "created_at": time.time(),
            "expires_at": time.time() + (max_hours * 3600),
            "requests_count": 0,
        }
        return {"session_id": session_id, "expires_in_hours": max_hours}

    def validate_session(self, session_id: str) -> dict:
        """Validate that a session is still active."""
        session = self._active_sessions.get(session_id)
        if not session:
            return {"valid": False, "reason": "Session not found"}
        if time.time() > session["expires_at"]:
            del self._active_sessions[session_id]
            return {"valid": False, "reason": "Session expired"}
        session["requests_count"] += 1
        return {"valid": True, "user_id": session["user_id"]}
```

### Audit Logging

Every tool call through an enterprise MCP deployment should be logged with enough detail for security review, compliance, and incident response.

```python
"""audit_logging.py -- Structured audit logging for MCP servers."""

import json
import time
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class AuditEvent:
    """A single audit event for an MCP tool call."""
    timestamp: float
    event_type: str  # "tool_call", "tool_result", "auth_failure", "policy_violation"
    user_id: str
    server_name: str
    tool_name: str
    session_id: str
    request_id: str
    arguments_hash: str  # SHA-256 of the arguments (not the arguments themselves)
    result_status: str  # "success", "error", "denied"
    duration_ms: float = 0.0
    error_message: Optional[str] = None
    data_classification: str = "internal"
    client_ip: str = ""
    user_agent: str = ""


@dataclass
class AuditLogger:
    """Structured audit logger that writes to multiple sinks."""
    sinks: list = field(default_factory=list)
    _buffer: list = field(default_factory=list)
    buffer_size: int = 100

    def log(self, event: AuditEvent) -> None:
        """Log an audit event."""
        self._buffer.append(asdict(event))
        if len(self._buffer) >= self.buffer_size:
            self.flush()

    def flush(self) -> None:
        """Flush buffered events to all sinks."""
        if not self._buffer:
            return
        events = list(self._buffer)
        self._buffer.clear()
        for sink in self.sinks:
            sink.write(events)

    def query(
        self,
        user_id: Optional[str] = None,
        server_name: Optional[str] = None,
        tool_name: Optional[str] = None,
        start_time: Optional[float] = None,
        end_time: Optional[float] = None,
    ) -> list:
        """Query audit events with filters."""
        self.flush()
        results = []
        for sink in self.sinks:
            if hasattr(sink, "query"):
                results.extend(sink.query(
                    user_id=user_id, server_name=server_name,
                    tool_name=tool_name,
                    start_time=start_time, end_time=end_time,
                ))
        return results
```

### Gateway Patterns

Enterprise MCP gateways sit between AI clients and MCP servers. They enforce policies, add authentication, log activity, and control which servers are available.

**The Central Gateway Model**

All MCP traffic flows through a central gateway service. Developers configure their AI clients to connect to the gateway instead of individual servers. The gateway authenticates the user, checks access policies, forwards the request to the appropriate server, logs the interaction, and returns the result.

```
Developer's AI Client
    |
    +-- connects to --> Enterprise MCP Gateway
                            |
                            +-- authenticates via SSO
                            +-- checks access policy
                            +-- forwards to --> MCP Server A
                            +-- forwards to --> MCP Server B
                            +-- logs to --> Audit Log
```

Advantages: Central policy enforcement. Single point of audit logging. Easy to add or remove servers. Can cache responses, rate limit, and filter.

Disadvantages: Single point of failure. Adds latency. Requires infrastructure.

**The Sidecar Model**

A lightweight policy agent runs alongside each MCP server on the developer's machine. The sidecar intercepts tool calls, checks policies against a central policy server, and logs activity.

Advantages: No central bottleneck. Works offline with cached policies. Lower latency.

Disadvantages: Must be installed on every machine. Policy updates require propagation. Harder to audit in real time.

### Policy Enforcement

Enterprise policies for MCP servers typically cover four areas:

1. **Server allowlist**: Only approved servers can be installed. Unapproved servers are blocked.
2. **Tool restrictions**: Even within an approved server, certain tools may be restricted by team.
3. **Data classification**: Tools that access confidential data require additional authorization.
4. **Rate limits**: Per-user and per-team rate limits prevent runaway usage.

```python
"""policy_engine.py -- Policy enforcement for enterprise MCP governance."""

import re
from dataclasses import dataclass, field


@dataclass
class PolicyRule:
    """A single policy rule."""
    rule_id: str
    description: str
    action: str  # "allow", "deny", "require_approval"
    server_pattern: str = "*"
    tool_pattern: str = "*"
    user_groups: list[str] = field(default_factory=list)
    priority: int = 0


@dataclass
class PolicyEngine:
    """Evaluate access policies for MCP tool calls."""
    rules: list[PolicyRule] = field(default_factory=list)

    def add_rule(self, rule: PolicyRule) -> None:
        """Add a policy rule."""
        self.rules.append(rule)
        self.rules.sort(key=lambda r: r.priority, reverse=True)

    def evaluate(
        self,
        server_name: str,
        tool_name: str,
        user_groups: list[str],
    ) -> dict:
        """Evaluate policies and return the access decision."""
        for rule in self.rules:
            if not self._matches(rule.server_pattern, server_name):
                continue
            if not self._matches(rule.tool_pattern, tool_name):
                continue
            if rule.user_groups:
                if not set(user_groups).intersection(set(rule.user_groups)):
                    continue
            return {
                "decision": rule.action,
                "rule_id": rule.rule_id,
                "description": rule.description,
            }

        # Default deny
        return {
            "decision": "deny",
            "rule_id": "default",
            "description": "No matching policy rule; default deny",
        }

    @staticmethod
    def _matches(pattern: str, value: str) -> bool:
        """Simple glob matching."""
        regex = pattern.replace(".", r"\.").replace("*", ".*").replace("?", ".")
        return bool(re.fullmatch(regex, value))
```

### Configuration Portability

Enterprise teams need a standard way to share MCP server configurations. A centralized configuration service distributes approved server configs to developer machines.

```python
"""config_portability.py -- Portable MCP configuration management."""

import json
from dataclasses import dataclass, field


@dataclass
class MCPServerConfig:
    """Configuration for a single MCP server."""
    name: str
    command: str
    args: list[str] = field(default_factory=list)
    env: dict[str, str] = field(default_factory=dict)
    env_secrets: list[str] = field(default_factory=list)
    enabled: bool = True
    required_groups: list[str] = field(default_factory=list)


@dataclass
class TeamConfig:
    """MCP configuration for a team."""
    team_name: str
    servers: list[MCPServerConfig] = field(default_factory=list)
    version: str = "1.0.0"

    def to_claude_desktop_config(self) -> dict:
        """Export as Claude Desktop configuration format."""
        mcp_servers = {}
        for s in self.servers:
            if not s.enabled:
                continue
            config = {"command": s.command, "args": s.args}
            if s.env:
                config["env"] = s.env
            mcp_servers[s.name] = config
        return {"mcpServers": mcp_servers}

    def to_cursor_config(self) -> dict:
        """Export as Cursor IDE configuration format."""
        return {
            "mcp": {
                "servers": {
                    s.name: {
                        "command": s.command,
                        "args": s.args,
                        "env": s.env,
                    }
                    for s in self.servers if s.enabled
                }
            }
        }

    def to_json(self) -> str:
        """Serialize to portable JSON."""
        return json.dumps({
            "team": self.team_name,
            "version": self.version,
            "servers": [
                {
                    "name": s.name,
                    "command": s.command,
                    "args": s.args,
                    "env": {k: v for k, v in s.env.items()},
                    "env_secrets": s.env_secrets,
                    "enabled": s.enabled,
                    "required_groups": s.required_groups,
                }
                for s in self.servers
            ],
        }, indent=2)
```

### Compliance Considerations

Enterprise MCP deployments must address regulatory requirements:

**Data Residency**: Some regulations require data to stay within specific geographic regions. MCP servers that access customer data must run in the same region as the data. Remote MCP servers (HTTP transport) must be deployed in compliant regions.

**Access Reviews**: Periodic reviews of who has access to which MCP servers. The audit log provides the data; the governance team reviews it quarterly.

**Data Loss Prevention**: MCP servers can exfiltrate data by including it in tool responses that flow to cloud-hosted AI models. DLP policies should scan tool responses for sensitive patterns (credit card numbers, SSNs, API keys) and redact them before they reach the model.

**Retention**: Audit logs must be retained per the organization's data retention policy. Tool call arguments and results may contain sensitive data and should be stored with appropriate encryption and access controls.

---

## Chapter 6: Monetization Strategies

### The MCP Server Business Landscape

MCP servers are the new APIs. Every business model that works for APIs works for MCP servers -- with one advantage: MCP servers are discoverable by AI agents, which means your market is not just human developers but also autonomous systems that find, evaluate, and pay for tools at machine speed. This chapter covers six monetization strategies, from freemium to pay-per-use, with implementation details for each.

### Strategy 1: Freemium (Basic Tools Free, Advanced Paid)

The most common model. Offer a set of basic tools for free to drive adoption, then gate advanced tools behind a paid tier. The free tier serves as a distribution mechanism -- every free user is a potential paid customer.

```python
"""freemium_server.py -- MCP server with tiered tool access."""

from dataclasses import dataclass, field
from typing import Optional
from mcp.server.fastmcp import FastMCP

server = FastMCP("analytics-server")


@dataclass
class TierConfig:
    """Configuration for a pricing tier."""
    name: str
    tools_allowed: set
    monthly_price_usd: float
    daily_call_limit: int
    max_rows_per_query: int


TIERS = {
    "free": TierConfig(
        name="Free",
        tools_allowed={"query_database", "list_tables", "describe_table"},
        monthly_price_usd=0.0,
        daily_call_limit=100,
        max_rows_per_query=100,
    ),
    "pro": TierConfig(
        name="Pro",
        tools_allowed={
            "query_database", "list_tables", "describe_table",
            "create_dashboard", "schedule_report", "export_data",
            "query_optimizer", "schema_diff",
        },
        monthly_price_usd=29.0,
        daily_call_limit=10000,
        max_rows_per_query=10000,
    ),
    "enterprise": TierConfig(
        name="Enterprise",
        tools_allowed={
            "query_database", "list_tables", "describe_table",
            "create_dashboard", "schedule_report", "export_data",
            "query_optimizer", "schema_diff",
            "admin_create_user", "admin_audit_log", "admin_backup",
            "custom_function", "cross_database_query",
        },
        monthly_price_usd=199.0,
        daily_call_limit=100000,
        max_rows_per_query=1000000,
    ),
}


@dataclass
class ClientProfile:
    """Tracks a client's tier and usage."""
    client_id: str
    tier: str = "free"
    daily_calls: int = 0
    last_reset_day: str = ""


_clients: dict[str, ClientProfile] = {}


def get_client(client_id: str) -> ClientProfile:
    """Get or create a client profile."""
    if client_id not in _clients:
        _clients[client_id] = ClientProfile(client_id=client_id)
    return _clients[client_id]


def check_tier_access(client_id: str, tool_name: str) -> None:
    """Verify the client's tier allows access to the tool."""
    import time
    client = get_client(client_id)
    tier = TIERS.get(client.tier)
    if not tier:
        raise PermissionError(f"Unknown tier: {client.tier}")

    # Check tool access
    if tool_name not in tier.tools_allowed:
        available_in = [
            t.name for t in TIERS.values()
            if tool_name in t.tools_allowed
        ]
        raise PermissionError(
            f"Tool '{tool_name}' requires a {' or '.join(available_in)} plan. "
            f"Your plan: {tier.name}. Upgrade at https://example.com/pricing"
        )

    # Check daily limit
    today = time.strftime("%Y-%m-%d")
    if client.last_reset_day != today:
        client.daily_calls = 0
        client.last_reset_day = today

    if client.daily_calls >= tier.daily_call_limit:
        raise PermissionError(
            f"Daily call limit of {tier.daily_call_limit} exceeded "
            f"for {tier.name} plan. Resets at midnight UTC. "
            f"Upgrade for higher limits."
        )

    client.daily_calls += 1
```

### Strategy 2: Usage-Based Billing (Per-Call Metering)

Charge per tool call. This model aligns cost with value -- users pay only for what they use. It works well for high-volume, low-cost operations like API calls, translations, and data lookups.

```python
"""usage_billing.py -- Per-call usage metering for MCP servers."""

import time
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional


@dataclass
class UsageMeter:
    """Track per-call usage for billing."""
    _usage: dict = field(default_factory=lambda: defaultdict(list))

    def record(
        self,
        client_id: str,
        tool_name: str,
        cost_usd: float,
        metadata: Optional[dict] = None,
    ) -> dict:
        """Record a billable tool call."""
        event = {
            "timestamp": time.time(),
            "tool_name": tool_name,
            "cost_usd": cost_usd,
            "metadata": metadata or {},
        }
        self._usage[client_id].append(event)
        return event

    def get_current_bill(self, client_id: str) -> dict:
        """Calculate the current billing period total."""
        events = self._usage.get(client_id, [])
        # Filter to current month
        current_month = time.strftime("%Y-%m")
        month_events = [
            e for e in events
            if time.strftime("%Y-%m", time.localtime(e["timestamp"])) == current_month
        ]
        total = sum(e["cost_usd"] for e in month_events)
        by_tool = defaultdict(float)
        for e in month_events:
            by_tool[e["tool_name"]] += e["cost_usd"]

        return {
            "client_id": client_id,
            "period": current_month,
            "total_usd": round(total, 4),
            "call_count": len(month_events),
            "by_tool": dict(by_tool),
        }

    def get_usage_report(self, client_id: str, days: int = 30) -> dict:
        """Generate a usage report for the last N days."""
        events = self._usage.get(client_id, [])
        cutoff = time.time() - (days * 86400)
        recent = [e for e in events if e["timestamp"] >= cutoff]

        daily = defaultdict(lambda: {"calls": 0, "cost": 0.0})
        for e in recent:
            day = time.strftime("%Y-%m-%d", time.localtime(e["timestamp"]))
            daily[day]["calls"] += 1
            daily[day]["cost"] += e["cost_usd"]

        return {
            "client_id": client_id,
            "period_days": days,
            "total_calls": len(recent),
            "total_cost_usd": round(sum(e["cost_usd"] for e in recent), 4),
            "daily_breakdown": dict(daily),
        }


# Pricing per tool call
TOOL_PRICING = {
    "translate": 0.002,       # $0.002 per translation
    "summarize": 0.005,       # $0.005 per summary
    "analyze_image": 0.01,    # $0.01 per image analysis
    "generate_report": 0.05,  # $0.05 per report
    "query_database": 0.001,  # $0.001 per query
}

meter = UsageMeter()
```

### Strategy 3: Enterprise Licensing

Sell annual or multi-year licenses to organizations. This model provides predictable revenue, higher deal sizes, and longer customer relationships. Enterprise customers typically need SSO integration, audit logging, SLA guarantees, and dedicated support.

The key differentiators for enterprise licensing:

- **Unlimited usage** within the license (no per-call fees).
- **SLA guarantees**: 99.9% uptime, response time commitments.
- **Dedicated infrastructure**: Option for on-premise or private cloud deployment.
- **SSO/SCIM integration**: Automatic user provisioning.
- **Priority support**: Dedicated Slack channel, guaranteed response times.
- **Custom tools**: Build custom tools specific to the customer's domain.

Enterprise pricing is typically based on the number of developer seats or the number of connected AI agents, ranging from $500 to $5,000 per seat per year depending on the domain.

### Strategy 4: Marketplace Models

List your MCP server on AI tool marketplaces and take a revenue share. As of April 2026, several marketplaces accept MCP server listings:

- **The official MCP registry**: Free to list, no revenue share. You handle billing directly.
- **AI client marketplaces**: Cursor, Windsurf, and other IDEs are building in-app marketplaces where developers can purchase premium MCP servers. Revenue share varies from 15% to 30%.
- **Enterprise marketplaces**: Azure API Center and similar platforms list MCP servers for enterprise customers. Higher deal sizes but longer sales cycles.

### Strategy 5: Combining MCP with x402 for Pay-Per-Use

The x402 protocol enables HTTP-native micropayments. By combining an MCP server with an x402-enabled endpoint, you can create a pay-per-use model where agent clients pay per tool call without needing a subscription or API key. This is especially powerful for agent-to-agent commerce where the calling agent discovers your MCP server and pays automatically.

```python
"""x402_integration.py -- Combine MCP server with x402 pay-per-use."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class X402PaymentGate:
    """Gate MCP tool calls behind x402 micropayments."""
    payment_address: str
    tool_prices: dict = field(default_factory=dict)
    _verified_payments: dict = field(default_factory=dict)

    def set_price(self, tool_name: str, price_usd: float) -> None:
        """Set the price for a tool call."""
        self.tool_prices[tool_name] = price_usd

    def generate_payment_request(self, tool_name: str) -> dict:
        """Generate an x402 payment request for a tool call."""
        price = self.tool_prices.get(tool_name, 0.01)
        return {
            "status": 402,
            "headers": {
                "X-Payment-Amount": str(price),
                "X-Payment-Currency": "USD",
                "X-Payment-Methods": "x402",
                "X-Payment-Address": self.payment_address,
                "X-Payment-Description": f"MCP tool call: {tool_name}",
            },
        }

    def verify_payment(self, payment_token: str, tool_name: str) -> dict:
        """Verify an x402 payment token."""
        # In production, verify against the x402 facilitator
        price = self.tool_prices.get(tool_name, 0.01)
        return {
            "verified": True,
            "amount_usd": price,
            "token": payment_token,
            "tool_name": tool_name,
        }

    def check_and_charge(
        self, tool_name: str, payment_token: Optional[str],
    ) -> dict:
        """Check payment for a tool call. Returns payment status."""
        if tool_name not in self.tool_prices:
            return {"paid": True, "free": True}

        if not payment_token:
            return {
                "paid": False,
                "payment_required": self.generate_payment_request(tool_name),
            }

        verification = self.verify_payment(payment_token, tool_name)
        if not verification["verified"]:
            return {"paid": False, "reason": "Payment verification failed"}

        return {"paid": True, "amount_charged": verification["amount_usd"]}


# Example: Gate MCP tools behind x402
gate = X402PaymentGate(payment_address="ghx_pay_example")
gate.set_price("translate", 0.002)
gate.set_price("summarize", 0.005)
gate.set_price("analyze_image", 0.01)
```

### Strategy 6: Revenue Tracking and Analytics

Regardless of your monetization model, you need revenue tracking. Build it into your MCP server from day one.

```python
"""revenue_analytics.py -- Revenue tracking for MCP server monetization."""

import time
from dataclasses import dataclass, field
from collections import defaultdict


@dataclass
class RevenueTracker:
    """Track and analyze MCP server revenue."""
    _events: list = field(default_factory=list)

    def record_revenue(
        self,
        client_id: str,
        amount_usd: float,
        source: str,
        tool_name: str = "",
    ) -> None:
        """Record a revenue event."""
        self._events.append({
            "timestamp": time.time(),
            "client_id": client_id,
            "amount_usd": amount_usd,
            "source": source,  # "subscription", "usage", "enterprise", "x402"
            "tool_name": tool_name,
        })

    def monthly_recurring_revenue(self) -> float:
        """Calculate MRR from subscription events in the current month."""
        current_month = time.strftime("%Y-%m")
        return sum(
            e["amount_usd"] for e in self._events
            if e["source"] == "subscription"
            and time.strftime("%Y-%m", time.localtime(e["timestamp"])) == current_month
        )

    def revenue_by_tool(self, days: int = 30) -> dict:
        """Break down revenue by tool for the last N days."""
        cutoff = time.time() - (days * 86400)
        by_tool = defaultdict(float)
        for e in self._events:
            if e["timestamp"] >= cutoff and e["tool_name"]:
                by_tool[e["tool_name"]] += e["amount_usd"]
        return dict(by_tool)

    def customer_lifetime_value(self, client_id: str) -> float:
        """Calculate total revenue from a single customer."""
        return sum(
            e["amount_usd"] for e in self._events
            if e["client_id"] == client_id
        )

    def churn_rate(self, period_days: int = 30) -> float:
        """Estimate churn rate based on active customers."""
        now = time.time()
        current_cutoff = now - (period_days * 86400)
        previous_cutoff = current_cutoff - (period_days * 86400)

        current_clients = set(
            e["client_id"] for e in self._events
            if e["timestamp"] >= current_cutoff
        )
        previous_clients = set(
            e["client_id"] for e in self._events
            if previous_cutoff <= e["timestamp"] < current_cutoff
        )

        if not previous_clients:
            return 0.0

        churned = previous_clients - current_clients
        return len(churned) / len(previous_clients)
```

---

## Chapter 7: Production Operations

### Deployment Patterns

MCP servers can be deployed in several ways, depending on whether they need to run locally or remotely, and whether they serve a single user or many.

**Local stdio Deployment**

The simplest deployment. The AI client starts the server as a subprocess. No infrastructure needed. Suitable for personal tools and development.

```json
{
  "mcpServers": {
    "my-tool": {
      "command": "python",
      "args": ["/opt/mcp-servers/my-tool/server.py"],
      "env": {
        "DATABASE_URL": "sqlite:///data/analytics.db"
      }
    }
  }
}
```

**Docker Deployment**

Package your MCP server as a Docker container for consistent environments and easy distribution. Especially useful for servers with complex dependencies.

```dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# For stdio transport (used with docker run -i)
CMD ["python", "server.py"]

# For HTTP transport
# EXPOSE 8080
# CMD ["python", "server.py", "--transport", "http", "--port", "8080"]
```

For stdio transport with Docker:

```json
{
  "mcpServers": {
    "my-tool": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "my-mcp-server:latest"]
    }
  }
}
```

**Serverless Deployment**

For HTTP-based MCP servers with bursty traffic, serverless platforms (AWS Lambda, Google Cloud Functions, Cloudflare Workers) provide automatic scaling and pay-per-use pricing.

The key constraint with serverless is cold start latency. MCP's `initialize` handshake adds to the first-request latency. Mitigate with provisioned concurrency or by using the streamable HTTP transport (which allows stateless request-response without persistent connections).

**Edge Deployment**

For latency-sensitive MCP servers, deploy at the edge using Cloudflare Workers, Deno Deploy, or AWS CloudFront Functions. Edge deployment puts your server within 50ms of most users globally.

### Monitoring and Alerting

Production MCP servers need the same monitoring as any production service: health checks, latency tracking, error rates, and alerting.

```python
"""monitoring.py -- Monitoring for production MCP servers."""

import time
from dataclasses import dataclass, field
from collections import defaultdict
from typing import Optional


@dataclass
class ToolMetrics:
    """Metrics for a single tool."""
    call_count: int = 0
    error_count: int = 0
    total_latency_ms: float = 0.0
    max_latency_ms: float = 0.0
    last_call_time: float = 0.0


@dataclass
class ServerMonitor:
    """Monitor MCP server health and performance."""
    _tools: dict[str, ToolMetrics] = field(default_factory=lambda: defaultdict(ToolMetrics))
    _alerts: list = field(default_factory=list)
    error_rate_threshold: float = 0.05  # 5%
    latency_threshold_ms: float = 5000.0  # 5 seconds

    def record_call(
        self,
        tool_name: str,
        latency_ms: float,
        success: bool,
    ) -> None:
        """Record a tool call for monitoring."""
        metrics = self._tools[tool_name]
        metrics.call_count += 1
        metrics.total_latency_ms += latency_ms
        metrics.last_call_time = time.time()

        if latency_ms > metrics.max_latency_ms:
            metrics.max_latency_ms = latency_ms

        if not success:
            metrics.error_count += 1

        # Check thresholds
        self._check_alerts(tool_name, metrics, latency_ms, success)

    def _check_alerts(
        self,
        tool_name: str,
        metrics: ToolMetrics,
        latency_ms: float,
        success: bool,
    ) -> None:
        """Check if any alert thresholds are exceeded."""
        # High error rate
        if metrics.call_count >= 10:
            error_rate = metrics.error_count / metrics.call_count
            if error_rate > self.error_rate_threshold:
                self._alerts.append({
                    "type": "high_error_rate",
                    "tool": tool_name,
                    "error_rate": round(error_rate, 3),
                    "threshold": self.error_rate_threshold,
                    "timestamp": time.time(),
                })

        # High latency
        if latency_ms > self.latency_threshold_ms:
            self._alerts.append({
                "type": "high_latency",
                "tool": tool_name,
                "latency_ms": latency_ms,
                "threshold": self.latency_threshold_ms,
                "timestamp": time.time(),
            })

    def get_health(self) -> dict:
        """Get overall server health status."""
        total_calls = sum(m.call_count for m in self._tools.values())
        total_errors = sum(m.error_count for m in self._tools.values())
        error_rate = total_errors / total_calls if total_calls > 0 else 0.0

        return {
            "status": "healthy" if error_rate < self.error_rate_threshold else "degraded",
            "total_calls": total_calls,
            "total_errors": total_errors,
            "error_rate": round(error_rate, 4),
            "tools": {
                name: {
                    "calls": m.call_count,
                    "errors": m.error_count,
                    "avg_latency_ms": round(m.total_latency_ms / m.call_count, 1) if m.call_count > 0 else 0,
                    "max_latency_ms": round(m.max_latency_ms, 1),
                }
                for name, m in self._tools.items()
            },
            "recent_alerts": self._alerts[-10:],
        }
```

### Scaling Strategies

**Horizontal Scaling for HTTP Servers**

For HTTP-based MCP servers, scale horizontally behind a load balancer. Each instance is stateless (or uses shared state via Redis or a database).

```
Load Balancer
    |
    +-- MCP Server Instance 1
    +-- MCP Server Instance 2
    +-- MCP Server Instance 3
    |
    +-- Shared State (Redis / PostgreSQL)
```

**Connection Pooling for stdio Servers**

stdio servers cannot be shared across clients, but they can be pooled. A pool manager maintains a set of pre-started server processes and assigns them to incoming client connections.

**Caching**

For tools that return the same result for the same input (deterministic tools like schema lookups, format conversions, and reference data), implement response caching:

```python
"""caching.py -- Response caching for MCP tools."""

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ToolCache:
    """LRU cache for deterministic MCP tool responses."""
    max_size: int = 1000
    ttl_seconds: float = 300.0  # 5 minutes
    _cache: dict = field(default_factory=dict)
    _access_order: list = field(default_factory=list)

    def _make_key(self, tool_name: str, arguments: dict) -> str:
        """Create a cache key from tool name and arguments."""
        canonical = json.dumps(
            {"tool": tool_name, "args": arguments},
            sort_keys=True, separators=(",", ":"),
        )
        return hashlib.sha256(canonical.encode()).hexdigest()

    def get(self, tool_name: str, arguments: dict) -> Optional[str]:
        """Get a cached result if available and not expired."""
        key = self._make_key(tool_name, arguments)
        entry = self._cache.get(key)
        if not entry:
            return None
        if time.time() - entry["timestamp"] > self.ttl_seconds:
            del self._cache[key]
            return None
        return entry["result"]

    def put(self, tool_name: str, arguments: dict, result: str) -> None:
        """Cache a tool result."""
        key = self._make_key(tool_name, arguments)
        self._cache[key] = {
            "result": result,
            "timestamp": time.time(),
        }
        # Evict oldest if over max size
        if len(self._cache) > self.max_size:
            oldest_key = min(
                self._cache, key=lambda k: self._cache[k]["timestamp"]
            )
            del self._cache[oldest_key]
```

### Version Upgrades Without Breaking Clients

When upgrading your MCP server, maintain backward compatibility by following these rules:

1. **Never remove tools** in a minor version. Deprecate them first (add "DEPRECATED" to the description), then remove in the next major version.
2. **Never change tool input schemas** in a breaking way. Adding optional parameters is safe. Removing parameters or changing types is breaking.
3. **Use feature flags** to roll out new tool behavior gradually.
4. **Version your transport endpoint** (`/v1/mcp`, `/v2/mcp`) for HTTP servers.
5. **Test against older clients** before releasing.

### Security Hardening

Production MCP servers handle untrusted input from AI models. Apply defense-in-depth:

1. **Input validation**: Validate every input against the schema and semantic constraints. Never trust model-generated input.
2. **Sandboxing**: Run tool handlers in sandboxed environments when they execute user-provided code or queries.
3. **Network isolation**: MCP servers should only have network access to the services they need. Use firewall rules to block everything else.
4. **Secret management**: Never hardcode API keys or credentials. Use environment variables or a secret manager.
5. **Dependency scanning**: Regularly scan your dependencies for known vulnerabilities.
6. **Rate limiting**: Always implement rate limiting, even for internal servers. A compromised client can flood a server.

---

## Chapter 8: Case Studies

### Case Study 1: Data Connector MCP Server (Database Access)

**The Problem**: A data analytics company has 500 analysts who need to query 12 databases across three cloud providers. Each analyst has different access levels. The current workflow: write SQL in a notebook, run it, wait, copy-paste results into reports. AI assistants could automate this, but each database requires different connection logic, authentication, and query syntax.

**The Solution**: A single MCP server that provides unified access to all 12 databases with role-based access control.

```python
"""data_connector.py -- Multi-database MCP server case study."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class DatabaseConfig:
    """Configuration for a single database connection."""
    name: str
    engine: str  # "postgresql", "mysql", "bigquery", "snowflake"
    connection_string: str
    allowed_roles: list[str] = field(default_factory=list)
    read_only: bool = True
    max_rows: int = 10000
    timeout_seconds: int = 30


@dataclass
class DataConnector:
    """Multi-database connector with role-based access."""
    databases: dict[str, DatabaseConfig] = field(default_factory=dict)

    def register_database(self, config: DatabaseConfig) -> None:
        """Register a database connection."""
        self.databases[config.name] = config

    def list_databases(self, user_role: str) -> list:
        """List databases the user can access."""
        return [
            {
                "name": db.name,
                "engine": db.engine,
                "read_only": db.read_only,
                "max_rows": db.max_rows,
            }
            for db in self.databases.values()
            if user_role in db.allowed_roles or not db.allowed_roles
        ]

    def check_access(self, database_name: str, user_role: str) -> bool:
        """Check if a user role has access to a database."""
        db = self.databases.get(database_name)
        if not db:
            return False
        return user_role in db.allowed_roles or not db.allowed_roles

    def validate_query(self, database_name: str, sql: str) -> dict:
        """Validate a query against the database's constraints."""
        db = self.databases.get(database_name)
        if not db:
            return {"valid": False, "error": f"Database '{database_name}' not found"}

        upper_sql = sql.strip().upper()

        if db.read_only and not upper_sql.startswith("SELECT"):
            return {"valid": False, "error": "Database is read-only. Only SELECT allowed."}

        dangerous = ["DROP", "DELETE", "TRUNCATE", "ALTER"]
        for keyword in dangerous:
            if keyword in upper_sql:
                return {"valid": False, "error": f"Keyword '{keyword}' is not allowed"}

        return {"valid": True, "database": database_name, "engine": db.engine}
```

**Results**: Query time for analysts dropped 70% because the AI assistant handles SQL generation, connection routing, and result formatting. Access control incidents dropped to zero because the server enforces the same RBAC policies regardless of which AI client the analyst uses.

### Case Study 2: API Wrapper MCP Server (Third-Party API)

**The Problem**: A SaaS company's customer success team uses five different APIs (Salesforce, Zendesk, Stripe, Mixpanel, Intercom) to manage customer accounts. Each API has its own authentication, rate limits, and data model. Customer success managers spend 30 minutes per account review switching between tools.

**The Solution**: An MCP server that wraps all five APIs behind unified tools that answer customer-centric questions.

```python
"""customer_360.py -- Unified customer data MCP server."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class APIEndpoint:
    """Configuration for a third-party API."""
    name: str
    base_url: str
    api_key: str
    rate_limit_per_minute: int
    timeout_seconds: int = 10


@dataclass
class Customer360Server:
    """Unified customer view from multiple API sources."""
    apis: dict[str, APIEndpoint] = field(default_factory=dict)
    _cache: dict = field(default_factory=dict)

    def register_api(self, endpoint: APIEndpoint) -> None:
        """Register an API endpoint."""
        self.apis[endpoint.name] = endpoint

    def get_customer_summary(self, customer_email: str) -> dict:
        """Build a 360-degree customer summary from all sources."""
        # In production, these would be actual API calls
        return {
            "email": customer_email,
            "crm": self._get_crm_data(customer_email),
            "support": self._get_support_data(customer_email),
            "billing": self._get_billing_data(customer_email),
            "engagement": self._get_engagement_data(customer_email),
        }

    def _get_crm_data(self, email: str) -> dict:
        """Get CRM data from Salesforce."""
        return {
            "source": "salesforce",
            "account_status": "active",
            "plan": "enterprise",
            "mrr": 5000.0,
            "renewal_date": "2026-09-15",
        }

    def _get_support_data(self, email: str) -> dict:
        """Get support data from Zendesk."""
        return {
            "source": "zendesk",
            "open_tickets": 2,
            "avg_resolution_hours": 4.2,
            "satisfaction_score": 4.5,
        }

    def _get_billing_data(self, email: str) -> dict:
        """Get billing data from Stripe."""
        return {
            "source": "stripe",
            "current_period_amount": 5000.0,
            "payment_status": "current",
            "last_payment_date": "2026-03-01",
        }

    def _get_engagement_data(self, email: str) -> dict:
        """Get engagement data from Mixpanel."""
        return {
            "source": "mixpanel",
            "dau_last_30": 22,
            "feature_adoption": 0.73,
            "last_active": "2026-04-06",
        }

    def assess_health(self, summary: dict) -> dict:
        """Assess customer health from summary data. Pure logic."""
        score = 100
        risks = []

        # Support issues
        open_tickets = summary.get("support", {}).get("open_tickets", 0)
        if open_tickets > 3:
            score -= 20
            risks.append(f"{open_tickets} open support tickets")

        # Engagement drop
        dau = summary.get("engagement", {}).get("dau_last_30", 0)
        if dau < 5:
            score -= 30
            risks.append(f"Low engagement: {dau} active days in last 30")

        # Payment issues
        payment = summary.get("billing", {}).get("payment_status", "")
        if payment != "current":
            score -= 25
            risks.append(f"Payment status: {payment}")

        # Feature adoption
        adoption = summary.get("engagement", {}).get("feature_adoption", 0)
        if adoption < 0.3:
            score -= 15
            risks.append(f"Low feature adoption: {adoption:.0%}")

        health = "healthy" if score >= 70 else "at_risk" if score >= 40 else "critical"

        return {
            "health_score": max(0, score),
            "health_status": health,
            "risks": risks,
            "recommendation": self._get_recommendation(health, risks),
        }

    @staticmethod
    def _get_recommendation(health: str, risks: list) -> str:
        """Generate a recommendation based on health assessment."""
        if health == "healthy":
            return "No action needed. Consider upsell opportunity."
        if health == "at_risk":
            return f"Schedule check-in to address: {'; '.join(risks)}"
        return f"Immediate intervention required. Critical issues: {'; '.join(risks)}"
```

**Results**: Account review time dropped from 30 minutes to 3 minutes. At-risk customers are identified automatically, and the AI assistant generates action plans. Net revenue retention improved 8 percentage points in the first quarter.

### Case Study 3: Domain-Specific Tool Server (Specialized Computation)

**The Problem**: A biotech company needs to perform protein structure predictions, molecular docking simulations, and drug interaction checks. These computations require specialized libraries (AlphaFold, RDKit, Open Babel) that are difficult to install and configure. Researchers want to access these tools through their AI assistant without managing the computational environment.

**The Solution**: An MCP server that wraps the computational tools behind simple, well-documented tool interfaces, running on a GPU-equipped server.

```python
"""biotech_tools.py -- Biotech computation MCP server case study."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ComputeJob:
    """A computational job submitted to the server."""
    job_id: str
    job_type: str
    status: str = "pending"  # pending, running, completed, failed
    input_params: dict = field(default_factory=dict)
    result: Optional[dict] = None
    error: Optional[str] = None
    submitted_at: float = 0.0
    completed_at: float = 0.0
    compute_seconds: float = 0.0


@dataclass
class BiotechServer:
    """MCP server for biotech computations."""
    _jobs: dict[str, ComputeJob] = field(default_factory=dict)
    max_concurrent_jobs: int = 4
    _running_count: int = 0

    def submit_structure_prediction(
        self,
        sequence: str,
        model: str = "alphafold2",
    ) -> dict:
        """Submit a protein structure prediction job."""
        # Validate sequence (amino acid letters only)
        valid_aa = set("ACDEFGHIKLMNPQRSTVWY")
        invalid = set(sequence.upper()) - valid_aa
        if invalid:
            return {
                "error": f"Invalid amino acid characters: {invalid}. "
                         f"Use standard single-letter codes."
            }

        if len(sequence) > 2000:
            return {
                "error": f"Sequence too long ({len(sequence)} residues). "
                         f"Maximum is 2000 residues."
            }

        if self._running_count >= self.max_concurrent_jobs:
            return {
                "error": f"Server at capacity ({self.max_concurrent_jobs} jobs). "
                         f"Try again in a few minutes."
            }

        import time, secrets
        job_id = f"sp_{secrets.token_hex(8)}"
        job = ComputeJob(
            job_id=job_id,
            job_type="structure_prediction",
            status="pending",
            input_params={
                "sequence": sequence,
                "model": model,
                "length": len(sequence),
            },
            submitted_at=time.time(),
        )
        self._jobs[job_id] = job

        return {
            "job_id": job_id,
            "status": "submitted",
            "estimated_time_seconds": len(sequence) * 0.5,
            "message": f"Structure prediction submitted for {len(sequence)}-residue sequence",
        }

    def check_drug_interaction(
        self,
        drug_a: str,
        drug_b: str,
    ) -> dict:
        """Check for known interactions between two drugs."""
        # In production, queries a drug interaction database
        return {
            "drug_a": drug_a,
            "drug_b": drug_b,
            "interaction_found": False,
            "severity": "none",
            "evidence_level": "no_data",
            "recommendation": f"No known interaction between {drug_a} and {drug_b}.",
            "disclaimer": "This is a computational prediction. Consult a pharmacist.",
        }

    def get_job_status(self, job_id: str) -> dict:
        """Get the status of a submitted computation job."""
        job = self._jobs.get(job_id)
        if not job:
            return {"error": f"Job '{job_id}' not found"}
        return {
            "job_id": job.job_id,
            "job_type": job.job_type,
            "status": job.status,
            "submitted_at": job.submitted_at,
            "completed_at": job.completed_at if job.completed_at else None,
            "compute_seconds": job.compute_seconds if job.completed_at else None,
            "result": job.result,
            "error": job.error,
        }
```

**Results**: Researchers can now ask their AI assistant "What is the predicted structure of this 300-residue protein?" and get results back in minutes without managing computational environments. The MCP server handles queueing, GPU allocation, and result formatting. The number of predictions run per week tripled because the barrier to entry dropped from "install AlphaFold and configure GPU drivers" to "ask the AI."

---

## What's Next

Building an MCP server is the first step. The market is early -- as of April 2026, the registry has 10,000 servers but millions of potential use cases remain uncovered. The developers who build the best MCP servers today will own the tool layer of the AI economy.

Start with a domain you know well. Build a server that solves a real problem for you. Publish it. Iterate based on usage data. Monetize when you have traction. The MCP specification is stable, the SDKs are mature, and the client ecosystem (Claude, GPT, Cursor, VS Code) is actively integrating. The infrastructure is ready. The opportunity is now.

