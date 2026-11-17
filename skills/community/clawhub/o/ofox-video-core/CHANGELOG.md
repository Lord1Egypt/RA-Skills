# Changelog

All notable changes to the **ofox-video-core** skill. Versioning follows SemVer.

This file starts at 1.2.0; earlier versions predate it.

## 2.0.3 — video-reference behavior now has a known-answer test

The video-reference documentation now reflects two artifact-level Seedance
2.5 measurements instead of the earlier inconclusive motionless-cup run. On a
four-beat synthetic control, one job preserved composition order, motion
directions and the three exact hard boundaries while changing the treatment;
a second began from the final state and continued into new space without
replaying the earlier layouts. Both 4-second / 480p `byteplus` dry-run quotes
matched their 56-cent bills.

The input contract is narrower and now tested: a small video data URI reaches
the client payload but the current route rejects it before job creation, so a
public web URL is required. The existing `frame_images` plus
`input_references` refusal is stated explicitly as a shipped-client boundary,
not generalized into a claim about direct API calls. The new
`previs-rerender` scenario skill owns the prompt and manual-review workflow.

## 2.0.2 — one authoritative multi-image reference recipe

The shared prompt guide now owns the complete `input_references` recipe:
canonical `@imageN` labels, array-order binding, one “supplies / ignore” role
sentence per asset, and a payload check before spending. It states the actual
evidence boundary—two images measured once, three or more untested, nine the
API ceiling—and explicitly rejects treating an 18-image gallery case as a
reproducible one-job example. The obsolete claim that position mapping was
unverified is removed.

## 2.0.1 — expired 1080p promotion no longer under-quotes offline

Seedance 2.5's 1080p promotion ended: the public catalog now reports $0.60/s
for t2v and $0.71/s for v2v, replacing $0.48/s and $0.568/s. The bundled
pricing snapshot and dated pricing reference now carry the live rates, so an
offline dry run no longer approves a bill below the current catalog price.

The pricing test no longer copies external rate constants. It reads the
fresh catalog cache when available and the generated bundled snapshot when
offline, then checks that the estimator agrees with that source. Future
repricing therefore exercises the estimator instead of failing on a stale
number handwritten into its own test.

## 2.0.0 — spending needs `--approved`

**Breaking.** Every command in this repo, and in every skill built on it, that
actually generates a video now has to carry one more flag. That is a change to
the command-line contract rather than to any behaviour behind it, which is what
a major version is for; calling it a minor bump would mean callers discovering
it from an error instead of from this file.

### What a caller has to do differently

**Add `--approved` to every real run of `generate`, `create`, `batch` and
`chain`.** Without it the command prints what to do and exits **1**, having
submitted nothing and billed nothing.

```bash
# before
bash references/ofox-video.sh generate --prompt "..." --duration 8 --resolution 720p
# after
bash references/ofox-video.sh generate --approved --prompt "..." --duration 8 --resolution 720p
```

`--dry-run` does **not** take it and never will: the quote is how the number
being approved gets produced, so a gate in front of it would close the only
route through itself. `batch` and `chain` forward the flag to each take/shot,
so it is written once per command, not once per job.

Nothing else is gated. `check`, `models`, `providers`, `contact-sheet`,
`last-frame`, `frame-at`, `mux-audio` and — deliberately — **`poll`** all run
exactly as before. `poll` is the command that collects a job you have already
paid for, and it is what this script prints as the recovery step whenever a run
is refused, times out or is interrupted; gating it would strand money rather
than protect it.

**Scenario skills still document the old commands.** Their examples are being
updated in their own next versions. Until then, an example copied out of
`shorts-reels`, `ugc-ads`, `product-demo`, `keyframe-animation`,
`talking-head`, `music-video`, `explainer`, `image-edit`, `product-image`,
`video-extend-edit` or any `seedance-*` skill needs `--approved` appended by
hand. The command is otherwise unchanged.

### Why

ClawHub's registry scan reported it, and the report was right: the approval
gate was written down in `references/approval-gate.md` as a rule an agent
should obey, and the script did not check anything. The rule is unchanged; it
now has a hook in the tool.

### What the flag does and does not do

It **records a stance. It cannot prove one.** No shell script can observe the
conversation between an agent and its user, and an agent can pass `--approved`
without ever showing anyone a price — exactly as it could previously just run
the command. What changed is that spending without quoting is no longer the
default: it has to be typed into the command, where a transcript shows it and a
reviewer can object to it.

This changelog, `SKILL.md` and `references/approval-gate.md` all say that in
those terms on purpose. "Approval is now enforced" would be a claim about the
world made from evidence that only supports a claim about the command line.

### Where the guard sits, and one behaviour change that follows

The refusal happens at the last free instant: after arguments are parsed, after
every parameter is validated against the model, after the provider is resolved
and after the estimate is printed — immediately before the one `POST` in this
script. Two consequences worth knowing:

- a wrong `--duration` is still reported as a wrong `--duration`, not as a
  missing approval, so nobody learns "add `--approved`" as the way past a
  parameter error;
- the refusal carries the `Estimated cost:` line with it, which is the number
  the user has to be shown anyway.

To keep that ordering true for `batch` and `chain`, both now run their
single-take/single-shot validation pass (the one `--dry-run` has always done)
on the **real** path too, before the gate. It sends nothing and costs nothing;
the visible difference is that a bad parameter is reported before
`--- creating take 1/N ---` rather than inside it.

### Tests

New suite: `references/test/approval.test.sh` (41 checks). It derives the
subcommand list from the script's own usage text, runs all twelve without the
flag, and asserts the split is exactly 4 gated / 8 free — so a subcommand added
later that reaches the billable request without a guard lands in the wrong set
and turns it red. Two defects are planted in throwaway copies and both are
confirmed to change the outcome: neutering `require_approved` makes an
unapproved `generate` run straight to the create call, and removing `batch`'s
forwarding makes an approved batch break at take 1.

Existing suites were updated where a case has to reach the request to be about
anything; `expect_reject` in `validation.test.sh` deliberately still runs
without the flag, so the gate preempting validation would show up there.

## 1.30.0 — the API key goes to one host, and the escape hatch cannot rewrite what you approved

Four guards, all of them narrowing capabilities this script really had. None
of them removes a capability; each one names the smaller shape it now has.
New suite: `references/test/keyguard.test.sh` (55 checks), which constructs
the refused input for every rule rather than watching a good input pass.

### The polling URL out of the create response is no longer followed off-host

`POST /videos` returns a `polling_url`, and the poll loop sends
`Authorization: Bearer $OFOX_API_KEY` to it. Until now that URL was used
verbatim, so **a tampered or misconfigured API response was enough to redirect
the key to a third party** — the only path here that needs no compromised
local environment at all.

It is now followed only when its `scheme://host:port` matches `API_BASE`.
Also refused: a URL whose authority hides the real host behind userinfo
(`http://api.ofox.ai@evil.example/…` is `evil.example`), a different port, a
different scheme, and anything that is not an http(s) URL.

**What a caller has to do differently:** nothing, unless the response really
does point elsewhere. The field is still used when it is on the configured
host, and the `API_BASE/videos/<id>` fallback when the field is absent is
unchanged. If it *is* refused, `generate`/`create` exits **3** with the job id
still on stdout, the request handoff saved, and the recovery command printed —
the job exists and is billable, so it is collected with
`ofox-video.sh poll <id>`, not abandoned and not re-created. `poll` builds its
URL itself and never reads one from a response.

The same check also sits inside `poll_and_download`, next to the request that
would leak rather than only next to the place the URL came from.

### `OFOX_API_BASE_URL` must be https, and an override is announced

Still supported — pointing a run at a staging deployment is a legitimate use
— but it decides which host receives the key, so:

- a non-`https://` base is refused (exit **2**) unless the host is loopback
  (`localhost`, `127.0.0.1`, `[::1]`), which keeps local test servers working;
- a value that is not an http(s) URL at all is refused (exit **2**);
- when it is set, a `NOTE:` on stderr names the host that will receive the
  key. **Relay that line** — it is the difference between "we are talking to
  Ofox" and "we are talking to whatever that variable says".

Checked for `check`, `models`, `providers`, `generate`, `create`, `batch`,
`chain` and `poll`. The four local tools (`contact-sheet`, `last-frame`,
`frame-at`, `mux-audio`) are deliberately excluded: they run ffmpeg over a
file you already have, send nothing, and refusing them over a variable that
cannot affect them would be overreach.

### `--extra-json` cannot overwrite a field that has a flag

It is merged **last** and its keys **win**, and the cost estimate is printed
**before** the merge. So `--duration 4 --resolution 480p --extra-json
'{"duration":30,"resolution":"1080p"}'` quoted 44 cents and would have
submitted a job billing about 7 dollars, having skipped every per-model check
on the way.

Refused now (exit **1**, before any request): `model`, `prompt`, `duration`,
`resolution`, `aspect_ratio`, `size`, `generate_audio`, `seed`,
`real_person`, `callback_url`, `frame_images`, and `provider.type`. The error
names the flag to use instead.

**What a caller has to do differently:** move those keys onto their flags.
Everything without a flag still passes through — `input_references` unchanged,
and **`provider.options` still works**: only `provider.type` is refused, so
`{"provider":{"options":{…}}}` merges alongside the pinned type rather than
replacing it.

### An explicitly empty `--extra-json` is an error (the 1.29.0 defect, closed)

1.29.0 documented this and deliberately left the behaviour alone. It is fixed
now, and the fix is narrow: the script records whether the flag was **written
on the command line**, which is the one thing bash cannot recover from the
value. Omitting `--extra-json` is byte-for-byte what it always was — asserted
by comparing the built payload against `--extra-json '{}'` — and only the
explicitly-empty spelling, which was never anything but a failed command
substitution, is refused.

**What a caller has to do differently:** an `--extra-json "$(jq …)"` whose
`jq` died on `ARG_MAX` now exits 1 instead of submitting a fully billed job
with none of your references in it. The `ARG_MAX` wall itself has not moved:
keep an encoded reference small (a 768 px long edge is tens of kilobytes) or
use `--frame-first-image`, which encodes through a temp file.

Two smaller things in the same area, both fail-open cases that could empty the
request body:

- `--extra-json` must be a JSON **object**. It is merged with jq's `*`, which
  is undefined between other types; a non-object made the merge fail, the
  command substitution yield an empty payload, and an empty body go out.
- validity is now checked with `jq empty` rather than `jq -e .`, which keyed
  its exit status on the *output value* and so called a perfectly valid `null`
  or `false` "not valid JSON". Both are still refused, by the object rule,
  which says what is actually wrong with them.

### The shared references now give the same recovery advice the scenario skills do

`references/approval-gate.md` and `references/creative-brief.md` each end their
"if this link didn't resolve" paragraph with an install command, and both still
said `npx skills add ofoxai/skills` — the whole repo. The 14 scenario skills
were narrowed in the same uncommitted change to ask for the **one** missing
skill and to hand the command to the user rather than run it, so the repo was
telling an agent two different things about the same situation depending on
which file it happened to read. Both now match: one skill, three routes
(skills.sh / `npx ofox-skills` / LobeHub-ClawHub), the user runs it.

No behaviour change. It is here because a rule that lives in two places drifts,
and this is the drift — the extraction convention in
`.trellis/spec/skills/index.md` exists precisely to keep these paragraphs in
one voice.

## 1.29.0 — an oversized `--extra-json` drops your references and bills you anyway

**Documentation only. No script, flag, default or guard changed** — and the
`ofox-video.sh` empty-`--extra-json` behaviour is deliberately left alone; see
the last paragraph.

1.28.0 documented `input_references` as working and noted that an image
reference accepts a `data:` URI, so no hosting is needed. True, and
incomplete in a way that costs real money. Measured 2026-09-17:

> Building that `data:` URI into `--extra-json` yourself passes it to `jq` as
> a **command-line argument**, so it is bounded by `ARG_MAX` (1,048,576 bytes
> here). Over the limit `jq` never executes — the shell writes one line to
> stderr, the command substitution yields an **empty string**, and
> `ofox-video.sh`'s `if [ -n "$extra_json" ]` guard treats an empty value as
> *not passed*: no JSON validation, no `references_conflict` check, and
> **nothing merged into the body**.

Reproduced with a 1.9 MB PNG (2,515,046-byte URI): **no `input_references` in
the printed payload, `STATUS dry_run`, exit `0`.** Without `--dry-run` that is
a submitted, fully billed **plain text-to-video** job that the caller believes
is reference-to-video — and the clip looks exactly like a model ignoring the
references.

**What a caller has to do differently:**

- **Stop treating "no error" as "the reference arrived."** There is no error.
  The single stderr line comes from the shell, not this script, so it carries
  no prefix and scrolls past above the normal output.
- **Downscale the image before encoding.** The measured r2v job's two
  references were 33 KB and 43 KB at a 768 px long edge.
- **Build the JSON into a variable, assert it is non-empty and parses**, then
  **`--dry-run --print-payload` and confirm `input_references` is really in
  the payload.** That last check is the only one that detects this. The guard
  to copy is in `references/api-params.md`.
- ⚠️ **Do not generalise from `--frame-first-image`, which is safe.** There
  the script encodes through a temp file and `jq --rawfile`; re-verified the
  same day on the same 1.9 MB PNG, whose full 2,515,046-byte URI really does
  reach the payload. **The two paths behave in opposite directions at the same
  file size.**

**A correction to this skill's own history, in `SKILL.md`.** The 2026-08-29
ARG_MAX write-up says the old `jq --arg` code failed "before any network call
was made". What was actually recorded is a **stderr line**, not an exit
status — nobody wrote down whether that run aborted or carried on, and the
new measurement shows a visible `Argument list too long` is entirely
compatible with the command continuing and succeeding. The sentence now says
what was observed and flags that "ARG_MAX fails loudly and stops you" is not
a safe general reading.

**Not done on purpose:** hardening `ofox-video.sh` so an empty
`--extra-json` is rejected rather than ignored. Treating empty as "not
passed" is long-standing behaviour something else may depend on, so it is a
separate decision rather than a fix smuggled into a documentation change.

## 1.28.0 — `r2v` works and the catalog omits it; `mode` is accepted and discarded

**Documentation only. No default, price, script or behaviour changed.** Three
measurements from 2026-09-16/17, one of which upgrades an inference this repo
had been repeating as if it were a finding.

**Callers who need to change something:**

- **If you told a user "Ofox does not support extend / edit", re-word it.** It
  is not a rejection they can catch. Job `4686f434-16b0-451f-8941-970e5b3d4a15`
  sent an invented `mode` value inside an ordinary text-to-video request and
  got `200`, a completed 4-second t2v clip, and a normal $0.44 t2v bill. The
  field is **accepted and discarded**. There is no error code, so anyone
  debugging against one will search forever. `references/api-params.md` has
  the wording to use and the three free probes that could not settle it alone.
  `duration: -1` — the gallery's input-locking form — returns `502
  route_error` instead, before any URL is fetched.
- **If you assumed `input_references` images were untested, they are not.**
  Job `0f5c8b4e-8813-40d2-a6bd-9e2d030b6d1e`, two images as `data:` URIs, 44
  cents: both references' features came through and the `image1` / `image2`
  position tokens resolved **in array order**, which had been this repo's one
  unverified point about that shape. It bills at the **plain t2v rate**, not
  the dearer video-to-video rate a `video_url` moves a job to. And an image
  reference accepts a `data:` URI, so nothing needs hosting first.
- **Do not read the catalog's `modes` column as a capability list.** It says
  `t2v i2v v2v` on every model and reference-to-video demonstrably works. Only
  `modes` is affected — the duration, resolution and aspect-ratio columns the
  script enforces against have held up. `models-snapshot.json` is **not**
  hand-edited for this; it is regenerated from the live catalog, so the
  correction lives in the docs.
- ⚠️ **Pass `--aspect-ratio` explicitly when you send image references.** That
  one job, with no flag and two 16:9 **landscape** references, delivered
  **480x854 portrait** — following neither the default nor the references.
  `frame_images` does not behave this way. One observation, no explanation
  offered, recorded as an anomaly rather than a rule.
- **New in `references/prompt-structure.md`: an attached first frame whose
  background disagrees with the written SCENE produces about 0.1s of the
  supplied picture and then a hard cut** (job `ede33e6d`, background
  brightness 250 through 0.08s, 33 from 0.12s). Three runs make a controlled
  set: two where the frame and the SCENE agreed showed no cut, the one where
  they disagreed did. Any scenario skill using `--frame-first-image` should
  either write the SCENE the photo is in or trim the opening 0.15s.

## 1.27.1 — one sentence in the shared file still said the frame route was closed

**Documentation only. No default, price, script or behaviour changed.**

1.27.0 corrected `references/prompt-structure.md` where it lists the API
constraints, but missed the words route's own introduction eighty lines
earlier: "This is the only route open when the subject is a photoreal person,
since image-to-video refuses those frames outright." The same file now says,
correctly, that `--real-person true` lifts that refusal — so the file
contradicted itself, and the sentence a scenario skill is most likely to read
was the stale one. It now says the frame is refused *unless the caller
asserts the rights to that likeness*, which is an authorisation nobody can
give on a user's behalf, and points at the constraints section for the rest.
The words route is still the route to reach for; what changed is the reason
given for it.

Found by a sweep for **absolutes** rather than for the word "untested" — this
sentence contained no hedging word at all, which is why two previous searches
walked past it.

## 1.27.0 — `--real-person true` works on 2.5, and "no way to check for a phantom job" was false

Three measurements from 2026-09-16 land here, and two of them correct claims
this skill had been repeating.

**`--real-person true` lifts the real-person refusal on `bytedance/seedance-2.5`.**
Every skill in this repo said this was untested on 2.5. It was tested as a
single-variable A/B — the same synthetic portrait, prompt, parameters (4s,
480p, i2v) and upstream (`byteplus`), differing only in the flag. With it, job
`28eee177-1eab-4852-a72f-d6a2de695672` completed, seed `311954977`, billed 44
cents, and delivered the person in the portrait. Without it, `HTTP 400
input_moderation_failed`, "may contain real person", unbilled. The control is
what makes it evidence: an accepting run on its own is equally well explained
by "that portrait never tripped the classifier", and those two explanations
look identical. This repo has already shipped one claim whose measurement
tested the other proposition (see the Seed entries), which is why the control
was run and why it is written up first.

**The wording is load-bearing and is now fixed in one place.**
`references/api-params.md` gains
"`--real-person true` lifts that refusal on 2.5 — for references you are
authorized to use", and that section is what scenario skills link instead of
paraphrasing. Ofox's own error text calls the flag "privacy-preserving
preprocessing for **AUTHORIZED** real-person references" — so it is an
**authorization mechanism, not a moderation bypass**, and the section says
outright never to offer it as a way past the check, never to use it as a
reflex retry after `input_moderation_failed`, never to set it on a user's
behalf, and never for a public figure. Setting it on material nobody has the
rights to does not make the use legitimate; it makes a false assertion and
generates the clip anyway, which is worse than a refusal.

What the run does **not** establish is listed as prominently: one upstream
(`byteplus`; `volcengine` untested), one tier and mode (480p, 4s, i2v with a
single first frame), one content class (a *synthetic* portrait — an actual
photograph of an actual person is untested), likeness fidelity under the
preprocessing (unmeasured above 480p), and one model.

The same framing is applied everywhere the old wording lived: the
`real_person` row of the parameter table, the `chain` section's "one hard
limit", the key-flags list, `prompt-structure.md`'s frame-semantics bullet,
and — most importantly — **the script's own `input_moderation_failed`
message**, which is what an agent reads at the exact moment it is tempted to
retry. That message now opens option 2 with "ONLY if the user holds the rights
to this person's likeness and has said so", and closes it with "a declaration
of authorization, NOT a retry flag — do not set it to clear this error".

**`GET /v1/videos` returns HTTP 200 and a job list — so a phantom job is now
diagnosable from the terminal.** This skill's answer to an ambiguous create
failure was "check the dashboard", because a probe had found `/v1/credits`,
`/v1/account` and `/v1/usage` all 404 and the conclusion drawn was that
nothing could be queried. `/v1/videos` had not been tried. It works, with the
key, and each entry carries `created_at`, `id`, `model`, `prompt`, `status`,
`unsigned_urls`, `updated_at` and `usage`. (`/v1/jobs` is still 404.)

`SKILL.md` gains "The recovery step: list the jobs, compare, then decide",
`api-params.md` gains a `GET /v1/videos` section, and the exit-`5` row and the
script's own exit-`5` message now print the listing command instead of only
pointing at the browser. **The no-resubmit rule itself is unchanged and is not
weakened by this** — the reason never to blind-retry was that nobody could
tell whether a job existed; now somebody can, so "don't guess" becomes "go and
find out, then act on what you found". That is exactly how the 2026-09-16 case
was settled: a create died on `curl (35)` with no HTTP response, the script
exited `5` and refused to guess, the list's newest entry was still hours old,
and the retry went ahead knowing rather than hoping.

Two smaller corrections follow from the same endpoint. "The API has no list
endpoint, so a short id cannot be expanded" was stated in both `SKILL.md` and
`api-params.md`; a downloaded file's 8-hex stem is a prefix of a real `id`, so
a recent job can often be recovered by listing and matching. That is a rescue,
not a record — the sidecar's full `job_id` is still the thing to rely on. And
the list is **not** a billing endpoint: per-job `usage` is not an account
balance, and `ofox-image-core`'s "no billing endpoint" finding stands.

**Content is irreproducible; dimensions are not. The two are now kept apart.**
The same 720x480 (3:2) frame delivered **794x530** in two independent
`bytedance/seedance-2.5` 480p jobs (`35b6aed1`, `69bc799d`). The standing
finding that a fixed seed does not reproduce a clip is about the **picture**
and is untouched; output size comes from the resolution tier and the frame's
ratio, and an editor planning a join can rely on it. Stated under both "A
fixed seed does not make this API reproducible" and the Seed section of
`api-params.md`, in each case so that neither sentence can be read as
undermining the other.

**Transport flakiness is now stated as a property of this API.** Three more
`curl (35)` events in the 2026-09-16 session — one on a create, two on polls —
bringing it to six across four days. Both halves of the script behaved
correctly every time: polls retried the poll and completed, the create refused
to guess. Six events is enough to say that neither the no-resubmit rule nor
its new recovery step is over-engineering.

Documentation and two stderr messages (the exit-`5` create failure and
`input_moderation_failed`); no change to request building, polling, validation
or pricing. All 13 test suites pass unchanged.

## 1.26.0 — a templated prompt in a shots file was five jobs, and the estimate looked fine

`--shots-file` is one prompt per **line**. `references/prompt-structure.md`
teaches prompts written across **several** lines — `STYLE:` / `SUBJECT:` /
`SCENE:` / `CAMERA:` / `CONSISTENCY:` / `SOUND:` / `AVOID:` and a timestamped
body — and every scenario skill built on this one writes them that way.
Nothing anywhere connected those two facts, so an author following this
repo's own craft guidance into this repo's own file format had their prompt
shredded into fragments, each fragment billed as a full-length job.

Found by a blind router test today and then reproduced directly: a 5-line
single prompt printed `Chaining 5 shots` and
`Estimated cost: ~$34.80 for 5 takes (29s x $0.24/s x 5)`. With the 9-line
template `music-video` teaches, one prompt is nine jobs.

**What made it survive review is that nothing goes wrong.** A fragment is a
valid prompt, so there is no crash and no error; the shot count is right there
in `--dry-run`, and the price it sits next to is arithmetically correct for
the shots the script believes it has. The only tell is a number a reader has
to already be suspicious of.

**The guard.** A shots-file line that opens with an ALL-CAPS label —
`^[A-Z][A-Z ]*:` — is refused. It fires while the file is being parsed, so it
lands **before the estimate is printed and before anything is submitted**,
the same placement as the ffmpeg pre-check and for the same reason. The
message names the offending line and its line number, says in one sentence
what the file format actually is, and gives the way out: one `--shot` per
prompt, which takes a multi-line value as a single prompt.

**What it deliberately does not do:**

- **It does not re-join the lines into one prompt.** That would be guessing at
  someone's intent with their money, and a wrong guess buys a 29-second job.
  Stopping is the whole fix.
- **It does not narrow the pattern to a known label list.** Any leading
  `[A-Z ]+:` trips it, which means a genuine one-line prompt opening with a
  label (`CLOSE UP: a mug on a table`) is refused too. That asymmetry is
  chosen: a false positive costs one edit to the command, a false negative
  costs a job per line. Digits end the label, so `SHOT 1: ...` is not caught.
- **It does not touch `--shot`.** Checked rather than assumed: a repeated
  `--shot "multi\nline"` is one argv element and reaches the payload as one
  `prompt` with embedded newlines (verified with `--print-payload`). There was
  nothing to fix on that path, and validating it would have broken the
  documented way out.

**Why a minor rather than a major**, since the guard rejects input that used
to be accepted: nothing it rejects could have been what the caller wanted. A
shots file of template labels has never produced a usable sequence — it
produced N billed fragments — and a file of real one-line prompts, which is
what the flag is for, is unaffected. The strict-SemVer reading is defensible;
this is recorded here rather than argued away.

Also in this release, from the same blind test: **`last-frame`'s step-back is
now a number.** `SKILL.md` said it grabs a frame "just before the end", which
left a tester unable to tell a user what the resulting seam would be. Read out
of `extract_last_frame` and then measured on a 2.000s clip at 10fps: the
normal path seeks to `duration - 0.1s` (duration from `ffprobe`) and takes the
first frame at or after it — the frame at 1.9s on that clip. The `-sseof -0.5`
branch is a **fallback**, reached only when ffprobe reports no duration or
that seek yields no frame, and it returns the first frame of the final half
second — 1.5s on the same clip. Both figures are in `SKILL.md` and both are
now asserted in the suite, because a number in a doc that nothing checks is
the kind that drifts.

Tests: `references/test/chain.test.sh`, 18 checks to 28. The guard cases
assert the refusal exits non-zero, names the offending line, offers `--shot`,
prints no estimate, and submits nothing; plus that the pattern does not eat
`SHOT 1:`, a lowercase label or a mid-sentence colon, and that a multi-line
`--shot` still resolves to exactly one job. Free by construction, as ever.

## 1.25.0 — two local subcommands, for the two things the API will not do

`frame-at VIDEO --at SECONDS` and `mux-audio VIDEO AUDIO`. Both are local
ffmpeg work in the shape `last-frame` and `contact-sheet` already had: no API
call, no key, no cost, and an ffmpeg check that fires **before** anything else
happens rather than half way through.

They exist because two things this API is documented as offering turned out
not to be offerings, and both gaps have a local answer:

- **`frame-at`** — a video reference cannot extend a clip past one job's
  duration ceiling, and must be a hosted URL besides. Extending a clip you
  already have therefore runs through a frame, not through `input_references`.
  `last-frame` covers "carry on from the end"; `frame-at` covers "re-shoot
  from second 3.2", which is the same mechanism pointed at a chosen moment.
- **`mux-audio`** — an `audio_url` reference is parsed, validated and fetched,
  and the delivered clip still carries a model-generated track (measured
  2026-09-15, job `d8561509`, 55 cents). So putting a specific track on a clip
  is a local mux, and this is now the only place that claim lives as code.

Three decisions inside them worth naming, each because the alternative was
silent:

- **`--at` is required, not defaulted.** The frame it writes is usually about
  to be fed to a paid image-to-video job, so a guessed timestamp buys a job of
  the wrong picture.
- **A timestamp at or past the end is an error naming the clip's real
  duration.** Left to ffmpeg it writes nothing and returns success, and the
  caller finds out by paying for a job with a missing frame.
- **`mux-audio` replaces the clip's own track rather than mixing**, and when
  the two inputs differ in length by more than half a second it says which one
  was cut and by how much. It still writes the file — truncating someone's
  music is worth a note, not a failure.

Tests: `references/test/localtools.test.sh`, 32 checks, free by construction —
no socket is opened and no key is read. Fixtures are synthesized with lavfi at
run time, so the suite carries no binaries.

## 1.24.0 — naming where the camera is puts the camera in the shot

One measurement, documentation only — no script change, no flag change.

`references/prompt-structure.md`'s `Camera language` → `Camera movement`
section now carries a ⚠️ under the `Phone POV` row: **a filming device given
a position in the room is rendered as an object in the room.** Measured
2026-09-15 on job `2ecbedec` (`bytedance/seedance-2.5`, 8s, 480p, 88 cents),
whose capture line read *"the phone is propped against a biscuit tin at the
back of the desk, slightly too low and a little off-square"*. The delivered
clip has a phone sitting in the box, visible in every frame, with a small
glowing screen — which also broke that same prompt's own `no legible text`
clause. The model has no concept of an off-screen camera; a noun with a
position is set dressing, and set dressing is rendered.

What the entry adds beyond the finding:

- **The gallery quotes in that row and in `Static / locked` are flagged as
  evidence of practice, not as safe wording.** `sometimes propped on gym
  equipment`, `as if a friend casually left a phone recording on a nearby
  bench` and `static phone propped on bathroom sink` are all the failing
  construction. They stay — they are what authors really wrote — but a reader
  is now told to take the viewpoint from them and drop the prop.
- **A split that makes it decidable**: a phone named as *how the image was
  made* (`real phone capture texture`, `selfie viewpoint`) is a format anchor
  and is safe; a phone named as *a thing at a place* (`propped against a mug`,
  `on a tripod`, `wedged on a shelf`) is scene content and renders.
- **A mechanical conversion** rather than a deletion, because the construction
  is doing real work — it is how imperfect framing, autofocus hunting and
  exposure shifts get conveyed: `the phone is propped against a mug at the
  back of the table, slightly too low` becomes `a fixed viewpoint from the
  back of the table, at mug height and a little too low`.
- **Back it in the negative list as objects** — `a phone, a camera, a tripod
  or a lit screen visible anywhere in the shot` — the form already measured to
  hold in `Unwanted text is designed out of the set, not forbidden in the
  list`.
- **The note that nothing catches this before delivery.** That prompt passed
  `--dry-run` and `--print-payload`; neither can see a rendered object. Only
  the extracted frames could.
- A second, shorter pointer under `Camera position / angle`, because two more
  quoted cells are the same construction and sit in a different table:
  `locked on a tripod at eye level` (case 41) and `propped camera` in the
  shot-numbering row (case 36). Both name equipment standing in the room.

**Blast radius**: `ugc-ads` owned the failing template (its `DEVICE:` slot is
now `CAPTURE:`) and `seedance-ad-creative`'s UGC-variant table carried the
same construction in a row of its own. Both are updated in the same change.

## 1.23.0 — the seed does not reproduce a take, and an audio reference is not a voice input

Two measurements, both paid, both correcting something this skill shipped as
fact.

### A fixed seed does not make this API reproducible

Since 1.16.0 this skill has said, in `SKILL.md`'s "Reproducing a shot", in
`references/api-params.md`'s Seed section, in the `batch` seed bullet and in a
comment in the script itself, that **the seed reproduces a take when the
prompt is byte-identical**. That sentence was never tested. It is false.

Measured 2026-09-15 — `bytedance/seedance-2.0-mini`, 4s / 480p / 16:9, seed
`424242`, one byte-identical prompt, three submissions:

| Job | Outcome |
|---|---|
| `2e45464c-9ea7-4836-96dd-93dffb5ef58d` | completed, 8 cents |
| `cf877512-3faf-42b5-92ad-2e83fa55dabf` | **failed** `output_moderation_failed`, not billed |
| `ef83ccb8-7147-416f-a4af-e2fb04a618d1` | completed, 8 cents |

The two completed clips are different generations: locating the single red
balloon in extracted frames, at t=1s it is at (484, 419) with 23,668 red
pixels in one and at (431, 335) with 1,785 in the other — different position,
13x the area. Same at t=3s. And one submission of three did not come back at
all.

**How the wrong claim got in.** The 2026-09-05 pair
(`1cf5ac46-058f-4615-a47b-067743f76f8c`, `50f623b2-c54a-4d9d-9646-31dd06e2a926`)
ran one seed across two prompts differing by a paragraph and came back with
different subjects. That measurement is sound and stays in the docs — it
establishes *changed prompt → changed result*. The sentence written from it
asserted the **converse**, which the run never touched. A byte-identical
prompt is necessary; it is not sufficient, and nothing about this API is.

**What changed in the files:**

- `SKILL.md`'s section is now "Re-attempting a shot", with the three jobs, the
  2026-09-05 pair kept and re-scoped to what it actually proves, and a
  three-bullet statement of what the seed is for: recording the request,
  aiming at a take again, and **not** a promise to a user.
- The `batch` seed bullet no longer says re-running with a take's seed
  "reproduces that take".
- `references/api-params.md`: the `seed` row now says Ofox documents the field
  as "deterministic generation" and that this was measured otherwise; the Seed
  section carries the same correction.
- `references/ofox-video.sh`: the same-seed batch NOTE now says the takes ask
  for the same generation and are billed for each, while stating that they may
  still differ because the API is not reproducible — **the advice to drop
  `--seed` from a batch is unchanged**, only its reason is. The usage header
  and the per-take seed comment lost the "reproduces that take" claim.

**Nothing about behaviour changed** — no request field, no estimate, no exit
code. What changed is what a caller can promise a user. If you are building a
"render the keeper at 1080p" flow on top of this skill, price it as another
roll aimed at the same shot and say so before the user pays.

### `input_references` accepts audio, fetches it, and ignores it

`references/api-params.md` has listed "≤3 audio clips (each ≤15s)" and an
error code enumerating a 3-audio limit since the skill's first release. Both
are accurate about the field and misleading about the capability. Two runs,
2026-09-15:

- **Free, HTTP 400 `invalid_request`** on a well-formed but unresolvable URL:
  `input_references[0]: url must be a public HTTPS URL (or data: URI): cannot
  resolve hostname: lookup … no such host`. The server parses the element,
  knows `audio_url`, and reaches DNS — it really does try to fetch. It also
  accepts `data:` URIs for audio, so no hosting is needed (unlike a video
  reference).
- **55 cents**, job `d8561509-dcc6-4f2c-8864-a193cd239b14` — a real 5-second
  speech clip as a `data:` URI on `bytedance/seedance-2.5`. Completed
  normally, and **the delivered audio is not the supplied audio**: the input's
  RMS envelope is near-continuous speech, the output's is sparse, correlation
  0.41. The model generated its own track.

So: no lip-sync, no voice-over input, no way to make a clip speak a line you
supply. Whether an audio reference weakly conditions anything is undecided and
one run cannot settle it. The catalog's `capabilities.audio_input: false`
turned out to describe reality better than this skill's own parameter table —
recorded in `api-params.md` under "An `audio_url` reference is accepted,
fetched, and does not become the audio", and flagged in the
`input_references` row and in `prompt-structure.md`'s limits bullet.

## 1.22.1 — the snapshot refresh corrected the data and left the prose quoting the old data

1.22.0's sibling snapshot refresh moved several catalog figures. The tables
built from the snapshot moved with it; the **prose in this file that quoted
those figures did not**, and nothing flags that kind of drift because there is
no code path from a paragraph to the number it names.

Two stale claims in "Which model, and what it costs", both re-checked live
today against `providers`/`models`:

- **`wan-2.7` was quoted at 10 cents/s at 720p. It is 8.6 cents/s.** The 0.1
  was the model-level `pricing.output_video_per_second` field, which this
  repo already documents as not-quotable — it is neither consistently the
  cheapest tier nor the default one. The script has always billed and
  estimated on the per-provider tier, so **no estimate or bill was ever
  wrong**; only this document was. (The two figures either side of it were
  correct and stay: `seedance-2.0-mini` 4 cents/s and `seedance-2.5`
  24 cents/s at 720p are both real per-provider t2v rates. `seedance-2.0-mini`
  is the case where the model-level field coincidentally equals the 720p tier
  while its 480p tier is half that — worth knowing before anyone "corrects"
  it back.)
- **"`wan-*` is 2-15s and 720p/1080p only; `seedance-2.5` … the only one with
  `21:9`/`4:3`/`3:4`"** — wrong on both halves now. `wan-3.0` and
  `wan-3.0-prime` are 2-30s and do offer 480p, so the family glob no longer
  holds; and `4:3`/`3:4` are offered by those two as well, with `21:9` on both
  `hailuo-3` models. This file was also contradicting its own
  `references/api-params.md`, which had the per-family ratio lists right.

**The fix is not just the numbers.** Both passages now name the command that
answers the question instead of carrying a copy of its answer: `models` to
rank, `providers MODEL` to quote, `generate --dry-run` for a specific job.
A figure that has drifted twice is a figure this file should not be holding.

Also documented here for the first time: **`providers` with no model argument
prints the flagship's matrix, not the catalog** — an easy way to read the most
expensive model's rates while believing you are shopping for the cheapest.

**What a caller has to do**: nothing. No behaviour, flag, output field or exit
code changed — this release is documentation only. If you had copied the
`wan-2.7` figure out of this file into your own notes, it was ~16% high.

## 1.22.0 — an attached frame sets the aspect ratio on every model, not just Seedance

Until now, `aspect_ratio=adaptive` was applied for an image-to-video request
only when the model was literally `bytedance/seedance-2.5`. Name any other
model with a frame attached — which became a documented thing to do the day
before this, when the scenario skills started honouring "use wan"/"use
hailuo" — and **no `aspect_ratio` field was sent at all**, so the opening
frame's shape might not be honoured and nothing said so. You found out after
paying for the clip.

The guard now distinguishes a requirement from a default, because collapsing
them would be wrong in both directions:

| Case | Behaviour |
|---|---|
| `bytedance/seedance-2.5` + a frame | forces `adaptive`, overriding an explicit `--aspect-ratio`. API requirement, unchanged from 1.21.3 |
| another model + a frame + no `--aspect-ratio` | defaults to `adaptive` when that model's catalog entry lists it — **new** |
| another model + a frame + an explicit `--aspect-ratio` | keeps the caller's value. These models never demanded `adaptive`, so overriding a stated choice would be the tool overreaching |
| catalog entry has no `adaptive`, or there is no entry at all | sends nothing extra, exactly as before — never invent a value the model may reject |

Whether a model offers `adaptive` is read from `video_attributes.aspect_ratios`
in the catalog the validation already loads (cache → live → stale cache →
bundled snapshot → fail open), not from a second hardcoded model list. Every
one of the four branches prints a `NOTE:` on stderr, including the two that
add nothing: this code has never changed a caller's aspect ratio silently and
still doesn't, and now it doesn't silently *decline* to either.

**What a caller has to do**: nothing, if you only ever used the default model.
If you pass `--model` with a frame attached, read the new `NOTE:` — on a
non-seedance model an explicit `--aspect-ratio` now competes with the frame's
own shape, and the ratio you pass wins. Omit the flag to get the frame's
shape. Scenario skills that told an agent "don't pass `--aspect-ratio`,
adaptive fires automatically" are true again as of this version, and say so
against their own model list.

Three things found while fixing it, all real and all fixed here:

- **The rule was keyed on the string the caller typed, not the model.**
  `--model seedance-2.5` (a documented alias the API accepts, along with
  `seedance-2.5-20260807`) skipped the force entirely, so an explicit
  `--aspect-ratio` on an alias went to the API as a request the API always
  rejects. It now compares the catalog's canonical `id`, falling back to the
  typed value when no entry is available. The bundled snapshot did not carry
  `aliases` at all, so `refresh-snapshot.sh` now keeps that field and offline
  runs resolve an alias like a live run does.

- **`minimax/hailuo-3`'s only resolutions were rejected offline.** The
  fallback union used when no model list is reachable still read
  `480p 720p 1080p 4k`, so `768p` and `2k` — hailuo-3's entire range — were
  refused locally on a cold cache with no network. A stale union rejects
  requests the API would have accepted, which is worse than the round trip it
  saves. Now `480p 720p 768p 1080p 2k 4k`. An uppercase `2K` is still rejected;
  the API's value is lowercase.
- **The bundled snapshot was from 2026-09-02 and predated four models**
  (`alibaba/wan-3.0`, `alibaba/wan-3.0-prime`, `minimax/hailuo-3`,
  `minimax/hailuo-3-max`), so an offline run got no per-model validation for
  exactly the models users are now being told to ask for. Regenerated with
  `refresh-snapshot.sh`; the pricing snapshot came with it and carries real
  drift since then — happyhorse 1.0/1.1 720p 13 → 14 cents/s, happyhorse 1.1
  1080p 17 → 18, wan 2.6/2.7 720p 10 → 8.6. The drift runs in **both**
  directions, which matters because only one of them is dangerous: the two
  happyhorse rates rose, so an offline estimate was **under**-quoting them by
  up to 7.1%, while wan's 720p rate fell, so an offline estimate was
  **over**-quoting it by 16.3%. Seedance rates are unchanged. Live estimates
  were never affected — the snapshot is read only when the catalog fetch
  fails.

`chain`'s sequence-level note about shots 2+ no longer claims `adaptive` is
required on models that merely offer it.

Also in this version, with no behaviour change: the three shared references a
scenario skill links to (`approval-gate.md`, `creative-brief.md`,
`prompt-structure.md`) described themselves as the spec for every
**`seedance-*`** scenario skill. Scenario skills are no longer all named that
way, and the approval gate in particular is the one file whose scope must not
be readable as "doesn't apply to me" — it now says every scenario skill built
on the cores, whatever it is called.

### The snapshot refresh moved the upstreams too, which broke two more things

Regenerating the catalog did not only add models. **Every `alibaba/*` model
went from one upstream to two** (`aliyun` alone on 2026-09-02; `alicloud` +
`aliyun` now), and the two `minimax/hailuo-3*` models arrived with `minimax`
+ `novita`. Two consequences, both fixed here:

- **`--provider` refused slugs that `providers` had just printed.**
  `VALID_PROVIDERS` is a hardcoded enum and did not contain `alicloud` or
  `novita`, so `ofox-video.sh providers alibaba/wan-3.0` printed
  `alicloud aliyun` and `--provider alicloud` then answered *"is not a known
  Ofox provider slug"* — the script contradicting its own output, created the
  moment the snapshot was refreshed. Both slugs added. The per-model check is
  unchanged, so `--provider alicloud` on a Seedance model still fails with
  *"does not serve"*, and an invented slug is still rejected.
- **Upstream pricing is no longer uniform.** `alibaba/wan-3.0` charges
  `alicloud` 11 cents/s and `aliyun` 8.57 cents/s at 720p — a 28% spread,
  where every previous measurement had upstream prices matching exactly. The
  code comment in `rate_for()` asserting that prices "happen to match across
  providers" was therefore false and has been corrected: preferring the pinned
  provider's card is load-bearing now, not a nicety. Unpinned, the lookup
  takes the first card, which for `wan-3.0` is the dearer one — the safe
  direction per "never under-quote", but by array order rather than by design,
  and recorded as such.

**Not changed, deliberately**: which models get pinned. `alibaba/*` and
`minimax/*` still route by weight. Pinning them would mean guessing at
upstream behaviour nobody has measured, which is exactly what the pin rule
warns against; it stays with Fizzy #841.

`references/api-params.md` corrections that fell out of the same refresh: the
upstream table said "all eight video models" and listed `aliyun` alone for
every `alibaba/*` row; the model count was 8 (now 12); the duration row was
missing Wan 3.0 (2–30) and Hailuo 3 (4–15) / Hailuo 3 Max (5–15); the
resolution row named Hailuo 3 but not Hailuo 3 Max (`480p` `768p`, also no
`720p`). Every count and table in that file now carries the date it was
measured, because this is the second time a figure there has gone stale
silently.

New suite: `references/test/aspect-adaptive.test.sh`, 39 assertions over all
four rows above plus the alias case and the text-to-video paths that must stay
untouched. Free by
construction — every case runs under `--dry-run` with the API base pointed at
an unroutable address. Its model list is seeded from the bundled snapshot
rather than hand-typed, and it asserts its own preconditions so a snapshot
change can't quietly turn a row into a no-op. All eleven existing suites
still pass.

## 1.21.3 — the relative path scenario skills use is a probe, not a constant

Docs only; no change to the script, the tests, the API calls or the billing.
"For scenario skills built on this" described
`../ofox-video-core/references/ofox-video.sh` as simply how a scenario skill
invokes this one. That holds for skills.sh, ClawHub and `npx ofox-skills`,
where a skill's directory is named after the skill, and **not** for LobeHub,
which unpacks each skill to `~/.agents/skills/ofoxai-skills-<name>` — so a
scenario skill there hits `No such file or directory` with this skill
installed right beside it. Reproduced in a faked LobeHub layout on 2026-09-14.

That section now states the two layouts, carries the probe the scenario skills
run, and says a new scenario skill built on this one wants the same "Where the
core skill lives" section. It also picks up `seedance-anime-drama`, which was
missing from its list of dependants.

`references/approval-gate.md` gets the same correction in two places, since it
is read from a scenario skill's working directory: its opening no longer reads
a missed link as proof the core is uninstalled — that is one of two causes, and
the other is a directory name — and its `--dry-run` commands say to substitute
whatever the calling skill's probe printed. A quote that cannot be produced
because a path missed is not a reason to skip the gate.
`references/creative-brief.md` carried the same "the file is missing, install
the repo" opening and gets the same two-branch reading.

## 1.21.2 — the changelog for 1.21.1 quoted the literal it had just removed

**Changelog text only; no change to the script, the tests, the API calls or
the billing.** The 1.21.1 entry below originally explained the scanner finding
by quoting the old test-fixture literal verbatim, so the published 1.21.1
still carried `suspicious.exposed_secret_literal`. ClawHub's stored scan report
(`clawhub scan download`, staticScan v2.4.26) placed it at `CHANGELOG.md:14`,
the line of the quote. A key-shaped string in prose explaining its own removal
is still a key-shaped string to the scanner.

- **The 1.21.1 entry is reworded in place** to describe the literal without
  reproducing it. This file ships in the bundle and is scanned like any other
  file; nothing key-shaped belongs in it, in any version's entry.
- **What this does *not* fix**: nothing else. The same stored report lists no
  other static-scan code for this skill, and its LLM review (skillSpector 2.3.5)
  already rated it `clean` / SAFE.

## 1.21.1 — the fake key in the tests read as a real one to a scanner

**Test fixtures only; no change to the script, the API calls or the billing.**
ClawHub's public page for this skill showed `suspicious` at high confidence
after the 2026-09-08 publish. The machine reason was a single code —
`suspicious.exposed_secret_literal` from staticScan v2.4.26 — and it was
correct about the pattern even though it was wrong about the risk: every test
file opened by exporting `OFOX_API_KEY` with a 33-character hyphenated literal
written inline — one whose text says, in words, that it is not a real key. A
static scanner matches the shape of the assignment; it does not read the value
and take its word for it.

- **The literal now goes through a variable**, and the variable's name has no
  `KEY` in it: `PLACEHOLDER=placeholder` then `export OFOX_API_KEY="$PLACEHOLDER"`.
  What changed is the *pattern*, not the length — picking a shorter secret-ish
  string would have been betting on a threshold nobody published.
- ⚠️ **`newuser.test.sh` had a worse one.** Its "a present key is not a verified
  key" case set the variable inline to a joke value carrying the `sk-` prefix a
  real OpenAI-style key has — which is exactly what made the string funny and
  exactly what made it scan badly. Same treatment.
- **Nothing about the tests' meaning moved.** The scripts only require the
  variable to be non-empty; the "present but unverified" case only requires it
  to be set. All 11 test files in this skill still pass.
- **What this does *not* fix**: the LLM-written `security.summary` on the same
  verify call reads differently from the machine code — it talks about dotenv
  sourcing and redirectable endpoints. Those are design properties, argued for
  elsewhere in this file, and no reason code is attached to them. This entry
  claims the static-scan code only.

## 1.21.0 — a key the agent was forbidden to load, in a file the user had already pointed at

**Documentation and `check` output only; no change to how a request is built
or billed.** This one came out of a real session on Codex: the user was
asked to `export OFOX_API_KEY`, replied that it was already in `.env`, then
gave the absolute path, then said "just read it" — and was refused all three
times. Nothing was generated. The refusal was correct per the text: the safety
contract's first line read *"`OFOX_API_KEY` is read **only from the shell
environment** — never from a dotenv file"*, and the only reading available to
an agent is that it may not touch the file even on request.

- **The first safety-contract line is split in two, because it was describing
  two different actors in one sentence.** The script's constraint is real and
  stays hard: `ofox-video.sh` parses no dotenv, ever. The agent's constraint was
  collateral damage from sharing the sentence. It now reads separately: you may
  load the key from a dotenv file *once the user has authorized it*, via
  `set -a; . <path>; set +a` in the shell you'll call the script from.
  Authorization is still the precondition — this is not licence to go hunting
  for `.env` files nobody mentioned.
- **The missing-key recovery bullet now carries the same second path.** This is
  the part that actually mattered. An agent hitting a missing key reads the
  nearest instruction, not the contract twelve screens up, and that bullet said
  `export` and only `export`. Splitting the contract alone would have left the
  dead end exactly where it was.
- **`check`'s stderr gained one line for the same reason** — the terminal user
  who runs the script directly was getting the same single-path advice.
- ⚠️ **New warning, because sourcing a dotenv is not as narrow as it looks.**
  `set -a; . <path>; set +a` imports *every* variable in the file. One of them
  is `OFOX_API_BASE_URL`, which `ofox-video.sh` honours (`ofox-video.sh:120`) — a stray value
  there silently redirects every API call in the session to somewhere else.
  Read the file before you source it. The `.env` that prompted this entry
  contained exactly that variable.

## 1.20.0 — a verified waypoint fix retracted, a proposed payoff fix verified, and a third measurement trap

**`prompt-structure.md` only; no script changes.** Everything here comes from
one run: job `cb6b7870-22f7-4a15-9168-8a013805775f` (2026-09-07, 15s, 720p,
**i2v** with a generated product-only first frame, seed `226221006`, a
`seedance-ad-creative` flask spot, **rejected** on content density). It was
written to reuse two of this file's own conclusions and it split them — one
held on its first real test, the other failed on its second — and the attempt
to measure *why* it was rejected turned up a third thing: a metric this repo
had been treating as a motion reading is not one.

- ⚠️ **The per-waypoint shot size is no longer a verified fix. It is "once
  held, once failed".** 1.17.0 promoted it on the strength of `8efeb556`
  alone — one confirming run on a different product at a different seed with
  the causal ordering preserved, which read at the time like a verification.
  `cb6b7870` has the same shape (a macro beat immediately before a waypoint
  orbit), states a shot size on all three waypoints (`a medium shot ... the
  whole bottle from cap to base inside the frame with margin above and
  below`), closes the paragraph with `the bottle stays fully in frame at
  every moment of the move` — and rendered six frames of upper-body close
  shot with the base never in frame. The macro HOOK's framing, inherited and
  never released. `A camera move needs its waypoint frames, not just a verb`
  now runs to five observations, the shot-size bullet under `What that means
  for writing` carries both outcomes, and the copyable waypoint block says
  the two lines are worth writing and not sufficient.
- **What differs between the two runs, none of it eliminated.** t2v against
  i2v with a paid macro still as the first frame — the one to suspect first,
  since an attached opening composition is a stronger pull toward its own
  framing than a text-described macro beat; a folded pair of glasses against
  a tall cylinder, where the shot size has to reach a base far below the
  label; and a 4s move in a 12s clip against a 5s move in 15s. Stated as
  leads, not as an explanation.
- ✅ **What the failing clip does settle: a shot size stated across a cut is
  on much firmer ground than one stated inside a continuous move.** The same
  prompt's `11-13s` `medium-close shot` and `13-15s` `medium shot dead front,
  the whole bottle centred` were both delivered, the last one holding the
  whole product cap to base with margin. So one clip contains the contrast —
  three in-move shot sizes ignored, two post-cut ones obeyed — which is the
  same distinction `e378f058`'s hedge already drew, now with direct evidence.
  When a move has to change how much of the subject is in frame, the safe
  form is a cut.
- ✅ **A small, fast physical event as its own timestamped frame is now
  verified.** That bullet was written from `60fbea52`'s failure (a drop that
  hung from a pipette through a five-second climax and never landed) and had
  never been run. `cb6b7870` gave the payoff its own boundary at `11-13s` and
  wrote `the steam has to leave the neck and travel up through the light
  within these two seconds, not merely hang above it` — a required-event
  clause whose negative half names the earlier failure exactly. The steam
  rises, glows and drifts, confirmed at t=12.5s. One before-and-after pair on
  two different events rather than a controlled test, but the fix is no
  longer a hypothesis, and the row for `60fbea52` now points at its own
  resolution.
- **`Checking the cuts` gains two rows and the blind spot is nine runs
  deep.** `e378f058`'s **20.958s** boundary (absent at 0.25, needs **0.15**)
  was described in a scenario skill but had never been entered in the shared
  record it pointed at; it is in now. And `cb6b7870` loses **two of its four
  cuts** at the 0.25 default, with scores descending monotonically through
  the clip — 0.395, 0.311, 0.216, 0.132 — because its shots get more alike as
  it goes; 0.15 finds three and 0.10 is the first threshold that finds all
  four. Thresholds needed, in order: 0.05, 0.10, 0.10, 0.15, 0.10 — five
  clips, and lowering the default is still not the fix. The monotonic descent
  is a new sub-observation and a useful one: a clip that works inward ends
  with its most similar shots, so a fixed threshold loses the *last*
  boundaries first.
- ⚠️ **New section: `A scene score is pixel churn, not motion`.** The third
  measurement trap in this file, after the detector count and the azimuth
  reading, and the same shape as both: a number that looks like it measures
  the thing you care about. Measured on `cb6b7870`, mean inter-frame `scene`
  at native 24fps with each segment's cut frame excluded — HOOK 0.0078,
  SHOWCASE 0.0039, CLIMAX 0.0077, PAYOFF **0.0008**, CLOSE 0.0003 — against
  what the frames show: the PAYOFF is steam visibly leaving the neck and
  drifting, the SHOWCASE is an orbit that never moved, and the HOOK is a
  static macro whose only change is a highlight sweeping brushed metal. **The
  ranking is close to inverted**, because `scene` counts whole-frame pixel
  difference: a thin white wisp on near-black is a few hundred pixels, a
  specular streak on a brushed cylinder is tens of thousands. The bias has a
  direction — large-area low-contrast changes over-counted, small-area
  high-contrast events under-counted — so a dark studio maximises both errors
  at once. A near-zero score is still informative as a bound (it is how
  `50f623b2`'s motionless orbit and a held final frame were confirmed); the
  ordering of two non-zero scores is not. This entered the file because a
  scenario skill had drafted a per-segment score table as evidence that a
  clip was too static; the conclusion survived on the frames, the table did
  not.
- ⚠️ **New paragraph: the cost of a single-threshold pass is a false claim
  about the model, not just a low count.** One pass at 0.15 over `cb6b7870`
  finds three of its four cuts, and the natural-sounding conclusion is "a
  fourth cut was written and the model dropped it" — a statement about
  obedience drawn entirely from a detector setting. The frames say all four
  landed, at 0.00 / −0.46 / +0.04 / +0.25 seconds of their stamps. A single
  threshold cannot separate "the cut is not there" from "the cut is not
  visible at this threshold", so it supports neither sentence.

Also: the closing checklist's item 5 now says a stated shot size is
necessary and has not proved sufficient, for the same reason as above.

## 1.19.1 — the key requirement, moved to the front of a description that gets truncated

Docs only; no script changes, no advice changed. `description` now **opens**
with one sentence: `Requires OFOX_API_KEY — create one at
https://app.ofox.ai.` The dependency itself is unchanged and was already
declared in `metadata.openclaw.requires.env`, which stays exactly as it
was — that is the route ClawHub and openclaw read. Nothing a caller does
changes.

**Two separate blind spots, measured 2026-09-06 against Codex CLI 0.149.1 with
a project-level install of this repo.** It listed all nine skills, but asked
which environment variables `seedance-product-video` needs before use it
answered that it could not tell from the visible skill metadata. The first
cause is the obvious one: some agents read only the frontmatter's `name` and
`description`, never `metadata`. The second only surfaced on a controlled
retry — same agent, same question, the requirement added to the **end** of the
description and nothing else changed — where the answer did not budge. Pressed
for a verbatim quote, the agent said the description in its context was
truncated and did not include the final sentence; it put its own visible tail
at about 257 characters, and the fragment it could still quote ends at
character 320 of the real text. So the window is roughly 300 characters, and
these descriptions run 828 to 1200. "Reads the description" is not the same as
"reads all of it".

**What that costs, beyond the key.** Inside a ~300-character window the
`Use when ...` trigger examples of all four scenario skills fall outside: they
begin at character 431 (`seedance-ad-creative`), 594
(`seedance-product-video`), 641 (`seedance-anime-drama`) and 690
(`seedance-short-drama`). This skill's own `Load this skill directly only when ...` clause begins at
character 522, likewise outside. A truncating agent has never matched any of them
on an example — it matches on the opening summary alone. Anything that has to
reach such a reader belongs in the first ~300 characters, which is why this
sentence leads instead of trailing, and why it is 58 characters rather than the
106 first drafted: that position is the scarcest space in the skill, and every
character spent there displaces a character of trigger material.

**Why character 0 and not the end of the opening sentence.** The first
sentence-ending period sits at character 268 in `ofox-image-core`, 430 in
`seedance-ad-creative` and 593 in `seedance-product-video`. Placed there the
sentence would straddle or clear the window in exactly those three, and
reaching a boundary at all in two of them would mean repunctuating shipped
prose. Character 0 is the only position that is inside the window under both
the 257- and the 320-character reading, for all six skills, without altering a
word of the existing text.

Two readers were never affected and are unchanged by this: Claude Code reads
the description in full, and OpenCode read at least the first 1075 characters
of `seedance-product-video` — it answered `OFOX_API_KEY` correctly even from
the trailing version.

## 1.19.0 — a scheduled cut is not a kept cut, and the anti-plastic sentence has one place not to point it

Docs only; no script changes. One job generated 2026-09-06 with 1.18.0's
findings already in hand — `9cd773d0-b84e-4135-bc75-8f4e8963be2b` (15s, 720p,
seed `621899521`, 3.60 USD) — plus one caveat carried back from a refused image
call the same day.

**1.18.0's framing was optimistic and is corrected in place.** That entry showed
prohibitions on a tempo failing and pointed at budgets as the sturdier
instrument, which invited the reading that the repair for `no hard cuts` is to
schedule the cuts instead. This job did exactly that — `HARD CUT at 00:04`,
`at 00:08`, `at 00:11.5` — and delivered no cut at 4.0s, a cut at 7.75s (0.25s
early), no cut at 11.5s, and two cuts nobody asked for at 6.29s and 9.67s. One
of three landed. The two misses were confirmed frame by frame at 3.8/4.1s and
11.3/11.6s, so they are absent cuts rather than cuts a detector missed.
"What a prohibition cannot buy: timing and behaviour" now says plainly that
**cut placement is unreliable under either wording**, and points at "Past that
envelope: six jobs, and what the mix does to a boundary" — where the lever with
evidence behind it, the hard-cut share of the timeline, already lives. If you
took 1.18.0 as licence to promise a caller a cut at a named second, stop
promising it; promise the mix and the length instead.

**The same job's two exact deliveries say what to lean on.** `at most 0.15
seconds of slow motion, and only at 00:13` held with no out-of-budget slow
motion anywhere — a budget clause reading true for the second job running. And
`the action ends at 00:13` produced 2.8 at 13s, 1.0 at 14s and 0.6 at 15s: the
predicted two quiet seconds, landing inside the 15 already paid for. That is
the first time `"Hold one second" buys about two` was **spent** rather than
measured — the overshoot planned for by scheduling the last beat two seconds
early — and that subsection now records the application alongside the two
measurements.

**And that subsection was parked where three of the four scenario skills could
not see it.** 1.18.0 put "What a prohibition cannot buy: timing and behaviour"
under "A camera move needs its waypoint frames, not just a verb" — a section
no scenario skill names in its load list. Scenario skills load shared sections
by name, so the finding reached only `seedance-anime-drama`, which happens to
name the subsection itself, and was invisible to `seedance-short-drama`,
`seedance-ad-creative` and `seedance-product-video`. It now
sits under **"Consistency locks and the negative list"**, next to "Unwanted
text is designed out of the set, not forbidden in the list" and "The plastic
look is designed out, not forbidden" — the same shape of finding, and a section
all four scenario skills already load. No scenario skill has to change to pick
it up. Its opening sentence used to point at the subsection above it; it now
names "Negative clauses are honoured more reliably than positive ones" and the
section that one lives in, so the reasoning still chains. The cross-reference
to it from "Rules that travel with the vocabulary" now names the new parent.

**Where to aim a texture sentence.** "The plastic look is designed out, not
forbidden" recommends naming skin texture positively. It can trip the image
API's safety filter when the subject is wet: a refused character frame carried
`water runs in threads down skin`, `skin shows visible texture and rain-slick
unevenness` and `soaked … clinging to her shoulders` in one paragraph. The same
paragraph with its descriptions landing on fabric, wet metal and water surfaces
instead passed and still suppressed the plastic look. The subsection's claim is
unchanged — this is a caveat about *where* to point the sentence, added inside
it.

## 1.18.0 — a prohibition cannot buy a tempo, but a budget can; and the cause chain, read frame by frame

Docs only; no script changes. Two anime jobs generated 2026-09-06 —
`c192dbe6-ae09-4dba-8e81-3a3e82ff5912` (30s, 720p, t2v with a first frame,
seed `457047702`, 7.20 USD) and `c2eb32e1-3b54-4a56-8d78-86e63bc355c7` (8s,
480p, text-only, seed `18854260`, 0.88 USD) — add six subsections to
`references/prompt-structure.md`, five of them measured on those two clips.

**A prohibition on a tempo is soft; a budget is not.** "What a prohibition
cannot buy: timing and behaviour", under the negative-clause section, tabulates
three: `no hard cuts` produced four cuts in the 30s clip, `neither of them
waits after separating` produced three low-motion stretches, and `no slow
preparation` produced two near-static opening seconds in the 8s clip. In the
same prompt, `at most 0.2 seconds of micro slow motion, only at the instant
the final kick lands` held. (Both prompts were written in Chinese; clauses are
quoted in translation, as this repo does for case 44.) The existing subsection already sorted prohibitions by
*what* they remove; this adds the axis of whether the thing removed is an
object or a tempo. It is written as a tendency to price in, not as a ban on
writing prohibitions — the 8s clip carried the same no-hard-cuts clause and
came back with zero
cuts, which says duration was doing as much work as the prohibition failing.

**The cause chain is now a first-class subsection with frame-level evidence.**
It had been living in `seedance-anime-drama`'s pattern table, sourced to cases
44 and 11 as writing anyone had done rather than as anything that had been
checked. Reading `c192dbe6`'s finishing kick at 1/12-second spacing puts each
link on a timestamp: target visible and unreacted at 24.85s, entry through
25.10s, the strike at 25.18s with **still no anticipatory recoil**, contact at
25.27s, reaction and displacement from 25.35s. Five frames of approach with no
early flinch is the specific failure `no impact reaction before contact`
names. The
anime skill's row now points here instead of restating it.

**Three more.** "Rules that travel with the vocabulary" gives `Camera language`
the three constraints case 44 puts around whichever move it picks — readability
over the effect, contact staying in one frame, a slow-motion budget — and notes
that the block inverts rather than disappears for catalog footage. "Continuing
a previous clip" splits the sequel problem into a frame route and a words
route, measures what the words route reproduces (staging, positions, props by
number and place, wardrobe, palette) against what it does not (exact pose,
camera distance, light level), and records that feeding a *delivered* frame
back in was refused for copyright on **both** upstreams — `5440c21e` on
byteplus and `c4cff71a` on volcengine, neither billed. "Hold one second buys
about two" measures the ending overshoot on both clips.

**And one that is craft, not measurement.** "The plastic look is designed out,
not forbidden" breaks the AI-render look into four faults — uniform surfaces,
unmotivated light, a single mirror highlight, global over-exposure — and gives
each a positive sentence, on the same principle as the neighbouring subsection
about unwanted text. Both anime jobs carried a positive style sandwich *and*
the usual negatives and came back with no CG sheen; which half did the work is
not isolated, and the subsection says so.

## 1.17.0 — the waypoints render, the ending does not: a second product clip settles two open items

Docs only; no script changes. A third `seedance-product-video` clip
(`8efeb556-bf38-45ec-940b-a792ef74bfcf`, 2026-09-06, 12s, 720p, t2v, seed
`616202922`, a folded pair of eyeglasses, 2.88 USD) was written to test two
fixes 1.16.x had proposed but not run, and it does three things to this
file's waypoint material: it **verifies** the per-waypoint shot size,
**measures** an extent that was previously unmeasurable, and **refutes** one
sentence 1.16.1 left standing. It is an independent run — different product,
different seed, different prompt — not a second half of the grinder pair, and
that is what makes it able to settle anything.

- **The per-waypoint shot size is verified, not proposed.** 1.16.1 recorded it
  as a fix "aimed at the observed cause"; `What that means for writing` now
  says it has been run. The new clip states a shot size on all three
  waypoints, closes the paragraph with `at every one of those views the entire
  pair of glasses is inside the frame, nothing cropped`, and **deliberately
  keeps the same macro-detail-then-orbit order** that caused the inheritance
  in the first place — so the defect had every chance to recur. Every frame of
  the move holds the whole product with margin, where the grinder's base was
  out of frame for its whole orbit. One confirming run with the causal
  ordering preserved; `Segment skeleton to copy`'s trap note and the
  `Waypoint block to copy` note say the same.
- **⚠️ "The move happens and it arrives" is withdrawn — the interior pictures
  arrive, the closing return does not.** This corrects the section preamble,
  claim 1 of the arrival subsection, and the `A total quantity is fine`
  bullet, all of which 1.16.1 left resting on the grinder clip's last frame
  matching the frame its prompt named. The new clip's orbit begins at the
  front (fixed by its own opening shot) and ends at the **rear**: front 6.0s →
  side 7.5s → rear about 9.6s, with the named front view returning only after
  the next hard cut. So the grinder's landing is explained by a half turn from
  an unasked-for rear start, not by the closing clause — **one coincidence and
  one plain failure, which is no evidence at all.** If a clip has to end on a
  named view, cut to it.
- **About half a turn is now measured.** `What the arrival does and does not
  establish` is renamed `How far the move goes, and where it stops` and
  carries both readings: the grinder's ~180 observable degrees with an
  unmeasurable total, and the eyewear clip's front → side → rear read frame by
  frame inside one continuous shot. Two independent clips agree on roughly
  half a turn, and the second one measures rather than infers it. The rule for
  a prompt: **expect a waypoint orbit to cover about half a turn.**
- **`Measuring a camera's travel: only inside one continuous shot` is
  validated, not superseded.** That subsection predicted that an asymmetric
  feature inside one continuous shot would make azimuth readable; the folded
  temples plus a cut-free orbit is exactly that case, and it read cleanly. It
  now says so, and says explicitly that `50f623b2`'s own total stays
  unmeasurable — a fact about that clip, which no later run changes.
- **A fourth row in the observations table**, and the heading counts to four.
  The movement-versus-no-movement finding still rests on the controlled pair
  and nothing else; the new row carries the shot-size verification and the
  extent.
- **Interior timing gets its first attributable run.** Both of the new clip's
  interior waypoints are distinct pictures that do not contradict themselves,
  so `The timing between waypoints is approximate` can now say which was late:
  the side on time, the rear about 0.6s late, the return never. Two interior
  pictures written and two rendered — the first run to hit this file's own
  recommended budget exactly, and it lost only the ending, which is why the
  "don't put the one that matters at the end" clause is new.
- **The same-lighting blind spot, third consecutive confirmation.**
  `Checking the cuts` gains an `8efeb556` row: at threshold 0.25 only 2.67s
  and 5.71s appear, and the third cut at **9.71s** needs **0.10**. Three
  clips, three after-the-fact discoveries (0.05, 0.10, 0.10) against a 0.25
  default wrong for all three — so **lowering the default is not the fix**,
  because how far to lower it is only knowable once the frames have been read.
- **New subsection, `A description is honoured; a number attached to it is
  not`** (`references/prompt-structure.md`, between the negative-clause rule
  and the copyable waypoint block, because it is the same grammar problem one
  level down). A quantity in a clause is the part most likely to be dropped
  while the description it hangs on renders fine: four instances, three of
  them measured here — an interleaved barrel hinge that came back with four
  knuckles against three written (`8efeb556`), a limb limit written twice and
  ignored (`60fbea52`), three interior waypoints rendering as two
  (`50f623b2`), and `a full 360 degrees` covering half a turn twice. The
  corollary is what keeps this from over-generalising: the *spatial*
  description that fixed the framing defect in the same clip landed, so what
  fails is the counting, not the writing-it-down.
- **`hold the final frame` is two in three, and the earlier figures were an
  artefact.** Measured without an `-ss` pre-seek — which gives the first
  post-seek frame no predecessor to diff against and therefore scores it as a
  change — the new clip is **completely** still (zero frames above 0.0005
  after 11.541667s, last change anywhere at 11.375s, about 0.67s of hold) and
  `50f623b2` drifts across **seven** frames, not the six 1.16.1 recorded.
  `Endings` states the count and keeps the advice: expect a settle, freeze in
  an editor.
- **Nothing claims the orbit was even or constant-speed.** `How far the move
  goes, and where it stops` says only that the azimuth advances monotonically
  with no dead stretch, and says explicitly that a per-half-second
  scene-delta reading cannot settle angular velocity on this subject, because
  near the front view the same rotation changes the picture much less.
- **`--aspect-ratio 16:9` and `--generate-audio false`, confirmed again**
  (`api-params.md`): 1280x720 out, and no audio stream at all rather than a
  silent one — three text-to-video runs, three times.
- **The no-resubmit rule survived a third live transport fault.** The same
  `curl: (35) LibreSSL ... SSL_ERROR_SYSCALL` mid-poll, the same poll-not-
  create retry six seconds later, the same clean completion. `SKILL.md` and
  `api-params.md` both read three for three now, on separate days.

Nothing here widens the untested edges: the turntable phrasing — a *product*
verb rather than a camera one — is still unmeasured, and no run in this repo
has ever shown a written 360 performed. `references/ofox-video.sh` is
untouched and all 271 assertions across the eleven suites still pass.

## 1.16.1 — how far that camera went is unmeasurable, and 1.16.0 said it completed a circuit

Docs only; no script changes. **This entry corrects 1.16.0, which is in the
same unreleased state as this one — read them together rather than treating
the newer one as an addition.** 1.16.0's headline finding stands: a camera
move written only as a verb produced no movement, and the same move written
as waypoint pictures produced movement and landed on the frame it named.
What it got wrong is the *extent* of that movement, which it recorded as a
completed 360-degree circuit. It is not measurable at all, and an
intermediate draft before it had the error in the other direction — about
180 degrees and no return. Three published readings of one clip, two of them
wrong, which is why the general rule now sits in the file as its own section
rather than as a note on this job.

- **New shared subsection, `Measuring a camera's travel: only inside one
  continuous shot`** (`references/prompt-structure.md`, immediately after
  `Checking the cuts: read frames, never a detector count alone`, because it
  is the same class of mistake — trusting a reading whose preconditions were
  never checked). **A camera's azimuth is only measurable within a continuous
  shot**: across a cut the camera can be anywhere, so travel cannot be read
  off endpoints that span the cut, and the reading also needs the subject to
  carry an asymmetric feature to track. A three-row table gives both wrong
  attempts, the endpoints each used and the precondition each skipped —
  attempt 1 measured from the moving segment's own first frame and under-read,
  attempt 2 measured across the hard cut at 6.291667s and over-read.
- **`50f623b2` now claims an arrival, not a circuit.** ⚠️ **Superseded in
  1.17.0: not an arrival either.** An independent clip shows the same form of
  move covering half a turn and stopping at the rear, so this clip's landing
  on the named frame is a coincidence of where the move began. Inside the
  continuous ORBIT segment the frames read rear → side → front, about 180
  degrees, ending on the orientation the clip's own 2.8s frame establishes as
  the front. The written path's other half could only have happened across that
  hard cut, and the shot before it is a macro of a knurled ring — rotationally
  near-symmetric, no orientation cue — so the segment simply *starts* at the
  rear and nothing distinguishes travelling there from being cut there. New
  subsection `What the arrival does and does not establish` carries the frame
  table, the two claims and the limitation; the section's preamble, the
  three-observation table, the `total quantity` bullet and the `Waypoint block
  to copy` note all match it now.
- **The per-waypoint timing table is retracted, not reworded.** 1.16.0 paired
  each written stamp with a verdict ("8s — about a second late"), which the
  confound recorded in the same release makes unattributable: each waypoint
  carried both a position label and an appearance clause, and on one of them
  the two contradict each other. `The timing between waypoints is
  approximate` now gives counts and durations only, and says the table was
  retracted so nobody restores it.
- **The near-stationary stretch is six sampled frames, not five.** 6.40, 6.80,
  7.20, 7.60, 8.00 and 8.40 all read crank-right, with 8.80 the transition —
  so roughly 2 seconds near-stationary and the rest of the move compressed
  into about 1.2 seconds. Wherever 1.16.0 said five of ten frames, it was
  short by one.
- **An unspecified shot size deletes waypoint content, it does not just crop
  the picture.** In `50f623b2` one waypoint asked for a knurled ring seen
  edge-on and that ring was outside the inherited macro framing for the whole
  move, so half of that waypoint had nowhere to render. `What that means for
  writing` and the `Segment skeleton to copy` trap note both say this now: a
  missing beat can be the prompt's own doing rather than the model ignoring
  it.
- **The scene-detector blind spot is a pair, at two different thresholds** —
  the strongest form this finding has taken here. 1.16.0 recorded one clip's
  miss at threshold 0.25. Both clips of the pair hid a real boundary at 0.25,
  and they needed **0.05** (`1cf5ac46`, at 9.750s) and **0.10** (`50f623b2`,
  at 10.041667s) respectively before it registered. No single lower number
  would have caught both, which is what "a lower threshold does not fix it"
  means concretely. `Checking the cuts` gains the second row and that
  reading, plus the converse: a detector reporting nothing inside a segment
  you asked to be continuous is weak evidence, since the same pass missed a
  cut three seconds later in the same clip.
- **`hold the final frame` buys a settle, not a freeze**, recorded in
  `Endings`. Over each clip's last half second `1cf5ac46` is still (every
  frame under a 0.0005 scene score) and `50f623b2` is not (six frames above
  0.0005, one above 0.002 — ⚠️ **re-measured in 1.17.0 as seven above
  0.0005**; the earlier count came from an `-ss` pre-seek that scores its
  first frame as a change) — same instruction, same seed, one paragraph
  apart. Freeze in an editor if the last frame really has to stop.

Every hedge 1.16.0 carried is still here — it is still two runs, and this
pass makes the evidence narrower rather than broader. `references/ofox-video.sh`
is untouched and all 271 assertions across the eleven suites still pass.

## 1.16.0 — a camera that never travelled, and the same camera travelling once it was given frames

Two runs on 2026-09-05 asked the same model for the same move twice, on one
seed, changing nothing but the wording of a single paragraph. The first
version — `the camera orbits the grinder a full 360 degrees at constant
height and constant speed, ending back at the front view. The product does
not move and does not rotate; only the camera travels.` — produced a
near-static front view with the crank arm pointing right in every frame. The
second version described the same move as a handful of still pictures, and
the camera went round: measured against the clip's own opening view, 180
degrees at 7.0s, the rear at 9.0s, back to the front at 10.0s. A controlled
experiment with a negative control, and still only two runs.

*(1.16.1 corrects the extent: the move arrives on the frame it names — ⚠️
**and 1.17.0 withdraws that half too: an independent clip covers the same
half turn and stops at the rear, so this one's landing is a coincidence of
where it began** — its observable travel inside the continuous segment is
about 180 degrees, and its total is unmeasurable because half the written
path could only have crossed a hard cut. The waypoint finding itself stands. **Three things in this entry are
superseded and are kept only as the record of what was claimed: every degree
figure; every statement that the circuit completed; and every per-waypoint
timing verdict — that last form was retracted rather than reworded, because
each waypoint confounded a camera-position label with an appearance clause
and no rendered frame can be attributed to a particular written stamp.**
Read 1.16.1 first.)*

- **New shared section, `A camera move needs its waypoint frames, not just a
  verb`** (`references/prompt-structure.md`, placed immediately before
  `Camera language`). What is described as a picture gets rendered;
  what is described *only* as a motion may silently not happen. Three job
  ids, weakest to strongest: a payoff dropped off the tail of a long climax
  (`60fbea52`), the negative control (`1cf5ac46`), the rewrite that worked
  (`50f623b2`). It is a top-level section rather than a subsection of `Camera
  language`, because that section is a vocabulary of quoted phrases and this
  is a rule about the grammar of a clause — and because it governs the
  timeline and the pacing sections just as much.
- **The move completes; the schedule does not.** *(Superseded by 1.16.1 in
  both halves: the completion is unmeasurable, and the per-waypoint verdicts
  below are retracted. What survives is the shape — two of three interior
  pictures rendered, six of ten sampled frames were the same picture, and the
  spacing did not hold.)* `50f623b2` delivered its full circuit, but of four
  written waypoints the 7s and 10s endpoints landed
  on time, the 8s one arrived about a second late, and the 9s one never
  appeared as a distinct beat at all — absorbed, with the move lingering on
  one side through roughly 6.4-8.4s and covering rear-to-front in the last
  second and a half. So: two or three waypoints per move, endpoints carrying
  the ones that matter, and **no beat planned to land on an exact second** —
  give that its own shot instead. Sampled at 0.4s intervals; the table is in
  the section.
- **How to measure a rotation without getting it wrong**, recorded because
  the first pass at these frames did. *(This bullet is the second wrong
  reading, not the method: measuring from the clip's opening view reaches
  across the hard cut at 6.291667s and over-reads the travel. 1.16.1 replaces
  it — both endpoints have to sit inside one continuous shot. The
  foreshortening half stands.)* The reference has to be the clip's own
  opening view, not the first frame of the moving segment, and the crank
  arm's foreshortening is what disambiguates front from side — from either
  side the arm reads compressed, and only from the front or the rear does it
  extend cleanly sideways.
- **Negative clauses are honoured more reliably than positive ones.** In
  `1cf5ac46` one sentence carried a prohibition and an instruction, and only
  the prohibition survived — the product really never rotated, and the camera
  really never moved. So a prohibition is no evidence that the instruction
  beside it will run, which is now written down next to the existing
  observation that a negative item holds in an empty set and fails on a
  street full of surfaces.
- **A segment inherits the previous segment's shot size.** *(The fix this
  bullet proposed — a shot size on every waypoint — was verified in 1.17.0 on
  an independent clip that kept the same macro-then-orbit ordering on
  purpose.)* In `50f623b2` the
  waypoints rendered correctly and every one of them ran at the macro
  closeness of the detail segment before them, so the subject's base was out
  of frame for the whole move. `Segment skeleton to copy` now marks the
  shot-size slot as not optional, and the `Quick checklist` gained an item for
  it — the checklist is renumbered from 6 onward as a result.
- **Cross-references added where the undecomposed form is still on the
  page**: `Camera language`'s preamble and its `Camera line to copy` (the
  `<movement>` slot takes a texture; a destination needs waypoints too),
  `Segment skeleton to copy` (the `orbit` slot, and the shot-size slot),
  `Pacing line to copy` (a small fast `<Climax event>` needs its own stamp),
  and `Endings` (four of its eight rows are moves rather than pictures, so
  write the arrival as a picture as well as the move). No template was made
  to ask for music; the new `Waypoint block to copy` points at the copyright
  section before an audio line is added.
- **What this entry does not claim.** A total quantity — `a full 360
  degrees`, `ending back at the front view` — is *not* recorded as a failing
  form: it was in the prompt that worked and the circuit completed. It is not
  the mechanism either; the waypoint pictures are. An intermediate draft of
  this section said the quantity clause was the one thing that failed, from a
  rotation measured against the wrong reference frame, and that claim is
  retracted rather than merely edited out — the section says so in place, so
  nobody re-derives it.

Three more facts from the same two runs, none of which changed any behaviour:

- **The seed reproduces a take only when the prompt is byte-identical**, and
  this is its boundary rather than a retraction. Both grinder clips ran seed
  `642303335` with identical parameters and came back with visibly *different
  subjects* — a wide steel collar on a short body versus a narrow collar on a
  longer body — from one edited paragraph. So the seed is the handle for "that
  one was good, render it at 1080p", where only `--resolution` moves; it is
  not a handle for "that one was good, now fix shot three". Recorded in
  `SKILL.md`'s `Reproducing a shot` and `Batch`'s seed bullet, and in
  `api-params.md`'s `Seed`, which is also why the sidecar stores the prompt as
  submitted — so a replay never depends on retyping it.

  *(⚠️ **1.23.0 withdraws the first half of this bullet.** The two grinder
  clips establish *changed prompt → changed result*, which stands. The
  sentence written from them asserts the converse — identical prompt →
  reproduced take — and the converse was never run. Three 2026-09-15
  submissions of one byte-identical request on a fixed seed returned two
  visibly different clips and one outright failure. The seed records a
  request; it does not reproduce a take, at any prompt. Read 1.23.0.)*
- **The no-resubmit rule has survived a real transport fault**, for the first
  time in this repo. Both jobs dropped their TLS connection mid-poll
  (`curl: (35) LibreSSL SSL_connect: SSL_ERROR_SYSCALL`), the script retried
  the poll and not the create, and both completed normally. 2.88 USD each, so
  a resubmit at that moment would have doubled both bills on a fault that
  cleared itself in six seconds. Every clause of that rule had been reasoned
  from the API's shape and never exercised by an actual broken connection.
- **A fifth confirmation of the scene detector's blind spot**, and the first
  at a looser threshold: `1cf5ac46` hid its third cut at threshold **0.25**
  while the detector found the two before it in the same pass. One uniform
  grey studio throughout, which is the condition — same place, same light —
  and a lower threshold does not fix it. Added to the existing table rather
  than starting a second list.

And two verifications that were cheap to get and had never been cleanly
observed, both in `api-params.md`:

- **`--aspect-ratio` is effective on the text-to-video path**, not merely
  accepted: `16:9` delivered a file measuring 1280x720. Every earlier clip in
  this repo attached a first frame and was therefore forced to `adaptive`,
  where the ratio comes from the image and the flag does nothing.
- **`--generate-audio false` produces no audio stream at all**, not a silent
  one. Anything downstream that assumes every clip has a stream to work with
  has to handle its absence.

Documentation only — `references/ofox-video.sh` is untouched, and all 271
assertions across the eleven suites still pass.

## 1.15.0 — a 15-second clip took over 600 seconds, and `batch` was multiplying that by the take count

One measurement started this: a 15s 720p job on 2026-09-05 spent **over 600
seconds** of wall clock. The account allows **100 requests per minute** and a
polling job spends 10 of them, so the rate limit was never the constraint —
the serial `batch` loop was. Three takes of that clip was half an hour of
waiting for ten minutes of generation, and the fan-out primitive to avoid it
(`create` and `poll` as separate subcommands) had existed all along and had
never been used.

- **`batch` now creates one take at a time and waits for all of them at
  once.** The split is the point. A create answers in seconds, so serialising
  it costs almost no wall clock and it is the only ordering in which "take 2
  was rejected, so takes 3..N were never sent" can be true — the money guard
  is preserved exactly, not traded away for speed. Firing N creates at once
  would spend N times to learn the first was going to fail.
- **A take that fails *after* submission no longer takes the others down.**
  That is a different animal from a rejected create: the money is already
  committed and the other takes are already running, so the failure is
  reported (`TAKE 2 <id> seed=<n> FAILED exit=3`) and the rest complete. And
  when a submission *is* rejected, takes already submitted are still waited
  for and downloaded — they are billable whether or not we collect them, and
  abandoning a paid job was never a saving.
- **`poll` takes several job ids**, polled together under the same cap. This
  is what makes cross-clip fan-out usable: N `create` calls, then one command
  that waits on all N. Each job's own stdout is replayed under a `=== JOB i/N
  <id> ===` delimiter **in the order the ids were given**, so `VIDEO_PATH` and
  `VIDEO_COST` read exactly as they do for a single poll, plus a
  `POLL_COST_TOTAL`. One id is byte-for-byte what it always was — same call,
  no subshell, no wrapper lines — because every existing caller depends on
  that shape.
- **`--concurrency N`, default 4, ceiling 10**, also settable via
  `OFOX_POLL_CONCURRENCY`. Both numbers are requests per minute rather than a
  guess: one polling job issues one GET per `--poll-interval`, so at the
  default 6s it spends 10 of the account's 100 RPM, which makes 10 concurrent
  polls exactly the whole limit — hence the ceiling, and hence why it is never
  the default. Four is 40%, and the rest is not spare: a batch's creates go
  out first, a 429 or 5xx retries at the same cadence, and an agent commonly
  has another Ofox call in flight in the same session. Lowering
  `--poll-interval` multiplies the rate, so the script computes the implied
  RPM and says so when the combination crowds the limit — a warning, not a
  block, since rate limiting costs a poll cycle per job rather than money.
- **Attribution is by take, not by finish order.** Takes now land in whatever
  order the API feels like, and the seed printed against take 3 has to be take
  3's or "re-render that one at 1080p" spends money on the wrong clip. Results
  are read back by index, take numbers survive a gap where a take failed, and
  a take's own diagnostics are flushed as one contiguous labelled block the
  moment it finishes — nothing is streamed, because four polls' warnings
  interleaved live are unreadable and, worse, unattributable. A heartbeat every
  30s covers the silence in between.
- **`STATUS batch_partial`** is new, and replaces `batch_completed` whenever
  the run is not what was asked for, alongside `TAKES_SUBMITTED`,
  `TAKES_FAILED`, `TAKES_RUNNING` and `TAKES_NOT_SUBMITTED`. A partial run
  used to print `batch_completed` with fewer `TAKE` lines and leave an agent
  to notice the counts disagreed. `batch` and a multi-id `poll` also pick the
  most severe actionable exit code: `3` if anything failed (needs a new
  prompt), `4` if something is merely still running (needs another poll), `0`
  only when everything landed.
- **Consecutive 429s now back off further per job**, doubling up to 60s and
  resetting the moment a request gets through. The first 429 still waits
  exactly one poll interval, as it always did; what changed is the
  pathological case, because with several polls sharing one account-wide limit
  the useful response to being rate limited is to ask less often rather than
  to keep asking at the same cadence. `--max-wait` is still wall clock, so a
  long backoff cannot overrun it.
- **`SKILL.md` gains "Waiting in parallel"**, which is half the point of this
  release: the primitive existed and nobody used it, so the file now says
  plainly that clips parallelise, that image-to-video **within** one clip does
  not (the first frame has to exist before the video job can be submitted, so
  that stretch of wall clock is irreducible), and that several takes of one
  prompt is the highest-value case. The example for the last one is job
  `60fbea52-b14b-4796-80bf-03afe0aa4fa0`, which came back technically clean
  with its written climax missing — a drop that was supposed to fall never
  detached. Nothing was wrong with the prompt or the bill; the answer to that
  is another take, and another take now costs the same wall clock as the
  first. The section also states the thing concurrency does not change:
  N takes is N bills arriving at once, so the approval gate's itemised table
  has to be on screen before a concurrent batch, never after.
- **What this costs, stated once rather than buried:** submitting every take
  up front removes the escape hatch the serial loop had. With takes billed one
  at a time, a user watching a bad take land could interrupt before the next
  one was paid for; now the whole total commits within seconds. The exchange
  is a batch that takes one clip's wall clock instead of N, and the
  consequence is that the cost table is the only place a concurrent batch can
  still be stopped — which is why `approval-gate.md` now says so in its
  batch section.
- **`approval-gate.md`'s image-estimate section rewritten a second time**,
  because 1.14.1 (above, hours earlier) described `ofox-image-core`'s lookup
  as pair-blind and that stopped being true when that skill shipped 1.7.0 the
  same day. The gate no longer tells an agent to work out which measured pair
  applies — the script does that — and instead names the two labels it can
  print, `ROUGH` for an exact pair match and `ROUGH UPPER BOUND` for a pair
  nobody has measured, with `Weak ceiling` on a model that has only one
  measured pair at all. Two new prohibitions, both aimed at the way a
  hand-corrected table drifts: do not substitute a figure of your own for the
  printed one, and do not quietly drop an `UPPER BOUND` to a cheaper measured
  point because it looks closer to the request. This is the shared spec four
  scenario skills read, so a stale sentence in it is four stale skills.
- **New test suite** `references/test/concurrency.test.sh`, 48 assertions,
  none of which spend anything: the cap's real high-water mark read off a
  start/end marker log, multi-id argument parsing in either position and with
  duplicates collapsed, single-id output shape unchanged, per-take
  seed/id/cost/path attribution under deliberately reversed completion order,
  a submission failure still stopping the run while the already-billable takes
  are still collected, and a post-submission failure leaving the others alone.
  Suite total is now 271 assertions across 11 files, with no existing
  assertion changed.

## 1.14.1 — the gate's own image example was broken by a chain reorder, and its rough figure carried no pair

Docs only; no script changes. Two defects in
`references/approval-gate.md`, both surfaced by `ofox-image-core` making
`openai/gpt-image-2` its chain head on 2026-09-04.

- **The image `--dry-run` example passed `--quality standard`**, which that
  model rejects at submission — HTTP 400, `Supported values are: 'low',
  'medium', 'high', and 'auto'`, nothing billed. The example pins no
  `--model`, so it resolved to the new head and a user copying the shared
  spec's own command hit an immediate error. It passes `high` now.
- **"When there is no estimate" said to relay the ROUGH figure without saying
  what that figure is scoped to, and that is a defect in the gate rather than
  a typo in an example.** A ROUGH figure is only valid for the
  `--quality`/`--size` pair its anchor was measured at, and at the time of
  writing the script did not compare that pair against the request — it
  looked up one count per model and printed it either way. (`ofox-image-core`
  1.7.0, later the same day, made the lookup pair-aware; see 1.15.0's
  approval-gate bullet for how this section reads now.) Measured 2026-09-04:
  `openai/gpt-image-2` spends
  196 output tokens at `low` / `1024x1024` and **5063** at `high` /
  `1792x1024`, about 0.6 cents against 15.4, and a real approval table quoted
  the 0.6-cent figure for a frame that billed 15.4. The section now states
  that there is no flat per-image price, tells the agent to read the anchor's
  own `quality` and `size` fields before relaying the line, and to declare an
  unmeasured pair as unmeasured instead of interpolating between two that are
  measured. An understated figure in the table is the one outcome this file
  exists to prevent.

## 1.14.0 — seven real clips' worth of measurements folded into the two shared references

Docs only; no script changes. Eight jobs produced between 2026-09-03 and
2026-09-04 (five short dramas, one anime shot, two product ads, about $36 of
generation) had their findings sitting only in the case records that shipped
with them. This release moves the cross-scenario half of those findings into
`prompt-structure.md` and `api-params.md`, where the skills that need them
already point.

- **`prompt-structure.md`, "Several shots in one job"**: the two-job section
  is now **"Past that envelope: six jobs, and what the mix does to a
  boundary."** The measured envelope inside one job grows from three shots in
  eight seconds to **10 shots in 30 seconds with up to 6 hard cuts**, at 480p
  and 720p, **with or without an attached first frame** — the image-plus-cuts
  combination (`7ae7d49e-7eb9-4165-9d95-09cd525d53ed` at 15s/5 shots/4 cuts,
  `ac927785-92ef-4e28-97b9-ff8172ec5554` at 20s/7 shots/6 cuts) had no
  measurement here before and is the normal shape for three scenario skills.
  Dialogue in several shots of one clip is covered too
  (`036ac3a8-6f68-47ad-a553-86a29aa3e5b8`, five lines over seven shots).
- **The transition-mix rule is upgraded from a two-sample hypothesis to a
  direction, with the sample count still on it.** Ordered by hard-cut share:
  3-of-9 lost all three hard cuts, while 3-of-8, 3-of-6, 5-of-7, 4-of-4 and
  6-of-6 kept every one. Five consistent samples against one is enough to act
  on — weight the mix toward hard cuts when a cutting rhythm matters — and
  still not enough to name a threshold, since the gap between the failing and
  passing cases is a single boundary.
- **New "Checking the cuts: read frames, never a detector count alone."**
  Scene detection at threshold 0.3 cannot see a cut between two shots in the
  same place under the same light, which is exactly shot/reverse-shot. It
  missed the pivotal cut in two accepted clips (`41f87ac7` at 9.5s,
  `036ac3a8` at 9s) and under-reported two more (`7ae7d49e`, `ac927785`). A
  count is where a check starts, not where it ends.
- **New "Unwanted text is designed out of the set, not forbidden in the
  list"** under "Consistency locks and the negative list". `no legible text`
  written as strongly as it can be still returned sign-like shapes on a neon
  street (`41f87ac7`), while a New Year courtyard with couplets in five of
  seven shots stayed clean by composition alone (`036ac3a8`) and two studio
  ads with no surface for lettering to sit on returned zero invented text.
  The negative list is a backstop; the set is the defence.
- **New "Asking for music can fail output moderation on copyright"** under
  "Dialogue and sound". A prompt asking for a cello note and a bell chime
  came back `failed` / `output_moderation_failed` with `the output audio may
  be related to copyright restrictions` (`1ff72400-0f30-4be1-a417-f52d43955d09`,
  **not billed**); the same ad with recorded sound only passed. One sample,
  so the trigger is not pinned down; the workable form is written out.
- **New "What a frame lock actually holds, measured"** under "Reference
  assets as visual anchors". A `--frame-first-image` holds appearance for the
  whole clip, not just the opening instant: no drift over 20 seconds, across
  six hard cuts, or while a person is in frame for seven or eight seconds of
  it (`ac927785`, three-way frame comparison). It is also the reliable way to
  get specific lettering into a clip. And the image file's real pixels have
  to be measured and cropped — requested size, reported size and file size
  were three different numbers on all three image runs behind the section.
- **`api-params.md`, the real-person section**: the refusal is now stated as
  a rule about **the attached picture only**, with a four-row evidence table.
  A non-photoreal frame passes (`16023efe-48d6-45fe-8fd8-f5c6fbfe6519`), a
  photoreal person generated from prompt text passes (five 20–30s jobs), and
  the two combine — an object-only frame plus a person written in text
  (`ac927785`). `--real-person true` on 2.5 remains untested and is now
  labelled as something that must not be described as a workaround.
- **`api-params.md`, the `output_moderation_failed` row** records the audio
  trigger with its job id.
- **`prompt-structure.md`, "Shot density, measured per case"**: the one-take
  registers get the failure mode that matches the static-cut-list one already
  there — a 20-second single take whose only movement was a very slow push
  was rejected as inert (`16023efe`), where the accepted gallery one-takes all
  cross space.
- The "Quick checklist" items on transitions, real people, endings and the
  closing line now carry these, so a prompt written straight off the
  checklist inherits them.

## 1.13.0 — a second finding on hard cuts, and a second round for a published deliverable

Docs only; no script changes. Both additions trace back to one accepted-but-
flagged clip: the first 720p `seedance-short-drama` job made on the 1.12.0
references (2026-09-03, job `4e5c9581-d462-443b-9663-b1aa6d72f527`, 30s, ten
shots, $7.20) obeyed every rule these two shared files already stated and
still drew four specific complaints from the repository owner — a plain
back half, a compressed climax, seconds wasted on transitions, and a request
for more say in the brief before the job runs.

- **New "Two 30-second jobs past that envelope: the mix, not the label,
  decided" under "Several shots in one job."** The existing envelope
  (three shots in eight seconds) said nothing about longer timelines with a
  mix of hard cuts and named continuous transitions. Two 30-second jobs fill
  that gap and contradict each other on the one claim either alone would
  support: job `844c9145-9b10-4335-9fdc-ec4937793a2f` (8 boundaries, 3 hard
  cuts against 5 continuous) had every explicit label render as written; job
  `4e5c9581-d462-443b-9663-b1aa6d72f527` (9 boundaries, 3 hard cuts against
  6 continuous) had **zero** of its written hard cuts detected at threshold
  0.3 — the whole clip read as one continuous flow. Stated as a working
  hypothesis from two samples, not a threshold: a boundary's rendering isn't
  decided independently of the rest of the timeline, so a timeline weighted
  toward continuous transitions can soften an explicitly labeled hard cut
  too.
- **`creative-brief.md` now allows a second round of up to four questions
  when the deliverable is published** (a page asset, a client deliverable,
  anything the user describes that way) rather than previewed once and set
  aside. The second round is reserved for a new class of axis —
  **"Pacing questions belong in round two"**: duration split, ending
  length, slow motion/freeze frame use, density of the standout segment, and
  hard-cut share — all five of which every scenario skill previously left
  entirely to the agent's own judgement, by default, with no question and no
  approval step in between. The flow diagram and anti-pattern 1 were updated
  to match; a follow-up (branch-triggered) and a round two (published-tier)
  are now two different, both-legitimate reasons to ask again.

`seedance-short-drama` 1.9.0 is the first scenario skill to wire the new
round-two axes into its own question table (`Pacing`, `Effects`) and to add
its own "Duration budget" section with concrete second counts. The other
three scenario skills were audited for the same duration-imbalance risk in
the same pass: `seedance-product-video` needed a related fix (its own
1.8.0 entry — a template whose segments didn't scale with `--duration`);
`seedance-ad-creative` and `seedance-anime-drama` did not change, because
their existing templates already bound their equivalent risk (a one-second
cap on the ad climax's slow motion already in the template text; an
escalation-driven segment structure for anime that does not front-load a
static setup or close).

## 1.12.0 — `prompt-structure.md`: shot density measured per case, and the transition choice made visible

Docs only; no script changes. Both additions come from a real failure: the
first short-drama clip generated with the 1.11.0 references (2026-09-03, job
`38ca8311-5b2d-47d5-a45d-e8ebea0e6312`, 20s at 480p, four static shots, cuts
landing where the timestamps said) obeyed every rule in this file and was
rejected as too plain to publish. Two of those rules were discoverable only
by an author who already knew to look for them.

- **New "Shot density, measured per case" under "Segmenting the timeline".**
  The existing "Segment length" gave ranges; this gives the per-case counts
  they were read off, which is what a draft can be compared against: case 11
  at 10 shots in 24s (2.4s each), case 34 at 13 cuts in 30s, case 1 at 9 in
  30s, case 18 at 8 in 30s, case 14 at 9 `CUT`s, case 22 at 6 in 30s, case 15
  at 5 in 20s — and the one-takes counted the same way, cases 8, 6, 2 and 3
  with zero cuts but a movement phase every 6–8 seconds. Two findings stated
  outright: among prompts that cut, nothing collected holds a cut shot longer
  than about five seconds; and **a timeline of 5-second shots with a static
  camera in each is the one shape the gallery does not contain** — which is
  precisely what a scenario template's defaults produce when nobody chooses a
  register. The narrow Ofox-verified envelope (three shots in eight seconds)
  is restated next to it so a denser count is priced as an experiment.
- **The transition choice is now on the skeleton.** "Skeleton to copy" gained
  a `TRANSITION` line between beats, pointing at "Transitions" and saying
  that an unnamed boundary renders as a hard cut. The nine kinds were already
  documented in full; what was missing was any prompt to use them at the
  moment a timeline is being written.
- **Checklist items 3 and 4 tightened**: item 3 now asks for a shot count
  that matches the register rather than a template's floor, and item 4 asks
  for a transition kind named at each boundary on purpose, not only for the
  timestamp's meaning to be declared.

## 1.11.0 — two shared references for every Seedance scenario skill: prompt structure and the creative brief

- **New `references/prompt-structure.md`**: how to structure the text that
  goes into `--prompt`, distilled from the 63-prompt Seedance 2.5 gallery (24
  ByteDance first-party, 39 community). The vendor's own formula and worked
  example; the header-manifest -> timeline -> closing-block skeleton; when to
  timestamp (56% of prompts do; 78% of 16–30s ones), which formats are in use
  and how long a segment runs; the two things a timestamp can mean; transition,
  camera, pacing and ending vocabularies; consistency locks and negative lists;
  dialogue density in two tiers; and the two meanings of an attached image —
  first-frame lock (`--frame-first-image`) versus identity reference
  (`input_references` through `--extra-json`) — with the API constraints that
  decide between them. Every entry carries the case numbers it was observed
  in, and the file says up front that frequency is not effect.
- **New `references/creative-brief.md`**: the other half of the same job —
  what to ask the user *before* a prompt exists. The three tiers (must-ask /
  ask-if-open / never-ask) and why a never-ask axis belongs in the cost table
  rather than in a question; one `AskUserQuestion` round of at most four
  questions with at most one branch follow-up; zero questions as a legitimate
  and common outcome; the shape of a question (12-character header, a
  recommendation first, visibly different pictures, no hand-rolled "Other");
  the three rules for "Let the AI decide" (always last, never pre-selected,
  resolves to a concrete value marked `(AI's pick)`, and a blanket "you
  decide" never covers must-ask); the generic skip rows (platform words to
  ratios, an attached asset, a repeat request in one session); the rule that
  every answer must be findable in the prompt or a flag; the order with the
  approval gate and the recap format; the fallback for a runtime with no
  `AskUserQuestion`; and ten anti-patterns. Scenario vocabulary is
  deliberately absent — each scenario skill supplies its own question set,
  inference rows and recap example.
- **What callers do**: nothing changes in the script or its flags. Scenario
  skills load `references/prompt-structure.md` before writing a prompt and
  `references/creative-brief.md` before asking anything, and link both
  instead of restating them, the same way they link `approval-gate.md`. The
  1.7.0 releases of `seedance-short-drama`, `seedance-anime-drama`,
  `seedance-ad-creative` and `seedance-product-video` do so and keep only
  their scenario-specific template and question set.
- **"Several shots in one job" carries a real-run record, not a
  placeholder.** Prompt text cannot show whether a video honoured its cuts,
  so the section was drafted with a `VERIFY-MULTICUT` marker and then filled
  from two paid `bytedance/seedance-2.5` runs on `byteplus` (2026-09-03, 8s,
  480p, three shots each). Both cut where the timestamps said, to about ±1s,
  in bare-timestamp and in manifest + `SHOT N` notation, and one character
  survived three shots on text alone. The subsection also lists what those
  runs did not cover — 30s or 8+ shots, dialogue across a cut, resolutions
  other than 480p, `volcengine` — so scenario skills can say "verified" only
  where it is.
- **`SKILL.md`'s `chain` section no longer opens on the claim this release
  disproves.** It began "One job is one continuous take, so a sequence means
  several jobs", which contradicted the new reference and the four scenario
  skills. It now says a job is one 4-30s clip that can hold several
  timestamped hard cuts, and frames `chain` as continuity *across* jobs — for
  a sequence past the duration ceiling, or when each shot needs its own
  approval, seed or resolution — with the two mechanisms combinable rather
  than alternatives. The commands and verified-behaviour notes below it are
  unchanged. Also corrected in the real-person subsection: what
  `seedance-anime-drama` reuses across shots is a generated frame of the
  character, not a character sheet — that skill's 1.7.0 forbids feeding a
  design sheet to `--frame-first-image`.
- `SKILL.md` links both files from "For scenario skills built on this", one
  subsection each, and names the division of labour between the three shared
  references. No behaviour change and no test changes; the one edit inside
  `ofox-video.sh` is `cmd_chain`'s header comment, which opened on the same
  retired claim — left alone, it is where the next maintainer would read it
  back out and re-propagate it.

## 1.10.0 — one approval gate, shared by every skill in this repo

- **New `references/approval-gate.md`**: the single spec for "never spend
  before an approved cost table". Required columns, where the numbers must
  come from (`--dry-run`, never the agent's own arithmetic), how to itemise a
  batch, what to do when no estimate is possible, and how a two-phase image →
  video flow splits into two approvals.
- The four `seedance-*` skills each carried their own prose version of the
  same rule, which is a guarantee of drift. They now link this file and keep
  only what is scenario-specific.
- `SKILL.md` links it from "Quote the price before you spend it" and from the
  guidance for scenario skills built on this one. The script's mechanics are
  unchanged — no behavior change here, only where the rules are written down.

## 1.9.0 — surface the keyless price check; stop leading with a misleading rate

A third role-play review, this time as a non-programmer with no Ofox account,
no API key, and an explicit fear of an accidental bill — starting at the
README rather than at SKILL.md.

Its main finding was not a bug: **the strongest thing this repo can offer that
reader already worked, and nothing told them it existed.** `--dry-run`,
`models` and `providers` all run with no API key, so a job can be priced
before signing up. The docs never said so; the *Availability check* section
implied the opposite order (check first, then go get a key), which sends
someone to a signup form before they know whether this costs $0.44 or $7.20.
The one accurate statement lived in a source comment nobody reads.

- `SKILL.md` leads with the keyless price check and says to quote first,
  point at signup second.
- `check` now separates *present* from *valid*: it makes no network call, so a
  typo'd key passes it and fails on the first real request. It says that. And
  when no key is set, it names the three commands that still work rather than
  dead-ending.
- **`models` shows each model's default-resolution rate**, labelled with that
  resolution. It printed `pricing.output_video_per_second` — for
  `seedance-2.5` that is the 480p rate ($0.11) while the model defaults to
  720p ($0.24). The reviewer's persona multiplied the first big number by 15
  and was off by 118%. `pricing.md` already warned never to quote that field,
  so the repo knew it misled and showed it anyway.

Tests: `references/test/newuser.test.sh`, 22 cases, all free.

## 1.8.0 — `create`, and fixes for three defects 1.7.0 introduced

A second role-play review — a sub-agent given only the SKILL.md files and told
nothing about the previous round — confirmed 1.7.0's fixes landed (it read the
dry-run flow out of the docs unprompted) and found twelve more issues. Three
were introduced by 1.7.0 itself.

**The timeout trap (the worst one).** `generate` blocks for up to
`--max-wait` seconds, default 540. Claude Code's Bash tool defaults to 120 and
caps at 600. A tool call dying mid-poll lands in the one state that actually
costs someone something: job created and billable, id never printed, no way to
recover it. `batch --takes 4` is worse — 36 minutes worst case, more than any
single tool call can be given — and 1.7.0 had just finished recommending
`batch` in all four scenario skills.

- **New `create` subcommand**: submits and returns the job id in seconds, no
  polling. `poll` already existed, so `create` → `poll` → `poll` is now a
  path that no short timeout can strand. `generate` is unchanged for callers
  that can wait.
- Documents the real duration expectations, the `takes x max-wait` arithmetic
  for `batch`, and lowering `--max-wait` for short drafts.

**Introduced by 1.7.0, now fixed:**

- `batch --dry-run` printed **two** `Estimated cost:` lines — the second was
  the inner validation call leaking its own per-take figure, which is exactly
  the number two documents tell you not to quote, right after promising
  "exactly one line". Inner stderr is now captured and only surfaced on error.
- Dry runs said "Actual billing is reported below" with nothing below.
- `--dry-run` required `OFOX_API_KEY` despite sending no authenticated
  request, so someone without a key could not even be quoted a price —
  against this repo's own fail-open rule.

**Pre-existing, also fixed:**

- `check` exited **1** on a missing key while the exit-code table defines 1 as
  "fix the flag and retry freely" and 2 as an environment error. Now exits 2.
- `--dry-run` did not validate `--out-dir`, so a bad path passed the free
  check and then cost a real job before failing with exit 6. Now resolved and
  checked during the dry run.
- **`batch` now assigns and prints a seed per take.** Takes differed only by a
  seed the API picked and never disclosed, which made "render take 3 properly"
  impossible — the workflow both SKILL.md files recommend. The `TAKE` line
  carries `seed=N`, and the summary shows the command to re-render one.

Tests: `references/test/create.test.sh`, 16 cases, free by construction.

## 1.7.0 — `--dry-run`, so a price can be quoted before it is spent

A sub-agent given only the SKILL.md files, asked to role-play delivering a
video, found that the documentation asked for something the script could not
do. The scenario skills said to relay the estimate the script prints — but
that estimate is printed five lines before `curl -X POST`, so by the time an
agent could relay it, the job existed and was billable. There was no
`--dry-run` anywhere in the script. Following the docs literally meant billing
someone without warning.

- **`--dry-run` on `generate`, `batch` and `chain`.** Parses arguments,
  validates every parameter against the model, resolves the upstream, builds
  the payload, prints the estimate — then stops. Nothing submitted, nothing
  billed, exit 0. A bad parameter now costs a message instead of a job.
- **An `Estimated cost:` line always prints.** It used to be wrapped in
  `if [ -n "$duration" ]`, so omitting `--duration` produced complete silence.
  Silence is the one outcome an agent cannot relay: it can repeat a number and
  it can repeat "unavailable", but it cannot notice a line it was never told
  to expect. Missing duration now says so explicitly.
- **Human-facing lines round to 2 decimals.** The batch summary read
  "That is $0.6400000000 for 4 takes" — a line written for a person, carrying
  ten decimals. `VIDEO_COST` and `BATCH_COST_TOTAL` keep the exact API string,
  because those are the machine contract and the billing record.
- **`BATCH_COST_PER_TAKE` guidance rewritten.** It called that field "the
  number that matters" and then said the number that matters is the total —
  two different fields in one sentence. `BATCH_COST_TOTAL` is what to quote:
  if one take in four is usable, that clip cost the whole total, and the
  per-take figure understates it 4x.

Tests: `references/test/dryrun.test.sh`, 19 cases, free by construction —
`--dry-run` makes no network call at all.

## 1.6.1 — fix: video-to-video was quoted at the text-to-video rate

The estimate added in 1.5.0 detected v2v by looking for `type == "video"` in
`input_references`. The API's actual value is **`video_url`**, so a v2v job was
priced at the t2v tier and the user was quoted low — a real run estimated
$0.44 and billed $0.56, 27% more. 1.5.0 existed to stop wrong estimates; this
was that exact failure inside the feature meant to prevent it. Both spellings
are accepted now.

The same run corrected a claim of ours that had never been measured:
`api-params.md` said `usage.video_seconds` "includes v2v input duration when
applicable". **It does not** — a 4s input with a 4s output billed 4 seconds,
not 8. The extra cost of v2v comes from the rate, not from counting the input.

Also documents, now that a real request has confirmed them: the
`input_references` element shapes (`image_url` / `audio_url` / `video_url`),
that a video reference must be a **URL** with no local-file path (unlike
`frame_images`), and that a completed job's `unsigned_urls` link works as one.

And states what the run did **not** settle: the output opened on nearly the
input's closing frame, but a motionless cup cannot distinguish "continues from
the last frame" from "restages a similar scene from a style reference". No
claim is made either way. For multi-shot continuity `chain` is better on every
measured axis — cheaper, takes local files, anchors on a real frame.

## 1.6.0 — `chain`: multi-shot sequences with real visual continuity

One job is one take, so a sequence meant several jobs that shared nothing and
drifted apart. `chain` feeds each shot's closing frame into the next as its
opening frame.

**Verified with a real paid run, which is the only way this could be settled.**
Shot 2 opened on very nearly the exact frame it was fed — cup position and
scale, window frame, table grain, light direction all carried over — then
followed its own prompt. Real continuity, not just matched framing. Brightness
shifts slightly across a seam.

- `chain --shot "..." --shot "..."`, or `--shots-file` with one prompt per
  line (blank lines and `#` comments skipped). Capped at 10 shots.
- Estimates the sequence up front; reports real per-shot cost and the total.
- **Stops on first failure**, keeping and reporting completed shots.
- Joins finished shots into one file (`--no-concat` to skip), re-encoding only
  when codecs differ. Fails open — no join, never a lost shot.
- Requires ffmpeg and **checks before submitting anything**, so a missing
  dependency can't cost a paid shot.
- New `last-frame VIDEO` subcommand: pull a clip's closing frame. No API call,
  no key, no cost. Grabs just before the end, since the literal last frame is
  often a fade.

### Found by the same run: real-person references are refused

`bytedance/seedance-2.5` image-to-video rejects a reference frame containing a
real person — `HTTP 400 / input_moderation_failed`, "may contain real person".
Nothing generated, nothing billed. So chaining works for products, landscapes,
illustration and anime, and **not** for live-action human sequences on this
model. This is also why `seedance-anime-drama` can reuse a character sheet
while a short-drama sequence cannot.

`input_moderation_failed` is now mapped (it previously fell through as
"unrecognized error code") and names both options: a non-photoreal reference,
or `--real-person true` — which Ofox documents for `bytedance/seedance-2.0`
and which is **untested on 2.5**, so the message says so rather than implying
a fix.

Tests: `references/test/chain.test.sh`, 18 cases, free by construction —
frame extraction is verified against a locally synthesized clip.

## 1.5.0 — cost estimates come from the live catalog, not a hardcoded table

The estimate shown before someone spends money was built from a 15-line `case`
of prices hand-copied off model pages two days earlier. It would have gone
wrong silently on the next repricing — and several of those rates are
promotional right now (Seedance 2.0 at 10% off, 2.0-fast at 30%, 2.5's 1080p a
time-limited $0.48 against a $0.60 list), so "the next repricing" is not
hypothetical. A wrong estimate is worse than no estimate.

- Rates now come from `provider_cards[].pricing.video_pricing.tiers[]` on the
  public, keyless catalog endpoint, via the same cache added in 1.4.0. Fallback
  ladder: fresh cache -> live -> stale cache -> bundled `pricing-snapshot.json`
  -> **no estimate**. That last rung is deliberate: the script never prints a
  number it cannot back up, and never blocks a run over pricing.
- **`generate` now estimates too**, not just `batch`. On stderr, so the
  `KEY VALUE` stdout contract is untouched.
- The resolution used for an estimate defaults to the model's own
  `default_resolution` instead of an assumed 720p.
- Image-to-video is priced at the **t2v** tier; only a video input moves it to
  v2v. (Confirmed earlier by a real i2v run billing 4s x $0.11 at 480p.)
- When a provider is pinned, the estimate reads that provider's own card.
  Prices matched across upstreams when measured, but that was an observation,
  not a contract — now the number follows if it ever stops being true.
- `references/pricing.md` no longer presents itself as the runtime source. It
  keeps the cheap-vs-expensive ladder (the argument for `batch` survives any
  repricing) as a dated snapshot, and points at `providers` for live numbers.
- `refresh-snapshot.sh` now regenerates the pricing snapshot as well.

Tests: `references/test/pricing.test.sh`, 14 cases, free by construction —
estimates print before anything is submitted.

## 1.4.0 — pin Seedance to the byteplus upstream

**Behavior change.** Seedance jobs now go to the `byteplus` upstream by
default. They previously went wherever Ofox's weighted routing sent them,
alternating unpredictably between BytePlus and Volcengine Ark.

Why it matters: Ofox states outright that with no `provider` field, "which
provider serves any single request is not predictable" — and the two upstreams
**moderate differently**. So an unpinned job that came back
`output_moderation_failed` may simply have landed on the stricter one, with
nothing for the user to point at. Pinning makes results reproducible.

- **New `--provider SLUG`.** Was previously reachable only by hand-writing
  `{"provider":{"type":"..."}}` into `--extra-json`, which nothing documented.
  `--provider auto` sends no pin; `OFOX_VIDEO_PROVIDER` sets a persistent
  default; an explicit flag beats the environment variable. `batch` forwards it.
- **Only multi-upstream models are pinned.** Measured across all eight video
  models: the four `bytedance/seedance-*` are served by `byteplus` +
  `volcengine`, the four `alibaba/*` by `aliyun` alone. Single-upstream models
  get no pin — routing is already deterministic there, and hardcoding it would
  only add a fact that can rot if they later gain a second upstream.
- **The default costs no network call** — it is a prefix rule, accurate per the
  measurement above, not a lookup.
- **Pricing is identical across upstreams** (verified tier by tier). This is a
  region and moderation choice, never a cost one; the docs now say so, so
  nobody assumes there is money in it.
- **Validation**: an unknown slug is rejected locally; a real slug that doesn't
  serve the chosen model is rejected too, naming the ones that do — but only
  when catalog data is at hand. An unreachable catalog never blocks a request.
- **Two error codes mapped**: `invalid_provider_type` and
  `provider_type_unavailable`, both pointing at `--provider auto`.
- **`output_moderation_failed` guidance now names the other upstream** as a
  remedy alongside changing the prompt. The rejected job was never billed and a
  retry is a new request, not a resubmission.
- **New `providers [MODEL]` subcommand**: a model's upstreams and their full
  price matrix, from the public keyless catalog endpoint. No API key needed.
- **New `--print-payload`**: dump the request body to stderr before sending.
  The API key is in a header, never the body, so this leaks nothing.
- The submit line now names the upstream:
  `Submitting job to Ofox (model=..., provider=byteplus)`.

Tests: `references/test/provider.test.sh`, 27 cases, free by construction.

## 1.3.0 — `batch` takes with real per-take billing, `contact-sheet`

- **New `batch --takes N`**: N takes of one prompt, each its own job, run
  through the same path a single `generate` uses — so the no-resubmit rule
  holds for free and no take can be double-billed. Prints an estimate before
  spending, then a real total and `BATCH_COST_PER_TAKE` built from each job's
  own `usage.video_cost`. Cost-per-*usable*-take is the number that actually
  matters when you generate several and keep one.
- A failed take **stops the run**: takes after it are not submitted, since
  whatever broke one will likely break the rest and each attempt costs money.
  Completed takes are still downloaded and reported (exit 3 for a partial run).
- Warns when `--seed` is fixed across takes — you would be paying N times for
  N identical clips. `--takes` is capped at 10 per run.
- **Contact sheet**: three frames per take tiled one row per take, so a human
  picks a winner from one image. Uses `ffmpeg` only (its `tile`/`vstack`
  filters — no ImageMagick dependency). Fails open: no ffmpeg means no sheet,
  stated plainly, videos untouched. `--no-contact-sheet` to skip.
- **New `contact-sheet VIDEO...` subcommand**: build a sheet from videos
  already on disk. No API call, no key, no cost.
- Reported sheet paths are absolute even when `--out-dir` was relative.

Verified with a real run: 3 takes on `seedance-2.0-mini` at 480p/4s, billed
$0.24 total ($0.08/take) exactly matching the estimate, contact sheet rendered.
That run also exercised the no-resubmit rule for real — polling hit two
`curl 35` failures and the script retried the *poll*, never the create.

## 1.2.0 — per-model validation, `models` subcommand

- **Parameters are validated against the model you actually chose.** The old
  hardcoded tables were wrong three ways, each verified against live
  `GET /v1/models` data:
  - `--aspect-ratio` accepted `3:2`, `2:3` and `9:21`, which `seedance-2.5`
    rejects. Those passed local validation and spent a round trip to come back
    as a generic `invalid_request`.
  - `--duration` was only range-checked when the model was literally
    `bytedance/seedance-2.5`. The other seven video models got no check at all,
    despite every one having a different range (`wan-*` 2-15s, `happyhorse-*`
    3-15s, `seedance-2.0*` 4-15s).
  - `--resolution` accepted `1K`/`2K` (no video model supports either) and
    rejected `4k` (which `seedance-2.0` supports, lowercase in the API).
  Errors now name the model and list that model's own legal values.
- Image-to-video is rejected up front for models whose `modes` lack `i2v`.
- **New `models` subcommand**: lists every video model with its real limits and
  base per-second price. Needs no API key — `GET /v1/models` is public — so it
  is safe to run before signing up, and it costs nothing.
- **Model data is fetched, not hardcoded**: fresh cache (24h, under
  `XDG_CACHE_HOME`) → live fetch → stale cache → bundled
  `references/models-snapshot.json`. Each fallback is announced on stderr,
  never silent. If no list can be had at all, validation falls back to the
  union of every model's values rather than blocking a request that would have
  worked. `OFOX_SKIP_MODEL_VALIDATION=1` skips per-model checks entirely.
- An id missing from a **live** list is rejected locally; missing from a
  **snapshot** it is deferred to the API, since the snapshot may simply predate
  the model.
- New `references/refresh-snapshot.sh` to regenerate the bundled snapshot, and
  `references/test/validation.test.sh` — 36 cases, all free by construction.
- Frontmatter: top-level `version` and `metadata.openclaw.homepage`/
  `envVars`/`primaryEnv`, which is what ClawHub's publish scanner reads.
