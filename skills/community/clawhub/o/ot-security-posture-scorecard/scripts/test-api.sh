#!/bin/bash
# ot-security-posture-scorecard - Quick test script
# Usage: ./test-api.sh
# Requires: TOOLWEB_API_KEY environment variable

set -euo pipefail

API_URL="https://portal.toolweb.in:8443/security/itotassessor"

if [ -z "${TOOLWEB_API_KEY:-}" ]; then
  echo "❌ Error: TOOLWEB_API_KEY is not set."
  echo ""
  echo "Get your API key from: https://portal.toolweb.in"
  echo "Then run: export TOOLWEB_API_KEY='your-key-here'"
  exit 1
fi

echo "🏭 OT Security Posture Scorecard — Test Run"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

RESPONSE=$(curl -sk -w "\n%{http_code}" -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $TOOLWEB_API_KEY" \
  -d '{
    "org_name": "Test Manufacturing Corp",
    "sector": "Manufacturing",
    "ot_size": "Medium",
    "integration_level": "Partial",
    "ot_technologies": ["SCADA", "PLC", "HMI"],
    "it_tools": ["Firewall", "SIEM"],
    "csf_scores": {
      "identify": 3,
      "protect": 2,
      "detect": 2,
      "respond": 1,
      "recover": 1
    },
    "threat_concern": "Ransomware targeting OT networks",
    "compliance": "IEC 62443"
  }')

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
  echo "✅ API call successful (HTTP $HTTP_CODE)"
  echo ""
  echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
elif [ "$HTTP_CODE" -eq 401 ]; then
  echo "❌ Authentication failed (HTTP 401). Check your TOOLWEB_API_KEY."
elif [ "$HTTP_CODE" -eq 429 ]; then
  echo "⚠️  Rate limit exceeded (HTTP 429). Wait 60 seconds and retry."
else
  echo "❌ API error (HTTP $HTTP_CODE)"
  echo "$BODY"
fi
