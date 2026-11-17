# HTML forms — the nice way to collect input

For anything with several fields (onboarding, a birth block, the 21-item career
check), a styled local form beats asking one question at a time in chat. It's
clearer for the user, faster, and it writes straight to their private home.

`scripts/form_server.py` serves a small localhost page, opens the browser, and on
submit writes the result via `companion.py` (atomic + consent-gated) and drops a
`~/.companion/.form_result.json` marker. Nothing leaves the machine.

## When to use it
- **Onboarding** (first run): the default *where a browser and a background process are
  both easy*. The chat flow in `onboarding.md` is an equally supported path, not a
  consolation prize — take it whenever the form is awkward (a sandboxed harness, no
  browser, a remote session) or the user would rather just talk. Same tiers, same
  consent rules, same result.
- **Career assessment**: strongly preferred — 21 Likert items + a values ranking is
  painful in chat, pleasant in a form.
- Short, single-answer things (a mood, one birthday, a yes/no) stay in chat — a form
  is overkill.

## How to run it
Launch it **in the background**, tell the user to fill the page, then read the
result once they submit:

```bash
# onboarding (pre-fills anything already in the profile):
python3 "$D/scripts/form_server.py" --form onboarding &
# career assessment:
python3 "$D/scripts/form_server.py" --form career &
```
It prints `SERVING http://127.0.0.1:8760/ …` and opens the browser. On submit it
prints `SUBMITTED {...}`, writes the data, then **stops itself** and prints `DONE`.

**Read the `todo` list in that `SUBMITTED` payload.** A form can only collect what it
asked; `todo` names what it could *not* finish — an unresolved timezone, birth
coordinates still null (so no Ascendant/houses), a missing gender (so no 大运 direction).
Finish those in chat before the reading, or you'll hit the hole later and the person
will have to be asked twice.
Give the user the URL too, in case the browser didn't auto-open — and read the port
from the SERVING line rather than assuming 8760: if that port is busy it walks forward
to the next free one.

**It cleans up after itself**, which matters because no harness but Claude Code
reliably lets you kill a background job on a later turn:
- stops on submit (`DONE`),
- stops after `--timeout` seconds with nothing submitted (default 900; exit code 3,
  message `TIMEOUT`) — then just ask if they'd rather do it in chat,
- `--keep-alive` opts out if you really want it to persist,
- `--no-open` skips the browser launch (headless / remote sessions).

## Knowing they're done
Two signals — poll whichever is easy:
- `~/.companion/.form_result.json` appears/updates with `{"status": …}`.
- For onboarding: `companion.py status` flips `onboarding_complete:true`.
- For career: `companion.py cache --module career_intake` has a `latest` block with
  `answers` (0–4 per item id), `values_rank`, and the jobs. Score it with
  `career_match.py --score-intake` (bands only, no fake %; exit 3 means the answers carry
  no shape, so say "can't measure").

When the user says they've submitted (or the marker appears), read the profile /
intake, confirm warmly in one line, and continue with what they came for. The server
is already gone by then. If you ever need to stop one by hand: `pkill -f form_server.py`.

## Design note
The forms are meant to feel like a private ledger, not a survey: paper/lamplight
(follows the OS theme), 朱砂 as the one accent, 五行 dots as section marks, a
consent *lock* on the birth block, a 印章 stamp on save. If you extend them, keep
that restraint — one accent, lots of calm. The honesty line stays on every form:
*算出来的是事实，读出来的是镜子；数据只在你本机。*

## Adding a new form
Add a `render_<name>()` + `write_<name>()` pair in `form_server.py` and a
`--form <name>` branch. Reuse the shared CSS + `page()`/`eyebrow()`/`opt()` helpers
so it stays visually one family.
