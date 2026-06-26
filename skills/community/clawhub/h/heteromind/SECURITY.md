# Security & Safety Documentation

## Overview

HeteroMind is a powerful knowledge QA system that can:
- Generate and execute SQL queries against databases
- Generate and execute SPARQL queries against knowledge graphs
- Generate and execute Python (pandas) code for table analysis
- Scan local file systems for table data
- Connect to external LLM APIs and SPARQL endpoints

This document describes the security model, risks, and mitigation measures.

---

## Threat Model

### Assets at Risk

| Asset | Risk | Impact |
|-------|------|--------|
| **Database Credentials** | Theft via logs/output | Unauthorized data access |
| **API Keys** | Leakage in generated code | Account compromise, billing fraud |
| **Local Files** | Unauthorized read access | Data exfiltration |
| **Network Endpoints** | Unrestricted access | Data leakage, resource abuse |

### Attack Vectors

1. **Prompt Injection** - Malicious input causing unintended queries
2. **Credential Leakage** - API keys exposed in output or logs
3. **SQL Injection** - Generated SQL with injection vulnerabilities
4. **Path Traversal** - File scanning accessing unintended directories
5. **Code Injection** - Generated Python code with malicious payloads

---

## Security Controls

### 1. Credential Protection

**Implementation:** `src/utils/api_security.py`

```python
# All outputs are sanitized
from src.utils.api_security import sanitize_output

safe_output = sanitize_output(llm_response)

# API keys validated before use
from src.utils.api_security import validate_no_api_key_in_response

if validate_no_api_key_in_response(generated_code):
    execute(generated_code)
```

**Best Practices:**
- Never hardcode credentials in code or config files
- Use environment variables exclusively
- Rotate API keys regularly
- Use read-only database credentials when possible

### 2. Sandboxed Execution

**Python Code Execution:**
```python
# Restricted scope - no arbitrary imports
safe_scope = {
    "df": dataframe,
    "pd": pandas,  # Only pandas, no os/sys/subprocess
    "np": numpy,
}

# Execute in restricted scope
exec(generated_code, safe_scope)
```

**SQL Execution:**
- Read-only queries only (SELECT)
- DDL/DML operations (DROP, DELETE, UPDATE) blocked
- Query timeout enforced (default: 30s)

### 3. User Consent

**Auto-Execution Control:**

```yaml
# config/source_detection.yaml
auto_execute: false         # Default: disabled
require_confirmation: true  # Default: enabled

thresholds:
  high_confidence: 0.95     # Very conservative
```

**Confirmation Flow:**
```
Query: "Show all employees"
Detection Confidence: 0.87

⚠️  Confidence below threshold (0.95)
Generated SQL: SELECT * FROM employees

Proceed with execution? [y/N]
```

### 4. File Access Restrictions

**Default Configuration:**
```yaml
entity_verification:
  tables:
    enabled: false          # Disabled by default
    paths: []               # No automatic paths
    explicit_paths_only: true
```

**Explicit Path Configuration:**
```yaml
entity_verification:
  tables:
    enabled: true
    paths:
      - "/home/user/data/sales_2024.csv"  # Explicit file, no wildcards
    max_file_size_mb: 10
```

### 5. Audit Logging

**Log Configuration:**
```yaml
logging:
  level: "INFO"
  log_layer_outputs: true
  log_verification_details: true
  log_generated_queries: true  # Log all generated SQL/SPARQL/code
  log_execution_results: true  # Log execution outcomes
```

**Log Output:**
```json
{
  "timestamp": "2026-04-12T10:30:00Z",
  "query": "How many employees?",
  "detected_source": "sql_database",
  "confidence": 0.92,
  "generated_sql": "SELECT COUNT(*) FROM employees",
  "execution_result": "success",
  "row_count": 150,
  "execution_time_ms": 234
}
```

---

## Configuration Profiles

### Profile 1: Maximum Security (Recommended for Production)

```yaml
# source_detection.yaml
auto_execute: false
require_confirmation: true

thresholds:
  high_confidence: 0.98
  medium_confidence: 0.8
  low_confidence: 0.6

entity_verification:
  tables:
    enabled: false
  sql:
    enabled: true
    read_only: true
  kg:
    enabled: true
    use_ask_query: true

execution:
  timeout:
    total_seconds: 30
    per_source_seconds: 10
```

### Profile 2: Balanced (Development/Testing)

```yaml
auto_execute: false
require_confirmation: true

thresholds:
  high_confidence: 0.9
  medium_confidence: 0.7
  low_confidence: 0.5

entity_verification:
  tables:
    enabled: true
    paths:
      - "${WORKSPACE}/test_data/*.csv"
    max_file_size_mb: 50
```

### Profile 3: Permissive (Local Development Only)

```yaml
auto_execute: true
require_confirmation: false

thresholds:
  high_confidence: 0.8
  medium_confidence: 0.5
  low_confidence: 0.3

# ⚠️  Only use in isolated development environments!
```

---

## Environment Variables

### Required

| Variable | Purpose | Security Level |
|----------|---------|----------------|
| `DEEPSEEK_API_KEY` | LLM query generation | High - protect like password |
| `OPENAI_API_KEY` | Alternative LLM | High - protect like password |

### Optional

| Variable | Purpose | Security Level |
|----------|---------|----------------|
| `MYSQL_CONNECTION_STRING` | Database access | Critical - use read-only creds |
| `CUSTOM_KG_ENDPOINT` | KG endpoint | Medium - verify endpoint trust |
| `WORKSPACE` | File scanning base | Medium - restrict to specific dirs |

### Setup

```bash
# Create .env file (NEVER commit to git)
cp .env.example .env
chmod 600 .env  # Restrict permissions

# Edit with your credentials
nano .env

# Load environment
export $(cat .env | xargs)

# Verify
echo $DEEPSEEK_API_KEY  # Should show value
git status .env         # Should show as untracked
```

---

## Incident Response

### If Credentials Are Compromised

1. **Immediately rotate** the affected API key or password
2. **Review audit logs** for unauthorized access
3. **Revoke access** for any suspicious sessions
4. **Update .env** file with new credentials
5. **Notify affected parties** if user data was accessed

### If Malicious Query Detected

1. **Stop execution** immediately (Ctrl+C or kill process)
2. **Review generated query** in audit logs
3. **Identify injection vector** in user input
4. **Add input validation** to prevent recurrence
5. **Report security issue** to maintainers

---

## Compliance Considerations

### Data Protection

- **GDPR**: Ensure personal data in databases is handled per GDPR requirements
- **CCPA**: Provide opt-out mechanisms for California residents
- **HIPAA**: Do not use with PHI unless properly configured and audited

### Access Control

- Use role-based database credentials (read-only for QA)
- Implement API key rotation policies
- Enable audit logging for compliance reporting

---

## Security Checklist

Before deploying HeteroMind:

- [ ] All credentials stored in environment variables (not code)
- [ ] `.env` file added to `.gitignore`
- [ ] `auto_execute: false` in production config
- [ ] `require_confirmation: true` in production config
- [ ] Database credentials are read-only
- [ ] File scanning restricted to specific directories
- [ ] Audit logging enabled
- [ ] API keys rotated within last 90 days
- [ ] Network endpoints whitelisted in firewall
- [ ] Security review completed

---

## Reporting Security Issues

If you discover a security vulnerability:

1. **Do not** create a public GitHub issue
2. **Email**: security@coinlab.seu.edu.cn (if applicable)
3. **Include**: Description, reproduction steps, impact assessment
4. **Wait**: Allow 90 days for patch before public disclosure

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1.0 | 2026-04-12 | Initial security documentation |

---

*Last Updated: 2026-04-12*  
*Version: 0.1.0*
