---
name: myaider-skill-importer
description: Import, create, and upgrade skills from MyAider MCP. Use this skill whenever the user wants to import their MyAider MCP skills into agent skills, or upgrade/update existing MyAider skills to the latest version. This skill checks if MyAider MCP is configured, retrieves available skills, presents them to the user for selection, and uses skill-creator to create or update each selected skill properly.
compatibility: []
---

# MyAider Skill Importer

## Purpose
Automate the process of importing skills from the MyAider MCP server into agent skills. This skill retrieves available skills, lets the user choose which ones to import, and creates proper skill files for each using existing skill-creator skill.

## MANDATORY WORKFLOW

### Step 0 — REQUIRED: Discover MyAider MCP Server Name and Check skill-creator Skill

**Note on naming convention:** MCP tool identifiers follow the format `mcp__<server-name>__<tool-name>`. The server name is whatever the user chose when configuring the MCP — it may not be `myaider`. Always discover the actual name rather than assuming it.

The MyAider MCP server exposes a distinctively named tool called `get_myaider_skills`. Because this name is unique to MyAider, searching for it avoids conflicts with other MCP servers.

#### Phase A — Discover the server name
Search your available tools for any tool whose name is `get_myaider_skills`. Use whatever tool-discovery mechanism your agent supports (e.g., listing available tools, searching by name). The full tool identifier will be in the form `mcp__<server-name>__get_myaider_skills`.

Extract the server name from the middle segment and store it as `{SERVER_NAME}`. Use `mcp__{SERVER_NAME}__get_myaider_skills` (and `mcp__{SERVER_NAME}__get_myaider_skill_updates`) for all subsequent calls.

#### Phase B — Branch on the result

- **Exactly 1 match found** → Extract `{SERVER_NAME}` from the tool identifier, proceed silently to Step 1.
- **0 matches found** → Inform the user that MyAider MCP needs to be set up first:

  > The MyAider MCP server doesn't appear to be configured. To use this skill, you need to set up the MyAider MCP server first.
  >
  > **Setup Instructions:**
  > 1. Go to https://www.myaider.ai/mcp
  > 2. Follow the instructions to configure the MyAider MCP server for your agent
  > 3. Once configured, come back and ask me to import your MyAider skills

  Do NOT proceed until the user confirms MyAider is configured.

- **2 or more matches found** → List all discovered server names and ask the user to confirm which one is their MyAider instance. Use the user's answer as `{SERVER_NAME}`.

Check if skill-creator skill is available; if not, ask the user to install skill-creator.

### Step 1 — REQUIRED: Get Available Skills
Call `mcp__{SERVER_NAME}__get_myaider_skills` (using the server name discovered in Step 0) with an empty object `{}` to retrieve all available skills from MyAider.

### Step 2 — REQUIRED: Present Skills to User
Present the list of skills to the user with their descriptions. Ask them to choose:
- "All" - import every skill
- Or specify which specific skills they want (by name)

Wait for user confirmation before proceeding.

### Step 3 — REQUIRED: For Each Selected Skill
For each skill the user wants to import:

1. **Extract the skill specification** from the getSkills result:
   - Skill name
   - Description (from the Usage Instructions or summary)
   - Usage Instructions (the main content)
   - **Tools with FULL usage details**: Extract each tool's name, description, and parameter schema from the "Tools" section in the getSkills result

2. **Create a properly formatted skill using skill-creator**:
   YOU MUST create the skill automatically instead of ask user to do it manually. YOU MUST use the Skill tool to invoke `skill-creator:skill-creator` with this template:

   ```
   Create a new skill called "[skill-name]" based on the following specification:

   ## Skill Name
   [skill-name]

   ## Description
   [description - make it comprehensive with triggering guidance]

   ## Metadata
   Add the following fields to the skill's YAML frontmatter (in addition to name and description):
   - source: myaider
   - updated_at: [ISO 8601 timestamp from the remote skill, e.g. 2026-03-06T12:00:00Z]

   ## Usage Instructions
   [full usage instructions from the myaider skill]

   ## Tools (MCP {SERVER_NAME})
   This skill uses the following MCP tools from {SERVER_NAME}. Include the full tool descriptions and parameter schemas BELOW to optimize token usage - the skill should NOT rely on the MCP protocol to get tool descriptions:

   ### [tool-name-1]
   [full tool description from get_myaider_skills result]

   **Parameters:**
   [parameter schema - include all parameters with their types, required/optional status, and descriptions]

   ### [tool-name-2]
   [full tool description from get_myaider_skills result]

   **Parameters:**
   [parameter schema - include all parameters with their types, required/optional status, and descriptions]
   ```

   **Critical**: The extracted tool descriptions and schemas must be included directly in the skill to avoid MCP protocol overhead. This optimizes token usage by enabling the skill to function without calling the MCP protocol for tool introspection.

3. **Confirm creation** to the user after each skill is created

### Step 4 — REQUIRED: Summarize
After all selected skills are created, provide a summary:
- List of successfully created skills
- File locations
- Any skills that failed (if any)

---

## Upgrade Workflow

Trigger this workflow when the user asks to **upgrade**, **update**, or **sync** their MyAider skills.

### Upgrade Step 0 — Discover server name
Same as the main Step 0. Search for `get_myaider_skills` to find `{SERVER_NAME}`. If MCP is not configured, show setup instructions and stop.

### Upgrade Step 1 — Fetch remote update info
Call `mcp__{SERVER_NAME}__get_myaider_skill_updates` with an empty object `{}`. This returns the latest skill definitions with their `updated_at` timestamps.

### Upgrade Step 2 — Read local MyAider skills
Find all locally installed skills that have `source: myaider` in their YAML frontmatter. For each, read the `updated_at` value. Build a map of `skill-name → local updated_at`.

### Upgrade Step 3 — Compare and classify
For each skill returned in Upgrade Step 1:
- **Remote `updated_at` is newer than local** → mark for **upgrade**
- **Skill does not exist locally** → mark for **new install**
- **Remote `updated_at` is same or older** → skip (already up to date)

Present the classification to the user (what will be upgraded, what is new, what is already current) and ask for confirmation before proceeding.

### Upgrade Step 4 — Upgrade outdated skills
For each skill marked for **upgrade**, invoke `skill-creator:skill-creator` with the full updated specification (same template as the main Step 3, including refreshed `updated_at` and tool schemas). skill-creator will overwrite the existing skill file.

### Upgrade Step 5 — Install new skills
For each skill marked for **new install**, invoke `skill-creator:skill-creator` exactly as in the main Step 3 (import workflow).

### Upgrade Step 6 — Summarize
Provide a final report:
- Skills upgraded (name + old → new `updated_at`)
- New skills installed
- Skills already up to date (skipped)
- Any failures

---

## Important Constraints
- Always discover the MCP server name by searching for `get_myaider_skills` first (Step 0) — do NOT hardcode `myaider` or any other name
- Always call `get_myaider_skills` after confirming MCP is configured — do NOT guess what skills are available
- **Always extract and include FULL tool descriptions and schemas** from `get_myaider_skills` — this is critical to optimize token usage. The created skill should work without needing MCP protocol tool introspection
- Use the discovered `{SERVER_NAME}` consistently for all MCP tool calls and in generated skill files
- Always include `source: myaider` and `updated_at` in the YAML frontmatter of every created or upgraded skill — these fields are required for the upgrade workflow
- Always wait for user confirmation before creating or upgrading skills
- Create/upgrade skills one at a time using skill-creator
- Keep the skill-creator conversation focused on each skill creation

## Example Usage
- "Import my MyAider skills"
- "Create skills from myaider"
- "Set up the skills from my MyAider MCP"
- "Upgrade my MyAider skills"
- "Update my MyAider skills to the latest version"
- "Sync my MyAider skills"
