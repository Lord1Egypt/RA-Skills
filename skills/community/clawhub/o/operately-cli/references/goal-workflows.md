# Goal Workflows

OKR patterns and goal management workflows in Operately, covering goal creation, hierarchy, targets, check-ins, and lifecycle management.

## Goal Lifecycle

### 1. Create Goal

```bash
operately goals create \
  --space-id s1 \
  --name "Increase Q2 Revenue" \
  --champion-id u1 \
  --reviewer-id u2 \
  --anonymous-access-level 0 \
  --company-access-level 10 \
  --space-access-level 70
```

Optional fields:
- `--description` - Markdown goal description
- `--parent-goal-id` - Link to parent goal

**Note:** Access levels are required. Use `--company-access-level 10 --space-access-level 70` for typical team goals.

### 2. Set Targets

```bash
# Create numeric target
operately goals create_target \
  --goal-id g1 \
  --name "Monthly Recurring Revenue" \
  --start-value 50000 \
  --target-value 100000 \
  --unit "USD"

# Create percentage target
operately goals create_target \
  --goal-id g1 \
  --name "Customer Retention" \
  --start-value 85 \
  --target-value 95 \
  --unit "%"
```

### 3. Regular Check-ins

```bash
operately goals create_check_in \
  --goal-id g1 \
  --status on_track \
  --due-date 2026-04-01 \
  --content "# Q2 Progress - Week 4\n\n## Current MRR\n$65,000 (target: $100,000)\n\n## Progress\n- 30% to target\n- On track for Q2 goal"
```

### 4. Update Target Values

```bash
operately goals update_target_value \
  --goal-id g1 \
  --target-id t1 \
  --value 65000
```

### 5. Close Goal

```bash
operately goals close \
  --goal-id g1 \
  --success achieved \
  --success-status achieved \
  --retrospective "# Q2 Revenue Goal Retrospective\n\n## Achievement\nReached $105,000 MRR (105% of target)\n\n## Key Drivers\n- New enterprise customers\n- Reduced churn\n- Upsells to existing customers"
```

## Goal Hierarchy

### Creating Parent-Child Relationships

```bash
# Create parent goal
operately goals create \
  --space-id s1 \
  --name "Company Growth 2024" \
  --champion-id u1 \
  --anonymous-access-level 0 \
  --company-access-level 10 \
  --space-access-level 70

# Create child goals
operately goals create \
  --space-id s1 \
  --name "Q1 Revenue" \
  --parent-goal-id g1 \
  --champion-id u2 \
  --anonymous-access-level 0 \
  --company-access-level 10 \
  --space-access-level 70

operately goals create \
  --space-id s1 \
  --name "Q2 Revenue" \
  --parent-goal-id g1 \
  --champion-id u2 \
  --anonymous-access-level 0 \
  --company-access-level 10 \
  --space-access-level 70

operately goals create \
  --space-id s1 \
  --name "Customer Acquisition" \
  --parent-goal-id g1 \
  --champion-id u3 \
  --anonymous-access-level 0 \
  --company-access-level 10 \
  --space-access-level 70
```

### Updating Parent Goal

```bash
# Change parent
operately goals update_parent_goal \
  --goal-id g2 \
  --parent-goal-id g1

# Remove parent (make top-level)
operately goals update_parent_goal \
  --goal-id g2 \
  --parent-goal-id null
```

### Searching Parent Goals

```bash
operately goals search_parent_goal --query "growth" --goal-id g1
```

### Moving Goals Between Spaces

```bash
operately goals update_space \
  --goal-id g1 \
  --space-id s2
```

## Target Management

### Creating Different Target Types

**Numeric targets:**
```bash
operately goals create_target \
  --goal-id g1 \
  --name "New Customers" \
  --start-value 100 \
  --target-value 500 \
  --unit "customers"
```

**Currency targets:**
```bash
operately goals create_target \
  --goal-id g1 \
  --name "Revenue" \
  --start-value 1000000 \
  --target-value 2000000 \
  --unit "USD"
```

**Percentage targets:**
```bash
operately goals create_target \
  --goal-id g1 \
  --name "Market Share" \
  --start-value 15 \
  --target-value 25 \
  --unit "%"
```

### Updating Targets

```bash
# Update target definition
operately goals update_target \
  --goal-id g1 \
  --target-id t1 \
  --name "Updated Target Name" \
  --start-value 100 \
  --target-value 600 \
  --unit "customers"

# Update current value
operately goals update_target_value \
  --goal-id g1 \
  --target-id t1 \
  --value 350

# Reorder targets
operately goals update_target_index \
  --target-id t1 \
  --index 0
```

### Deleting Targets

```bash
operately goals delete_target --goal-id g1 --target-id t1
```

## Check-in Patterns

### Weekly Check-ins

```bash
operately goals create_check_in \
  --goal-id g1 \
  --status on_track \
  --due-date 2026-04-01 \
  --content "# Week 1 Update\n\n## Progress\n- MRR: $52,000 (+$2,000)\n- New customers: 15\n\n## Next Week\n- Launch marketing campaign\n- Close 3 enterprise deals"
```

### Monthly Check-ins

```bash
operately goals create_check_in \
  --goal-id g1 \
  --status on_track \
  --due-date 2026-04-01 \
  --content "# April Progress\n\n## Metrics\n- MRR: $60,000 (60% to target)\n- Customer count: 250 (50% to target)\n- Churn rate: 3% (below 5% target)\n\n## Highlights\n- Closed 2 enterprise deals\n- Product launch successful\n\n## Challenges\n- Sales cycle longer than expected\n\n## May Plan\n- Focus on mid-market segment\n- Accelerate onboarding"
```

### At-Risk Check-ins

```bash
operately goals create_check_in \
  --goal-id g1 \
  --status at_risk \
  --due-date 2026-04-01 \
  --content "# Risk Alert - Week 8\n\n## Issue\nMRR growth slowed to $1,000/week (need $3,000/week to hit target)\n\n## Root Cause\n- Marketing campaign underperforming\n- 2 enterprise deals delayed\n\n## Mitigation Plan\n- Revise marketing strategy\n- Increase sales outreach\n- Consider target adjustment"
```

### Off-Track Check-ins

```bash
operately goals create_check_in \
  --goal-id g1 \
  --status off_track \
  --due-date 2026-04-01 \
  --content "# Status Update - Week 10\n\n## Current State\nMRR: $58,000 (58% to target with 2 weeks left)\n\n## Analysis\nUnlikely to reach $100,000 target\n\n## Options\n1. Extend timeline to Q3\n2. Revise target to $75,000\n3. Close as partially achieved\n\n## Recommendation\nRevise target based on market conditions"
```

### Acknowledging Check-ins

```bash
# Reviewer acknowledges check-in
operately goals acknowledge_check_in --id ci1

# List check-ins
operately goals list_check_ins --goal-id g1

# Get specific check-in
operately goals get_check_in --id ci1

# Update check-in
operately goals update_check_in \
  --check-in-id ci1 \
  --status on_track \
  --content "# Updated Status\n\nRevised after team discussion."
```

## Roles and Responsibilities

### Champion

The champion owns the goal and drives execution.

```bash
# Set champion
operately goals update_champion \
  --goal-id g1 \
  --champion-id u1
```

Champion responsibilities:
- Regular check-ins
- Target updates
- Risk management
- Team coordination

### Reviewer

The reviewer provides oversight and accountability.

```bash
# Set reviewer
operately goals update_reviewer \
  --goal-id g1 \
  --reviewer-id u2
```

Reviewer responsibilities:
- Acknowledge check-ins
- Provide feedback
- Approve goal closure
- Escalate issues

## Goal Checks (Sub-goals/Milestones)

### Creating Checks

```bash
operately goals create_check \
  --goal-id g1 \
  --name "Launch new pricing tier"

operately goals create_check \
  --goal-id g1 \
  --name "Hire 2 sales reps"

operately goals create_check \
  --goal-id g1 \
  --name "Implement referral program"
```

### Managing Checks

```bash
# Toggle check completion
operately goals toggle_check --check-id c1

# Update check
operately goals update_check \
  --check-id c1 \
  --name "Updated check name"

# Reorder checks
operately goals update_check_index \
  --check-id c1 \
  --index 0

# Delete check
operately goals delete_check --check-id c1
```

## Goal Discussions

### Creating Discussions

```bash
operately goals create_discussion \
  --goal-id g1 \
  --title "Target Adjustment Discussion" \
  --message "# Should We Revise Our Q2 Target?\n\n## Context\nMarket conditions have changed.\n\n## Proposal\nRevise from $100K to $75K.\n\n## Feedback Needed\nThoughts from the team?"

operately goals create_discussion \
  --goal-id g1 \
  --title "Target Adjustment Discussion" \
  --message-file ./target-adjustment.md
```

### Managing Discussions

```bash
# List discussions
operately goals list_discussions --goal-id g1

# Update discussion
operately goals update_discussion \
  --activity-id d1 \
  --title "Updated Discussion Title" \
  --message "# Updated Content"

operately goals update_discussion \
  --activity-id d1 \
  --title "Updated Discussion Title" \
  --message-file ./updated-discussion.md
```

## Access Control

### Managing Access Members

```bash
# Add access members
operately goals create_access_members \
  --goal-id g1 \
  --members.0.id u1 \
  --members.0.access-level 70 \
  --members.1.id u2 \
  --members.1.access-level 40

# List access members
operately goals list_access_members --goal-id g1

# Update access level
operately goals update_access_member \
  --goal-id g1 \
  --person-id u1 \
  --access-level 70

# Remove access member
operately goals delete_access_member --goal-id g1 --person-id u1
```

### Updating Access Levels

```bash
operately goals update_access_levels \
  --goal-id g1 \
  --access-levels.public 0 \
  --access-levels.company 10 \
  --access-levels.space 70
```

Access levels:
- `0` - No access
- `10` - View only
- `40` - Comment
- `70` - Edit
- `100` - Full access

## Goal Lifecycle States

### Reopen Goal

```bash
operately goals get --id g1
```

Use cases:
- Goal closed prematurely
- New information requires continuation
- Quarterly goals rolling into next quarter

### Close Goal

```bash
# Achieved
operately goals close \
  --goal-id g1 \
  --success achieved \
  --success-status achieved \
  --retrospective "# Success!\n\nExceeded target by 15%."

# Not achieved
operately goals close \
  --goal-id g1 \
  --success no \
  --success-status missed \
  --retrospective "# Lessons Learned\n\nMarket conditions changed significantly."
```

## Common Patterns

## Gotchas

### Target Value Updates

Update target values regularly (weekly or bi-weekly) to keep progress visible. Don't wait until check-ins.

### Check-in vs Target Update

Check-ins are narrative updates. Target value updates are data points. Both are important.

### Parent Goal Changes

Changing a goal's parent affects visibility and reporting. Ensure the new parent's space has appropriate access.

### Goal Hierarchy Depth

Keep hierarchy shallow (2-3 levels max). Deep hierarchies become hard to manage:
- Level 1: Company/Annual goals
- Level 2: Department/Quarterly goals
- Level 3: Team/Monthly goals

### Access Control

Goals inherit space access by default. Use access members for cross-functional goals that need specific visibility.
