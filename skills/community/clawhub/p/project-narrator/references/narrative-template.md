# [Project Name]: The Complete Narrative

*Last updated: YYYY-MM-DD*

<!-- 
  This is your project's single source of truth.
  If everything disappeared except this file, could someone rebuild the project?
  If yes, this narrative is complete.
-->

## What Is This Project?

<!-- 2-3 sentences. What does it do? Who is it for? Why does it exist? -->

**Repository:** <!-- git remote URL -->
**Status:** <!-- production / staging / alpha / archived -->
**Primary language:** <!-- e.g., TypeScript -->
**Team:** <!-- who works on this? -->

## Current Status

<!-- 
  What's the health of the project right now?
  - Is it deployed and running?
  - Any ongoing incidents?
  - Key metrics (uptime, users, request volume)?
  - What's actively being worked on?
-->

## Architecture

<!--
  High-level architecture. Think: what would a new developer need to understand
  on day one? Components, data flow, external services.
  
  A simple ASCII diagram often helps:
  
  [Client] → [API Gateway] → [Worker] → [Database]
                                ↓
                          [Queue] → [Processor]
-->

**Stack:** <!-- e.g., Next.js + Hono + D1 + Cloudflare Workers -->

**Key components:**
- <!-- Component 1: what it does -->
- <!-- Component 2: what it does -->
- <!-- Component 3: what it does -->

**Data flow:**
<!-- How does data move through the system? -->

## Infrastructure

**Hosting:** <!-- Where does this run? -->
**Database:** <!-- What database(s)? Where hosted? -->
**CDN/Assets:** <!-- Static hosting, CDN, image pipeline? -->
**DNS:** <!-- Registrar, nameservers -->
**Monitoring:** <!-- What watches the system? Alerts? -->

**Services & accounts:**
| Service | Purpose | Account/ID |
|---------|---------|------------|
| <!-- e.g., Cloudflare --> | <!-- Workers, DNS --> | <!-- account ID --> |

## Pipeline / Workflow

**Local development:**
```bash
# How to run locally
```

**Testing:**
```bash
# How to run tests
```

**Deployment:**
<!-- 
  Step-by-step: how does code get to production?
  - Push to main? PR merge? Manual deploy command?
  - CI/CD pipeline details
  - Any manual steps?
-->

**Rollback:**
<!-- How do you undo a bad deploy? -->

## API Routes

<!-- List all API endpoints with method, path, and brief description -->

| Method | Path | Description |
|--------|------|-------------|
| <!-- GET --> | <!-- /api/health --> | <!-- Health check --> |

## Scripts

<!-- Every script in the project: what it does, when to use it, any gotchas -->

| Script | Purpose | Usage |
|--------|---------|-------|
| <!-- scripts/deploy.sh --> | <!-- Deploy to prod --> | <!-- `./scripts/deploy.sh` --> |

**package.json scripts:**
- <!-- `npm run dev` — Start dev server -->
- <!-- `npm run build` — Production build -->

## Configuration

**Environment variables:**
<!-- List every env var, what it controls, where to get the value -->

| Variable | Purpose | Where stored |
|----------|---------|-------------|
| <!-- DATABASE_URL --> | <!-- D1 connection --> | <!-- .env / wrangler.toml --> |

**Config files:**
- <!-- wrangler.toml — Cloudflare Workers config -->
- <!-- tsconfig.json — TypeScript compiler options -->

## Security Model

<!-- 
  This section matters more than you think.
  - How is authentication handled?
  - What's the authorization model?
  - Where are secrets stored?
  - What's the trust boundary?
  - Any known security concerns?
-->

## Known Issues

<!-- 
  BE HONEST HERE. This section prevents repeating mistakes.
  
  Format:
  - **Issue**: Description
    - **Impact**: What breaks or degrades?
    - **Workaround**: How to handle it now
    - **Fix**: What needs to happen (if known)
-->

## Design Principles

<!-- 
  THIS IS THE MOST IMPORTANT SECTION.
  
  Architecture can be reverse-engineered from code.
  Design principles cannot.
  
  For each major decision, document:
  1. What was decided
  2. What alternatives were considered
  3. Why this option won
  4. What tradeoffs were accepted
  
  Examples:
  - "We chose SQLite/D1 over Postgres because we deploy to edge workers"
  - "We process feeds sequentially, not in parallel, because rate limits matter more than speed"
  - "We store raw API responses alongside processed data so we can reprocess without re-fetching"
-->

## Changelog

<!-- 
  Not git log — significant changes with context.
  Date, what changed, why, any impact.
-->

| Date | Change | Impact |
|------|--------|--------|
| <!-- YYYY-MM-DD --> | <!-- What changed --> | <!-- What it affected --> |

## Key Credentials & IDs

<!-- 
  ⚠️ NO ACTUAL SECRETS. Reference where they're stored.
  
  Format: What — Where stored
-->

| Credential | Storage Location |
|-----------|-----------------|
| <!-- API key for X --> | <!-- ~/.openclaw/secrets/x.key --> |

## File Map

<!-- 
  Top-level directory structure with annotations.
  Update when significant files are added/removed.
-->

```
project-root/
  src/              # Application source
  scripts/          # Utility scripts
  tests/            # Test files
  .github/          # CI/CD workflows
  package.json      # Dependencies and scripts
  wrangler.toml     # Cloudflare config
```
