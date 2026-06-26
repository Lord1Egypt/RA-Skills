#!/usr/bin/env bash
# verify.sh — Auto-extract context for proof-agent verification
# Usage: ./verify.sh [base-ref]
# Default base-ref: HEAD~1 (last commit)
#
# Outputs a filled verification prompt to stdout.

set -euo pipefail

BASE="${1:-HEAD~1}"

# Get changed files
FILES=$(git diff --name-only "$BASE" HEAD 2>/dev/null || git diff --name-only --cached 2>/dev/null || echo "(no git changes detected)")

# Count
FILE_COUNT=$(echo "$FILES" | grep -c '.' || echo 0)

# Get diff summary
DIFF=$(git diff --stat "$BASE" HEAD 2>/dev/null || echo "(no diff available)")

# Get commit messages since base
COMMITS=$(git log --oneline "$BASE"..HEAD 2>/dev/null || echo "(no commits)")

# Check for sensitive files
SENSITIVE=""
for pattern in auth secret permission Dockerfile .env; do
  MATCHES=$(echo "$FILES" | grep -i "$pattern" || true)
  if [ -n "$MATCHES" ]; then
    SENSITIVE="${SENSITIVE}${MATCHES}\n"
  fi
done

# Determine if verification is needed
SHOULD_VERIFY=false
if [ "$FILE_COUNT" -ge 3 ]; then
  SHOULD_VERIFY=true
fi
if [ -n "$SENSITIVE" ]; then
  SHOULD_VERIFY=true
fi

if [ "$SHOULD_VERIFY" = false ]; then
  echo "SKIP: Only $FILE_COUNT file(s) changed, no sensitive files detected."
  echo "Use --force or run manually to verify anyway."
  exit 0
fi

# Build the prompt
cat <<EOF
VERIFICATION REQUEST

## Files Changed ($FILE_COUNT files)
$FILES

## Diff Summary
$DIFF

## Commits
$COMMITS

## Sensitive Files Detected
$([ -n "$SENSITIVE" ] && echo -e "$SENSITIVE" || echo "None")

## Your Job

You are an independent verifier. The worker who made these changes CANNOT verify their own work — only you can assign a verdict.

### Review Checklist
1. Correctness: Does the code actually do what was requested?
2. Bugs & Edge Cases: Regressions, unhandled errors, missed cases?
3. Security: Vulnerabilities, exposed secrets, permission issues?
4. Build: Does it build/compile/lint cleanly?
5. Facts: Are any claims, version numbers, or URLs verifiable? Check them.

### Rules
- For EVERY check, include the actual command you ran and its output
- Do NOT take the worker's word for anything
- Do NOT give PASS without running at least 3 verification commands
- You have NO information about the worker's test results — verify independently

## Verdict

Assign EXACTLY ONE:

PASS — All checks passed. Every claim backed by command output.
FAIL — Issues found. List each: file, line, what's wrong, severity (critical/major/minor).
PARTIAL — Some passed, some unverifiable. List both with evidence.
EOF
