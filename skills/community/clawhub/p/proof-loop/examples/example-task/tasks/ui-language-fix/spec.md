# Task: ui-language-fix

## Task Statement

Fix the language switcher so a user who selects German sees the navigation labels in German after saving the preference.

## Acceptance Criteria

**AC1:** A user with  sees the main navigation labels in German after saving language preference.
- Verify: run the browser check described in  and confirm Home, Settings, and Billing are rendered as Startseite, Einstellungen, and Abrechnung.

**AC2:** The language preference survives a page reload.
- Verify: reload the page after saving German and confirm the same German navigation labels remain visible.

**AC3:** The existing English navigation remains unchanged for .
- Verify: switch back to English and confirm Home, Settings, and Billing are rendered in English.

## Constraints

- Do not change the navigation route structure.
- Do not change stored user preference keys.
- Do not introduce a new translation framework.

## Non-Goals

- Translating every page in the product.
- Adding new locale options.
- Reworking the account settings UI.

## Verification Approach

A fresh verifier should run the locale browser checks for German and English, inspect the stored preference after save, and record PASS / FAIL / UNKNOWN for each AC in .
