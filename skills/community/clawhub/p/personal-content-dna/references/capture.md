# Capture, confirmation and continued accumulation

## What to capture

Capture meaningful new user choices/rejections and reasons, concrete aesthetic edits, changed views, experimental results, failures/corrections and unresolved questions. Merge multiple turns about one event. Routine progress, tool output, unilateral AI proposals and repeated requirements usually do not warrant a new card.

Prefer user quotations within scope. If visible messages lack stable IDs, retain the available conversation title/date, a short searchable quotation and checked date. Unknown event dates remain unknown; capture date is not event date. Local sources use paths and sections/lines. Public repositories preferably use commit-pinned links; otherwise state branch and checked date.

Inspect permitted README files, related changes and exploration records to identify upstream work, collaborators and actual roles. Work claims can prompt missing-evidence questions; code does not establish the user's design motive. Reading documentation is not execution verification.

## Structure and index

Use Markdown cards and `index.csv`; prefer `cards/` for events and `style/` for rules. Follow existing project paths when different.

```text
id,kind,title,path,status,public_use,source_type,source_locator,checked_at
```

- `kind` is `material` or `style_rule`, consistent in frontmatter and index.
- `path` is relative to the library root and points to an existing file.
- `source_type`: `user_message`, `public_repo`, `project_record`, `project_rule`, `reference_profile` or `feedback`.
- Follow existing ID conventions. New libraries may use `PD-date-sequence` and `STYLE-sequence`; inspect occupied IDs first.
- The index excludes restricted quotations, private details and credentials. Keep safe titles and necessary locators.

Use [material-card.md](../assets/material-card.md) and [style-rule.md](../assets/style-rule.md). Unknown fields remain unknown.

## State changes

1. New candidates: `candidate + pending`. Confirmed speaker attribution alone does not establish public scope.
2. Usable materials: `approved + allowed` after user confirmation of meaning, ownership and public scope; retain the confirmation record. Direct user reports are self-report sources, with independent verification recorded separately.
3. Restricted materials: `restricted`; save only safe information permitted for retention and exclude them from routine writing.
4. Changed results, conflicting sources or withdrawn scope: `needs_review`; stop using affected claims.
5. Earlier views: `historical`, preserving the prior version and change reason. To write a public account of that change, first create an approved, allowed current event card.

One confirmation may cover explicit cards, claims or a shared scope. Reuse existing permission within scope. Approving wording for one draft does not expose an entire source or authorize account publication.

## Active-session routine

- At a milestone, complete the main task, reconcile valuable events in scope, save candidates and synchronize the index.
- For a new user judgment, retain the quotation and event; use candidate state unless meaning and scope are already confirmed.
- For confirmation, show key claims and boundaries; record corrections or adoption.
- In a requested weekly review, examine candidates, duplicates, changed views and source gaps; suggest a few worthwhile additions and reader uses. Review does not automatically upgrade states.
- After editing, follow writing-feedback instructions. New facts still require this capture process.

Cross-project requests specify permitted project/conversation scope and a shared destination. Do not scan all local sessions to compensate for unspecified sources.

## Readback

Check unique IDs and paths, index/card consistency, traceable quotations and speakers, action/result state, and confirmation support for `approved + allowed`. Do not overwrite historical cards with new conclusions; preserve change reasons.

Give Writers only topic-relevant allowed excerpts and exact paths/versions. Restricted-source research requires separately specified user scope.

The material-library concept was informed by [Nicolas Cole: The Right Way To Write With AI](https://artandbiz.substack.com/p/the-right-way-to-write-with-ai); this workflow adds source, contribution, public scope, state and feedback controls.
