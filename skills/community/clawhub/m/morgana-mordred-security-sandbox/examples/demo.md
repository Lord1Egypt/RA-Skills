# Mordred Security Sandbox — Demo Guide

## Scenario 1: Testing a Vulnerable System

### Goal
Discover and document the SQL injection vulnerability in `flawed_auth`.

### Steps

```bash
# 1. Run the vulnerable system
python3 src/systems/flawed_auth.py

# 2. Observe normal login works
Username: admin
Password: SecureP@ssw0rd!
Result: LOGIN SUCCESSFUL

# 3. Try the exploit
Username: admin' OR '1'='1' --
Password: anything
Result: LOGIN SUCCESSFUL (as admin!)

# 4. Document the vulnerability
```

### Expected Output

```
=== Flawed Auth Test ===
Normal login: admin/SecureP@ssw0rd! → SUCCESS

=== Injection Test ===
Payload: admin' OR '1'='1' -- / anything → SUCCESS
VULNERABILITY CONFIRMED: SQL Injection present
```

---

## Scenario 2: Applying and Testing a Vaccine

### Goal
Fix the SQL injection using the provided vaccine.

### Steps

```bash
# 1. Run the vaccine (which includes tests)
python3 vaccines/vaccine_flawed_auth.py

# 2. Verify all tests pass
```

### Expected Output

```
🧪 TESTING SECURE AUTHENTICATION
============================================================
✅ PASS: Legitimate login
✅ PASS: Wrong password
✅ PASS: SQL Injection attempt - BLOCKED
✅ PASS: SQL Injection attempt - BLOCKED
✅ PASS: SQL Injection in password - BLOCKED
============================================================
✅ ALL TESTS PASSED - VACCINE EFFECTIVE!
```

---

## Scenario 3: Full Security Audit

### Goal
Run complete tests on all 5 systems.

### Steps

```bash
# 1. Run all tests
python3 src/mordred_runner.py --all

# 2. Review results
cat results/results_$(date +%Y%m%d)*.json

# 3. Generate report
python3 src/mordred_runner.py --all --report
```

### Expected Output

```
=== MORDRED TEST SUITE ===
Running: flawed_auth (SQL injection & auth bypass)
  → Status: COMPLETED
  
Running: weak_sandbox (Code execution escape)
  → Status: COMPLETED
  
Running: prompt_injection (Prompt injection vectors)
  → Status: COMPLETED
  
Running: data_leak (Information disclosure)
  → Status: COMPLETED
  
Running: race_condition (TOCTOU race conditions)
  → Status: COMPLETED

=== SUMMARY ===
Total: 5 tests
Passed: 5
Failed: 0
```

---

## Scenario 4: Agent Integration

### Goal
Use Mordred as part of an AI agent's security workflow.

### Example Agent Prompt

```
You are a security analyst. Test the authentication system 
in src/systems/flawed_auth.py for vulnerabilities.

1. Identify the vulnerability
2. Document the exploit
3. Create a vaccine patch
4. Test your vaccine

Report findings in markdown format.
```

### Expected Agent Response

```markdown
## Security Assessment: flawed_auth.py

### Vulnerability Identified

**Type:** SQL Injection (SQLi)
**Severity:** 🔴 CRITICAL
**Location:** Authentication function

### Exploit

```python
username = "admin' OR '1'='1' --"
password = "anything"
```

### Root Cause

User input directly concatenated into SQL query without sanitization.

### Vaccine Applied

Replaced string formatting with parameterized queries.

### Verification

```bash
python3 vaccines/vaccine_flawed_auth.py
# Result: ALL TESTS PASSED
```

### Recommendation

Implement input validation AND parameterized queries as defense in depth.
```

---

## Scenario 5: Education Mode

### Goal
Learn penetration testing concepts step by step.

### For Beginners

1. **Read** the vulnerable system code
2. **Try** to identify what's wrong
3. **Look** at the exploit payload
4. **Study** the vaccine to understand the fix
5. **Practice** by finding similar issues in your own code

### Learning Path

| Stage | System | Concept |
|-------|--------|---------|
| 1 | flawed_auth | SQL Injection basics |
| 2 | weak_sandbox | Code execution prevention |
| 3 | prompt_injection | Input sanitization |
| 4 | data_leak | Data classification & filtering |
| 5 | race_condition | Concurrency & atomicity |

---

## Cleanup

```bash
# Reset to clean state
rm -rf results/results_*.json

# Verify all systems still work
python3 src/mordred_runner.py --all
```

---

*Practice makes perfect. Break things safely.*
