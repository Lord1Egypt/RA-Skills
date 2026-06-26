---
name: greenhouse-apply
description: >
  Submit job applications on Greenhouse (job-boards.greenhouse.io). Handles the full flow:
  fill text fields, set React Select dropdowns, select phone country, upload resume, enter
  email verification code, and submit. Use when: applying to a job on Greenhouse, filling out
  a Greenhouse application form, submitting a resume to a company that uses Greenhouse ATS.
---

# Greenhouse Application Skill

Fill and submit Greenhouse job application forms via browser automation.

## Prerequisites

- Browser tool available (OpenClaw browser or Chrome extension)
- Resume PDF accessible on the filesystem
- Gmail or email access to retrieve verification codes
- User-provided: name, email, phone, resume path, answers to custom questions

## Workflow

### Phase 1: Open the Job Page
Navigate to the Greenhouse job URL.

### Phase 2: Fill All Text Fields via JS Evaluate
**Critical:** Do NOT use type on individual fields. Use a single evaluate call with native setters.

### Phase 3: Phone Country Dropdown
The phone country selector is an intl-tel-input widget. It hijacks focus from other dropdowns.

### Phase 4: React Select Dropdowns
Use Playwright click, type, press Enter on the combobox ref.

### Phase 5: Resume Upload
Use the browser upload tool with the Attach button ref.

### Phase 6: Audit Before Submit
Take a snapshot and verify EVERY field.

### Phase 7: Submit & Verification Code
The code input is 8 individual inputs with IDs security-input-0 through security-input-7.
DO NOT use Playwright type on snapshot refs for code boxes — use JS evaluate instead.

## Failure Modes & Recovery
- Characters in wrong fields: Use JS getElementById instead of snapshot refs
- Country dropdown stealing focus: Click document.body first to blur
- Dropdown shows Select after setting: Use click-type-Enter pattern
- Submit button stays disabled: Ensure input+change events fire with bubbles:true
- Code expired: Re-submit to get fresh code

## Notes
- Voluntary EEO fields are optional
- The Why Company textarea is the highest-value field
- Phone auto-formats after country selection
- Greenhouse may throttle repeat submissions