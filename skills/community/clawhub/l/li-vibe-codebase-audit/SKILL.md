# 🔒 Vibe Codebase Audit - Multi-Agent Security Audit Skill

**Comprehensive security auditing for AI-generated codebases** - Automated vulnerability scanning and multi-model AI consensus auditing.

> Supports OpenCode, Hermes, OpenClaw, and other agentic AI systems with standardized MCP tool interface.

---

## ⭐ NEW: Enhanced Features (v2.0)

### 🤖 Agent-Native Audit (Zero Setup!)
- **No API key required!** Use your current agent's LLM connection directly
- Seamlessly integrates with OpenCode, Hermes, OpenClaw
- Leverages existing context and capabilities
- Lower cost, better integration

### 🔌 Multi-Provider Support
- **Agent LLM** (Primary) - Use current agent's connection
- **OpenAI** - GPT-4, GPT-4-turbo, and compatible APIs
- **Claude** - Claude-3 Sonnet/Opus
- **DeepSeek** - Cost-effective alternative
- **Qwen/Tongyi** - Alibaba's models
- **Ollama** - Run local models (Llama2, Mistral, etc.)
- **OpenRouter** - Access to 100+ models

### 📦 Dependency Security Scanning
- Check for known vulnerabilities (CVE)
- Detect outdated dependencies
- License compliance checking
- Support for npm, pip, maven, cargo, go mod

### ⚙️ Configuration Security Checks
- Exposed .env file detection
- CORS misconfiguration detection
- Authentication configuration review
- Debug mode detection

### 🚀 Performance Features
- **Smart Caching** - Don't re-scan unchanged files
- **Incremental Audit** - Only audit changed files
- **Diff Audit** - Compare security state between commits
- **Parallel Processing** - Multi-threaded scanning
- **History Tracking** - Monitor security trends

### 🛡️ Custom Rule Engine
- Define custom security patterns
- YAML/JSON rule definitions
- Severity customization
- Project-specific rules

---

## 📋 Skill Overview

This skill provides comprehensive security auditing capabilities for "vibe coded" projects (AI-generated code) through multiple approaches:

1. **Automated Pattern Scanning** - Fast local analysis for common security issues
2. **Multi-Model AI Consensus** - Independent review by multiple AI models
3. **Agent-Native Audit** - Use current agent's LLM (NEW!)
4. **Dependency Scanning** - Check for vulnerable dependencies (NEW!)
5. **Configuration Audit** - Check for config security issues (NEW!)

**Use Cases:**
- Pre-publish security audits for open-source projects
- CI/CD integration for continuous security monitoring
- AI-generated code validation before deployment
- Compliance checking for security standards

---

## 🎯 What This Skill Detects

### Secrets & Credentials
- ✅ API keys (OpenAI, Anthropic, AWS, GitHub, etc.)
- ✅ Authentication tokens and bearer tokens
- ✅ Database credentials and passwords
- ✅ SSH keys and certificates
- ✅ OpenRouter API keys

### Personal Data Exposure
- ✅ Email addresses
- ✅ Phone numbers
- ✅ SSN and credit card numbers
- ✅ File paths revealing user directories
- ✅ Obsidian vault references

### Security Vulnerabilities
- ✅ Command injection risks
- ✅ SQL injection patterns
- ✅ Path traversal vulnerabilities
- ✅ Unsafe deserialization
- ✅ Weak cryptography usage
- ✅ Debug mode enabled

### Code Quality Issues
- ✅ Security-related TODOs/FIXMEs
- ✅ Incomplete security implementations

---

## 🛠️ Available Tools

### 1. `vibe_audit_scan` - Automated Pattern Scanner

**Description:** Fast local security scan using pattern matching and static analysis.

**Parameters:**
- `project_path` (string, required): Path to the project directory to audit
- `output_format` (string, optional): Report format - "json", "markdown", or "console" (default: "json")
- `severity_threshold` (number, optional): Minimum severity to report (1-5, default: 3)

**Returns:**
```json
{
  "risk_score": 0-100,
  "risk_level": "SAFE|LOW|MEDIUM|HIGH|CRITICAL",
  "total_findings": number,
  "findings_by_severity": {
    "critical": number,
    "high": number,
    "medium": number,
    "low": number
  },
  "detailed_findings": [...]
}
```

**Risk Score Calculation:**
- Critical findings: 20 points each
- High findings: 10 points each
- Medium findings: 5 points each
- Low findings: 2 points each

**Example Usage:**
```python
# In OpenCode/Hermes/OpenClaw
result = vibe_audit_scan(
    project_path="/path/to/project",
    output_format="markdown",
    severity_threshold=3
)
```

---

### 2. `vibe_audit_multi_model` - AI Consensus Auditor

**Description:** Multi-model AI audit using Claude, GPT-4, and Gemini via OpenRouter API.

**Parameters:**
- `project_path` (string, required): Path to the project directory to audit
- `models` (array of strings, optional): AI models to use - default: ["claude", "gpt4", "gemini"]
- `openrouter_api_key` (string, optional): OpenRouter API key (or use env var OPENROUTER_API_KEY)
- `consensus_mode` (string, optional): How to determine consensus - "conservative" (max score) or "average" (default: "conservative")

**Returns:**
```json
{
  "consensus_risk_score": 0-100,
  "consensus_risk_level": "SAFE|LOW|MEDIUM|HIGH|CRITICAL",
  "private_data_found": boolean,
  "publish_safe": "YES|NO|WITH_FIXES",
  "model_results": {
    "claude": {...},
    "gpt4": {...},
    "gemini": {...}
  },
  "all_findings": [...]
}
```

**Prerequisites:**
- OpenRouter API key (set as `OPENROUTER_API_KEY` environment variable)
- Internet connection for API calls

**Example Usage:**
```python
result = vibe_audit_multi_model(
    project_path="/path/to/project",
    models=["claude", "gpt4"],
    consensus_mode="conservative"
)
```

---

### 3. `vibe_audit_full` - Complete Security Workflow

**Description:** Automated scan followed by multi-model consensus audit.

**Parameters:**
- `project_path` (string, required): Path to the project directory to audit
- `auto_fix_suggestions` (boolean, optional): Generate fix suggestions for findings (default: true)

**Returns:**
Combined results from both audit methods plus actionable recommendations.

**Workflow:**
1. Run automated scan
2. If risk_score > 20, flag for review
3. Run multi-model audit
4. Generate comprehensive report with fix suggestions

---

## 📊 Understanding Risk Levels

| Risk Level | Score Range | Action Required |
|-----------|-------------|-----------------|
| ✅ **SAFE** | 0-19 | Safe to publish |
| 🟡 **LOW** | 1-19 | Minor issues, review recommended |
| 🟠 **MEDIUM** | 20-49 | Review and fix issues before publishing |
| 🔴 **HIGH** | 50-79 | Significant issues, fixes required |
| ⛔ **CRITICAL** | 80-100 | DO NOT PUBLISH - severe security risks |

---

## 🔧 Agent Integration

### OpenCode Integration
```json
{
  "tools": ["vibe_audit_scan", "vibe_audit_multi_model", "vibe_audit_full"],
  "context": "security_audit",
  "auto_invoke": "pre_publish"
}
```

### Hermes Integration
```yaml
skill: li_vibe_codebase-audit
capabilities:
  - static_analysis
  - multi_model_consensus
  - security_patterns
triggers:
  - pre_commit
  - pre_publish
```

### OpenClaw Integration
```python
from skills import VibeCodebaseAudit

audit = VibeCodebaseAudit()
result = audit.scan("/project/path", mode="full")
```

### Generic MCP Integration
All tools follow the MCP (Model Context Protocol) specification:
- Input schema validation
- Structured output format
- Error handling with context
- Tool discovery metadata

---

## 🎓 Recommended Workflow

### Step 1: Initial Scan
```
vibe_audit_scan(project_path=".")
```
Review findings. If risk_score > 20, investigate flagged issues.

### Step 2: Fix Critical Issues
- Remove API keys and secrets
- Redact personal file paths
- Address security vulnerabilities

### Step 3: Multi-Model Validation
```
vibe_audit_multi_model(project_path=".")
```
Get AI consensus on publish-readiness.

### Step 4: Final Review
- Check that all models agree (or understand disagreements)
- Verify "private_data_found: false"
- Confirm "publish_safe: YES"

### Step 5: Publish
Once all audits pass, publish with confidence.

---

## 🔐 Privacy & Security

### Automated Scan (vibe_audit_scan)
- ✅ Runs entirely locally
- ✅ No data transmitted
- ✅ No external dependencies

### Multi-Model Audit (vibe_audit_multi_model)
- ⚠️ Code sent to AI providers via OpenRouter
- ⚠️ Use ONLY on code you're comfortable sharing
- ⚠️ OpenRouter privacy policy applies
- 💡 **Best practice:** Run automated scan first, fix issues, THEN run multi-model audit

---

## 📝 Output Formats

### JSON Format
Structured data for programmatic use and CI/CD integration.

### Markdown Format
Human-readable report for documentation and review.

### Console Format
Colored terminal output for interactive use.

---

## ⚙️ Configuration

### Environment Variables
```bash
# Required for multi-model audit
export OPENROUTER_API_KEY="sk-or-v1-..."

# Optional: customize behavior
export VIBE_AUDIT_VERBOSE=true
export VIBE_AUDIT_MAX_FILE_SIZE=1000000  # 1MB default
```

### Custom Patterns
Add project-specific security patterns:
```json
{
  "custom_patterns": {
    "MyAPI Key": "my_api_key_pattern_here",
    "Internal Token": "internal_token_regex"
  }
}
```

### Ignored Paths
Default ignored directories:
- `.git/`, `node_modules/`, `__pycache__/`
- `.DS_Store`, `venv/`, `.venv/`
- `dist/`, `build/`

---

## 🚀 Advanced Features

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Security Audit
  run: |
    vibe_audit_scan project_path="." output_format="json"
    if [ $(jq '.risk_score' audit-report.json) -gt 50 ]; then
      echo "Risk score too high!"
      exit 1
    fi
```

### Batch Processing
```python
projects = ["~/project1", "~/project2", "~/project3"]
for project in projects:
    result = vibe_audit_full(project_path=project)
    print(f"{project}: {result['risk_level']}")
```

### Custom Severity Thresholds
```python
# Only report HIGH and CRITICAL issues
result = vibe_audit_scan(
    project_path=".",
    severity_threshold=4  # 4=HIGH, 5=CRITICAL
)
```

---

## 🤝 Supported Agents

| Agent | Integration Type | Features |
|-------|-----------------|----------|
| **OpenCode** | Native skill | All tools, auto-discovery |
| **Hermes** | Plugin | Static analysis, consensus |
| **OpenClaw** | Module | Full API, custom workflows |
| **Generic MCP** | Protocol | Standard MCP interface |
| **Claude** | Tool calling | Via OpenRouter integration |
| **GPT-4** | Tool calling | Via OpenRouter integration |
| **Gemini** | Tool calling | Via OpenRouter integration |

---

## 📚 Examples

### Example 1: Pre-Publish Audit
```python
# Quick check before publishing
result = vibe_audit_scan(project_path=".")
if result['risk_score'] > 20:
    print("⚠️ Issues found - review before publishing")
    for finding in result['detailed_findings']:
        print(f"- {finding['severity']}: {finding['issue']}")
else:
    print("✅ Safe to publish")
```

### Example 2: CI/CD Gate
```yaml
# Block deployment if critical issues found
- vibe_audit_scan(project_path=".")
- condition: result.risk_level != "CRITICAL"
  then: deploy()
  else: alert_team()
```

### Example 3: Multi-Model Validation
```python
# Get consensus from multiple AI models
result = vibe_audit_multi_model(
    project_path=".",
    models=["claude", "gpt4", "gemini"],
    consensus_mode="conservative"
)

if result['publish_safe'] == "YES":
    publish()
elif result['publish_safe'] == "WITH_FIXES":
    apply_fixes(result['required_fixes'])
    re_audit()
else:
    halt_publish()
```

---

## 🎯 Real-World Scenarios

### Scenario 1: Tea App Incident Prevention
The 2023 Tea dating app incident (database credentials leaked in public repo) would have been prevented:
1. `vibe_audit_scan` would flag database credentials immediately
2. Risk score would be CRITICAL (80+)
3. Developer alerted before publishing

### Scenario 2: Obsidian Vault Leak
Developer uses AI to generate code that references their Obsidian notes:
1. `vibe_audit_scan` detects `/Users/name/obsidian/vault` paths
2. Multi-model audit confirms private data exposure
3. Paths redacted before publishing

### Scenario 3: API Key in Config
AI-generated code includes hardcoded API key:
1. Automated scan detects `sk-or-v1-...` pattern
2. Severity: CRITICAL (API key exposure)
3. Fix suggestion: Use environment variable instead

---

## 🔍 Troubleshooting

### Common Issues

**Issue:** "No files found to scan"
- **Cause:** Path doesn't exist or all files are ignored
- **Fix:** Check path validity and ignored patterns

**Issue:** "OPENROUTER_API_KEY not set"
- **Cause:** Multi-model audit requires API key
- **Fix:** Set environment variable or pass key directly

**Issue:** "Risk score seems too high"
- **Cause:** False positives from example/placeholder values
- **Fix:** Review findings - example keys have reduced severity

**Issue:** "Models disagree on risk level"
- **Cause:** Different security perspectives
- **Fix:** Use "conservative" consensus mode (takes highest risk)

---

## 📖 Additional Resources

- **GitHub Repository:** [vibe-codebase-audit](https://github.com/csmoove530/vibe-codebase-audit)
- **OpenRouter Docs:** [openrouter.ai/docs](https://openrouter.ai/docs)
- **MCP Specification:** [modelcontextprotocol.io](https://modelcontextprotocol.io)
- **Security Best Practices:** [OWASP Top 10](https://owasp.org/www-project-top-ten/)

---

## 📜 License

MIT License - Use freely for personal and commercial projects.

---

## 🎯 Roadmap

Future enhancements:
- [ ] GUI interface for non-technical users
- [ ] VS Code extension for real-time scanning
- [ ] Pre-commit hooks for automatic auditing
- [ ] Additional AI model support
- [ ] Custom reporting templates
- [ ] Team/enterprise features

---

**Ship with confidence. Audit with rigor. Vibe in peace.** 🚀

---

## 💡 Quick Reference

| Tool | Speed | Accuracy | Best For |
|------|-------|----------|----------|
| `vibe_audit_scan` | Fast (seconds) | Pattern-based | Quick checks, CI/CD |
| `vibe_audit_multi_model` | Slower (minutes) | AI-powered | Pre-publish validation |
| `vibe_audit_full` | Comprehensive | Both methods | Complete workflow |

**Choose based on your needs:**
- Quick check → `vibe_audit_scan`
- Thorough validation → `vibe_audit_multi_model`
- Complete audit → `vibe_audit_full`
