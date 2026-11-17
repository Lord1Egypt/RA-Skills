# 🔒 Vibe Codebase Audit Skill - Enhanced Version

**Comprehensive security auditing for AI-generated codebases with agent integration**

> 🎉 **NEW in v2.0**: Agent-native audit, multi-provider support, dependency scanning, and more!

---

## ⚡ Quick Start

### Method 1: Agent-Native Audit (Recommended, Zero Setup!)

```python
# No API key needed! Uses your current agent's LLM
from vibe_audit_enhanced import vibe_audit_enhanced

result = await vibe_audit_enhanced(
    project_path="/path/to/project",
    primary_provider="agent_llm"  # Use current agent's LLM
)
```

### Method 2: With Your API Key

```python
# Use your own OpenAI/Claude/Other API
result = await vibe_audit_enhanced(
    project_path="/path/to/project",
    primary_provider="openai",  # or "claude", "ollama", "deepseek"
    fallback_provider="claude"
)
```

### Method 3: CLI Usage

```bash
# Use agent's LLM (no API key needed)
python vibe_audit_enhanced.py /path/to/project --provider agent_llm

# Use OpenAI
python vibe_audit_enhanced.py /path/to/project --provider openai

# Use local Ollama model
python vibe_audit_enhanced.py /path/to/project --provider ollama

# Incremental audit (only changed files)
python vibe_audit_enhanced.py /path/to/project --incremental --base-branch main
```

---

## 🆕 What's New in v2.0

### 1. 🤖 Agent-Native Integration
- **Zero setup required** - No API key needed
- Uses your current agent's LLM connection
- Seamless integration with OpenCode, Hermes, OpenClaw
- Lower cost - leverage existing agent subscription

### 2. 🔌 Multi-Provider Support
- **Agent LLM** - Use current agent (recommended)
- **OpenAI** - GPT-4, GPT-4-turbo
- **Claude** - Claude-3 Sonnet/Opus
- **DeepSeek** - Cost-effective alternative
- **Qwen/Tongyi** - Alibaba's models
- **Ollama** - Run local models (free!)
- **OpenRouter** - Access 100+ models

### 3. 📦 Dependency Security Scanning
- Check for known vulnerabilities (CVE)
- Detect outdated dependencies
- License compliance checking
- Support: npm, pip, maven, cargo, go mod

### 4. ⚙️ Configuration Security Checks
- Exposed .env file detection
- CORS misconfiguration detection
- Debug mode detection
- SSL verification checks

### 5. 🚀 Performance Features
- **Smart Caching** - Don't re-scan unchanged files
- **Incremental Audit** - Only audit changed files
- **Diff Audit** - Compare security between commits
- **Parallel Processing** - Faster scanning

### 6. 🛡️ Custom Rule Engine
- Define your own security patterns
- YAML/JSON rule definitions
- Project-specific rules

---

## 📊 Tool Comparison

| Tool | Speed | Accuracy | Features | API Key | Best For |
|------|-------|----------|----------|---------|----------|
| `vibe_audit_enhanced` | Medium-Fast | High | All features | Optional | **Production** |
| `vibe_audit_scan` | Fast | Medium | Basic | No | Quick checks |
| `vibe_audit_multi_model` | Slow | Highest | AI consensus | Yes | Critical projects |
| `vibe_audit_incremental` | Very Fast | Medium | Git-aware | Optional | CI/CD |

**Recommendation**: Use `vibe_audit_enhanced` with `primary_provider="agent_llm"`

---

## 🎯 Use Cases

### Pre-Publish Security Audit
```python
result = await vibe_audit_enhanced(
    project_path="/path/to/project",
    primary_provider="agent_llm",
    enable_dependency_scan=True,
    enable_config_scan=True
)

if result['summary']['risk_level'] in ['CRITICAL', 'HIGH']:
    print("⛔ DO NOT PUBLISH - Critical security issues found!")
    for finding in result['findings']:
        print(f"  - {finding['severity']}: {finding['issue']}")
else:
    print("✅ Safe to publish!")
```

### CI/CD Integration
```yaml
# GitHub Actions example
- name: Security Audit
  run: |
    python vibe_audit_enhanced.py . \
      --provider agent_llm \
      --incremental \
      --base-branch main
    
- name: Check Results
  run: |
    if [ $(jq '.summary.risk_score' audit-report.json) -gt 50 ]; then
      echo "Risk score too high!"
      exit 1
    fi
```

### PR Security Review
```python
# Only audit changed files
result = vibe_audit_incremental(
    project_path="/path/to/project",
    base_branch="main"
)

# Audit the changed files
for file in result['changed_files']:
    print(f"Checking {file}...")
```

---

## 🔧 Configuration

### Basic Configuration (.vibe-audit.yaml)

```yaml
version: "1.0"

audit:
  primary_provider: agent_llm
  fallback_provider: openai
  cache_enabled: true
  parallel_workers: 4

providers:
  openai:
    api_key: "${OPENAI_API_KEY}"
    model: "gpt-4"
  
  ollama:
    base_url: "http://localhost:11434"
    model: "llama2"

dependency:
  enabled: true
  check_vulnerabilities: true

config:
  enabled: true
  check_env_files: true
```

### Custom Security Rules (custom-rules.yaml)

```yaml
rules:
  - id: CUSTOM_001
    name: "Dangerous Function Usage"
    severity: high
    patterns:
      - pattern: "eval\\s*\\("
        message: "eval() can lead to code injection"
        recommendation: "Use JSON.parse() instead"
```

---

## 🌐 Provider Setup

### Agent LLM (Recommended)
```python
# No setup needed! Just use:
primary_provider="agent_llm"
```

### OpenAI
```bash
export OPENAI_API_KEY="sk-..."
# Optional: export OPENAI_MODEL="gpt-4-turbo"
```

### Claude
```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### DeepSeek
```bash
export DEEPSEEK_API_KEY="sk-..."
```

### Qwen/Tongyi
```bash
export DASHSCOPE_API_KEY="sk-..."
```

### Ollama (Local, Free)
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull model
ollama pull llama2

# Use in audit
primary_provider="ollama"
```

---

## 📈 Performance Optimization

### Enable Caching (Default: On)
```python
result = await vibe_audit_enhanced(
    project_path="/path/to/project",
    use_cache=True  # Cache results for 7 days
)
```

### Incremental Audit
```python
# Only audit files changed since last commit
result = vibe_audit_incremental(
    project_path="/path/to/project",
    base_branch="main"
)
```

### Clear Cache
```python
from vibe_audit_enhanced import AuditCache

cache = AuditCache()
cache.clear()
```

---

## 🔍 Detection Capabilities

### Secrets & Credentials
- ✅ API keys (OpenAI, Anthropic, AWS, GitHub, etc.)
- ✅ Authentication tokens
- ✅ Database credentials
- ✅ SSH keys and certificates
- ✅ JWT secrets
- ✅ AWS credentials patterns

### Security Vulnerabilities
- ✅ SQL injection patterns
- ✅ Command injection risks
- ✅ XSS patterns
- ✅ Path traversal
- ✅ Weak cryptography
- ✅ CSRF issues

### Dependency Security (NEW)
- ✅ Known CVE vulnerabilities
- ✅ Outdated packages
- ✅ License compliance
- ✅ npm audit integration
- ✅ pip audit integration

### Configuration Security (NEW)
- ✅ Exposed .env files
- ✅ CORS misconfigurations
- ✅ Debug mode enabled
- ✅ SSL verification disabled
- ✅ Hardcoded IPs

---

## 📝 Output Formats

### JSON (Default)
```python
output_format="json"
```

### Markdown
```python
output_format="markdown"
# Results include formatted markdown report
```

### HTML
```python
output_format="html"
# Interactive HTML report with styling
```

---

## 🚨 Risk Levels

| Level | Score | Action |
|-------|-------|--------|
| ✅ SAFE | 0 | Safe to publish |
| 🟢 LOW | 1-19 | Minor issues, review recommended |
| 🟡 MEDIUM | 20-49 | Review and fix before publishing |
| 🟠 HIGH | 50-79 | Significant issues, fixes required |
| 🔴 CRITICAL | 80-100 | **DO NOT PUBLISH** |

---

## 🤝 Supported Agents

| Agent | Integration | Setup | Best For |
|-------|-------------|-------|----------|
| **OpenCode** | Native skill | Auto | Seamless workflow |
| **Hermes** | Plugin | Add to plugins | Pre-commit checks |
| **OpenClaw** | Module import | Import directly | Custom workflows |
| **MCP Clients** | Protocol | Configure server | Standard integration |

---

## 📚 Documentation

- **SKILL.md** - Comprehensive documentation
- **IMPROVEMENT_ANALYSIS.md** - Feature analysis and roadmap
- **vibe-audit-config.yaml** - Configuration template
- **custom-rules-example.yaml** - Custom rules examples

---

## 🆘 Migration Guide

### From v1.x to v2.0

**Old (v1.x):**
```python
result = vibe_audit_multi_model(
    project_path="/path/to/project",
    openrouter_api_key="sk-or-..."
)
```

**New (v2.0):**
```python
result = await vibe_audit_enhanced(
    project_path="/path/to/project",
    primary_provider="agent_llm",  # No API key needed!
    enable_dependency_scan=True,   # New feature
    enable_config_scan=True        # New feature
)
```

**Benefits:**
- ✅ No API key needed
- ✅ Dependency scanning included
- ✅ Configuration checks included
- ✅ Better caching
- ✅ More provider options

---

## 🎯 Best Practices

1. **For OpenCode/Hermes/OpenClaw**: Use `primary_provider="agent_llm"`
2. **For CI/CD**: Use incremental audit + caching
3. **For Critical Projects**: Use multi-provider with consensus
4. **For Large Codebases**: Enable caching + parallel processing
5. **For Teams**: Create custom rules for project-specific requirements

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/csmoove530/vibe-codebase-audit/issues)
- **Documentation**: See SKILL.md for details
- **Examples**: See examples/ directory

---

**Ship with confidence. Audit with rigor. Vibe in peace.** 🚀
