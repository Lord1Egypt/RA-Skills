---
name: project-task-manager
description: "Project Task Manager: AI-powered task planning: generate hierarchical task trees from objectives, decompose tasks, track progress, visualize status. Persistent across sessions. Use when an agent needs project task manager, ai task generation, automatic task breakdown, project decomposition, objective to tasks, decompose, task, level of detail through AgentPMT-hosted remote tool calls. Discovery terms: project task manager, ai task generation, automatic task breakdown, project decomposition."
version: 1.0.0
homepage: https://www.agentpmt.com/marketplace/project-task-manager
compatibility: "Agent instructions for AgentPMT-hosted remote tool calls. Follow this skill body for supported account, wallet, and setup routes. No local command runtime is declared."
metadata: {"author":"agentpmt","openclaw":{"homepage":"https://www.agentpmt.com/marketplace/project-task-manager"}}
---
# Project Task Manager

## Freshness
Last updated: `2026-06-10`.

If the current date is more than 7 days after the last updated date, reinstall this skill from skills.sh or ClawHub before relying on endpoints, schemas, setup steps, or examples.

## What This Tool Does
AI Powered task generation and project management service that transforms high-level objectives into structured, hierarchical task breakdowns using large language model reasoning. The generate action accepts a project goal or objective along with optional context about available technologies and constraints, then produces a complete task tree with priorities, time estimates, dependencies between tasks, recommended tools, and measurable success criteria. The AI automatically selects the optimal prompting strategy based on objective complexity, using Chain of Thought reasoning for complex goals, ReAct methodology for technical implementations, or direct generation for straightforward requests. Task hierarchies can be configured from 1 to 4 levels deep depending on desired granularity. The decompose action breaks individual tasks into smaller actionable steps at basic, standard, or detailed levels without creating a persistent tree. Progress tracking supports updating task status through pending, in progress, completed, failed, and blocked states with percentage completion and notes. The status action provides real-time progress summaries including completed task counts, currently active work, blocked items, and estimated completion times. All generated task trees persist across sessions with full history available through the list action, enabling long-running project tracking and multi-session workflows.

## Product Instructions
### Project Task Manager

AI-powered task generation and project management tool. Break down objectives into structured, hierarchical task trees with dependencies, priorities, and time estimates. Track progress as you work through tasks.

#### Actions

##### generate

Create a hierarchical task breakdown from a high-level objective. An AI model analyzes your objective and produces a structured tree of tasks with dependencies, time estimates, and priorities.

**Required fields:**
- `action`: `"generate"`
- `objective` (string): What you want to accomplish. Be specific about the end goal. Max 2000 characters.

**Optional fields:**
- `context` (object): Technologies or constraints. Example: `{"tech": ["python", "postgresql"], "constraints": ["must use docker", "deploy to AWS"]}`
- `max_depth` (integer, 1-4): How many levels deep to break down tasks. 2 = simple, 3 = standard (default), 4 = very detailed.

**Example:**
```json
{
  "action": "generate",
  "objective": "Build a REST API for user management with JWT authentication",
  "context": {"tech": ["python", "fastapi"], "constraints": ["must use PostgreSQL"]},
  "max_depth": 3
}
```

**Response includes:** `tree_id` (save this for future actions), `task_ids` (list of all task IDs), `tasks` (full hierarchy), `total_tasks`, `estimated_total_time` (minutes), and `dependency_graph`.

---

##### update

Mark progress on a specific task within a task tree. Use this as you start, complete, or get blocked on tasks.

**Required fields:**
- `action`: `"update"`
- `tree_id` (string): The tree_id returned from the generate action.
- `task_id` (string): The specific task_id to update (from the generate response task_ids list).

**At least one of these is required:**
- `status` (string): New status. One of: `"pending"`, `"in_progress"`, `"completed"`, `"failed"`, `"blocked"`.
- `progress` (number, 0-100): Completion percentage. 0 = not started, 50 = halfway, 100 = done.
- `notes` (string): What happened or what you discovered. Max 500 characters.

**Example:**
```json
{
  "action": "update",
  "tree_id": "abc-123-def",
  "task_id": "task-456",
  "status": "in_progress",
  "progress": 25,
  "notes": "Started implementing the database schema"
}
```

**Response includes:** `updates_applied`, `new_progress` (overall tree progress), and `tasks_remaining`.

---

##### decompose

Break a single task description into smaller, actionable subtasks. This is a standalone operation that does not require an existing task tree.

**Required fields:**
- `action`: `"decompose"`
- `task` (string): The task to break into smaller steps. Be specific.

**Optional fields:**
- `level_of_detail` (string): How detailed the breakdown should be. One of: `"basic"` (3-5 steps), `"standard"` (5-10 steps, default), `"detailed"` (10-15 steps).

**Example:**
```json
{
  "action": "decompose",
  "task": "Implement user login with session management and password reset",
  "level_of_detail": "detailed"
}
```

**Response includes:** `subtasks` (list with name, description, estimated_time, dependencies, and tools for each), `total_subtasks`.

---

##### status

Check the current progress and status of a task tree.

**Required fields:**
- `action`: `"status"`
- `tree_id` (string): The tree_id returned from the generate action.

**Example:**
```json
{
  "action": "status",
  "tree_id": "abc-123-def"
}
```

**Response includes:** `overall_progress` (percentage), `completed_tasks`, `total_tasks`, `current_tasks` (in-progress tasks), `blocked_tasks`, `estimated_completion`, and `last_updated`.

---

##### list

Show all your task trees, sorted by most recently updated. Returns up to 50 trees.

**Required fields:**
- `action`: `"list"`

**Example:**
```json
{
  "action": "list"
}
```

**Response includes:** `trees` (list with tree_id, objective, task_count, progress, created_at, updated_at for each), `total`.

---

#### Common Workflows

##### Plan and Execute a Project
1. Use `generate` with your objective to create a task tree. Save the returned `tree_id` and `task_ids`.
2. Use `status` with the `tree_id` to review the plan.
3. Use `update` to mark tasks as `"in_progress"` when you start them.
4. Use `update` to mark tasks as `"completed"` when finished, or `"blocked"` / `"failed"` if issues arise.
5. Use `status` periodically to check overall progress.

##### Quick Task Breakdown
Use `decompose` when you just need to break a single task into steps without creating a full project tree. Good for ad-hoc planning.

##### Resume Previous Work
Use `list` to find your existing task trees, then `status` with the relevant `tree_id` to see where you left off.

#### Important Notes

- The `tree_id` returned from `generate` is required for all `update` and `status` calls. Always save it.
- Task IDs come from the `task_ids` array in the generate response. Use these exact IDs when calling `update`.
- Setting status to `"completed"` automatically sets progress to 100%.
- Time estimates are in minutes.
- The `decompose` action is independent and does not create or modify task trees.
- Task trees are stored per user and persist between sessions.

## When To Use
- Use this skill for `Project Task Manager` on AgentPMT.
- Use it when an agent needs this specific tool's behavior, schema, inputs, outputs, and invocation shape.
- Search and activation keywords: project task manager, ai task generation, automatic task breakdown, project decomposition, objective to tasks, decompose, task, level of detail.
- Supported action names: `decompose`, `generate`, `list`, `status`, `update`.

## Use Cases
- AI task generation
- automatic task breakdown
- project decomposition
- objective to tasks
- goal decomposition
- hierarchical task creation
- work breakdown structure
- WBS generation
- project planning automation
- sprint planning
- task prioritization
- dependency mapping
- task dependency graph
- time estimation
- effort estimation
- project scoping

## Categories And Industries
No categories or industry tags are published for this tool.

## Actions And Schema
Complete generated action schema: `./schema.md`.
Supported action count: `5`.
x402 availability: not enabled for this product.

- `decompose` (action slug: `decompose`): Break a single task description into smaller, actionable subtasks. Standalone operation that does not require an existing task tree. Price: `20` credits. Parameters: `level_of_detail`, `task`.
- `generate` (action slug: `generate`): Create a hierarchical task breakdown from a high-level objective. An AI model analyzes the objective and produces a structured tree of tasks with dependencies, time estimates, and priorities. Price: `20` credits. Parameters: `context`, `max_depth`, `objective`.
- `list` (action slug: `list`): Show all your task trees sorted by most recently updated. Returns up to 50 trees with their IDs, objectives, task counts, and progress. Price: `20` credits. Parameters: none.
- `status` (action slug: `status`): Check the current progress and status of a task tree. Returns overall progress, completed/remaining tasks, blocked items, and estimated completion time. Price: `20` credits. Parameters: `tree_id`.
- `update` (action slug: `update`): Mark progress on a specific task within a task tree. Update status, completion percentage, and add notes about what happened. Price: `20` credits. Parameters: `notes`, `progress`, `task_id`, `task_status`, `tree_id`.

## Live Schema And Examples
Use the compact schema above for ordinary calls. Before a new production integration, or whenever parameters, enum values, nested objects, outputs, or examples are unclear, fetch live details first.

- Exact schema: call `agentpmt-tool-search-and-execution` with `action: "get_schema"`, and `tool_id: "project-task-manager"`.
- Detailed examples: call `agentpmt-tool-search-and-execution` with `action: "get_instructions"` and `tool_id: "project-task-manager"`, or call this product with `action: "get_instructions"` when the product tool is already selected.
- Treat returned live schema and instructions as more specific than this generated summary.

MCP schema lookup through the main AgentPMT MCP server:

```json
{
  "method": "tools/call",
  "params": {
    "name": "AgentPMT-Tool-Search-and-Execution",
    "arguments": {
      "action": "get_schema",
      "tool_id": "project-task-manager"
    }
  }
}
```

For live examples, keep the same MCP tool and use these arguments:

```json
{
  "action": "get_instructions",
  "tool_id": "project-task-manager"
}
```

Authenticated AgentPMT REST schema lookup body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_schema",
    "tool_id": "project-task-manager"
  }
}
```

Authenticated AgentPMT REST live examples body:

```json
{
  "name": "agentpmt-tool-search-and-execution",
  "parameters": {
    "action": "get_instructions",
    "tool_id": "project-task-manager"
  }
}
```

## Call This Tool
Product slug: `project-task-manager`

Marketplace page: https://www.agentpmt.com/marketplace/project-task-manager

- AgentPMT account route: first use `../agentpmt-account-mcp-rest-api-setup` to connect the main MCP server or REST API for an Agent Group where this tool is enabled.
- x402 route: not enabled for this product.
- AgentPMT overview: use `../what-is-agentpmt` for marketplace, Agent Group, workflow, MCP, REST, and payment concepts.

If those setup skills are not installed beside this product skill, use the downloads below.

Core AgentPMT setup skills:
- What AgentPMT is: ../what-is-agentpmt
  - ClawHub page: https://clawhub.ai/agentpmt/what-is-agentpmt
  - OpenClaw install: `openclaw skills install what-is-agentpmt`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup
  - ClawHub page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup
  - OpenClaw install: `openclaw skills install agentpmt-account-mcp-rest-api-setup`
  - skills.sh install: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`

skills.sh install script:

```bash
npx skills add AgentPMT/agent-skills --skill what-is-agentpmt
npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup
```

MCP call shape after the main AgentPMT MCP server is connected:

```json
{
  "method": "tools/call",
  "params": {
    "name": "Project-Task-Manager",
    "arguments": {
      "action": "decompose",
      "level_of_detail": "basic",
      "task": "example task"
    }
  }
}
```

Use the exact tool name returned by `tools/list`; the name above is the expected readable form.

Authenticated AgentPMT REST call body:

```json
{
  "name": "project-task-manager",
  "parameters": {
    "action": "decompose",
    "level_of_detail": "basic",
    "task": "example task"
  }
}
```

Use the setup skill for the account connection details before making REST calls.

## Response Handling
- Treat the returned JSON as the source of truth for this tool call.
- If the response includes warnings or correction targets, apply them before retrying.
- If the response includes a `passed` or success-style boolean, use it as the workflow gate.
- If validation fails or the response shape is unclear, call `get_schema` or `get_instructions` before retrying.
- If `decompose` fails, preserve the request parameters and retry only after fixing schema, auth, or payment errors.

## Security
- Do not place account secrets, wallet private keys, mnemonics, signatures, or payment headers in prompts or logs.
- Keep tool inputs scoped to the minimum content needed for the task.
- Use the setup skills for credential handling; this product skill only defines product-specific behavior.

## AgentPMT Reference
- What AgentPMT is: ../what-is-agentpmt (ClawHub: `what-is-agentpmt`, page: https://clawhub.ai/agentpmt/what-is-agentpmt; skills.sh: `npx skills add AgentPMT/agent-skills --skill what-is-agentpmt`)
- AgentPMT account MCP/REST setup: ../agentpmt-account-mcp-rest-api-setup (ClawHub: `agentpmt-account-mcp-rest-api-setup`, page: https://clawhub.ai/agentpmt/agentpmt-account-mcp-rest-api-setup; skills.sh: `npx skills add AgentPMT/agent-skills --skill agentpmt-account-mcp-rest-api-setup`)
- Marketplace product: https://www.agentpmt.com/marketplace/project-task-manager
- AgentPMT main MCP server: https://api.agentpmt.com/mcp/
- AgentPMT REST invoke endpoint: https://api.agentpmt.com/products/purchase
