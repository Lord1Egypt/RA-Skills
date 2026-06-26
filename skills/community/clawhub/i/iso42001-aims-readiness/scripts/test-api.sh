#!/bin/bash
# iso42001-aims-readiness - Quick test script
# Usage: ./test-api.sh
# Requires: TOOLWEB_API_KEY environment variable

set -euo pipefail

API_URL="https://portal.toolweb.in:8443/iso42001"

if [ -z "${TOOLWEB_API_KEY:-}" ]; then
  echo "❌ Error: TOOLWEB_API_KEY is not set."
  echo ""
  echo "Get your API key from: https://portal.toolweb.in"
  echo "Then run: export TOOLWEB_API_KEY='your-key-here'"
  exit 1
fi

echo "🤖 ISO 42001 AIMS Readiness Assessment — Test Run"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

RESPONSE=$(curl -sk -w "\n%{http_code}" -X POST "$API_URL" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $TOOLWEB_API_KEY" \
  -d '{
    "organization_name": "Test Technology Corp",
    "industry": "Technology",
    "org_size": "medium",
    "ai_role": "AI-powered customer support chatbots and document processing",
    "existing_frameworks": ["ISO 27001"],
    "ai_systems_count": 5,
    "has_ai_policy": false,
    "has_risk_assessment_process": true,
    "has_impact_assessment_process": false,
    "has_data_governance": true
  }')

HTTP_CODE=$(echo "$RESPONSE" | tail -1)
BODY=$(echo "$RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
  echo "✅ API call successful (HTTP $HTTP_CODE)"
  echo ""
  echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"
elif [ "$HTTP_CODE" -eq 401 ]; then
  echo "❌ Authentication failed (HTTP 401). Check your TOOLWEB_API_KEY."
elif [ "$HTTP_CODE" -eq 403 ]; then
  echo "❌ Access denied (HTTP 403). Ensure your API key is valid."
elif [ "$HTTP_CODE" -eq 429 ]; then
  echo "⚠️  Rate limit exceeded (HTTP 429). Wait 60 seconds and retry."
else
  echo "❌ API error (HTTP $HTTP_CODE)"
  echo "$BODY"
fi
