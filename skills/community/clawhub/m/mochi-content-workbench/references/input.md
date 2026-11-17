# Content input contract

Use schema `mochi-content-workbench.v1`. The [complete sample](../samples/campaign.json) shows the structure.

- `reportLanguage`: `zh-CN` or `en` for labels/checklists.
- `sources`: 1–30 `{id,text,title?,url?}` records. Preserve supplied text; max 40,000 characters per source. Optional HTTP(S) URLs are source locators only: the script does not fetch or validate their contents, ownership or availability.
- `facts`: 0–100 `{id,text,evidence:[{sourceId,quote}]}` records. At least one short quote (max 500 characters) is required per fact; it must occur in the source after whitespace normalization. Numeric/link spellings in the fact must occur in the quoted evidence. This cannot prove semantic equivalence or establish truth.
- `channels`: 1–10 `{id,label,language,maxCharacters}` records. Language is `zh-CN` or `en`; character budget is an integer 1–50,000, defined by the user/task. Do not represent it as an official platform limit.
- `drafts`: one `{channelId,blocks}` per requested channel. Each of 1–30 blocks is `{kind,text,factIds}`. `kind` is `fact`, `commentary` or `call-to-action`. Factual blocks require valid fact IDs. Numbers/links in every kind of block need corresponding cited evidence.

IDs are up to 40 characters of letters/digits/hyphens/underscores. Input is a UTF-8 JSON object of at most 1 MiB. Unknown/duplicate channel drafts, absent requested drafts, unsupported evidence, overlength or missing factual citations block mechanical completion. Identical/highly similar copy creates warnings and is retained for review, since cross-posting similar text can be intentional.

Draft text is joined using blank lines. Counts include those blank lines, whitespace and each Unicode code point. They are not grapheme counts, bytes, token counts or platform-specific weighted character counts. Chinese/English checks flag likely mismatches but are not complete language detection; proper names and mixed technical text require review.

New `mochi-content-workbench-UUID/` outputs:

- `drafts.md`: copyable literal drafts, counts, issues and cited fact IDs.
- `drafts.json`: raw draft text/counts for the user to reuse, clearly marked `requiresHumanReview:true`.
- `facts.md`: fact ledger, original short quotes and supplied source locations. HTML/Markdown in source material is not executed.
- `report.json`: structured issues, `publicationPerformed:false` and `semanticAccuracyVerified:false`.
- `run.json`: generation time, input SHA-256 and report.

Exit 0 is `review_required`, exit 2 is `blocked` with saved reports, exit 1 means invalid input or execution failure. Do not delete original facts or change source text to suppress an error. No external API, social login, timing job or publication occurs.

`--output-dir` must name an existing real directory. Symlink/junction ancestors are refused; each run creates a new folder and never overwrites earlier files. Offline tests:

```text
node --test --test-isolation=none "{baseDir}/tests/check.test.mjs"
```

Install at `<workspace>/skills/mochi-content-workbench/SKILL.md`, inspect the code and run `openclaw skills check`. Format reference: https://docs.openclaw.ai/tools/skills (checked 2026-10-22).
