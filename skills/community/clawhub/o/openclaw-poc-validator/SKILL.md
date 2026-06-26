---
name: poc-validator
description: >
  Automated Vulnerability Verification and Payload Replay Probe. Dynamically executes HTTP requests and analyzes HTTP status codes/error traces (e.g., SQL Injection errors).
  Use when: Testing specific payloads, verifying vulnerabilities, or replaying raw HTTP requests to analyze stack traces.
  NOT for: Automated mass scanning, DDoS attacks, or unauthorized exploitation.
---

# Autonomous PoC Validator

## When to Run

- The user provides raw HTTP request data or a specific malicious payload and requests a target interface test.
- The user asks to "verify this PoC", "replay this request", or "check for 500 errors/SQL exceptions".

## Workflow

1. Parse the target URL, Method, Headers (specifically `Cookie` and `User-Agent`), and the Payload provided by the user.
2. Format the request data and pass it to the `scripts/replay.py` execution script.
   - Command execution example: `python3 scripts/replay.py --url "{URL}" --method "{METHOD}" --data "{PAYLOAD}" --headers "{JSON_HEADERS}"`
3. Parse the JSON output returned by the script (includes status code, headers, and smart body snippet).
4. Perform deep analysis on the response context:
   - Identify HTTP `500 Internal Server Error` (often indicates syntax escape or fatal exception).
   - Scan the `body_snippet` for signature keywords: `SQLSTATE`, `Syntax error`, `ExtractValue`, `XPATH syntax error`, `Call to undefined function`, etc.
5. Generate the final vulnerability validation report strictly adhering to the `Output Format` below.

## Output Format

[+] PoC Validation Report

[*] Target Interface : {Method} {URL}
[*] Test Payload   : {The critical injection code/payload}
[*] Response Status: {Status Code} (e.g., 200 OK / 500 Internal Server Error)

[!] Analysis Conclusion:
{Clearly state if the vulnerability exists. E.g., "SQL Error-Based Injection confirmed. Successfully captured SQLSTATE[42000] exception." or "Injection failed. The target returned 200 OK with sanitized input."}

[-] Critical Evidence / Stack Trace:
```text
{The extracted error logs or relevant response snippet demonstrating the vulnerability}