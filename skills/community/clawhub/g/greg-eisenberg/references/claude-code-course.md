# CLAUDE CODE FULL COURSE 4 HOURS: Build & Sell (2026)

**Video:** https://www.youtube.com/watch?v=QoQBzR1NIqI
**Host:** Greg Eisenberg
**Length:** ~4 hours

## Who This Is For

Non-technical people who want to use Claude Code to build and sell products. Greg runs a $4M+/year profit business using Claude Code daily and teaches 2000+ people how to use it.

## Course Structure

### Part 1: Setup & Basics
- Download and install Claude Code
- IDEs: walks through 3 main ones (VS Code, Cursor, Antigravity)
- Antigravity recommended as the best GUI for Claude Code
- Setting up the CLAUDE.md (project brain file)

### Part 2: CLAUDE.md Deep Dive
- CLAUDE.md is injected as a system prompt before every conversation turn
- Pattern: User → Model → User → Model (CLAUDE.md sits before all of this)
- Keep it concise — every token costs money and dilutes focus
- Structure: project overview, tech stack, coding conventions, key files
- "Mega prompt" approach: front-load context so Claude needs fewer follow-ups

### Part 3: Building a Web App
- Practical build of a live web app
- Emphasis on learning by doing
- Covers deployment to make it live on the internet

### Part 4: Advanced Claude Code Features
- **Claude directory** and subagents folder
- **Plan mode** — Claude creates an implementation plan before coding
- **Dangerously skip permissions mode** — bypasses confirmation prompts (use with caution)
- **Context management** — the #1 skill for effective Claude Code usage

### Part 5: Token Usage & Context Management
- Auto-compaction: oldest messages compressed into high-density summaries
- RAG (retrieval augmented generation) strategies
- Continuously compress CLAUDE.md
- Tell Claude to write concisely but enable extended thinking
- Check Twitter/X for latest community strategies on reducing token usage

### Part 6: Design & Frontend
- 3 major approaches to designing sites with Claude Code
- Building award-winning designs (Greg claims to have built 15 high-quality sites in one project)
- Deployment strategies

### Part 7: Agent Teams (Parallelization)
- Multiple agents working simultaneously on different tasks
- Example: 3 agents each create fundamentally different website designs, then compare
- Example: agents act as code reviewers and debaters on an open-source codebase
- Parent agent (Opus 4.6) delegates to child agents
- Terminal UX better than GUI for agent teams currently
- Fast mode for quicker iteration

### Part 8: MCP Servers & Integrations
- Model Context Protocol for connecting Claude to external tools
- Context7 for up-to-date documentation
- Various MCP servers for different services

### Part 9: Business & Selling
- How to package and sell what you build
- Greg's approach to using Claude Code commercially
- Scaling with Claude Code as leverage

## Key Insights

1. **CLAUDE.md is everything** — treat it like onboarding a new employee. The better the brief, the better the output
2. **Context management is the real skill** — not prompting, not coding, but managing what Claude knows and when
3. **Agent teams are the next level** — parallel agents debating and reviewing each other's work produces better results than single-agent workflows
4. **You don't need to be technical** — the course is designed for non-coders who want to build products
5. **Auto-compaction** — Anthropic compresses old messages automatically, which saves tokens and improves quality (against their own revenue interest)
6. **Fast mode** — toggle for quicker Claude Code responses during iterative work
7. **Antigravity** — Greg's recommended IDE/GUI for Claude Code

## Relevance to Finn's Setup
- Agent teams could be useful for parallelizing tasks on the Mac Mini
- CLAUDE.md best practices apply directly to OpenClaw workspace files (agents.md, soul.md)
- Context management strategies apply to keeping OpenClaw token costs down with Haiku
- MCP server patterns can inform the Gmail/Google Workspace setup
