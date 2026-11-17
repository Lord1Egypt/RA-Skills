# Reply input contract

Use `mochi-reply-drafts.v1`; [sample/reply.json](../samples/reply.json) is a complete fictional fixture.

- `reportLanguage`: `zh-CN` or `en`; the model writes the actual reply in the requested language.
- `channel`: `email` (default) or `support`. Email destinations are bare addresses; support destinations may be explicit single-line ticket IDs.
- `incoming`: `{from,body}`. Body is retained verbatim as source `incoming`, classified `incoming-claim`. This reserved ID cannot be replaced.
- `sources`: 0–30 `{id,kind,text}` entries. `kind` is `provided`, `policy` or `incoming-claim`. “Provided” describes provenance, not independent verification. Source text is limited to 40,000 characters each.
- `facts`: 0–100 `{id,sourceId,quote,text}` entries. A short quote (max 1,000 characters) must occur in the source after whitespace normalization. Fact numbers/links must be present in that quote. A quote does not prove that a paraphrase is accurate.
- `requests`: 0–50 `{id,text,quote}` entries with quotes from the incoming body. Link draft paragraphs to the requests they address.
- `allowedRecipients`: 0–10 destinations actually supplied/approved by the user. No newly inferred CC/BCC. Missing or disallowed destinations block completion.
- `allowedCommitments`: 0–30 `{id,text,factIds}` exact statements expressly authorized by user-provided facts/policy. Supporting facts cannot be solely customer claims. The script checks structural evidence, not whether the operator actually granted authority.
- `draft`: `{to,subject,greeting?,paragraphs,closing?}`. Subject is a single line. Each of 1–30 paragraphs is `{text,factIds,requestIds,commitmentId?}` and must reference facts or an incoming request. A sensitive commitment must exactly match its referenced allowed statement after whitespace normalization.

IDs are up to 40 characters, using letters, digits, hyphens or underscores. JSON is UTF-8, at most 1 MiB. Quote and preserve source evidence; do not change it to make validation pass. Numbers/links in subject/greeting/closing are also checked. A missing draft response to a request is a visible warning.

Outputs in a new `mochi-reply-drafts-UUID/` directory:

- `draft.txt`: a clearly marked local draft with destination and subject; not an email message file and never sent.
- `checklist.md`: mechanical issues and source/evidence review; untrusted source content is in literal fenced blocks.
- `report.json`: `blocked` or `review_required`, issue codes, `deliveryPerformed:false` and `semanticAccuracyVerified:false`.
- `run.json`: report plus input SHA-256 and generation time.

Exit 0 means no blocking mechanical issue, never “safe to send”. Exit 2 preserves blocked drafts/checklists. Exit 1 means input/execution failure. Promise detection is heuristic in Chinese/English: independently review promises, payment claims, negatives and conditional wording. No signature, attachment, mailbox fetching or CRM status update is performed.

Use an existing real workspace directory as `--output-dir`; symlink/junction ancestors are refused. Earlier reports and unrelated files are not modified. Self-test:

```text
node --test --test-isolation=none "{baseDir}/tests/check.test.mjs"
```

Install under `<workspace>/skills/mochi-reply-drafts/` with `SKILL.md` at that folder root, inspect the package and use `openclaw skills check`. OpenClaw format: https://docs.openclaw.ai/tools/skills (checked 2026-10-22).
