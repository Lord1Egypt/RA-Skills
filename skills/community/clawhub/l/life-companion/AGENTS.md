# life-companion — agent entry point

This repository **is** a skill: a personal AI companion for one person, with four
lenses (八字/destiny charts, daily fortune & journaling, career fit, relationship
reflection) built on a private, on-device profile + journal.

**Read [`SKILL.md`](SKILL.md) first — it is the router and the operating procedure.**
Everything below is only what a harness needs in order to follow it correctly.

## Running it anywhere

Nothing here is Claude-specific. It needs **Python 3.9+**, a shell, and the ability to
read files. All computation is offline: no API keys, no network calls, no spend.

The one exception, stated rather than glossed: on FIRST run the scripts may
`pip install` their four dependencies, which is a network call (a package download, not
user data leaving). `LIFE_COMPANION_NO_AUTOINSTALL=1` forbids it and makes them print
the install command instead. Nothing after that touches the network.

```bash
D="$(dirname "$(realpath AGENTS.md)")"     # or wherever this repo is checked out
python3 "$D/scripts/companion.py" doctor   # python + dependencies + what degrades
python3 "$D/tests/test_scripts.py"         # regression suite (429 tests, ~70s, offline)
```

`doctor` names every missing package with its install command and what stops working
without it. Scripts try to `pip install` what they need; where that fails (no network,
PEP 668 externally-managed Python) they exit with that message rather than a traceback.
`LIFE_COMPANION_NO_AUTOINSTALL=1` disables the install attempt entirely.

Dependencies: `PyYAML`, `lunar-python` (BaZi), `pyswisseph` (Western charts — astro.py
only), `sxtwl` (optional 立春 cross-check).

**Windows:** use `python` or `py -3` in place of `python3`. `COMPANION_HOME` cannot be
`chmod 700` there, so don't repeat the "only you can read it" claim verbatim.

## Two things harnesses differ on

1. **The skill's own directory.** Some harnesses inject it; most don't. It is simply
   the folder containing `SKILL.md`. Resolve it once into `$D` and use it everywhere.

2. **Asking questions.** SKILL.md asks for *selectable options* rather than free-text
   questions in several places, and names `AskUserQuestion` (a Claude Code tool). If
   your harness has no equivalent, present the same options as a **numbered list** and
   ask the person to reply with numbers — do not fall back to open-ended prose. The
   21-item career interest check in particular is unusable as free text.

Two optional paths degrade cleanly if your harness can't do them:

- **HTML forms** (`scripts/form_server.py`) need a browser and a background process.
  If either is awkward, use the chat flow in `references/onboarding.md` — a fully
  supported equal path, same fields, same consent rules. The server stops itself on
  submit and after `--timeout` seconds, so it can't be orphaned.
- **Live web lookups.** `references/safety.md` §1 rule 6 requires verifying high-stakes
  external facts (visa, tax, licensing, an employer's current status) against a dated
  official source. With no web access you cannot ship such an answer: say you couldn't
  verify it and route the person to the source. Never answer those from memory.

## The line that must not be crossed

**Compute honestly, interpret humbly.** The charts are real, reproducible computation
— and where an engine has no independent cross-check (`ziwei.py`) or deliberately
withholds an answer (`synastry.py` emits no 合/不合), the payload says so and you repeat
it rather than smoothing it over;
every interpretation is labeled a reflective lens, never a prediction. No fabricated
numbers, no fatalism, no medical/financial/legal advice, and — most important — **never
an improvised crisis helpline number.** The canonical list is inline in SKILL.md and in
`references/safety.md` §2.

`scripts/selfcheck.py` is the deterministic backstop for all of that. Run it on your
draft before sending, and send the draft you checked (an edit after it passed has not been
checked):

```bash
python3 "$D/scripts/selfcheck.py" --module destiny --file draft.md   # exit 1 = blocker
```

It matches surface patterns, so passing it is necessary, not sufficient — the module
checklists in `references/modules/` still apply.

## Privacy

Everything personal lives in `COMPANION_HOME` (default `~/.companion`), outside this
repo, `chmod 700`, never transmitted. Consent is per-category (`birth`, `relationships`,
`mood`) and revocable. `companion.py forget …` first shows what it would remove, and really
deletes once it runs again with `--yes`. Never commit user data —
`.gitignore` has a defensive backstop, but the real rule is that it belongs outside.
