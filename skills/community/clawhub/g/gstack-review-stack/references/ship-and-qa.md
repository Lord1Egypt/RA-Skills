# Ship And QA Gate

Use this for release, publish, deploy, submit-for-review, and "is it ready?" work.

## Ship Gate

Before release:
- Confirm package/version identity.
- Confirm permission and privacy disclosures match actual behavior.
- Run local unit and e2e checks appropriate to the blast radius.
- Test the main user flow as a real user, not only with mocked internals.
- Inspect logs/network errors for hidden failures.
- Confirm listing screenshots, icons, URLs, support links, and privacy pages.
- Identify store-side or account-side blockers separately from code blockers.

## QA Output

Report:
- Tests run
- User flows verified
- Critical failures found/fixed
- Remaining blockers
- Ship/no-ship recommendation
- Rollback or recovery path

## Stop Conditions

Stop before destructive actions unless the user explicitly approved:
- Unpublish/delete/hide a live listing
- Submit a store listing with inaccurate claims
- Publish with known broken core flow
- Ship a privacy disclosure that omits data sharing or permissions
