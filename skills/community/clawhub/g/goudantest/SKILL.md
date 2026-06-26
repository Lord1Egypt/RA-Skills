---
name: code-review-v2
description: Advanced code review assistant with intelligent analysis, multi-language support, and structured feedback. Performs comprehensive reviews covering correctness, security, performance, maintainability, and observability. Use when reviewing pull requests, code changes, conducting security audits, performance reviews, or when the user requests detailed code analysis. Supports Python, JavaScript/TypeScript, Java, Go, Rust, C#, Ruby, PHP.
---

# Code Review v2

## Intelligent Review Workflow

### Phase 1: Context Analysis
Before reviewing code, understand the context:

1. **Identify change scope**: What files/modules are affected?
2. **Understand intent**: Read PR description, linked issues, commit messages
3. **Assess risk level**: 
   -🔴High**: Core logic, auth, payment, data handling, public APIs
   -Medium**: Business logic, internal APIs, utilities
   -Low**: Tests, docs, config, minor refactoring
4. **Determine review depth** based on risk level

### Phase 2: Automated Analysis
Run these checks mentally before manual review:

```
□ Static analysis patterns (type mismatches, unused imports, dead code)
□ Security patterns (injection, unsafe deserialization, hardcoded secrets)
□ Performance patterns (N+1 queries, unbounded loops, missing indexes)
□ Concurrency patterns (race conditions, deadlocks, missing synchronization)
```

### Phase 3: Manual Review
Follow the [CHECKLIST.md](CHECKLIST.md) for systematic review.

### Phase 4: Feedback Generation
Use templates from [TEMPLATES.md](TEMPLATES.md) for structured feedback.

---

## Quick Reference: Review Dimensions

| Dimension | Focus Area | Key Questions |
|-----------|-----------|---------------|
| **Correctness** | Logic, edge cases | Does it work correctly in all scenarios? |
| **Security** | Vulnerabilities, data protection | Are there security risks or data leaks? |
| **Performance** | Efficiency, resource usage | Will this scale? Any bottlenecks? |
| **Maintainability** | Readability, structure | Can others understand and modify this? |
| **Observability** | Logging, monitoring, debugging | Can we detect and diagnose issues? |
| **Testing** | Coverage, quality | Are changes adequately tested? |

---

## Severity Classification

| Level | Icon | When to Use | Response Required |
|-------|------|-------------|-------------------|
| **Blocker** | Security vulnerability, data loss, crash | Must fix before merge |
| **Critical** |🔴 Bug, incorrect logic, broken functionality | Must fix before merge |
| **Warning** | Code smell, suboptimal pattern, minor issue | Should address |
| **Suggestion** |💡 Improvement opportunity, alternative approach | Consider |
| **Info** |ℹ | Observation, documentation note | Optional |

---

## Language-Specific Quick Checks

### Python
```
□ Type hints on public functions
□ No mutable default arguments
□ Context managers for resources
□ f-strings over .format() or %
□ Proper exception handling (not bare except)
□ __init__.py exports are intentional
```

### JavaScript / TypeScript
```
□ async/await with try-catch (no unhandled promises)
□ No implicit any (TypeScript strict mode)
□ Proper null/undefined handling
□ No direct DOM manipulation in React
□ Keys in list rendering
□ useEffect dependencies complete
```

### Java
```
□ try-with-resources for Closeable
□ Optional for nullable returns
□ Proper equals/hashCode implementation
□ No raw types (generics)
□ Stream API used appropriately
□ Thread safety considered
```

### Go
```
□ Error handling (not ignored)
□ defer for cleanup
□ Context passed as first parameter
□ No goroutine leaks
□ Proper mutex usage
□ go vet and golangci-lint clean
```

### Rust
```
□ No unnecessary clones
□ Proper error types (Result)
□ Lifetimes annotated correctly
□ No unsafe blocks without justification
□ Iterator chains over loops where appropriate
□ Clippy warnings addressed
```

### C#
```
□ async/await patterns correct
□ using statements for IDisposable
□ Nullable reference types enabled
□ LINQ queries efficient
□ Proper exception filtering
□ CancellationToken usage
```

### Ruby
```
□ No N+1 queries (includes/eager_load)
□ Proper error handling (rescue)
□ Bang methods for mutating operations
□ Frozen string literals
□ RuboCop clean
```

### PHP
```
□ Type declarations on parameters/returns
□ Prepared statements (no SQL injection)
□ Proper error handling (try-catch)
□ No global state
□ PSR standards followed
```

---

## Common Anti-Patterns to Flag

### Security
- Hardcoded credentials or API keys
- SQL/NoSQL injection via string interpolation
- XSS via unescaped output
- Insecure deserialization
- Missing rate limiting on public endpoints
- Overly permissive CORS configuration

### Performance
- N+1 query patterns
- Unbounded result sets (missing LIMIT)
- Synchronous operations in hot paths
- Missing caching for expensive computations
- Inefficient data structures (O(n²) where O(n log n) possible)
- Memory leaks (unclosed resources, growing caches)

### Maintainability
- God classes or functions over 50 lines
- Deep nesting (3+ levels)
- Magic numbers without constants
- Duplicated logic across files
- Tight coupling between modules
- Missing or outdated documentation

### Concurrency
- Race conditions on shared state
- Missing synchronization primitives
- Deadlock potential (lock ordering)
- Thread-unsafe collections
- Improper async/await usage

---

## Review Output Formats

### Format 1: Markdown (Default)
See [TEMPLATES.md](TEMPLATES.md) for detailed markdown templates.

### Format 2: JSON (Machine-Readable)
```json
{
  "summary": "Brief overview",
  "issues": [
    {
      "severity": "critical",
      "file": "src/auth.py",
      "line": 42,
      "category": "security",
      "message": "SQL injection vulnerability",
      "suggestion": "Use parameterized queries"
    }
  ],
  "positive_notes": ["Good use of type hints"],
  "recommendation": "approve_with_changes"
}
```

### Format 3: Checklist Report
```
Review Summary for PR #123
==========================
[✓] Correctness - 2 issues found
[✓] Security - 1 critical issue
[✓] Performance - No issues
[✓] Maintainability - 3 suggestions
[✓] Testing - Coverage adequate
[✓] Observability - Missing error context

Recommendation: Changes required before merge
```

---

## Additional Resources

- [CHECKLIST.md](CHECKLIST.md) - Comprehensive review checklist
- [TEMPLATES.md](TEMPLATES.md) - Feedback templates for various scenarios
- [examples.md](examples.md) - Real-world review examples
