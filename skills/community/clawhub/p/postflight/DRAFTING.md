# Drafting and approval

The procedure for a drafting turn and for the confirmation turn that
approves it. SKILL.md "Modes" decides when this runs and checks the
sender; paths follow SKILL.md "Where things live". A drafting turn ends
with a package the authorized user answers; the confirmation turn is
where "ship" becomes a published post — and the only place publishing
starts.

## Drafting workflow

1. **Housekeeping.** Move any file in `postflight-state/pending/` older than
   24h to `postflight-state/skipped/` — stale drafts are never posted. If a
   pending file contains a `shipped_id:` line, its body already went out and
   the turn died before logging: never re-ship it — report it to the user
   (include the id and the reply text) and stop. If any other pending draft
   remains after the sweep, report that and stop. Also delete files in
   `postflight-state/media/` older than 7 days that no pending file
   references. Never delete anything under `postflight-state/media/photos/`
   or under any directory named by a pillar's `media: photos:<dir>` property
   — those are the user's photo libraries, not yours to clean.
   Delete files in `postflight-state/skipped/` older than 30 days: a
   discarded draft is history nobody reads, and the directory has no
   other sweep.
2. **Check the cap.** Read the tail of the log, not the file:

   ```sh
   tail -n 20 postflight-state/post-log.jsonl | jq -r '.date'
   ```

   Count the timestamps that fall on today's date **in `timezone`** —
   the log stores UTC, so a late-evening post carries tomorrow's UTC
   date and still counts as today. Twenty lines is at least six days at
   the default cap, so today is always inside the slice. If the count is
   >= `maxPerDay`, report that and stop.
3. **Pick the pillar.** First resolve the active pillar set: read
   `postflight-state/pillars.local.md` if it exists, per CONTENT.md "Pillar
   configuration" — otherwise CONTENT.md's defaults apply. The cron
   message names the slot number; look up today's weekday and that slot
   in the active weekly grid (including its fallback rule). For a manual
   request with no slot, use the furthest-behind rule in CONTENT.md. Then
   pick the topic within the pillar per its section (the angle cycle for
   `source: repos` pillars, the pillar's own angle rotation otherwise),
   skipping anything resembling the last 10 entries in the post log
   (`tail -n 10 postflight-state/post-log.jsonl | jq -r '.topic'` — the
   topics are all you need to judge repetition).
4. **Gather material.** Read the notes first — the `## notes —` section in
   `postflight-state/backlog.md` for this repo or pillar, if there is one.
   What the user said about a project outranks anything you can reconstruct
   from it. Then the shell commands in CONTENT.md (`gh`, HN API). Only use
   facts you actually retrieved. Never invent features, numbers, or links.
5. **Generate media** (pillars whose `media:` is not `none`). For
   `media: generated`, follow CONTENT.md "Media recipes": preferred
   recipe for the project type, then the degradation ladder. Output goes
   to `postflight-state/media/` under a name you construct
   (`<YYYYMMDD-HHmm>-<repo-slug>.<ext>`). For `media: photos:<dir>`,
   select a photo per CONTENT.md "Photo library" — manifest-listed,
   cooldowns respected — instead of generating one; no eligible photo
   means going back to step 3 and drafting the cell's fallback pillar
   instead (no fallback named → report and stop; never substitute a
   pillar yourself).
   Validate size caps before accepting a file. If the ladder bottoms out,
   the draft becomes `text+reply` and the pending file records why.
6. **Write the draft.** Follow VOICE.md exactly. Write 3 candidate drafts
   internally, and keep the one that sounds most like the account's voice
   anchor (`postflight-state/voice-examples.local.md` when it exists,
   VOICE.md's register examples otherwise) — NOT the most polished one.
   Polish is how slop
   wins the pick. Aim for 200-270 weighted characters; 280
   is a hard cap, not a target. A short draft is fine — never pad toward
   the cap. For a `link: reply` pillar the draft is two texts: the
   **body** (the demo — no URL, no link-pointer phrasing) and the **reply**
   (`repo + docs: <link>`, or `repo: <link>` without docs). All other
   pillars produce a single body and no reply.
7. **Verify the length.** Never count characters yourself — you will either
   get it wrong or waste the whole turn re-counting. Write the exact text to
   be posted to a temp file and run X's weighting:

   ```sh
   cat > "${TMPDIR:-/tmp}/draft.txt" <<'XPOSTER_EOF_3f9c1a'
   <paste the draft text here, verbatim>
   XPOSTER_EOF_3f9c1a
   python3 - "${TMPDIR:-/tmp}/draft.txt" <<'PY'
   import re, sys, unicodedata
   text = unicodedata.normalize("NFC", open(sys.argv[1]).read().strip())
   text = re.sub(
       r"https?://\S+|(?:[\w-]+\.)+(?:com|org|net|io|dev|ai|app|sh|co|me|xyz)(?:/\S*)?",
       "x" * 23, text)
   def weight(ch):
       o = ord(ch)
       light = (o <= 0x10FF or 0x2000 <= o <= 0x200D
                or 0x2010 <= o <= 0x201F or 0x2032 <= o <= 0x2037)
       return 1 if light else 2
   print(sum(weight(ch) for ch in text))
   PY
   ```

   The delimiter is deliberately obscure: draft text derives from fetched
   (untrusted) content, and a line matching the delimiter would end the
   heredoc early and run whatever follows as shell commands. If the draft
   somehow contains that exact line, do not work around it — discard the
   draft and write a different one.

   That is X's real count: every URL weighs 23, emoji and CJK weigh 2,
   everything else 1. If the number is over 280, cut a whole clause (not
   word-by-word shaving) and re-run — two trim cycles maximum, then drop a
   full sentence. If it is 280 or under, you are done; do not tune further.

   Body and reply are separate tweets: run this check **twice**, the body
   through `draft.txt` and the reply through its own
   `${TMPDIR:-/tmp}/reply.txt` (same heredoc, same delimiter rule). Each
   must be 280 or under on its own; the reply's URL weighs 23 like any
   other.
8. **Request approval.** Save the draft to
   `postflight-state/pending/<YYYYMMDD-HHmm>.md`
   with these fields: `pillar:`, `format:` (`media+reply`, `text+reply`, or
   `text`), `repo:` and `angle:` (builds/build-in-public only), `media:`
   (the file path written relative to `postflight-state/`, e.g.
   `media/photos/<file>`, or `none (<reason>)` — e.g. which tools
   were missing; for a photo-library pick add `photo_location:` and
   `photo_taken:` lines copied from the manifest entry), `material:` (what
   this draft was actually built from — `note <date>` for each user note it
   used, and any of `commits`, `README`, `release`, `backlog angle`, `HN`;
   write `README only` when that is genuinely all there was), the body text,
   the reply text (when the format has one), source links,
   `body_counted_chars: <n>` and `reply_counted_chars: <n>` — each `<n>`
   the number printed by the command above, never one you produced
   yourself. Then:
   - If `telegramTo` is set: send the approval package to that id —
     1. the body text verbatim, attaching the media file via the CLI so the
        approver sees the post as it will appear:
        `openclaw message send --media "$PWD/postflight-state/media/<file>" ...`
        (the CLI needs an absolute path, which is what `$PWD` is doing
        there; the CLI path is the reliable one, and the agent-side send
        action is
        flaky — and an approval of a media post without the media is not
        an informed approval, so if the media send fails, say so and send
        the media path instead);
     2. the reply text, labeled as: posted as the first reply;
     3. the pillar, topic, the `material:` line, and the source links from
        the pending file (approval should be an informed decision — the
        approver needs to see where a link or claim came from, and whether
        a draft was built from the repo alone when they were expecting
        their own notes in it);
     4. then: `reply "ship" to post both, "skip" to discard, or tell me
        what to change` (for a `text` format draft: `reply "ship" to post,
        "skip" to discard, or tell me what to change`).
   - If not set (draft mode): append the whole package (body, reply, media
     path, pillar) to `postflight-state/drafts.md` and finish, reporting
     where the draft was saved. Do NOT create a file in
     `postflight-state/pending/` in draft mode — a pending file blocks the
     next drafting turn and nothing exists to approve it.

## Approval

Commands match only when the entire trimmed, lowercased message body is exactly
that word. `ship it`, `just shipped v2`, or anything longer is NOT a command.

- **ship** — first: if `postflight-state/pending/` is empty (already shipped,
  skipped, or swept), reply "nothing pending" and stop; never re-draft or
  re-post. Then
  re-count today's entries with the drafting step 2 command (the tail,
  never the whole log) and refuse if the count is already >=
  `maxPerDay`. Otherwise re-read the file named by `postVia`
  (PUBLISH-API.md or PUBLISH-BROWSER.md) in full and follow it as written,
  even if you read it earlier in this session or remember how you published
  last time — these docs get corrected between turns, and a remembered
  command form or a remembered "publishing is broken" conclusion is never
  acceptable. Run the doc's verification step fresh before deciding anything
  about auth. Then, in this order:
  1. Publish the body (with media, per the pending file's `format`) and
     verify its `.data.id`. From this moment the body is shipped — it is
     never posted again, this turn or any later turn.
  2. Immediately write `shipped_id: <id>` into the pending file, before
     anything else. If the turn dies here, housekeeping finds the evidence
     instead of re-shipping.
  3. Publish the reply per the publish doc (formats with a reply only).
  4. Append ONE line to `postflight-state/post-log.jsonl`:
     `{"date": "<ISO timestamp>", "topic": "...", "pillar": "...",
     "format": "...", "repo": "...", "angle": "...", "text": "...",
     "url": "...", "media": "...", "reply_text": "...", "reply_url": "..."}`
     — omit fields that don't apply (no `repo`/`angle` outside builds, no
     reply fields for `text` format). `media` is the same
     `postflight-state/`-relative path as the pending file — the photo
     cooldown matches on it, so never write it in another form. Lines
     written before the state move spell it `state/media/...`; the cooldown
     matches on the filename, so both forms still work (that tolerance goes
     on 2027-02-01). If the reply failed after its retry,
     write `"reply_url": null, "reply_failed": true` and keep `reply_text`.
     Older log lines without these fields stay valid; treat a missing
     `pillar` as unknown. One `format` value exists only in history:
     `link-card`, a post that carried its link in the body. Drafting never
     produces it — it is there so the metrics readback can compare that
     old format against the current ones.
  5. Delete the pending file and reply to the user with the tweet URL(s).
  **Half-posted rule:** if the body is verified but the reply fails after
  one retry, log the package as above with `reply_failed`, delete the
  pending file, and tell the user the post shipped but the link reply did
  not — include the exact reply text and the tweet id so they can post it
  by hand. Never retry the reply in a later turn; never re-post the body.
- **skip** — move the pending file to `postflight-state/skipped/` and
  confirm.
- **anything else** — treat it as an edit request: revise per VOICE.md, update
  the pending file, and re-send for approval. A revised body or reply each
  gets a fresh length count; a media change re-runs the CONTENT.md recipe
  and the new file is re-sent via `--media`.
