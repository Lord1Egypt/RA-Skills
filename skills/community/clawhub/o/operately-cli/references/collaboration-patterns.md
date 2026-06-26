# Collaboration Patterns

Team collaboration workflows in Operately, covering spaces, members, permissions, discussions, comments, reactions, and notifications.

## Space Management

### Creating Spaces

```bash
operately spaces create \
  --name "Engineering" \
  --mission "Build great products" \
  --company-permissions 10 \
  --public-permissions 0
```

### Getting Space Details

```bash
operately spaces get --id s1
```

### Listing Spaces

```bash
operately spaces list
```

### Searching Spaces

```bash
operately spaces search --query "engineering"
```

### Updating Spaces

```bash
operately spaces update \
  --id s1 \
  --name "Engineering & Product" \
  --mission "Build and ship great products"
```

### Deleting Spaces

```bash
operately spaces delete --space-id s1
```

## Member Management

### Adding Members

```bash
# Add single member
operately spaces add_members \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 70

# Add multiple members
operately spaces add_members \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 70 \
  --members.1.id u2 \
  --members.1.access-level 40 \
  --members.2.id u3 \
  --members.2.access-level 40
```

### Listing Members

```bash
operately spaces list_members --space-id s1
```

### Searching for Members

```bash
operately spaces search_potential_members \
  --space-id s1 \
  --query "engineer"
```

### Removing Members

```bash
operately spaces delete_member \
  --space-id s1 \
  --member-id u1
```

### Joining Spaces

```bash
# User joins a space
operately spaces join --space-id s1
```

## Permissions and Access Levels

### Member Permissions

```bash
operately spaces update_members_permissions \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 70 \
  --members.1.id u2 \
  --members.1.access-level 70
```

Access levels:
- `0` - No access
- `10` - View only
- `40` - Comment
- `70` - Edit
- `100` - Full access (admin)

### Space Permissions

```bash
operately spaces update_permissions \
  --space-id s1 \
  --access-levels.public 0 \
  --access-levels.company 10 \
  --access-levels.space 70
```

## Space Tools

### Listing Available Tools

```bash
operately spaces list_tools --space-id s1
```

### Enabling/Disabling Tools

```bash
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled true \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true
```

Common tool types:
- `projects` - Project management
- `goals` - Goal tracking
- `resource_hub` - Knowledge base
- `discussions` - Team discussions
- `tasks` - Task management

## Discussions

### Space Discussions

**Create discussion:**
```bash
operately spaces create_discussion \
  --space-id s1 \
  --title "Q2 Planning Discussion" \
  --body "# Q2 Planning\n\nLet's discuss our priorities for Q2.\n\n## Topics\n- Revenue goals\n- Product roadmap\n- Team growth"

operately spaces create_discussion \
  --space-id s1 \
  --title "Q2 Planning Discussion" \
  --body-file ./q2-planning.md
```

**List discussions:**
```bash
operately spaces list_discussions --space-id s1
```

**Get discussion:**
```bash
operately spaces get_discussion --id d1
```

**Update discussion:**
```bash
operately spaces update_discussion \
  --id d1 \
  --title "Updated: Q2 Planning" \
  --body "# Q2 Planning - Updated\n\n[revised content]"

operately spaces update_discussion \
  --id d1 \
  --title "Updated: Q2 Planning" \
  --body-file ./q2-planning-updated.md
```

**Archive discussion:**
```bash
operately spaces archive_discussion --id d1
```

**Publish discussion:**
```bash
operately spaces publish_discussion --id d1
```

### Project Discussions

**Create discussion:**
```bash
operately projects create_discussion \
  --project-id p1 \
  --title "Architecture Decision: Database" \
  --message "# Database Selection\n\n## Options\n1. PostgreSQL\n2. MongoDB\n\n## Recommendation\nPostgreSQL for ACID compliance."

operately projects create_discussion \
  --project-id p1 \
  --title "Architecture Decision: Database" \
  --message-file ./database-selection.md
```

**List discussions:**
```bash
operately projects list_discussions --project-id p1
```

**Get discussion:**
```bash
operately projects get_discussion --id d1
```

**Update discussion:**
```bash
operately projects update_discussion \
  --id d1 \
  --title "Decision Made: PostgreSQL" \
  --message "# Final Decision\n\nWe chose PostgreSQL."

operately projects update_discussion \
  --id d1 \
  --title "Decision Made: PostgreSQL" \
  --message-file ./final-decision.md
```

### Goal Discussions

**Create discussion:**
```bash
operately goals create_discussion \
  --goal-id g1 \
  --title "Target Adjustment Needed?" \
  --message "# Target Discussion\n\nShould we revise our Q2 target based on market conditions?"

operately goals create_discussion \
  --goal-id g1 \
  --title "Target Adjustment Needed?" \
  --message-file ./target-discussion.md
```

**List discussions:**
```bash
operately goals list_discussions --goal-id g1
```

**Update discussion:**
```bash
operately goals update_discussion \
  --activity-id d1 \
  --title "Target Revised" \
  --message "# Decision\n\nRevised target from $100K to $75K."

operately goals update_discussion \
  --activity-id d1 \
  --title "Target Revised" \
  --message-file ./target-revised.md
```

## Comments

### Creating Comments

```bash
# Comment on project check-in
operately comments create \
  --entity-id ci1 \
  --entity-type "project_check_in" \
  --content "Great progress! The design phase looks solid."

# Comment on goal check-in
operately comments create \
  --entity-id ci2 \
  --entity-type "goal_check_in" \
  --content "Concerned about the timeline. Can we discuss?"

# Comment on task
operately comments create \
  --entity-id t1 \
  --entity-type "task" \
  --content "I'll take this one. Should be done by EOD."

# Comment on discussion
operately comments create \
  --entity-id d1 \
  --entity-type "discussion" \
  --content "I agree with option 1. Here's why..."
```

Common entity types:
- `project_check_in`
- `goal_check_in`
- `task`
- `discussion`
- `document`
- `milestone`

### Listing Comments

```bash
operately comments list \
  --entity-id ci1 \
  --entity-type "project_check_in"
```

### Updating Comments

```bash
operately comments update \
  --comment-id c1 \
  --parent-type project_check_in \
  --content "Updated comment with more details."
```

### Deleting Comments

```bash
operately comments delete --comment-id c1 --parent-type project_check_in
```

## Reactions

### Adding Reactions

```bash
# Thumbs up
operately reactions create \
  --entity-id ci1 \
  --entity-type "project_check_in" \
  --emoji "👍"

# Heart
operately reactions create \
  --entity-id c1 \
  --entity-type "comment" \
  --parent-type "project_check_in" \
  --emoji "❤️"

# Celebrate
operately reactions create \
  --entity-id g1 \
  --entity-type "goal" \
  --emoji "🎉"
```

### Removing Reactions

```bash
operately reactions delete --reaction-id r1
```

## Notifications

### Listing Notifications

```bash
operately notifications list
```

### Getting Unread Count

```bash
operately notifications get_unread_count
```

### Managing Subscriptions

**Important:** Subscribe and unsubscribe commands require a `subscription-list-id`, not the resource ID. You must first retrieve the subscription list ID from the resource.

```bash
# Check subscription status (uses resource-id)
operately notifications is_subscribed \
  --resource-id p1 \
  --resource-type project

# Get subscription-list-id from the resource
operately projects get \
  --id p1 \
  --include-subscription-list

# Important: without --include-subscription-list, a missing
# subscription_list in the response means "not preloaded",
# not that the project lacks one.

# Subscribe to resource (uses subscription-list-id from above)
operately notifications subscribe \
  --subscription-list-id <subscription-list-id> \
  --type "project"

# Unsubscribe from subscription list (uses subscription-list-id)
operately notifications unsubscribe \
  --subscription-list-id <subscription-list-id>
```

### Marking as Read

```bash
# Mark single notification
operately notifications mark_as_read --id n1

# Mark multiple notifications
operately notifications mark_many_as_read \
  --ids n1 \
  --ids n2 \
  --ids n3

# Mark all as read
operately notifications mark_all_as_read
```

## Company-Level Operations

### Company Members

**Create member:**
```bash
operately companies create_member \
  --full-name "John Doe" \
  --email "john@example.com" \
  --title "Senior Engineer"
```

**Create admin:**
```bash
operately companies create_admins \
  --people-ids u1 \
  --people-ids u2
```

**Delete admin:**
```bash
operately companies delete_admin --person-id u1
```

**Delete member:**
```bash
operately companies delete_member --person-id u1
```

**Restore member:**
```bash
operately companies restore_member --person-id u1
```

**Convert member to guest:**
```bash
operately companies convert_member_to_guest --person-id u1
```

**Invite guest:**
```bash
operately companies invite_guest \
  --email "guest@example.com" \
  --full-name "Guest User" \
  --title "Consultant"
```

### Company Permissions

```bash
operately companies update_members_permissions \
  --members.0.id u1 \
  --members.0.access-level edit_access \
  --members.1.id u2 \
  --members.1.access-level edit_access
```

### Resource Access

```bash
operately companies grant_resource_access \
  --person-id u1 \
  --resources.0.resource-type project \
  --resources.0.resource-id p1 \
  --resources.0.access-level view_access \
  --resources.1.resource-type goal \
  --resources.1.resource-id g1 \
  --resources.1.access-level edit_access
```

### Global Search

```bash
operately companies global_search --query "roadmap"
```

### Activity Feed

```bash
# Get company activity
operately companies get_activity --id a1

# List activities
operately companies list_activities \
  --scope-id c1 \
  --scope-type company \
  --actions project_created \
  --actions goal_created \
  --actions project_check_in_submitted
```

## Common Collaboration Patterns

### New Team Onboarding

```bash
# 1. Create space
operately spaces create \
  --name "Product Team" \
  --mission "Deliver customer value" \
  --company-permissions 10 \
  --public-permissions 0

# 2. Add team members
operately spaces add_members \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 100 \
  --members.1.id u2 \
  --members.1.access-level 70 \
  --members.2.id u3 \
  --members.2.access-level 70

# 3. Set permissions
operately spaces update_members_permissions \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 100  # Team lead - full access

operately spaces update_members_permissions \
  --space-id s1 \
  --members.0.id u2 \
  --members.0.access-level 70 \
  --members.1.id u3 \
  --members.1.access-level 70  # Team members - edit access

# 4. Enable tools
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled true \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true

# 5. Find the space's resource hub ID
operately spaces list_tools --space-id s1

# 6. Create welcome discussion
operately spaces create_discussion \
  --space-id s1 \
  --title "Welcome to Product Team!" \
  --body "# Welcome!\n\nGlad to have you on the team.\n\n## Getting Started\n- Review our resource hub\n- Join daily standups\n- Introduce yourself"
```

### Cross-Functional Project

```bash
# 1. Create project in shared space
operately projects create \
  --space-id shared_space \
  --name "Product Launch" \
  --champion-id product_lead \
  --anonymous-access-level 0 \
  --company-access-level 10 \
  --space-access-level 70

# 2. Add contributors from different teams
operately projects create_contributor \
  --project-id p1 \
  --person-id eng_lead \
  --responsibility "Engineering Lead" \
  --permissions edit_access \
  --role contributor

operately projects create_contributor \
  --project-id p1 \
  --person-id design_lead \
  --responsibility "Design Lead" \
  --permissions edit_access \
  --role contributor

operately projects create_contributor \
  --project-id p1 \
  --person-id marketing_lead \
  --responsibility "Marketing Lead" \
  --permissions edit_access \
  --role contributor

# 3. Create discussion for alignment
operately projects create_discussion \
  --project-id p1 \
  --title "Launch Timeline Discussion" \
  --message "# Timeline\n\nLet's align on the launch date and key milestones."
```

## Gotchas

### Discussion vs Comments

Discussions are top-level conversation starters. Comments are responses to existing content. Use discussions for new topics, comments for feedback.

### Reactions vs Comments

Use reactions for quick reactions (👍, ❤️, 🎉). Use comments for substantive feedback.

### Entity Types

Entity types must match exactly:

```bash
# Wrong
operately comments create \
  --entity-id ci1 \
  --entity-type "check_in"  # ❌

# Right
operately comments create \
  --entity-id ci1 \
  --entity-type "project_check_in"  # ✅
```

### Space Tools

Disabling a tool (e.g., projects) doesn't delete existing resources, but makes them inaccessible through the space. Re-enable to restore access.

### Guest Access

Guests have limited access. Use `convert_member_to_guest` carefully - it restricts their permissions across the company. People who work in the company should never be converted to guests. Guests should only be used for external collaborators.

### Subscription Management

Subscriptions are resource-specific. Subscribing to a project doesn't subscribe to its tasks or milestones. Subscribe to each resource separately if needed.
