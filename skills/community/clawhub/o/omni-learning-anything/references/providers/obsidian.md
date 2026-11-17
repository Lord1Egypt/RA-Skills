# Obsidian

Obsidian is the explicit local-first exception to cloud API delivery. Use [guided connection](../onboarding.md) to validate/save the existing Vault path; the learner does not need an API account. The official Obsidian CLI can assist opening/reading notes when the installed app supports it; there is no bundled official cloud-write API. Ask for an existing Vault directory and a dedicated relative course subdirectory, not an API token/account. Example:

```json
{"platform":"obsidian","mode":"local","destination":{"vault_path":"/confirmed/vault","subdir":"Omni Learning/History"}}
```

`publish` copies `plan.md`/`DayNN.md` with a stable delivery marker and content-hashed teaching assets. Image references are relative to the course notes. Existing different files, user edits and symlinks escaping the course/Vault are rejected. Retries reuse matching bytes. Readback checks the note and image bytes before verifying; the receipt returns the actual note path and an Obsidian URI.

Open the note in the real Obsidian client for visual acceptance, including Chinese text, figure, source links and metadata. Do not edit the user's existing notes or `.obsidian` settings. Existing Obsidian Sync/iCloud/other sync software is responsible for cross-device availability; the publisher cannot attest that synchronization finished.

If the Vault is unavailable on an unattended host, retain the local course artifact and ask for access/a confirmed new location. Do not substitute another user's Vault or use community REST plugins without explicit user intent.

Official sources checked 2026-10-14:
- https://obsidian.md/help/import/markdown
- https://help.obsidian.md/Extending+Obsidian/Obsidian+URI

Native acceptance on 2026-10-18: reopened the previously delivered QA plan and Day01 in the actual Vault; inspected full reading views, bilingual text/practice, local diagram/credit and five rendered hyperlink fixtures per note. This supplements filesystem/readback/idempotency checks; it does not establish cross-device sync or validate the synthetic `example.com` fixtures as research sources.
