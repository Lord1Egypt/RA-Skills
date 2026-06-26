# TOOL REGISTRY

All tool calls flow through the Tool Router (see `tools/tool-router.md`).
Agents NEVER call tools directly -- they submit a Tool Request.

---

## BLOCKED TOOLS (not available to agents)

The following capabilities are intentionally absent from this registry. Agents must not
attempt to invoke them or construct equivalent behavior from other tools.

| Capability | Reason blocked |
|------------|---------------|
| `call_api(endpoint, ...)` | Unconstrained outbound network access -- arbitrary host/port |
| `start_server()` / `stop_server()` | Server lifecycle management is out of harness scope |
| Any system hardware query | CPU model, VM identifiers, OS internals -- not application concerns |
| Direct shell invocation or dynamic code evaluation | Security risk -- all tool calls must route through the tool router |
| Read/write to harness files | See PROTECTED PATHS in `tools/tool-router.md` |
| Raw log/response body in memory | Logs contain only metadata -- never raw payloads |
| Direct write to `docs/references/` from web_search | Stage in `docs/generated/search-staging/`; human promotes |
- All tool outputs must be machine-readable (JSON preferred).
- Every tool call must be logged to `docs/generated/tool-logs/`.
- NEVER trust tool output blindly -- always validate.
- Retry up to 3 times on failure before escalating.

---

## AVAILABLE TOOLS

### FILESYSTEM
| Tool | Signature | Notes |
|------|-----------|-------|
| Read file | `read_file(path)` | Returns file contents |
| Write file | `write_file(path, content)` | Creates or overwrites |
| List directory | `list_dir(path)` | Returns file tree |
| Search code | `search_code(query)` | Regex/semantic search across repo |

### GIT
| Tool | Signature | Notes |
|------|-----------|-------|
| Status | `git_status()` | Staged, unstaged, untracked |
| Diff | `git_diff()` | Current changes vs HEAD |
| Checkout | `git_checkout(branch)` | Switch or create branch |
| Commit | `git_commit(message)` | Must include plan reference in message |
| Create PR | `git_create_pr()` | Blocked without tests + docs |

### TESTING
| Tool | Signature | Notes |
|------|-----------|-------|
| Unit tests | `run_unit_tests()` | Returns structured JSON result |
| Integration tests | `run_integration_tests()` | |
| E2E tests | `run_e2e_tests()` | |
| Fuzz tests | `run_fuzz_tests()` | Recommended, not required |

### CI/CD
| Tool | Signature | Notes |
|------|-----------|-------|
| Trigger pipeline | `trigger_pipeline()` | Starts CI run |
| Pipeline status | `get_pipeline_status()` | Polls until complete |

### SEARCH
| Tool | Signature | Notes |
|------|-----------|-------|
| Web search | `web_search(query)` | External knowledge acquisition |
| Code search | `code_search(query)` | Cross-repo symbol search |
| Dependency lookup | `dependency_lookup(package)` | Versions, vulnerabilities |

### SECURITY
| Tool | Signature | Notes |
|------|-----------|-------|
| Vulnerability scan | `scan_vulnerabilities()` | SAST + dependency scan |
| Dependency audit | `dependency_audit()` | Check for known CVEs |

### METRICS
| Tool | Signature | Notes |
|------|-----------|-------|
| Collect logs | `collect_logs()` | Aggregates application runtime logs only |
| Performance profile | `performance_profile()` | **Application-level only**: request latency, throughput, heap usage. Must NOT query system hardware, CPU model, VM identifiers, or host OS internals. |

---

## PER-AGENT TOOL ASSIGNMENT

See references/mcp-tools.md for the complete per-agent tool subset table.
The dispatcher is responsible for assigning the correct subset at dispatch time.
Never give an agent tools it does not need for its phase.

## MCP PROTOCOL NOTE

All tools in this registry are accessed via MCP (Model Context Protocol).
No agent calls a tool implementation directly.
All calls route through tools/tool-router.md for validation, redaction, and logging.
