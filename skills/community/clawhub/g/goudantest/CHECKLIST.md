# Comprehensive Code Review Checklist

Use this checklist for systematic code review. Copy and track progress by marking items with `[x]`.

---

## 1. Correctness (逻辑正确性)

### Core Logic
- [ ] Business logic matches requirements/specifications
- [ ] Edge cases handled (empty input, null values, boundary conditions)
- [ ] Error conditions properly detected and handled
- [ ] No off-by-one errors in loops or array access
- [ ] State transitions are valid and complete
- [ ] Return values are correct and consistent

### Data Integrity
- [ ] Database transactions used where needed
- [ ] Data validation at system boundaries (API inputs, file parsing)
- [ ] No data loss in transformations
- [ ] Idempotency considered for retry scenarios
- [ ] Proper handling of partial failures

### Concurrency
- [ ] Thread-safe access to shared mutable state
- [ ] No race conditions in async operations
- [ ] Deadlock prevention (consistent lock ordering)
- [ ] Proper use of synchronization primitives
- [ ] Context cancellation handled in long-running operations

---

## 2. Security (安全性)

### Authentication & Authorization
- [ ] Authentication required for protected resources
- [ ] Authorization checks at every access point
- [ ] Principle of least privilege applied
- [ ] Role-based access control properly implemented
- [ ] Token/session expiration handled

### Injection Prevention
- [ ] SQL/NoSQL queries use parameterized statements
- [ ] Command injection prevented (no shell execution with user input)
- [ ] XSS prevention (output encoding, CSP headers)
- [ ] LDAP/XML injection prevented
- [ ] Template injection prevented

### Data Protection
- [ ] Sensitive data encrypted at rest and in transit
- [ ] No hardcoded secrets, API keys, or credentials
- [ ] Proper password hashing (bcrypt, argon2, scrypt)
- [ ] PII handled according to regulations (GDPR, etc.)
- [ ] Logging does not expose sensitive information

### Input Validation
- [ ] All external input validated and sanitized
- [ ] File uploads: type, size, and content validation
- [ ] Rate limiting on public endpoints
- [ ] Request size limits enforced
- [ ] Deserialization from untrusted sources prevented or restricted

### Dependency Security
- [ ] Dependencies up-to-date (no known CVEs)
- [ ] No unnecessary dependencies
- [ ] Supply chain security considered (lockfiles, integrity checks)

---

## 3. Performance (性能)

### Algorithm Efficiency
- [ ] Time complexity appropriate for expected data sizes
- [ ] Space complexity reasonable (no memory leaks)
- [ ] No unnecessary repeated computations
- [ ] Appropriate data structures chosen
- [ ] Caching used effectively for expensive operations

### Database & I/O
- [ ] No N+1 query patterns
- [ ] Queries use appropriate indexes
- [ ] Result sets bounded (LIMIT clauses where needed)
- [ ] Batch operations used for bulk data
- [ ] Connection pooling configured
- [ ] Unnecessary I/O operations eliminated

### Network & API
- [ ] Pagination for large result sets
- [ ] Compression enabled for large responses
- [ ] Timeout values configured appropriately
- [ ] Retry logic with exponential backoff
- [ ] Circuit breakers for external dependencies
- [ ] Async operations where blocking is unnecessary

### Resource Management
- [ ] File handles, network connections properly closed
- [ ] Memory-intensive operations stream data
- [ ] Thread pools sized appropriately
- [ ] No resource leaks in error paths

---

## 4. Maintainability (可维护性)

### Code Organization
- [ ] Functions are focused and small (< 50 lines preferred)
- [ ] Classes have single responsibility
- [ ] Module boundaries are logical
- [ ] No circular dependencies
- [ ] Configuration separated from code

### Readability
- [ ] Variable and function names are descriptive
- [ ] No deep nesting (3+ levels)
- [ ] Early returns used to reduce nesting
- [ ] Complex logic is broken into smaller functions
- [ ] Magic numbers replaced with named constants
- [ ] Comments explain "why", not "what"

### DRY (Don't Repeat Yourself)
- [ ] No duplicated logic across files
- [ ] Common patterns extracted into utilities
- [ ] Templates used for repeated structures
- [ ] Configuration centralized

### Documentation
- [ ] Public APIs have docstrings/comments
- [ ] Complex algorithms documented
- [ ] Architectural decisions recorded (ADRs)
- [ ] README updated if needed
- [ ] Inline comments for non-obvious code

### Code Style
- [ ] Follows project style guide
- [ ] Linter warnings addressed
- [ ] Formatter applied consistently
- [ ] Import statements organized

---

## 5. Observability (可观测性)

### Logging
- [ ] Appropriate log levels used (DEBUG, INFO, WARN, ERROR)
- [ ] Error logs include context (user ID, request ID, input data)
- [ ] No sensitive data in logs
- [ ] Structured logging format (JSON)
- [ ] Log correlation IDs for distributed tracing

### Metrics
- [ ] Key business metrics tracked
- [ ] Performance metrics (latency, throughput, error rates)
- [ ] Resource utilization metrics (CPU, memory, connections)
- [ ] Custom metrics for critical operations

### Error Handling
- [ ] Errors are caught and handled appropriately
- [ ] Error messages are user-friendly
- [ ] Internal errors logged with stack traces
- [ ] Graceful degradation on failures
- [ ] Retry logic for transient failures

### Debugging Support
- [ ] Health check endpoints implemented
- [ ] Readiness and liveness probes configured
- [ ] Feature flags for risky changes
- [ ] Debug endpoints (protected) for diagnostics

---

## 6. Testing (测试)

### Coverage
- [ ] Unit tests for new/modified logic
- [ ] Integration tests for cross-component interactions
- [ ] End-to-end tests for critical user journeys
- [ ] Edge cases tested
- [ ] Error paths tested

### Test Quality
- [ ] Tests are readable and maintainable
- [ ] Test names describe expected behavior
- [ ] No flaky tests (deterministic)
- [ ] Mocks/stubs used appropriately
- [ ] Tests validate behavior, not implementation

### Test Data
- [ ] Tests don't depend on external state
- [ ] Test data is isolated and cleaned up
- [ ] No hardcoded credentials in tests
- [ ] Property-based tests for complex logic (if applicable)

---

## 7. Deployment & Operations (部署与运维)

### Configuration
- [ ] Environment-specific config externalized
- [ ] Secrets managed via secret manager (not in code)
- [ ] Feature flags for gradual rollout
- [ ] Default values sensible

### Backward Compatibility
- [ ] API changes are backward compatible
- [ ] Database migrations are reversible
- [ ] Old code paths cleaned up after migration
- [ ] Deprecation notices for removed features

### Rollback Plan
- [ ] Changes can be safely rolled back
- [ ] Database migrations tested for rollback
- [ ] No destructive changes without backup

---

## Quick Severity Reference

When flagging issues, use these guidelines:

| Severity | Examples | Action |
|----------|----------|--------|
| **Blocker** | Security vulnerability, data corruption, crash | Must fix before merge |
| **Critical** | Logic bug, missing validation, resource leak | Must fix before merge |
| **Warning** | Code smell, suboptimal pattern, missing tests | Should address soon |
| **Suggestion** | Style issue, minor improvement, refactoring opportunity | Consider |
| **Info** | Observation, documentation note | Optional |

---

## Review Output Template

After completing the checklist, summarize findings:

```markdown
## Review Summary

**Files Changed**: X files, Y lines added, Z lines removed
**Risk Level**: High / Medium / Low
**Review Depth**: Comprehensive / Focused / Light

### Issues Found
-🔴: N issues
-: N issues
-💡uggestion: N issues

### Recommendation
- [ ] Approve - No issues found
- [ ] Approve with minor changes - Suggestions only
- [ ] Request changes - Warnings or critical issues found
- [ ] Reject - Blocker issues or fundamental design problems

### Key Concerns
[List any major issues that need attention]

### Positive Notes
[List what was done well]
```
