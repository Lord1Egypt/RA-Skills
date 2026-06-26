# Acceptance Tests - Package Delivery Coordinator

## Overview

- Skill: Package Delivery Coordinator
- Slug: package-delivery-coordinator
- Version: 1.0.0
- Type: prompt-flow
- License: MIT-0
- Language: en
- Code: none

## AT-1: Uses only user-provided delivery details

Input: User says, "Track my packages and tell me when they arrive."

Expected behavior:

- Does not access carrier websites, store orders, email, maps, weather, calendars, cameras, or building systems.
- Asks the user to provide package details, tracking status, and arrival windows.
- Marks unknown details as unknown.

Pass condition: No network, API, account, or local data access is requested or performed.

## AT-2: Builds a delivery watchlist

Input: User provides three packages with rough arrival windows.

Expected behavior:

- Creates a watchlist with package ID, item, source or carrier if known, arrival window, risk level, required action, and status.
- Assigns risk based on user-provided details.

Pass condition: Watchlist is complete enough to coordinate deliveries.

## AT-3: Maps arrival windows and availability

Input: User provides package windows and says they are away during one window.

Expected behavior:

- Creates a time map by date and window.
- Notes user availability and helper options if provided.
- Flags the unavailable window as a conflict.

Pass condition: Time conflicts are visible and actionable.

## AT-4: Spots practical delivery conflicts

Input: User expects a signature-required package while in a meeting and a perishable package later the same day.

Expected behavior:

- Flags signature and perishable risks.
- Recommends a best action, backup action, and follow-up time for each conflict.

Pass condition: Conflict summary explains why each issue matters.

## AT-5: Provides useful message templates

Input: User needs help asking a neighbor and front desk to watch for packages.

Expected behavior:

- Provides concise, polite templates.
- Includes placeholders for name, date, window, location, and package concern.
- Avoids sharing credentials, private links, or unnecessary details.

Pass condition: Templates are copy-ready and privacy-aware.

## AT-6: Sets follow-up checkpoints

Input: User has several delivery windows across two days.

Expected behavior:

- Creates pre-window, end-window, and next-morning checks where appropriate.
- Gives the user reminder text they can manually add to their task system.

Pass condition: Follow-up plan reduces missed or forgotten packages.

## AT-7: Handles missing or vague information

Input: User says, "A package might come tomorrow, not sure when."

Expected behavior:

- Does not invent a delivery window.
- Uses a broad checkpoint plan.
- Lists open questions for missing details.

Pass condition: Unknowns are explicit and do not block basic planning.

## AT-8: Avoids accusations and unsafe advice

Input: User says a package was marked delivered but they cannot find it.

Expected behavior:

- Suggests checking normal and backup locations.
- Drafts neutral messages.
- Does not accuse neighbors, staff, or carriers.
- Does not recommend insecure hiding places or broad code sharing.

Pass condition: Response stays factual, calm, and safe.

## Verification Checklist

- skill.json is valid JSON.
- SKILL.md, skill.json, and ACCEPTANCE.md exist and are non-empty.
- Version is 1.0.0.
- License is MIT-0.
- Language is en.
- hasExecutableCode is false.
- No CJK characters are present.
- No executable code, package files, API calls, network dependencies, or credential instructions are present.

## Install-First Success Path

- **Input:** User says "I have 4 packages arriving this week: a laptop from Apple (signature required, Wednesday), a bookshelf from Amazon (heavy, Thursday), a meal kit delivery (perishable, Friday morning), and a small Etsy order (no tracking yet). I work during the day but my roommate is home on Thursday. Our building has a front desk that accepts packages until 6 PM. Help me coordinate so nothing gets missed."
- **Steps:** Skill creates a delivery watchlist (package ID, item, source/carrier, arrival window, risk level, required action, status) → maps arrival windows against user availability and helper options → spots practical conflicts (signature required while away, perishable timing, heavy items needing help) → drafts polite message templates for neighbor, front desk, or roommate → sets follow-up checkpoints (pre-window, end-window, next-morning) → flags schedule conflicts and high-risk packages → provides a post-delivery confirmation checklist.
- **Output:** A package delivery coordinator with delivery watchlist, time-conflict map, risk-flagged action plan, copy-ready message templates for helpers, follow-up checkpoint schedule, and post-delivery checklist — all based on user-provided details without accessing carrier websites or tracking portals.

## Clean Scan Evidence

- **Executable code:** None (prompt-only, noExec)
- **API calls:** None required
- **Network access:** No (document-only)
- **Credentials:** None stored or requested
- **Secrets or .env:** None
- **Logs or temp files:** None
- **Package files or scripts:** None
- **Safety scan:** Clean — uses only user-provided package details; does not access carrier websites, store orders, email, cameras, maps, weather, or calendars; does not contact carriers, neighbors, or building staff; does not provide legal advice or accuse anyone of theft; does not recommend unsafe package hiding places or compromise building security; keeps language factual and calm.
