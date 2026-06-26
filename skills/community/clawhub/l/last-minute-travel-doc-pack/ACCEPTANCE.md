# Acceptance Tests - Last-Minute Travel Doc Pack

## Overview
- **Skill:** Last-Minute Travel Doc Pack
- **Slug:** last-minute-travel-doc-pack
- **Priority:** P2
- **Project:** daily-50-skills-2026-05-08
- **Total Tests:** 8

## AT-1: Trip snapshot is captured.
- **Check:** Output identifies departure timing, destination, transit, travelers, and travel mode.
- **Expected:** The checklist is tailored to the actual trip.
- **Pass:** The trip context is clear enough to organize documents.

## AT-2: Required papers are listed.
- **Check:** Output includes identity, entry, transport, lodging, insurance, health, minor, pet, driving, invitation, onward travel, or emergency contact documents where relevant.
- **Expected:** The document list covers likely travel needs while asking the user to verify official rules.
- **Pass:** The list is destination-ready and not generic only.

## AT-3: Documents are sorted by traveler.
- **Check:** Output creates one section per traveler or traveler label.
- **Expected:** Each traveler has must-have, print, offline, backup, and missing items.
- **Pass:** A group can pack without mixing documents.

## AT-4: Private ID numbers are not stored.
- **Check:** Output uses document labels only and avoids passport numbers, national ID numbers, visa numbers, ticket numbers, payment card details, and full birth dates.
- **Expected:** Sensitive identifiers are neither requested nor recorded.
- **Pass:** Privacy boundary is maintained.

## AT-5: Missing items are prioritized.
- **Check:** Output includes urgency, next action, owner, and deadline for missing or uncertain items.
- **Expected:** Critical blockers are clearly distinguished from helpful backups.
- **Pass:** User knows what to resolve first.

## AT-6: Print, offline, original, and backup categories are separated.
- **Check:** Output says what to carry original, print, download offline, and keep as backup.
- **Expected:** The user can prepare for phone failure, poor internet, and document checks.
- **Pass:** Each category is practical and distinct.

## AT-7: Packet order and final check are included.
- **Check:** Output orders documents for departure, transit, destination entry, lodging, return, and emergency use.
- **Expected:** A final departure check confirms originals, printed copies, offline copies, and critical missing items.
- **Pass:** The packet is ready to use under time pressure.

## AT-8: Official rules and no-guarantee boundary are respected.
- **Check:** Output does not guarantee boarding or entry and directs official verification when requirements matter.
- **Expected:** No legal, immigration, or customs certainty is invented.
- **Pass:** The skill stays logistical and safety-aware.

## Clean Scan Evidence

- **Secrets scan:** No API keys, tokens, passwords, or private identifiers present. Skill explicitly avoids storing passport numbers, national ID numbers, visa numbers, ticket numbers, payment card details, or full birth dates.
- **Executable scan:** No scripts (.sh, .py, .js, .rb), no package files, no build artifacts.
- **Network scan:** No API calls, no HTTP client usage, no webhook URLs, no remote endpoints.
- **Credential scan:** No credential instructions, no .env references, no auth flow.
- **Safety metadata:** document_only, promptOnly, runtime:none, execution:noExec, no_code_execution, no_network, no_credentials, requires_api:false.
- **Encoding:** English-only (ASCII-safe), no CJK, no RTL, no special Unicode.
- **File count:** 3 files (SKILL.md, ACCEPTANCE.md, skill.json), no temp/log/hidden files.

## Install-First Success Path

**Input:** User says "We fly tomorrow from Canada to Italy through Germany with two adults and one child. Our papers are scattered."

**Steps:**
1. Agent reads the skill and asks for departure date/time, destination, transit countries, traveler details (adult/child/infant/pet), and travel mode.
2. Agent builds a document checklist by type: passport/ID, visa/ETA, transport bookings, lodging, insurance, health docs, minor consent, pet docs, driving permits, event letters, return proof, emergency contacts.
3. Agent sorts documents by traveler, creating per-person sections with carry-original, print, download-offline, and backup-copy categories.
4. Agent marks missing items with urgency levels (Critical/Important/Helpful), next action, owner, and deadline.
5. Agent creates a packet order: departure, transit, destination entry, lodging, return, emergency backups, plus a grab-first section for the first two hours.

**Output:** A Destination-Ready Travel Document Pack with trip snapshot, traveler-by-traveler document lists, missing item tracker, print/download checklists, packet order, and final departure check. No private ID numbers are stored.
