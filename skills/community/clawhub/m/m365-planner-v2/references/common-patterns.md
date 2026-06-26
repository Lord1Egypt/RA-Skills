# Common Patterns for M365 Planner

## Pattern 1: Create Project Structure

Create a complete project with predefined buckets:

```bash
# 1. Create or get group
GROUP_ID=$(az ad group list --query "[?displayName=='Project Team'].id" -o tsv)

# 2. Create plan with buckets (using helper script)
./scripts/create_plan.sh "Website Redesign" "$GROUP_ID"
```

## Pattern 2: Bulk Task Import

Create multiple tasks from a list:

```bash
BUCKET_ID="your-bucket-id"

cat tasks.txt | while read -r TASK; do
    mgc planner tasks create \
        --title "$TASK" \
        --bucket-id "$BUCKET_ID" \
        --output none
    echo "Created: $TASK"
done
```

## Pattern 3: Task Status Update

Update task progress:

```bash
TASK_ID="your-task-id"

# Mark as in progress (50%)
mgc planner tasks patch \
    --planner-task-id "$TASK_ID" \
    --percent-complete 50

# Mark as complete (100%)
mgc planner tasks patch \
    --planner-task-id "$TASK_ID" \
    --percent-complete 100
```

## Pattern 4: Weekly Report

Generate a task summary:

```bash
PLAN_ID="your-plan-id"

# Get all tasks
echo "Weekly Planner Report"
echo "===================="
./scripts/list_tasks.sh "$PLAN_ID"
```

## Pattern 5: Assign Tasks to Team

Assign tasks to multiple users:

```bash
# Get user IDs
USER1=$(az ad user show --id "alice@company.com" --query id -o tsv)
USER2=$(az ad user show --id "bob@company.com" --query id -o tsv)

# Assign tasks
./scripts/assign_task.sh "task-id-1" "$USER1"
./scripts/assign_task.sh "task-id-2" "$USER2"
```

## JSON Output Processing

Many commands support `--output json` for automation:

```bash
# Extract specific fields
mgc planner plans list --output json | \
    jq -r '.value[] | select(.title | contains("Project")) | .id'

# Save to file
mgc planner tasks list --planner-bucket-id "$BUCKET" --output json > tasks.json
```
