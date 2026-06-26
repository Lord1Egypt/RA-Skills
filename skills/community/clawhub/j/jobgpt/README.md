# JobGPT Skills

Agent skills for [JobGPT](https://6figr.com/jobgpt-ai) — job search automation, auto apply, resume generation, application tracking, salary intelligence, and recruiter outreach.

## Install

**Claude Code**
```bash
claude skill add --url https://github.com/6figr-com/skills
```

**Vercel Skills.sh**
```bash
npx skills add 6figr-com/skills
```

**OpenClaw**
```bash
clawhub install jobgpt
```

**Manual**
Copy `SKILL.md` to your agent's skills directory (e.g., `~/.claude/skills/jobgpt/SKILL.md`).

## Requirements

- A [JobGPT](https://6figr.com/jobgpt-ai) account
- API key from Account → MCP Integrations
- The `jobgpt-mcp-server` MCP server configured in your AI tool

```bash
npx jobgpt-mcp-server
```

## What You Can Do

Ask your AI assistant things like:

- "Find remote senior React jobs paying over $150k"
- "Auto-apply to the top 5 matches from my job hunt"
- "Generate a tailored resume for this Google application"
- "Apply to this job for me - https://boards.greenhouse.io/company/jobs/12345"
- "Show my application stats for the last 7 days"
- "Find recruiters for this job and draft an outreach email"

34 tools covering job search, applications, resumes, outreach, salary intelligence, and more.

## Links

- [JobGPT](https://6figr.com/jobgpt-ai) — Main platform
- [MCP Server](https://github.com/6figr-com/jobgpt-mcp-server) — The MCP server this skill uses
- [npm](https://www.npmjs.com/package/jobgpt-mcp-server) — npm package
