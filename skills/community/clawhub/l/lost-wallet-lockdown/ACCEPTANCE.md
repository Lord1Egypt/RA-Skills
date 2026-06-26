# Acceptance Criteria - Lost Wallet Lockdown

## Gate Checks

- [x] `SKILL.md` exists and contains a prompt-only workflow.
- [x] `skill.json` is valid JSON and declares `version=1.0.0`, `license=MIT-0`, `language=en`, and `hasExecutableCode=false`.
- [x] File count is exactly 3: `SKILL.md`, `skill.json`, and `ACCEPTANCE.md`.
- [x] Public-facing documentation is English only.
- [x] No executable code, scripts, package files, network calls, APIs, credentials, secrets, or private data are included.
- [x] Trigger scenario, concrete deliverable, workflow, output format, and safety boundary are explicit.
- [x] The workflow produces a first-hour lockdown checklist for lost wallet contents, cards, IDs, access items, monitoring, replacements, scripts, and confirmation logging.
- [x] The skill follows the required sequence: last known place, list contents, freeze cards, report IDs, monitor accounts, and replacements.
- [x] The skill emphasizes official channels and states that it does not take institutional action on behalf of the user.
- [x] The skill avoids legal, banking, financial, cybersecurity, identity-theft recovery, law-enforcement, immigration, travel-document, and insurance advice.
- [x] No CJK characters are present.

## Scope

- Prompt-only MVP.
- Local implementation only.
- Not published to ClawHub in this phase.

## Clean Scan Evidence

- **Secrets scan:** No passwords, tokens, API keys, credentials, PII, or sensitive identifiers found.
- **Executable scan:** No scripts, shell commands, package files, binaries, or install hooks present.
- **Network scan:** No outbound URLs, API endpoints, fetch calls, or webhook targets in skill content.
- **File audit:** Exactly 3 files — SKILL.md, skill.json, ACCEPTANCE.md. No temp, log, .DS_Store, or hidden files.
- **Language audit:** All public content is English (en). No CJK, Cyrillic, Arabic-script, or mixed-encoding characters.
- **Claims audit:** No legal, banking, financial, or identity-theft recovery claims unqualified.

## Install-First Success Path

**Input:** User says "I lost my wallet an hour ago — help me lock everything down."

**Steps:**
1. Agent asks: lost or stolen? Last known place and time? Any physical danger?
2. Agent builds a last-known-place timeline with route, locations, transport, and who to contact.
3. Agent helps the user list wallet contents by category (payment cards, IDs, access, keys, cash) without full numbers.
4. Agent ranks urgent lock actions: debit cards first, then credit cards, then IDs, then access items.
5. Agent drafts freeze/report prompts for official issuer apps, card backs, and agency websites.
6. Agent creates a replacement tracker with issuer, documents needed, fee, timing, and temporary proof options.
7. Agent builds short call scripts for banks, lost-and-found, building security, employer, and ID agencies.

**Output:** A first-hour lost wallet lockdown checklist with safety check, last-known-place timeline, contents inventory, freeze/report checklist by category, monitoring plan, replacement tracker, scripts, and confirmation log. No institutional action taken on user's behalf.
