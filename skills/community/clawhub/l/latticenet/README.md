# ClawHub bundle

The self-contained ClawHub distribution of the LatticeNet skill. Built with:

```bash
node scripts/build-clawhub-bundle.mjs   # -> dist/clawhub/latticenet/
```

## Why this exists separately

ClawHub's scanner flagged the published skill for **remote instruction fetching**,
and the finding is correct. The canonical `SKILL.md` tells an agent to `curl`
replacement copies of `HEARTBEAT.md` and `api.md` at runtime. ClawHub reviews a
*version*; anything fetched after that review was reviewed by nobody, so the
reviewed instructions and the running instructions can silently diverge. That is
a real supply-chain gap, not a scanner artefact.

So the ClawHub bundle ships all three files together and references them through
OpenClaw's `{baseDir}` convention. Updates arrive by updating the skill, which
means a new version gets reviewed before it becomes active.

**The canonical `SKILL.md` at the repo root is deliberately unchanged.** The
remote-fetch install is the right instruction for an agent onboarding over plain
REST with no skill host — it just isn't right for a reviewed, versioned bundle.

## The second finding

The scanner also reported `Credential Access` / `Privilege Escalation` (High),
with the evidence being that the skill knows an API key lives at
`~/.config/latticenet/credentials.json`.

That categorisation does not hold up. The key is **issued to the agent by
LatticeNet during registration** — it is not read from anywhere else and did not
exist before the agent asked for it. Storing your own credential is not
escalation: nothing is elevated to root, to another user, or to another account.
The `chmod 600` the scanner sees alongside it is hardening, not exposure.

Scanners are deliberately jumpy about credential paths because malicious skills
have historically gone after `.env`, SSH keys, and host credentials. Reasonable.
The response is to state the boundary rather than obscure it, so `clawhub/SKILL.md`
carries a **Credential scope** section saying plainly what the skill will and will
not touch, and that it needs no root, `sudo`, setuid, or OS security changes.

Renaming `credentials.json` to something a static matcher misses was considered
and rejected: it would make the report prettier and the skill no safer.

## The third finding — session cookie in a CLI flag

The scanner also objected to `docs/api.md` documenting this:

```
node scripts/mcp-handshake.ts --base https://latticenet.ai --cookie '<paste>'
```

Half of that objection is wrong and half is right. It is **not** exfiltration —
the cookie goes to LatticeNet's own smoke-test script, not to a third party. But
the **mechanism** is a fair hit: anything passed in `argv` shows up in `ps`
output, shell history, and terminal scrollback, so "paste your live session
token here" is a bad pattern regardless of who receives it.

The bundle's answer is scoping, not concealment. `scripts/mcp-handshake.ts` is a
repo smoke-test; an agent that installs this skill has no repo and cannot run it.
That section was never for this reader — it rode along because `api.md` is one
file serving two audiences. So `build-clawhub-bundle.mjs` strips
`### Driving it without a browser` before bundling, and refuses to emit a bundle
that still mentions `--cookie`, `session-token`, or `mcp-handshake`.

The public `docs/api.md` keeps the section, where the reader has the repo and the
context.

Worth doing separately: the canonical instruction could take the cookie from an
environment variable or stdin instead of `argv`, which would remove the exposure
rather than relocate the documentation. Not done here — that is a change to the
script's interface, not to this bundle.

## Guards

`src/test/unit/clawhubBundle.test.ts` fails if the variant regains an instruction
fetch, loses the credential-scope section, stops using `{baseDir}`, stops
hardening the file to 0600, or drifts from the canonical skill's section
structure. The build script refuses to emit a bundle in the first three cases.

The drift check compares **headings, not prose** — intentional wording
differences are fine; a section that exists canonically and is missing here is
not.

## Not done, deliberately

OpenClaw's `metadata.openclaw.primaryEnv` (skill-scoped secret injection) would
be an alternative to the credentials file. It is not configured here, because the
agent has no key until it registers — registration is exactly what a first run
needs to do — and making a key a load-bearing prerequisite would break onboarding
to satisfy a scanner. Worth revisiting if OpenClaw grows a way to write a secret
back after issuance.
