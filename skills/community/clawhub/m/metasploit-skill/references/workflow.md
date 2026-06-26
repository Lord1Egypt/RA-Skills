# Execution and Reporting Workflow

## 1. Pre-Execution Checklist

- Confirm explicit authorization and current test window.
- Confirm in-scope targets and prohibited techniques.
- Confirm rollback and communication channel for incidents.
- Confirm listener host/port availability.
- Confirm module options and payload alignment.

## 2. Command Sequence (Recommended)

```bash
msfconsole -q
search type:exploit <keyword-or-cve>
use exploit/<path>
show options
show payloads
```

Build and execute a resource script:

```bash
python3 scripts/build_rc.py --module exploit/<path> --rhosts <target> --check --output run.rc
msfconsole -q -r run.rc
```

## 3. Troubleshooting Loop

When execution fails, change one variable per iteration:

1. Validate target reachability and service state.
2. Validate version match assumptions.
3. Validate payload compatibility.
4. Validate required options and authentication values.
5. Retry with controlled module or payload fallback.

Record each change and outcome.

## 4. Evidence Collection Fields

- Timestamp and operator
- Target and scope reference
- Module and payload identifiers
- Effective option set (redacted where needed)
- Check result and exploit result
- Session metadata (`sessions -l`)
- Proof artifact summary

## 5. Reporting Template (Concise)

### Objective
- What was tested and why

### Procedure
- Exact commands/resource script used

### Result
- Success/failure and confidence level

### Impact
- Practical security implication

### Remediation
- Actionable fixes and validation method
