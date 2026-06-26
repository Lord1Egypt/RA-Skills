# Guard-Scanner Integration Manifest

As per P2 Ecosystem Integration requirements, this manifest defines the required permissions and principle of least privilege for each operational mode.

## 1. Offline Static Scan Mode (`guard-scanner scan`)
**Purpose:** Scans local directories for malicious patterns without executing code.
**Permissions Required:**
- `fs:read` (Target directory and subdirectories)
- `fs:write` (Only for generating reports like `guard-scanner-report.json`)
- **Blocked:** `network:*`, `exec:*`

## 2. Runtime Guard Mode (OpenClaw `before_tool_call` hook)
**Purpose:** Intercepts agent tool calls before execution to enforce security policies.
**Permissions Required:**
- `fs:read` (To read configuration and context)
- `process:env` (To check execution context if needed)
- **Blocked:** `fs:write`, `network:*`, `exec:*`

## 3. MCP Service Mode (`guard-scanner serve`)
**Purpose:** Runs as a persistent Model Context Protocol server exposing scanning tools to agents.
**Permissions Required:**
- `network:listen` (To expose the MCP API or WebSocket)
- `fs:read` (To scan requested paths)
- **Blocked:** `exec:*`

## 4. Asset Audit Mode (`guard-scanner audit`)
**Purpose:** Queries external services (GitHub, npm, VT) to audit supply chain assets.
**Permissions Required:**
- `network:connect` (To connect to `api.github.com`, `registry.npmjs.org`, etc.)
- `fs:read` (To read local credential config if needed)
- **Blocked:** `exec:*`, `fs:write`

## 5. CI Mode (GitHub Actions / GitLab CI)
**Purpose:** Integrates directly into CI pipelines emitting SARIF or Code Climate formats.
**Permissions Required:**
- `fs:read` (To scan workspace)
- `fs:write` (To write SARIF/JSON artifacts)
- `env:read` (To read CI-specific variables like `GITHUB_WORKSPACE`)
- **Blocked:** `exec:*`, `network:*` (Unless combined with Asset Audit)
