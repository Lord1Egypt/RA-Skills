# Changelog

All notable changes to the **product-demo** skill. Versioning follows SemVer.

## 2.0.0 — every real-run command carries `--approved`, and the core refuses without it

**Breaking, and the break is upstream.** `ofox-video-core` 2.0.0 makes its
four billable subcommands — `generate`, `create`, `batch`, `chain` — refuse to
run unless `--approved` is on the command line. This skill's one real-run
`generate` command now passes it. The `--dry-run` commands are untouched: a
quote is how the number being approved gets produced, so gating it would close
the only route through itself.

**What a caller has to do differently**

- **Install `ofox-video-core` 2.0.0 or newer.** This version of this skill
  needs it. On an older core the updated commands stop with `unknown option
  '--approved'` before any request — nothing is submitted and nothing is
  billed, so the failure is safe, but every real run fails.
- **A command copied from an older version of this file is now refused.**
  Anything pasted from an earlier revision, a transcript or a wrapper script
  hits the guard, prints the quote-first steps and exits non-zero. Nothing is
  submitted and nothing is billed. Re-run it with `--dry-run` to get the
  quote, or with `--approved` once the cost table has gone in front of the
  user.
- **The `batch` route needs it too.** This file shows only `batch --dry-run`;
  its real run takes `--approved` in the same place.

**What `--approved` is not.** It does not prove that an approval happened — an
agent can type it without showing anyone a price, exactly as it could
previously just run the command. What changed is that spending without quoting
is no longer the default: it now has to be written into the command, where a
transcript shows it and a reviewer can object. The gate in
[`../ofox-video-core/references/approval-gate.md`](../ofox-video-core/references/approval-gate.md)
is still the rule, and this skill still states it in full.

**Documentation only otherwise. No price, default, prompt template, flag
meaning or generation behaviour changed.**

## 1.1.2 — the recovery command asked for the whole repo, and asked the agent to run it

**Documentation only. No flag, price, prompt template or generation behaviour
changed.**

"If the script isn't found" ended in a skills.sh command that installed *every*
skill in this repo, into *every* agent, user-level, with confirmation
suppressed — four widenings past the one skill that was actually missing.
ClawHub's scanner flags exactly that (rule T08, "unpinned and overbroad
third-party installation via npx"), and the flag is accurate rather than noise:
an agent that read the line and ran it would have rewritten the user's whole
skills setup to recover one relative path.

The line now asks for the missing skill and nothing else —
`npx skills add ofoxai/skills --skill ofox-video-core`, which asks for that one
skill and answers none of the agent, scope or confirmation questions on the
user's behalf. The repo's own `npx ofox-skills ofox-video-core` still answers
all three (every agent, user-level, no prompts), which is why the line handed
to the user is the skills.sh one.

**What a caller has to do**: nothing changes for any command this skill
already prints, and nothing changes while `ofox-video-core` is installed. What
changes is conduct on the one path where it genuinely is absent — **relay the
command and let the user run it**; do not run an installer yourself. An
install writes outside the working directory, and that is not a decision to
take silently for someone.

All three distribution routes are still named (this repo's own
`npx ofox-skills`, skills.sh, and LobeHub or ClawHub), because recovery advice
that names one installer is wrong advice on every other channel this skill
ships through.

## 1.1.1 — the borrowed timing claim is withdrawn

**Documentation only. No default, price, prompt template or behaviour
changed.** Nothing measured *in this skill* moved; what moved is a claim this
file borrowed from its sibling.

"The timing, from the sibling scenario" told callers to plan for
`it settles early and then holds`, from `keyframe-animation`'s job `259c3ce2`
(~53% of the distance in the first quarter, arrival at 3 of 4 seconds). A
second run on that mechanism (`1b7a3fab`, 5s) came back near-linear, arriving
at 4.5 of 5 seconds with about half a second of tail. Two clips, two curves,
four variables different between them — so there is no curve to plan against,
and the sibling has withdrawn the claim at source (`keyframe-animation`
1.2.0).

**What a caller has to do differently:** stop promising a hold at the end, and
stop justifying a longer `--duration` as buying one. Plan for the final state
to be **reached and legible** — which is this skill's actual deliverable and
is measured, twice, on its own clips. If the length of the tail matters, draft
it cheaply and look.

This file's own observation is unchanged and still stands: its clips were
crisp and settled by t=2.0s of 4 seconds. What was wrong was treating
"compatible with an early settle" as evidence for a curve. The `--duration`
row in the defaults table now gives the bill as the reason to stay at the
model's minimum, rather than a hold nobody can predict.

## 1.1.0 — a face in a capture is no longer a flat dead end, and cropping is still the answer

Three places in `SKILL.md` said `--real-person true` was untested on
`bytedance/seedance-2.5`. It was measured on 2026-09-16 and it lifts the
refusal, so those three lines were wrong and are fixed. Minor rather than
patch, because the guidance around a flag changed.

**The measurement lives in `ofox-video-core`, not here.** This file links to
[`api-params.md`](../ofox-video-core/references/api-params.md) → the
real-person section rather than restating a single-variable A/B in a third
place, which is the same convention this skill already follows for the prompt
craft, the brief and the spend rule.

**The wording is fixed and is the point of the release.** `--real-person true`
is Ofox's privacy-preserving preprocessing path for real-person references the
user is **authorised** to use — an authorisation route, never a way past the
check. Nothing in this skill describes it as a flag that gets a rejected
capture accepted.

**The edit is deliberately small, because this scenario barely has the
problem.** The input here is captures of a user interface: a photoreal face
shows up as a profile picture, a testimonial block or a customer photo, and
**cropping it out costs nothing and is almost always right**, because the face
is essentially never the subject of a UI demo. So the flag is recorded as a
measured alternative and explicitly as the heavier one, in the capture
checklist, the `--real-person` default row, and the `input_moderation_failed`
failure row. It has not been promoted into a feature, a question in the brief,
or a recommended default, and it should not be.

## 1.0.1 — it happened a second time, through this file's own template

1.0.0 shipped saying this skill rested on **one** measured job. It rests on
two. No prompt, flag or default moved — what changed is that a measurement got
recorded — so this is a patch.

**Job `427278b4`** (2026-09-15), `bytedance/seedance-2.5`, 4 seconds, 480p,
again **44 cents billed**: same model, duration, tier and input pair as
`5e59baa2`, with the prompt filled in from this file's template by an agent
working from this skill and nothing else, so what that run exercised was the
skill rather than the API. The delivered clip's final frame renders all four
changed values correctly and legibly (`Business`, `$99.00`, `25`,
`Manage seats`), the layout is identical to the input capture, nothing drifted
and nothing was invented.

That matters more here than a replication usually would: a seed does not
reproduce a take on this API, so the second run is a genuinely independent
sample rather than a re-roll of the first.

`SKILL.md` was rewritten around it. The evidence section gained an "It
happened twice" heading and says what the second run adds and what it does
not; the parameter defaults cite both jobs; the draft check is marked as
having been run on both; the two text-failure rows in the troubleshooting
table name which job each observation came from; and the cost anchor reads 44
cents **twice**, on `5e59baa2` and `427278b4`, rather than once.

What this release deliberately does **not** claim: that the second run widened
anything about the inputs. Same pair, so it is a replication, not a
broadening. Everything 1.0.0 declined to claim — a pair differing in many
places or in layout, a model other than `bytedance/seedance-2.5`, a pointer or
cursor — it still declines to claim.

## 1.0.0 — first release

A scenario skill for turning two screenshots of one interface into a short
demo clip: the before state is attached as the first frame, the after state as
the last frame, in one `ofox-video-core` job.

**This scenario was expected to fail, and the test said otherwise.**
Generative video models fabricate text, a UI is almost entirely text, and
every other scenario skill in this repo carries an `AVOID: subtitles,
on-screen text` line for that reason. Job `5e59baa2`,
`bytedance/seedance-2.5`, 4 seconds, 480p, 44 cents billed, fed two genuine
Chrome-rendered screenshots of one pricing panel that differed in four places
(plan name, price, seat count, button label). The delivered clip's own frames
show, at t=1.3s, the four changed values **mid-fade but correctly spelled and
correctly positioned**, the unchanged labels still solid, and by t=2.0s every
string crisp and correct. No garbling, no invented text, no layout drift.

**So this skill does not carry the blanket anti-text AVOID line**, and that is
a deliberate decision recorded in the skill itself rather than an omission.
Those lines exist for text the model has to *invent*; with both endpoints
supplied it is interpolating between two given renderings, and a blanket
prohibition on text would be pointed at the user's own interface. The AVOID
list instead forbids text-shaped things that are in **neither** capture
(tooltip, toast, badge, cursor) and text that stops being text (blurred,
doubled, malformed glyphs) — the real failure modes.

What the skill deliberately does **not** claim, because one job cannot support
it: anything about a pair differing in many places or in layout rather than in
values; anything about a model other than `bytedance/seedance-2.5` (the
catalog's `i2v` flag says nothing about locking both ends, and nothing at all
about lettering); anything about a pointer or cursor, which would be an
element in neither endpoint. Each of those is marked untested where it comes
up.

Also in this release:

- **The timing note is borrowed from the sibling job and labelled as such.**
  The front-loaded easing (about 53% of the change in the first quarter of the
  clip, arrival at 3 seconds of 4, then a hold) was measured on the motion
  clip `259c3ce2`, not on the UI clip, which was read for legibility instead.
  The practical consequence — the tail of the clip is a hold on the final
  state — is what the duration advice is written around.
- **No hardcoded model, price, resolution or duration table.** Those are
  catalog facts and the skill points at `ofox-video.sh models` / `providers` /
  `generate --dry-run` instead. The one cost figure it prints carries the
  exact parameter pair it was measured at.
- **The core-directory probe ships from day one** — an ordered candidate list
  rather than a hardcoded `../ofox-video-core/...`, so the skill works on
  LobeHub's `ofoxai-skills-<name>` layout as well as skills.sh / ClawHub /
  `npx ofox-skills`.
- **Aspect ratio written against `ofox-video-core` 1.22.0**: with frames
  attached, `adaptive` is *forced* on `bytedance/seedance-2.5` and *defaulted*
  on a model whose catalog entry lists it. The advice is to crop both captures
  to the target shape first — crop, never pad, since padding bakes the bars
  into the video — and pass no `--aspect-ratio` on any model.
- **A way to confirm both captures are attached before paying for the
  answer.** A dry run quotes the price but names only the model, duration and
  resolution, so a flag that didn't take looks exactly like a healthy quote.
  The skill points at `generate --dry-run --print-payload`, greps the two
  `frame_type` entries out of the request body, and says what one line or a
  reversed order means. No new tooling — the flag already existed and its
  output is dumped before the dry run stops.
- **`--out-dir` is stated as absolute and passed to the dry run**, which is
  where the script creates and enters it: a bad path exits `6` with nothing
  submitted, instead of after a job is paid for.
- **It says when not to buy.** A screen recording of the real app costs
  nothing and is exact; the skill raises that before quoting a job.

**What a caller has to do**: install `ofox-video-core` 1.22.0 or newer beside
this skill. `npx ofox-skills` installs every skill in this repo, which is what
keeps the sibling path resolvable.
