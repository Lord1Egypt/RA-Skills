# Security Policy

## Overview

NIMA Core uses LadybugDB (Kùzu graph database) for memory storage. **LadybugDB does not support parameterized Cypher queries**, which means string escaping is the only defense against Cypher injection attacks.

This document outlines:
- Security constraints and risks
- Defense-in-depth strategy
- Secure coding guidelines
- How to report security vulnerabilities

## Cypher Injection Risks

### User-Controlled Data Paths

User-controlled data flows into Cypher queries through several paths:

1. **Search keywords** — from task strings via `build_agent_context()` → `query_memories()`
2. **Memory layer names** — via `HiveMind.__init__()` `memory_types_to_query` parameter
3. **Agent metadata** — agent labels, model names, and result summaries via `capture_agent_result()`

### Potential Attack Vectors

An attacker controlling these inputs could potentially:

- **Exfiltrate sensitive data** using comment injection to bypass query logic
- **Modify or delete memory nodes** using query termination and chained queries
- **Cause denial of service** through malformed queries or excessive resource consumption
- **Bypass access controls** using boolean logic injection (e.g., `' OR '1'='1`)

## Defense-in-Depth Strategy

This project implements **three layers of security** to prevent Cypher injection:

### Layer 1: String Escaping (`_escape()` function)

All user-controlled strings are escaped before interpolation into Cypher queries.

**Protected against:**
- ✅ Null bytes (`\x00`) — removed entirely (can terminate strings)
- ✅ Backslashes (`\`) — escaped to `\\` (prevents escape sequence attacks)
- ✅ Single quotes (`'`) — escaped to `\'` (Cypher string delimiter)
- ✅ Newlines/carriage returns/tabs (`\n`, `\r`, `\t`) — escaped to prevent query breaking
- ✅ Comment markers (`//`, `/*`, `*/`) — escaped to prevent comment injection

**Escape order is critical:** Backslashes must be escaped *before* quotes to prevent double-escaping vulnerabilities.

### Layer 2: Whitelist Validation (`_validate_and_escape_layers()`)

Memory layer names are validated against known types before use.

**Validation steps:**
1. **Whitelist check** — preferred known layer types: `contemplation`, `episodic`, `semantic`, `legacy_vsa`, `procedural`, `working`, `sensory`
2. **Regex validation** — fallback for custom layers: `[a-zA-Z][a-zA-Z0-9_]{0,31}`
3. **Escaping** — applied even after validation (defense-in-depth)

**Rejected patterns:**
- Layer names with special characters: `-`, `.`, `;`, `'`, `"`
- Layer names starting with numbers: `1layer`
- Layer names containing injection attempts: `test'; DROP TABLE--`
- Layer names longer than 32 characters
- Empty or whitespace-only layer names

### Layer 3: Input Type Validation

Numeric parameters are validated before interpolation.

**Example:** `get_swarm_status(hours)` function:
- Validates `hours` as integer in range `[0, 8760]` (0 to 1 year)
- Validates calculated `cutoff_ms` as positive integer
- Rejects non-numeric values and out-of-range values

## Mitigated Attack Vectors

The following attack vectors have been tested and mitigated (see `tests/test_cypher_security.py`):

| Attack Vector | Example Input | Mitigation |
|---------------|---------------|------------|
| Null byte injection | `"test\x00'; DROP TABLE--"` | Null bytes removed |
| Single-line comment | `"test// OR 1=1"` | `//` escaped to `\/\/` |
| Multi-line comment | `"test/* OR 1=1 */"` | `/*` and `*/` escaped |
| Quote escape | `"test\' OR 1=1--"` | Quotes escaped to `\'` |
| Backslash escape | `"test\\\\ OR 1=1"` | Backslashes doubled |
| Newline breaking | `"test\nMATCH (n) DELETE n"` | Newlines escaped to `\n` |
| Layer name injection | `["episodic', true); DELETE--"]` | Validation rejects invalid patterns |
| Boolean injection | `"' OR '1'='1"` | Quote escaping prevents logic bypass |

## Secure Coding Guidelines

### ✅ CORRECT: Use `_escape()` for all user-controlled strings

```python
from nima_core.hive_mind import _escape

# User input from task string
keyword = _escape(user_input)
query = f"MATCH (n) WHERE n.text CONTAINS '{keyword}' RETURN n"
```

### ✅ CORRECT: Validate and escape layer names

```python
from nima_core.hive_mind import _validate_and_escape_layers

# User-provided layer names
layers = _validate_and_escape_layers(user_layers)
layers_str = "[" + ",".join(f"'{layer}'" for layer in layers) + "]"
query = f"MATCH (n) WHERE n.layer IN {layers_str} RETURN n"
```

### ✅ CORRECT: Validate integers before interpolation

```python
import time

# Validate numeric parameter
hours_validated = int(hours)
if hours_validated < 0 or hours_validated > 8760:
    raise ValueError("hours must be in range [0, 8760]")

cutoff_ms = int((time.time() - hours_validated * 3600) * 1000)
query = f"MATCH (n) WHERE n.timestamp > {cutoff_ms} RETURN n"
```

### ❌ UNSAFE: Never interpolate user input without escaping

```python
# VULNERABLE to injection!
query = f"MATCH (n) WHERE n.text CONTAINS '{user_input}' RETURN n"
```

### ❌ UNSAFE: Never trust "sanitized" input without validation

```python
# VULNERABLE — no validation of layer names!
query = f"MATCH (n) WHERE n.layer = '{layer_name}' RETURN n"
```

### ❌ UNSAFE: Never use string concatenation for query building

```python
# VULNERABLE — concatenation bypasses security!
query = "MATCH (n) WHERE n.text CONTAINS '" + user_input + "' RETURN n"
```

## Development Checklist

When adding new Cypher queries to this codebase:

- [ ] **Identify all user-controlled inputs** — task strings, agent labels, model names, memory layers, any data from external sources
- [ ] **Apply `_escape()` to ALL string literals** — even if you think the input is "safe"
- [ ] **Use whitelist validation for enums** — if the value should be from a known set, validate against that set first
- [ ] **Validate numeric types explicitly** — use `int()` cast and range checks before interpolating
- [ ] **Never concatenate raw user input** — always escape first, validate first, or use both
- [ ] **Test with malicious inputs** — see `tests/test_cypher_security.py` for examples
- [ ] **Add security test cases** — when adding new query paths, add corresponding security tests

## Testing

Comprehensive security tests are located in `tests/test_cypher_security.py`.

Run security tests:

```bash
python -m pytest tests/test_cypher_security.py -v
```

The test suite includes:
- 42 test cases covering all injection vectors
- Tests for `_escape()` and `_escape_cypher()` functions
- Tests for `_validate_and_escape_layers()` validation
- Tests for `get_swarm_status()` parameter validation
- End-to-end security scenarios

## Reporting Security Vulnerabilities

We take security seriously. If you discover a security vulnerability:

### DO NOT open a public GitHub issue

Instead, please report security vulnerabilities privately:

1. **Email:** Send details to the project maintainers (see `MAINTAINERS` file or `pyproject.toml`)
2. **Include:**
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if available)

### What to expect

- **Acknowledgment** within 48 hours
- **Assessment** within 7 days
- **Fix timeline** communicated based on severity
- **Credit** in release notes (if desired)

### Severity Levels

- **Critical** — Remote code execution, data exfiltration, authentication bypass
- **High** — Cypher injection, privilege escalation, denial of service
- **Medium** — Information disclosure, input validation bypass
- **Low** — Best practice violations, minor information leaks

## Security Best Practices

### General Guidelines

1. **Principle of least privilege** — Grant minimal database permissions required
2. **Input validation everywhere** — Validate at entry points AND before use
3. **Defense-in-depth** — Multiple security layers reduce risk of single-point failures
4. **Fail securely** — On validation failure, reject the request (don't sanitize)
5. **Security testing** — Add test cases for each new attack vector discovered
6. **Code review** — All Cypher query changes require security-focused code review

### Database Configuration

- Use separate database instances for dev/staging/production
- Limit database file permissions to application user only
- Monitor for unusual query patterns or excessive resource usage
- Regularly back up memory databases

### Monitoring

Consider monitoring for:
- Unusually long query execution times
- High volume of failed queries
- Queries with escaped special characters (may indicate attack attempts)
- Unexpected database file size growth

## References

- **Cypher Query Language:** [https://opencypher.org/](https://opencypher.org/)
- **LadybugDB (Kùzu):** [https://kuzudb.com/](https://kuzudb.com/)
- **OWASP Injection Prevention:** [https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html](https://cheatsheetseries.owasp.org/cheatsheets/Injection_Prevention_Cheat_Sheet.html)

## Documentation

For detailed implementation documentation, see:
- `nima_core/hive_mind.py` — Module-level security documentation
- `tests/test_cypher_security.py` — Security test suite
- This file (`SECURITY.md`) — Security policy and guidelines

---

**Last Updated:** 2026-03-12
**Security Review Required:** When adding new Cypher queries or modifying escape functions
