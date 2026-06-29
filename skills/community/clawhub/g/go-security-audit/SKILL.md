---
name: go-security-audit
description: >
  Perform a security audit of a Go codebase. Targets SSH servers, BBS systems,
  API services, and CLI tools. Finds race conditions, goroutine leaks, missing
  error handling, command injection, and auth bypasses. Produces a prioritized
  finding list with file:line citations and minimal diff patches.
  Use when asked to audit, review, or security-test a Go repository.
---

# Go Security Audit

## Workflow

### Phase 1: Reconnaissance
1. Map the codebase: `go.mod` for dependencies, `cmd/` for entry points, `internal/` for core logic
2. Identify concurrency primitives: `sync.Mutex`, `sync.RWMutex`, channels, goroutines
3. Identify external inputs: HTTP handlers, SSH sessions, CLI args, env vars, DB queries
4. Note subprocess execution: `exec.Command`, `os.StartProcess`

### Phase 2: Race Condition Analysis
Check every shared mutable state:

**TOCTOU patterns — check/act gaps:**
```go
// BAD: unlock between check and use
r.mu.Lock()
entry, ok := r.m[id]
r.mu.Unlock()          // ← gap here
if !ok { return }
entry.Close()          // ← entry could be gone

// GOOD: defer unlock or keep locked through the operation
r.mu.Lock()
defer r.mu.Unlock()
entry, ok := r.m[id]
if !ok { return }
delete(r.m, id)
entry.Close()
```

**Map concurrent access:**
- Any `map` written in one goroutine and read in another without mutex → data race
- Use `sync.Map` or protect with `sync.RWMutex`

**Channel patterns:**
- Unbuffered channels sent to from goroutines that may outlive the receiver → goroutine leak
- `close()` called on a channel that may already be closed → panic

### Phase 3: Error Handling Audit
Find silent failures:

```go
// Flag patterns:
result, _ = someFunc()     // error discarded
res.LastInsertId()          // return value ignored
time.Parse(layout, val)    // two-return ignored with _
```

Every `_` on the error position should be justified or flagged.

**SQL patterns:**
```go
// Check LastInsertId separately:
id, err := res.LastInsertId()
if err != nil {
    return 0, fmt.Errorf("get insert id: %w", err)
}
```

### Phase 4: Command Injection
Check every `exec.Command` / `exec.CommandContext` call:

```go
// Risky: user-controlled input split with strings.Fields
parts := strings.Fields(os.Getenv("USER_CMD"))
cmd := exec.CommandContext(ctx, parts[0], parts[1:]...)

// Safe: validate no shell metacharacters, or use explicit args
if strings.ContainsAny(cmdline, "|;&$`(){}") {
    return fmt.Errorf("invalid command")
}
```

### Phase 5: Auth and Session Checks
- Are admin routes protected? Check every handler for auth middleware
- Session IDs: are they random (crypto/rand) or sequential/guessable?
- Is `context.WithTimeout` used for all external calls?
- Are sessions cleaned up on disconnect (no memory leak)?

### Phase 6: Resource Leak Audit
```go
// File descriptors — check every os.Open has defer Close()
f, err := os.Open(path)
// missing defer f.Close() → leak

// Goroutine leaks — goroutines started without a stop mechanism
go func() {
    for { select { case <-ch: ... } }  // ← what closes ch?
}()

// DB rows — rows.Close() deferred after rows.Next() loop
rows, _ := db.Query(...)
defer rows.Close()  // must be present
```

## Output Format

```
## Finding [N]: [Title] — [Critical/High/Medium/Low]
**File:** path/file.go:LINE
**Impact:** [what can go wrong]
**Root cause:** [exact code snippet]
**Fix:**
\`\`\`go
// corrected code
\`\`\`
```

Prioritize by: Critical (data loss/auth bypass) → High (crash/leak) → Medium (silent failure) → Low (hardening)
