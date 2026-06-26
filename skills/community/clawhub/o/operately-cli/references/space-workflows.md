# Space Workflows

Complete workflows for managing spaces in Operately, covering space creation, member management, tools configuration, discussions, tasks, and access control.

## Space Lifecycle

### 1. Create Space

```bash
operately spaces create \
  --name "Engineering" \
  --mission "Build great products" \
  --company-permissions 10 \
  --public-permissions 0
```

**Permission values:**
- `0` - No access
- `10` - View only
- `40` - Comment
- `70` - Edit
- `100` - Full access

**Common patterns:**
- **Open team space**: `--company-permissions 10`
- **Secret space**: `--company-permissions 0`
- **Collaborative space**: `--company-permissions 40`

### 2. Configure Space Tools

```bash
# List available tools and their status
operately spaces list_tools --space-id s1

# Enable all tools
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled true \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true

# Enable only specific tools
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled true \
  --tools.discussions-enabled false \
  --tools.resource-hub-enabled true
```

**Note:** The `list_tools` command returns the resource hub ID needed for document and link operations.

### 3. Add Members

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
  --members.0.access-level 100 \
  --members.1.id u2 \
  --members.1.access-level 70 \
  --members.2.id u3 \
  --members.2.access-level 40
```

### 4. Update Space Details

```bash
operately spaces update \
  --id s1 \
  --name "Platform Engineering" \
  --mission "Build and maintain scalable infrastructure"
```

### 5. Manage Space

```bash
# List all spaces
operately spaces list

# Get space details
operately spaces get --id s1

# Search for spaces
operately spaces search --query "engineering"

# Delete space
operately spaces delete --space-id s1
```

## Member Management Patterns

### Adding Members

```bash
# Add team lead with full access
operately spaces add_members \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 100

# Add team members with edit access
operately spaces add_members \
  --space-id s1 \
  --members.0.id u2 \
  --members.0.access-level 70 \
  --members.1.id u3 \
  --members.1.access-level 70

# Add observers with comment access
operately spaces add_members \
  --space-id s1 \
  --members.0.id u4 \
  --members.0.access-level 40
```

### Managing Members

```bash
# List space members
operately spaces list_members --space-id s1

# Update member permissions
operately spaces update_members_permissions \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 100

# Update multiple members at once
operately spaces update_members_permissions \
  --space-id s1 \
  --members.0.id u2 \
  --members.0.access-level 70 \
  --members.1.id u3 \
  --members.1.access-level 40

# Remove member
operately spaces delete_member \
  --space-id s1 \
  --member-id u1
```

### Searching for Members

```bash
# Search for potential members
operately spaces search_potential_members \
  --space-id s1 \
  --query "engineer"

# Search with exclusions
operately spaces search_potential_members \
  --space-id s1 \
  --query "john" \
  --exclude-ids u1 \
  --exclude-ids u2

# Limit results
operately spaces search_potential_members \
  --space-id s1 \
  --query "developer" \
  --limit 10
```

### Joining Spaces

```bash
# Join a space (if permitted)
operately spaces join --space-id s1
```

## Space Tools Configuration

### Understanding Space Tools

Spaces support three tools:
- **Tasks** - Task management and Kanban boards
- **Discussions** - Team conversations and updates
- **Resource Hub** - Documents, files, and links

### Enabling Tools

```bash
# Check current tool status
operately spaces list_tools --space-id s1

# Enable tasks for team task management
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled true \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true

# Disable unused tools
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled false \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true
```

### Working with Enabled Tools

Once tools are enabled:

**Tasks:**
```bash
# Create space task
operately tasks create \
  --type space \
  --id s1 \
  --name "Update documentation" \
  --milestone-id null \
  --assignee-id u1 \
  --due-date 2024-06-15

# List space tasks
operately spaces list_tasks --space-id s1
```

**Discussions:**
```bash
# Create discussion
operately spaces create_discussion \
  --space-id s1 \
  --title "Q2 Planning" \
  --body "# Q2 Planning\n\nLet's discuss our priorities."

# Create discussion from a markdown file
operately spaces create_discussion \
  --space-id s1 \
  --title "Q2 Planning" \
  --body-file ./q2-planning.md
```

**Resource Hub:**
```bash
# Get resource hub ID from list_tools, then use documents/links commands
operately documents create \
  --resource-hub-id rh1 \
  --name "Team Guide" \
  --content "# Getting Started"
```

## Space Discussions

### Creating Discussions

```bash
# Basic discussion
operately spaces create_discussion \
  --space-id s1 \
  --title "Team Sync" \
  --body "# Weekly Sync\n\n## Topics\n- Sprint planning\n- Blockers"

# Draft discussion
operately spaces create_discussion \
  --space-id s1 \
  --title "Proposal: New Architecture" \
  --body "# Architecture Proposal\n\nDetailed proposal..." \
  --post-as-draft true

# Discussion with notifications
operately spaces create_discussion \
  --space-id s1 \
  --title "Important Update" \
  --body "# Important Update\n\nPlease review..." \
  --send-notifications-to-everyone true

# Discussion with specific subscribers
operately spaces create_discussion \
  --space-id s1 \
  --title "Technical Review" \
  --body "# Code Review\n\nReview needed..." \
  --subscriber-ids u1 \
  --subscriber-ids u2
```

### Managing Discussions

```bash
# List discussions
operately spaces list_discussions --space-id s1

# List with metadata
operately spaces list_discussions \
  --space-id s1 \
  --include-author \
  --include-comments-count

# List including drafts
operately spaces list_discussions \
  --space-id s1 \
  --include-my-drafts

# If author, comments_count, or my_drafts is missing from the response,
# that means the matching --include-* flag was not requested,
# not that the discussion or drafts do not exist.

# Get discussion details
operately spaces get_discussion --id d1

# Update discussion
operately spaces update_discussion \
  --id d1 \
  --title "Updated Title" \
  --body "# Updated Content"

# Update discussion from a markdown file
operately spaces update_discussion \
  --id d1 \
  --title "Updated Title" \
  --body-file ./updated-content.md

# Publish draft
operately spaces publish_discussion --id d1

# Archive discussion
operately spaces archive_discussion --id d1
```

## Space Tasks

### Enabling Space Tasks

```bash
# Enable tasks tool first
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled true \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true
```

### Creating Space Tasks

```bash
# Basic space task
operately tasks create \
  --type space \
  --id s1 \
  --name "Review documentation" \
  --milestone-id null \
  --assignee-id u1 \
  --due-date 2024-06-15

# Unassigned space task
operately tasks create \
  --type space \
  --id s1 \
  --name "Update onboarding guide" \
  --milestone-id null \
  --assignee-id null \
  --due-date null
```

**Note:** Space tasks cannot belong to milestones. Always set `--milestone-id null`.

### Managing Space Tasks

```bash
# List space tasks
operately spaces list_tasks --space-id s1

# Update task status
operately tasks update_status \
  --task-id t1 \
  --type space \
  --status.id done \
  --status.label "Done" \
  --status.color green \
  --status.index 2 \
  --status.value done \
  --status.closed true

# Update assignee
operately tasks update_assignee \
  --task-id t1 \
  --type space \
  --assignee-id u2

# Update due date
operately tasks update_due_date \
  --task-id t1 \
  --type space \
  --due-date 2024-06-20
```

### Custom Task Statuses for Spaces

```bash
# Update space task statuses
operately spaces update_task_statuses \
  --space-id s1 \
  --task-statuses.0.id ts1 \
  --task-statuses.0.label "To Do" \
  --task-statuses.0.color gray \
  --task-statuses.0.index 0 \
  --task-statuses.0.value todo \
  --task-statuses.0.closed false \
  --task-statuses.1.id ts2 \
  --task-statuses.1.label "In Progress" \
  --task-statuses.1.color blue \
  --task-statuses.1.index 1 \
  --task-statuses.1.value in_progress \
  --task-statuses.1.closed false \
  --task-statuses.2.id ts3 \
  --task-statuses.2.label "Done" \
  --task-statuses.2.color green \
  --task-statuses.2.index 2 \
  --task-statuses.2.value done \
  --task-statuses.2.closed true
```

## Access Control Patterns

### Understanding Access Levels

Spaces have two permission layers:
- **Company-wide access** - Baseline for all company members
- **Member access** - Explicit access for added members

The most permissive level applies when both are present.

### Updating Permissions

```bash
# Update company-wide access
operately spaces update_permissions \
  --space-id s1 \
  --access-levels.company 10

# Make space secret (no company access)
operately spaces update_permissions \
  --space-id s1 \
  --access-levels.company 0

# Update space member default access
operately spaces update_permissions \
  --space-id s1 \
  --access-levels.space 70

# Update multiple levels
operately spaces update_permissions \
  --space-id s1 \
  --access-levels.public 0 \
  --access-levels.company 40 \
  --access-levels.space 70
```

### Access Level Meanings

- **0 (No Access)** - Cannot see or access the space
- **10 (View)** - Can see space and content
- **40 (Comment)** - View + comment on resources
- **70 (Edit)** - Comment + create/edit content
- **100 (Full Access)** - Edit + manage members and settings

### Secret Space Pattern

```bash
# Create secret space
operately spaces create \
  --name "Leadership Team" \
  --mission "Strategic planning and decisions" \
  --company-permissions 0 \
  --public-permissions 0

# Add specific members
operately spaces add_members \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 100 \
  --members.1.id u2 \
  --members.1.access-level 70
```

### Public Space Pattern

```bash
# Create public space
operately spaces create \
  --name "Company Updates" \
  --mission "Company-wide announcements and news" \
  --company-permissions 40 \
  --public-permissions 0

# Everyone can view and comment, space members can edit
operately spaces add_members \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 70
```

## Common Patterns

### Department Space Setup

```bash
# 1. Create department space
operately spaces create \
  --name "Engineering" \
  --mission "Build and maintain product infrastructure" \
  --company-permissions 10 \
  --public-permissions 0

# 2. Enable tools
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled true \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true

# 3. Add department members
operately spaces add_members \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 100 \
  --members.1.id u2 \
  --members.1.access-level 70 \
  --members.2.id u3 \
  --members.2.access-level 70

# 4. Create initial discussion
operately spaces create_discussion \
  --space-id s1 \
  --title "Welcome to Engineering" \
  --body "# Welcome\n\nThis is our team space for collaboration."
```

### Cross-Functional Team Space

```bash
# 1. Create project team space
operately spaces create \
  --name "Product Launch Team" \
  --mission "Coordinate Q2 product launch" \
  --company-permissions 10 \
  --public-permissions 0

# 2. Add members from different departments
operately spaces add_members \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 100 \
  --members.1.id u2 \
  --members.1.access-level 70 \
  --members.2.id u3 \
  --members.2.access-level 70 \
  --members.3.id u4 \
  --members.3.access-level 70

# 3. Enable tasks for coordination
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled true \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true

# 4. Create coordination tasks
operately tasks create \
  --type space \
  --id s1 \
  --name "Finalize launch plan" \
  --milestone-id null \
  --assignee-id u1 \
  --due-date 2024-06-01

operately tasks create \
  --type space \
  --id s1 \
  --name "Prepare marketing materials" \
  --milestone-id null \
  --assignee-id u2 \
  --due-date 2024-06-10
```

### Private Leadership Space

```bash
# 1. Create secret space
operately spaces create \
  --name "Executive Team" \
  --mission "Strategic planning and leadership decisions" \
  --company-permissions 0 \
  --public-permissions 0

# 2. Add leadership team only
operately spaces add_members \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 100 \
  --members.1.id u2 \
  --members.1.access-level 100 \
  --members.2.id u3 \
  --members.2.access-level 100

# 3. Enable discussions for strategic conversations
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled false \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true
```

### Company-Wide Announcement Space

```bash
# 1. Create public space
operately spaces create \
  --name "Company News" \
  --mission "Company-wide updates and announcements" \
  --company-permissions 40 \
  --public-permissions 0

# 2. Add content managers with edit access
operately spaces add_members \
  --space-id s1 \
  --members.0.id u1 \
  --members.0.access-level 100 \
  --members.1.id u2 \
  --members.1.access-level 70

# 3. Enable discussions only
operately spaces update_tools \
  --space-id s1 \
  --tools.tasks-enabled false \
  --tools.discussions-enabled true \
  --tools.resource-hub-enabled true

# 4. Post announcement
operately spaces create_discussion \
  --space-id s1 \
  --title "Q2 Company Update" \
  --body "# Q2 Update\n\n## Highlights\n- Revenue growth\n- New hires\n- Product launches" \
  --send-notifications-to-everyone true
```

## Gotchas

### Space vs Project Tasks

- **Space tasks** cannot belong to milestones (always `--milestone-id null`)
- **Project tasks** can belong to milestones
- Both use the same task commands with different `--type` parameter

### Tool Enablement

Tools must be enabled before use:
- Enable tasks tool before creating space tasks
- Enable discussions tool before creating discussions
- Resource hub is typically enabled by default

### Access Level Conflicts

When a user has both company-wide and member-specific access, the **higher** level applies. Use this to grant elevated access to specific members while keeping company-wide access restricted.

### Permission Updates

Updating space permissions affects future access. Existing members retain their explicit access levels unless updated separately via `update_members_permissions`.

## Count and Search

### Counting Spaces

```bash
# Count spaces by access level
operately spaces count_by_access_level --access-level view_access
```

### Searching Spaces

```bash
# Search for spaces
operately spaces search --query "engineering"
```
