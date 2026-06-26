# Mission Control Publish Instruction Template

Use this template for publish-ready instruction documents (non-blog).

```md
# Mission Control: Setup ClawDash Pro Dashboard After Purchase

## Tags

- mission control
- agent OS
- openclaw dashboard
- AI agents
- admin dashboards

## Who This Is For

Customers who purchased Mission Control and need to configure the ClawDash Pro dashboard.

## Integration Goal

Connect Open Cloud "brain/data" to the purchased pre-designed Next.js UI while keeping the current design unchanged.

## What You Need Before Starting

- Node.js 18+
- API key(s)
- Workspace/organization ID
- Mission Control package from ClawDash Pro

## Step 1: Open Mission Control Project

```bash
cd mission-control
```

## Step 2: Install Dependencies

```bash
npm install
```

## Step 3: Configure Credentials

```bash
cp .env.example .env.local
```

Add your Open Cloud values in `.env.local`:
- API key
- Workspace/organization ID
- Base URL

## Step 4: Run Mission Control

```bash
npm run dev
```

## Step 5: Send This Prompt to Open Cloud

```text
Connect Open Cloud to this existing Mission Control (ClawDash Pro) Next.js application.
Design lock requirement: do not redesign, restyle, rename, or restructure the current UI.
Keep all existing pages/components/layout as-is.

Integrate data wiring for these domains only:
1) Overview metrics (status, memory usage, health KPIs)
2) Agents (active agents, states, last activity)
3) Skills and contracts (capabilities and assigned contracts/policies)
4) Tasks command view (queued/running/completed/failed with history)
5) Token usage (per agent and total)
6) Documents (available documents and indexing state)

Use adapter/service layer changes behind existing components so frontend visuals remain unchanged.
Return a change summary listing wired endpoints, env vars, and routes touched.
```

## Step 6: Verify Connection

1. Agent status loads.
2. Task/activity data appears.
3. No auth/network errors in logs.
4. Token usage values update.
5. Documents list/indexing state is visible.
6. UI design remained unchanged.

## Troubleshooting

- Missing data in one section:
  - Verify endpoint and workspace ID mapping for that domain.
- UI changed unexpectedly:
  - Re-run with explicit design lock requirement and request backend-only changes.
- Auth failures:
  - Re-check API key and base URL in `.env.local`.

## Publish / Go-Live Checklist

- Overview, Agents, Skills/Contracts, Tasks, Token Usage, Documents all show data.
- No UI redesign or component structure changes were introduced.
- Environment variables documented for production deploy.
- User can repeat setup from this guide without extra context.

## Other Decks

- Executive Deck: KPI-focused view for leadership.
- Operations Deck: agent throughput, failures, queue depth.
- Admin Deck: users, roles, workspace settings, audit trail.

## Links

- Product: https://clawdash.pro
- Pricing: https://clawdash.pro/pricing
```
