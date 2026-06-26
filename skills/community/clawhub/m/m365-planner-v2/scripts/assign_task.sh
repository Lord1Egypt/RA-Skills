#!/bin/bash
# Assign a task to a user

set -e

if [ $# -lt 2 ]; then
    echo "Usage: $0 <task-id> <user-id>"
    echo "Example: $0 abc123... user@domain.com"
    exit 1
fi

TASK_ID="$1"
USER_ID="$2"

echo "Assigning task $TASK_ID to $USER_ID"

# Get the task etag first for update
ETAG=$(mgc planner tasks get --planner-task-id "$TASK_ID" --output json | jq -r '.["@odata.etag"]')

# Build assignments JSON
ASSIGNMENTS=$(jq -n \
    --arg user "$USER_ID" \
    '{($user): {"@odata.type": "#microsoft.graph.plannerAssignment", "orderHint": " !"}}')

# Update task with assignment
mgc planner tasks update \
    --planner-task-id "$TASK_ID" \
    --if-match "$ETAG" \
    --assignments "$ASSIGNMENTS" \
    --output none

echo "Task assigned successfully!"
