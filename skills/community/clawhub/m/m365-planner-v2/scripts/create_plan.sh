#!/bin/bash
# Create a new Planner plan with default buckets

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <plan-name> <group-id>"
    echo "Example: $0 'Project Alpha' 12345678-1234-1234-1234-123456789abc"
    exit 1
fi

PLAN_NAME="$1"
GROUP_ID="$2"

echo "Creating plan: $PLAN_NAME"

# Create the plan
PLAN_RESULT=$(mgc planner plans create \
    --name "$PLAN_NAME" \
    --group-id "$GROUP_ID" \
    --output json)

PLAN_ID=$(echo "$PLAN_RESULT" | jq -r '.id')

echo "Created plan ID: $PLAN_ID"

# Create default buckets
echo "Creating default buckets..."

BUCKETS=("To Do" "In Progress" "Done")
for BUCKET in "${BUCKETS[@]}"; do
    mgc planner buckets create \
        --name "$BUCKET" \
        --plan-id "$PLAN_ID" \
        --output none
    echo "  Created bucket: $BUCKET"
done

echo ""
echo "Plan '$PLAN_NAME' created successfully!"
echo "Plan ID: $PLAN_ID"
echo ""
echo "To add tasks:"
echo "  mgc planner buckets list --planner-plan-id $PLAN_ID"
