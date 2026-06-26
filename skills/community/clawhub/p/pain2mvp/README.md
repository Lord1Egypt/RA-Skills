# pain2mvp

OpenClaw skill for turning public user pain points into ranked opportunities and persisted PRDs.

## Install

1. Install this skill via ClawHub.
2. Navigate to your local skills directory for this skill.
3. Run `npm install` to install local dependencies.
4. Set `TIDB_DATABASE_URL` to your TiDB Cloud Zero database URL with `?sslaccept=strict`.
5. Run `npm run bootstrap:tidb` to initialize tables.

## Use

- Discovery mode: ask for top pain points by user group, idea, or existing solution.
- Example: "What are the top pain points for in-house IP counsel?"
- Example: "What are OpenClaw users frustrated by?" or "What are Harvey users complaining about?"
- PRD mode: ask for a PRD from a persisted opportunity id or latest high-confidence result.
- Example: "Generate a PRD from opportunity `opp_20260328_01`."

See `SKILL.md` for runtime flow and `references/contracts.md` for the command contract.
