# Troubleshooting

## `not_authenticated`

Run `python3 scripts/pocketbook.py auth login` from an interactive terminal on the OpenClaw host. The password prompt is hidden.

## Session refresh fails

Re-run `auth login`. Do not place the password in `.env`, shell history, chat, or a skill file.

## Multiple providers

PocketBook can return more than one shop/provider for an account. Interactive login lists them. Pick the provider used by the user's PocketBook Cloud library.

## Ambiguous book

Use `search` and resolve by author, format, ISBN, filename, id, or `fastHash`. Destructive operations must not guess.

## Book has no download link

Some purchased/DRM/LCP items are not exposed as ordinary downloadable files. The skill does not bypass those restrictions.

## Notes are empty

PocketBook notes are keyed by `fast_hash`. A book can legitimately have no notes/highlights/bookmarks even when reading progress exists.

## HTTP 429 or 5xx

Treat as transient. Retry with delay and a strict bound; do not spin. Persistent failures can indicate a PocketBook Cloud outage or API change.
## Telegram FB2/XML inflates model context

Some OpenClaw versions automatically extract `application/xml` and `text/xml` document bodies into the model-visible prompt. Telegram can label FB2 as `application/xml`, so a normal ebook upload can consume tens of thousands of prompt characters before the skill runs.

For a PocketBook upload agent, configure `gateway.http.endpoints.responses.files.allowedMimes` explicitly and omit `application/xml` and `text/xml`. Keep the ordinary MIME types the agent should still auto-read, such as `text/plain`, `text/markdown`, `text/html`, `text/csv`, `application/json`, `application/pdf`, YAML, and JavaScript. The original attachment remains available through `MediaPath`; only automatic text extraction is skipped.

For multiple current ebook attachments, pass all `MediaPaths` once to `upload-inbound-many`. Do not loop through books in separate model turns.

## Upload accepted but not verified

`accepted: true` is not the same as a verified library entry. If PocketBook returns no `fast_hash`, or the exact hash has not appeared in the library yet, the helper returns `verified: false`. Do not repeat the upload automatically: that can create duplicates. Keep the source file and check again before retrying.

## Large batch requires confirmation

When a batch transfer returns `requiresConfirmation: true`, no transfer has started. Ask the user for a separate explicit confirmation. Only on that next confirmation turn rerun the same batch command with `--confirmed`; do not add `--confirmed` in the initiating turn.

## Delete accepted but not verified

If deletion returns `accepted_unverified` / `reconcileRequired`, PocketBook accepted the request but disappearance was not verified. Do not report the book as deleted and do not replay the consumed confirmation. Reconcile with a read-only library check; any later destructive retry begins with a new `delete prepare`.
