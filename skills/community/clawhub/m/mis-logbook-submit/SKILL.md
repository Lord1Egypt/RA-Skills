---
name: mis-logbook-submit
description: Submit a daily PENS MIS Kerja Praktek logbook entry at online.mis.pens.ac.id after an approval-first workflow. Gather same-day work evidence, synthesize concise Indonesian activity text for the Kegiatan/Materi field, sign in with local secrets, navigate to Entry Logbook KP, save the entry, and verify the new row appears. Use when inspecting, preparing, or submitting MIS KP logbooks.
---

# MIS logbook submit

Read `references/workflow.md` before doing real work.

## Core rules

- Use local secrets for login, never ask for or echo credentials in chat.
- Prefer browser automation with Playwright.
- Write `Kegiatan/Materi` in natural Indonesian.
- Respect the approval-first flow when a pending draft exists.
- Keep the text under the form limit and avoid literal `SELECT`, `INSERT`, `UPDATE`, and `DELETE` because the page may reject them.
- Check for an existing row before creating a new one.
- Verify both the success state and the saved row after submit.
