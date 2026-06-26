---
name: niche-calendar
description: Specialized calendars for developers and ClawHub: WHL hockey (Blades) schedules, npm/ClawHub release timelines, Saskatchewan events, custom dev planning/publish schedules. Use when: &quot;Blades next game?&quot;, &quot;React release calendar&quot;, &quot;new ClawHub skills&quot;, &quot;Saskatoon events&quot;, &quot;plan ClawHub skill publishes&quot;.</description>
---

# Niche Calendar

## Triggers &amp; Use Cases
- **Sports:** WHL Saskatoon Blades schedule, games, standings.
- **Releases:** NPM packages, ClawHub new/updated skills timelines.
- **Events:** Saskatoon/Clavet local (housing, hockey, dev meetups).
- **Dev Planning:** ClawHub skill version planning, publish timelines.

NOT for: general weather (weather skill), personal calendars (no caldav tool).

## Workflow
1. **Parse query:** Identify type (sports/release/event/planning).
2. **Gather data:**
   - Sports: `web_search &quot;WHL Saskatoon Blades schedule {current_month} 2026 site:blades.ca&quot; country=&quot;CA&quot;`
   - Releases NPM: `web_search &quot;{package} release schedule 2026&quot;`
   - ClawHub: `exec &quot;clawhub list&quot;`, `web_search &quot;clawhub.com new skills&quot;`
   - Events: `web_search &quot;Saskatoon events {date range}&quot; country=&quot;CA&quot;`
   - Planning: Suggest milestones (design/v1/test/publish).
3. **Extract &amp; format:** Dates, descriptions, links. Use tables.
4. **Enhance:** Current date via `session_status`. Future-focused.

## Example Outputs
**Blades Schedule:**
| Date       | Opponent     | Time   | Venue     | Result/Link |
|------------|--------------|--------|-----------|-------------|
| 2026-03-30 | Regina Pats | 7pm   | SaskTel   | [tickets](url) |

**ClawHub Recent:**
- niche-email v1.0.0 (Mar 28)
- Upcoming: Check search &quot;dev calendar&quot;

## Tools
- `web_search` + `web_fetch` primary.
- `exec &quot;clawhub search {term}&quot;` for ClawHub.
- `session_status` for date/time.

Proactive: If publish-related, suggest `clawhub publish` steps.
