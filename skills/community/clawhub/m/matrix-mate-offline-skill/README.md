# Matrix Mate - ITA Matrix Flight Search and Parse Tool

Matrix Mate Offline is an offline-first Codex skill for turning ITA Matrix itinerary links into traveler-safe itinerary summaries, fare rule audits, discrepancy reviews, and export-ready trip output. It pairs a local Matrix Mate app with a local MCP runtime so agents can parse Matrix links, inspect trip details, export traveler and agent summaries, and use browser automation to search ITA Matrix before handing the resulting itinerary back into Matrix Mate for verification.

## Who this skill is for

This skill is for travelers, points enthusiasts, premium-cabin deal hunters, and travel agents who want an ITA Matrix parsing workflow that stays grounded in a local tool instead of guessing from screenshots or unverified search pages.

It is especially useful when you want to:

- parse an existing ITA Matrix itinerary link into structured trip data
- audit fare rules before sharing a trip with a traveler or agent
- compare verified itinerary details with fare-rule caveats
- export traveler-safe and agent-facing summaries
- search ITA Matrix in an agent browser, then pass the resulting itinerary into Matrix Mate

## What Matrix Mate Offline does

- Parses `matrix.itasoftware.com/itinerary?search=...` links through the local Matrix Mate app
- Supports manual JSON plus rules fallback when Matrix cannot verify the itinerary automatically
- Returns verified, needs-review, or draft-grade parse states with discrepancy counts
- Produces traveler-safe itinerary packages, fare breakdowns, and future booking intent payloads
- Gives agents a browser-assisted Matrix workflow without pretending to book tickets or bypass site protections

## Install on skills.sh

Use a public mirror of this bundle and install it with the standard skills.sh flow:

```bash
npx skills add <owner>/matrix-mate-offline-skill
```

After install, run `npm install` in the bundle root, then print the local MCP config:

```bash
node scripts/print-offline-mcp-config.mjs
```

## Install on ClawHub

Package the same bundle directory for ClawHub/OpenClaw publication.

Recommended release shape:

1. Publish the bundle root with semver tags.
2. Keep the runtime local and read-focused.
3. Document that the user must run a local Matrix Mate app before invoking the skill.
4. Do not claim a hosted Matrix Mate MCP endpoint unless one actually exists.

## Local MCP setup

1. Start Matrix Mate locally.
2. Install dependencies in the skill bundle root.
3. Start the MCP runtime:

```bash
node scripts/run-offline-mcp.mjs
```

4. Or print a ready-to-paste MCP client config:

```bash
node scripts/print-offline-mcp-config.mjs
```

## Browser-assisted ITA Matrix workflow

Matrix Mate Offline is designed for a search-then-parse loop:

1. Gather the user’s route, date, cabin, and passenger intent.
2. Use an agent browser to run the ITA Matrix search.
3. Capture the resulting itinerary or share link.
4. Pass that link into Matrix Mate with `parse_matrix_link`.
5. Use the verified trip output for summaries, audits, and exports.

If the Matrix site only yields a search page, expired result, or incomplete verification surface, the skill falls back to manual JSON plus fare rules input instead of fabricating certainty.

## Trust boundary and limitations

See `SECURITY.md` for reviewer-focused controls, risks, and verification checks.

- This is an offline-first local skill, not a hosted booking product.
- Browser automation is read/search only.
- No login handling, payment flows, or CAPTCHA bypass promises are part of this skill.
- Matrix Mate remains the trusted parse engine for itinerary verification and discrepancy reporting.
- Poke support is recipe-ready, not live-publish-ready, until a public Matrix Mate MCP URL exists.

## FAQ

### Can this skill search ITA Matrix for me?

Yes. The intended workflow is to use browser automation to search ITA Matrix, then feed the resulting itinerary URL back into Matrix Mate for parsing.

### Can this skill verify fare rules from an ITA Matrix link?

Yes, when Matrix Mate can fetch enough booking details and fare rules from the itinerary link. If not, the skill falls back to manual JSON plus rules input.

### Can this skill book tickets or complete checkout?

No. This skill is for parsing, auditing, and export-oriented trip review only.

### Is this a hosted MCP server?

No. This bundle is designed for local runtime use. A future public MCP endpoint can be added later for hosted Poke publication.

## Keywords

ITA Matrix parser, fare rules audit, ITA Matrix itinerary link parser, traveler-safe itinerary summary, premium cabin fare workflow, browser-assisted Matrix search, local MCP travel skill, Matrix Mate offline skill
