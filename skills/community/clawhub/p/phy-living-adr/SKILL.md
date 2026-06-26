---
name: Living ADR
description: Living Architecture Decision Records — automatically draft, number, and update ADRs from git diffs, PR descriptions, or plain-English decisions. Detects architectural signals in code changes (new database tables, new auth methods, new external integrations, framework changes) and drafts a pre-filled ADR in the RFC 822 / Nygard format. Also marks existing ADRs as "Superseded" when new decisions replace them. Outputs to docs/adr/ with sequential ADR-NNN numbering. Zero external API — works entirely from your codebase and git history. Triggers on "write ADR", "document this decision", "architecture decision", "new ADR", "living adr", "/living-adr".
license: Apache-2.0
homepage: https://canlah.ai
metadata:
  author: Canlah AI
  version: "1.0.3"
  tags:
    - adr
    - architecture
    - documentation
    - decision-records
    - git
    - team
    - developer-tools
    - documentation-as-code
---

# Living ADR

Keep your architecture decisions documented and alive. Paste a git diff, a PR description, or just describe what you decided — and get a formatted, numbered ADR file ready to commit. When a new decision supersedes an old one, the old ADR gets automatically updated.

**No templates to fill in. No formats to remember. Works from diffs, PRs, or plain English.**

---

## Trigger Phrases

- "write ADR", "create ADR", "new architecture decision"
- "document this decision", "we decided to use X instead of Y"
- "architecture decision record", "why did we choose X"
- "update ADR", "this supersedes ADR-012"
- "/living-adr"

---

## How to Provide Input

```
# Option 1: Describe the decision in plain English
/living-adr We're switching from REST to GraphQL for the user-facing API because
REST was causing over-fetching and the mobile team needed flexible queries.

# Option 2: Paste a git diff
/living-adr
[paste git diff here]

# Option 3: Paste a PR title + description
/living-adr
PR: "Replace JWT with session cookies for auth"
Description: JWTs were causing issues with token revocation...

# Option 4: Point to current changes
/living-adr --from-diff HEAD~1
/living-adr --from-pr 142

# Option 5: Explicitly supersede an existing ADR
/living-adr --supersedes ADR-008
We're moving from PostgreSQL to CockroachDB for global distribution...
```

---

## Step 1: Discover Existing ADRs

Before creating a new ADR, inventory what already exists:

```bash
# Find the ADR directory (check common locations)
find . -type d -name "adr" 2>/dev/null | grep -v node_modules | head -5
find . -type d -name "decisions" 2>/dev/null | grep -v node_modules | head -5
find . -path "*/docs/adr*" -type f 2>/dev/null | grep -v node_modules | head -20

# If no ADR directory exists, create it
mkdir -p docs/adr
```

Parse all existing ADRs to build a registry:

```bash
# List all ADRs with their numbers, titles, and status
ls -1 docs/adr/*.md 2>/dev/null | while read f; do
  num=$(grep -m1 "^# ADR-" "$f" 2>/dev/null | grep -oE "ADR-[0-9]+" | head -1)
  title=$(grep -m1 "^# " "$f" 2>/dev/null | sed 's/^# //')
  status=$(grep -i "^## Status" -A1 "$f" 2>/dev/null | tail -1 | tr -d ' ')
  echo "$f | $num | $status | $title"
done
```

**Registry output example:**
```
docs/adr/ADR-001-use-postgresql.md | ADR-001 | Accepted | Use PostgreSQL as primary database
docs/adr/ADR-005-jwt-auth.md | ADR-005 | Accepted | Use JWT for API authentication
docs/adr/ADR-010-monorepo.md | ADR-010 | Deprecated | Use monorepo structure
```

Determine the next ADR number: `max(existing numbers) + 1`.

---

## Step 2: Detect Architectural Signals (from diff or description)

When input is a git diff, scan for these architectural change patterns:

### Database / Schema Changes
```bash
# New migration files = new DB decision
git diff --name-only HEAD~1 | grep -iE "migration|schema|alembic|flyway|prisma/migrations"

# New table, DROP TABLE, ALTER TABLE = schema evolution
git diff HEAD~1 | grep -iE "^+.*(CREATE TABLE|DROP TABLE|ADD COLUMN|ALTER TABLE)" | head -10
```

### New External Integrations
```bash
# New dependencies in package.json / requirements.txt / go.mod
git diff HEAD~1 -- package.json requirements.txt go.mod Cargo.toml | grep "^+" | grep -v "^+++" | head -20

# New import of external SDK/client
git diff HEAD~1 | grep "^+.*import" | grep -iE "(stripe|twilio|sendgrid|aws|gcp|openai|anthropic)" | head -10
```

### Auth / Security Pattern Changes
```bash
git diff HEAD~1 | grep -iE "(jwt|session|oauth|saml|ldap|auth0|cognito|firebase.auth)" | grep "^+" | head -10
```

### Framework / Architecture Pattern Changes
```bash
# New config files suggesting framework adoption
git diff --name-only HEAD~1 | grep -iE "(next\.config|vite\.config|webpack\.config|docker-compose|k8s|helm/)"

# New top-level directories suggesting architectural restructure
git diff --name-only HEAD~1 | grep "^[^/]*/$" | head -10
```

### From the signals detected, classify the decision type:

| Signal | Decision Category |
|--------|------------------|
| New DB migration | Data Architecture |
| New external package (payments, email, auth) | External Integration |
| JWT → sessions, OAuth2 → SAML | Authentication & Authorization |
| REST → GraphQL, new API version | API Design |
| New Dockerfile, k8s configs | Infrastructure & Deployment |
| Monorepo restructure, new package | Repository Structure |
| New caching layer (Redis, Memcached) | Performance Architecture |
| New message queue (Kafka, RabbitMQ) | Async Architecture |

---

## Step 3: Check for Supersession

Before creating a new ADR, check if it contradicts an existing one:

```bash
# Extract keywords from the new decision
# Then search existing ADRs for related content
grep -rl "PostgreSQL\|database\|Postgres" docs/adr/ 2>/dev/null
grep -rl "JWT\|auth\|token" docs/adr/ 2>/dev/null
```

If a related existing ADR is found:
- **If the new decision replaces it** → mark existing as `Superseded by ADR-NNN`
- **If the new decision extends it** → reference it in the new ADR's "Context" section
- **If they coexist** → note both in "Related ADRs"

---

## Step 4: Draft the ADR

Use the Nygard format (the industry standard, used by ThoughtWorks, GitHub, Spotify):

```markdown
# ADR-[NNN]: [Short imperative title — what was decided]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded by [ADR-NNN]
**Deciders:** [team/person who made this decision]
**Tags:** [database, auth, api, infrastructure, ...]

---

## Context

[What situation forced this decision? What constraints existed?
What problem were we trying to solve? 2-4 sentences max.]

## Decision

[The actual decision, stated clearly. "We will use X." or "We decided to Y."
One paragraph. No hedging.]

## Consequences

### Positive
- [benefit 1]
- [benefit 2]

### Negative / Trade-offs
- [drawback or cost 1]
- [known limitation]

### Neutral
- [things that are neither good nor bad, just different]

## Alternatives Considered

| Option | Why Rejected |
|--------|-------------|
| [Alt 1] | [reason] |
| [Alt 2] | [reason] |

## Related ADRs

- [ADR-NNN]: [relationship] — e.g., "Supersedes ADR-005 (JWT Auth)"
- [ADR-NNN]: [relationship] — e.g., "Related to ADR-002 (Database Choice)"

## References

- [Link to relevant docs, RFCs, blog posts, or issue tracker tickets]
```

---

## Step 5: Write the File

```bash
# Determine next ADR number
NEXT_NUM=$(ls docs/adr/ADR-*.md 2>/dev/null | grep -oE "ADR-[0-9]+" | grep -oE "[0-9]+" | sort -n | tail -1)
NEXT_NUM=$(printf "%03d" $((${NEXT_NUM:-0} + 1)))

# Slugify the title
SLUG=$(echo "$TITLE" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd '[:alnum:]-')

# Write the file
cat > "docs/adr/ADR-${NEXT_NUM}-${SLUG}.md" << 'EOF'
[generated ADR content]
EOF

echo "Created: docs/adr/ADR-${NEXT_NUM}-${SLUG}.md"
```

### If superseding an existing ADR, update it:

```bash
# Add supersession notice to the old ADR
OLD_ADR="docs/adr/ADR-005-jwt-auth.md"
sed -i '' "s/^**Status:** Accepted/**Status:** Superseded by ADR-${NEXT_NUM}/" "$OLD_ADR"
echo "" >> "$OLD_ADR"
echo "> **Superseded:** This decision was replaced by [ADR-${NEXT_NUM}](ADR-${NEXT_NUM}-${SLUG}.md) on $(date +%Y-%m-%d)." >> "$OLD_ADR"
```

---

## Output Format

After creating the ADR, report:

```markdown
## ADR Created: ADR-NNN

**File:** `docs/adr/ADR-NNN-use-graphql-for-user-api.md`
**Status:** Proposed (ready for team review)

### What was detected
- Signal: `src/api/graphql/` directory created, `graphql` added to package.json
- Category: API Design
- Supersedes: ADR-003 (REST API Design) — that ADR has been marked "Superseded"

### ADR Summary
- **Decision:** Switch user-facing API from REST to GraphQL
- **Why:** Mobile team reported 3x over-fetching; query flexibility needed
- **Trade-offs:** GraphQL learning curve; N+1 query risk without DataLoader

### Next Steps
1. Review draft: `docs/adr/ADR-NNN-use-graphql-for-user-api.md`
2. Change status from `Proposed` → `Accepted` when team agrees
3. Commit both files: the new ADR + updated ADR-003

### Git command
```bash
git add docs/adr/ADR-NNN-use-graphql-for-user-api.md docs/adr/ADR-003-rest-api-design.md
git commit -m "docs(adr): ADR-NNN — use GraphQL for user-facing API"
```
```

---

## ADR Status Lifecycle

```
Proposed → Accepted → Deprecated
                    ↘ Superseded by ADR-NNN
```

| Status | Meaning |
|--------|---------|
| `Proposed` | Draft, under discussion |
| `Accepted` | Team agreed, this is the current approach |
| `Deprecated` | No longer relevant, not replaced by anything specific |
| `Superseded by ADR-NNN` | Replaced by a newer decision |

---

## ADR Index Generation

After creating or updating ADRs, optionally regenerate the index:

```bash
# Generate docs/adr/README.md index
echo "# Architecture Decision Records" > docs/adr/README.md
echo "" >> docs/adr/README.md
echo "| ADR | Title | Status | Date |" >> docs/adr/README.md
echo "|-----|-------|--------|------|" >> docs/adr/README.md

ls -1 docs/adr/ADR-*.md 2>/dev/null | sort | while read f; do
  num=$(grep -m1 "^# ADR-" "$f" | grep -oE "ADR-[0-9]+")
  title=$(grep -m1 "^# ADR-" "$f" | sed "s/^# ADR-[0-9]*: //")
  status=$(grep -m1 "^\*\*Status:\*\*" "$f" | sed 's/\*\*Status:\*\* //')
  date=$(grep -m1 "^\*\*Date:\*\*" "$f" | sed 's/\*\*Date:\*\* //')
  fname=$(basename "$f")
  echo "| [$num]($fname) | $title | $status | $date |" >> docs/adr/README.md
done
echo "Generated docs/adr/README.md"
```

---

## Quick Mode

For a fast, minimal ADR when you just want to record a decision:

```
/living-adr --quick "We're using Redis for session storage because the DB was getting hit too hard."

→ Creates ADR-NNN-use-redis-for-session-storage.md
   with pre-filled Context, Decision, and a placeholder Consequences section.
   Status: Proposed. Edit the file to add alternatives and sign off.
```

---

## Why "Living" ADRs

Most ADR tools generate the file and stop. The "living" part means:

1. **Auto-detection** — no need to remember to write an ADR; the skill detects architectural signals in your diff
2. **Supersession tracking** — when you migrate from A to B, the skill finds the A-related ADR and marks it Superseded, keeping history clean
3. **Index maintenance** — the `docs/adr/README.md` index stays current
4. **Committed alongside code** — the git commit command is included in the output so the decision and the code change travel together in history

The goal: six months later, a new team member can run `ls docs/adr/` and understand every significant architectural choice the team made, why they made it, and what replaced what.

---

## Author

**[Canlah AI](https://canlah.ai)** — Run performance marketing without breaking your brand.

- GitHub: [github.com/PHY041](https://github.com/PHY041)
- All Skills: [clawhub.ai/PHY041](https://clawhub.ai/PHY041)
