#!/bin/bash
# List all tasks in a plan with details

set -e

if [ $# -lt 1 ]; then
    echo "Usage: $0 <plan-id>"
    echo "Example: $0 abc123..."
    exit 1
fi

PLAN_ID="$1"

echo "Fetching tasks for plan: $PLAN_ID"
echo ""

# Get all buckets in the plan
BUCKETS=$(mgc planner buckets list --planner-plan-id "$PLAN_ID" --output json)

# For each bucket, list tasks
echo "$BUCKETS" | jq -r '.value[] | "\(.id)|\(.name)"' | while IFS='|' read -r BUCKET_ID BUCKET_NAME; do
    echo "=== $BUCKET_NAME ==="
    
    TASKS=$(mgc planner tasks list --planner-bucket-id "$BUCKET_ID" --output json 2>/dev/null || echo '{"value":[]}')
    
    echo "$TASKS" | jq -r '.value[] | "  [\(.percentComplete // 0)%] \(.title)"' | head -20
    
    COUNT=$(echo "$TASKS" | jq '.value | length')
    if [ "$COUNT" -eq 0 ]; then
        echo "  (no tasks)"
    fi
    
    echo ""
done
