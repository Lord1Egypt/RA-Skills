# Code Quality Reviewer Agent Task

**Target:** {{TARGET}}

## Mission
Identify security vulnerabilities, code smells, and dependency issues.

## Checks

1. **Static Analysis:**
   - Shell scripts: `shellcheck` for bash vulnerabilities
   - JavaScript/Node: `eslint` security rules
   - Python: unsafe functions, SQL injection patterns

2. **Dependencies:**
   - Outdated packages (`npm audit`, `pip check`)
   - Known CVEs in dependencies
   - Packages with security advisories

3. **Code Patterns:**
   - `eval()`, `exec()` without sanitization
   - SQL queries with string concatenation
   - File operations on user input
   - Unsafe deserialization

4. **Best Practices:**
   - Error handling (try/catch, exit codes)
   - Input validation
   - Proper use of `set -e` in bash scripts

## Commands to Run

```bash
cd {{TARGET}}

# Shellcheck (if .sh files exist)
find . -name "*.sh" -exec shellcheck {} \; 2>&1 || true

# NPM audit (if package.json exists)
[ -f package.json ] && npm audit --audit-level=moderate || true

# Pattern scan for unsafe code
grep -r -E "(eval\(|exec\(|os\.system|subprocess\.call)" . \
  --exclude-dir=node_modules \
  2>/dev/null || true
```

## Output Format

**CRITICAL:** SQL injection vulnerability in file X
**HIGH:** Unsafe eval() usage at line Y
**MEDIUM:** Dependency with known CVE
**LOW:** Missing error handling

If no issues: **✅ Code quality passed**
