# Acceptance Tests - Gift-Idea Match Board

## Overview
- **Skill:** Gift-Idea Match Board
- **Slug:** gift-idea-match-board
- **Version:** 1.0.0
- **Project:** daily-50-skills-2026-05-08
- **Total Tests:** 10

## AT-1: Privacy-Light Inputs
- **Check:** The skill asks only for non-sensitive gift planning details.
- **Expected:** It uses nicknames, roles, broad interests, occasions, constraints, and past gift notes without requiring full addresses, private identifiers, exact birth dates, account details, or confidential information.
- **Pass:** Sensitive personal data is not requested or required.

## AT-2: Financial Boundary
- **Check:** The skill avoids financial advice.
- **Expected:** Budget is treated only as a user-supplied comfort range or effort level, with no debt, credit, investment, or spending advice.
- **Pass:** The board remains financially neutral.

## AT-3: No Shopping Links
- **Check:** The skill forbids shopping, affiliate, tracking, and vendor-specific links.
- **Expected:** Ideas are generic and may use link-free search phrases only if needed.
- **Pass:** No links or vendor pushes are included.

## AT-4: Recipient Occasion Board
- **Check:** The output includes a recipient-to-occasion board.
- **Expected:** It captures recipient label, occasion, timing, interest clues, constraints, and effort or comfort range if supplied.
- **Pass:** The user can see gift planning context in one place.

## AT-5: Idea Match Matrix
- **Check:** The output compares multiple gift candidates.
- **Expected:** Each candidate includes why it fits, fit score, effort level, timing needs, confirmation needed, and risk or mismatch note.
- **Pass:** Gift ideas are evaluated rather than listed randomly.

## AT-6: Confirmation Flags
- **Check:** Sensitive or uncertain ideas are flagged.
- **Expected:** Health, religion, culture, age-restricted items, allergies, pets, children, workplace gifts, sizes, and relationship-sensitive ideas require confirmation when relevant.
- **Pass:** The skill avoids guessing sensitive preferences.

## AT-7: Top Picks And Fallbacks
- **Check:** The output includes top picks.
- **Expected:** It names a best match, backup idea, low-effort fallback, and non-material option if appropriate.
- **Pass:** The user has clear next choices.

## AT-8: Reusable Notes
- **Check:** The output includes reusable future notes.
- **Expected:** It records what worked, what to avoid, a future clue, and the next occasion placeholder.
- **Pass:** The board supports future planning without becoming intrusive.

## AT-9: Document Language
- **Input:** Any valid trigger.
- **Expected:** Output is English-only with no CJK text.
- **Pass:** Main output is in English.

## AT-10: No-Code Compliance
- **Check:** No executable files, scripts, packages, API calls, network calls, or credential requirements exist.
- **Expected:** `skill.json` has `hasExecutableCode: false`, `no_code_execution: true`, `requires_api: false`, `no_network: true`, and `no_credentials: true`.
- **Pass:** Skill is document-only and prompt-flow only.

## Clean Scan Evidence

- **Executable code:** None — document-only prompt-flow skill
- **API calls:** None required
- **Network access:** None required
- **Credentials:** None required or stored
- **External dependencies:** None
- **File count:** 3 (SKILL.md, skill.json, ACCEPTANCE.md)
- **Non-ASCII content:** None — English only
- **Secrets, tokens, or keys:** None present
- **Logs, temp files, or build artifacts:** None

## Install-First Success Path

1. **Input:** User says "My sister's birthday is in two weeks and I have no ideas. Build me a match board."

2. **Steps:**
   - Agent asks for privacy-light details: sister's interests, past gifts that worked/didn't, constraints
   - Agent captures recipient label, occasion, timing, interest clues, and comfort range
   - Agent generates multiple idea candidates with fit scoring (usefulness, delight, effort, timing)
   - Agent flags any ideas needing size, allergy, or relationship confirmation
   - Agent selects top picks: best match, backup, and low-effort fallback

3. **Output:** A Gift-Idea Match Board with recipient board, idea match matrix with fit scores, confirmation flags, top picks, and reusable future notes — no shopping links, no private data, no financial advice.
