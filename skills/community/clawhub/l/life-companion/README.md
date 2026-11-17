# Life Companion

*[中文文档 →](README.zh-CN.md)*

> **The computation is fact. The reading is a mirror. You're the one who decides.**

A private companion that gets to know **one person** over time. Not the character-chat
kind — it computes real systems (八字, a real ephemeris, O\*NET occupation data) and
then hands you the result as a mirror, refusing to tell you what will happen.

It remembers you: a profile and a journal that live **only on your machine**, threads
it follows up on across sessions, and four lenses to read your life through —
**destiny charts · daily fortune · career fit · relationship reflection**.

One rule runs through all of it: **compute honestly, interpret humbly.** Real systems
(BaZi 八字, a real ephemeris, O\*NET occupation data) are computed faithfully, and what
they produce is a reproducible fact. What any of it *means* is a mirror for
self-reflection, **not a scientific prediction**. It invents no numbers, hands down no
verdicts, gives no medical, financial or legal advice, and when someone is in crisis it
drops the fortune-telling entirely and points them at real help.

---

## Install

Needs **Python 3.9+**. Nothing to install by hand — the scripts fetch `PyYAML`,
`lunar-python`, `pyswisseph` and `sxtwl` on first use, and say exactly what to run if
they can't (no network, PEP 668). Check with
`python3 scripts/companion.py doctor`.

**Option 1 — one line with [`npx skills`](https://github.com/vercel-labs/skills):**

```bash
npx skills add dong845/life-companions
```

It prompts for the agent and scope. Add `-g` for all projects, `-a claude-code` (or
`-a codex`) to skip the agent prompt, `-y` for non-interactive. The repository root
*is* the skill, so the whole directory is copied into your skills folder.

**Option 2 — as a Claude Code plugin** (managed updates):

```text
/plugin marketplace add dong845/life-companions
/plugin install life-companion@life-companion
/reload-plugins
```

Plugin skills are namespaced, so it is invoked as `/life-companion:life-companion`.
Two things worth knowing: if you *also* keep a manual copy in `~/.claude/skills/`
you will see the skill twice — there is no dedup, so remove one. And third-party
marketplaces do not auto-update; run `/plugin marketplace update life-companion` to
pick up a new release.

**Option 3 — clone** (best if you intend to edit it; changes take effect immediately,
which the plugin cache does not give you):

```bash
git clone --depth 1 https://github.com/dong845/life-companions.git ~/.claude/skills/life-companion
```

Whichever path you pick, your data does not come with it: the profile and journal live
in `~/.companion/`, outside the repo, and are never part of an install or an update.

---

## Using it

Just talk. There are no commands to remember. The first run collects a short,
consent-gated profile.

| You want… | Say something like | Lens |
|---|---|---|
| Your chart read | "read my BaZi — 12 Apr 1993, 7:35am, male, Beijing" | destiny |
| Today's reading / to journal | "log today and tell me how it looks" · "rough day…" | daily + journal |
| To think about work | "I'm not sure what kind of work suits me" | career |
| To make sense of a relationship | "we had a fight, help me think it through" | relationships |
| Just to talk | "help me sort out where I'm at" | journal + companion |

The four lenses are independent. You get the one you asked for, not all four.

### The four lenses

**Destiny charts — BaZi 八字, Western natal, 紫微斗数, and 合婚**
Four Pillars, day master, five elements, Ten Gods, 大运 and 流年, all computed
(`lunar-python`, with `sxtwl` independently cross-checking the 立春 year boundary). The
Western natal chart runs on a real Swiss ephemeris and omits the Ascendant rather than
guessing when the birth time is unknown. 紫微斗数 builds the twelve palaces, 命/身宫,
五行局, the fourteen major stars and 生年四化 from the standard 安星法. The output
states the caveat plainly: no second engine exists here to cross-check it.
合婚 computes the traditional branch relations between two charts and **deliberately
emits no verdict, no score, and no recommendation**, because a "you two aren't
compatible" reading has ended relationships that were fine.

Readings are **layered**: one plain sentence → a personality sketch in everyday words →
seven life areas → a decade-by-decade timeline. Every term is glossed the first time it
appears.

**Daily fortune + journal**
Today's 流年/流月/流日 woven together with what you actually wrote in your journal:
a short read on the day's tone plus a gentle 宜/忌. No star ratings and no invented lucky
numbers: a colour or a number appears only as your chart's traditional 五行
correspondence, labelled as such. It logs the day for you if you want.

**Career fit**
A transparent 21-item interest check grounded in Holland/RIASEC, scored against **188
real O\*NET occupations** (CC BY 4.0). You get a **Low / Moderate / Strong** band and a
confidence note. Never a fake percentage. All 188 carry O\*NET 31.0 interest ratings
and **173** also carry Work Values, so adding a values ranking makes the match genuinely
data-weighted. `--find` maps what you *call* a job
("核磁共振技师", "high school teacher") to an actual occupation code, and labels anything
short of the job itself a weak neighbour, so a role the dataset doesn't hold ("MRI
reconstruction") never comes back as a match. For CVs and cover letters it hands off to
the `job-hunt` skill.

**Relationship reflection**
Attachment theory, Gottman and NVC used as a mirror: separate what happened from the
story about it, voice both sides, name the pattern, and give concrete moves (a repair
phrase, an NVC sentence, the question worth asking them). It tracks people across
incidents so a pattern rests on the actual record rather than on memory. One incident
is never a pattern. Safety comes first: coercive control or violence switches it into
safety mode, which never both-sides abuse and routes to real specialist help.

---

## Your data — where it lives, how to delete it

Everything personal sits in **`~/.companion/`** (`chmod 700`; on POSIX systems only you
can read it) and **is never uploaded anywhere**:

- `profile.yaml` — who you are · `consent.yaml` — what you allowed
- `journal/` — your entries (a monthly `.md` plus a machine-readable `index.jsonl`)
- `state/` — cached charts, working memory, per-person tracking

**Consent is per category and revocable.** Birth data, relationship details and mood
history are each granted separately. Without consent it isn't collected, inferred or
stored. Revoking is not deleting: the moment you say no, every script stops reading that
category, but the files stay and you are told what is still stored and how to delete it,
so a mistaken revoke loses nothing.

**Deletion is real, and it reaches every copy.** Just ask. It removes the matching
content from the journal, its index, the relationship log, the working memory and the
caches, not only the one obvious file (the tests search the whole folder afterwards):

| Say | Runs |
|---|---|
| "delete my birth data" | `companion.py forget --birth` |
| "forget June" | `companion.py forget --month 2026-06` |
| "delete what I just logged" | `companion.py forget --entry 2026-06-18 --nth 2` |
| "delete everything about him" | `companion.py forget --person Sam --with-entries` |
| "stop keeping relationship notes" | `companion.py forget --relationships` |
| "delete my mood scores" | `companion.py forget --mood` |
| "wipe everything" | `companion.py forget --all` |

Run like that, each one only lists what it would remove. Nothing goes until you confirm and it runs
again with `--yes`.

Every computation is **offline**. BaZi, charts and career matching make no network
calls, so your data never leaves the machine and nothing costs API credit.

**One exception, stated precisely:** the *first* run may reach the network to
`pip install` its four dependencies. That is a package download, not your data leaving
— but it is a network call, so it should not hide behind the word "offline". Set
`LIFE_COMPANION_NO_AUTOINSTALL=1` to forbid it and install them yourself; the scripts
then print the exact command instead of reaching out. After that, nothing this skill
does touches the network.

---

## Notes for anyone modifying it

```
SKILL.md              the router (always loaded)
AGENTS.md             entry point for non-Claude agents (Codex and friends)
references/           onboarding · profile-schema · journaling · continuity · forms
                      factcheck · voice · safety (always in force)
  modules/            destiny · daily-fortune · career · relationships
scripts/              companion.py · bazi.py · astro.py · ziwei.py · synastry.py
                      career_match.py · relationship_patterns.py · safety_scan.py
                      trends.py · form_server.py · selfcheck.py
                      _deps.py · _zh.py · _branches.py · _tz.py
data/content/         bazi-interpretation · bazi-life-arc · relationships
                      (the editable interpretation layer — real frameworks)
data/career/          occupations.json (188 real O*NET, CC BY 4.0) · assessment_items.json
data/zh/              OpenCC traditional→simplified table (Apache-2.0): the honesty gate and
                      the crisis scan fold traditional characters before matching
tools/                build_occupations.py: rebuilds data/career/occupations.json from the
                      O*NET databases (for maintainers; the skill never runs it)
                      run_agent_evals.py: runs evals/evals.json through codex, one throwaway
                      project and home each (for maintainers)
tests/                regression suite (plain unittest, fully offline)
```

**Dependencies** — `PyYAML`, `lunar-python` (MIT, BaZi), `pyswisseph` (Western charts),
`sxtwl` (BSD, the optional 立春 cross-check). Scripts try to `pip install` what's
missing; when that fails (no network, PEP 668 externally-managed Python) they print the
exact install command and what degrades without it instead of a traceback.
`python3 scripts/companion.py doctor` reports everything at once.

**Tests** — `python3 tests/test_scripts.py` (a few hundred cases, a minute or two, no network).
Also `python3 scripts/career_match.py --selftest` and `python3 scripts/ziwei.py --selftest`.

**Check a draft before sending it** —
`python3 scripts/selfcheck.py --module destiny --file draft.md`

Two independent checks in one command:

- **Honesty** (can block, exit 1): fabricated percentages and star ratings, fatalism
  including hedged forms like "大概率保不住", forecasts about a relative's health,
  almanac-style prohibitions, hiring predictions, clinical labels on an absent partner,
  **an invented crisis helpline number**, a missing disclaimer, unglossed 十神, a
  high-stakes external fact shipped without a dated source, and a reading being used to
  settle a real decision.
- **Voice** (never blocks): the wording tells that make a reply read like a filled-in
  form: "not X, but Y" as a reflex, stock phrases, em-dashes as the default connective,
  uniformly long sentences, no fragments at all, filler adverbs. See
  `references/voice.md`, which also covers writing plainly in either language.

**The interpretation content lives in `data/content/`** — to change the tone or add
detail, edit there; you don't need to touch the scripts.

**The honesty and safety floor is `references/safety.md`**, and it outranks every
module and any request to drop the framing.

---

## Licence

Code and prose: see [`LICENSE`](LICENSE). Occupation data is from the O\*NET Resource
Center (U.S. Department of Labor), used under **CC BY 4.0**; the attribution ships
inside `data/career/occupations.json` and must stay there.

---

*The computation is fact. The reading is a mirror. You're the one who decides.*
