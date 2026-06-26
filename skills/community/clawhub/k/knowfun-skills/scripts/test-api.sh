#!/bin/bash
# Quick API test script to verify Knowfun.io API connectivity
#
# Copyright (c) 2026 Knowfun.io
# Licensed under the MIT License

set -e

API_KEY="${KNOWFUN_API_KEY}"
BASE_URL="https://api.knowfun.io"

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "🧪 Knowfun.io API Test Suite"
echo "=============================="
echo ""

# Check API key
if [ -z "$API_KEY" ]; then
    echo -e "${RED}❌ Error: KNOWFUN_API_KEY not set${NC}"
    echo "Please set it with: export KNOWFUN_API_KEY='kf_your_api_key'"
    exit 1
fi

echo -e "${GREEN}✓${NC} API Key found"

# Test 1: Check schema (no auth required)
echo ""
echo "Test 1: Fetching schema (no auth required)..."
SCHEMA_RESPONSE=$(curl -s "$BASE_URL/api/openapi/v1/schema")
if echo "$SCHEMA_RESPONSE" | grep -q '"success":true'; then
    echo -e "${GREEN}✓${NC} Schema endpoint working"
else
    echo -e "${RED}✗${NC} Schema endpoint failed"
    echo "$SCHEMA_RESPONSE"
fi

# Test 2: Check credits balance
echo ""
echo "Test 2: Checking credit balance..."
CREDITS_RESPONSE=$(curl -s -w "\n%{http_code}" \
    "$BASE_URL/api/openapi/v1/credits/balance" \
    -H "Authorization: Bearer $API_KEY")

HTTP_CODE=$(echo "$CREDITS_RESPONSE" | tail -n1)
BODY=$(echo "$CREDITS_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓${NC} Credit balance endpoint working"
    if command -v jq &> /dev/null; then
        AVAILABLE=$(echo "$BODY" | jq -r '.data.available')
        echo "  Available credits: $AVAILABLE"
    fi
else
    echo -e "${RED}✗${NC} Credit balance endpoint failed (HTTP $HTTP_CODE)"
    echo "$BODY"
fi

# Test 3: Check pricing
echo ""
echo "Test 3: Checking pricing..."
PRICING_RESPONSE=$(curl -s -w "\n%{http_code}" \
    "$BASE_URL/api/openapi/v1/credits/pricing" \
    -H "Authorization: Bearer $API_KEY")

HTTP_CODE=$(echo "$PRICING_RESPONSE" | tail -n1)
BODY=$(echo "$PRICING_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓${NC} Pricing endpoint working"
else
    echo -e "${RED}✗${NC} Pricing endpoint failed (HTTP $HTTP_CODE)"
    echo "$BODY"
fi

# Test 4: List tasks
echo ""
echo "Test 4: Listing recent tasks..."
LIST_RESPONSE=$(curl -s -w "\n%{http_code}" \
    "$BASE_URL/api/openapi/v1/tasks?limit=5" \
    -H "Authorization: Bearer $API_KEY")

HTTP_CODE=$(echo "$LIST_RESPONSE" | tail -n1)
BODY=$(echo "$LIST_RESPONSE" | sed '$d')

if [ "$HTTP_CODE" -eq 200 ]; then
    echo -e "${GREEN}✓${NC} Task list endpoint working"
    if command -v jq &> /dev/null; then
        TASK_COUNT=$(echo "$BODY" | jq -r '.data.tasks | length')
        echo "  Recent tasks: $TASK_COUNT"
    fi
else
    echo -e "${RED}✗${NC} Task list endpoint failed (HTTP $HTTP_CODE)"
    echo "$BODY"
fi

# Test 5: Create a simple test task (optional, requires credits)
echo ""
read -p "Run task creation test? This will use 100 credits. (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Test 5: Creating test task..."

    REQUEST_ID="test_$(date +%s)"

    CREATE_RESPONSE=$(curl -s -w "\n%{http_code}" \
        "$BASE_URL/api/openapi/v1/tasks" \
        -X POST \
        -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d "{
            \"requestId\": \"$REQUEST_ID\",
            \"taskType\": \"poster\",
            \"material\": {
                \"text\": \"API Test: This is a test poster creation\",
                \"type\": \"text\"
            }
        }")

    HTTP_CODE=$(echo "$CREATE_RESPONSE" | tail -n1)
    BODY=$(echo "$CREATE_RESPONSE" | sed '$d')

    if [ "$HTTP_CODE" -eq 200 ]; then
        echo -e "${GREEN}✓${NC} Task creation endpoint working"
        if command -v jq &> /dev/null; then
            TASK_ID=$(echo "$BODY" | jq -r '.data.taskId')
            echo "  Task ID: $TASK_ID"
            echo ""
            echo "  Monitor task with: ./knowfun-cli.sh status $TASK_ID"
        fi
    else
        echo -e "${RED}✗${NC} Task creation failed (HTTP $HTTP_CODE)"
        echo "$BODY"
    fi
else
    echo -e "${YELLOW}⊘${NC} Task creation test skipped"
fi

echo ""
echo "=============================="
echo "Test suite completed!"
