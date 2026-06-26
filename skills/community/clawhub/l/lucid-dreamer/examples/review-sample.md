# Memory Review — 2026-03-16

## Candidate Updates

### 1. Atlas Agent — New Infrastructure (high confidence)
- **Add to Projects section:** `atlas-node` VM (Tailscale `10.0.0.42`) running Atlas agent with GPT-5.4 via OAuth, systemd service `atlas-gateway.service`, lightweight vector memory enabled
- **Source:** `memory/2026-03-15.md` (Atlas Agent Setup) + `memory/2026-03-13.md` (initial install)
- **Context:** Replaces `old-orbit` (retired 2026-03-13), `Pilot` vs `Atlas` decision still pending as of 2026-03-15

### 2. atlas-webchat Project (medium confidence)
- **Add to Projects section:** `atlas-webchat` — Next.js 15 + FastAPI mock backend, repo `alexchen-labs/atlas-webchat`, deployed on atlas-node ports 8444/8445 (currently disabled), **no real Atlas agent connected yet**
- **Source:** `memory/2026-03-16.md` (atlas-webchat project section)

### 3. Morning Briefing Model — Pending Change (medium confidence)
- **Update Model Strategy table:** `Morning Briefing` row — currently shows Kimi, but 2026-03-14 benchmarks found Sonnet wins. Pending Alex decision.
- **Source:** `memory/2026-03-14.md` (~"Morning Briefing Model" section)

### 4. Backup System Overhaul (high confidence)
- **Update MEMORY.md:** Add note that `scripts/backup-remote.sh` was rewritten 2026-03-15 to use native `openclaw backup create`. Old split-workspace + separate-config approach replaced.
- **Source:** `memory/2026-03-15.md` (Backup System section)

### 5. web-search-plus Skill Version Mismatch (medium confidence)
- **MEMORY.md Published Skills table** shows `web-search-plus 2.7.2` but notes show it was bumped to 2.9.0 (2026-03-12) and the plugin to 1.2.2 (2026-03-11). Table is stale.
- **Source:** `memory/2026-03-12.md` (web-search-plus v2.9.0) + `memory/2026-03-11.md` (plugin v1.2.2)

### 6. QUERY_API_KEY TODO (low confidence)
- **Lessons Learned / Operational:** `QUERY_API_KEY` still missing from `skills/web-search-plus/config.json` — noted as TODO since 2026-03-12. Worth adding as a formal TODO or note.
- **Source:** `memory/2026-03-12.md` (web-search-plus v2.9.0 section, end)

---

## Open Loops

### 1. Pilot vs Atlas Decision
- **Started:** 2026-03-15 — Plan was "test Atlas this week → if stable, shut down Pilot"
- **Missing:** No closure signal. Pilot still running (6€/mo). Atlas tested on 2026-03-15/16 but decision not final.
- **Source:** `memory/2026-03-15.md` ("Decision: Pilot vs Atlas")

### 2. atlas-webchat — Real Agent Integration
- **Started:** 2026-03-16 — Mock backend only, no real Atlas agent connected
- **Missing:** Actual integration + UI polish ("still rough" per Alex)
- **Source:** `memory/2026-03-16.md` ("Next Steps")

### 3. Skill Selection — Life OS / GitClaw / others
- **Started:** 2026-03-12 brainstorm → carried through 2026-03-15/16
- **Missing:** No decision made after 4+ days of discussion
- **Source:** `memory/2026-03-16.md` (Skill Ideas section) + `memory/2026-03-15.md` (Top 3 section)

### 4. X/Twitter Login on browser-node
- **Started:** 2026-03-14 — Manual login via noVNC needed, bot detection blocks automated flow
- **Missing:** Still not logged in as of 2026-03-15
- **Source:** `memory/2026-03-15.md` + `memory/2026-03-14.md`

### 5. awesome-mcp-servers PR #3156
- **Started:** 2026-03-13 — Submitted, waiting on merge after AAA score (2026-03-14)
- **Missing:** No confirmation of merge
- **Source:** `memory/2026-03-14.md` (web-search-plus-mcp section)

### 6. Morning Briefing Model Switch (Kimi → Sonnet)
- **Started:** 2026-03-14 — Sonnet identified as winner but not yet changed
- **Missing:** Config update never happened; explicit decision pending
- **Source:** `memory/2026-03-14.md` (Morning Briefing Model section)

### 7. agent-chronicle 0.6.2 → ClawHub publish
- **Started:** 2026-03-10 (Open TODOs) — local ahead of ClawHub 0.6.0
- **Missing:** Still listed as TODO across 6+ days with no resolution
- **Source:** `memory/2026-03-10.md` + `memory/2026-03-12.md`

### 8. personas --force update to 2.2.6
- **Started:** 2026-03-10 — local 2.2.4, ClawHub 2.2.6
- **Missing:** Never resolved despite appearing in every TODO list
- **Source:** `memory/2026-03-10.md` through `memory/2026-03-12.md`

### 9. Partner Follow-up (Jamie / Casey)
- **Started:** 2026-03-09 email sent, reminder cron set for 2026-03-16 09:00 Vienna
- **Missing:** As of 2026-03-15, no reply yet. Today (2026-03-16) is the follow-up date — status unknown.
- **Source:** `memory/2026-03-14.md` + `memory/2026-03-15.md`

### 10. Gigabrain Fork Decision
- **Started:** 2026-03-12 — "Tomorrow decide if we start"
- **Missing:** No decision noted in 2026-03-13/14/15/16 notes
- **Source:** `memory/2026-03-12.md` (Memory System Research section)

---

## Blockers

### 1. atlas-webchat UI quality ("still rough")
- Alex explicitly noted the UI is still rough after two code passes
- Mentioned on 2026-03-16 with no resolution in same session
- **Source:** `memory/2026-03-16.md`

### 2. Persistent low-priority TODOs (personas, agent-chronicle)
- `personas --force update to 2.2.6` and `publish agent-chronicle 0.6.2` appear repeatedly from 2026-03-10 through 2026-03-16 — never acted on
- Both are trivial 5-minute tasks that keep getting deprioritized
- **Source:** `memory/2026-03-10.md`, `2026-03-12.md`, `2026-03-14.md`, `2026-03-15.md`

---

## Belief Updates

### 1. Browser Tool Default Changed
- **Previously (2026-03-11):** `browser` tool used `profile: "browserless"` as explicit default
- **Now (2026-03-14+):** `browser-node` is the new default — no profile parameter needed
- AGENTS.md was updated; MEMORY.md references are consistent with this
- **Source:** `memory/2026-03-14.md` (Infrastructure Notes) + `memory/2026-03-11.md`

### 2. Old Orbit Server — Deleted
- **Previously:** Multiple references to `10.0.0.43` / `orbit.tail12345.ts.net` / `oldorbit.tail12345.ts.net` as experimental servers
- **Now:** Deleted by Alex 2026-03-13 — no active server at that IP
- MEMORY.md appears clean of these references already
- **Source:** `memory/2026-03-13.md` (end: "Old Orbit — deleted")

### 3. Vendor Trial — Evaluation Stopped
- **Previously (2026-03-10/15):** External agent vendor being tested, credits received
- **Now (2026-03-15):** Uninstalled after repeated disconnect issues, decided not a fit
- MEMORY.md doesn't mention it — no update needed
- **Source:** `memory/2026-03-15.md` (Vendor Trial section)

---

## Stale Facts

### 1. MEMORY.md Model Strategy Table — Morning Briefing
- Table shows `Morning Briefing → Kimi`
- 2026-03-14 benchmarks clearly show Sonnet wins Morning Briefing
- However: decision to switch is explicitly pending → confidence medium (don't change until Alex decides)
- **Source:** MEMORY.md "Model Strategy" section vs `memory/2026-03-14.md`

### 2. MEMORY.md Published Skills Table — Versions
- `web-search-plus 2.7.2` is stale → actually 2.9.0 (since 2026-03-12)
- `web-search-plus-plugin 1.0.1` stale → actually 1.2.2 (since 2026-03-11)
- These are high-confidence staleness findings
- **Source:** `memory/2026-03-12.md` + `memory/2026-03-11.md`

### 3. Partner Reminder Cron — One-shot, likely fired
- MEMORY.md still shows: "Reminder Cron: set for 2026-03-16 09:00 Vienna (ID: `demo-cron-1234`)"
- Today is 2026-03-16 — this cron has already fired (or was due to). Should be removed from MEMORY.md once the follow-up loop closes.
- **Source:** MEMORY.md Partner Follow-up section + `memory/2026-03-14.md`

---

## Trends

### 🔁 Recurring Issues
_Same issue/topic flagged on 3+ separate days in the last 14 days._

1. **tailscale down / disconnect** — appeared on 4 days (2026-03-10, 2026-03-12, 2026-03-14, 2026-03-15)
2. **personas --force update pending** — appeared on 7 days (2026-03-10, 2026-03-11, 2026-03-12, 2026-03-13, 2026-03-14, 2026-03-15, 2026-03-16)

### 🕸️ Possibly Stale Projects
_Projects in MEMORY.md not mentioned in any daily note for 30+ days._

_All tracked projects appear active._

### ⚠️ Escalated Patterns (Repeated Mistakes)
_Same lesson/mistake appearing in 3+ daily notes — pattern not yet broken._

_No escalated patterns detected._

---

## Duplicate/Merge Suggestions

### 1. Atlas Agent — Scattered Across Notes
- Atlas setup info appears across 2026-03-13 and 2026-03-15 daily notes
- No single coherent MEMORY.md entry exists yet for `atlas-node`
- Suggest adding a consolidated "Pilot / Atlas" section to MEMORY.md
- **Source:** `memory/2026-03-13.md` + `memory/2026-03-15.md`

### 2. Pilot section in MEMORY.md — Merge with Atlas when decided
- Current Pilot section is standalone; once the Pilot vs Atlas decision is made, these should be consolidated
- Low urgency until decision is final
- **Source:** MEMORY.md "Pilot" section
