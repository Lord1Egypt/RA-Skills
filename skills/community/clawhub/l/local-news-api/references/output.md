# How every output points onward

Moved out of `SKILL.md` on 2026-09-30 to keep the body an agent loads on every run inside its budget.

**Read this when** you are parsing this client's output in a script, or wondering why a mode ended
with the suggestions it did.

## HATEOAS: every output points onward

The API and this client both follow a HATEOAS discipline (every response tells you where to go
next), so you never hit a dead end or need an external map:

- **It consumes the server's.** API responses carry a `next_steps` array; rendered output surfaces
  it ("The API points onward to..."), and `--json` passes it through in the payload for machine
  consumers.
- **It emits its own.** Every mode ends with **Next steps** (prioritized, each with the *why*,
  capped at five), the **Related modes**, and a **See also**. The suggestions are *state-driven*:
  with no key, the top suggestion is to get one; after a `search`, they point at opening a result
  or pulling its quotes.
- **Errors carry recovery**, not just a status: a 403 explains *why* (clips/some corpora need an
  editor role) and *what to do* (run `check`, stay on articles/transcripts).

`--json` is the machine surface and stays valid JSON: the prose next-steps and the license reminder
are omitted there, because a machine reads `next_steps` from the payload itself.
