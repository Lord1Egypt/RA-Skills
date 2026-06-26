# Project Workflows

Complete lifecycle patterns for managing projects in Operately, from creation through milestones, tasks, check-ins, and closure.

## Project Lifecycle

### 1. Create Project

```bash
operately projects create \
  --space-id s1 \
  --name "Q2 Product Roadmap" \
  --champion-id u1 \
  --reviewer-id u2 \
  --anonymous-access-level 0 \
  --company-access-level 40 \
  --space-access-level 70
```

Optional fields:
- `--description` - Markdown project description
- `--goal-id` - Link to parent goal

**Note:** Access levels are required. Use `--company-access-level 40 --space-access-level 70` for typical team projects.

### 2. Set Up Milestones

```bash
# Create milestones
operately projects create_milestone \
  --project-id p1 \
  --name "Design Phase" \
  --due-date 2024-05-15

operately projects create_milestone \
  --project-id p1 \
  --name "Development Phase" \
  --due-date 2024-06-15

operately projects create_milestone \
  --project-id p1 \
  --name "Launch" \
  --due-date 2024-06-30
```

### 3. Add Contributors

```bash
# Add team members with roles
operately projects create_contributor \
  --project-id p1 \
  --person-id u3 \
  --responsibility "Lead Designer" \
  --permissions edit_access \
  --role reviewer

operately projects create_contributor \
  --project-id p1 \
  --person-id u4 \
  --responsibility "Backend Engineer" \
  --permissions edit_access \
  --role contributor

operately projects create_contributor \
  --project-id p1 \
  --person-id u5 \
  --responsibility "QA Lead" \
  --permissions edit_access \
  --role contributor
```

### 4. Create Tasks

```bash
# Create tasks for milestones
operately tasks create \
  --type project \
  --id p1 \
  --name "Create wireframes" \
  --milestone-id m1 \
  --assignee-id u3 \
  --due-date 2024-05-10

operately tasks create \
  --type project \
  --id p1 \
  --name "Design mockups" \
  --milestone-id m1 \
  --assignee-id u3 \
  --due-date 2024-05-15

operately tasks create \
  --type project \
  --id p1 \
  --name "API development" \
  --milestone-id m2 \
  --assignee-id u4 \
  --due-date 2024-06-10
```

### 5. Regular Check-ins

```bash
# Weekly check-in
operately projects create_check_in \
  --project-id p1 \
  --status on_track \
  --description "# Week 1 Progress\n\n## Completed\n- Wireframes done\n- Design review scheduled\n\n## Next Week\n- Start mockups\n- Finalize color palette"

# Off-track check-in
operately projects create_check_in \
  --project-id p1 \
  --status off_track \
  --description "# Week 3 Progress\n\n## Issues\n- API development delayed due to infrastructure issues\n\n## Mitigation\n- Working with DevOps to resolve\n- May need to extend milestone by 3 days"
```

### 6. Update Project Status

```bash
# Update milestone dates
operately projects update_milestone_due_date \
  --milestone-id m2 \
  --due-date 2024-06-18

# Update task status
operately tasks update_status --task-id t1 --type project --status.id done --status.label "Done" --status.color green --status.index 2 --status.value done --status.closed true
operately tasks update_status --task-id t2 --type project --status.id in_progress --status.label "In Progress" --status.color blue --status.index 1 --status.value in_progress --status.closed false
```

### 7. Close Project

```bash
operately projects close \
  --project-id p1 \
  --retrospective "# Project Retrospective\n\n## What Went Well\n- Strong team collaboration\n- Clear milestones\n\n## What Could Improve\n- Earlier infrastructure planning\n- More frequent stakeholder updates" \
  --success-status achieved
```

## Milestone Management Patterns

### Creating Milestones

```bash
operately projects create_milestone \
  --project-id p1 \
  --name "Phase 1: Discovery" \
  --due-date 2024-05-01

operately projects create_milestone \
  --project-id p1 \
  --name "Phase 2: Implementation" \
  --due-date 2024-06-01

operately projects create_milestone \
  --project-id p1 \
  --name "Phase 3: Launch" \
  --due-date 2024-06-30
```

### Updating Milestone Details

```bash
# Update title
operately projects update_milestone_title \
  --milestone-id m1 \
  --title "Phase 1: Discovery & Research"

# Update description
operately projects update_milestone_description \
  --milestone-id m1 \
  --description "# Discovery Phase\n\n## Goals\n- User research\n- Competitive analysis\n- Requirements gathering"

# Update due date
operately projects update_milestone_due_date \
  --milestone-id m1 \
  --due-date 2024-05-05
```

### Milestone Task Management

```bash
# List tasks for a milestone
operately projects list_milestone_tasks --milestone-id m1
```

## Contributor Workflows

### Adding Contributors

```bash
# Single contributor
operately projects create_contributor \
  --project-id p1 \
  --person-id u1 \
  --responsibility "Technical Lead" \
  --permissions edit_access \
  --role reviewer

# Multiple contributors
operately projects create_contributors \
  --project-id p1 \
  --contributors.0.person-id u2 \
  --contributors.0.responsibility "Product Lead" \
  --contributors.0.access-level edit_access \
  --contributors.1.person-id u3 \
  --contributors.1.responsibility "Engineering Lead" \
  --contributors.1.access-level edit_access \
  --contributors.2.person-id u4 \
  --contributors.2.responsibility "Designer" \
  --contributors.2.access-level comment_access
```

### Managing Contributors

```bash
# List contributors
operately projects list_contributors --project-id p1

# Get contributor details
operately projects get_contributor --contributor-id c1

# Update responsibility
operately projects update_contributor \
  --contrib-id c1 \
  --responsibility "Lead Engineer & Architecture Owner"

# Remove contributor
operately projects delete_contributor --contrib-id c1
```

### Searching for Contributors

```bash
operately projects search_potential_contributors \
  --project-id p1 \
  --query "engineer"
```

## Key Resources

### Adding Resources

```bash
# Add design doc
operately projects create_key_resource \
  --project-id p1 \
  --title "Technical Design" \
  --link "https://docs.example.com/design" \
  --resource-type "document"

# Add Figma link
operately projects create_key_resource \
  --project-id p1 \
  --title "Design Mockups" \
  --link "https://figma.com/file/abc123" \
  --resource-type "design"
```

### Managing Resources

```bash
# Get resource
operately projects get_key_resource --id kr1

# Update resource
operately projects update_key_resource \
  --id kr1 \
  --title "Updated Design Doc" \
  --url "https://docs.example.com/design-v2"

# Delete resource
operately projects delete_key_resource --id kr1
```

## Project Discussions

### Creating Discussions

```bash
operately projects create_discussion \
  --project-id p1 \
  --title "Architecture Decision: Database Choice" \
  --message "# Database Selection\n\n## Options\n1. PostgreSQL\n2. MongoDB\n\n## Recommendation\nPostgreSQL for ACID compliance."

operately projects create_discussion \
  --project-id p1 \
  --title "Architecture Decision: Database Choice" \
  --message-file ./database-choice.md
```

### Managing Discussions

```bash
# List discussions
operately projects list_discussions --project-id p1

# Get discussion
operately projects get_discussion --id d1

# Update discussion
operately projects update_discussion \
  --id d1 \
  --title "Updated: Database Decision" \
  --message "# Final Decision\n\nWe chose PostgreSQL."

operately projects update_discussion \
  --id d1 \
  --title "Updated: Database Decision" \
  --message-file ./final-decision.md
```

## Check-in Patterns

### Weekly Status Updates

```bash
operately projects create_check_in \
  --project-id p1 \
  --status on_track \
  --description "# Weekly Update - Week of May 1\n\n## Progress\n- Completed 5 tasks\n- Design review approved\n\n## Next Week\n- Start development\n- Set up CI/CD"
```

### Milestone Completion Check-in

```bash
operately projects create_check_in \
  --project-id p1 \
  --status on_track \
  --description "# Milestone Complete: Design Phase\n\n## Deliverables\n- ✅ Wireframes\n- ✅ High-fidelity mockups\n- ✅ Design system components\n\n## Next Milestone\nStarting development phase."
```

### Off-Track Check-in

```bash
operately projects create_check_in \
  --project-id p1 \
  --status off_track \
  --description "# Risk Alert\n\n## Issue\nKey engineer on leave, development delayed.\n\n## Mitigation\n- Reassigning tasks\n- Extending timeline by 1 week\n- Daily standups for visibility"
```

### Acknowledging Check-ins

```bash
# Reviewer acknowledges check-in
operately projects acknowledge_check_in --id ci1

# List check-ins
operately projects list_check_ins --project-id p1

# Get specific check-in
operately projects get_check_in --id ci1
```

## Retrospectives

### Updating Retrospective

```bash
operately projects update_retrospective \
  --retrospective-id r1 \
  --content "# Q2 Roadmap Retrospective\n\n## What Went Well\n- Clear milestones and deliverables\n- Strong team collaboration\n- Regular check-ins kept everyone aligned\n\n## What Could Improve\n- Earlier infrastructure planning\n- More buffer time for QA\n- Better stakeholder communication\n\n## Action Items\n- Document infrastructure requirements upfront\n- Add 20% buffer to estimates\n- Weekly stakeholder updates" \
  --success-status achieved
```

### Getting Retrospective

```bash
operately projects get_retrospective --project-id p1
```

## Project Permissions

### Updating Access Levels

```bash
operately projects update_permissions \
  --project-id p1 \
  --public false \
  --anonymous-access-level 0 \
  --company-access-level 10 \
  --space-access-level 70
```

Access levels:
- `0` - No access
- `10` - View only
- `40` - Comment
- `70` - Edit
- `100` - Full access

## Moving Projects

### Move to Different Space

```bash
operately projects move_to_space \
  --project-id p1 \
  --space-id s2
```

## Project States

### Pause Project

```bash
operately projects pause \
  --project-id p1 \
  --reason "Waiting for budget approval"
```

### Resume Project

```bash
operately projects resume --project-id p1
```

## Gotchas

### Milestone Ordering

Milestones are ordered by the sequence in `update_milestone_ordering`. If you don't specify order, they appear in creation order.

### Task Status IDs

Task status IDs are project-specific. Use `operately projects get --id p1` to see available statuses for a project.

### Check-in Frequency

Regular check-ins (weekly or bi-weekly) keep stakeholders informed and help catch issues early. Don't wait for problems to create check-ins.

### Contributor vs Member

Contributors are project-specific roles. Space members have broader access. Add contributors to clarify project responsibilities and give them specific permissions.
