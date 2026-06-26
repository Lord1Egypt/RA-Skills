---
name: find-skills
description: Discover and install skills from the open agent skills ecosystem. Use when: (1) user asks "how do I do X" where X might have an existing skill, (2) user says "find a skill for X" or "is there a skill for X", (3) user asks "can you do X" where X is a specialized capability, (4) user wants to extend agent capabilities, (5) user wants to search for tools, templates, or workflows, (6) user mentions they wish they had help with a specific domain (design, testing, deployment, etc.).
---

# Find Skills

Discover and install skills from the open agent skills ecosystem using the Skills CLI (`npx skills`).

## Skills CLI Commands

```bash
npx skills find [query]    # Search for skills interactively or by keyword
npx skills add <package>   # Install a skill from GitHub or other sources
npx skills check           # Check for skill updates
npx skills update          # Update all installed skills
```

Browse skills at: https://skills.sh/

## How to Help Users Find Skills

### Step 1: Understand What They Need

Identify:
- The domain (e.g., React, testing, design, deployment)
- The specific task (e.g., writing tests, creating animations, reviewing PRs)
- Whether this is a common enough task that a skill likely exists

### Step 2: Search for Skills

```bash
npx skills find [query]
```

Examples:
- "how do I make my React app faster?" → `npx skills find react performance`
- "can you help me with PR reviews?" → `npx skills find pr review`
- "I need to create a changelog" → `npx skills find changelog`

Results format:
```
Install with npx skills add <owner/repo@skill>

vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### Step 3: Present Options to the User

Include:
- The skill name and what it does
- The install command
- A link to learn more at skills.sh

Example:
```
I found a skill that might help! The "vercel-react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.

To install it:
npx skills add vercel-labs/agent-skills@vercel-react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### Step 4: Offer to Install

Install with global flag and auto-confirm:
```bash
npx skills add <owner/repo@skill> -g -y
```

## Common Skill Categories

| Category | Example Queries |
|----------|----------------|
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing | testing, jest, playwright, e2e |
| DevOps | deploy, docker, kubernetes, ci-cd |
| Documentation | docs, readme, changelog, api-docs |
| Code Quality | review, lint, refactor, best-practices |
| Design | ui, ux, design-system, accessibility |
| Productivity | workflow, automation, git |

## Tips for Effective Searches

- Use specific keywords: "react testing" is better than just "testing"
- Try alternative terms: If "deploy" doesn't work, try "deployment" or "ci-cd"
- Check popular sources: `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`

## When No Skills Are Found

If no relevant skills exist:
1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using general capabilities
3. Suggest creating a custom skill with `npx skills init`

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```
