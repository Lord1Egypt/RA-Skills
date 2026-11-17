# Online presence: ask once, check, confirm, write back

Read this when you enter apply, discover or assess. It turns a candidate's public
profiles (GitHub, Google Scholar, personal website) into confirmed facts in their
master profile, so a CV that lags behind their public work stops costing them.
The design document is kept in the source repository, https://github.com/addsumtech/job-hunt.

Run it before the profile is frozen: in apply before the master fingerprint
(`check_claims.py --record`), in discover before `snapshot_profile.py`, in assess
before `evidence_blocks.py`. A write-back made after that point is checked against
the old master.

## 1. Status, and ask once

```bash
python3 scripts/online_presence.py status --name "<name>" --workspace <ws>
```

It prints JSON: `to_ask`, `stale`, `broken`, `refused`, `malformed`, `other_records`,
`shared_with` and `pending_for_master`, and journals the step (`check_apply.py` and
`check_shortlist.py` print `NOTICE_NO_ONLINE_PRESENCE_STEP` when it is missing).

- `other_records` non-empty and nothing recorded here: ask once whether that
  directory is the same person. If yes:
  `online_presence.py link --name "<name>" --with "<other>" --words "<their answer>"`.
- `to_ask`: ask for those profiles in **one** question (GitHub username, plus any
  organisations or `org/repo` the profile page does not list; Scholar profile URL;
  website URL). Store every answer, including "none" and "rather not":
  `online_presence.py record --name … --source github --status given --value <user>
  --extra <org/repo> … --words "<their words>"`. An answer is recorded once:
  never re-ask a recorded answer unless the user asks to change it.
- `broken` (the last check got 404): show the stored value and ask whether it is
  mistyped; record the correction. That is not a fresh ask.
- `malformed`: the stored answer is damaged (hand-edited, no value). Show it and
  ask the user to correct it; it is not re-asked as a new question.
- A GitHub answer may be a username, `@user` or a profile URL; it is stored as the
  username. Another site or a repository URL is refused: ask again for the username.
- LinkedIn is not a source here, and neither is any page that needs a login.

## 2. Check the stale sources

GitHub is fetched by the script. Scholar and the website are read by you with the
existing browser route, then ingested:

Capture Scholar with `hl=en` and newest first, so the parser can read the table
and new papers are on the first page (the default order is by citations and shows
only 20): append `&hl=en&view_op=list_works&sortby=pubdate` to the profile URL.

```bash
python3 scripts/run_tool.py --browser chrome browser \
    --url '<scholar or website URL>' --output <ws>/raw/online-<source>.json
python3 scripts/online_presence.py ingest --name "<name>" --source scholar \
    --capture <ws>/raw/online-scholar.json --workspace <ws>
python3 scripts/online_presence.py check --name "<name>" --workspace <ws>
```

`check` re-fetches GitHub only when its last check is older than 14 days; pass
`--force` when the user says they just published something. On a host without a
browser, skip the capture: GitHub is still checked.

A refusal (403, 429, captcha, "unusual traffic", a login wall) follows
`references/source-policy.md`: no retry and no other route. This step is not what
the user came for, so it does not hold the mode: name the site and page, offer the
`references/user-recovery.md` hand-off once, and continue the mode without that
source. Never report a refused source as "nothing new": a refused or failed check
stays in `stale` (and `refused`) until a later check succeeds. If `ingest` reports
Scholar as `failed` with "no papers recognised", the page layout was not understood;
say so and look at the capture rather than telling the user nothing changed. A
`warning` (fewer papers read than the page's "Articles 1–N" total, or lines that fit
no row) means the snapshot is partial: say which, and look at the capture.

## 3. Confirm

`check` prints at most four findings (`shown`) and how many more are pending. Show
them in one message with selectable options per finding: add to my profile / not
relevant / add, but correct it. Ask for the user's role on a repository when it
is not obvious. Then record each decision:

```bash
python3 scripts/online_presence.py confirm --name "<name>" --finding <id> \
    --decision confirmed --words "<their words>" [--role "<their role>"]
```

An ignored finding is not offered again unless it changes (a new release is a new
finding). Pending findings come back next run; offer to show them now if the user
wants. Nothing found online reaches a CV, letter or verdict until confirmed.

## 4. Write back

```bash
python3 scripts/online_presence.py writeback --name "<name>" --language <cv language> --workspace <ws>
```

Confirmed repositories become `projects` entries, confirmed papers become
`publications`, and missing profile links go into `contact.links`, written through
`save_profile.py` (dated backup). Tell the user before the first write-back that the
master is reformatted when it is saved: the leading comment block is kept, but
comments inside the body and the original key order are lost (the dated backup
keeps the old file). A link whose last check got 404 is not written. When
`projects` or `publications` is not a list, that finding is left unwritten with a
`skipped_reason`; tell the user to add it by hand or make the field a list. Star, fork and release numbers are never written;
when a CV wants one, read it from the newest snapshot and cite it as a
`fetched-artifact` with its date. An entry the user already wrote is never edited.
Without a master yet, findings wait as `confirmed_unwritten`. `pending_for_master`
lists confirmed findings another language's master still lacks; offer them when
that master is used.

If an apply workspace is resumed after a write-back, `check_claims.py` reports
`MASTER_WRITEBACK`: tell the user what was added, then re-run
`check_claims.py --record`.
