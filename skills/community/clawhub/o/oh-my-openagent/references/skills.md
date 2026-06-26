## Built-in skills

OmO ships with 6 built-in skills. Skills inject specialized knowledge into agents when loaded.

### playwright

- Domain: Browser automation via Playwright MCP
- Use for: Verification, browsing, web scraping, testing, screenshots
- MUST USE for any browser-related tasks
- Loaded with: `load_skills=["playwright"]`

### playwright-cli

- Domain: Playwright CLI operations
- Use for: Running Playwright test suites, generating tests

### agent-browser

- Domain: Advanced browser automation
- Use for: Complex multi-step browser workflows

### dev-browser

- Domain: Browser automation with persistent page state
- Use for: Navigate websites, fill forms, take screenshots, extract web data, test web apps
- Trigger phrases: "go to [url]", "click on", "fill out the form", "take a screenshot", "scrape"
- Loaded with: `load_skills=["dev-browser"]`

### git-master

- Domain: Git operations expertise
- MUST USE for ANY git operations
- Covers: Atomic commits, rebase/squash, history search (blame, bisect, log -S)
- Trigger phrases: "commit", "rebase", "squash", "who wrote", "when was X added"
- Strongly recommended: Use with `task(category='quick', load_skills=['git-master'])`
- Loaded with: `load_skills=["git-master"]`

### frontend-ui-ux

- Domain: Frontend design and development
- Use for: Crafting UI/UX even without design mockups
- Best paired with category: visual-engineering
- Loaded with: `load_skills=["frontend-ui-ux"]`

## Loading skills in task()

Skills are loaded via the `load_skills` parameter:

```
task(
  category="visual-engineering",
  load_skills=["frontend-ui-ux", "playwright"],
  prompt="...",
  run_in_background=false
)
```

Multiple skills can be loaded simultaneously.

## Custom skills

### Skill file format

Skills are SKILL.md files with optional YAML frontmatter:

```yaml
---
name: my-skill
description: What this skill does
mcp:
  server-name:
    command: npx
    args: ["-y", "mcp-server"]
---
# Skill prompt content here
```

### Skill load locations (priority order)

1. `.opencode/skills/*/SKILL.md` (project, OpenCode native)
2. `~/.config/opencode/skills/*/SKILL.md` (user, OpenCode native)
3. `.claude/skills/*/SKILL.md` (project, Claude Code compat)
4. `.agents/skills/*/SKILL.md` (project, Agents convention)
5. `~/.agents/skills/*/SKILL.md` (user, Agents convention)

### Skills with embedded MCPs

Skills can declare MCP servers in frontmatter. The MCP is started when the skill is loaded:

```yaml
---
name: my-mcp-skill
description: Skill with an MCP server
mcp:
  my-server:
    command: npx
    args: ["-y", "@my-org/mcp-server"]
    env:
      API_KEY: "${MY_API_KEY}"
---
```

Tools from the MCP become available via `skill_mcp` tool.
