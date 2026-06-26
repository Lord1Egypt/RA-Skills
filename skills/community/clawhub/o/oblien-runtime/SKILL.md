---
name: oblien-runtime
description: >-
  Complete Oblien workspace environment — what you are running inside (Firecracker microVM), how auth works (gateway JWT vs raw token), and the full Internal API reference: files, search, exec, terminal, and watcher on port 9990.
license: MIT
compatibility:
  - claude-code
  - cursor
  - openclaw
  - goose
  - jetbrains-ai
metadata:
  author: oblien
  version: 1.0.0
  source: https://oblien.com/docs
---

# Oblien Workspace Runtime

You are operating inside an **Oblien workspace** — an isolated Firecracker microVM with its own Linux kernel, filesystem, and network interface. This is not a container. You have full root access to a real Linux environment.

## What you can do

The workspace runs an **Internal API** — an HTTP server on port 9990 inside the VM. Through this API you can:

- **Read and write files** anywhere on the filesystem
- **Execute commands** synchronously or stream output in real-time via SSE
- **Search code** using ripgrep (content search) or filesystem search (filename matching)
- **Open interactive terminal sessions** over WebSocket (multiplexed PTY)
- **Watch for file changes** in real-time over WebSocket

## How authentication works

There are two ways to reach this API:

| Method | URL | Token | When to use |
|--------|-----|-------|-------------|
| **Gateway** | `https://workspace.oblien.com` | Gateway JWT (~1hr, signed) | Calling from outside — your app, CI, SDK |
| **Direct** | `http://10.x.x.x:9990` | Raw connection token (hex) | Calling from another workspace (lower latency) |

Gateway access requires `public_access: true` on the workspace network config. Direct access requires a private link between the two workspaces.

## Key facts

- The filesystem persists across restarts (writable overlay on top of the base image)
- Default working directory is `/root`
- Outbound internet is ON by default, inbound is OFF by default (network-dark)
- The workspace has dedicated CPU, memory, and disk — configured at creation time
- Port 9990 is the Internal API. Your application can use any other port.

---

The reference below covers every Internal API endpoint with parameters, response schemas, and code examples.

# Connection & Authentication

Before using the [Workspace Internal API](/docs/internal-api), the HTTP server inside the VM must be enabled. Once enabled, there are **two ways** to connect:

| Method | URL | Auth | Network requirement | Use case |
|--------|-----|------|---------------------|----------|
| **Gateway** | `workspace.oblien.com` | `Authorization: Bearer <gateway_jwt>` | [`public_access: true`](/docs/api/network#update-network) | External access - your app, SDK, CI, MCP |
| **Direct** | `10.x.x.x:9990` | `Authorization: Bearer <raw_token>` | [Private link](/docs/api/network#private-links) from caller | Workspace-to-workspace over private network |

Both methods hit the same server and the same endpoints. The difference is how you authenticate and how the request reaches the VM.

---

## Enable the server

Start the internal server via the [Oblien API](/docs/api/internal-api-access#enable-server). This returns a **Gateway JWT** for immediate use.


**SDK:**

```typescript

const client = new Oblien({
  clientId: process.env.OBLIEN_CLIENT_ID!,
  clientSecret: process.env.OBLIEN_CLIENT_SECRET!,
});

const access = await client.workspaces.apiAccess.enable('ws_a1b2c3d4');
console.log(access.token);   // Gateway JWT (eyJhbG...)
console.log(access.enabled); // true
```


**REST API:**

```http
POST https://api.oblien.com/workspace/ws_a1b2c3d4/internal-api-access/enable
X-Client-ID: your_client_id
X-Client-Secret: your_client_secret
```


**cURL:**

```bash
curl -X POST "https://api.oblien.com/workspace/ws_a1b2c3d4/internal-api-access/enable" \
  -H "X-Client-ID: $OBLIEN_CLIENT_ID" \
  -H "X-Client-Secret: $OBLIEN_CLIENT_SECRET"
```


> **Note:** Enable is **idempotent** - calling it on an already-enabled workspace returns a fresh JWT without restarting the server.


---

## Gateway connection

Use the **Gateway JWT** to access the workspace through `workspace.oblien.com`. The JWT embeds the VM's private IP and port - the gateway decodes it and routes your request to the correct VM automatically.

> **Warning:** The target workspace must have [`public_access: true`](/docs/api/network#update-network) in its network configuration. Without it, the gateway cannot reach the VM through the firewall. Enable it via the [Network API](/docs/api/network#update-network):

```typescript
await client.workspaces.network.update('ws_a1b2c3d4', { public_access: true });
```


**SDK:**

```typescript
// The SDK manages tokens automatically via client.workspaces.runtime()
const rt = await client.workspaces.runtime('ws_a1b2c3d4');

const files = await rt.files.list({ dirPath: '/app' });
const result = await rt.exec.run(['ls', '-la']);
await rt.terminal.create({ shell: '/bin/bash' });
```


**REST API:**

```http
GET https://workspace.oblien.com/files?path=/app
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
# HTTP
curl "https://workspace.oblien.com/files?path=/app" \
  -H "Authorization: Bearer $GATEWAY_JWT"

# WebSocket
wscat -c "wss://workspace.oblien.com/ws" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


> **Warning:** The URL is `workspace.oblien.com/endpoint` - **not** `workspace.oblien.com/ws_id/endpoint`. Routing is handled by the JWT payload, not the URL path.


### Token lifetime

The standard Gateway JWT expires after **~1 hour**. You have two options to manage this:

- **Rotate** - call [`rotateToken`](/docs/api/internal-api-access#rotate-token) or re-enable to get a fresh short-lived JWT
- **Force refresh** - use `client.workspaces.runtime(id, { force: true })` in the SDK to bypass the cached token

Both token types work the same way - `Authorization: Bearer <token>` against `workspace.oblien.com`. The only difference is expiry.

---

## Direct connection

For **workspace-to-workspace** communication, connect directly to the target VM's private IP. This bypasses the gateway entirely - lower latency, no JWT overhead.

### Setup flow

```
1. Enable the server on the target workspace
2. Create a private link from caller → target
3. Get the raw token + private IP of the target
4. Call the target directly from the calling workspace
```

### Step 1: Enable the target

```typescript
await client.workspaces.apiAccess.enable('ws_target');
```

### Step 2: Create a private link

Private links open a network path between two workspaces. Without a link, VMs cannot reach each other - they are **network-dark by default**. The link whitelists the caller's IP in the target workspace's firewall.

```typescript
await client.workspaces.network.update('ws_target', {
  private_link_ids: ['ws_caller'],
});
```

> **Note:** The `private_link_ids` field takes workspace IDs, not IPs. The platform resolves each ID to its internal IP and configures the target's firewall automatically. See [Private Links](/docs/api/network#private-links) for details.


### Step 3: Get the raw connection token

The raw token is a hex string used directly by the VM's auth middleware. Unlike the Gateway JWT, it doesn't embed routing info - you provide the IP yourself.

```typescript
const raw = await client.workspaces.apiAccess.rawToken('ws_target');

console.log(raw.token); // "a1b2c3d4e5f6..."
console.log(raw.ip);    // "10.0.1.42"
console.log(raw.port);  // 9990
```

See the full endpoint reference at [Raw token](/docs/api/internal-api-access#raw-token).

### Step 4: Call from the other workspace

From code running inside `ws_caller`, call `ws_target` directly over the private network:

```typescript
// Running inside ws_caller
const res = await fetch('http://10.0.1.42:9990/files?path=/app', {
  headers: { 'Authorization': `Bearer ${raw.token}` },
});
const files = await res.json();
```

```bash
curl "http://10.0.1.42:9990/exec" \
  -H "Authorization: Bearer a1b2c3d4e5f6..." \
  -H "Content-Type: application/json" \
  -d '{"cmd":["npm","test"]}'
```

> **Note:** Direct calls go **VM-to-VM** - no gateway, no JWT encoding/decoding overhead. This is the lowest-latency way to interact with a workspace.


---

## Disable the server

Stop the internal server, kill all sessions, and close connections.

```typescript
await client.workspaces.apiAccess.disable('ws_a1b2c3d4');
```

See the full endpoint reference at [Disable server](/docs/api/internal-api-access#disable-server).

---

## Token comparison

| | Gateway JWT | Raw Connection Token |
|---|---|---|
| **Use with** | `workspace.oblien.com` | Direct `10.x.x.x:9990` |
| **Auth header** | `Authorization: Bearer <jwt>` | `Authorization: Bearer <raw_token>` |
| **Lifetime** | ~1 hour (standard) or 30 days (workspace token) | Until rotated |
| **Contains VM IP** | Yes (embedded in JWT) | No (you get the IP separately) |
| **How to get** | [`enable`](/docs/api/internal-api-access#enable-server) / [`rotateToken`](/docs/api/internal-api-access#rotate-token) | [`rawToken`](/docs/api/internal-api-access#raw-token) |
| **When to use** | External access - apps, SDK, CI, MCP | Workspace-to-workspace orchestration |

---

## Full API access reference

All server management endpoints are on the [Oblien API](/docs/api/internal-api-access) at `api.oblien.com`:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/workspace/:id/internal-api-access` | `GET` | [Server status](/docs/api/internal-api-access#server-status) |
| `/workspace/:id/internal-api-access/enable` | `POST` | [Enable server](/docs/api/internal-api-access#enable-server) |
| `/workspace/:id/internal-api-access/disable` | `POST` | [Disable server](/docs/api/internal-api-access#disable-server) |
| `/workspace/:id/internal-api-access/token` | `POST` | [Rotate token](/docs/api/internal-api-access#rotate-token) |
| `/workspace/:id/internal-api-access/token/raw` | `GET` | [Raw token + IP](/docs/api/internal-api-access#raw-token) |
| `/workspace/:id/internal-api-access/reconnect` | `POST` | [Reconnect](/docs/api/internal-api-access#reconnect) |
| `/workspace/:id/internal-api-access/workspace` | `POST` | [30-day token](/docs/api/internal-api-access#workspace-access-token) |

---

# Files

The file system endpoints let you list, read, write, and delete files inside the workspace VM. All paths are absolute filesystem paths (e.g. `/app/src/main.go`).

> **Note:** Requires the internal server to be [enabled](/docs/internal-api/server-setup#enable-the-server). All requests require a valid token - see [Connection & Auth](/docs/internal-api/server-setup).


## List directory

List files and directories in a given path. Supports recursive traversal, content inclusion, hash computation, and filtering.


**SDK:**

```typescript
const rt = await client.workspaces.runtime('ws_a1b2c3d4');

const result = await rt.files.list({
  dirPath: '/app/src',
  nested: true,
  flatten: true,
  includeContent: true,
  codeFilesOnly: true,
  maxDepth: 5,
});

console.log(result.entries);       // fileEntry[]
console.log(result.count);         // number of entries
```


**REST API:**

```http
GET https://workspace.oblien.com/files?path=/app/src&nested=true&flatten=true&include_content=true&code_files_only=true&max_depth=5
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl "https://workspace.oblien.com/files?path=/app/src&nested=true&flatten=true&include_content=true&code_files_only=true&max_depth=5" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | `string` | No | Directory path to list. Defaults to `/` |
| `nested` | `boolean` | No | Recurse into subdirectories. Default `false` |
| `flatten` | `boolean` | No | Return flat list instead of tree. Default `false` |
| `light` | `boolean` | No | Omit size and modified time for faster response. Default `false` |
| `include_hash` | `boolean` | No | Include SHA-256 hash for each file. Default `false` |
| `include_content` | `boolean` | No | Include file content inline. Default `false` |
| `include_extensions` | `boolean` | No | Include file extension field. Default `false` |
| `code_files_only` | `boolean` | No | Only return code/config files. Default `false` |
| `use_gitignore` | `boolean` | No | Respect `.gitignore` rules. Default `true` |
| `max_depth` | `integer` | No | Maximum recursion depth. Default `20` |
| `path_filter` | `string` | No | Case-insensitive substring filter on path |
| `include_ext` | `string` | No | Comma-separated extensions to include (e.g. `js,ts,go`) |
| `ignore_patterns` | `string` | No | Comma-separated glob patterns to ignore |
| `max_content_budget` | `integer` | No | Max total bytes for inline content. Default ~50 MiB |

### Response

```json
{
  "success": true,
  "path": "/app/src",
  "entries": [
    {
      "name": "main.go",
      "path": "/app/src/main.go",
      "type": "file",
      "size": 1234,
      "modified": "2025-01-15T10:30:00Z",
      "extension": ".go",
      "content": "package main\n...",
      "hash": "a1b2c3..."
    },
    {
      "name": "utils",
      "path": "/app/src/utils",
      "type": "directory",
      "children": [...]
    }
  ],
  "count": 42
}
```

> **Warning:** The list endpoint is capped at **50,000 entries**. For large directories, use `path_filter`, `include_ext`, or `code_files_only` to narrow results, or use the [stream endpoint](#stream-directory) for NDJSON streaming.


---

## Stream directory

Stream directory entries as **NDJSON** (newline-delimited JSON). Ideal for large directories - entries flow to the client as they're discovered, without accumulating in memory.


**SDK:**

```typescript
for await (const entry of rt.files.stream({
  dirPath: '/app',
  includeContent: true,
  codeFilesOnly: true,
})) {
  console.log(entry.name, entry.path);
}
```


**REST API:**

```http
GET https://workspace.oblien.com/files/stream?path=/app&include_content=true&code_files_only=true
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```

Response: `Content-Type: application/x-ndjson`


**cURL:**

```bash
curl -N "https://workspace.oblien.com/files/stream?path=/app&include_content=true&code_files_only=true" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Parameters

Same as [List directory](#list-directory). The `nested` and `flatten` options are always enabled for streaming.

### Response format

Each line is a JSON object. The stream starts with a `start` event and ends with a `done` event:

```jsonl
{"event":"start","path":"/app"}
{"name":"main.go","path":"/app/main.go","type":"file","size":1234}
{"name":"utils.go","path":"/app/utils.go","type":"file","size":567}
{"event":"done","count":2}
```

> **Note:** The stream endpoint uses **batched directory reads** for memory efficiency. Entries are not sorted - they arrive in filesystem order. Use the list endpoint if you need sorted output.


---

## Read file

Read the content of a file. Supports line ranges for partial reads.


**SDK:**

```typescript
const file = await rt.files.read({
  filePath: '/app/src/main.go',
});

console.log(file.content);    // file content as string
console.log(file.lines);      // number of lines returned
console.log(file.size);       // file size in bytes

// Read specific line range
const partial = await rt.files.read({
  filePath: '/app/src/main.go',
  startLine: 10,
  endLine: 25,
  withLineNumbers: true,
});
```


**REST API:**

```http
GET https://workspace.oblien.com/files/read?path=/app/src/main.go&start_line=10&end_line=25&with_line_numbers=true
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl "https://workspace.oblien.com/files/read?path=/app/src/main.go&start_line=10&end_line=25&with_line_numbers=true" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | `string` | Yes | Absolute path to the file |
| `start_line` | `integer` | No | First line to read (1-based) |
| `end_line` | `integer` | No | Last line to read (1-based, inclusive) |
| `with_line_numbers` | `boolean` | No | Prefix each line with its line number |

### Response

```json
{
  "success": true,
  "path": "/app/src/main.go",
  "content": "package main\n\nfunc main() {\n\tfmt.Println(\"hello\")\n}",
  "size": 1234,
  "lines": 5,
  "extension": ".go",
  "start_line": 10,
  "end_line": 25
}
```

`start_line` and `end_line` are only included when a line range was requested.

---

## Write file

Create or overwrite a file. Uses atomic write (temp file + rename) by default. Accepts both `POST` and `PUT`.


**SDK:**

```typescript
const result = await rt.files.write({
  fullPath: '/app/src/hello.txt',
  content: 'Hello, world!',
  createDirs: true,
});

console.log(result.path);  // "/app/src/hello.txt"
console.log(result.size);  // 13

// Append to an existing file
await rt.files.write({
  fullPath: '/app/logs/output.log',
  content: 'New log entry\n',
  append: true,
  createDirs: true,
});
```


**REST API:**

```http
POST https://workspace.oblien.com/files/write
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "path": "/app/src/hello.txt",
  "content": "Hello, world!",
  "create_dirs": true
}
```


**cURL:**

```bash
curl -X POST "https://workspace.oblien.com/files/write" \
  -H "Authorization: Bearer $GATEWAY_JWT" \
  -H "Content-Type: application/json" \
  -d '{"path":"/app/src/hello.txt","content":"Hello, world!","create_dirs":true}'
```


### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | `string` | Yes | Absolute path for the file |
| `content` | `string` | Yes | File content |
| `create_dirs` | `boolean` | No | Create parent directories if they don't exist. Default `false` |
| `append` | `boolean` | No | Append to existing file instead of overwriting. Default `false` |
| `mode` | `string` | No | File permissions in octal (e.g. `"0644"`). Default `"0644"` |

### Response

```json
{
  "success": true,
  "path": "/app/src/hello.txt",
  "size": 13
}
```

HTTP status: `201 Created`

---

## Create directory

Create a directory and any necessary parent directories.


**SDK:**

```typescript
await rt.files.mkdir({
  path: '/app/src/utils/helpers',
});
```


**REST API:**

```http
POST https://workspace.oblien.com/files/mkdir
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "path": "/app/src/utils/helpers"
}
```


**cURL:**

```bash
curl -X POST "https://workspace.oblien.com/files/mkdir" \
  -H "Authorization: Bearer $GATEWAY_JWT" \
  -H "Content-Type: application/json" \
  -d '{"path":"/app/src/utils/helpers"}'
```


### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | `string` | Yes | Directory path to create |
| `mode` | `string` | No | Directory permissions in octal (e.g. `"0755"`). Default `"0755"` |

### Response

```json
{
  "success": true,
  "path": "/app/src/utils/helpers"
}
```

HTTP status: `201 Created`

---

## Stat

Get detailed information about a file or directory.


**SDK:**

```typescript
const info = await rt.files.stat({
  path: '/app/src/main.go',
});

console.log(info.type);        // "file"
console.log(info.size);        // 1234
console.log(info.permissions); // "0644"
console.log(info.is_code);     // true
```


**REST API:**

```http
GET https://workspace.oblien.com/files/stat?path=/app/src/main.go
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl "https://workspace.oblien.com/files/stat?path=/app/src/main.go" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | `string` | Yes | Path to the file or directory |

### Response

```json
{
  "success": true,
  "path": "/app/src/main.go",
  "name": "main.go",
  "type": "file",
  "size": 1234,
  "modified": "2025-01-15T10:30:00Z",
  "permissions": "0644",
  "is_code": true,
  "extension": ".go"
}
```

For symlinks:

```json
{
  "success": true,
  "path": "/app/link",
  "name": "link",
  "type": "symlink",
  "size": 0,
  "modified": "2025-01-15T10:30:00Z",
  "permissions": "0777",
  "is_code": false,
  "symlink_target": "/app/src/main.go"
}
```

---

## Delete

Delete a file or directory. Directories are removed recursively.


**SDK:**

```typescript
await rt.files.delete({
  path: '/app/src/old-file.txt',
});
```


**REST API:**

```http
DELETE https://workspace.oblien.com/files/delete?path=/app/src/old-file.txt
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl -X DELETE "https://workspace.oblien.com/files/delete?path=/app/src/old-file.txt" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | `string` | Yes | Path to the file or directory to delete |

The path can also be provided in the request body as `{"path": "..."}`.

### Response

```json
{
  "success": true,
  "path": "/app/src/old-file.txt"
}
```

> **Warning:** System paths (`/`, `/bin`, `/sbin`, `/usr`, `/lib`, `/lib64`, `/etc`, `/dev`, `/proc`, `/sys`, `/boot`, `/run`) are protected and cannot be deleted.


---

## Error responses

All file endpoints return errors in a consistent format:

```json
{
  "error": "file not found: /app/missing.txt"
}
```

| Status | Meaning |
|--------|---------|
| `400` | Invalid parameters (missing path, path is a directory when file expected, etc.) |
| `401` | Missing or invalid token |
| `403` | Attempted to delete a protected system path |
| `404` | File or directory not found |
| `413` | File too large to read or content too large to write |
| `500` | Internal server error |

---

# Search

Two search modes are available inside the workspace:

- **Content search** - powered by [ripgrep](https://github.com/BurntSushi/ripgrep), searches file contents with regex, whole-word, and context line support
- **Filename search** - built-in filesystem search that matches against file paths

> **Note:** Requires the internal server to be [enabled](/docs/internal-api/server-setup#enable-the-server). Content search requires ripgrep - use the [install endpoint](#install-ripgrep) to set it up.


---

## Content search

Search file contents using ripgrep. Results are grouped by file with line numbers and match context.


**SDK:**

```typescript
const rt = await client.workspaces.runtime('ws_a1b2c3d4');

const results = await rt.search.content({
  query: 'handleRequest',
  path: '/app/src',
  contextLines: 2,
  maxResults: 100,
});

for (const file of results.results) {
  console.log(file.path);
  for (const match of file.matches) {
    console.log(`  Line ${match.line}: ${match.text}`);
  }
}
```


**REST API:**

```http
GET https://workspace.oblien.com/files/search?q=handleRequest&path=/app/src&context_lines=2&max_results=100
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl "https://workspace.oblien.com/files/search?q=handleRequest&path=/app/src&context_lines=2&max_results=100" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | `string` | Yes | Search query (max 1000 characters) |
| `path` | `string` | No | Directory or file to search in. Default `/` |
| `case_sensitive` | `boolean` | No | Case-sensitive matching. Default `false` |
| `regex` | `boolean` | No | Treat query as a regex pattern. Default `false` |
| `whole_word` | `boolean` | No | Match whole words only. Default `false` |
| `max_results` | `integer` | No | Maximum number of matches. Default `100` |
| `timeout` | `integer` | No | Timeout in seconds (max 60). Default `10` |
| `context_lines` | `integer` | No | Lines of context around matches (0–10). Default `0` |
| `file_types` | `string` | No | Comma-separated file extension filters (e.g. `go,js,py`). Converted to glob patterns internally |
| `include_hidden` | `boolean` | No | Include hidden files/directories. Default `false` |
| `no_gitignore` | `boolean` | No | Ignore `.gitignore` rules. Default `false` |
| `ignore_patterns` | `string` | No | Comma-separated glob patterns to skip |

### Response

Results are returned as an **object keyed by file path**, with each value being an array of matches:

```json
{
  "success": true,
  "query": "handleRequest",
  "path": "/app/src",
  "results": {
    "src/server.go": [
      {
        "line": 42,
        "column": 6,
        "text": "func handleRequest(w http.ResponseWriter, r *http.Request) {"
      },
      {
        "line": 105,
        "column": 2,
        "text": "\thandleRequest(w, r)"
      }
    ],
    "src/router.go": [
      {
        "line": 18,
        "column": 12,
        "text": "\trouter.HandleFunc(\"/\", handleRequest)"
      }
    ]
  },
  "total_matches": 3,
  "total_files": 2,
  "capped": false
}
```

| Field | Description |
|-------|-------------|
| `results` | Object mapping file paths to arrays of matches |
| `total_matches` | Total number of matching lines across all files |
| `total_files` | Number of files with at least one match |
| `capped` | `true` if `max_results` was reached before all matches were found |

---

## Filename search

Search for files by name. Uses a fast filesystem walk with substring matching on relative paths.


**SDK:**

```typescript
const results = await rt.search.files({
  query: 'controller',
  path: '/app/src',
  maxResults: 50,
});

console.log(results.files);        // ["auth/controller.go", "user/controller.go"]
console.log(results.total_files);  // 2
```


**REST API:**

```http
GET https://workspace.oblien.com/files/search/files?q=controller&path=/app/src&max_results=50
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl "https://workspace.oblien.com/files/search/files?q=controller&path=/app/src&max_results=50" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `q` | `string` | Yes | Search query - matches against relative file paths (max 1000 characters) |
| `path` | `string` | No | Directory to search in. Default `/` |
| `case_sensitive` | `boolean` | No | Case-sensitive matching. Default `false` |
| `include_hidden` | `boolean` | No | Include hidden files/directories. Default `false` |
| `max_results` | `integer` | No | Maximum number of results. Default `200` |
| `ignore_patterns` | `string` | No | Comma-separated glob patterns to skip |

### Response

```json
{
  "success": true,
  "query": "controller",
  "path": "/app/src",
  "files": [
    "auth/controller.go",
    "user/controller.go"
  ],
  "total_files": 2
}
```

> **Note:** Filename search does **not** require ripgrep - it works out of the box with no additional setup.


---

## Ripgrep status

Check if ripgrep is installed and available for content search.


**SDK:**

```typescript
const status = await rt.search.status();
console.log(status.installed); // true or false
console.log(status.version);   // "ripgrep 14.1.0" or null
```


**REST API:**

```http
GET https://workspace.oblien.com/files/search/init
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl "https://workspace.oblien.com/files/search/init" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Response

When ripgrep is installed:

```json
{
  "success": true,
  "installed": true,
  "path": "/usr/local/bin/rg",
  "version": "ripgrep 14.1.0"
}
```

When not installed:

```json
{
  "success": true,
  "installed": false,
  "message": "ripgrep is not installed - use POST /files/search/init to install"
}
```

---

## Install ripgrep

Download and install ripgrep from GitHub releases. This is a one-time setup per workspace.


**SDK:**

```typescript
const result = await rt.search.init();
console.log(result.installed); // true
console.log(result.version);   // "14.1.1"
```


**REST API:**

```http
POST https://workspace.oblien.com/files/search/init
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl -X POST "https://workspace.oblien.com/files/search/init" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Response

```json
{
  "success": true,
  "version": "ripgrep 14.1.0",
  "path": "/usr/local/bin/rg"
}
```

If ripgrep is already installed, the endpoint returns the current installation info without re-downloading.

> **Warning:** Installation requires internet access from inside the workspace to download from GitHub releases. The binary is installed to `/usr/local/bin/rg`.


---

## Error responses

| Status | Meaning |
|--------|---------|
| `400` | Missing `q` parameter, query too long, or path is not a directory |
| `401` | Missing or invalid token |
| `404` | Search path not found |
| `409` | Ripgrep installation already in progress |
| `503` | Content search requested but ripgrep is not installed |
| `504` | Search timed out |

---

# Command Execution

The exec endpoints let you run commands inside the workspace VM. Commands can run synchronously (wait for result) or asynchronously (stream output via SSE). Long-running tasks persist in the background and can be polled, streamed, or killed.

> **Note:** Requires the internal server to be [enabled](/docs/internal-api/server-setup#enable-the-server).


## Overview

Two execution modes:

| Mode | How | Use case |
|------|-----|----------|
| **Synchronous** | `POST /exec` (no `stream` flag) | Quick commands - get stdout/stderr in response |
| **Streaming** | `POST /exec` with `stream: true`, or `GET /exec/stream?task_id=ID` | Long-running tasks - real-time output via SSE |

---

## Run command

Execute a command inside the workspace.


**SDK:**

```typescript
// Synchronous - wait for result
const rt = await client.workspaces.runtime('ws_a1b2c3d4');
const result = await rt.exec.run(['echo', 'hello']);

console.log(result.exit_code);  // 0
console.log(result.stdout);     // "hello\n"
console.log(result.stderr);     // ""
```

```typescript
// Streaming - real-time output via async generator
for await (const ev of rt.exec.stream(['npm', 'install'])) {
  if (ev.event === 'stdout') process.stdout.write(atob(ev.data));
  if (ev.event === 'stderr') process.stderr.write(atob(ev.data));
  if (ev.event === 'exit') console.log(`Done: ${ev.exit_code}`);
}
```


**REST API:**

**Synchronous:**

```http
POST https://workspace.oblien.com/exec
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "cmd": ["echo", "hello"]
}
```

**Streaming (SSE):**

```http
POST https://workspace.oblien.com/exec
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "cmd": ["npm", "install"],
  "stream": true
}
```


**cURL:**

```bash
# Synchronous
curl -X POST "https://workspace.oblien.com/exec" \
  -H "Authorization: Bearer $GATEWAY_JWT" \
  -H "Content-Type: application/json" \
  -d '{"cmd": ["echo", "hello"]}'

# Streaming (SSE)
curl -N -X POST "https://workspace.oblien.com/exec" \
  -H "Authorization: Bearer $GATEWAY_JWT" \
  -H "Content-Type: application/json" \
  -d '{"cmd": ["npm", "install"], "stream": true}'
```


### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cmd` | `string[]` | Yes | The command to execute as an array (e.g. `["node", "app.js"]`) |
| `stream` | `boolean` | No | If `true`, returns SSE stream instead of waiting |
| `exec_mode` | `string` | No | `auto` (default), `shell`, or `direct` |
| `timeout_seconds` | `integer` | No | Kill command after N seconds. Default `0` (no timeout) |
| `ttl_seconds` | `integer` | No | Keep task metadata for N seconds after exit. Default `0` (uses 5-minute server default). Set to `-1` to never expire |
| `keep_logs` | `boolean` | No | Retain stdout/stderr after completion. Default `false` |

### Execution modes

| Mode | Behavior |
|------|----------|
| `auto` | Uses shell if `cmd` contains shell metacharacters (`\|`, `&`, `;`, etc.), otherwise runs directly |
| `shell` | Always wraps in `/bin/sh -c "..."` |
| `direct` | Splits and runs directly - no shell interpretation |

### Synchronous response

The response is the full task object:

```json
{
  "id": "abc123",
  "command": ["echo", "hello"],
  "status": "exited",
  "guest_pid": 4521,
  "exit_code": 0,
  "stdout": "hello\n",
  "stderr": "",
  "created_at": "2025-01-15T10:30:00Z",
  "started_at": "2025-01-15T10:30:00Z",
  "exited_at": "2025-01-15T10:30:01Z",
  "ttl_seconds": 300
}
```

### Streaming response (SSE)

When `stream: true`, the response is an SSE stream. The data payloads are JSON. stdout/stderr content is **base64-encoded**:

```
event: task_id
data: {"task_id":"abc123"}

event: stdout
data: {"data":"SW5zdGFsbGluZyBkZXBlbmRlbmNpZXMuLi4="}

event: stderr
data: {"data":"bnBtIHdhcm4gZGVwcmVjYXRlZA=="}

event: exit
data: {"exit_code": 0, "pid": 4521}
```

| Event | Data format | Description |
|-------|-------------|-------------|
| `task_id` | `{"task_id": "..."}` | Task identifier for future polling |
| `stdout` | `{"data": "..."}` | Standard output chunk (base64-encoded) |
| `stderr` | `{"data": "..."}` | Standard error chunk (base64-encoded) |
| `exit` | `{"exit_code": N, "pid": N}` | Process finished |

---

## List tasks

List all tracked tasks.


**SDK:**

```typescript
const tasks = await rt.exec.list();

for (const task of tasks) {
  console.log(`${task.id}: ${task.command.join(' ')} (status: ${task.status})`);
}
```


**REST API:**

```http
GET https://workspace.oblien.com/exec
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl "https://workspace.oblien.com/exec" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Response

```json
{
  "success": true,
  "tasks": [
    {
      "id": "abc123",
      "command": ["npm", "install"],
      "status": "running",
      "guest_pid": 4521,
      "created_at": "2025-01-15T10:30:00Z",
      "started_at": "2025-01-15T10:30:00Z",
      "ttl_seconds": 300
    }
  ]
}
```

Task status values: `pending`, `running`, `exited`, `failed`.

---

## Get task

Get the status and output of a specific task.


**SDK:**

```typescript
const task = await rt.exec.get('abc123');

console.log(task.status);     // "exited"
console.log(task.exit_code);  // 0
console.log(task.stdout);     // "full output..."
```


**REST API:**

```http
GET https://workspace.oblien.com/exec/abc123
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl "https://workspace.oblien.com/exec/abc123" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Response

```json
{
  "id": "abc123",
  "command": ["npm", "install"],
  "status": "exited",
  "guest_pid": 4521,
  "exit_code": 0,
  "stdout": "added 150 packages in 12s\n",
  "stderr": "",
  "created_at": "2025-01-15T10:30:00Z",
  "started_at": "2025-01-15T10:30:00Z",
  "exited_at": "2025-01-15T10:30:12Z",
  "ttl_seconds": 300
}
```

---

## Kill task

Remove a task from tracking and close its stdin pipe.


**SDK:**

```typescript
await rt.exec.kill('abc123');
```


**REST API:**

```http
DELETE https://workspace.oblien.com/exec/abc123
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl -X DELETE "https://workspace.oblien.com/exec/abc123" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Response

```json
{
  "success": true
}
```

---

## Delete all tasks

Remove all tasks from tracking and close stdin pipes.


**REST API:**

```http
DELETE https://workspace.oblien.com/exec
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl -X DELETE "https://workspace.oblien.com/exec" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Response

```json
{
  "success": true,
  "deleted": 3
}
```

---

## Send stdin

Send input to a running task's stdin. The request body is sent as **raw bytes** (not JSON).


**SDK:**

```typescript
await rt.exec.input('abc123', 'yes\n');
```


**REST API:**

```http
POST https://workspace.oblien.com/exec/abc123/input
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/octet-stream

yes
```


**cURL:**

```bash
curl -X POST "https://workspace.oblien.com/exec/abc123/input" \
  -H "Authorization: Bearer $GATEWAY_JWT" \
  --data-binary 'yes
'
```


### Response

```json
{
  "success": true,
  "bytes_written": 4
}
```

---

## Stream output (SSE)

Subscribe to real-time output from a running task. This is useful when you started a task with `stream: false` or from another client and want to attach to its output.


**SDK:**

```typescript
for await (const ev of rt.exec.subscribe('abc123')) {
  if (ev.event === 'stdout') process.stdout.write(atob(ev.data));
  if (ev.event === 'stderr') process.stderr.write(atob(ev.data));
  if (ev.event === 'exit') console.log(`Exited: ${ev.exit_code}`);
}
```


**REST API:**

```http
GET https://workspace.oblien.com/exec/stream?task_id=abc123
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Accept: text/event-stream
```

Or create and stream a new task via POST (alias for `POST /exec` with `stream: true`):

```http
POST https://workspace.oblien.com/exec/stream
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "cmd": ["npm", "install"]
}
```


**cURL:**

```bash
curl -N "https://workspace.oblien.com/exec/stream?task_id=abc123" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### SSE events

```
event: stdout
data: {"data":"SW5zdGFsbGluZyBkZXBlbmRlbmNpZXMuLi4="}

event: stderr
data: {"data":"bnBtIHdhcm4gZGVwcmVjYXRlZA=="}

event: exit
data: {"exit_code": 0, "pid": 4521}
```

When subscribing to a task that has already finished, the server sends an `output` event with buffered stdout/stderr as raw text, then the `exit` event.

---

## Error responses

| Status | Meaning |
|--------|---------|
| `400` | Missing `cmd` field or invalid parameters |
| `401` | Missing or invalid token |
| `404` | Task not found |
| `405` | Method not allowed |
| `429` | Too many tasks (max 50 concurrent) |
| `500` | Failed to start process |

---

# Terminal Sessions

The terminal endpoints let you create interactive PTY sessions inside the workspace VM. Terminal I/O is multiplexed over a single WebSocket connection.

> **Note:** Requires the internal server to be [enabled](/docs/internal-api/server-setup#enable-the-server). Up to **10 concurrent terminal sessions** per workspace.


## Overview

```
1. Create a terminal session  →  get session ID
2. Open WebSocket at /ws      →  bidirectional I/O
3. Send stdin as binary       →  [id_byte][data]
4. Receive stdout as binary   →  [id_byte][data]
5. Resize / close via JSON messages or REST
```

---

## Create session

Create a new terminal session with an interactive PTY.


**SDK:**

```typescript
const rt = await client.workspaces.runtime('ws_a1b2c3d4');

const term = await rt.terminal.create({
  shell: '/bin/bash',
  cols: 120,
  rows: 40,
});

console.log(term.id);      // "1"
console.log(term.cols);    // 120
console.log(term.rows);    // 40
```


**REST API:**

```http
POST https://workspace.oblien.com/terminals
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "cmd": ["/bin/bash"],
  "cols": 120,
  "rows": 40
}
```


**cURL:**

```bash
curl -X POST "https://workspace.oblien.com/terminals" \
  -H "Authorization: Bearer $GATEWAY_JWT" \
  -H "Content-Type: application/json" \
  -d '{"cmd":["/bin/bash"],"cols":120,"rows":40}'
```


### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `cmd` | `string[]` | No | Command to run (e.g. `["/bin/bash"]`). Falls back to default shell |
| `command` | `string[]` | No | Alias for `cmd` |
| `cols` | `integer` | No | Terminal width in columns |
| `rows` | `integer` | No | Terminal height in rows |

### Response

```json
{
  "success": true,
  "id": "1",
  "cols": 120,
  "rows": 40,
  "command": ["/bin/bash"]
}
```

HTTP status: `201 Created`

---

## List sessions

List all active terminal sessions.


**SDK:**

```typescript
const sessions = await rt.terminal.list();

for (const term of sessions) {
  console.log(`${term.id}: ${term.command.join(' ')} (alive: ${term.alive})`);
}
```


**REST API:**

```http
GET https://workspace.oblien.com/terminals
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl "https://workspace.oblien.com/terminals" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Response

```json
{
  "success": true,
  "terminals": [
    {
      "id": "1",
      "command": ["/bin/bash"],
      "cols": 120,
      "rows": 40,
      "alive": true,
      "exit_code": 0,
      "created_at": "2025-01-15T10:30:00Z"
    }
  ]
}
```

---

## Close session

Close a terminal session and kill its process.


**SDK:**

```typescript
await rt.terminal.close('1');
```


**REST API:**

```http
DELETE https://workspace.oblien.com/terminals/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl -X DELETE "https://workspace.oblien.com/terminals/1" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Response

```json
{
  "success": true,
  "terminal_id": "1"
}
```

---

## Get scrollback

Retrieve the scrollback buffer for a terminal session. Useful for restoring terminal state after reconnection.


**SDK:**

```typescript
const scrollback = await rt.terminal.scrollback('1');

console.log(scrollback.size);       // bytes in buffer
console.log(scrollback.alive);      // session still running
console.log(scrollback.scrollback); // base64-encoded data
```


**REST API:**

```http
GET https://workspace.oblien.com/terminals/1/scrollback
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl "https://workspace.oblien.com/terminals/1/scrollback" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Response

```json
{
  "success": true,
  "scrollback": "dXNlckBzYW5kYm94Oi9hcHAkIA==",
  "size": 2048,
  "alive": true,
  "exit_code": 0
}
```

| Field | Description |
|-------|-------------|
| `scrollback` | Base64-encoded terminal output (64 KiB ring buffer) |
| `size` | Size of the scrollback data in bytes |
| `alive` | Whether the session is still running |
| `exit_code` | Process exit code (0 if still alive) |

---

## WebSocket

Terminal I/O flows over a single multiplexed WebSocket connection at `/ws`. Multiple terminal sessions share the same connection.

### Connect


**SDK:**

```typescript
// Create a terminal session
const term = await rt.terminal.create({ shell: '/bin/bash' });

// Open a RuntimeWebSocket for bidirectional I/O
const ws = rt.ws();

ws.onTerminalOutput((id, data) => {
  process.stdout.write(data);
});

ws.onClose(() => console.log('WebSocket closed'));

await ws.connect();
ws.writeTerminalInput(term.id, 'ls -la\n');
ws.resizeTerminal(term.id, 160, 50);
```


**REST API:**

```
WebSocket: wss://workspace.oblien.com/ws
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**JavaScript:**

```javascript
const ws = new WebSocket('wss://workspace.oblien.com/ws', {
  headers: { Authorization: `Bearer ${gatewayJwt}` },
});

ws.binaryType = 'arraybuffer';

ws.onmessage = (event) => {
  if (event.data instanceof ArrayBuffer) {
    // Binary: terminal output
    const bytes = new Uint8Array(event.data);
    const terminalId = bytes[0];
    const data = bytes.slice(1);
    console.log(`Terminal ${terminalId}:`, new TextDecoder().decode(data));
  } else {
    // Text: control messages (exit, etc.)
    const msg = JSON.parse(event.data);
    console.log('Control:', msg);
  }
};
```


### Protocol

#### Binary frames

| Direction | Format | Description |
|-----------|--------|-------------|
| Client → Server | `[id_byte][stdin_data]` | Send input to terminal |
| Server → Client | `[id_byte][stdout_data]` | Receive output from terminal |

The first byte is the terminal ID byte (mapped from the session ID). The remaining bytes are raw terminal data.

#### Text frames

**Resize a terminal:**

```json
{
  "channel": "terminal",
  "type": "resize",
  "id": "1",
  "cols": 160,
  "rows": 50
}
```

**Terminal exit notification (server → client):**

```json
{
  "channel": "terminal",
  "type": "exit",
  "id": "1",
  "code": 0
}
```

### On connect

When a WebSocket connection is established, the server automatically sends:

1. **Scrollback data** - binary frames with buffered output for each active session
2. **Exit notifications** - text frames for any sessions that have already exited

This allows clients to restore terminal state after reconnection without explicit scrollback requests.

---

## Error responses

| Status | Meaning |
|--------|---------|
| `400` | Missing terminal ID |
| `401` | Missing or invalid token |
| `404` | Terminal session not found |
| `405` | Method not allowed |
| `500` | Failed to create PTY session |

---

# File Watcher

Watch directories for file system changes in real time. The watcher monitors filesystem events and streams them over the [WebSocket connection](/docs/internal-api/terminal#websocket) at `/ws`.

> **Note:** Requires the internal server to be [enabled](/docs/internal-api/server-setup#enable-the-server). Up to **5 concurrent watchers** per workspace.


## Overview

```
1. Create a watcher via REST    →  get watcher ID
2. Open WebSocket at /ws        →  receive "ready" event
3. File changes in watched dir  →  receive "change" events
4. Delete watcher when done     →  cleanup
```

Watcher events arrive as **JSON text frames** on the `"watcher"` channel of the same WebSocket used for [terminal I/O](/docs/internal-api/terminal#websocket).

---

## Create watcher

Start watching a directory for changes. The watcher recursively monitors all subdirectories and streams events over the WebSocket.


**SDK:**

```typescript
const rt = await client.workspaces.runtime('ws_a1b2c3d4');

const watcher = await rt.watcher.create({
  path: '/app/src',
  excludes: ['*.log', 'tmp'],
});

console.log(watcher.id);   // "1"
console.log(watcher.root); // "/app/src"
console.log(watcher.dirs); // 42
```


**REST API:**

```http
POST https://workspace.oblien.com/watchers
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
Content-Type: application/json

{
  "path": "/app/src",
  "excludes": ["*.log", "tmp"]
}
```


**cURL:**

```bash
curl -X POST "https://workspace.oblien.com/watchers" \
  -H "Authorization: Bearer $GATEWAY_JWT" \
  -H "Content-Type: application/json" \
  -d '{"path": "/app/src", "excludes": ["*.log", "tmp"]}'
```


### Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | `string` | Yes | Directory to watch (recursively) |
| `excludes` | `string[]` | No | Glob patterns to exclude (merged with defaults) |

### Response

```json
{
  "id": "1",
  "root": "/app/src",
  "dirs": 42,
  "excludes": ["node_modules", ".git", "*.log", "tmp"]
}
```

### Default excludes

These patterns are always excluded, even if you don't specify any:

```
node_modules, .git, .svn, .hg, __pycache__, .pytest_cache,
.mypy_cache, .next, .nuxt, dist, build, .DS_Store, *.swp, *.swo, *~
```

Your custom `excludes` are merged with these defaults.

---

## List watchers

Get all active watchers.


**SDK:**

```typescript
const watchers = await rt.watcher.list();

for (const w of watchers) {
  console.log(`${w.id}: watching ${w.root} (${w.dirs} dirs)`);
}
```


**REST API:**

```http
GET https://workspace.oblien.com/watchers
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl "https://workspace.oblien.com/watchers" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Response

```json
{
  "watchers": [
    {
      "id": "1",
      "root": "/app/src",
      "dirs": 42,
      "excludes": ["node_modules", ".git"]
    }
  ]
}
```

---

## Get watcher

Get info for a specific watcher.


**REST API:**

```http
GET https://workspace.oblien.com/watchers/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl "https://workspace.oblien.com/watchers/1" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Response

```json
{
  "id": "1",
  "root": "/app/src",
  "dirs": 42,
  "excludes": ["node_modules", ".git"]
}
```

---

## Delete watcher

Stop a watcher and release its resources.


**SDK:**

```typescript
await rt.watcher.delete('1');
```


**REST API:**

```http
DELETE https://workspace.oblien.com/watchers/1
Authorization: Bearer eyJhbGciOiJIUzI1NiIs...
```


**cURL:**

```bash
curl -X DELETE "https://workspace.oblien.com/watchers/1" \
  -H "Authorization: Bearer $GATEWAY_JWT"
```


### Response

```json
{
  "success": true
}
```

---

## WebSocket events

Watcher events are delivered as JSON text frames on the `"watcher"` channel of the `/ws` WebSocket. All events include the `watcher_id` so you can distinguish events from multiple watchers on the same connection.

### `ready`

Sent immediately after a watcher is created and has finished scanning the directory tree.

```json
{
  "channel": "watcher",
  "type": "ready",
  "watcher_id": "1",
  "root": "/app/src",
  "dirs": 42
}
```

### `change`

Sent when a file is created, modified, deleted, or renamed within the watched directory.

```json
{
  "channel": "watcher",
  "type": "change",
  "watcher_id": "1",
  "path": "/app/src/index.ts",
  "op": "write"
}
```

#### Operations

| `op` value | Trigger |
|------------|---------|
| `create` | File or directory created, or moved into the watched tree |
| `write` | File content modified or saved |
| `remove` | File or directory deleted |
| `rename` | File or directory moved out of the watched tree |

Events are **debounced** - rapid changes to the same path within 50ms are collapsed into a single event with the last operation.

### `overflow`

Sent when the event queue overflows. This means some events may have been lost.

```json
{
  "channel": "watcher",
  "type": "overflow",
  "watcher_id": "1",
  "message": "Event queue overflow, some events may have been lost"
}
```

If you receive an overflow event, re-sync the file tree by [listing the directory](/docs/internal-api/files#list-directory) to get the current state.

---

## Listening for events

Connect to the same WebSocket used for [terminal I/O](/docs/internal-api/terminal#websocket). Text frames with `"channel": "watcher"` are file watcher events.

```javascript
const socket = new WebSocket('wss://workspace.oblien.com/ws', {
  headers: { Authorization: `Bearer ${gatewayJwt}` },
});

socket.onmessage = (event) => {
  if (typeof event.data === 'string') {
    const msg = JSON.parse(event.data);

    if (msg.channel === 'watcher') {
      switch (msg.type) {
        case 'ready':
          console.log(`Watcher ${msg.watcher_id} ready: ${msg.root} (${msg.dirs} dirs)`);
          break;
        case 'change':
          console.log(`${msg.op}: ${msg.path}`);
          break;
        case 'overflow':
          console.log('Events may have been lost, re-syncing...');
          break;
      }
    }
  }
};
```

---

## Limits

| Limit | Value |
|-------|-------|
| Max concurrent watchers | 5 per workspace |
| Debounce interval | 50ms per path |
| Auto-watch new subdirectories | Yes |
| Excludes | Merged with defaults, glob matching |

---

## Error responses

| Status | Meaning |
|--------|---------|
| `400` | Missing or invalid `path` |
| `401` | Missing or invalid token |
| `404` | Watcher not found |
| `409` | Already at 5 watchers limit |
| `500` | Failed to create file watcher |
