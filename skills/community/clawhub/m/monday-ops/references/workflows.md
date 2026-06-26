
Detailed step-by-step workflows for common monday.com operations. Each workflow follows the Discover → Plan → Execute pattern.

---

## 1. Project Setup from Scratch

**Trigger:** User says "create a project board for X" or "set up a board to track Y"

### Steps

1. **Gather requirements** — Ask the user:
   - What is the project name?
   - What stages/phases should items move through? (Default: To Do → In Progress → Review → Done)
   - What information should be tracked per item? (Default: Status, Assignee, Due Date, Priority)
   - Any specific team members to add?

2. **Create the board**
   ```
   create_board(name="Project Name", board_kind="public")
   ```
   Save the returned `board_id`.

3. **Create groups** for each stage
   ```
   create_group(board_id, group_name="To Do")
   create_group(board_id, group_name="In Progress")
   create_group(board_id, group_name="Review")
   create_group(board_id, group_name="Done")
   ```

4. **Add columns** based on requirements
   ```
   create_column(board_id, title="Priority", column_type="status")
   create_column(board_id, title="Due Date", column_type="date")
   create_column(board_id, title="Assignee", column_type="people")
   create_column(board_id, title="Effort (hours)", column_type="numbers")
   create_column(board_id, title="Notes", column_type="long_text")
   ```

5. **Create initial items** if the user provided tasks
   ```
   get_board_schema(board_id)  # Get column IDs for the new columns
   create_item(board_id, item_name="Task 1", group_id="...", column_values={...})
   ```

6. **Present results** — Show the board URL and a summary of what was created.

---

## 2. Sprint Planning Board

**Trigger:** User says "set up a sprint board" or "plan sprint N"

### Steps

1. **Create or identify the board**
   - If new: `create_board(name="Sprint N - Team Name")`
   - If existing: `get_board_schema(board_id)` to understand structure

2. **Create sprint groups**
   ```
   create_group(board_id, "Sprint Backlog")
   create_group(board_id, "In Development")
   create_group(board_id, "Code Review")
   create_group(board_id, "QA")
   create_group(board_id, "Done")
   ```

3. **Ensure required columns exist** (check schema first)
   - Status (status) — Sprint status
   - Assignee (people) — Developer
   - Story Points (numbers) — Effort estimate
   - Due Date (date) — Sprint end date
   - Priority (status) — P0/P1/P2/P3
   - PR Link (link) — Pull request URL

4. **Populate with backlog items** from user input or existing board

5. **Post a sprint kickoff update** on each item summarizing scope

---

## 3. Status Report / Sprint Summary

**Trigger:** User says "give me a status report" or "sprint summary for board X"

### Steps

1. **Discover the board**
   ```
   get_board_schema(board_id)
   ```
   Identify the status column ID, group structure, and people column.

2. **Fetch all items**
   ```
   get_board_items_by_name(board_id, term="")  # Empty term = all items
   ```
   May need multiple calls if paginated.

3. **Aggregate data**
   Group items by:
   - Status (Done / In Progress / Stuck / Not Started)
   - Assignee
   - Group (sprint phase)

4. **Calculate metrics**
   - Total items
   - Completion rate (Done / Total)
   - Items per status
   - Items per person
   - Overdue items (compare due dates to today)

5. **Present the report** as a clear summary table. Example format:
   ```
   ## Sprint 5 Status Report
   **Board:** [Board Name](url)
   **Total Items:** 24 | **Done:** 12 (50%) | **In Progress:** 8 | **Stuck:** 2 | **Not Started:** 2

   ### By Status
   - ✅ Done: 12
   - 🔄 In Progress: 8
   - 🚫 Stuck: 2
   - ⬜ Not Started: 2

   ### Stuck Items (need attention)
   - "Fix auth bug" — assigned to [Person], due 2026-05-01 (overdue)
   - "API rate limiting" — unassigned
   ```

---

## 4. Bulk Item Creation

**Trigger:** User provides a list of tasks to create, or says "add these items to board X"

### Steps

1. **Parse the task list** from the user's message. Extract:
   - Item names
   - Any mentioned statuses, dates, assignees, priorities

2. **Discover the board**
   ```
   get_board_schema(board_id)
   ```
   Map the user's field names to column IDs.

3. **Resolve people references**
   If the user mentions names, call `list_users_and_teams` to get user IDs.

4. **Identify the target group**
   Default to the first group unless the user specifies otherwise.

5. **Create items sequentially**
   ```
   for each task:
     create_item(board_id, item_name, group_id, column_values)
   ```
   Report progress: "Created 3 of 10 items..."

6. **Summary** — List all created items with their IDs.

---

## 5. Triage and Routing

**Trigger:** User says "triage the intake board" or "sort incoming requests"

### Steps

1. **Discover the board structure**
   ```
   get_board_schema(board_id)
   ```
   Identify: intake group, destination groups, status/priority columns.

2. **Fetch intake items**
   ```
   get_board_items_by_name(board_id, term="")  # Filter to intake group
   ```

3. **For each item, determine routing:**
   - Read the item title and any description
   - Suggest a priority level based on keywords (e.g., "urgent", "blocker" → high priority)
   - Suggest an assignee based on domain (if user provides routing rules)
   - Suggest a destination group

4. **Present the triage plan** to the user for approval:
   ```
   | Item | Suggested Priority | Assignee | Route To |
   |------|-------------------|----------|----------|
   | Fix login bug | Critical | Dev Team | Sprint Backlog |
   | Update docs | Low | Content Team | Backlog |
   ```

5. **Execute after approval**
   ```
   change_item_column_values(item_id, {priority, assignee, ...})
   move_item_to_group(item_id, target_group_id)
   create_update(item_id, "Triaged: Priority set to X, routed to Y group.")
   ```

---

## 6. Meeting Action Items → Board Items

**Trigger:** User says "create tasks from this meeting" or provides meeting notes / Fireflies transcript

### Steps

1. **Extract action items** from the meeting content
   - Look for patterns: "Action item:", "[Person] will...", "TODO:", "Follow up on..."
   - Extract: task description, assignee name, due date if mentioned

2. **Identify or create the target board**
   - Ask which board to add items to, or create a new one

3. **Discover board schema and resolve people**
   ```
   get_board_schema(board_id)
   list_users_and_teams(name="person name")  # For each mentioned person
   ```

4. **Create items with context**
   ```
   create_item(board_id, item_name, column_values={status, assignee, date})
   create_update(item_id, "Created from meeting: [Meeting Title]\nContext: [relevant excerpt]")
   ```

5. **Summary** — Show all created items with assignees and due dates.

---

## 7. Cross-Board Reporting

**Trigger:** User says "status across all boards" or "what's blocking the launch?"

This workflow requires Dynamic API Tools to query multiple boards efficiently.

### Steps

1. **Use `all_monday_api`** to query boards:
   ```graphql
   query {
     boards(ids: [board1_id, board2_id, board3_id]) {
       name
       groups { id title }
       items_page(limit: 100) {
         items {
           name
           group { title }
           column_values { id text value }
         }
       }
     }
   }
   ```

2. **Aggregate across boards** — Count items by status, find blockers, identify overdue items.

3. **Present a unified report** organized by board, with cross-board metrics.

---

## 8. Automating Recurring Workflows

**Trigger:** User says "every week, update the status board" or "automate X"

Claude cannot create persistent automations, but can execute the workflow on demand. For each request:

1. **Document the workflow** clearly so the user can re-trigger it.
2. **Execute all steps** in the current session.
3. **Suggest monday.com native automations** for truly recurring needs (e.g., "When status changes to Done, move to Done group").

---

## Integration Workflows

### monday.com → Google Calendar

After creating items with due dates:
```
1. Get the due date from the item's column values
2. Google Calendar: create_event(summary="[Item Name]", startTime=due_date, ...)
3. create_update(item_id, "Calendar event created for due date.")
```

### Fireflies → monday.com

After a meeting:
```
1. Fireflies: fireflies_get_summary(transcriptId) → extract action items
2. For each action item: create_item on the relevant board
3. create_update on each item with meeting context
```

### monday.com → Gmail

For status change notifications:
```
1. get_board_items_by_name → find items with status "Done"
2. For each item, get the assignee's email
3. Gmail: create_draft(to=email, subject="Task Complete: [Item Name]", body=...)
```
