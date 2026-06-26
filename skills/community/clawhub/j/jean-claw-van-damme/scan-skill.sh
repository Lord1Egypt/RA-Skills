#!/bin/bash
# scan-skill.sh -- Helper script for Jean-Claw Van Damme skill scanning
# Performs static analysis on a ClawHub skill before installation
#
# Usage: ./scan-skill.sh <skill-directory-path>
#
# This script checks for common malicious patterns in OpenClaw skills.
# It is meant to augment (not replace) the agent's own analysis of SKILL.md content.

set -euo pipefail

SKILL_DIR="${1:?Usage: scan-skill.sh <skill-directory-path>}"
SCAN_TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
RISK_SCORE=0
FINDINGS=()

# Colors for terminal output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m'

echo "======================================"
echo "JEAN-CLAW STATIC SCAN"
echo "Target: ${SKILL_DIR}"
echo "Timestamp: ${SCAN_TIMESTAMP}"
echo "======================================"
echo ""

# Check SKILL.md exists
if [ ! -f "${SKILL_DIR}/SKILL.md" ]; then
    echo -e "${RED}[FAIL]${NC} No SKILL.md found. Not a valid skill."
    exit 1
fi

# 1. Prompt injection patterns
echo "Scanning for prompt injection patterns..."
INJECTION_PATTERNS=(
    "ignore previous"
    "ignore all previous"
    "ignore above"
    "you are now"
    "act as"
    "system override"
    "admin mode"
    "developer mode"
    "jailbreak"
    "DAN mode"
    "bypass"
    "pretend you"
    "new instructions"
    "forget everything"
    "disregard"
)

for pattern in "${INJECTION_PATTERNS[@]}"; do
    if grep -riq "${pattern}" "${SKILL_DIR}/" 2>/dev/null; then
        FINDINGS+=("[WARN] Prompt injection pattern detected: '${pattern}'")
        RISK_SCORE=$((RISK_SCORE + 2))
    fi
done

if [ ${#FINDINGS[@]} -eq 0 ]; then
    echo -e "${GREEN}[PASS]${NC} No prompt injection patterns found"
else
    echo -e "${YELLOW}[WARN]${NC} ${#FINDINGS[@]} prompt injection pattern(s) found"
fi

# 2. Data exfiltration patterns
echo "Scanning for data exfiltration patterns..."
EXFIL_COUNT=0

# Check for curl/wget to external URLs
if grep -riqE '(curl|wget|fetch)\s+.*(http|https)://' "${SKILL_DIR}/" 2>/dev/null; then
    FINDINGS+=("[WARN] External HTTP requests detected (curl/wget/fetch)")
    EXFIL_COUNT=$((EXFIL_COUNT + 1))
    RISK_SCORE=$((RISK_SCORE + 2))
fi

# Check for base64 encoding
if grep -riqE '(base64|btoa|atob)\s' "${SKILL_DIR}/" 2>/dev/null; then
    FINDINGS+=("[WARN] Base64 encoding/decoding detected")
    EXFIL_COUNT=$((EXFIL_COUNT + 1))
    RISK_SCORE=$((RISK_SCORE + 1))
fi

# Check for DNS-based patterns
if grep -riqE '(dns|nslookup|dig)\s' "${SKILL_DIR}/" 2>/dev/null; then
    FINDINGS+=("[WARN] DNS query tools referenced")
    EXFIL_COUNT=$((EXFIL_COUNT + 1))
    RISK_SCORE=$((RISK_SCORE + 2))
fi

if [ ${EXFIL_COUNT} -eq 0 ]; then
    echo -e "${GREEN}[PASS]${NC} No data exfiltration patterns found"
else
    echo -e "${YELLOW}[WARN]${NC} ${EXFIL_COUNT} exfiltration pattern(s) found"
fi

# 3. Credential access
echo "Scanning for credential access patterns..."
CRED_COUNT=0

CRED_PATTERNS=(
    "API_KEY"
    "SECRET"
    "TOKEN"
    "PASSWORD"
    "PRIVATE_KEY"
    "SSH_KEY"
    "WALLET"
    "SEED_PHRASE"
    "MNEMONIC"
    ".env"
    "credentials"
    "keychain"
    "ssh-rsa"
    "BEGIN RSA"
    "BEGIN PRIVATE"
)

for pattern in "${CRED_PATTERNS[@]}"; do
    if grep -riq "${pattern}" "${SKILL_DIR}/" 2>/dev/null; then
        FINDINGS+=("[WARN] Credential reference: '${pattern}'")
        CRED_COUNT=$((CRED_COUNT + 1))
        RISK_SCORE=$((RISK_SCORE + 2))
    fi
done

if [ ${CRED_COUNT} -eq 0 ]; then
    echo -e "${GREEN}[PASS]${NC} No credential access patterns found"
else
    echo -e "${YELLOW}[WARN]${NC} ${CRED_COUNT} credential reference(s) found"
fi

# 4. Privilege escalation
echo "Scanning for privilege escalation patterns..."
PRIV_COUNT=0

PRIV_PATTERNS=(
    "SOUL.md"
    "IDENTITY.md"
    "openclaw.json"
    "config.yaml"
    "sudo"
    "chmod 777"
    "chown root"
    "/etc/passwd"
    "/etc/shadow"
)

for pattern in "${PRIV_PATTERNS[@]}"; do
    if grep -riq "${pattern}" "${SKILL_DIR}/" 2>/dev/null; then
        FINDINGS+=("[WARN] Privilege escalation pattern: '${pattern}'")
        PRIV_COUNT=$((PRIV_COUNT + 1))
        RISK_SCORE=$((RISK_SCORE + 3))
    fi
done

if [ ${PRIV_COUNT} -eq 0 ]; then
    echo -e "${GREEN}[PASS]${NC} No privilege escalation patterns found"
else
    echo -e "${RED}[FAIL]${NC} ${PRIV_COUNT} privilege escalation pattern(s) found"
fi

# 5. Hidden execution
echo "Scanning for hidden execution patterns..."
EXEC_COUNT=0

EXEC_PATTERNS=(
    "eval("
    "exec("
    "Function("
    "import("
    "require("
    "\\\\x[0-9a-f]"
    "String.fromCharCode"
    "\\$\\(.*\\)"
)

for pattern in "${EXEC_PATTERNS[@]}"; do
    if grep -riqE "${pattern}" "${SKILL_DIR}/" 2>/dev/null; then
        FINDINGS+=("[WARN] Hidden execution pattern: '${pattern}'")
        EXEC_COUNT=$((EXEC_COUNT + 1))
        RISK_SCORE=$((RISK_SCORE + 3))
    fi
done

if [ ${EXEC_COUNT} -eq 0 ]; then
    echo -e "${GREEN}[PASS]${NC} No hidden execution patterns found"
else
    echo -e "${RED}[FAIL]${NC} ${EXEC_COUNT} hidden execution pattern(s) found"
fi

# Final risk assessment
echo ""
echo "======================================"
echo "SCAN COMPLETE"
echo "======================================"
echo "Total findings: ${#FINDINGS[@]}"
echo "Risk score: ${RISK_SCORE}/50"

if [ ${RISK_SCORE} -le 3 ]; then
    echo -e "Risk level: ${GREEN}LOW${NC}"
    echo "Recommendation: SAFE TO INSTALL"
elif [ ${RISK_SCORE} -le 10 ]; then
    echo -e "Risk level: ${YELLOW}MEDIUM${NC}"
    echo "Recommendation: INSTALL WITH CAUTION -- review findings below"
elif [ ${RISK_SCORE} -le 20 ]; then
    echo -e "Risk level: ${RED}HIGH${NC}"
    echo "Recommendation: DO NOT INSTALL without thorough manual review"
else
    echo -e "Risk level: ${RED}CRITICAL${NC}"
    echo "Recommendation: DO NOT INSTALL"
fi

echo ""
if [ ${#FINDINGS[@]} -gt 0 ]; then
    echo "DETAILED FINDINGS:"
    for finding in "${FINDINGS[@]}"; do
        echo "  ${finding}"
    done
fi

# Output JSON for the agent to consume
echo ""
echo "---JSON-OUTPUT---"
cat <<EOF
{
  "scan_timestamp": "${SCAN_TIMESTAMP}",
  "skill_path": "${SKILL_DIR}",
  "risk_score": ${RISK_SCORE},
  "finding_count": ${#FINDINGS[@]},
  "risk_level": "$([ ${RISK_SCORE} -le 3 ] && echo 'LOW' || ([ ${RISK_SCORE} -le 10 ] && echo 'MEDIUM' || ([ ${RISK_SCORE} -le 20 ] && echo 'HIGH' || echo 'CRITICAL')))",
  "recommendation": "$([ ${RISK_SCORE} -le 3 ] && echo 'SAFE TO INSTALL' || ([ ${RISK_SCORE} -le 10 ] && echo 'INSTALL WITH CAUTION' || echo 'DO NOT INSTALL'))"
}
EOF
