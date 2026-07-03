# lynx-skill — Architecture Document

> **Document version:** 2.0  
> **AP-12 deliverable:** Architecture design for the Lynx skill  
> **Status:** Final  
> **Last updated:** 2026-05-31  

## Table of Contents

1. [Overview](#1-overview)
2. [Architecture Constraints](#2-architecture-constraints)
3. [Quality Attributes](#3-quality-attributes)
4. [Directory Structure](#4-directory-structure)
5. [CLI Commands](#5-cli-commands-one-per-mcp-tool)
6. [Architecture Decisions (ADRs)](#6-architecture-decisions-adrs)
7. [GWT-RPC Protocol Reference](#7-gwt-rpc-protocol-reference)
8. [Data Flow](#8-data-flow)
9. [Open Decision Points](#9-open-decision-points)
10. [Comparison: lynx-skill vs lynx-mcp-server](#10-comparison-lynx-skill-vs-lynx-mcp-server)
11. [Lessons from Implementation](#11-lessons-from-implementation)
12. [Security Considerations](#12-security-considerations)
13. [Known Issues & Technical Debt](#13-known-issues--technical-debt)

---

## 1. Overview

`lynx-skill` is a stateless Go CLI that replicates every tool from the
`lynx-mcp-server` MCP server as standalone commands. No daemon, no SSE, no
Bearer token — each invocation authenticates independently via GWT-RPC against
`www.lynx-reservations.com` and writes JSON to stdout.

### Purpose

- Replace the MCP server with a zero-dependency CLI usable directly in shell
  scripts, CI/CD pipelines, and OpenClaw agent workflows.
- Eliminate the need for a running server process and Bearer token management.
- Keep the same 7 actions exposed by the original MCP server.

### How a command executes

```
┌──────────┐     ┌──────────┐     ┌─────────────┐     ┌──────────────────────┐
│   User    │     │ lynx CLI │     │  Lynx Backend │     │     GWT-RPC          │
│ (shell/   │     │ (Go bin) │     │ (lynx-reserv- │     │    Protocol          │
│  agent)   │     │          │     │  ations.com)  │     │    (PIPE-DELIMITED)  │
└─────┬─────┘     └─────┬────┘     └──────┬────────┘     └──────────────────────┘
      │                  │                 │                        │
      │  1. lynx <cmd>   │                 │                        │
      │─────────────────>│                 │                        │
      │                  │                 │                        │
      │                  │  2. POST /lynx/service/security.rpc     │
      │                  │     (GWT-RPC login body)                │
      │                  │────────────────>│                        │
      │                  │                 │  3. Validate creds     │
      │                  │                 │────────────────────────│
      │                  │                 │<────────────────────────│
      │                  │ 4. JSESSIONID   │                        │
      │                  │    cookie set   │                        │
      │                  │<────────────────│                        │
      │                  │                 │                        │
      │                  │  5. POST /lynx/service/file.rpc         │
      │                  │     (GWT-RPC action body)               │
      │                  │────────────────>│                        │
      │                  │                 │  6. Parse & execute    │
      │                  │                 │────────────────────────│
      │                  │                 │<────────────────────────│
      │                  │ 7. GWT-RPC      │                        │
      │                  │    response     │                        │
      │                  │<────────────────│                        │
      │                  │                 │                        │
      │                  │ 8. Parse GWT →  │                        │
      │                  │    JSON output  │                        │
      │                  │                 │                        │
      │  9. JSON stdout  │                 │                        │
      │<─────────────────│                 │                        │
```

**Steps in detail:**

1. Read credentials from `LYNX_USERNAME`, `LYNX_PASSWORD`, `LYNX_COMPANY_CODE`
   environment variables (optionally from `.env`).
2. Authenticate via GWT-RPC `POST /lynx/service/security.rpc` → obtains
   `JSESSIONID` cookie stored in the HTTP client's cookie jar.
3. Build the GWT-RPC request body for the specific action.
4. POST the body to the appropriate endpoint on `www.lynx-reservations.com`.
5. Parse the GWT-RPC response into a typed Go struct.
6. Marshal to indented JSON and write to stdout (errors go to stderr).
7. Exit with code 0 on success, 1 on error.

## 2. Architecture Constraints

| Constraint | Description | Source |
|---|---|---|
| **Backend protocol locked** | Lynx only exposes GWT-RPC (text/x-gwt-rpc). No modern REST/JSON API exists. | `lynx-mcp-server` analysis (AP-15) |
| **No runtime dependencies** | CLI must be a single static binary. Zero external packages. | Zero-dependency design goal |
| **Stateless operation** | No daemon, no SSE, no Bearer token. Each invocation is independent. | Migration from MCP server |
| **Backward compatible** | Must replicate all 7 MCP tools with identical server-side behavior. | Story AP-1 requirements |
| **Credential isolation** | Never store credentials in files, logs, or commit to VCS. | Security requirement |
| **Go language** | Must use Go 1.23+ (same as MCP server) for protocol knowledge transfer. | AP-16 decision |
| **JSON output** | All commands write JSON to stdout; errors to stderr. Unix-philosophy compliant. | CLI convention |

## 3. Quality Attributes

| Attribute | Target | Measure |
|---|---|---|
| **Startup time** | < 100 ms (binary loading) | `time lynx --help` |
| **Command latency** | ~500-1500 ms (includes GWT-RPC login + action) | `time lynx file-search-by-party-name --party-name=X` |
| **Binary size** | < 15 MB (stripped) | `ls -lh bin/lynx` |
| **Test coverage** | > 50% on `gwt/` package (parsing logic) | `go test -cover ./gwt/` |
| **Memory usage** | < 50 MB per invocation | `ulimit -v` or `time -v` |
| **Error surface** | All errors go to stderr; exit code 1; no silent failures | Manual audit |
| **Maintainability** | Zero external dependencies; pure stdlib | `go list -m all` |

## 4. Directory Structure

```
lynx-skill/
├── main.go                     # Entry point — calls cmd.Run()
├── go.mod                      # Module: dodmcdund.cc/lynx-travel-agent/lynxskill (Go 1.23.10)
├── go.sum
├── .gitignore                  # Ignores /bin/, /lynxskill
├── .env                        # Local credentials (gitignored?)
├── SKILL.md                    # OpenClaw skill definition (YAML frontmatter + docs)
├── README.md                   # User-facing documentation
├── lynx_architecture.md        # This file
│
├── cmd/                        # CLI commands — one file per command + dispatcher
│   ├── cmd.go                  # Command registry, dispatcher, config loader
│   ├── file_search_by_party_name.go
│   ├── file_search_by_file_reference.go
│   ├── retrieve_itinerary.go
│   ├── retrieve_file_documents.go
│   ├── attachment_upload.go
│   ├── file_document_save.go
│   └── transaction_document_save.go
│
├── gwt/                        # GWT-RPC protocol layer
│   ├── types.go                # GWT type constants (class names)
│   ├── build.go                # GWT-RPC body builders (one func per action)
│   └── parse.go                # GWT response parsers + response structs
│
└── lynx/                       # HTTP client layer
    ├── auth.go                 # GWT-RPC login → JSESSIONID
    └── client.go               # HTTP helpers: DoGWTRequest, DoMultipartRequest
```

### Layering

```
main.go
   └─ cmd.Run()
        └─ cmd.<action>.run(args)
             ├─ cmd.GetConfig()       ← reads env vars
             ├─ lynx.Login()          ← auth → http.Client with JSESSIONID
             │    └─ gwt.BuildLoginBody()
             ├─ gwt.Build<Action>Body()
             ├─ lynx.DoGWTRequest()   ← POST to /lynx/service/file.rpc
             └─ gwt.Parse<Action>Response()
                  └─ json.MarshalIndent → stdout
```

## 5. CLI Commands (one per MCP tool)

| # | CLI Command | MCP Tool (original) | Flags | GWT RPC Endpoint |
|---|-------------|---------------------|-------|------------------|
| 1 | `file-search-by-party-name` | `file_search_by_party_name` | `--party-name` | `/lynx/service/file.rpc` — `FileService.searchWithCount` |
| 2 | `file-search-by-file-reference` | `file_search_by_file_reference` | `--file-reference` | `/lynx/service/file.rpc` — `FileService.searchWithCount` |
| 3 | `retrieve-itinerary` | `retrieve_itinerary` | `--file-identifier` | `/lynx/service/file.rpc` — `FileService.retrieveItinerary` |
| 4 | `retrieve-file-documents` | `retrieve_file_documents` | `--file-identifier`, `--transaction-identifier` | `/lynx/service/file.rpc` — `FileService.getFileDocumentsAsList` |
| 5 | `attachment-upload` | `attachment_upload` | `--identifier`, `--file` (local path) | `POST /lynx/fileDocumentUpload` (multipart) |
| 6 | `file-document-save` | `file_document_save` | `--file-identifier`, `--name`, `--content`, `--type`, `--attachment-url` (opt.) | `/lynx/service/file.rpc` — `FileService.saveFileDocumentsDetails` |
| 7 | `transaction-document-save` | `transaction_document_save` | `--file-identifier`, `--transaction-identifier`, `--name`, `--content`, `--type`, `--attachment-url` (opt.) | `/lynx/service/file.rpc` — `FileService.saveFileDocumentsDetails` |

### Output convention

All commands write JSON to stdout on success:

```json
{
  "count": 1,
  "results": [...]
}
```

Errors go to stderr and the process exits with code 1.

## 6. Architecture Decisions (ADRs)

All decisions are recorded as lightweight Architecture Decision Records (ADRs)
with date, context, and rationale.

### ADR-001: Technology — Go 1.23+

**Date:** 2026-05 (AP-16)  
**Status:** Accepted  
**Decision:** Go (not Python).

**Context:** The MCP server is Go. The CLI must be a statically-linked binary
with zero runtime deps.

**Rationale:**
- Language consistency with `lynx-mcp-server` — protocol knowledge transfers.
- Single static binary, no interpreter, fast startup.
- Standard library covers `net/http`, `flag`, `encoding/json`, `cookiejar`.
- Trivial cross-compilation (GOOS/GOARCH).

### ADR-002: Authentication — GWT-RPC per command

**Decision:** Each command logs in independently with a fresh GWT-RPC call.

**Rationale:**
- The Lynx backend uses GWT-RPC with `JSESSIONID` cookies (15 min TTL).
- No persistent session server needed — avoiding the MCP server's Bearer token
  indirection removes operational complexity.
- Trade-off: every invocation pays ~500 ms login overhead, but the CLI is
  designed for occasional agent use, not high-throughput automation.

**Protocol details:**
| Endpoint | `POST https://www.lynx-reservations.com/lynx/service/security.rpc` |
|---|---|
| Content-Type | `text/x-gwt-rpc; charset=utf-8` |
| Body format | `7\|0\|9\|...\|login\|...\|companyCode\|username\|password\|...` |
| Success | `//OK` prefix in response + Set-Cookie `JSESSIONID=...` |
| Failure | `//EX` prefix with GWT serialized exception |

### ADR-003: HTTP Client — Go standard library

**Date:** 2026-05 (AP-16)  
**Status:** Accepted  
**Decision:** Use `net/http` with custom `cookiejar` — no external HTTP library.

**Rationale:**
- `net/http` is sufficient for the 6 GWT-RPC endpoints + 1 multipart upload.
- The `cookiejar` stores `JSESSIONID` automatically for the duration of the
  command, avoiding manual cookie handling.
- Multipart form upload is built manually without external packages (keeping
  zero dependencies).

### ADR-004: CLI Framework — Go `flag` package

**Date:** 2026-05 (AP-16)  
**Status:** Accepted  
**Decision:** Use Go's standard `flag` package per command.

**Rationale:**
- Simple, zero-dependency, widely understood.
- Each command defines its own `flag.FlagSet` so `--help` works per-command.
- No need for cobra/viper for a 7-command CLI.
- Kebab-case flag names (`--file-identifier`) for consistency with CLI conventions.

### ADR-005: Response Parsing — Custom GWT-RPC parser

**Date:** 2026-05 (AP-17)  
**Status:** Accepted  
**Decision:** Parse GWT-RPC response format directly (no Java/GWT runtime).

**Rationale:**
- GWT-RPC serialization is a well-known text format (version 7).
- The parser handles: strings (single/double quoted), integers, floats, nested
  arrays, and error responses (`//EX`).
- Two serialization formats are handled:
  - **Old format (pre-mid 2025):** Type strings like
    `com.lynxtraveltech.client.shared.model.FileSearchResults` appear directly
    in the data array.
  - **New format (lazy serialization):** Type strings are resolved through
    index-based references in a mapped array. The first mapped string
    determines which format is active.
- **Trade-off:** Fragile if Lynx changes their GWT-RPC format. Mitigated by
  clear error messages and a single parse layer to update.

### ADR-006: Attachment Upload — Direct file I/O

**Date:** 2026-05 (AP-17)  
**Status:** Accepted  
**Decision:** Accept a local file path (`--file`) instead of base64-encoded content.

**Rationale:**
- The MCP server required base64 in JSON, which bloats the agent context.
- The CLI reads the file from disk, infers the filename, and sends a proper
  `multipart/form-data` request to `POST /lynx/fileDocumentUpload`.
- The server returns `SUCCESS:/documents/file/...` which is parsed into JSON.

### ADR-007: Configuration — Environment variables

**Date:** 2026-05 (AP-16)  
**Status:** Accepted  
**Decision:** Read credentials from `LYNX_USERNAME`, `LYNX_PASSWORD`,
`LYNX_COMPANY_CODE`.

**Rationale:**
- Standard 12-factor app pattern.
- Works with `.env` files, direnv, CI/CD secrets, and container orchestration.
- No config file to manage alongside the binary.

### ADR-008: Error Handling

**Date:** 2026-05 (AP-17)  
**Status:** Accepted  
**Decision:** Structured approach with three error tiers:

| Layer | Error type | Handling |
|---|---|---|
| Auth | `authentication failed: ...` | Env vars not set or login rejected |
| GWT protocol | `GWT error: ...` | Lynx backend returned `//EX` |
| Parsing | `failed to parse response: ...` | Response format unexpected or changed |

- All errors are `fmt.Errorf` with wrapping (`%w`).
- Final output: `fmt.Fprintf(os.Stderr, "Error: %v\n", err)` then `os.Exit(1)`.
- JSON is never written to stdout when an error occurs.

### ADR-009: .env Auto-Load

**Date:** 2026-05 (AP-17 fix)  
**Status:** Accepted  
**Decision:** Auto-load `.env` from CWD at startup with zero-dependency parser.

**Rationale:**
- Convenience for local development.
- Reads `.env` silently if it doesn't exist.
- Only sets vars not already set (env takes precedence).
- `.gitignore` excludes `.env` to prevent credential leaks.

### ADR-010: Session Cookie via cookiejar (not manual cookie)

**Date:** 2026-05 (AP-17 fix)  
**Status:** Accepted  
**Decision:** Return `*http.Client` with `cookiejar` from `Login()`, pass it
through all requests — no manual `JSESSIONID` cookie header.

**Rationale:**
- Eliminates duplicated cookie-setting code in every command.
- `cookiejar` handles domain/path matching automatically.
- Simpler API: `client, _, err := lynx.Login(...)` then
  `lynx.DoGWTRequest(client, ...)`.

## 7. GWT-RPC Protocol Reference

### 7.1 Wire Format

GWT-RPC (Google Web Toolkit Remote Procedure Call) is a text-based
serialization protocol used by the Lynx backend. Version 7 of the protocol
uses pipe-delimited (`|`) fields:

```
7|0|<fieldCount>|https://<host>/lynx/lynx/|<strongName>|<serviceInterface>|<methodName>|<paramTypes>|<paramValues>|...|0|
```

| Field | Offset | Description |
|-------|--------|-------------|
| `7` | 0 | Protocol version (always 7) |
| `0` | 1 | Flags (0 = no flags) |
| `<fieldCount>` | 2 | Number of pipe-delimited fields in payload |
| `https://...` | 3 | Module base URL |
| `<strongName>` | 4 | GWT permutation strong name (hash) |
| `<interface>` | 5 | Fully-qualified service interface |
| `<method>` | 6 | RPC method name |
| `<params>` | 7+ | Serialized parameter types and values |
| `0` | last | Trailing zero (end marker) |

**Strong names used:**

| Strong Name | Service |
|---|---|
| `4775EB021C85EC0B04470837F40FC64A` | SecurityService (login) |
| `E6FD624F490EC48C3F3EE2883991BDC9` | FileService (all file operations) |

### 7.2 Request Examples

**Login request** (from `gwt/build.go:5-9`):
```
7|0|9|https://www.lynx-reservations.com/lynx/lynx/|4775EB021C85EC0B04470837F40FC64A|com.lynxtraveltech.common.gui.client.rpc.SecurityService|login|java.lang.String/2004016611|Z|<company>|<user>|<pass>|1|2|3|4|4|5|5|5|6|7|8|9|0|
```

**File search by party name** (from `gwt/build.go:12-16`):
```
7|0|9|https://www.lynx-reservations.com/lynx/lynx/|E6FD624F490EC48C3F3EE2883991BDC9|com.lynxtraveltech.client.client.rpc.FileService|searchWithCount|com.lynxtraveltech.client.shared.model.FileSearchCriteria/2731823162||<partyName>|PARTY_NAME|DD MMM YYYY|1|2|3|4|1|5|5|6|6|0|0|0|1|7|6|50|8|6|9|0|0|6|
```

### 7.3 Response Format

**Success:** `//OK[<GWT array data>]`  
**Error:** `//EX[<GWT serialized exception>]`

The GWT array is a comma-separated, recursively-parsed format:

```
['K',50,22,46,0,49,'$yfl',6,48,'BAiA',29,3,47,9,46,0,45,'$7z6',...]
```

Elements are:
- **Strings**: single-quoted (`'hello'`) or double-quoted (`"hello"`) with
  doubled-quote escaping (`''` → `'`, `""` → `"`)
- **Integers**: bare numbers (`50`, `22`, `0`)
- **Nested arrays**: `[<elements>]`
- **Special strings**: `$`-prefixed (GWT internal identifiers)

### 7.4 Response Parsing Algorithm

All GWT response parsers follow the same backward-scanning pattern:

1. Strip `//OK` or `//EX` prefix
2. Parse the outer GWT array (comma-separated, respecting quotes and nesting)
3. Locate the **data array** at position `len-3` (third from last)
4. Read **one-based index** at position `len-4` → points into data array
5. Determine format by inspecting the indexed string:
   - Starts with `java.util.ArrayList` → **lazy serialization (current)**
   - Starts with `FileSearchResponse/...` → **old format**
6. Walk **backward** from position `len-6`, looking for type markers:
   - `FileSearchResults` → extract 10 fields
   - `DocumentDetails` → extract 17 fields
   - `TransactionSummary` → extract 15 fields
7. Fields are resolved via index references into the data array
8. `\\x<hex>` escape sequences are unescaped (e.g. `\\x26` → `&`)

### 7.5 Endpoint Reference

| Endpoint | Method | Content-Type | Purpose |
|---|---|---|---|
| `POST /lynx/service/security.rpc` | POST | `text/x-gwt-rpc; charset=utf-8` | GWT-RPC login → JSESSIONID |
| `POST /lynx/service/file.rpc` | POST | `text/x-gwt-rpc; charset=utf-8` | All file operations (6 tools) |
| `POST /lynx/fileDocumentUpload` | POST | `multipart/form-data` | Attachment upload (1 tool) |

## 8. Data Flow

### 8.1 Command dispatch flow

```
main.main()
  └─ cmd.Run()                           ← parse os.Args, dispatch
       ├─ loadDotEnv()                    ← init(): auto-load .env
       ├─ Find command by name             ← match os.Args[1]
       └─ command.Run(args)               ← run handler
            ├─ flag.NewFlagSet(...)        ← parse --flags
            ├─ cmd.GetConfig()            ← read LYNX_* env vars
            ├─ lynx.Login()               ← GWT-RPC login → http.Client + JSESSIONID
            │    ├─ gwt.BuildLoginBody()   ← pipe-delimited body
            │    └─ POST /service/security.rpc
            ├─ gwt.Build<Action>Body()    ← build GWT-RPC action body
            ├─ lynx.DoGWTRequest()        ← POST /service/file.rpc
            │    └─ GWT error? → ParseErrorResponse() → return error
            ├─ gwt.Parse<Action>Response() ← backward-scan GWT array
            └─ json.MarshalIndent → stdout
```

### 8.2 Flow for attachment-upload (non-GWT)

```
command.Run(args)
  ├─ os.ReadFile(--file)                 ← read file from disk
  ├─ lynx.Login()                        ← GWT-RPC login (same auth flow)
  ├─ Build multipart form
  │    ├─ field "fileId" = --identifier
  │    └─ file "file" = binary content
  ├─ lynx.DoMultipartRequest()           ← POST /lynx/fileDocumentUpload
  └─ parseAttachmentResponse()           ← parse "SUCCESS:/path:" → JSON
       └─ json.MarshalIndent → stdout
```

### 8.3 Error flow

```
Any layer error
  └─ fmt.Errorf("layer: %w", err)        ← wrap with context
       └─ fmt.Fprintf(os.Stderr, "Error: %v\n", err)
            └─ os.Exit(1)                ← exit code 1, no stdout
```

## 9. Open Decision Points

| # | Question | Options | Recommendation | Status |
|---|----------|---------|----------------|--------|
| 1 | **Session caching** | (a) No cache — login per command (current) / (b) Cache JSESSIONID in temp file with 10 min TTL | Stick with (a) for simplicity; revisit if latency becomes an issue | Decided |
| 2 | **Rate limiting** | (a) No limiter / (b) Simple token bucket / (c) Exponential backoff on 429 | Add simple retry with backoff if 429 observed in practice | Deferred |
| 3 | **GWT-RPC format versioning** | (a) Single parser with format detection / (b) Versioned parsers selected by heuristics | Current auto-detection (old vs lazy format) works; add explicit version if 3rd format appears | Deferred |
| 4 | **Binary release** | (a) Manual `go build` / (b) GitHub Actions release workflow per tag | Add a `.github/workflows/release.yml` for automatic cross-compilation and GitHub Release | Future |
| 5 | **Environment variable validation** | (a) Fail at startup / (b) Fail on first action | Current behavior: fail on first command with per-variable error messages | Decided |
| 6 | **.env file handling** | (a) Manual sourcing / (b) Auto-load `.env` with `godotenv` | Stick with (a) to keep zero deps; users source `.env` themselves | Decided |
| 7 | **Credential committing risk** | (a) `.env` in `.gitignore` / (b) Environment-only | `.env` is now in `.gitignore` — git will ignore it even if it contains real credentials | Resolved |
| 8 | **Retry/backoff** | (a) No retry / (b) Exponential backoff like MCP server | CLI has no retry yet; add if 429 or transient failures observed | Deferred |
| 9 | **GWT-RPC parser format** | (a) Single parser / (b) Dual-format auto-detection | Implemented dual-format (old + lazy) with backward scanning; tested with 10-result real response | Implemented |
| 10 | **Test coverage** | (a) None / (b) Basic tests / (c) Full coverage | `parse_test.go` covers FileSearchResponse parsing with real GWT data | Partial |

## 10. Comparison: lynx-skill vs lynx-mcp-server

| Aspect | lynx-mcp-server | lynx-skill |
|--------|----------------|------------|
| **Architecture** | MCP server with SSE transport | Stateless CLI |
| **Session** | Bearer token + shared JSESSIONID per server | Fresh JSESSIONID per command |
| **Attachment upload** | Base64-encoded in JSON content | Direct file path from disk (`--file`) |
| **Flag style** | camelCase (MCP schema) | kebab-case (CLI convention) |
| **Binary name** | `lynx-mcp-server` | `lynx` |
| **Output** | MCP response envelope (`content`, `isError`) | Raw JSON to stdout, errors to stderr |
| **Dependencies** | `github.com/mark3labs/mcp-go`, `github.com/joho/godotenv` | Zero external dependencies |
| **Entry point** | Long-lived server process | One-shot process |
| **GWT-RPC format** | Old format only | Old + lazy serialization (v2) |

## 11. Lessons from Implementation (AP-17)

### 11.1 GWT-RPC Dual-Format Parser

The biggest implementation challenge was the GWT-RPC response parser. The Lynx backend
returns two serialization formats that the parser must auto-detect:

- **Old format (pre-mid 2025):** Type strings like
  `com.lynxtraveltech.client.shared.model.FileSearchResponse/2457361185` appear
  directly in the data array. Parsing walks backward from the end of the parsed array.
- **Lazy serialization (current):** Type strings are referenced through index-based
  mappings in the data array. The first mapped string determines the format.

The `ParseFileSearchResponse` function (`gwt/parse.go:183-288`) implements backward
scanning — it iterates from the last element backward, identifies `FileSearchResults`
type markers, and extracts 10 fields per result. This handles multi-result responses
correctly (validated with 10-result test in `gwt/parse_test.go`).

### 11.2 .env Auto-Load

`cmd/cmd.go:13-33` implements a lightweight `.env` loader with zero dependencies:

- Reads `.env` from CWD at startup (silent if file doesn't exist)
- Only sets env vars that are **not already set** (env takes precedence)
- `.env` is in `.gitignore` — resolves the credential risk flagged in Open Decision Points

### 11.3 Attachment Upload Response Parsing

The Lynx backend returns `SUCCESS:/path/to/file:` (note trailing colon). The MCP server
has duplicated parsing logic in two files (`pkg/tools/attachment_upload.go` and
`pkg/rest/attachment_upload.go`). The CLI consolidates this into a single function
`parseAttachmentResponse` in `cmd/attachment_upload.go:84-101`.

### 11.4 Missing Retry Logic

The MCP server's `RetryHTTPRequest` implements exponential backoff (0s → 5s → 10s → 30s → 30s,
max 5 attempts). GWT errors (`//EX`) are **not** retried. The CLI has no retry — each
command makes exactly one request. This is acceptable for agent use cases but may need
retry if 429 rate limits or transient failures are observed.

### 11.5 MCP Identifier Typo Corrected

The MCP server's `attachment_upload` uses `identifer` (missing 'i'). The CLI correctly
uses `--identifier`. This is a minor but intentional breaking change from the MCP naming.

### 11.6 Test Coverage

`gwt/parse_test.go` contains a real-world test case using a GWT-RPC response from a
BRAY search that returns 10 results. The test validates all fields (partyName,
clientReference, fileIdentifier, travelDate, status, currency, companyCode) for each
result. Run with:

```bash
cd lynx-travel-agent/lynx-skill && go test ./gwt/ -v
```

## 12. Security Considerations

- **Credentials:** `LYNX_USERNAME`, `LYNX_PASSWORD`, `LYNX_COMPANY_CODE` are
  sensitive. Never hardcode them in scripts or commit to version control.
- **Session replay:** The `JSESSIONID` cookie is valid for ~15 minutes.
  If an attacker captures it, they can impersonate the user until expiry.
  Mitigated by short TTL and per-command login in the CLI.
- **TLS:** All requests go to `https://www.lynx-reservations.com` — TLS is
  enforced at the URL level.
- **No token storage:** Unlike the MCP server which exposes a Bearer token,
  the CLI never stores or logs credentials or session tokens.

## 13. Known Issues & Technical Debt

### 13.1 Duplicated GWT Array Parser

The `parseGWTArray` / `parseGWTElement` functions exist in **two packages**:

| Package | File | Lines |
|---------|------|-------|
| `gwt/` | `gwt/parse.go` | `ParseGWTArray` line 62, `parseGWTElement` line 133 |
| `lynx/` | `lynx/client.go` | `parseGWTArray` line 126, `parseGWTElement` line 197 |

The `lynx/client.go` copy is used only for parsing `//EX` error responses from
the HTTP client layer. The `gwt/parse.go` copy is the main parser for all
successful responses. The duplication was introduced because the HTTP client
(`lynx`) package cannot import the `gwt` parser package without creating a
circular dependency (since `gwt` builders are called from `cmd/`, and `lynx/`
is also called from `cmd/`).

**Impact:** Low — both copies are identical.  
**Fix:** Extract the GWT array parser into a shared `internal/` package or
consolidate into `gwt/` and call it from `lynx/` via a thin adapter.

### 13.2 No Retry/Backoff

The MCP server's `RetryHTTPRequest` implements exponential backoff
(0s → 5s → 10s → 30s → 30s, max 5 attempts). The CLI has no retry —
each command makes exactly one attempt.

**Impact:** Low for agent use cases (one-shot commands). Medium if Lynx
backend returns transient errors or 429 rate limits.

### 13.3 Only FileSearch Parser Has Dual-Format Support

`ParseRetrieveItinerary` and `ParseFileDocumentsResponse` both assume the
**lazy serialization format** only (checking for `java.util.ArrayList` at
the mapped index). If the Lynx backend switches to old format for these
responses, they will fail to parse.

**Impact:** Low — current Lynx backend uses lazy format consistently.  
**Fix:** Add format auto-detection to the other two parsers, mirroring the
pattern in `ParseFileSearchResponse`.

### 13.4 Hardcoded Strong Names

The GWT-RPC strong names (`4775EB021C85EC0B04470837F40FC64A` for login,
`E6FD624F490EC48C3F3EE2883991BDC9` for file service) are hardcoded as string
literals in `gwt/build.go`. These are GWT permutation hashes and may change
when Lynx recompiles their GWT frontend.

**Impact:** Medium — if strong names change, all actions break until the
literals are updated.  
**Mitigation:** The strong names have been stable across both old and new
GWT-RPC formats observed during implementation.

### 13.5 No Integration Tests

Test coverage exists only for the GWT-RPC parser (`gwt/parse_test.go`).
There are no integration tests against the live Lynx backend.

**Impact:** Medium — code changes that break the GWT body format (pipe-delimited
structure) would only be caught during manual testing against production.

### 13.6 Hardcoded RemoteHost

`cmd/cmd.go:109` hardcodes `RemoteHost: "www.lynx-reservations.com"`. This
cannot be overridden without code changes.

**Impact:** Low — the production host is stable. Useful to make configurable
if a staging/test environment is ever needed.
