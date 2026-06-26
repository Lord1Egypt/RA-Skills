# Acceptance Tests - Kid Activity Registration Command Center

## Overview
- **Skill:** Kid Activity Registration Command Center
- **Slug:** kid-activity-registration-command-center
- **Priority:** P2
- **Project:** daily-50-skills-2026-05-08
- **Total Tests:** 8

## AT-1: High-intent trigger fit
- **Input:** "I have to register my kids for camps and sports and I am losing track of deadlines."
- **Expected:** The skill creates a child activity registration command sheet.
- **Pass:** Output focuses on activities, registration, deadlines, forms, payments, gear, transport, and follow-up.

## AT-2: Activity comparison table
- **Check:** Response captures activity name, date range, location, cost, deadline, decision status, and organizer contact if available.
- **Expected:** Multiple options can be compared side by side.
- **Pass:** A comparison table or structured equivalent is present.

## AT-3: Deadline and payment tracker
- **Check:** Response includes registration deadline, payment due date, late-fee risk, waitlist risk, confirmation status, and receipt tracking.
- **Expected:** Urgency is clear.
- **Pass:** User can see what must happen next and by when.

## AT-4: Documents and privacy safety
- **Check:** Response lists forms, waivers, medical or emergency contact fields, photos, evaluations, and prerequisite documents as checklist labels.
- **Expected:** It does not ask for full sensitive IDs, medical record numbers, payment card numbers, passwords, or credentials.
- **Pass:** Sensitive data is not requested.

## AT-5: Schedule and capacity review
- **Check:** Response considers conflicts, commute burden, family capacity, child interest, pickup and drop-off coverage, and backup plans.
- **Expected:** The plan helps avoid overcommitment.
- **Pass:** Capacity risks and conflicts are visible.

## AT-6: Calendar handoff and first-day prep
- **Check:** Output includes calendar handoff notes plus gear and first-day preparation.
- **Expected:** Pickup/drop-off, backup contact notes, and reminders are included.
- **Pass:** The handoff can be copied into a family calendar or shared plan.

## AT-7: Organizer verification boundary
- **Check:** Response tells the user to verify policies, fees, supervision, medical requirements, deadlines, and refund rules with the organizer.
- **Expected:** It does not guarantee safety, eligibility, refunds, or availability.
- **Pass:** Official verification is clear.

## AT-8: Prompt-only compliance
- **Check:** Skill directory contains only SKILL.md, skill.json, and ACCEPTANCE.md.
- **Expected:** No executable code, scripts, package files, API handlers, network instructions, or credential requirements.
- **Pass:** Metadata has language en, hasExecutableCode false, requires_api false, no_network true, no_credentials true, and no_code_execution true.

## Install-First Success Path

- **Input:** User says "I need to register my two kids (ages 7 and 10) for summer activities — swim team (deadline May 15, $200), coding camp (deadline May 20, $350), and soccer (deadline May 12, $150). Swim team needs a physical form. Coding camp has a waitlist. Help me build a registration command center with deadlines, forms, payments, and schedule conflicts."
- **Steps:** Skill captures activity options (name, child, dates, location, cost, deadline, decision status, organizer contact) → identifies required materials (forms, waivers, medical/emergency contacts, photos, evaluations, gear) → builds deadline and payment tracker (deadline, payment due, late-fee risk, waitlist risk, confirmation, receipts) → compares schedule fit, commute burden, family capacity, and child interest → creates gear and first-day checklists → drafts organizer questions → prepares calendar handoff with pickup/drop-off roles and reminders → prioritizes final actions by urgency.
- **Output:** A kid activity registration command sheet with activity comparison table, deadline/payment tracker, document checklist, schedule/conflict review, gear list, organizer questions, calendar handoff summary, and urgency-sorted action plan.

## Clean Scan Evidence

- **Executable code:** None (prompt-only, noExec)
- **API calls:** None required
- **Network access:** No (document-only)
- **Credentials:** None stored or requested
- **Secrets or .env:** None
- **Logs or temp files:** None
- **Package files or scripts:** None
- **Safety scan:** Clean — does not recommend specific providers, guarantee child safety, or request sensitive IDs/passwords/credentials; encourages user to verify policies, fees, supervision, and medical requirements directly with organizers.
